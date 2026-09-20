# Pre-publish Checklist

## Contents
- A. Minimum bar (every skill)
- B. Shareable skills (publishing externally or to a team)
- C. High-stakes / destructive skills
- D. After publishing
- Quick sanity questions
- Related references

Run through every item before shipping a skill. Group A is the minimum bar; group B is for shareable skills; group C is for high-stakes skills.

## A. Minimum bar (every skill)

### Frontmatter
- [ ] `name` matches folder name exactly (case-sensitive)
- [ ] `name` regex: lowercase + digits + single hyphens, 1–64 chars
- [ ] `name` not in reserved list (`anthropic`, `claude`)
- [ ] `description` is 1–1024 chars, third-person voice
- [ ] `description` includes both **what** and **when**
- [ ] `description` includes ≥3 specific trigger phrases
- [ ] No XML tags or angle brackets in `name` or `description`
- [ ] YAML frontmatter starts at line 1 with `---`
- [ ] All required fields present, all optional fields valid

### Body
- [ ] Imperative voice ("Read X. Run Y."), not second-person ("You should…")
- [ ] Dense format — no polite-prose padding, no decorative blockquotes
- [ ] ≤500 lines / ~5k tokens
- [ ] No time-sensitive content (or quarantined under "Old patterns")
- [ ] Consistent terminology throughout
- [ ] Concrete examples, not abstract placeholders
- [ ] Forward-slash paths only (no `\`)

### References
- [ ] Reference files one level deep from SKILL.md (no chained refs)
- [ ] Files >100 lines have a TOC at top
- [ ] All `[text](path)` links resolve

### Scripts (if any)
- [ ] `chmod +x` on every executable script
- [ ] Explicit error handling (no punting to the agent)
- [ ] Constants documented (no voodoo numbers)
- [ ] Required packages listed in SKILL.md or `compatibility`
- [ ] Forward-slash paths

### Validation
- [ ] `skill-validator check --strict` passes (or `npx skills-ref validate` if you prefer the lighter check)
- [ ] No validator warnings (or each is justified in a comment)

### Testing
- [ ] At least 3 evaluations defined: gap-finder, gap-closer, transfer
- [ ] Tested with a fresh session (Claude-B pattern)
- [ ] Tested with the model(s) you'll use it with (Haiku/Sonnet/Opus differ)
- [ ] Trigger fires on natural user phrasing, not just the literal description

## B. Shareable skills (publishing externally or to a team)

### Metadata
- [ ] `license` field set
- [ ] `metadata.version` set (semver or date-based)
- [ ] `metadata.author` or team ownership documented
- [ ] `compatibility` field describes any non-trivial requirements

### Documentation
- [ ] SKILL.md states the skill's purpose in one line near the top
- [ ] Common pitfalls / gotchas documented if non-obvious
- [ ] External dependencies (other skills, MCPs, packages) listed

### Portability
- [ ] Stuck to open-spec frontmatter only, OR explicitly documented single-vendor target
- [ ] Stored in `.agents/skills/` if multi-agent reuse expected
- [ ] No platform-specific paths in scripts (use env vars or relative paths)

### Quality
- [ ] LLM-as-judge score (`skill-validator score`) ≥ team threshold, if used
- [ ] Peer-reviewed by at least one other person
- [ ] Tested by someone other than the author

## C. High-stakes / destructive skills

For skills that deploy, delete, mass-modify, or otherwise take irreversible actions.

### Invocation control (Claude Code / VS Code Copilot)
- [ ] `disable-model-invocation: true` so the agent won't auto-trigger
- [ ] User must explicitly run `/skill-name` to activate
- [ ] For Codex: `agents/openai.yaml` with `policy.allow_implicit_invocation: false`

### Safety patterns
- [ ] Plan-validate-execute structure (don't act until validation passes)
- [ ] Verifiable intermediate output (e.g., `changes.json` before applying)
- [ ] Explicit confirmation step ("Run validate.py and review output before proceeding")
- [ ] Rollback or undo path documented
- [ ] `allowed-tools` field restricts to minimum needed tools

### Audit trail
- [ ] Skill logs what it does (timestamp, action, target)
- [ ] Critical operations have a dry-run mode
- [ ] Failure modes documented with recovery steps

### Security
- [ ] No external URL fetches (or all URLs are pinned and audited)
- [ ] Scripts don't elevate privileges
- [ ] No credential exfiltration paths
- [ ] Reviewed for prompt-injection resistance if processing user content

## D. After publishing

- [ ] Track real-usage failures and feed back into iteration
- [ ] Update `metadata.version` on each non-trivial change
- [ ] Maintain a CHANGELOG if frequently revised
- [ ] Re-run validators on every change
- [ ] Re-test the 3 evaluations on every non-trivial change

## Quick sanity questions

If you can't answer "yes" to all of these, fix it before publishing:

1. Could a teammate read this SKILL.md cold and execute the workflow correctly?
2. Does the description make it obvious when *not* to use this skill?
3. If I removed any one section, would the skill still work for the common case?
4. Have I tested at least one case where the skill should NOT trigger, and confirmed it doesn't?
5. Is the most fragile step protected by validation before it runs?

## Related references

- `frontmatter.md` — full frontmatter rules and examples
- `pitfalls.md` — top 13 community pitfalls (what to specifically avoid)
- `validation.md` — validator setup and CI integration
- `design-patterns.md` — choosing the right structure
