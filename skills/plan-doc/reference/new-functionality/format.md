## New Functionality Document

**Purpose**: define a new capability and how to implement and verify it. For a new project, describe the absence of an implementation rather than inventing current behavior.

When this is the primary type, read [Dual Workflow](../dual.md) only if the user requests dual, or if no tier was specified and the requirements need confirmation before design or are too extensive to review alongside it. Otherwise use single. A secondary type follows the primary type's organization.

Write these sections in order after the header:

1. **Capability objectives and scope**: users or consumers, goal, inputs, outcomes and behavior covered by the task.
2. **Current context**: relevant current behavior and dependencies with sources, including behavior the capability must coexist with.
3. **Applicable constraints**: follow [Constraints](../constraints.md).
4. **Functional requirements**: follow [Requirements](../requirements.md).
5. **Detailed design**: follow [Detailed Design](../detailed-design.md).
6. **Target files**: follow [Target files](../writing.md#target-files).
7. **Acceptance criteria and verification**: concrete input-to-result criteria and checks mapped to requirement IDs or applicable constraints.
8. **Decisions**: follow [Plan Decisions](../decisions.md).
