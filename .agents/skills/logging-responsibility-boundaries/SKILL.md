---
name: logging-responsibility-boundaries
description: Decide where logs, exception records, stack traces, retry attempts, and business outcomes belong in a code path, and review logging for duplication, missing outcomes, and unsafe context. Use this skill whenever adding or reviewing logging, exception handling, retry or fallback logic, observability, or error reporting, and whenever one failure produces several log entries or a success log is written before the outcome is confirmed. Apply it even when the user only asks for logs to be added or says the logs are noisy, and even when no one mentions responsibility.
disable-model-invocation: false
user-invocable: true
---

# Logging Responsibility Boundaries

A log is evidence about an event. One event should have one primary record, written by the component that can establish what happened and owns the processing result. Repeated records for the same event obscure where the outcome was determined and make one failure look like several; missing outcome records leave the workflow's actual state unknown.

## Decide Where a Log Belongs

For each material event, identify three things:

1. **Meaning** — what actually happened (technical finding, handling decision, business outcome).
2. **Outcome** — who determines what it means for the operation.
3. **Required context** — which identifiers and facts must accompany the record.

Assign the primary log to the earliest boundary that has all three and owns the processing result. Caller, callee, and layer names do not decide this. A call site qualifies only when it has the context; a lower component may own a precise technical finding; orchestration may own path selection, retry, fallback, degradation, and workflow outcomes.

Give every material event one primary owner. Other components log only when they produce a **distinct** event: a technical finding, a retry decision, a fallback, or a final business consequence.

| Event | Typical primary owner |
| --- | --- |
| Technical finding (timeout, malformed response, connection loss) | The component that detects it, where the precise location and data are available |
| Exception handling outcome | The boundary that consumes, converts, retries, degrades, rolls back, or returns the final result |
| Path selection, retry, fallback, degradation, workflow outcome | Orchestration |
| Business consequence | The business workflow or service that determines it |
| Confirmed success | The boundary that confirms the state transition, not the one that merely sent or accepted a request |

## Procedure

1. **Define events and owners before writing logs.** List the technical findings, business outcomes, and orchestration decisions that need observation. Choose one primary owner per event and an explicit reason for its placement. Finish when every material event has one owner and every additional log has a distinct meaning.

2. **Use explicit processing results.** Base orchestration decisions on structured return values, error codes, or exception contracts. If a boolean hides several causes, replace it with a structured result or explicit error types. Keep lower-level logs as diagnostic evidence; never parse them as an interface or reproduce the callee's decision logic just to write a log. Finish when the caller can determine the relevant outcome from the callee's declared contract.

3. **Assign exception logs to handling outcomes.** The boundary that consumes, converts, retries, degrades, rolls back, or returns the final result owns the primary exception record. Catching and rethrowing alone does not establish ownership; preserve the cause for the boundary that decides how to handle it. Record the complete stack once there. Finish when the handling owner is explicit and other records add distinct information instead of another copy of the stack.

4. **Control retry logging.** Record expected, recoverable attempts at an appropriate lower severity or in aggregate. The retry owner records terminal failure after exhaustion, with retry count, cause, and final outcome in structured fields. Finish when intermediate attempts are distinguishable from terminal failure and exhaustion has a clear owner.

5. **Observe confirmed outcomes.** Tie each success record to the state transition actually confirmed. Distinguish start, external-call acceptance, local transaction commit, asynchronous publication, consumer completion, and final business completion. External acceptance or publication alone is not final success. Record important terminal failures, including unconfirmed outcomes, and use metrics, traces, or aggregation for expected high-frequency events where appropriate. Finish when event names and statuses match confirmed states.

6. **Provide structured, safe context.** Include applicable event code, outcome, business object identifier, request or task identifier, source or processing path, error type or code, status, quantity, duration, and retry count. Redact secrets, tokens, identity documents, full payment data, and other sensitive values from messages, fields, exception details, headers, and payloads. Apply the retention and access requirements of security audit events. Finish when records explain their events without exposing sensitive values.

## Review Mode

When reviewing existing logging, look for these failure modes in order:

- The same failure is logged with a full stack at more than one layer.
- A caller decides retry, fallback, or business behavior from a boolean or by reading log text.
- Every recoverable retry attempt is logged as a terminal error, or exhaustion has no record.
- Success is logged when a request was sent or accepted, not when the outcome was confirmed.
- Errors are logged without identifiers, outcome, or error type, or with sensitive values in headers or payloads.
- A layer logs only to "be safe" while adding no distinct meaning.

Name the owner for each event and say what the other layers should stop logging. Do not ask for logging at every layer as a substitute for an explicit result contract.

## Implementation Mode

Add records at the owners identified above, not between layers. Prefer changing the result contract over adding a log that the caller must interpret. When editing existing code, keep behavior unchanged except for logging, and match the project's logging conventions and field names.

## Example: Submission Timeout With Retries

The adapter, service, and workflow each log the same timeout with a full stack, every recoverable attempt is a terminal error, and the workflow receives only a boolean. The result is three identical stacks, a misleading severity, and no clear record of the business outcome.

```text
WHEN the lower-level operation times out:
    return an explicit timeout outcome or propagate its exception cause

AT the retry owner:
    if the failure is recoverable and retries remain:
        observe the attempt at lower severity or in aggregate
        retain the cause and attempt count
        retry according to the policy
    if retries are exhausted:
        record retry exhaustion with structured context
        include the exception stack once, if an exception is available
        pass the explicit terminal result to the business workflow

AT the business workflow:
    determine the business outcome from the explicit result
    record that submission could not be confirmed after retry exhaustion
    retain correlation identifiers without repeating the exception stack
```

A timeout does not establish whether the remote system completed the submission; the business record must say "unconfirmed", not "failed" or "succeeded".

## Before Finishing

Check that:

- every material event has one primary owner, and each additional record has distinct meaning;
- callers determine outcomes from declared results, not from booleans or log text;
- the exception stack appears once, at the handling owner;
- intermediate retry attempts are distinguishable from terminal failure;
- success records match confirmed state transitions, and unconfirmed outcomes are observable;
- records carry the needed structured context and no sensitive values.
