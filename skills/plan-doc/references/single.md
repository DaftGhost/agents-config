## Single-Document Template

The single tier exists so contained work costs little to document: the core content once, one set of acceptance criteria, no ceremony. Write it as its own compact document and leave out the sections the dual documents carry.

```
# <title>
Status: Draft
Tier: single - <reason>

## Goal and scope
## Requirements
## Plan
## Verification
## Decisions
```

- **Goal and scope**: the goal in a sentence or two, with today's behavior (or "new project"); in scope; out of scope; the constraints you found and how the plan respects them.
- **Requirements**: the table from the Document Rules.
- **Plan**: a table of touchpoint, change, requirement IDs. Mark a change no requirement asks for as incidental. Below the table, list the edge cases that matter, such as duplicate delivery, partial failure, and other callers of changed code.
- **Verification**: test cases mapped to requirement IDs, placed in the project's existing test layout, so every acceptance criterion has a case.
- **Decisions**: the table from the Document Rules.

Before saving: every requirement ID is served by a Plan row and covered by a Verification case, and the document stays near 100 lines. When it would run much longer, the work likely belongs in the dual tier; say so in the Decisions section.
