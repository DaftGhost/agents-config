---
name: plan-doc
description: Turn a development task into plan documents before any code is written - requirements (what to do, with acceptance criteria) and detailed design (how to do it) - as one document for contained work or two sequential documents for larger work. Works for modifying or maintaining an existing project and for starting a new one. Use this skill whenever the user asks for a plan, 方案, 需求文档, 详细设计, design doc, spec, or "figure out what and how first" for a feature, refactor, migration, fix, or new project, even if they only say "出个方案" and name no tier. Do not use it to implement the change, to write README or API reference docs, or to answer a quick question.
---

# Plan Doc

Tasks go wrong when "what" and "how" are decided together: the design quietly settles product questions, and the requirements inherit whatever the code happens to allow. A plan document separates them. Current facts, requirements, and the gap between them state what must change; the technical design states how, and the modified targets and verification state what changes and how to prove it. Write plan documents only; leave project source untouched.

## Workflow

1. **Investigate first.** Read what exists: the code the task touches, README, deploy and config files, ops notes. For a new project, inspect the working directory and the user's stated stack. Test the request against itself: once every part is done, does each part still mean something? A part that becomes empty or impossible (such as releasing what is no longer held) is a contradiction. Then look for conflicts between the request and what the project allows. Constraints that bind a design often live outside the code.
2. **Resolve blockers before writing.** A blocker is a question whose different answers lead to different documents: a contradiction in the request, a conflict that makes the request infeasible as stated, or an ambiguity that changes what the task is or which tier fits. If a recommended default would leave the document sound (a time limit, a policy for an edge case, what to do about money already taken), it is a Decisions row, not a blocker. Ask with the interactive question tool (such as AskUserQuestion) when you have one, otherwise a short numbered message: at most four questions, each with options and a recommended default. Write nothing until they are answered. Everything that can wait belongs in the document's Decisions section.
3. **Choose the tier yourself, after investigating.** An explicit tier request from the user wins. Otherwise:
   - **Single** is the default: the requirements are clear from the request and the investigation, and every open decision has a recommended default that leaves the scope unchanged. Repository size and the number of files or modules the change touches do not move a clear task out of single.
   - **Dual** is for unclear requirements or a huge task: what must be true afterward needs the user's confirmation before design is worth doing (several interacting behavior changes, a policy question for existing users or stored data, a constraint that makes part of the request infeasible as stated), or the requirements are too many to review alongside a design.

   Ask only when you cannot tell. Record the tier and the reason in the tier line.
4. **Write the document for the current phase** as the tier section below directs. Single is one document; dual is one document per phase, and only the first phase runs unless the user has already confirmed the requirements.

## Document Rules

- **Location**: `docs/plans/<topic>/` with a short kebab-case topic. Single: `plan.md`. Dual: `requirements.md`, then `design.md`.
- **Task scope**: these documents are working papers for this task: they sort out the current requirement and guide its implementation, and they are not project documentation meant to outlast it. Leave README and other project documentation alone, and plan no documentation upkeep unless the request asks for it.
- **Header**: title, `Status: Draft` (or `Confirmed`), and `Tier: <single|dual> - <reason>`.
- **Language**: follow the user's request.
- **Requirements table**: columns ID, requirement, acceptance criterion. IDs (R1, R2, ...) are unique, and a removed ID is never reused. An acceptance criterion is a concrete input-to-result check.
- **Observable terms**: current facts, requirements, and gap name no function, class, table, or file, and no mechanism (scheduler, cron, queue, schema). Constraints appear as outcomes ("closes within 5 minutes of the limit"). Names and mechanisms belong to the technical design and modified targets.
- **Modified targets**: each is a file or function you opened, or is marked new. Each gap row, modified target, and verification item cites the requirement IDs it concerns.
- **Decisions section**: a table of ID (Q1, ...), question, options, recommended default, and a blank decision column for the user. A requirement that depends on a question is marked "pending Qn"; its criterion is written for the recommended default. Write "None" when empty.
- **Communication happens in the document.** Open decisions, assumptions, and impacts live in the document so the user reviews one place. The reply names the files, states the tier in a line, says what to review, and says what happens next. It neither lists nor paraphrases Decisions rows ("review the Decisions section" is enough), and it carries no open questions; blockers were settled before writing.

## Single Tier

Read [references/single.md](references/single.md) and write `plan.md` in one pass.

## Dual Tier

The user reviews and confirms each document, so write both top-down: an overview a reader can stop after and still know the whole picture, then sections that each open with their main point, with details grouped from the whole to its parts (by area or flow, not in the order you found them).

**Phase 1 - requirements.** Read [references/requirements.md](references/requirements.md) and write `requirements.md` as Draft. Stop there, even when the user names the dual tier or asks for both documents in one message: the design is written against requirements the user has confirmed, and review often changes them, so a design written alongside is rework. The reply points to the Decisions section and says the design follows the user's confirmation. Finish the investigation here, because a conflict first found during design forces the requirements to be reopened.

**Phase 2 - design.** Start when the user confirms the requirements. The conversation that produced `requirements.md` may be gone, and the code may have changed since, so the document and the project as they are now are the only inputs. Change the status line of `requirements.md` to Confirmed and nothing else, read [references/design.md](references/design.md), investigate the code as it directs, and write `design.md` as Draft. If the design shows a requirement cannot be met as written, treat it as a blocker: ask first, then revise per the revising reference.

## Existing Documents

When documents for this task already exist, resume at the phase they indicate. When the user gives feedback on a document or changes a requirement, read [references/revising.md](references/revising.md) before editing.

## Done

- The document for the current phase sits at the location above with status, tier, and the sections its reference lists. In the dual tier a finished first phase leaves `requirements.md` alone in the folder.
- No project file other than the plan documents changed.
