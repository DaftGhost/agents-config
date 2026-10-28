## Code Refactoring Document

**Purpose**: define a structural improvement and verify that existing behavior and contracts remain unchanged.

When this is the primary type, read [Dual Workflow](../dual.md) only if the user requests dual, or if no tier was specified and the requirements need confirmation before design or are too extensive to review alongside it. Otherwise use single. A secondary type follows the primary type's organization.

Write these sections in order after the header:

1. **Refactoring objectives and scope**: affected components, current structural problems and desired structural properties, with requirement IDs.
2. **Behavioral and contract preservation requirements**: observable behavior, interfaces, callers and constraints that must remain unchanged, with requirement IDs and supporting sources. Name internal components when they are the subject of the refactor.
3. **Structural design and implementation sequence**: proposed responsibilities, boundaries and order of changes; identify interface effects on callers. List inspected or new targets with their requirement IDs.
4. **Acceptance criteria and behavior preservation verification**: inspectable structural criteria and checks demonstrating preserved behavior and contracts, mapped to requirement IDs. Use relevant existing tests or focused checks.
5. **Decisions**: follow [Plan Decisions](../decisions.md).

Use stable requirement IDs (R1, R2, ...); never reuse a removed ID. Link acceptance criteria and verification checks to their requirements; map requirements that necessitate a change to inspected or new targets.
