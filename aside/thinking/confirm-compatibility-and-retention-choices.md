## Confirm Compatibility and Retention Choices

### What

Before a migration, refactor, replacement, or removal introduces a compatibility or retention choice, resolve that choice with the user. Trigger confirmation by the actual impact: internal restructuring with no such choice does not require confirmation merely because it is called a migration or refactor.

### Why

Implementation and review need an agreed scope for supported behavior and retained code or data. Separate choices keep each change within the user's authorization.

### How

- **Separate the decisions:** Distinguish backward compatibility (supported interfaces, input formats, and behavior), legacy implementation retention (old code and workflows), and historical data retention (preservation, migration, archival, or deletion). Compatibility can be maintained through a new implementation. Permission to drop compatibility does not authorize deleting data.
- **Use existing decisions:** Follow choices already explicit in the user's instructions or applicable project requirements. Ask again only when new evidence changes the choice or the impact exceeds the confirmed scope. A general request to migrate or refactor does not settle these choices.
- **Prepare a concrete choice:** Identify affected interfaces, behavior, implementations, data, and known consumers; state dependencies that could not be verified. Present feasible options, their user impact and maintenance cost, and an evidence-based recommendation. Obtain the user's choice before implementing the affected path; neither preservation nor removal is the default, and a recommendation or lack of reply is not confirmation.
- **Record the scope:** Specify exactly what remains supported or retained, what is removed, and how affected consumers or data will migrate. For temporary compatibility or legacy retention, agree on an exit condition. Record the confirmed choices where subsequent implementation and review can find them.
- **Continue independent work:** While a choice is pending, pause changes that depend on it and continue investigation or unaffected work. Keep the current affected state intact while awaiting a decision; this does not establish a retention policy.
- **Verify the agreement:** Check retained behavior, replacement behavior, and data handling against the confirmed scope. Before operations that are difficult to reverse, explain the recovery approach and its limits. Complete the work only when the implemented choices match the user's decisions and the relevant checks support the claimed outcomes; passing tests does not authorize an unconfirmed compatibility or retention choice.
