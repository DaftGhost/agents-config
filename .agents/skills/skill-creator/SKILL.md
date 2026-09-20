---
name: skill-creator
description: |
  Create and audit Agent Skills (SKILL.md files). Covers frontmatter, progressive disclosure, trigger-keyword design, validation, and common pitfalls. Triggers when the user asks to create, audit, or fix a SKILL.md.
compatibility: DSH (DeepSeek Harness) & other agentskills.io-compatible agents
whenToUse: 'Applies to any skill authoring, review, or maintenance request, including activation problems.'
---

# Skill Creator

Build a skill once. Reuse it across sessions, repos, and agents. This skill encodes the 2026 author + audit playbook.

## When to use

- User says "create a skill for this" after completing a workflow with you.
- User wants to audit, improve, or fix a `SKILL.md`.
- User reports "skill won't trigger" or "skill bloats context".

If the user asks up front "create a skill for X" with no prior workflow, ask them to do the task once first, then invoke this skill at the end. Skills built without a real-task baseline encode imagined needs, not real ones (Anthropic's evaluation-driven development pattern).

## Core mental model

A skill is a folder containing `SKILL.md` plus optional `scripts/`, `references/`, `assets/`. Agents load it in three phases:

1. **Discovery** (~100 tok per skill, always loaded): YAML `name` + `description`.
2. **Activation** (≤5k tok recommended, loaded when matched): full SKILL.md body.
3. **Resources** (loaded on demand): files in `references/`, `scripts/`, `assets/`.

Optimize ruthlessly for the discovery and activation phases. Resources are effectively free.

## Workflow

### 1. Decide the skill type

Pick the design framing that matches the task. See [design-patterns.md](references/design-patterns.md).

- **Problem-first**: user describes an outcome → skill orchestrates tools. Sequential workflow.
- **Tool-first**: capability already exists → skill teaches conventions. Reference + decision tree.

### 2. Pick the location

| Path | Scope | Use when |
|---|---|---|
| `.opencode/skills/<name>/` | project, OpenCode-only | repo-specific, OpenCode users only |
| `.agents/skills/<name>/` | project, cross-platform | repo-specific, multi-agent team (Codex, Gemini CLI, OpenCode) |
| `.claude/skills/<name>/` | project, Claude-compatible | repo-specific, Claude Code users |
| `~/.config/opencode/skills/<name>/` | global, OpenCode | personal, OpenCode-only |
| `~/.agents/skills/<name>/` | global, cross-platform | personal, multi-agent |
| `~/.claude/skills/<name>/` | global, Claude-compatible | personal, Claude-compatible |

Project skills override personal skills override extension skills when names collide.

For shareable skills, prefer `.agents/skills/` — emerging cross-platform convention adopted by OpenCode, Codex, Gemini CLI, Antigravity.

### 3. Write the frontmatter

Required: `name`, `description`. Recognized by OpenCode: `license`, `compatibility`, `metadata`. Optional/experimental: `allowed-tools`. Full reference + platform-specific extensions: [frontmatter.md](references/frontmatter.md).

```yaml
---
name: skill-name
description: |
  [What it does in one line.] Triggers on: "[phrase 1]", "[phrase 2]", "[phrase 3]".
  Use when [specific context]. [Optional: alternative-to disambiguation.]
license: Apache-2.0
---
```

**Name** rules: `^[a-z0-9]+(-[a-z0-9]+)*$`, 1–64 chars, must match folder name, no reserved words (`anthropic`, `claude`). Prefer gerund (`processing-pdfs`) or action-first (`process-pdfs`). Avoid `helper`, `utils`, `tools`.

**Description** rules: 1–1024 chars, third-person, no XML tags or angle brackets, includes both *what* and *when*, with ≥3 quoted trigger phrases. The description is the trigger — agents do not read a `triggers:` field for activation, only `description`.

Bad: `description: Helps with documents.`
Good: `description: Extract text and tables from PDFs, fill forms, merge documents. Triggers on "extract PDF", "fill form", "merge PDFs". Use when working with .pdf files.`

### 4. Write the body — dense format

Frequently-loaded SKILL.md bodies are paid for in tokens on every activation. Cut padding.

**Padded** (~75 tokens, polite prose):
```
> Note: Before generating a migration, you should always verify
> that the schema file is up to date.
First, take a look at the current schema, which lives in `src/db/schema.ts`.
You may need to compare it against the latest migration file...
```

**Dense** (~25 tokens, same procedure):
```
1. Read `src/db/schema.ts`. Compare against latest in `drizzle/migrations/`. Flag column-type changes and renames.
2. Run `npx drizzle-kit generate`.
```

Use imperative voice ("Read X. Run Y."), not second person ("You should read X..."). Drop blockquote scaffolding, redundant section headers, and explanations of things the model already knows. Reserve discursive prose for `references/` files (loaded on demand).

### 5. Split via progressive disclosure

If SKILL.md exceeds ~500 lines / 5k tokens, split. Move detail into `references/`. Link with relative paths. Keep references **one level deep** from SKILL.md — agents may only `head` files reached by chained references.

Add a TOC at the top of any `references/*.md` file longer than 100 lines so agents can plan partial reads.

### 6. Add scripts only when reliability matters

Bundle `scripts/` for deterministic operations (validation, parsing, formatting) where token-generating equivalent code would be unreliable or wasteful. Make execution intent explicit:

- "Run `scripts/validate.py`" → execute.
- "See `scripts/validate.py` for the algorithm" → read as reference.

Always: forward-slash paths, `chmod +x`, explicit error handling (don't punt to the agent), no voodoo constants. Declare runtime requirements in `compatibility` or in SKILL.md.

### 7. Validate before publishing

```bash
# Spec compliance + link resolution + token counts + quality scoring
brew install agent-ecosystem/tap/skill-validator
skill-validator check --strict ./path/to/skill

# Or, lighter spec-only check
npx skills-ref validate ./path/to/skill/SKILL.md

# Or, Python option
pip install skillcheck && skillcheck ./path/to/skill
```

See [validation.md](references/validation.md) for CI integration, pre-commit hooks, and full validator option matrix.

### 8. Test with real tasks

Three evaluations minimum, per Anthropic's eval-driven development:
1. Run a representative task **without** the skill — note failures.
2. Install skill, run same task — confirm gaps closed.
3. Run a related but unseen task — confirm trigger fires and instructions transfer.

Test with the models you'll use (Haiku/Sonnet/Opus differ on how much guidance they need).

### 9. Iterate via Claude-A / Claude-B loop

Use one session ("A") to author the skill. Test it in a fresh session ("B") on real tasks. Observe where B struggles. Bring concrete observations back to A: "B forgot to filter test accounts when generating the regional report — make that rule more prominent." Repeat.

## Common pitfalls

Top issues from community deployments (full list with fixes: [pitfalls.md](references/pitfalls.md)):

1. Description without trigger keywords → skill never activates.
2. Missing or malformed YAML frontmatter (must be lines 1–N starting with `---`).
3. Second-person voice ("you should…") instead of imperative.
4. Angle brackets or XML tags in `description` (rejected by validators).
5. Bloated SKILL.md not split into `references/`.
6. Scripts without `chmod +x`.
7. Polite-prose padding inflating token cost on every load.
8. Time-sensitive content ("after Aug 2025…") that goes stale.
9. Windows-style backslashes in paths.
10. Trusting community skills without auditing them — much circulating content is AI-generated and unreliable.

## Pre-publish checklist

Concrete verification before shipping. Full version: [checklist.md](references/checklist.md).

- [ ] `name` matches folder, lowercase-hyphen, ≤64 chars, no reserved words
- [ ] `description` 3rd-person, what + when + ≥3 trigger phrases, ≤1024 chars, no `<>`
- [ ] SKILL.md body dense, imperative, ≤500 lines
- [ ] References one level deep, forward slashes, TOC on files >100 lines
- [ ] Scripts: `chmod +x`, explicit errors, documented constants
- [ ] No time-sensitive info (or quarantined under "Old patterns")
- [ ] Validated with `skill-validator check --strict` (or equivalent)
- [ ] Tested across 3 evaluations on the models you'll use
- [ ] For destructive ops: consider `disable-model-invocation: true`
- [ ] Audited if shared from a third party

## Skills vs. neighbors

| Construct | Trigger | Use for |
|---|---|---|
| Skill | model-invoked via description | Procedural how-to |
| AGENTS.md / custom instructions | always-on | Project context, conventions |
| Slash command / prompt file | user-invoked | Templates, one-offs |
| MCP server | tool call | External connectivity |
| Subagent | delegation | Parallel specialized reasoning |

Skills tell the agent **how to do something**. AGENTS.md tells it **what the project is**. MCP gives it **what to call**. They compose.

## Credentials (only if needed)

If your skill requires credentials, add an `.env.example` listing variables (no real values), an `.env` (gitignored) with the real values, and a `.gitignore` that excludes `.env`. Most skills don't need this — skip it unless your scripts authenticate to an external service.

## References

Loaded on demand:
- [frontmatter.md](references/frontmatter.md) — full field reference, platform-specific extensions, examples by portability target
- [design-patterns.md](references/design-patterns.md) — problem-first vs tool-first, three skill categories, common patterns
- [pitfalls.md](references/pitfalls.md) — top 13 community pitfalls with fixes
- [validation.md](references/validation.md) — validators, CI integration, pre-commit hooks
- [checklist.md](references/checklist.md) — full pre-publish checklist

## External

- OpenCode skills docs: https://opencode.ai/docs/skills
- Open standard: https://agentskills.io/specification
- Anthropic best practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- Examples: https://github.com/anthropics/skills
