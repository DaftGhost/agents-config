---
name: ask-open-choices
description: 'Use for any task (code, writing, data, planning) whose request leaves a key choice open between reasonable options that change the result: a feature''s fields or defaults, an email or summary''s audience or tone, which record a dedupe keeps, what "clean up" covers. Requests often look complete when they are not. Ask instead of picking and reporting afterward. Skip when the user chose or said "you pick", or the request, conventions, or standard practice settle it.'
disable-model-invocation: false
user-invocable: true
---

# Ask Open Choices

When two options are both reasonable and the user would notice which one you deliver, the choice is theirs. Producing one and flagging it afterward still decides for them: the result becomes the default they must argue against.

## Steps

1. Look at the relevant material (code, documents, data, earlier messages), just enough to name the options concretely.
2. For each choice, decide which option you would recommend and what the recommendation rests on:
   - **Settled**: it rests on the user's words in their plain meaning, on what the existing material already does, or on standard practice for that kind of work. Do it without asking, even if alternatives exist; name a notable alternative in one line of the reply.
   - **Delegated**: the user said "you pick" or similar. Pick, then name the choice and one alternative in the reply.
   - **Open**: it rests on a guess about something you cannot see, such as the user's audience, data, consumers, or preferences, and the options would produce different results: which records survive, who the text is for, what a vague verb covers. Ask only these.

   Each question costs the user a round trip, so a choice you can justify from the request, the material, or standard practice is not a question.
3. If any choice is open, ask before producing the part that depends on it, with every open choice in one ask: each with its options, a one-line tradeoff, and your recommendation first.
   - Whenever the harness offers a question tool (such as AskUserQuestion), ask through it rather than in prose; the user answers there directly. If the tool is listed but its schema is not loaded, load it first (for example with ToolSearch).
   - Only when no question tool exists, end your reply with the questions.
