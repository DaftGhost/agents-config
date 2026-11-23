# Writing Plan Documents

Apply these rules together with the selected type's format. Write for both the person reviewing the plan and the agent executing it.

## Human understanding

- Make the plan self-contained. State the goal, scope, essential context and constraints, explaining task-specific terms and assumptions.
- Before assigning requirement IDs, classify each part of the request using [Constraints: Classification](constraints.md#classification).
- Organize requirements from the overall outcome to areas or flows and then to concrete requirements and relevant conditions. For a complex document, add a brief key-points overview before the detailed sections.
- Use Mermaid diagrams where a flow, relationship or state change is easier to understand visually. Each diagram should explain one meaningful part with enough context and relationships to be useful; if it covers too much to follow, split it by area or level and connect the parts in the text. Prefer prose or a table when a diagram would add little. Place each diagram beside the explanation it supports.

## Content development

- Start from the request and inspected project evidence. Ask what a reviewer must understand to judge the proposal and what an implementer must know to carry it out. Follow the task-specific questions this exposes, including topics absent from the format prompts; support the answers with evidence or mark assumptions and pending decisions.
- Use the required sections as review anchors. Add subsections, examples, diagrams or supporting sections where they make the task understandable; keep each subject and its explanation together. Place supporting sections beside the content they explain, preserving the required sections' relative order.
- Choose depth by the consequence of leaving something unexplained: expand where an omission could change the review decision, intended behavior, implementation or verification. Give established context a concise explanation and source; use concrete examples to resolve ambiguity. Describe necessary task-specific concerns even when they are not technical implementation decisions.
- Before saving, read through the plan as a reviewer and as its next reader. Can they explain the outcome and its basis, identify pending choices, and take the next action without guessing an unresolved requirement or design choice? Fill substantive gaps found by this read-through, including those outside the format prompts, and remove repetition that adds no understanding.

## Requirement traceability

- Use stable requirement IDs (R1, R2, ...); never reuse a removed ID. Apply this to objectives and outcomes as well as requirement tables.
- Map requirements that necessitate a change to the relevant Detailed design section, and map acceptance criteria and verification checks to requirement IDs or applicable constraints.
- Before saving, check that requirement IDs are unambiguous and that all required mappings are present and resolve to the intended content.

## Target files

- Consolidate all files to be changed in a separate **Target files** section. Use a table with only **File** and **Operation** columns. Each row contains a file path and one operation: **Modify**, **Delete** or **Add**, translated to the document's language (修改、删除、新增 in Chinese). Keep change details and requirement IDs in Detailed design.
- Before saving, check that every planned file change appears in Target files and that Detailed design explains the changes without listing files to change.

## Agent execution

- State the inputs or starting state, processing or actions, expected outputs or state changes, and verification for the work. Provide enough detail to identify what to inspect or change and how to check the result; distinguish confirmed facts, assumptions and pending decisions.
- Before saving, check that every actionable change has an expected result and a check.
