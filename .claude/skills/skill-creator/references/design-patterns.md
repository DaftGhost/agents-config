# Design Patterns

## Contents
- Two design framings (problem-first, tool-first)
- Three skill categories
- Degrees of freedom (when to be specific vs flexible)
- Five common patterns
- Foundation skills (cross-skill referencing)

## Two design framings

Skills emerge from two directions. Recognizing which one you're starting from prevents wasted effort.

### Problem-first

Start from the user's goal. "I need to set up a new project workspace." The skill orchestrates whatever tools are needed to accomplish the outcome. The user describes what they want; the skill handles how.

Tend toward sequential workflows with clear phases. Examples:
- Project bootstrap
- Multi-step research synthesis
- Release / deploy flows
- End-to-end testing

### Tool-first

Start from an available capability. "We have a Jira MCP server connected." The skill teaches the agent your team's conventions for using it effectively. The user has access; the skill provides expertise.

Tend toward reference patterns + decision trees. Examples:
- Jira workflow conventions on top of a Jira MCP
- Database schema knowledge on top of a SQL connection
- Brand-guideline application on top of generic doc creation

Most skills lean one way. Knowing which helps you choose the right structure.

## Three skill categories

| Category | Shape | Example |
|---|---|---|
| **Workflow** | Sequential, numbered steps with verification points | "Create a new API endpoint" |
| **Reference / expertise** | Decision trees, rules, conventions, examples | "Apply our brand guidelines" |
| **Capability** | Wraps deterministic scripts as tools | "Validate OOXML structure" |

A skill can blend categories, but biasing toward one keeps the structure clean.

## Degrees of freedom

Match specificity to task fragility. From Anthropic's best-practices guide:

### High freedom — text-based instructions

When multiple approaches are valid and decisions depend on context.

```
## Code review process
1. Analyze structure and organization
2. Check for bugs and edge cases
3. Suggest readability improvements
4. Verify project conventions
```

### Medium freedom — pseudocode + parameters

When a preferred pattern exists but configuration affects behavior.

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```

### Low freedom — exact scripts

When operations are fragile and consistency is critical.

```bash
## Database migration
Run exactly this:
python scripts/migrate.py --verify --backup

Do not modify the command or add additional flags.
```

**Analogy.** Narrow bridge with cliffs → low freedom. Open field → high freedom. Match the freedom level to the actual hazard.

## Five common patterns

### 1. Template pattern (strict or flexible)

Strict — when output format is contractual (API responses, data formats):

```markdown
ALWAYS use this exact structure:

# [Title]
## Executive summary
[One-paragraph overview]
## Key findings
- Finding 1
- Finding 2
## Recommendations
1. ...
2. ...
```

Flexible — when adaptation is useful:

```markdown
Sensible default; adjust for the specific analysis:

# [Title]
## Executive summary
[Overview]
## Key findings
[Adapt sections based on what you discover]
```

### 2. Examples pattern

For style-sensitive output, provide input/output pairs.

```
Input: Added user authentication with JWT tokens
Output:
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

Examples teach style faster than rules.

### 3. Conditional workflow pattern

Guide through decision points.

```markdown
1. Determine modification type:
   - Creating new content? → Creation workflow below
   - Editing existing content? → Editing workflow below

2. Creation workflow:
   - Use docx-js
   - Build from scratch
   - Export to .docx

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

### 4. Plan-validate-execute pattern

For batch / destructive operations: have the agent first produce a plan file, validate it deterministically, then execute. Catches errors before damage.

```markdown
1. Run scripts/analyze.py → fields.json (the plan)
2. Run scripts/validate.py fields.json (the gate)
3. If validation fails: fix fields.json, re-validate.
4. Only when validation passes: run scripts/apply.py fields.json
5. Run scripts/verify.py to confirm result
```

### 5. Feedback loop pattern

Validator → fix errors → repeat. Improves output quality dramatically.

```markdown
1. Make edits to word/document.xml
2. Validate immediately: scripts/validate.py unpacked_dir/
3. If validation fails:
   - Read the error
   - Fix the XML
   - Re-validate
4. Only proceed when validation passes
5. Rebuild: scripts/pack.py
```

## Foundation skills (cross-skill referencing)

When multiple skills share procedural knowledge, factor the common part into a foundation skill that the others reference.

Example from this user's library: `applescript-foundation` contains AppleScript date formatting, whose-clause filtering, error handling, and timeout configuration. Skills `macos-calendar`, `macos-mail`, `macos-notes`, etc. each list `Requires applescript-foundation skill` in their `compatibility` field and link to it from SKILL.md.

How to do this:

1. Identify procedural knowledge repeated across ≥3 skills.
2. Extract into a new foundation skill.
3. Each consuming skill:
   - Adds `compatibility: Requires <foundation> skill` to frontmatter
   - Links to it in SKILL.md body: `See [foundation-name skill] for shared patterns`
4. Foundation skill keeps its own SKILL.md focused on what it provides.

Foundation skills are descriptive, not enforced — agents won't auto-load the foundation when activating a consumer. The dependency is documentation. Consumers should restate critical rules they depend on, not rely on the agent to chase the link.

## Anti-patterns

- **Skills that present too many options.** "Use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or…" → pick a default with one escape hatch.
- **Skills that cover too much.** A "do everything with Excel" skill becomes hard to trigger correctly. Split by task: `analyzing-spreadsheets`, `generating-charts`, `formula-debugging`.
- **Skills that duplicate AGENTS.md.** Skills are procedural how-tos. Project context belongs in AGENTS.md.
- **Skills bundled with massive always-loaded examples.** Move examples to `references/examples.md`.

## When NOT to write a skill

- Single-use task with no reuse expected → just do it inline.
- Knowledge that belongs in AGENTS.md → put it there.
- External tool access → use MCP, optionally with a thin skill on top.
- Simple text template → use a slash command / prompt file instead.
