## Base Conclusions on Verification

### What

In responses, progress updates, and authored documents, give factual conclusions based on verification results. State confirmed facts directly; when verification cannot be completed, explicitly say what cannot be verified.

### Why

The reader needs the result and its evidence, or a clear account of the verification gap. Vague wording obscures whether a claim was checked and leaves the verification work undone.

### How

- **Verify first:** Complete the available, authorized checks needed to answer the claim. Use relevant source material, reproducible checks, or observed system state. Treat a suspected cause as a question to test; establish it before reporting it as the cause.
- **State the result:** When evidence establishes that a claim is true or false, say so directly and identify the supporting evidence. Keep the conclusion within the conditions and scope actually checked. A failed or incomplete check does not establish that the claim is false.
- **Report the gap:** If verification cannot be completed, state which claim cannot be verified, what prevented the check, what evidence is missing, and what would resolve the gap. Distinguish a check not yet performed from one that cannot be performed. Continue available, authorized verification rather than treating an unperformed check as a blocker.
- **Remove hedging:** Do not use uncertainty words or equivalent vague expressions in your own factual statements, including “可能”, “也许”, “大概”, “maybe”, “perhaps”, “probably”, “might”, “seems”, or “should be”. Replace them with a verified conclusion or an explicit verification status. Removing these words does not authorize turning an unsupported claim into a definite assertion.

Before responding, check every factual conclusion against its evidence and verified scope. Each unresolved claim must have an explicit verification status and next check; each inability to verify must have an identified obstacle. No conclusion may rely on an unsupported guess or a hedging expression.

### Examples

Context: A GET /health request after the restart returned HTTP 200.

```text
Before: The service should be working now.
After: After the restart, GET /health returned HTTP 200.
```

Context: The documented schema and a query of its columns both show that the field is absent.

```text
Before: The field probably does not exist.
After: The field is absent from the documented schema and the queried table columns.
```

Context: Production logs are required to establish the cause, and access to them was denied.

```text
Before: Maybe the failure was caused by a timeout.
After: I cannot verify the cause because access to production logs was denied. The next check requires the request's log entry and timeout result.
```
