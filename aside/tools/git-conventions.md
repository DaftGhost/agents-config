## Git Conventions

### What

When choosing a development branch or preparing a commit, keep each commit limited to one task and describe the actual change and validation.

### Why

Task-scoped commits make changes reviewable and their effects traceable. Accurate messages preserve the reason and the validation evidence.

### Choose the Development Branch

Identify the target branch from the user's instructions or repository conventions. The target branch is the integration destination.

- For a large change, create a feature branch from the target branch and develop on it. Do not commit a large change directly to the target branch.
- A clearly scoped bug fix may be developed and committed directly on the target branch. If it grows into a large refactor, move the work to a feature branch.

Complete branch selection when the target and development branches are identified and the branch choice matches the change's scope.

### Prepare Each Commit

Inspect the staged changes and confirm that they belong to one task. Exclude unrelated files and unauthorized working-tree changes.

Write the commit message from the staged diff, and verify each factual claim in it against the diff before committing.

**Subject**: `<type>(<scope>): <summary>`

- `type`: choose from the types in recent history. Use `feat` for new capability, `refactor` for restructuring or renaming without behavior change, and `chore` for configuration and ignore rules.
- `summary`: state the purpose of the whole change in one short line. Cover the main intent of all the changes, not only one part of them, and leave the details that belong in the body out of the line. 

**Body**: required for code commits, except pure formatting changes or single-file spelling corrections. Include these items when they apply:

- The reason for the change, and the main areas changed, including the affected modules or features. For renames, list `old -> new`, with each new name's purpose when its meaning is not obvious.
- The validation commands actually run and their results, including test and failure counts or build results where applicable. Do not report unrun checks as passing.
- Breaking changes: what stops working and what consumers must update.
- What did not change, when that helps review.

Exclude process narration, such as failed attempts, amend history, or review feedback.

Create the commit only after its staged scope and message agree with the actual changes and validation evidence.

### Integrate Branches

For branch integration and integration-conflict recovery, follow the `git-merge` skill. This document continues to cover development-branch selection and ordinary commit preparation.

### Example

For a code commit, replace the placeholders with facts from the actual change and checks:

```text
refactor(channelcore): consolidate order search on the v2 endpoint

Reason: <why the change is needed>
Changes: <main changes and affected modules or features; for renames, `old -> new` with each new name's purpose when its meaning is not obvious>
Validation: <commands actually run and their results>
Breaking: <what stops working and what consumers must update; omit when none>
Unchanged: <what did not change, when that helps review; omit when not useful>
```
