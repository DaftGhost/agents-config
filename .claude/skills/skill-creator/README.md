# skill-creator

Author and audit Agent Skills (`SKILL.md` files) for OpenCode and any agent that supports the [agentskills.io](https://agentskills.io) v1 spec — Claude Code, Cursor, Codex, Copilot, Gemini CLI, Goose, and 30+ others.

This is the source repo. The skill itself lives in [`SKILL.md`](SKILL.md) at the root.

## What's in the skill

- **[SKILL.md](SKILL.md)** — workflow for creating and auditing skills (lean, dense, ~200 lines / ~2.4k tokens)
- **[references/frontmatter.md](references/frontmatter.md)** — full field reference + platform-specific extensions
- **[references/design-patterns.md](references/design-patterns.md)** — problem-first vs tool-first, 5 common patterns, foundation skills
- **[references/pitfalls.md](references/pitfalls.md)** — top 13 community pitfalls with fixes
- **[references/validation.md](references/validation.md)** — 4 validators, CI integration, pre-commit hooks
- **[references/checklist.md](references/checklist.md)** — A/B/C tiered pre-publish checklist

## Install

### With [skillshare](https://github.com/runkids/skillshare)

```bash
skillshare install dewdad/skill-creator
```

Tracked install (preserves `.git` for updates):

```bash
skillshare install dewdad/skill-creator --track
```

Project-level install (into the current repo's skills directory):

```bash
skillshare install dewdad/skill-creator -p
```

Update later:

```bash
skillshare update skill-creator
```

### Manual

Clone into any of the locations your agent discovers:

```bash
# OpenCode global
git clone https://github.com/dewdad/skill-creator ~/.config/opencode/skills/skill-creator

# Cross-platform (Codex, Gemini CLI, OpenCode, Antigravity)
git clone https://github.com/dewdad/skill-creator ~/.agents/skills/skill-creator

# Claude-compatible
git clone https://github.com/dewdad/skill-creator ~/.claude/skills/skill-creator
```

Or install into a project's local skills directory:

```bash
git clone https://github.com/dewdad/skill-creator .opencode/skills/skill-creator
```

## When this skill triggers

Phrases like:
- "create a skill for this"
- "new SKILL.md"
- "audit this skill"
- "review my SKILL.md"
- "skill not triggering"
- "make this reusable across sessions"
- "improve skill description"

The skill teaches the agent to:
1. Wait for a real workflow before generalizing it into a skill (eval-driven dev).
2. Pick the right discovery path (`.opencode/`, `.agents/`, `.claude/`, etc.).
3. Write spec-compliant frontmatter with trigger keywords.
4. Use dense imperative voice, not polite prose.
5. Split into `references/` via progressive disclosure.
6. Validate with `skill-validator`, `skills-ref`, or `skillcheck` before publishing.
7. Test via the Claude-A-builds / Claude-B-tests loop.

## Validation

This skill passes:
- `skills-ref validate ./SKILL.md` → **Valid skill**
- `skillshare audit skill-creator` → **LOW risk (1/100)**, 100% auditable, 0 critical/high/medium/low findings

## Compatibility

Designed for OpenCode and any agent compatible with the agentskills.io v1 spec.

Tested with:
- OpenCode (primary)
- Claude Code
- Cursor
- VS Code Copilot

Frontmatter uses only open-spec fields (`name`, `description`, `license`, `compatibility`, `metadata`) for maximum portability. See [references/frontmatter.md](references/frontmatter.md) for platform-specific extensions if you need them.

## Provenance

Built from synthesized 2026 best practices across:
- [agentskills.io specification](https://agentskills.io/specification)
- [Anthropic Skills authoring best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Anthropic engineering blog: Equipping agents for the real world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [OpenCode Skills documentation](https://opencode.ai/docs/skills)
- [agent-ecosystem/skill-validator](https://github.com/agent-ecosystem/skill-validator)
- [Serghei Iakovlev — Agent Skills 101](https://blog.serghei.pl/posts/agent-skills-101/) (Feb 2026)
- [Strapi — What Are Agent Skills and How To Use Them](https://strapi.io/blog/what-are-agent-skills-and-how-to-use-them) (Feb 2026)

## License

Apache-2.0. See [LICENSE](LICENSE).
