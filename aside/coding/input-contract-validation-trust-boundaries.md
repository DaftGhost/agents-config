## Input Contract Validation Trust Boundaries

### What

When implementing or reviewing input-processing paths, validate input contracts at trust boundaries and carry the validated state through controlled internal calls.

Input contracts cover presence, type, format, encoding, length, structure, and serialization shape. Business rules, functional prerequisites, state, and authorization remain with application services or domain rules; input validation does not establish these conditions.

### Why

Each independent entry point can receive invalid input. Repeating the same input checks at every internal layer obscures responsibility without covering an entry point that bypasses those layers. Explicit boundary owners and internal contract types make clear where trust is established, where it remains valid, and where it must be established again.

### How

1. **Identify entry points and boundaries.** Trace HTTP/API handlers, external callbacks, message consumers, scheduled or retry jobs, manual entry points, and startup callbacks. Assign a validation owner to each trigger's raw arguments, payload, task record, or configuration. Also identify cross-process calls, HTTP/RPC, message or file serialization, plugin calls, and reconstruction from independently mutable persisted payloads. Finish this step when every independent trigger and receiving boundary has an explicit validation point.

2. **Validate on every boundary invocation.** Have each owner establish input trust before passing received data into controlled processing. The validating constructor or factory in the next step can be the boundary's validation point; avoid checking the same contract both before and inside it. A previous trigger's successful validation does not establish trust for a later retry, callback, or reconstructed payload. Finish this step when every trigger validates its own received input and each new boundary validates the corresponding received contract.

3. **Make established guarantees explicit.** Define each internal method's input contract and ensure its callers establish the required guarantees. Pass ordinary parameters directly when their guarantees remain valid; wrapping every argument or call in a new DTO is unnecessary. When using an internal `Command`, `Value Object`, or normalized context to represent accepted input, make it immutable and enforce its contract through a controlled constructor or factory; a raw DTO carrying `validated=true` is insufficient. Finish this step when every internal parameter has an explicit contract and an identified caller or constructor that establishes it.

4. **Preserve trust and own transformations.** Within the same process and trust domain, lower layers may rely on established input guarantees that remain valid without repeating their checks, whether the input is an ordinary parameter or a contract object. When a producer assembles, maps, or transforms fields into a new lower-level parameter, it owns satisfaction of that parameter's declared contract. Establish the new guarantees in the producer's logic or, when constructing a contract object, its controlled constructor or factory. Fail fast with diagnostic context on an internal contract violation. Finish this step when each transformation has a contract owner and internal consumers rely only on guarantees that remain valid.

5. **Match the interface to its callers.** Use private or package visibility, or internal contract types, for methods confined to a controlled call chain. Treat any interface accepting raw external DTOs from uncontrolled callers as a boundary with its own validation owner. Finish this step when callers cannot enter a trusted path through an unvalidated raw-input interface.

Complete the implementation or review only when every independent trigger and new receiving boundary has a validation owner, controlled calls pass parameters with established guarantees without duplicate input checks, producers enforce transformed contracts, and internal contract violations fail fast with enough context to diagnose them. Keep business, state, and authorization checks with their application or domain owners.

### Example

Before: The HTTP handler, export service, and writer each validate the same raw request. A retry job calls the writer with a persisted task payload and bypasses the handler's checks.

After: The HTTP handler and retry job each validate their own received input and construct an immutable `ExportCommand`. The export service accepts that contract type and constructs a valid `WritePlan`; the writer accepts the plan without repeating the input checks. If work crosses a message boundary, the consumer validates the received payload and constructs a new internal command.

The pseudocode treats input validation as a boundary responsibility. Each independent trigger or receiving boundary performs it for its own input.

```text
ON EACH independent trigger or new receiving boundary:
    receive raw input
    validate its input contract
    if the contract is violated:
        reject the input
    otherwise:
        pass accepted input into controlled processing

DURING controlled processing within the same trust boundary:
    rely on the established input contract
    when transforming input into a new internal parameter:
        ensure the producer establishes the new contract
        if the internal contract is violated:
            fail fast with diagnostic context
    pass internal input to lower layers without repeating its validation
```

For an internal method, assume every caller is in the same trust domain and already guarantees that `baseName` and `extension` are present strings satisfying the required filename format. Both versions receive these ordinary parameters directly and produce the same filename. The method, parameters, callers, and formatting logic remain unchanged; only repeated input checks are removed.

```text
Before:
    PRIVATE METHOD formatExportFileName(baseName, extension):
        recheck the presence, type, and format of baseName and extension
        return baseName + "." + extension

After:
    PRIVATE METHOD formatExportFileName(baseName, extension):
        return baseName + "." + extension
```

The internal method relies on guarantees established by its callers. Private visibility alone does not establish those guarantees. If a caller receives raw input from outside this trust boundary, validate it at the receiving boundary before invoking the internal method.
