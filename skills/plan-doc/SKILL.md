---
name: plan-doc
description: Write plan documents before implementation when the user asks for a plan, 方案, 需求文档, 详细设计, design doc, or spec for new functionality, changes to existing functionality, code refactoring, operations and delivery, or another project task. Use for new projects too. Do not implement the change or use for a quick question.
---

# Plan Doc

Create task-specific plan documents; do not implement the planned change.

## Workflow

1. **Identify intent.** Select the primary outcome and read its guide. For mixed tasks, also read the guides for the other requested outcomes. If the intent is unclear, start with the general guide and refine the selection during investigation.
   - [New functionality](reference/new-functionality/guide.md): add a capability, including a new project.
   - [Existing functionality change](reference/existing-functionality/guide.md): change, fix or retire behavior or business rules.
   - [Code refactoring](reference/refactoring/guide.md): change internal structure while preserving behavior.
   - [Operations and delivery](reference/operations/guide.md): change deployment, CI/CD, environment configuration or infrastructure.
   - [General](reference/general/guide.md): a project task outside the four types above.
2. **Investigate and check.** Follow the selected guides to inspect the affected project context, constraints and consumers. Check the request and findings for ambiguity, contradictions and feasibility conflicts. If a blocker prevents identifying the task or its scope, ask before writing; use an interactive question tool when available, with at most four questions, options and a recommended default. After an answer or new finding, refine the intent and scope, load any newly relevant guides, and investigate and check again. Decisions that can wait with a sound default belong in the document. Finish the loop when the task and scope are clear, blockers are resolved, and the information needed to establish feasibility and choose the document organization is available.
3. **Read the format and write.** Read the format linked from the selected guide and [writing requirements](reference/writing.md), then apply both to the current document. For mixed tasks, also read the other relevant formats and incorporate their content into the primary type's document without duplicating sections.

## Document Rules

- **Organization**: for mixed tasks, use the primary type's rule. Repository size and file count alone do not justify dual.
- **Location**: `docs/plans/<topic>/` with a short kebab-case topic. Single: `plan.md`. Dual: `what-to-do.md`, then `how-to-do.md`.
- **Scope**: plan documents are working documents for the task, not persistent project documentation.
- **Header**: title, `Status: Draft` (or `Confirmed`), `Type: <document type>`, and `Tier: <single|dual> - <reason>`.
- **Language**: follow the user's request.
- **Reply**: link each document using its name as the link text and its path as the target; say what to review and what happens next. Refer to the Decisions section without repeating its rows. Keep the document type and tier in the header only.

## Done

The current document has the header and sections required by its selected type. In dual's first phase, `what-to-do.md` is produced; `how-to-do.md` follows confirmation.
