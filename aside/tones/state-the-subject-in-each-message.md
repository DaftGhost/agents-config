## State the Subject in Each Message

### What

Explicitly establish the subject within each prose message in a turn. An entire message must not consist of statements whose subjects are all omitted.

A turn begins with one user message and ends with the final reply to that message, including all reasoning and operations in between. Apply this rule to agent-authored prose throughout the turn: reasoning, plans, operation descriptions, progress messages, and the final reply. Preserve the required syntax of executable commands and structured tool arguments.

### Why

A message that never states its subject leaves the reader to infer who acted or what a result or judgment describes. A subject mentioned in another message during the same turn does not make the current message self-contained.

### How

Name the acting or described subject within the message itself. Use "I" for your own actions and name the relevant command, file, component, or other entity when describing its behavior, state, or result.

Once the subject is explicit within a message, later clauses or sentences may omit a repeated subject when they clearly continue describing that same subject. Introduce a new subject when the actor or topic changes. The requirement applies to the message as a whole; it does not require repeating a subject in every sentence.

Before emitting each message, check that its own content explicitly establishes the subject and makes clear who performed the actions or what the statements describe. Do not rely solely on the user message or another message in the turn to supply it.

### Example

Before: Updated the configuration and verified the change.

After: I updated the configuration and verified the change.
