## Git Conventions

### Commit Messages

- The commit subject must accurately summarize the change and use the `<type>(<scope>): <summary>` format. For example: `refactor(channelcore): remove the Fliggy order-list search endpoint`.
- Code commits must include a body, except for pure formatting changes or single-file spelling corrections. The body must state the reason for the change, the main areas changed, and the affected modules or features.
- The body must record the validation commands actually run and their results, such as test and failure counts or the build result. Do not report tests that were not run as passing.
- State any known limitations, unresolved issues, or related changes intentionally left out in the body so the commit message does not hide remaining risks.
- Each commit must contain only changes related to one task. Do not include unrelated files or unauthorized working-tree changes.

### Branches

The target branch is the integration branch designated by the user or repository conventions.

- For a large change, create a feature branch from the target branch, develop on that branch, complete review, and then merge it back into the target branch. Do not commit directly to the target branch for a large change.
- A clearly scoped bug fix may be changed and committed directly on the target branch. If the fix grows into a large refactor, create a new branch.

### Merging

- By default, integrate branches with a squash merge by running `git merge --squash <source-branch>` from the target branch. Follow the user's explicit request to retain a merge commit, use a regular merge, or use another integration method.
- A squash merge does not create a merge commit automatically. After confirming the staged content and validation results, create one commit on the target branch. Keep the `<type>(<scope>): <summary>` subject format and append `(squash from <source-branch>)` to identify the source branch. For example: `feat(channelcore): add a Fliggy order adapter (squash from codex/fliggy-order)`.
- Before committing a squash merge, inspect `git diff --cached`, `git diff --cached --check`, and the staged file list. Confirm that the staged changes are limited to the merge scope. The commit body must follow the commit-message rules and record the validation actually run.

#### Conflict Resolution

These rules apply to Git integration operations that can produce conflicts, including `git merge`, `git rebase`, and `git cherry-pick`:

1. **Stop and inventory conflicts immediately:** Preserve the conflict state and assign a number to each conflicted file. Record the current branch and the branch being integrated (or the commit being cherry-picked). Describe the concrete changes from both sides and whether each side added new files. By default, handle test code together with its related business code instead of listing it separately. Call out independent changes, cases that cannot be determined, and validation failures separately. Do not discuss the conflicting files' commit versions, common ancestor, or history.
2. **Confirm choices before resolving conflicts:** For each numbered file, describe the conflict region, both sides' content, and the impact. Ask the user whether to keep one side or combine them. The user only needs to choose; they do not need to edit conflict markers or stage files.
3. **Resolve and continue according to the confirmed choices:** Edit only the confirmed regions, remove their conflict markers, run `git add`, and report the result. Leave any unconfirmed region unresolved. After all conflicts are resolved, the agent may run checks, continue with `merge --continue`, `rebase --continue`, or `cherry-pick --continue`, or commit.
