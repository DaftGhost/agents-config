## Request Required Permissions and Continue

### What

When a Bash command or tool call required by the task is blocked by sandbox or agent permissions, obtain the required execution permission through the environment's available approval mechanism, retry the operation, verify its effect, and continue the task. Use an allowed escalation path before treating the initial restriction as a terminal blocker.

### Why

A restricted execution attempt can fail even when the environment permits the same operation after approval. Stopping at that failure leaves authorized work unfinished. Diagnosing the restriction serves the next recovery action; describing its cause alone does not restore task progress.

### How

#### 1. Identify the Required Recovery Action

Inspect the tool response, exit status, and relevant diagnostics. Distinguish a normal command or application result from a sandbox restriction or an agent permission restriction. For example, `rg` returning status 1 means no matches and requires no escalation. A generic “permission denied” message alone does not identify the boundary; use a narrow permitted diagnostic when necessary.

Limit diagnosis to the evidence needed to select the next action. Handle normal command results through the task's ordinary workflow; for permission restrictions, proceed to the approval step.

Complete this step when the evidence supports a concrete recovery action.

#### 2. Request the Required Permission

Check the current environment's escalation rules and approval mechanism. If escalation is allowed and the operation is within the user's authorized task, submit the request to execute that specific operation with the required permission or outside the sandbox.

State the operation, required access, reason, and material effects. Redact secrets and request only the additional permission needed. Use the environment's approval flow; do not substitute `sudo` or another tool for that mechanism.

Submit the request rather than merely describing the restriction, directing the user to run the command, or ending the task. Execute only after the required permission is granted. If escalation is unavailable, prohibited, or rejected, follow the remaining-path procedure below.

Complete this step when permission has been granted for the specific operation, or the restriction or rejection has been identified for permitted follow-up. Submitting a request alone does not authorize execution.

#### 3. Retry, Verify, and Resume

Before retrying an operation that could duplicate a write or external action, check whether the first attempt had partial effects. Retry with the approved access and account for any partial completion.

Inspect the retry's result and verify the intended effect. If it succeeds, resume the remaining task. If it fails, use the new diagnostics to choose the next permitted recovery action.

Complete recovery when the required operation has run with permitted access, its effect has been verified, and task execution has resumed. Approval, dispatch, and successful execution are intermediate steps; completion of the overall task depends on its actual success criteria.

#### 4. Exhaust Permitted Paths Before Reporting a Blocker

When escalation is unavailable, prohibited, or rejected, follow any permitted review or alternative execution path and continue unaffected work. Respect explicit denials: do not bypass them through another tool or repeat the same rejected request without new evidence or authorization.

Report an unresolved blocker only after applicable permitted recovery paths are unavailable or exhausted. Identify the specific operation, the restriction, the recovery paths attempted or unavailable, and the required user intervention.

Complete this branch when no applicable permitted recovery path remains, the precise blocker has been reported, and unaffected work has been continued. Keep the blocked operation explicitly unresolved.

### Example

A task requires reading a configuration file. The read is denied by the sandbox, and the environment permits requesting approval for that read:

```text
Before:
    attempt to read the required configuration file
    receive a sandbox denial
    report that the task cannot continue and stop

After:
    attempt to read the same configuration file
    receive the same sandbox denial
    confirm that the authorized read has an allowed approval path
    request permission for that read through the environment's approval mechanism
    once permission is granted, retry the read with approved access
    verify that the required content was obtained completely
    use the configuration to continue the task
```
