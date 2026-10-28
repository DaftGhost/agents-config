## Existing Functionality Change Document

**Purpose**: define a change, fix or retirement of existing behavior and verify its effects.

When this is the primary type, read [Dual Workflow](../dual.md) only if the user requests dual, or if no tier was specified and the requirements need confirmation before design or are too extensive to review alongside it. Otherwise use single. A secondary type follows the primary type's organization.

Write these sections in order after the header:

1. **Change scope** *(what)*: affected behavior, users or consumers, and in-scope and out-of-scope changes.
2. **Current and desired behavior** *(what)*: a table of requirement IDs, current outcome and desired outcome; identify behavior and contracts to preserve. For a fix, include a reproducible trigger and actual versus expected results. For retirement, identify removed behavior and affected consumers.
3. **Impact and constraints** *(what)*: affected paths and existing consumers or data, with relevant project constraints and their sources.
4. **Change approach** *(how)*: affected entry points and callers, the cause for a fix, and the proposed changes and consequences. List inspected or new targets with their requirement IDs.
5. **Acceptance and regression** *(how and acceptance)*: before-and-after criteria and checks, including preserved behavior and affected paths where relevant, mapped to requirement IDs.
6. **Decisions** *(what)*: use a table of ID (Q1, ...), question, options, recommended default, and a blank decision column. Mark a requirement depending on a decision `pending Qn`. Write `None` when empty.

Use stable requirement IDs (R1, R2, ...); never reuse a removed ID. Link acceptance criteria and verification checks to their requirements; map requirements that necessitate a change to inspected or new targets. In dual, record any new implementation-only decisions in a Decisions section in `how-to-do.md` without copying earlier decisions.
