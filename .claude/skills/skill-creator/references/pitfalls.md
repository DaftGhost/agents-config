# Pitfalls

## Contents
- Top 13 community pitfalls (ranked by frequency)
- Validator-detectable vs human-only
- Quick-fix table

Compiled from Anthropic's best-practices guide, Nate's "100+ people, same problems" Substack (Oct 2025), Serghei Iakovlev's practical guide (Feb 2026), and `agent-ecosystem/skill-validator` rule set.

## Top 13 pitfalls

### 1. Description without trigger keywords → skill never activates

**Symptom:** Skill is installed, agent has access, but it never fires.

**Cause:** Description like `Helps with documents` or `Useful for files`. The agent has nothing to match user intent against.

**Fix:** Rewrite with what + when + ≥3 quoted trigger phrases.

```yaml
# Before
description: Helps with PDFs.

# After
description: Extract text/tables from PDFs, fill forms, merge documents. Triggers on "extract PDF", "fill PDF form", "merge PDFs". Use when working with .pdf files.
```

Detectable by: `skill-validator` (heuristic), human review.

### 2. Missing or malformed YAML frontmatter

**Symptom:** Skill silently doesn't load.

**Cause:** Most common cause per claudedesignskills audit. SKILL.md must start at line 1 with `---`, contain valid YAML, end with `---`. Anything else (a `## Description` markdown section, BOM characters, leading whitespace) means the skill is invisible.

**Fix:**
```markdown
---
name: my-skill
description: ...
---

# Body starts here
```

Detectable by: any validator.

### 3. Second-person voice ("you should…")

**Symptom:** Skill loads but agent applies it inconsistently or misinterprets instructions.

**Cause:** "You should read X" reads like the agent is talking to a user, not following a procedure. Imperative voice ("Read X") is unambiguous.

**Fix:** Rewrite in imperative or third-person:
- Bad: "You should first check the schema."
- Good: "Check the schema." or "Begin by reading `schema.ts`."

Description specifically must be third-person:
- Bad: `description: I can help you process Excel files.`
- Good: `description: Processes Excel files. Use when…`

### 4. Angle brackets / XML tags in description

**Symptom:** Validator rejects, or some agents fail to parse.

**Cause:** `<` and `>` in YAML strings can break XML parsers downstream. Anthropic's spec explicitly bans XML tags in `name` and `description`.

**Fix:** Remove or escape. Use Markdown emphasis or quotes instead.

```yaml
# Bad
description: Use when running <build> or <test> commands.

# Good
description: Use when running build or test commands. Triggers on "build", "test", "compile".
```

Detectable by: any validator.

### 5. Bloated SKILL.md not split into references/

**Symptom:** Skill activates but bloats context. Token usage on every load is high.

**Cause:** SKILL.md exceeds ~500 lines / 5k tokens with detail that isn't needed for the common path.

**Fix:** Move detail to `references/`. Link with relative paths from SKILL.md. Keep references one level deep — don't chain `SKILL.md → a.md → b.md → c.md` (agents may only `head` chained refs).

### 6. Polite-prose padding on every load

**Symptom:** Higher token cost than needed. Slow context fill.

**Cause:** Prose like "First, take a look at..." and decorative blockquote callouts in SKILL.md body. The body loads on every activation; padding is paid for repeatedly.

**Fix:** Compress every step. Imperative voice. Drop blockquote scaffolding for the model. Keep prose for `references/` (loaded on demand).

```
# Padded (~75 tok)
> Note: Always verify schema is up to date.
First, take a look at the schema. You may need to compare it...

# Dense (~25 tok)
1. Read schema.ts. Compare against latest in migrations/. Flag column-type changes.
```

### 7. Scripts without `chmod +x`

**Symptom:** "Permission denied" when agent tries to run a script.

**Cause:** Forgot to set executable bit after creating Python/shell scripts.

**Fix:**
```bash
chmod +x scripts/*.py scripts/*.sh
```

Add to your skill init script or pre-commit hook.

Detectable by: `skill-validator check` flags non-executable script files.

### 8. Time-sensitive content

**Symptom:** Skill silently goes stale. Agent applies old patterns or refers to deprecated APIs.

**Cause:** Phrasing like "If before August 2025, use the old API." The model has no notion of "now" beyond conversation context.

**Fix:** Quarantine old patterns under a clearly-labelled section.

```markdown
## Current method
Use the v2 endpoint: api.example.com/v2/messages

## Old patterns (deprecated)
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used api.example.com/v1/messages. No longer supported.
</details>
```

### 9. Windows-style backslashes in paths

**Symptom:** Skill works on Windows agents, fails on Unix agents.

**Cause:** `scripts\helper.py` instead of `scripts/helper.py`. Forward slashes work on all platforms.

**Fix:** Always use forward slashes, even when authoring on Windows.

Detectable by: `skill-validator check`.

### 10. Voodoo constants (Ousterhout's law)

**Symptom:** Scripts fail in edge cases. Agent can't tune them.

**Cause:** Magic numbers in scripts (`TIMEOUT = 47`, `RETRIES = 5`) without explanation.

**Fix:** Document why every constant has its value.

```python
# Bad
TIMEOUT = 47

# Good
# HTTP requests typically complete within 30s.
# Longer timeout accounts for slow connections.
REQUEST_TIMEOUT = 30
```

If you don't know the right value, the agent won't either.

### 11. Punting errors to the agent

**Symptom:** Scripts crash on common failure modes; agent has to recover with imperfect information.

**Cause:** `def process_file(path): return open(path).read()` — fails on missing file, permission errors, etc.

**Fix:** Handle errors explicitly with helpful messages.

```python
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, "w") as f:
            f.write("")
        return ""
    except PermissionError:
        print(f"Cannot access {path}, using default")
        return ""
```

Make validation scripts especially verbose: `"Field 'signature_date' not found. Available: customer_name, order_total, signature_date_signed"` beats `"validation failed"`.

### 12. Trusting community skills without auditing

**Symptom:** Strange agent behavior, prompt-injection-shaped failures, or worse.

**Cause:** Public skill registries are unmoderated. Much circulating content is AI-generated and unverified — vague instructions, incorrect patterns, plausible-sounding procedures that fail in practice. Some are actively malicious.

**Fix:** Before installing any external skill, read the SKILL.md yourself. Check:
- Does the description follow trigger patterns or just summarize?
- Are instructions procedural or just documentation?
- Do bundled scripts actually exist and do what they claim?
- Any external URLs the script fetches from?
- Any unusual file access patterns?

Treat skills like installing software. Trust scope = source trust × audit depth.

### 13. Cross-agent silent failures

**Symptom:** Skill works on one agent, breaks on another in the same team.

**Cause:** Used Claude-Code-specific frontmatter (`disable-model-invocation`, `model:`, `hooks:`) on a skill shared with Cursor, Codex, or OpenCode. The fields are silently ignored — the skill loads, but invocation behavior differs unpredictably.

**Fix:** Decide your portability target up front:
- Multi-agent → stick to open spec only (`name`, `description`, `license`, `compatibility`, `metadata`).
- Claude Code only → fine to use full frontmatter.
- Document the target in `compatibility`.

## Validator-detectable vs human-only

| Pitfall | Auto-detectable | Tools |
|---|---|---|
| 1. No trigger keywords | Heuristic | skill-validator (LLM judge) |
| 2. Missing/malformed YAML | Yes | all validators |
| 3. Second-person voice | Heuristic | skill-validator (LLM judge) |
| 4. XML tags in fields | Yes | skills-ref, skill-validator |
| 5. Bloated SKILL.md | Yes (token count) | skill-validator |
| 6. Padding | No | manual review |
| 7. Scripts not executable | Yes | skill-validator |
| 8. Time-sensitive content | No | manual review |
| 9. Windows paths | Yes | skill-validator |
| 10. Voodoo constants | No | code review |
| 11. Punting errors | No | code review |
| 12. Untrusted source | No | manual audit |
| 13. Cross-agent fields | Partial | skill-validator (warns) |

Use validators for the auto-detectable set. Reserve human review for the rest.
