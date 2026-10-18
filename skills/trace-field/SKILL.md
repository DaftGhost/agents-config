---
name: trace-field
description: Trace a named field or data property through a codebase. Use whenever someone asks where a field comes from, where it is written or read, what API/UI/database output exposes it, or what behavior it influences. Identify concrete writers, readers, output paths, business-logic consumers, and supporting code locations; state clearly when a category has no confirmed consumer.
---

# Trace a field through the codebase

Given a field, property, column, setting, or data key, build an evidence-backed path through the code. The goal is to distinguish where the value is created or changed, where it is consumed, where it leaves a boundary, and where it affects behavior.

## Workflow

1. **Pin down the target and scope.** Use the exact field name and any model, endpoint, feature, or directory context in the request. If the name is ambiguous, inspect plausible definitions and explain the ambiguity; ask only if it prevents a useful trace. Do not assume similarly named fields are the same field.
2. **Find its definition and writers.** Search for declarations, schema/model definitions, defaults, constructors, assignments, mutations, deserialization, database writes, and migrations. Separate authoritative writes from derived copies or test fixtures. Record the conditions that control meaningful writes when relevant.
3. **Find its readers.** Search references to the field and trace aliases, destructuring, mapping, serialization, and helper calls far enough to establish what reads the value. Distinguish direct references from indirect data flow; do not label a same-named but unrelated value as a consumer without evidence.
4. **Trace outputs and boundaries.** Check whether the value is returned or accepted by an API, rendered in a UI, serialized into an event/job, written to or read from storage, logged, exported, or passed to an external integration. Name the boundary and follow transformations that rename, omit, mask, or format the field.
5. **Identify business-logic consumers.** Explain where the value changes decisions or outcomes: branching, filtering, validation, authorization, calculations, state transitions, sorting, feature gates, or side effects. A display-only read is not a business-logic consumer. Follow the relevant call path and state the practical effect.
6. **Verify each claim at its source.** Use the repository's available code navigation and search tools. Prefer symbol/reference tools or a code graph when available; otherwise use targeted `rg` searches and read the surrounding source. Follow callers and callees as needed. Cite repository-relative file paths with line numbers, and include enough code-path detail for the reader to verify each step. Avoid inferring behavior from a field name alone.
7. **Report gaps explicitly.** For each category, say when no consumer or output was found in the searched scope. Describe the scope searched when relevant. Do not claim global absence based on one file or an incomplete search. If the field is only written and never read in the visible code, say so and identify any external/dynamic boundaries that prevent a stronger conclusion.

## Report format

Write the report in the language of the user's current request. Translate the section headings below into that language while preserving their meaning and order. Keep code identifiers, filenames, and quoted source text in their original form.

Choose the report depth to match the request. For a full trace, start with a one-sentence summary and use all six sections below. For a focused question, give a compact answer covering the requested stages; when explaining behavior, report writes, reads or outputs, and business-logic impact separately. State the searched scope for any category with no confirmed use.

- **Definition and writes** — definition, defaults, authoritative writers, and notable write conditions.
- **Reads and propagation** — direct readers and important transformations/aliases.
- **Outputs and boundaries** — API/UI/storage/event/log/export/external output paths, or explicitly state none found.
- **Business logic impact** — decisions or side effects driven by the field, or explicitly state no business-logic consumer was found.
- **Code paths** — concise ordered paths such as `request → validator → model assignment → persistence → response serializer`, with evidence citations at each relevant step.
- **Scope and unresolved items** — search scope, unresolved ambiguity, dynamic/reflection/generated-code limitations, and categories with no confirmed use.

Use precise language: distinguish “I found no consumer in the searched scope” from “there is no consumer.” If a field has multiple independent flows, report them separately rather than merging them into one speculative narrative.

## Evidence and style

- Attach a specific source location to every substantive claim, preferably `path/to/file.ext:line` (or a clickable repository-relative file link in the host UI).
- Cite the implementation that performs a write or read, not only a type declaration or test expectation.
- When explaining a behavior, trace and report separately where it is written, where it is read/output, and where it affects business logic.
- Keep direct observations separate from inferences. Label an inference and show the code path that supports it.
- Summarize relevant paths; do not dump broad search results or list every irrelevant textual match.
