# Validation

## Contents
- Tool comparison
- skill-validator (recommended) — install + use
- skills-ref (lightweight)
- skillcheck (Python)
- Manual review checklist
- Pre-commit hooks
- CI integration

## Tool comparison

| Tool | Language | Install | Strengths | Best for |
|---|---|---|---|---|
| `skill-validator` | Go | `brew install agent-ecosystem/tap/skill-validator` | Spec + link resolution + token counts + LLM-as-judge scoring + 13 platform pre-commit hooks | Pre-publish, CI |
| `skills-ref` | Node | `npx skills-ref validate ...` | Reference impl from agentskills.io. Spec compliance only. | Quick spec check |
| `skillcheck` | Python | `pip install skillcheck` | Cross-agent issue detection | Python pipelines |
| Manual | — | — | Catches things validators can't (voodoo constants, padding, time-sensitive content) | After tool checks pass |

Run `skill-validator` for the auto-detectable set, then do a manual pass for the rest.

## skill-validator

The most thorough option. Source: https://github.com/agent-ecosystem/skill-validator

### Install

```bash
# Homebrew (macOS, Linux)
brew tap agent-ecosystem/tap
brew install skill-validator

# Go
go install github.com/agent-ecosystem/skill-validator/cmd/skill-validator@latest

# Source
git clone https://github.com/agent-ecosystem/skill-validator.git
cd skill-validator && go build -o skill-validator ./cmd/skill-validator
```

### Use

```bash
# Full check (spec + links + token counts + structure)
skill-validator check ./my-skill

# Strict mode (warnings → errors, exit 1)
skill-validator check --strict ./my-skill

# Spec compliance only
skill-validator validate structure ./my-skill

# Skip orphan-file detection
skill-validator validate structure --skip-orphans ./my-skill

# Allow non-spec frontmatter (for Claude Code extensions)
skill-validator validate structure --allow-extra-frontmatter ./my-skill

# Allow flat layouts (no scripts/references/assets dirs)
skill-validator validate structure --allow-flat-layouts ./my-skill

# Custom subdirectories
skill-validator validate structure --allow-dirs=evals,testing ./my-skill
```

### Exit codes

- `0` — pass
- `1` — error (or warning under `--strict`)
- `2` — warning (under default mode)

### LLM-as-judge scoring

Optional. Scores skills on clarity, actionability, novelty. Requires LLM credentials.

```bash
export ANTHROPIC_API_KEY=...
skill-validator score ./my-skill
```

Useful for skill libraries where you want a quality bar before publishing.

### What it checks

- Frontmatter: required fields present, types correct, char limits respected, no XML tags
- Name regex compliance + folder match
- Description: non-empty, length, no XML tags
- Internal link resolution (no broken `[text](references/x.md)`)
- Token counts per file (warns if SKILL.md > 5k tokens)
- Skill ratio (instructions vs decoration)
- Code fence integrity
- Orphan files (in skill folder but unreferenced)
- Cross-language contamination (e.g., Python deps used but not declared)
- File permissions (scripts executable)
- Forward-slash paths

## skills-ref

Spec-compliance check from the agentskills.io reference library.

```bash
npx skills-ref validate ./my-skill/SKILL.md
```

Faster than `skill-validator`, narrower scope. Good for tight loops while authoring.

## skillcheck

Python-based linter; catches cross-agent issues.

```bash
pip install skillcheck
skillcheck ./my-skill
skillcheck path/to/skills/dir  # batch
```

## Manual review

Things validators can't catch. Skim every skill for:

- **Voodoo constants** in scripts (`TIMEOUT = 47`, `RETRIES = 5` without justification).
- **Punting** (errors raised without recovery).
- **Time-sensitive content** ("after Aug 2025…").
- **Polite-prose padding** in SKILL.md body.
- **Too many options** offered without a default.
- **Verbose explanations of things the model already knows** ("PDF stands for Portable Document Format and is a common file format…").
- **Cross-skill drift** — terminology that contradicts a foundation skill it depends on.
- **Untrusted external fetches** (URLs in scripts pointing at sources the user doesn't control).

## Pre-commit hooks

`skill-validator` ships hooks for 13 platforms. Each picks the right skill directory automatically.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/agent-ecosystem/skill-validator
    rev: v0.5.0
    hooks:
      - id: skill-validator-claude    # validates .claude/skills/
      # other available hooks:
      #   skill-validator-amp
      #   skill-validator-cline
      #   skill-validator-codex
      #   skill-validator-copilot
      #   skill-validator-cursor
      #   skill-validator-gemini
      #   skill-validator-goose
      #   skill-validator-kiro
      #   skill-validator-mistral-vibe
      #   skill-validator-roo-code
      #   skill-validator-trae
      #   skill-validator-windsurf
```

Generic hook with custom path:

```yaml
- id: skill-validator
  args: ["check", ".opencode/skills/"]
```

For OpenCode specifically, use the generic hook pointing at `.opencode/skills/` (no dedicated hook ships yet).

## CI integration

GitHub Actions example:

```yaml
# .github/workflows/skills.yml
name: Validate Skills
on:
  pull_request:
    paths:
      - '.opencode/skills/**'
      - '.agents/skills/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install skill-validator
        run: |
          go install github.com/agent-ecosystem/skill-validator/cmd/skill-validator@latest
      - name: Validate all skills
        run: |
          for skill in .opencode/skills/*/ .agents/skills/*/; do
            [ -d "$skill" ] || continue
            echo "Validating $skill"
            skill-validator check --strict "$skill"
          done
```

Failure on `--strict` blocks the PR. Without `--strict`, warnings are non-blocking but visible in logs.

## Local development loop

Tightest feedback while authoring:

```bash
# Watch mode (using entr or fswatch)
ls .opencode/skills/my-skill/**/*.md | entr -c skill-validator check .opencode/skills/my-skill
```

Or simply:

```bash
alias skv='skill-validator check --strict'
skv .opencode/skills/my-skill
```

## When validation passes but skill still doesn't work

Validation is necessary, not sufficient. If your skill is spec-compliant but won't trigger:

1. Re-read the description as if you're the agent. Does it match the user's natural phrasing?
2. Check for skill-name collisions (project-level wins over personal; an unrelated skill with the same name elsewhere can shadow yours).
3. Check OpenCode permission rules (`opencode.json` `permission.skill` block) — your skill may be `deny`-ed.
4. Run `opencode --debug` (or equivalent) to see skill-loading errors at startup.
5. Test in a fresh session — old sessions may not pick up new skills.
