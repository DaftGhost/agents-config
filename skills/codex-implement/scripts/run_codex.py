#!/usr/bin/env python3
"""Run Codex non-interactively and record everything the supervising agent needs.

The task brief is fed on stdin, so it can contain quotes, newlines, and non-ASCII
text without shell escaping. Events are written as JSONL while the run proceeds,
which lets the caller tail progress instead of waiting for the final message.

Writes into --run-dir:
  events.jsonl       Codex JSONL event stream (live)
  codex.log          Codex progress and diagnostics
  last-message.md    Codex's final message
  command.json       Exact argv, cwd, model, effort, and resume target
  summary.json       Exit status, thread id, usage, commands, file changes, errors
"""

import argparse
import json
import os
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Repository or directory Codex should work in")
    parser.add_argument("--brief", required=True, help="File containing the task brief, passed on stdin")
    parser.add_argument("--run-dir", required=True, help="Directory for logs and the run record")
    parser.add_argument("--model", help="Codex model id; omit to use the configured default")
    parser.add_argument(
        "--effort",
        choices=["minimal", "low", "medium", "high", "xhigh", "max"],
        help="Reasoning effort; use only a level the chosen model supports",
    )
    parser.add_argument("--resume", metavar="SESSION_ID", help="Resume an existing Codex session")
    parser.add_argument(
        "--sandbox",
        choices=["read-only", "workspace-write", "danger-full-access"],
        help="Sandbox mode. Omit to use --approve-for-me (workspace-write with automatic review).",
    )
    parser.add_argument(
        "--no-approve-for-me",
        action="store_true",
        help="Do not pass --approve-for-me; useful only when approvals are already handled",
    )
    parser.add_argument("--add-dir", action="append", default=[], help="Extra writable directory (initial run only)")
    parser.add_argument("--timeout", type=int, default=0, help="Seconds before terminating the run; 0 means no limit")
    parser.add_argument(
        "codex_args",
        nargs=argparse.REMAINDER,
        help="Extra arguments after -- are passed to codex exec unchanged",
    )
    return parser.parse_args(argv)


def build_command(args):
    cmd = ["codex", "exec"]
    if args.resume:
        cmd += ["resume", args.resume]
    else:
        cmd += ["-C", str(Path(args.repo).resolve())]

    cmd += ["--json", "-o", str(Path(args.run_dir).resolve() / "last-message.md")]
    if args.model:
        cmd += ["-m", args.model]
    if args.effort:
        cmd += ["-c", f"model_reasoning_effort={args.effort}"]

    if args.resume:
        if args.sandbox or args.add_dir:
            print("warning: resume ignores --sandbox and --add-dir", file=sys.stderr)
    else:
        if args.sandbox:
            cmd += ["-s", args.sandbox]
        elif not args.no_approve_for_me:
            cmd += ["--approve-for-me"]
        for directory in args.add_dir:
            cmd += ["--add-dir", directory]

    extra = list(args.codex_args)
    if extra and extra[0] == "--":
        extra = extra[1:]
    cmd += extra
    cmd += ["-"]  # read the brief from stdin
    return cmd


def summarize(run_dir, exit_code, timed_out, duration, cmd, args):
    thread_id = None
    usage = None
    errors = []
    file_changes = []
    commands = []
    agent_messages = []

    events_path = Path(run_dir) / "events.jsonl"
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                errors.append({"type": "unparseable_event", "line": line[:500]})
                continue

            event_type = event.get("type")
            if event_type == "thread.started":
                thread_id = event.get("thread_id")
            elif event_type == "turn.completed":
                usage = event.get("usage")
            elif event_type in {"turn.failed", "error"}:
                errors.append(event)
            elif event_type == "item.completed":
                item = event.get("item", {})
                item_type = item.get("type")
                if item_type == "file_change":
                    file_changes.extend(item.get("changes", []))
                elif item_type == "command_execution":
                    commands.append(
                        {
                            "command": item.get("command"),
                            "exit_code": item.get("exit_code"),
                            "status": item.get("status"),
                        }
                    )
                elif item_type == "agent_message":
                    agent_messages.append(item.get("text", ""))

    return {
        "ok": exit_code == 0 and not timed_out and not any(e.get("type") == "turn.failed" for e in errors),
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_seconds": round(duration, 3),
        "thread_id": thread_id,
        "model": args.model,
        "effort": args.effort,
        "resume": args.resume,
        "repo": str(Path(args.repo).resolve()),
        "run_dir": str(Path(run_dir).resolve()),
        "command": cmd,
        "command_display": " ".join(shlex.quote(part) for part in cmd),
        "usage": usage,
        "file_changes": file_changes,
        "commands": commands,
        "agent_messages": agent_messages,
        "errors": errors,
        "last_message_path": str((Path(run_dir) / "last-message.md").resolve()),
        "events_path": str(events_path.resolve()),
        "log_path": str((Path(run_dir) / "codex.log").resolve()),
    }


def main(argv=None):
    args = parse_args(argv)
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    repo = Path(args.repo).resolve()
    brief = Path(args.brief)

    if not brief.is_file():
        print(f"error: brief not found: {brief}", file=sys.stderr)
        return 2
    if not repo.is_dir():
        print(f"error: repository not found: {repo}", file=sys.stderr)
        return 2

    cmd = build_command(args)
    command_record = {
        "argv": cmd,
        "argv_display": " ".join(shlex.quote(part) for part in cmd),
        "cwd": str(repo),
        "brief": str(Path(args.brief).resolve()),
        "model": args.model,
        "effort": args.effort,
        "resume": args.resume,
    }
    (run_dir / "command.json").write_text(
        json.dumps(command_record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    started = time.monotonic()
    timed_out = False
    try:
        with open(brief, "rb") as brief_file, open(run_dir / "events.jsonl", "wb") as events, open(
            run_dir / "codex.log", "wb"
        ) as log:
            process = subprocess.Popen(
                cmd,
                cwd=repo,
                stdin=brief_file,
                stdout=events,
                stderr=log,
                start_new_session=True,
            )
            try:
                exit_code = process.wait(timeout=args.timeout or None)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                exit_code = 124
    except FileNotFoundError:
        print("error: codex executable not found on PATH", file=sys.stderr)
        exit_code = 127
    except OSError as exc:
        print(f"error: could not start codex: {exc}", file=sys.stderr)
        exit_code = 126

    summary = summarize(run_dir, exit_code, timed_out, time.monotonic() - started, cmd, args)
    (run_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(
        f"codex run: {'ok' if summary['ok'] else 'not ok'}, exit={exit_code}, "
        f"{summary['duration_seconds']}s, thread={summary['thread_id'] or 'unknown'}"
    )
    print(f"run dir: {summary['run_dir']}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
