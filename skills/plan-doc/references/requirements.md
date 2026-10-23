## Requirements Document

`requirements.md` fixes what must change, in terms someone who has not read the code can check. The user confirms it before any design exists, so it carries everything the design would otherwise have to reopen.

### Sections

1. **Overview**: in two to four sentences, today's behavior, what must be true afterward, and who is affected.
2. **Current facts**: today's behavior (or "new project"); who or what depends on it, such as interfaces, stored data, other systems, and records that already exist; and each constraint found in the project (README, deploy, config, existing facilities) with its source.
3. **Requirements**: in scope and out of scope, then the table from the Document Rules.
4. **Gap**: a table of requirement IDs, today, required, and how closing it stays within the constraints. Check every requirement against the constraints now. A gap that cannot close under a constraint is a blocker: ask before writing, and write the requirement in the form the answer allows.
5. **Decisions**: the table from the Document Rules.

### Before Saving

- Every requirement has an ID, a checkable criterion, and a gap row (or a note that it is already met), and the whole document follows the observable-terms rule.
- Every requirement was checked against the code and the constraints.
- Every open product decision is a Decisions row, not a silent choice.
- The document contains no design content: modified targets, schema, mechanisms, tests.
