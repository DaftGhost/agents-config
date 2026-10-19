## Design Document

`design.md` shows how to get from today's state to the confirmed requirements, so an implementer can start without re-deriving anything. The requirements are fixed input.

### Investigate Before Designing

`requirements.md` states outcomes in observable terms, so it cannot say where a change goes or what else it touches. When it is the only carry-over (a new session, or code that has changed since it was written), the code is unread: investigate it before designing.

- Reuse what this conversation already holds. Code opened earlier in this conversation, with the callers and constraints found then, needs no second read unless it may have changed since (edits, a pull, a long gap). Open only what is still missing.
- Open the code behind every requirement: the functions that change, their callers, tests, and the config and deploy files the constraints came from. Look for each path that reaches the changed behavior, including paths the requirements never mention (an admin action, a job, a second entry point).
- Compare what you find with the requirements' background, impact, and constraints, which are claims to check. Only a requirement that the facts make impossible to meet is a blocker (ask first); every other discrepancy or gap is handled in the design.
- A path or situation the requirements do not cover but the design must handle (a second caller, records that exist before the change ships) is a Decisions row with a recommended default; `requirements.md` stays as confirmed.

### Sections

1. **Approach**: a few lines; alternatives only where a real choice exists.
2. **Changes by touchpoint**: a table of touchpoint, change, requirement IDs.
3. **Data and interface changes**: schema, API, config, migration, compatibility.
4. **Edge cases and failure handling**: concrete scenarios tied to the touchpoints, such as duplicate delivery, partial failure, concurrency, and other callers of changed code.
5. **Implementation acceptance criteria**: a table of ID (D1, ...), criterion, covered requirement IDs, how to check. Each is a condition an implementer or reviewer checks in the code or a test run (a transaction rolls back as a unit, a job is registered, the suite passes). Together they show every requirement is met; they do not restate a requirement's behavior in other words, since the covered-requirement column already links them.
6. **Rollout and rollback**: order of steps, handling of existing data, how to undo.
7. **Incidental changes**: each change that no requirement asks for, such as a defect fixed along the way, with its impact. A touchpoint row lists only what the requirements need, and each cites the requirement that forces it (a migration for existing records cites the requirement whose behavior needs it); an extra change in the same function, or work no requirement forces, gets its own line here. Write "None" when there are none.
8. **Decisions**: the table from the Document Rules. A situation the requirements do not cover but the design must handle (a late event, records that already exist) becomes a row with a recommended default; `requirements.md` stays as confirmed.

### Before Saving

- Every requirement ID appears in a touchpoint row and in an implementation acceptance criterion.
- No requirement is relaxed, dropped, or extended.
- Every touchpoint was opened in this conversation or is marked new.
