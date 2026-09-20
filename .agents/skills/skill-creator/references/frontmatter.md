# Frontmatter Reference

## Contents
- Open spec fields (portable across all skills-compatible agents)
- Platform-specific extensions (Claude Code, VS Code Copilot, Codex)
- Convention fields (tooling-only, agents ignore)
- Worked examples by portability target

## Open spec fields

These are defined by the agentskills.io v1 spec and supported across all skills-compatible agents.

### `name` (required)

- 1–64 characters
- Regex: `^[a-z0-9]+(-[a-z0-9]+)*$` (lowercase alphanumeric + single hyphens)
- Must not start or end with `-`, must not contain `--`
- Must match the parent directory name exactly (case-sensitive)
- Reserved words forbidden by Anthropic: `anthropic`, `claude`. A mismatch silently prevents loading on several platforms.

Naming conventions (community + Anthropic guidance):
- Prefer gerund: `processing-pdfs`, `analyzing-spreadsheets`
- Or action-first: `process-pdfs`, `analyze-spreadsheets`
- Or noun-phrase: `pdf-processing`
- Avoid: `helper`, `utils`, `tools`, `documents`, `data`, `files` (vague), `claude-tools`, `anthropic-helper` (reserved)

### `description` (required)

- 1–1024 characters
- Non-empty
- No XML tags or angle brackets (`<`, `>`) — these break some validators and risk prompt-injection patterns
- Third-person voice. Not "I can help you with X" or "You can use this to X" — use "Processes X. Use when…"
- Must answer **what** the skill does AND **when** to use it
- Should include ≥3 specific trigger phrases or keywords
- This is the only field agents read for activation. There is no separate `triggers:` field that controls activation.

Effective patterns:
```yaml
description: Extract text and tables from PDFs, fill forms, merge documents. Triggers on "extract PDF", "fill form", "merge PDFs". Use when working with .pdf files.

description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes. Triggers on "commit message", "what should I commit", "review staged changes".

description: Automate Apple Calendar with AppleScript. Create events, search by date range, query multiple calendars. Use when user asks about calendars, events, schedules, appointments, or meetings. Requires applescript-foundation skill.
```

Ineffective:
```yaml
description: Helps with documents.        # vague, no when
description: Does stuff with files.       # vague
description: I can help you process Excel files.  # first-person
description: You can use this to deploy.  # second-person
```

### `license` (optional)

Either a license name or a reference to a bundled `LICENSE` file. Recommended for shareable skills.

```yaml
license: Apache-2.0
license: MIT
license: Proprietary. See LICENSE.txt for terms.
```

### `compatibility` (optional)

Max 500 chars. Document genuine environment requirements. Most skills don't need this.

```yaml
compatibility: Designed for OpenCode and Claude Code
compatibility: Requires Python 3.11+, git, and network access
compatibility: Requires applescript-foundation skill on macOS
```

### `metadata` (optional)

Arbitrary string-to-string map. Tooling-friendly. Use for version, author, changelog, ownership.

```yaml
metadata:
  version: "2.0"
  author: example-org
  changelog: docs/CHANGELOG.md
  team: platform-engineering
```

Use reasonably unique key names to avoid conflicts with other tooling.

### `allowed-tools` (optional, experimental)

Space-separated string of pre-approved tools. Support varies by agent — Claude Code full, Gemini CLI partial, others ignore. Treat as advisory.

```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read Grep
```

## Platform-specific extensions (single-vendor only)

These are NOT in the open spec. Use only when you've explicitly chosen a single-vendor target.

### Claude Code + VS Code Copilot

`disable-model-invocation: true` — agent never auto-loads. Description is dropped from context. Invocation is manual via `/skill-name`. Use for destructive or high-stakes operations: production deploys, force pushes, mass deletions, end-of-sprint checklists.

`user-invocable: false` — user cannot trigger from slash-command picker. Use for background-knowledge skills the model should pull autonomously but users have no reason to trigger directly.

The 2×2 matrix:

| | user-invocable: true | user-invocable: false |
|---|---|---|
| **disable-model-invocation: false** (default) | Both auto and manual (default) | Auto only |
| **disable-model-invocation: true** | Manual only | Neither (do not ship) |

### Claude Code only

`model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`, `argument-hint`, `arguments`, `when_to_use` — Claude-Code-specific. See https://code.claude.com/docs/en/skills for current semantics. Surface evolves.

### Codex

Invocation control is NOT in SKILL.md frontmatter. Codex uses a separate `agents/openai.yaml` with `policy.allow_implicit_invocation: false`. Ship both if cross-targeting Codex and Claude Code.

## Convention fields (tooling-only, agents ignore)

These are not in any spec. Agents do not read them for activation. They exist for skill catalogs and external tooling.

`tags: [security, compliance, audit]` — categorization for catalogs.

`triggers: ["phrase 1", "phrase 2"]` — explicit activation phrases for documentation. **Agents do not use this for activation.** If you want phrases to trigger your skill, put them in `description`. The `triggers` field is purely for human-readable indexes.

## Examples by portability target

### Spec-level portability (works on all 40+ skills-compatible agents)

```yaml
---
name: security-audit
description: |
  Run security reviews and vulnerability assessments. Use when reviewing code for security issues,
  performing OWASP Top 10 checks, scanning dependencies, or detecting secrets.
  Triggers on "security review", "OWASP", "vulnerability scan", "dependency audit".
license: MIT
---
```

### Cross-platform with optional metadata

```yaml
---
name: architecture-review
description: |
  Review system architecture, evaluate design patterns, audit module boundaries.
  Use when reviewing architectural decisions, evaluating service boundaries, or auditing dependencies.
  Triggers on "architecture review", "design pattern review", "module boundary".
license: Apache-2.0
compatibility: Read-only operations; no file modification
metadata:
  version: "1.2"
  author: platform-team
allowed-tools: Read Grep Glob
---
```

### Claude Code single-vendor, manual-only deploy checklist

```yaml
---
name: production-release
description: Walk through the production release checklist for the payments service.
disable-model-invocation: true
allowed-tools: Read Bash
---
```

The agent will not auto-load this skill — the user must explicitly invoke `/production-release`.

## Validation

All these field rules are enforced (with varying strictness) by:
- `skill-validator check --strict` — full check including unknown-field warnings
- `skills-ref validate` — spec compliance only
- `skillcheck` — Python validator with cross-agent issue detection

See `validation.md` for setup.
