## Logging Responsibility Boundaries

### What

When implementing or reviewing logging, assign responsibility by the event's meaning, outcome, and required context. The primary log belongs to the earliest boundary that can establish all three and owns the processing result. Caller, callee, and layer names alone do not determine responsibility.

Assign one primary responsibility point per event. Additional components record logs when they produce distinct events, such as a technical finding, retry decision, fallback, or final business outcome.

### Why

Repeated logs for the same event obscure where the outcome was determined and make one failure look like several. Missing business outcomes and premature success logs leave the workflow's actual state unclear. Explicit event owners and result contracts preserve both diagnostic causes and processing consequences.

### How

1. **Define events and owners.** Identify the technical findings, business outcomes, and orchestration decisions that need observation. For each event, choose the earliest component that can explain its meaning, determine its outcome, and supply the required identifiers. A call site qualifies only when it has that context. Lower components can own precise technical findings; business components can own consequences; orchestration can own path selection, retry, fallback, degradation, and workflow outcomes. Finish this step when every material event has one primary owner and each additional log has a distinct meaning.

2. **Use explicit processing results.** Base orchestration decisions on structured return values, error codes, or exception contracts. If a boolean hides several failure causes, replace it with a structured result or explicit error type. Keep lower-level logs as diagnostic evidence; do not parse them as an interface or reproduce the callee's decision logic just to write a log. Finish this step when the caller can determine the relevant outcome from the callee's declared result contract.

3. **Assign exception logs to handling outcomes.** The boundary that consumes, converts, retries, degrades, rolls back, or returns the final result owns the primary exception log. Catching and rethrowing alone does not establish ownership: preserve the cause for the boundary that decides how to handle it. Record the complete stack trace there without duplicating it at every layer. Finish this step when the exception's handling owner is explicit and other logs add distinct information rather than another copy of the same stack.

4. **Control retry logging.** For expected, recoverable attempts, use an appropriate lower severity or aggregate the observations. The retry owner records terminal failure after retry exhaustion. Retain retry count, cause, and final outcome in structured fields. Finish this step when intermediate attempts are distinguishable from terminal failure and exhaustion has a clear logging owner.

5. **Observe confirmed outcomes.** Tie each success log to the state transition actually confirmed. Distinguish start, external-call acceptance, local transaction commit, asynchronous message publication, consumer completion, and final business completion. External acceptance or publication alone does not establish final success. Assign an observability owner to important terminal failures; use metrics, traces, or aggregation for expected high-frequency outcomes when appropriate. Finish this step when event names and statuses match confirmed states and material outcomes remain observable.

6. **Provide structured, safe context.** Include applicable event code, outcome, business object identifier, request or task identifier, source or processing path, error type or code, status, quantity, duration, and retry count. Redact secrets, tokens, identity documents, full payment data, and other sensitive values in messages, fields, exception details, headers, and payloads. Apply the retention and access requirements of security audit events. Finish this step when records contain the context needed to explain their events without exposing sensitive values.

Complete the implementation or review only when material events have primary owners, additional logs add distinct meaning, callers use explicit results, exception stacks are not duplicated, retry and success records match confirmed outcomes, and each chosen observability mechanism carries appropriate structured and redacted context.

### Example

Context: A remote submission times out. The workflow retries it and records the final business outcome after retry exhaustion.

Before: The adapter, service, and workflow each log the same timeout with a complete stack trace. Every recoverable attempt is recorded as a terminal error, and the workflow receives only a boolean failure.

After: The adapter returns an explicit timeout outcome or propagates the exception cause. The retry owner observes recoverable attempts at lower severity or in aggregate, then logs retry exhaustion with the cause and any available exception stack once. The business workflow uses the explicit terminal result to record the distinct consequence that submission could not be confirmed, without repeating the exception stack. A timeout does not establish whether the remote system completed the submission.

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
