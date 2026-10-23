---
name: clarify-ambiguous-requests
description: 'Use before acting on, planning, or implementing a request whose wording allows more than one reading that would change what you do: an unclear referent ("the config", "it"), a word with two meanings ("biweekly", "last"), a number without a unit, a vague cutoff ("old"), a misspelled or inexact name, or contradictory instructions. Check the material, then act or ask. Not for explaining or translating such words; for open design choices on a clear request, use ask-open-choices.'
---

# Clarify Ambiguous Requests

Acting on a guessed meaning produces work the user must inspect and undo. Asking first costs one round trip; asking when the meaning is clear costs the same for nothing.

## Steps

1. List the readings the user's words allow. Then check the material (files, earlier messages) read-only and drop readings it rules out: a typo that matches one name, an "it" with one candidate. A convention in the material (such as a field's unit) does not tell you what the user meant when their words leave it out.
2. Act without asking when one reading survives, or when every surviving reading produces the same result (for example, writing the user's own word "biweekly" into a note). State the reading you used in one line of the reply.
3. Otherwise, ask before changing anything, including the unambiguous parts of the same request: the answer may change them.
   - Ask only about the meaning. Leave out choices the user's words, the material, or common practice already settle.
   - Give each reading concretely (what it would change, found in the material), recommended first when the evidence favors one.
   - Use the harness's question tool (such as AskUserQuestion) when one exists, loading its schema first if needed; otherwise end the reply with the question.
