# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## 5. Input Contract Validation Trust Boundaries

Use input-contract validation to establish and carry trust through controlled call chains. Input contracts cover presence, type, format, encoding, length, structure, and serialization shape. Business rules, functional prerequisites, state, and authorization remain with application services or domain rules.

- **Root triggers establish trust:** HTTP/API handlers, external callbacks, message consumers, scheduled or retry jobs, manual entry points, and startup callbacks validate their received raw arguments, payloads, task records, or configuration on every trigger. Each independent trigger has an explicit validation point.
- **Represent validated input explicitly:** After validation, convert the input to an immutable internal `Command`, `Value Object`, or normalized context. Controlled internal calls pass these internal contract types. The type, constructor, or factory expresses the validated state; a `validated=true` marker does not.
- **Propagate trust within the boundary:** Within the same process and trust domain, when a value is created through a controlled constructor or factory and has not passed through external input, serialization, or uncontrolled reconstruction, the caller guarantees the lower-level contract. The lower layer may rely on that contract without repeating the same input checks.
- **Make producers own new contracts:** When an upper layer assembles, maps, or transforms fields into a lower-level parameter, the upper layer ensures that the new object satisfies the lower layer's declared input contract before calling it. An invalid internal object is an implementation defect and fails fast with diagnostic context.
- **Revalidate at new boundaries:** Cross-process calls, HTTP/RPC, message or file serialization, plugin calls, external callbacks, and reconstruction from independently mutable persisted payloads establish a new input trust boundary. The receiving side validates the corresponding contract again.
- **Match visibility to trust:** Methods used only by a controlled call chain should use `private`, package visibility, or internal contract types where practical. A method with an uncontrolled caller range that accepts a raw external DTO is an input boundary and owns its validation.
- **Completion criteria:** An implementation or review is complete only when every root trigger has an explicit validation owner, validated values use internal contract types, controlled lower layers have no duplicate input checks, every new boundary has corresponding validation, and illegal internal objects fail fast with enough context to diagnose the contract violation.

## 6. Logging Responsibility Boundaries

Assign logging responsibility by event semantics and available context, not mechanically by caller, callee, or code layer. For each defined technical or business event, the primary log belongs to the earliest boundary that can determine the event's meaning, outcome, and required context. Later components add logs only when they produce a new semantic event.

- **Assign one primary responsibility point:** Choose the component that can explain the event, owns the relevant processing result, and has the required business identifiers. The actual call site is the responsibility point only when it has this information. A lower component may record a technical cause while an upper component records a retry, fallback, or final business result when those are separate events.
- **Separate technical and business meaning:** Lower components record technical failures or data findings that they can identify precisely. Business components record the business consequence and result. Orchestration components record path selection, retry, fallback, degradation, and final workflow outcome. Each log must add distinct meaning rather than repeat the same error.
- **Keep orchestration dependent on explicit results:** An orchestration component uses a structured return value, error code, or exception contract from the callee to determine the business outcome. A lower layer's log is supplementary diagnostic information and is not an interface for upper-layer decisions. Orchestration code does not reproduce lower-layer decision logic merely to produce a log.
- **Log handled exceptions at the handling boundary:** Catching an exception alone does not establish logging responsibility. The boundary that consumes, converts, retries, degrades, rolls back, or returns the final result owns the primary exception log. If a layer only rethrows the exception, the layer that determines the handling outcome records the complete stack trace. The same exception is not logged with a complete stack trace at every layer.
- **Control retry logging:** Intermediate retry attempts use an appropriate lower severity or an aggregated record when the attempt is expected and recoverable. The retry owner records the terminal failure after retry exhaustion. Retry count, cause, and final outcome remain available in structured fields.
- **Log confirmed state transitions:** Record success only after the corresponding success boundary is confirmed. Distinguish start, external-call acceptance, local transaction commit, asynchronous message publication, consumer completion, and final business completion. A successful external call or message publication does not by itself prove final business success.
- **Make material outcomes observable:** Important terminal failures have a clear observability owner. Expected high-frequency outcomes may use metrics, traces, or aggregation instead of an individual error log. A boolean result that hides multiple failure causes should become a structured result or explicit error type before logging responsibility is assigned.
- **Use structured and safe context:** Include applicable fields such as event code, outcome, business object identifier, request or task identifier, source or processing path, error type or code, status, quantity, duration, and retry count. Redact secrets, tokens, identity documents, full payment data, and other sensitive values in messages, fields, exception details, request headers, and payloads. Security audit events follow their retention and access requirements.
- **Completion criteria:** An implementation or review is complete only when each material event has one primary logging responsibility point, additional logs represent distinct semantic events, exception stacks are not duplicated, success is logged after the correct boundary, upper layers use explicit results, expected outcomes have suitable observability, and applicable context is structured and redacted.

## 7. Define and Work Within Capability Boundaries

Every program is a bounded system. Before implementation, define the strongest truthful contract it can fulfill by analyzing the requested outcome, its feasibility, the operating conditions, and what the program can control or verify. A request does not implicitly require a perfect system that handles every conceivable case or guarantees outcomes beyond its boundary.

- **Define the promised outcome:** Identify the useful result and supported cases. State adjacent or end-to-end outcomes that the program will not claim.
- **Establish feasibility:** Distinguish achievable, conditional, uncertain, and infeasible parts against known computational, physical, technical, and resource constraints. A limit on the end-to-end guarantee does not invalidate a useful part that the program can deliver.
- **Bound the operating envelope:** Record the inputs, states, workloads, dependencies, failure modes, and measurable limits that materially affect the promise. Ground quantitative targets in available evidence and resources.
- **Locate the control and evidence boundary:** Separate actions and facts the program can control or verify from outcomes that depend on another system, person, environment, or later step. Names, return values, statuses, logs, and success conditions describe confirmed facts rather than unverified external completion.
- **Work to the boundary:** Complete the useful behavior inside the boundary and make the supported paths correct, testable, observable, and maintainable. State residual uncertainty instead of implying control the program does not have.
- **Preserve continuation:** When work may continue beyond the boundary, retain enough explicit state and context for the appropriate retry, reconciliation, callback, or manual intervention.
- **Expand deliberately:** Extend the boundary only when a concrete requirement, observed failure, or measured risk justifies the additional behavior and complexity.
- **Completion criteria:** An implementation or review is complete only when the promised outcome is feasible within stated conditions, every claim is backed by observable evidence, the strongest useful behavior within the boundary is implemented, residual uncertainty is explicit, and a continuation path exists where the workflow requires one.

## Git Conventions

### Commit Messages

- The commit subject must accurately summarize the change and use the `<type>(<scope>): <summary>` format. For example: `refactor(channelcore): remove the Fliggy order-list search endpoint`.
- Code commits must include a body, except for pure formatting changes or single-file spelling corrections. The body must state the reason for the change, the main areas changed, and the affected modules or features.
- The body must record the validation commands actually run and their results, such as test and failure counts or the build result. Do not report tests that were not run as passing.
- State any known limitations, unresolved issues, or related changes intentionally left out in the body so the commit message does not hide remaining risks.
- Each commit must contain only changes related to one task. Do not include unrelated files or unauthorized working-tree changes.

### Branches

The target branch is the integration branch designated by the user or repository conventions.

- For a large change, create a feature branch from the target branch, develop on that branch, complete review, and then merge it back into the target branch. Do not commit directly to the target branch for a large change.
- A clearly scoped bug fix may be changed and committed directly on the target branch. If the fix grows into a large refactor, create a new branch.

### Merging

- By default, integrate branches with a squash merge by running `git merge --squash <source-branch>` from the target branch. Follow the user's explicit request to retain a merge commit, use a regular merge, or use another integration method.
- A squash merge does not create a merge commit automatically. After confirming the staged content and validation results, create one commit on the target branch. Keep the `<type>(<scope>): <summary>` subject format and append `(squash from <source-branch>)` to identify the source branch. For example: `feat(channelcore): add a Fliggy order adapter (squash from codex/fliggy-order)`.
- Before committing a squash merge, inspect `git diff --cached`, `git diff --cached --check`, and the staged file list. Confirm that the staged changes are limited to the merge scope. The commit body must follow the commit-message rules and record the validation actually run.

#### Conflict Resolution

These rules apply to Git integration operations that can produce conflicts, including `git merge`, `git rebase`, and `git cherry-pick`:

1. **Stop and inventory conflicts immediately:** Preserve the conflict state and assign a number to each conflicted file. Record the current branch and the branch being integrated (or the commit being cherry-picked). Describe the concrete changes from both sides and whether each side added new files. By default, handle test code together with its related business code instead of listing it separately. Call out independent changes, cases that cannot be determined, and validation failures separately. Do not discuss the conflicting files' commit versions, common ancestor, or history.
2. **Confirm choices before resolving conflicts:** For each numbered file, describe the conflict region, both sides' content, and the impact. Ask the user whether to keep one side or combine them. The user only needs to choose; they do not need to edit conflict markers or stage files.
3. **Resolve and continue according to the confirmed choices:** Edit only the confirmed regions, remove their conflict markers, run `git add`, and report the result. Leave any unconfirmed region unresolved. After all conflicts are resolved, the agent may run checks, continue with `merge --continue`, `rebase --continue`, or `cherry-pick --continue`, or commit.
