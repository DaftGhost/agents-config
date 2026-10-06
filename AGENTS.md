# Repository Guidelines

## Repository Purpose

This project authors instructions for agents: behavioral rules, skills, workflows, and response and writing standards. Treat changes as instruction design: identify the intended agent behavior, then improve the guidance. Business domains and code snippets are teaching examples, not requests to implement those systems here. Hooks and configuration deliver instructions.

## Project Structure & Module Organization

`.agents/` holds the base prompt heading and shared skills; `aside/` holds canonical optional instruction modules. Other agent directories contain agent-specific content and adaptations. Update the relevant shared source before referencing or adapting it for an agent.

- `.agents/AGENTS.md` provides the base heading always included by the prompt generator.
- `.agents/skills/<skill-name>/` holds `SKILL.md` entry points and references.
- `.claude/skills/` provides relative symlinks to shared skills.
- `.claude/rules/` holds Claude-specific rules with YAML `paths` frontmatter.
- `.codex/` contains Codex-specific configuration and adaptations.

Organize aside modules by their instruction purpose. Use the current directory tree and module contents to identify categories and their responsibilities. Before placing a rule, inspect the existing categories and reuse one that fits its purpose. Create a new category only when no existing category covers that purpose.

## Instruction Writing & Naming Conventions

When creating or editing agent-facing content, choose an approach suited to the task: use `writing-for-agents`, select another relevant available skill, or apply the principles below directly. The purpose is to keep the content addressed to the agent that will execute it and make instructions unambiguous, actionable, and verifiable.

Write for the consuming agent: turn decisions into instructions, constraints, and reference material it can use. Keep the author's deliberations, work logs, and explanations to the user in the conversation rather than in the guidance. Before saving, check that each passage helps the agent decide what to do or how to do it.

State when instructions apply, what actions are required, and how completion is verified. Keep essential guidance in the entry point; link to task-specific details with explicit conditions for reading them.

Use actionable instructions and fenced examples. Preserve each document's language. Use kebab-case for skill directories and for names of directories and files under `aside/`; retain `SKILL.md`.
Use one level-two heading (`##`) as the main title of each aside file, with deeper headings for subsections.

Maintain one canonical source per rule. Update the shared source before adjusting agent-specific references or adaptations.
When moving, renaming, or merging instruction documents, update responsibility descriptions and references, then check for obsolete paths and duplicate rules.
