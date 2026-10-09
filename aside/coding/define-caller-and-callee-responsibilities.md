## Define Caller and Callee Responsibilities

### What

When designing, changing, or reviewing a function, explicitly determine what its caller must do and what its callee must do before implementing the affected behavior. Ground each assignment in the function's purpose, actual callers, available context, and control over the operation. Be able to explain why each responsibility belongs there.

### Why

An unexplained division of work leaves callers guessing about prerequisites, duplicates decisions across functions, and leaves failures or resource lifetimes without an owner. A deliberate division makes the function's contract usable and its design reviewable.

### How

1. **Inspect the call relationship.** Identify the function's intended outcome, its existing or intended callers, and the operations it delegates. Trace the context and decisions each participant owns. Finish when the affected call paths and the information available on each side are identified; record any callers that cannot be inspected.

2. **Assign responsibilities with reasons.** For each relevant decision or operation, identify its owner: preparing inputs, applying policy, enforcing invariants, producing side effects, managing resources or transactions, and handling results or failures. Choose the owner with the required knowledge and control. Compare caller ownership with callee ownership where either is viable, considering repeated work across callers and dependencies introduced into the callee. A caller often owns workflow choices and a callee often owns the operation it promises, but establish the assignment from the actual contract. Finish when every relevant responsibility has an owner and an evidence-based reason for its placement.

3. **Express the agreement in the interface.** Make clear what the caller must establish before the call, what the callee guarantees, which side owns supplied resources and side effects, and what results or failures the caller must handle. Use names, parameter and result types, and visibility to express the contract; document reasons and obligations that these cannot convey. Keep the explanation proportional to the function. Finish when a caller can use the function correctly without reconstructing its implementation.

4. **Verify both sides.** Check that each affected caller fulfills its obligations and handles the declared outcomes, and that the callee delivers its guarantees under those conditions. Check success and failure paths for duplicated decisions, missing work, and conflicting ownership. Use focused tests where behavior requires verification. Finish when the inspected paths agree with the contract and any verification gaps are explicit.

For input-validation assignments, apply [Input Contract Validation Trust Boundaries](input-contract-validation-trust-boundaries.md). For logging assignments, apply [Logging Responsibility Boundaries](logging-responsibility-boundaries.md).

Complete the design or review when the caller's obligations, the callee's guarantees, and the reasons for their division are explicit and supported by the affected call paths. Resolve any missing context needed to assign a responsibility before implementing that part.

### Example

Context: A workflow exports selected records as CSV to a stream it opens and closes. The workflow knows the selection policy and destination; the CSV writer knows the serialization format.

```text
CALLER:
    select records according to the export policy
    open the destination stream
    call writeCsv(records, stream)
    handle completion or a write failure
    close the stream on both success and failure

CALLEE writeCsv(records, stream):
    serialize records using the declared CSV format
    write to the supplied stream, leaving it open
    propagate write failures to the caller
```

The caller owns selection and the stream lifetime because they belong to its workflow. The callee owns CSV serialization and writing because those define its promised operation. Its contract leaves the supplied stream open and allows partial output on a write failure; the caller owns the decision about that partial output.
