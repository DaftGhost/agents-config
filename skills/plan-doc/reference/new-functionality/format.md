## New Functionality Document

**Purpose**: define a new capability and how to implement and verify it. For a new project, describe the absence of an implementation rather than inventing current behavior.

When this is the primary type, read [Dual Workflow](../dual.md) only if the user requests dual, or if no tier was specified and the requirements need confirmation before design or are too extensive to review alongside it. Otherwise use single. A secondary type follows the primary type's organization.

Write these sections in order after the header:

1. **Capability and scope** *(what)*: users or consumers, goal, inputs, outcomes, in-scope and out-of-scope behavior.
2. **Context and constraints** *(what)*: relevant current behavior, dependencies and constraints with sources, including behavior the capability must coexist with.
3. **Capability requirements** *(what)*: a table of requirement IDs and observable outcomes, including relevant boundary cases.
4. **Implementation** *(how)*: the flow and affected entry points, components, interfaces and data; for a new project, describe the proposed layout. List inspected or new targets with their requirement IDs.
5. **Acceptance and verification** *(how and acceptance)*: concrete input-to-result criteria and checks mapped to requirement IDs.
6. **Decisions** *(what)*: use a table of ID (Q1, ...), question, options, recommended default, and a blank decision column. Mark a requirement depending on a decision `pending Qn`. Write `None` when empty.

Use stable requirement IDs (R1, R2, ...); never reuse a removed ID. Link acceptance criteria and verification checks to their requirements; map requirements that necessitate a change to inspected or new targets. In dual, record any new implementation-only decisions in a Decisions section in `how-to-do.md` without copying earlier decisions.
