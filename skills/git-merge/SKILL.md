---
name: git-merge
description: Use when integrating one branch into another, choosing or completing a squash or regular merge, or resolving conflicts during merge, rebase, or cherry-pick. Guides review-first integration, user-confirmed conflict resolution, and verification through completion.
argument-hint: "[source-branch] [target-branch]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
  - AskUserQuestion
  - Bash(git *)
---

# Merge a branch

Use this workflow to integrate reviewed changes from a source branch into a target branch. It covers the integration method, conflicts, and verification through completion.

## Prepare the integration

1. Identify the source branch and target branch from the user's request and repository state. Confirm the intended direction of integration.
2. Check the current branch and working tree before starting. Preserve unrelated changes and keep them out of the integration.
3. Complete the required review of a feature branch before integrating it.
4. Unless the user or repository instructions specify another method, switch to the target branch and run `git merge --squash <source-branch>`. Follow an explicit request for a regular merge, retained merge commit, or other integration method.

**Complete preparation** when the source, target, integration method, and review status are clear, and the integration operation has started from the target branch.

## Resolve integration conflicts

Use this procedure when `git merge`, `git rebase`, `git cherry-pick`, or another integration operation produces conflicts.

1. **Inventory before editing.** Stop and preserve the conflict state. Record the current branch and the branch being integrated, or the commit being cherry-picked. Number every conflicted file and each conflict region. For every region, describe both sides' concrete changes and their impact, and note whether either side added new files. By default, present test code with its related business code while retaining each conflicted file's identifier. Call out independent changes, cases that cannot be determined, and validation failures separately. Do not discuss the conflicting files' commit versions, common ancestor, or history.

   **Complete the inventory** when every conflicted file and region is accounted for.

2. **Obtain choices.** For each numbered file and conflict region, ask the user whether to keep one side or combine the changes. Proceed with a region only after its resolution is explicitly confirmed.

   **Complete this step** when each region to be resolved has an explicit user choice.

3. **Apply confirmed resolutions.** Edit only confirmed regions and remove their conflict markers. Leave unconfirmed regions unresolved. Stage files with `git add` only when all their conflicts are resolved, and report which files were staged. Confirmation for one region does not authorize resolving another region in the same file.

   **Complete this step** when fully resolved files are staged and unconfirmed regions remain unresolved.

4. **Verify and continue.** After all conflicts are resolved, verify that the result matches the user's choices and run the relevant checks. Continue the active operation with `git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`, or its applicable commit step. Verify the operation's result before reporting integration complete.

   **Complete conflict recovery** when every region has a confirmed resolution, all conflicted files are resolved and staged, and the active integration operation has completed. If choices remain pending, report the unresolved regions and preserve the conflict state.

## Complete and verify the integration

A squash merge prepares changes but does not create a commit automatically. Before completing it:

1. Inspect `git diff --cached`, `git diff --cached --check`, and the staged file list with `git diff --cached --name-only`.
2. Confirm that the staged changes are limited to the reviewed integration scope and consider the relevant validation results.
3. Create one integration commit on the target branch, appending `(squash from <source-branch>)` to its subject.
4. Verify that the target branch contains the integrated changes and that the integration operation has completed.

For a regular merge or another integration method, verify that the operation completed and the target branch contains the intended changes.

Example squash commit subject for source branch `codex/fliggy-order`:

```text
feat(channelcore): add a Fliggy order adapter (squash from codex/fliggy-order)
```

**Complete integration** when the operation has finished and its result matches the reviewed integration scope. Preparing squash changes without creating the resulting commit does not complete integration.
