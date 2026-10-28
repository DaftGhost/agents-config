## New Functionality Document

**Purpose**: define a new capability and how to implement and verify it. For a new project, describe the absence of an implementation rather than inventing current behavior.

When this is the primary type, read [Dual Workflow](../dual.md) only if the user requests dual, or if no tier was specified and the requirements need confirmation before design or are too extensive to review alongside it. Otherwise use single. A secondary type follows the primary type's organization.

Write these sections in order after the header:

1. **Capability objectives and scope**: users or consumers, goal, inputs, outcomes, in-scope and out-of-scope behavior.
2. **Current context and constraints**: relevant current behavior, dependencies and constraints with sources, including behavior the capability must coexist with.
3. **Functional requirements**: follow [Requirements](../requirements.md).
4. **Implementation design**: the flow and affected entry points, components, interfaces and data; for a new project, describe the proposed layout. List inspected or new targets with their requirement IDs.
5. **Acceptance criteria and verification**: concrete input-to-result criteria and checks mapped to requirement IDs or applicable constraints.
6. **Decisions**: follow [Plan Decisions](../decisions.md).
