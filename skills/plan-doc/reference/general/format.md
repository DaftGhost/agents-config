## General Plan Document

**Purpose**: make the outcome, implementation and verification of a project task outside the four specific types reviewable.

When this is the primary type, read [Dual Workflow](../dual.md) only if the user requests dual, or if no tier was specified and the requirements need confirmation before design or are too extensive to review alongside it. Otherwise use single. A secondary type follows the primary type's organization.

Write these sections in order after the header:

1. **Task objectives and scope**: what to do, the relevant starting state and scope, with requirement IDs.
2. **Applicable constraints**: constraints relevant to the task.
3. **Detailed design**: the key logic, flow, execution steps and inspected or new targets, linked to requirement IDs.
4. **Expected outcomes**: the expected results or state changes for each requirement ID.
5. **Verification approach**: how to check the expected outcomes, mapped to requirement IDs.
6. **Decisions**: follow [Plan Decisions](../decisions.md).

Use stable requirement IDs (R1, R2, ...); never reuse a removed ID. Link acceptance criteria and verification checks to their requirements; map requirements that necessitate a change to inspected or new targets.
