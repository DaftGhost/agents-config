## Use Strong Types in Code Design

### What

When designing, implementing, or reviewing code, express known data structures, domain distinctions, and supported states through concrete types. Use the project's language and type system to detect invalid combinations and incorrect calls as early as they can be checked.

### Why

Generic objects, string-keyed bags, and interchangeable primitive values leave known contracts implicit. Concrete types make those contracts visible to callers and let compilers or static analyzers detect errors before execution. Type declarations alone do not establish runtime validity or business correctness.

### How

1. **Identify the distinctions that matter.** Inspect the affected interfaces and callers for fixed structures, values with different meanings but the same primitive representation, finite states, optional values, and alternative outcomes. Reuse existing types when they express the required contract. Keep ordinary primitives when their meaning is unambiguous; introduce a type when it enforces a concrete distinction or invariant. Finish when each proposed type has an identified guarantee and affected callers.

2. **Use concrete structures and generic parameters.** Represent known fields with records, structs, classes, or equivalent typed structures, and declare collection element, key, and value types. Use maps for genuinely dynamic keys. Keep unavoidable dynamic data at the interface that requires it, then narrow it into the known internal contract. Finish when callers can access known fields and collection elements without unchecked casts or implicit shape assumptions.

3. **Encode domain distinctions and valid states.** Use distinct types for identifiers, units, or values whose interchange would be incorrect. Choose a representation that the language actually treats as distinct; an alias that remains interchangeable provides naming only. Model finite choices with enums or literal unions, and mutually exclusive states with tagged unions, sealed variants, or equivalent constructs. Define each variant's required data together so unrelated flags and nullable fields cannot form unsupported combinations. Finish when the chosen types enforce the intended distinctions and represent every supported state.

4. **Make absence and outcomes explicit.** Express optional data with the project's nullable or optional-value conventions. When callers must distinguish several outcomes, define result variants carrying the data required for each outcome, or use the project's explicit exception contract. Give finite variants exhaustive handling where the language supports it. Finish when every supported outcome has a defined caller response and required data does not depend on sentinel values or unchecked assumptions.

5. **Connect external data to internal types.** For parsing, deserialization, or external input, apply [Input Contract Validation Trust Boundaries](input-contract-validation-trust-boundaries.md) to establish the runtime contract before controlled processing. A cast, type assertion, or generic deserialization target does not validate received data. Keep serialization details in boundary mappings and preserve the agreed external format. Finish when each conversion establishes the guarantees claimed by its internal type and any externally imposed unknown values have a defined treatment.

6. **Verify the guarantees.** Run the available compiler or static type checker for the affected scope. Verify meaningful guarantees, such as rejection of interchanged identifiers and exhaustive handling of result variants, with focused type checks where supported. Use runtime checks or tests for properties the type system cannot establish, including decoding and value constraints. In languages without static enforcement, use their available type-analysis tools and report the remaining runtime guarantees explicitly. Finish when the checks support the claimed guarantees and any unavailable verification is identified.

Complete the change or review when affected internal contracts use the simplest types that enforce their required distinctions, callers handle supported states and outcomes, and verification separates static guarantees from runtime guarantees. Scope changes to the task; follow [Confirm Compatibility and Retention Choices](../thinking/confirm-compatibility-and-retention-choices.md) when changing supported interfaces or formats introduces a compatibility choice.

### Example

The following is typed pseudocode. `OrderId` and `HotelId` are nominally distinct types, and result variants carry their own required fields.

```text
Before:
    submit(orderId: String, hotelId: String): Map<String, Object>
    // Callers can interchange identifiers and must guess result keys and types.

After:
    type OrderId = distinct String
    type HotelId = distinct String

    type SubmissionResult =
        Accepted(reference: String)
        | Rejected(reason: RejectionReason)
        | Unconfirmed(correlationId: String)

    submit(orderId: OrderId, hotelId: HotelId): SubmissionResult

    match submit(orderId, hotelId):
        Accepted(reference): recordAcceptance(reference)
        Rejected(reason): handleRejection(reason)
        Unconfirmed(correlationId): reconcile(correlationId)
```

With the stated type rules, interchanging the identifiers is a type error and each result branch exposes its declared fields. `Accepted` records submission acceptance; final completion requires its own confirmed outcome. Runtime parsing still establishes the validity of received identifier values.
