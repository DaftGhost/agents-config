## Git Conventions

### What

When choosing a development branch or preparing a commit, keep each commit limited to one task and describe the actual change and validation.

### Why

Task-scoped commits make changes reviewable and their effects traceable. Accurate messages preserve the reason, validation evidence, and remaining limitations.

### Choose the Development Branch

Identify the target branch from the user's instructions or repository conventions. The target branch is the integration destination.

- For a large change, create a feature branch from the target branch and develop on it. Do not commit a large change directly to the target branch.
- A clearly scoped bug fix may be developed and committed directly on the target branch. If it grows into a large refactor, move the work to a feature branch.

Complete branch selection when the target and development branches are identified and the branch choice matches the change's scope.

### Prepare Each Commit

Inspect the staged changes and confirm that they belong to one task. Exclude unrelated files and unauthorized working-tree changes.

Write the subject in the `<type>(<scope>): <summary>` format and accurately summarize the staged change. Code commits require a body, except for pure formatting changes or single-file spelling corrections. The body must include:

- The reason for the change, the main areas changed, and the affected modules or features.
- The validation commands actually run and their results, including test and failure counts or build results where applicable. Do not report unrun checks as passing.
- Any known limitations, unresolved issues, or related changes intentionally left out.

Create the commit only after its staged scope and message agree with the actual changes and validation evidence.

### Integrate Branches

For branch integration and integration-conflict recovery, follow the `git-merge` skill. This document continues to cover development-branch selection and ordinary commit preparation.

### Example

For a code commit, replace the placeholders with facts from the actual change and checks:

```text
refactor(channelcore): remove the Fliggy order-list search endpoint

Reason: <why the endpoint is being removed>
Changes: <main changes and affected modules or features>
Validation: <commands actually run and their results>
Limitations: <known limitations, unresolved issues, or intentionally omitted changes>
```
