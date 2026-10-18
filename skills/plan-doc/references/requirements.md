## Requirements Document

`requirements.md` fixes what must be true when the task is done, in terms someone who has not read the code can check. The user confirms it before any design exists, so it carries everything the design would otherwise have to reopen.

### Sections

1. **Background and goal**: today's behavior (or "new project"), and the goal.
2. **Scope**: in scope, out of scope.
3. **Requirements**: the table from the Document Rules.
4. **Impact**: who or what depends on the changed behavior, such as interfaces, stored data, other systems, and records that already exist.
5. **Constraints and feasibility**: each constraint found in the project (README, deploy, config, existing facilities) and how the requirements respect it. Check every requirement against these now. A requirement that cannot be met under a constraint is a blocker: ask before writing, and write the requirement in the form the answer allows.
6. **Decisions**: the table from the Document Rules.

### Before Saving

- Every requirement has an ID and a checkable criterion, and the whole document follows the observable-terms rule.
- Every requirement was checked against the code and the constraints.
- Every open product decision is a Decisions row, not a silent choice.
- The document contains no design content: touchpoints, schema, mechanisms, tests.
