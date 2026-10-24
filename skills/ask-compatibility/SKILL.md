---
name: ask-compatibility
description: 'Use when a task would retire something old (an old name, API field, config format, CLI flag, package, code path, or stored data) through a rename, replacement, migration, or removal. Ask the user whether to keep supporting it or keep a backup of it, including when they left it "up to you" or said "clean up" or "migrate", and when project notes seem to answer it.'
disable-model-invocation: false
user-invocable: true
---

# Ask Compatibility

The user knows consumers and records that you cannot see in the repository, so the keep-or-drop choice is theirs. Keeping a backup of the old thing (a legacy copy, a `.bak` file, an archived record) is one way of keeping it, so it belongs to the same choice. Surface the question, then follow the answer.

## Steps

1. Check what the user said in this conversation. A choice they stated there is settled for exactly what it names; carry that part out as given, and put the compatibility, code, and data questions it leaves unnamed to them. A general delegation such as "you decide" or "clean up" leaves the question open. Treat notes and records elsewhere in the project as background, and still ask.
2. Look up the impact in the repository: callers, docs, consumer lists, readers of the same data, and any existing backups. Name consumers you cannot verify, such as other teams, external clients, and customer-held files.
3. Ask right away, as soon as steps 1 and 2 give you enough to put the question, and hold the affected change until the user answers. Use the question tool the harness provides (for example AskUserQuestion) whenever one is available, and otherwise ask in your final message.
