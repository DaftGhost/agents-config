## Existing Functionality Change Document

**Purpose**: define a change, fix or retirement of existing behavior and verify its effects.

When this is the primary type, read [Dual Workflow](../dual.md) only if the user requests dual, or if no tier was specified and the requirements need confirmation before design or are too extensive to review alongside it. Otherwise use single. A secondary type follows the primary type's organization.

Write these sections in order after the header:

1. **Current functionality and implementation**: for each affected flow, describe the trigger and inputs, the existing entry points, relevant processing and branches, and outputs or side effects. Identify the files and symbols responsible and cite the project sources supporting these facts. For a fix, include the reproducible trigger, actual versus expected results and any verified cause; for retirement, identify the behavior being removed. Distinguish verified facts from assumptions.
2. **Requirements and gap analysis**: write requirements using [Requirements](../requirements.md). For each requirement ID, pair the relevant current behavior from section 1 with the required behavior and state only the difference between them; note any requirement already met.
3. **Applicable constraints**: describe constraints relevant to this change.
4. **Scope of change**: affected behavior, effects of the required change on users or consumers, and in-scope and out-of-scope changes.
5. **Change implementation approach**: describe the proposed changes against the current flows, requirements and constraints. List inspected or new targets with their requirement IDs.
6. **Impact assessment**: explain which callers, users, interfaces, existing data or other dependencies are affected, how they depend on current behavior and the consequences of the proposed changes. Link impacts to requirement IDs and mark unresolved impacts.
7. **Acceptance criteria and regression verification**: before-and-after criteria and checks, including preserved behavior and affected paths where relevant, mapped to requirement IDs.
8. **Decisions**: follow [Plan Decisions](../decisions.md).
