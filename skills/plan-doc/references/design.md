## Design Document

`design.md` shows how to close the gap in the confirmed `requirements.md` and what that changes, so an implementer can start without re-deriving anything. The requirements are fixed input.

### Investigate Before Designing

`requirements.md` states its facts in observable terms, so it cannot say where a change goes or what else it touches. When it is the only carry-over (a new session, or code that has changed since it was written), the code is unread: investigate it before designing.

- Reuse what this conversation already holds. Code opened earlier in this conversation, with the callers and constraints found then, needs no second read unless it may have changed since (edits, a pull, a long gap). Open only what is still missing.
- Open the code behind every requirement: the functions that change, their callers, tests, and the config and deploy files the constraints came from. Look for each path that reaches the changed behavior, including paths the requirements never mention (an admin action, a job, a second entry point).
- Compare what you find with the current facts and gap in `requirements.md`, which are claims to check. Only a requirement that the facts make impossible to meet is a blocker (ask first); every other discrepancy or gap is handled in the design.
- A path or situation the requirements do not cover but the design must handle (a second caller, records that exist before the change ships) is a Decisions row with a recommended default; `requirements.md` stays as confirmed.

### Sections

1. **Overview**: in a few sentences, how the design closes the gap and which areas it modifies, with a link to `requirements.md`.
2. **Technical Design**:
   - **Flow**: the changed behavior end to end, from trigger to result, at the level of components; alternatives only where a real choice exists.
   - **Data and interface changes**: schema, API, config, migration, compatibility.
   - **Edge cases and failure handling**: concrete scenarios tied to the modified targets, such as duplicate delivery, partial failure, concurrency, and other callers of changed code.
   - **Rollout and rollback**: order of steps, handling of existing data, how to undo.
3. **Modified targets**: a table of target, today, change, requirement IDs, grouped by area or flow. Each row cites the requirement that forces it (a migration for existing records cites the requirement whose behavior needs it). A change no requirement asks for, such as a defect fixed along the way, gets its own row marked incidental, with its impact.
4. **Verification**: a table of ID (D1, ...), criterion, covered requirement IDs, how to check. Each is a condition an implementer or reviewer checks in the code or a test run (a transaction rolls back as a unit, a job is registered, the suite passes). Together they show every requirement is met; they do not restate a requirement's behavior in other words.
5. **Decisions**: the table from the Document Rules. A situation the requirements do not cover but the design must handle (a late event, records that already exist) becomes a row with a recommended default; `requirements.md` stays as confirmed.

### Before Saving

- Every requirement ID appears in a modified-target row and in a verification criterion.
- No requirement is relaxed, dropped, or extended.
- Every modified target was opened in this conversation or is marked new.
