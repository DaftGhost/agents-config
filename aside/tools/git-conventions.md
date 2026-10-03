## Git Conventions

### What

When choosing development branches, creating commits, or integrating Git changes, keep each commit limited to one task, describe the actual change and validation, and resolve integration conflicts according to the user's confirmed choices.

### Why

Task-scoped commits make changes reviewable and their effects traceable. Accurate messages preserve the reason, validation evidence, and remaining limitations. Confirmed conflict choices prevent the agent from silently discarding or combining changes the user intended to keep.

### How

#### Choose the Development Branch

Identify the target branch from the user's instructions or repository conventions. The target branch is the integration destination.

- For a large change, create a feature branch from the target branch, develop on it, complete review, and then integrate it back into the target branch. Do not commit a large change directly to the target branch.
- A clearly scoped bug fix may be developed and committed directly on the target branch. If it grows into a large refactor, move the work to a feature branch.

Complete branch selection when the target and development branches are identified and the branch choice matches the change's scope.

#### Prepare Each Commit

Inspect the staged changes and confirm that they belong to one task. Exclude unrelated files and unauthorized working-tree changes.

Write the subject in the `<type>(<scope>): <summary>` format and accurately summarize the staged change. Code commits require a body, except for pure formatting changes or single-file spelling corrections. The body must include:

- The reason for the change, the main areas changed, and the affected modules or features.
- The validation commands actually run and their results, including test and failure counts or build results where applicable. Do not report unrun checks as passing.
- Any known limitations, unresolved issues, or related changes intentionally left out.

Create the commit only after its staged scope and message agree with the actual changes and validation evidence.

#### Integrate Branches

Complete the required review before integrating a feature branch. From the target branch, use `git merge --squash <source-branch>` by default. Follow an explicit user request for a regular merge, a retained merge commit, or another integration method.

If the operation produces conflicts, follow the conflict procedure below before continuing.

A squash merge prepares changes but does not create a commit automatically. Before creating the resulting commit:

1. Inspect `git diff --cached`, `git diff --cached --check`, and the staged file list with `git diff --cached --name-only`.
2. Confirm that the staged changes are limited to the integration scope and review the validation results.
3. Apply the commit requirements above and append `(squash from <source-branch>)` to the subject.
4. Create one commit on the target branch and verify that it contains the reviewed changes.

Complete a squash integration when that commit exists on the target branch and its content and message match the reviewed scope and validation evidence. Preparing the squash changes alone does not complete integration.

#### Resolve Integration Conflicts

Apply this procedure whenever `git merge`, `git rebase`, `git cherry-pick`, or another integration operation produces conflicts.

1. **Inventory before editing.** Stop and preserve the conflict state. Record the current branch and the branch being integrated, or the commit being cherry-picked. Number every conflicted file and describe each conflict region, both sides' concrete changes, their impact, and whether either side added new files. By default, present test code with its related business code while retaining each conflicted file's identifier. Call out independent changes, cases that cannot be determined, and validation failures separately. Do not discuss the conflicting files' commit versions, common ancestor, or history. Complete the inventory when every conflicted file and region is accounted for.
2. **Obtain choices.** For each numbered file and conflict region, ask the user whether to keep one side or combine the changes. The user chooses; the agent edits and stages. Proceed with a region only when its resolution is explicitly confirmed.
3. **Apply confirmed resolutions.** Edit only confirmed regions and remove their conflict markers. Leave unconfirmed regions unresolved. Run `git add` for files whose conflicts are fully resolved, and report the result. A confirmed region does not authorize resolving another region in the same file.
4. **Verify and continue.** After all conflicts are resolved, verify that the resolutions match the confirmed choices and run the relevant checks. Continue the active operation with `git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`, or the applicable commit step. Verify the operation's result before reporting integration complete.

Complete conflict recovery when every region has a confirmed resolution, all conflicted files are resolved and staged, and the active integration operation has completed. While choices remain pending, report the unresolved regions and preserve the conflict state.

### Example

For a code commit, replace the placeholders with facts from the actual change and checks:

```text
refactor(channelcore): remove the Fliggy order-list search endpoint

Reason: <why the endpoint is being removed>
Changes: <main changes and affected modules or features>
Validation: <commands actually run and their results>
Limitations: <known limitations, unresolved issues, or intentionally omitted changes>
```

For a squash integration of `codex/fliggy-order`, use the same body requirements and identify the source branch in the subject:

```text
feat(channelcore): add a Fliggy order adapter (squash from codex/fliggy-order)
```
