## Single-Document Template

The single tier exists so contained work costs little to document: each section once, one set of acceptance criteria, no ceremony.

```
# <title>
Status: Draft
Tier: single - <reason>

## Current facts
## Requirements
## Gap
## Technical Design
## Modified targets
## Verification
## Decisions
```

- **Current facts**: today's behavior the task touches (or "new project"), and the constraints you found with their source (README, deploy, config). A few lines.
- **Requirements**: the goal in a sentence, in scope and out of scope, then the table from the Document Rules.
- **Gap**: one line per difference between today and the requirements, citing requirement IDs. A requirement already met today says so.
- **Technical Design**: how the gap closes, in a few lines, including how it respects each constraint, and the edge cases that matter (duplicate delivery, partial failure, other callers of changed code).
- **Modified targets**: a table of target, change, requirement IDs. Mark a change no requirement asks for as incidental.
- **Verification**: test cases mapped to requirement IDs, placed in the project's existing test layout, so every acceptance criterion has a case.
- **Decisions**: the table from the Document Rules.

Before saving: every requirement ID appears in the gap, a modified-target row, and a verification case, and the requirements and gap stay short. A long modified-targets table is fine; when the requirements or gap would run long, the work likely belongs in the dual tier; say so in the Decisions section.
