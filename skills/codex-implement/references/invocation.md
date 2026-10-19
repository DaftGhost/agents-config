# Codex Non-Interactive Invocation Reference

Verified against `codex-cli 0.163.0`. Check `codex exec --help` before relying on a flag that a newer or older CLI may not have.

## Initial run

```bash
codex exec - \
  -C "$REPO" \
  -m "$MODEL" \
  -c model_reasoning_effort="$EFFORT" \
  --approve-for-me \
  --json \
  -o "$RUN_DIR/last-message.md" \
  < "$RUN_DIR/brief.md" \
  > "$RUN_DIR/events.jsonl" \
  2> "$RUN_DIR/codex.log"
```

- `-` makes Codex read the prompt from stdin. This avoids shell quoting problems with newlines, quotes, and non-ASCII text.
- `-C` sets the working root. The process may also be started with that directory as its cwd; `scripts/run_codex.py` does both.
- `-m` selects the model. Omit it to use the configured default.
- `-c model_reasoning_effort="<level>"` sets reasoning effort. Supported levels depend on the model; the CLI accepts `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`. Use only a level the model documents, and treat `xhigh` and `max` as opt-in.
- `--approve-for-me` routes approval requests through automatic review and implies the workspace-write sandbox. It conflicts with `--sandbox`; do not pass both. If the CLI version has no `--approve-for-me`, use `-s workspace-write` and be prepared for approval behavior to differ.
- `--json` makes stdout a JSONL event stream. Progress and diagnostics go to stderr.
- `-o` writes the final agent message to a file. It is also present in the event stream.
- `--add-dir <DIR>` adds another writable directory to the initial run.
- `--output-schema <FILE>` can constrain the final message to a JSON Schema. Use it only when the caller needs structured output; it is not required for ordinary implementation work.
- `--ephemeral` avoids saving the session, but then `resume` is unavailable. Do not use it when the supervising agent may need a feedback loop.
- `--skip-git-repo-check` allows a non-Git directory. Use it only for read-only work or when no diff review is needed; implementation work should happen in a Git repository.

## Resume (feedback loop)

```bash
cd "$REPO"
codex exec resume "$THREAD_ID" \
  -m "$MODEL" \
  -c model_reasoning_effort="$EFFORT" \
  --json \
  -o "$RUN_DIR/resume-1/last-message.md" \
  - < "$RUN_DIR/feedback-1.md" \
  > "$RUN_DIR/resume-1/events.jsonl" \
  2> "$RUN_DIR/resume-1/codex.log"
```

`codex exec resume` accepts `-m`, `-c`, `--json`, `-o`, `--output-schema`, and `-`. It does **not** accept `-C`, `-s`, `--approve-for-me`, or `--add-dir`. Run it from the repository directory so the session continues in the same working root. Use the `thread_id` from the initial `thread.started` event; `--last` is available but is unsafe when other Codex sessions may be running.

## Event stream

Each line of `events.jsonl` is one JSON object. The useful types are:

| Event | Fields |
|---|---|
| `thread.started` | `thread_id` - save this for resume |
| `turn.started` | - |
| `item.started` / `item.completed` | `item.id`, `item.type`, and type-specific fields |
| `turn.completed` | `usage` with input/output/cached token counts |
| `turn.failed` | failure information |
| `error` | an error event |

Useful `item.type` values:

- `reasoning`: the model's reasoning text.
- `command_execution`: `command`, `aggregated_output`, `exit_code`, `status`. A failed command is visible here even when the overall turn succeeds.
- `file_change`: `changes` is a list of `{path, kind}` entries. This is the earliest reliable signal of what Codex edited.
- `agent_message`: the assistant's messages, including the final one.

The final answer is the last `agent_message`, and `-o` writes it to a file. Do not treat the presence of an `agent_message` as proof of success; inspect the exit code, `turn.failed`/`error` events, command exit codes, and the diff.

## Monitoring and timeouts

`codex exec` blocks until the turn finishes. For a long task, start it in the background and tail `events.jsonl`; the file is appended as the run proceeds. `scripts/run_codex.py --timeout <seconds>` terminates the process group on timeout and records `timed_out` in `summary.json`.

Do not run two Codex writers in the same working tree concurrently. Use separate worktrees or serialize the runs.

## Failure modes

- **`codex` not found**: report the PATH problem; do not substitute another agent silently.
- **Authentication or provider error**: report the tail of `codex.log`; do not silently switch providers.
- **Model rejected**: if the user chose it, report and ask. If the supervising agent chose it, retry with the configured default and state the change.
- **Approval or sandbox denial**: read the failing command in `events.jsonl` and the diagnostics in `codex.log`. Narrow the scope or adjust the sandbox only as the user's authorization allows.
- **`turn.failed` or nonzero exit**: report the error and the last meaningful event. Resume only when the failure looks transient or the feedback can be made concrete.
- **No Git repository**: Codex expects one. Ask, initialize a baseline in a temporary/eval workspace, or use `--skip-git-repo-check` for read-only work.
