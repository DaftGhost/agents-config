---
name: codex-implement
description: >-
  Use this skill whenever the user names Codex (Codex CLI, `codex exec`, a `gpt-5.x-codex` model) as the agent that should perform a coding task. This covers any phrasing — delegating, assigning, or directly commanding: "delegate to codex", "let codex fix this", "用 codex 实现", "让 codex 去改", "用 codex 补上", "交给 codex" — even a single clause inside a larger or multi-step request. The coding action may be any implementation verb: implement, fix, debug, refactor, migrate, add, update, rewrite, or complete a feature or module. Also use it when a Codex model or reasoning effort (e.g. "gpt-5.1-codex", "sonnet 级别", "思考深度 high", "effort medium") is specified for such work. The current agent plans the brief, runs Codex as a supervised subagent, verifies the diff and tests, and reports back. Do not use for review-only requests, explanation, translation, documentation or config examples, planning without implementation, or requests for this agent to edit the files itself.
disable-model-invocation: false
user-invocable: true
---

# Codex Implement

Codex does the editing; you own the task. The user sees your report, not Codex's transcript, so you decide what Codex is asked to do, how much model and reasoning it gets, whether it is making progress, whether its result actually works, and what the user is told.

`codex exec` is non-interactive: Codex cannot ask you a question mid-run. Every ambiguity that matters must be settled in the brief before launch, or the run will silently choose for you.

## Workflow

1. **Confirm the task is implementation.** If the user only wants a review, an explanation, or a plan, do not launch Codex. If the request is ambiguous about scope or a product rule, settle it with the user first; Codex cannot do that for you.

2. **Inspect before delegating.** Read the files the change touches, the tests, the README, and `git status --short`. Find the project's real validation commands: the interpreter that actually exists, the test runner, and any build or lint step. Do not assume `python` exists or that a test command is configured. You need enough context to write acceptance criteria and to judge Codex's diff later. Do not delegate the investigation itself unless the user asked for that.

3. **Set the execution boundary.** Use the repository the user named. Check whether it is a Git repository: Codex expects one, and you need the diff. If it is not a repository, ask before initializing one, or work in a temporary copy. Record any pre-existing uncommitted changes so you can tell Codex's work apart from the user's.

4. **Choose the model and reasoning effort.** The user's explicit choice wins. Parse phrases such as "模型用 X", "思考深度 high", "use model X at high effort"; if only one is given, decide the other. When the user leaves both to you, decide deliberately and say why:
   - Read `${CODEX_HOME:-$HOME/.codex}/config.toml` for the configured `model` and `model_reasoning_effort`. Those are the settings known to work in this environment.
   - Small, contained change with clear tests: the configured model at `low` or `medium` effort.
   - Normal feature or bug fix across a few files: the configured model at `medium` or `high` effort.
   - Cross-module change, migration, ambiguous behavior, or hard debugging: the strongest model the environment documents, at `high`; use `xhigh` or `max` only when that model supports it.
   - Use only a model id that appears in the user's request, the Codex config, or a documented model catalog. Never invent one. If a chosen model is rejected, report it and retry with the configured default rather than guessing another id.
   - Record the choice and the reason; the final report must state both.

5. **Write the task brief.** Read [references/brief-template.md](references/brief-template.md) and write the brief to a file in the run directory. Make it self-contained: Codex does not see this conversation. Include the objective, acceptance criteria, allowed and forbidden scope, relevant context, the exact validation commands that exist in this environment, and the required final response. State the constraints that matter: do not commit, do not change unrelated files, do not install dependencies unless allowed, ignore unrelated skills and plugins, and stop and report rather than inventing a missing product rule.

6. **Run Codex with recorded output.** Use [scripts/run_codex.py](scripts/run_codex.py), resolving it relative to this SKILL.md (not the current working directory):

   ```bash
   RUN_DIR="${TMPDIR:-/tmp}/codex-implement/$(date +%Y%m%d-%H%M%S)-$$"
   mkdir -p "$RUN_DIR"
   python3 <skill-dir>/scripts/run_codex.py \
     --repo "$REPO" \
     --brief "$RUN_DIR/brief.md" \
     --run-dir "$RUN_DIR" \
     --model "$MODEL" \
     --effort "$EFFORT"
   ```

   The helper feeds the brief on stdin, passes `--json`, captures the event stream and final message, and writes `command.json` and `summary.json` with the thread id, usage, commands, file changes, and errors. It defaults to `--approve-for-me`, which implies workspace-write; do not combine it with `--sandbox`. Read [references/invocation.md](references/invocation.md) for the exact flags, event fields, resume form, and failure modes.

   Set a timeout proportionate to the task (for example 10-20 minutes for a small change) so a stuck run cannot block indefinitely. For a long run, start the helper in the background and tail `events.jsonl` as it grows. Do not run two Codex writers in the same working tree at the same time; serialize them or use separate worktrees.

7. **Monitor while it runs.** Watch for file changes, failing commands, repeated loops, and `turn.failed` or `error` events. If Codex is blocked, looping, or heading outside the brief, stop it and report rather than waiting for a bad result. You are the supervisor, not a message relay.

8. **Verify independently.** After the run, read `summary.json`, `last-message.md`, and the diff. Then:
   - Run the project's tests, build, and lint yourself. Do not report Codex's claimed results without running them.
   - Check each acceptance criterion against actual behavior.
   - Check scope: unexpected files, deleted files, lockfile churn, generated artifacts, debug prints, secrets, and unrelated formatting.
   - If Codex changed a file outside the brief, keep it only when the brief allowed that file and the change is a correct, low-risk consequence; list it explicitly in the report. Otherwise revert that file before reporting, or ask the user when the change might be intentional.
   - Confirm no commit, push, or history rewrite happened unless the user asked for one.
   - Treat a green test suite as necessary but not sufficient: read the diff for behavior the tests do not cover.

9. **Feed back through the same session when needed.** If the result is incomplete or a check fails, resume the same Codex session with evidence, not a vague retry:

   ```bash
   python3 <skill-dir>/scripts/run_codex.py \
     --repo "$REPO" \
     --brief "$RUN_DIR/feedback-1.md" \
     --run-dir "$RUN_DIR/resume-1" \
     --resume "$THREAD_ID" \
     --model "$MODEL" \
     --effort "$EFFORT"
   ```

   The feedback brief should quote the failing command and output, state what must change, and restate what must not change. Limit yourself to a small number of resume attempts; if Codex still cannot finish, stop and report the failure with the evidence. If the blocker is environmental or a missing product decision, handle it yourself or ask the user instead of asking Codex again.

10. **Report in the user's language.** Use this structure unless the user asked for something else:

    ```markdown
    ## Result
    <done | partially done | blocked> - <one line>

    ## Changes
    - `<file>`: <what changed>

    ## Validation
    - `<command>`: <result>

    ## Codex run
    - Model: `<model or configured default>`; effort: `<effort>`
    - Session: `<thread_id>`; record: `<run dir>`
    - Iterations: <n>

    ## Open items
    - <none, or unresolved issues and risks>
    ```

    Report what the diff and the checks show. Do not paste Codex's transcript or claim completion that the validation did not establish.

## Safety and failure handling

- Keep the default sandbox (`--approve-for-me`). Do not use `--dangerously-bypass-approvals-and-sandbox` or `danger-full-access` without explicit user authorization in an isolated environment.
- Never let Codex commit, push, or rewrite history unless the user asked. If it did, report it; do not rewrite history to hide it.
- Never run `git reset --hard`, `git checkout -- .`, or equivalent to clean up Codex's changes. If the diff includes unrelated edits, isolate or revert only the specific files, and only when the baseline is clean and you are sure the changes are Codex's.
- If Codex is not installed, not authenticated, or the provider fails, report the actual error and stop. Do not silently substitute another agent.
- If a user-specified model is unavailable, report it. If a model you chose is unavailable, retry with the configured default and say so in the report.
- If the user asks for changes in a non-Git directory, decide with them whether to initialize a repository or use a temporary copy. Do not use `--skip-git-repo-check` for implementation work that you will need to review as a diff.

## Done

- Codex ran through `codex exec` with a recorded model, effort, thread id, and run directory.
- The main agent independently verified the acceptance criteria and scope.
- The report states changes, validation evidence, model/effort, session, and open items.
- No unrelated changes, commits, or history rewrites were introduced.
