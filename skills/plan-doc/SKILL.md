---
name: plan-doc
description: Turn a development task into plan documents before any code is written - requirements (what to do, with acceptance criteria) and detailed design (how to do it) - as one document for contained work or two sequential documents for larger work. Works for modifying or maintaining an existing project and for starting a new one. Use this skill whenever the user asks for a plan, 方案, 需求文档, 详细设计, design doc, spec, or "figure out what and how first" for a feature, refactor, migration, fix, or new project, even if they only say "出个方案" and name no tier. Do not use it to implement the change, to write README or API reference docs, or to answer a quick question.
---

# Plan Doc

Tasks go wrong when "what" and "how" are decided together: the design quietly settles product questions, and the requirements inherit whatever the code happens to allow. A plan document separates them. Requirements state what must be true when the task is done; the design states how to get there. Write plan documents only; leave project source untouched.

## Workflow

1. **Investigate first.** Read what exists: the code the task touches, README, deploy and config files, ops notes. For a new project, inspect the working directory and the user's stated stack. Test the request against itself: once every part is done, does each part still mean something? A part that becomes empty or impossible (such as releasing what is no longer held) is a contradiction. Then look for conflicts between the request and what the project allows. Constraints that bind a design often live outside the code.
2. **Resolve blockers before writing.** A blocker is a question whose different answers lead to different documents: a contradiction in the request, a conflict that makes the request infeasible as stated, or an ambiguity that changes what the task is or which tier fits. If a recommended default would leave the document sound (a time limit, a policy for an edge case, what to do about money already taken), it is a Decisions row, not a blocker. Ask with the interactive question tool (such as AskUserQuestion) when you have one, otherwise a short numbered message: at most four questions, each with options and a recommended default. Write nothing until they are answered. Everything that can wait belongs in the document's Decisions section.
3. **Choose the tier yourself, after investigating.** An explicit tier request from the user wins. Otherwise:
   - **Single**: the work is contained (one module or one new small component), leaves no scope-changing decision open, and is easy to revert.
   - **Dual**: the work spans modules, alters persisted data or a public interface, or needs the requirements settled before design starts.

   Ask only when you cannot tell. Record the tier and the reason in the tier line.
4. **Write the documents** as the tier section below directs.

## Document Rules

- **Location**: `docs/plans/<topic>/` with a short kebab-case topic. Single: `plan.md`. Dual: `requirements.md`, then `design.md`.
- **Task scope**: these documents serve this task. Leave README and other project documentation alone, and plan no documentation upkeep unless the request asks for it.
- **Header**: title, `Status: Draft` (or `Confirmed`), and `Tier: <single|dual> - <reason>`.
- **Language**: follow the user's request.
- **Requirements table**: columns ID, requirement, acceptance criterion. IDs (R1, R2, ...) are unique, and a removed ID is never reused. An acceptance criterion is a concrete input-to-result check. Everything in the requirements part, today's-behavior description included, is written in observable terms: no function, class, table, or file names, and no mechanisms (scheduler, cron, queue, schema). Constraints appear as outcomes ("closes within 5 minutes of the limit"). Names and mechanisms belong to the plan or design.
- **Touchpoints**: each is a file or function you opened, or is marked new. Each cites the requirement IDs it serves.
- **Decisions section**: a table of ID (Q1, ...), question, options, recommended default, and a blank decision column for the user. A requirement that depends on a question is marked "pending Qn"; its criterion is written for the recommended default. Write "None" when empty.
- **Communication happens in the document.** Open decisions, assumptions, and impacts live in the document so the user reviews one place. The reply names the files, states the tier in a line, says what to review, and says what happens next. It neither lists nor paraphrases Decisions rows ("review the Decisions section" is enough), and it carries no open questions; blockers were settled before writing.

## Single Tier

Read [references/single.md](references/single.md) and write `plan.md` in one pass.

## Dual Tier

**Phase 1 - requirements.** Read [references/requirements.md](references/requirements.md) and write `requirements.md` as Draft. Stop there: the reply points to the Decisions section and says the design follows the user's confirmation. Finish the investigation here, because a conflict first found during design forces the requirements to be reopened.

**Phase 2 - design.** Start when the user confirms the requirements. Change the status line of `requirements.md` to Confirmed and nothing else, read [references/design.md](references/design.md), and write `design.md` as Draft. If the design shows a requirement cannot be met as written, treat it as a blocker: ask first, then revise per the revising reference.

## Existing Documents

When documents for this task already exist, resume at the phase they indicate. When the user gives feedback on a document or changes a requirement, read [references/revising.md](references/revising.md) before editing.

## Done

- The document or documents sit at the location above with status, tier, and the sections their reference lists.
- No project file other than the plan documents changed.
