---
name: ask-compatibility
description: Resolve compatibility and retention choices with the user before implementing a migration, refactor, replacement, or removal that changes what is supported or kept. Use this skill whenever a change would remove, rename, or reshape a public or consumed interface, field, config format, CLI flag, cache key, file format, or package name; whenever old code paths, adapters, or deprecated modules would be kept or deleted; or whenever rows, tables, files, or logs would be dropped, archived, migrated, or deleted. Trigger even when the user only says "clean it up", "drop it", "replace it", "migrate", or "you decide", because general delegation does not settle these choices. Do not use it for internal restructuring with no supported-behavior or data impact, such as extracting private helpers or renaming local variables.
---

# Ask Compatibility

Whether old behavior stays supported, whether old code stays in the tree, and whether old data survives are decisions about consumers and records the user may know about and you cannot see. Deleting or breaking them is often irreversible, and a request such as "migrate" or "clean up" does not say which way the user wants these decisions to go. Resolve each choice with the user before touching the affected path, then implement exactly what they decided.

## Decide Whether a Choice Exists

Confirmation follows the actual impact, not the vocabulary. Ask when the change would alter anything a consumer or record depends on:

- a supported interface, input format, output field, CLI flag, config format, cache key, file format, or package name;
- old code, adapters, or workflows that are kept or deleted;
- rows, tables, files, or logs that are preserved, migrated, archived, or deleted.

Do not ask when the change is internal restructuring: private helpers, local names, or code moves whose public behavior, data, and supported formats stay identical. Calling it a "migration" or "refactor" does not create a choice. Verify that public signatures and behavior are unchanged, then proceed.

## Procedure

1. **Separate the decisions.** Treat these as three independent choices:
   - *backward compatibility*: which interfaces, formats, and behaviors stay supported (a new implementation can still honor them);
   - *legacy implementation retention*: whether old code and workflows stay;
   - *historical data retention*: whether data is preserved, migrated, archived, or deleted.

   Permission to drop compatibility does not authorize deleting data. Permission to delete old code does not decide what existing consumers see.

2. **Collect what is already decided.** Take choices the user stated explicitly in this conversation or recorded in project requirements (for example a retention policy in a README) as settled. Ask again only when new evidence changes the choice or the impact exceeds what was confirmed. A general request, or delegation such as "you decide", does not settle any choice, because the user has not seen the consumers and data you found.

3. **Inspect the impact.** Find affected interfaces, behavior, implementations, data, and known consumers in the repository, including docs, scripts, deploy files, and readers of the same data. List the repository's docs and notes (README, consumer lists, policy and partner files) and read those that mention the affected name; the decisive fact is often written there, not in code. Name consumers you cannot verify (other repos, external clients, customer-maintained files) as unverified instead of assuming they do not exist.

4. **Ask with a concrete brief.** Give the user what they need to decide in one message: what is affected and by whom, the feasible options with user impact and maintenance cost, which dependencies could not be verified, and your recommendation with its evidence. Neither preservation nor removal is the default. A recommendation, or silence from the user, is not confirmation. Ask only about compatibility and retention choices; note anything else in a line. See [references/choice-brief.md](references/choice-brief.md) for the layout and an example.

5. **Keep working on what does not depend on the choice.** While a choice is pending, pause only the changes that depend on it and do the independent work: bug fixes, additive changes, investigation, and moving in-repo callers onto a replacement (the old interface stays in place, so the move does not wait on the removal choice). Leave the affected state as it is. Not deleting something while you wait is a pause, not a retention policy; say so.

6. **Record the confirmed scope.** After the user chooses, state exactly what stays supported or retained, what is removed, and how consumers or data move over. For temporary compatibility or legacy retention, include an exit condition (a version, a date, or a measurable event). Put the decision where implementation and review will find it, such as the project's decision log, the change description, or the file the user named.

7. **Implement and verify against the agreement.** Check retained behavior, replacement behavior, and data handling against the confirmed scope. Before an operation that is hard to reverse, explain the recovery approach and its limits. Report the work as done only when what was implemented matches the user's decisions; passing tests does not authorize a choice the user never made.

## When the User Asked Not to Be Asked

An instruction such as "don't ask me" or "decide yourself" applies to ordinary implementation questions. It does not settle a compatibility or retention choice, but it does tell you how to ask: finish all the work that does not depend on the choice first, then lead the final message with what is done. Raise only the unsettled choice, as one decision the user can answer in a word, with your recommended option and exit condition already filled in. Keep unrelated observations (for example a changed return value) as a one-line note, not as extra questions. Leave the affected path untouched so the user can still choose either way.

## When the Choice Is Already Settled

When the user has supplied every choice for the affected path (for example "no v1 compatibility, delete the v1 code, leave the historical table untouched"), implement it without asking again, and still honor each limit they set. Say briefly what was done and what was deliberately left alone.

## Before Finishing

Check that:

- each compatibility, code-retention, and data-retention choice that the change touches is either settled by the user or pending with the affected path untouched;
- unverified consumers are named, not assumed absent;
- nothing was deleted or broken on the basis of a recommendation, "clean up", or "you decide";
- confirmed scope and any exit condition are recorded where the next implementer will find them;
- independent work was not held up by the pending question.
