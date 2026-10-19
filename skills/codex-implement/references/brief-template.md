# Codex Task Brief

Write the brief to `<run-dir>/brief.md` before launching Codex. Codex does not see the conversation, so the brief must stand on its own. Keep it short enough to read in one pass and specific enough that a different engineer could verify the result.

```markdown
# Task brief

## Objective
<What must be built, fixed, or changed, and why.>

## Acceptance criteria
- [ ] <Observable behavior: input, action, expected result.>
- [ ] <Another criterion.>
- [ ] <Validation command that must pass.>

## Scope
- Modify: <files or directories>
- Do not modify: <files or directories that are out of scope>
- Do not commit, push, or change Git history.
- Do not install dependencies unless <allowed / explicitly listed>.
- Ignore unrelated skills and plugins; follow only this brief.
- Preserve existing uncommitted changes in the working tree.

## Context
- Relevant files: <paths and what they do>
- Current behavior: <what happens today>
- Constraints: <compatibility, style, performance, or data constraints>
- Decisions already made: <anything Codex must not re-decide>

## Validation
Run:
- `<command>` - expected: <result>
- `<command>` - expected: <result>

## If blocked
If a required product rule, credential, or destructive action is missing, stop and explain what is missing. Do not invent a rule or broaden the change.

## Final response
End with:
1. Files changed and why.
2. Validation commands and actual results.
3. Anything incomplete, uncertain, or outside the requested scope.
```

## Rules for the supervising agent

- Put every requirement that matters in the acceptance criteria. Codex cannot ask follow-up questions.
- Name the allowed files and the forbidden files explicitly; "do the right thing" is not a boundary.
- Include the exact validation commands the main agent will run later. If the project has no test command, say so and define a concrete manual check.
- Do not include secrets, tokens, or credentials.
- For a resume, write a new brief with the failing command, its output, what must change, and what must not change. Do not simply repeat the original brief.
