## General Plan Document

**Purpose**: make the outcome, implementation and verification of a project task outside the four specific types reviewable.

When this is the primary type, read [Dual Workflow](../dual.md) only if the user requests dual, or if no tier was specified and the requirements need confirmation before design or are too extensive to review alongside it. Otherwise use single. A secondary type follows the primary type's organization.

Write these sections in order after the header:

1. **Goal and scope** *(what)*: requested outcome, in-scope and out-of-scope items, and affected consumers or resources.
2. **Current state and constraints** *(what)*: relevant facts, dependencies and constraints with sources.
3. **Required outcomes** *(what)*: a table of requirement IDs and required outcomes or properties.
4. **Approach and targets** *(how)*: describe the approach and inspected or new targets, linked to requirement IDs.
5. **Acceptance and verification** *(how and acceptance)*: observable results or inspectable properties and checks mapped to requirement IDs.
6. **Decisions** *(what)*: use a table of ID (Q1, ...), question, options, recommended default, and a blank decision column. Mark a requirement depending on a decision `pending Qn`. Write `None` when empty.

Use stable requirement IDs (R1, R2, ...); never reuse a removed ID. Link acceptance criteria and verification checks to their requirements; map requirements that necessitate a change to inspected or new targets. In dual, record any new implementation-only decisions in a Decisions section in `how-to-do.md` without copying earlier decisions.
