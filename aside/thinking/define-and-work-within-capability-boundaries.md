## Define and Work Within Capability Boundaries

### What

Every program is a bounded system. Before implementation, define the strongest truthful contract it can fulfill by analyzing the requested outcome, its feasibility, the operating conditions, and what the program can control or verify. A request does not implicitly require a perfect system that handles every conceivable case or guarantees outcomes beyond its boundary.

### Why

Explicit limits make the promised outcome testable and keep completion grounded in what the program can deliver and verify.

### How

- **Define the promised outcome:** Identify the useful result and supported cases. State adjacent or end-to-end outcomes that the program will not claim.
- **Establish feasibility:** Distinguish achievable, conditional, uncertain, and infeasible parts against known computational, physical, technical, and resource constraints. A limit on the end-to-end guarantee does not invalidate a useful part that the program can deliver.
- **Bound the operating envelope:** Record the inputs, states, workloads, dependencies, failure modes, and measurable limits that materially affect the promise. Ground quantitative targets in available evidence and resources.
- **Locate the control and evidence boundary:** Separate actions and facts the program can control or verify from outcomes that depend on another system, person, environment, or later step. Names, return values, statuses, logs, and success conditions describe confirmed facts rather than unverified external completion.
- **Work to the boundary:** Complete the useful behavior inside the boundary and make the supported paths correct, testable, observable, and maintainable. State residual uncertainty instead of implying control the program does not have.
- **Preserve continuation:** When work may continue beyond the boundary, retain enough explicit state and context for the appropriate retry, reconciliation, callback, or manual intervention.
- **Expand deliberately:** Extend the boundary only when a concrete requirement, observed failure, or measured risk justifies the additional behavior and complexity.
- **Completion criteria:** An implementation or review is complete only when the promised outcome is feasible within stated conditions, every claim is backed by observable evidence, the strongest useful behavior within the boundary is implemented, residual uncertainty is explicit, and a continuation path exists where the workflow requires one.
