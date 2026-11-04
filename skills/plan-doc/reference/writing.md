# Writing Plan Documents

Apply these rules together with the selected type's format. Write for both the person reviewing the plan and the agent executing it.

## Human understanding

- Make each document self-contained for its phase: state the goal, scope, essential context and constraints, explaining task-specific terms and assumptions. In dual, the design may link to the confirmed requirements, but summarize the essential context needed to understand its approach.
- Classify each part of the request by meaning before assigning requirement IDs: outcomes or behaviors the task must deliver belong in requirements; limits the work must respect, including prohibitions and behaviors or contracts to preserve, belong in constraints; excluded work belongs in the out-of-scope part of scope. For example, “keep the API unchanged” is a constraint, and “historical data migration is excluded from this task” is out of scope. A request to remove or stop existing behavior is still a requirement when that change is a required outcome. Keep constraints and exclusions in their respective sections rather than duplicating them as requirements. Verify applicable constraints separately from requirements.
- Organize requirements from the overall outcome to areas or flows and then to concrete requirements and relevant conditions. For a complex document, add a brief key-points overview before the detailed sections.
- Use Mermaid diagrams where a flow, relationship or state change is easier to understand visually. Each diagram should explain one meaningful part with enough context and relationships to be useful; if it covers too much to follow, split it by area or level and connect the parts in the text. Prefer prose or a table when a diagram would add little. Place each diagram beside the explanation it supports.

## Design and target files

- Use implementation design sections for logic, flows, responsibilities, interfaces, data and execution order. Link requirements to the relevant design explanations; keep file-change inventories out of these sections.
- Consolidate all files to be changed in a separate **Target files** section in the single plan or, for dual, in `how-to-do.md`. Use a table with only **File** and **Operation** columns. Each row contains a file path and one operation: **Modify**, **Delete** or **Add**, translated to the document's language (修改、删除、新增 in Chinese). Keep change details and requirement IDs in the design sections.
- Before saving, check that every planned file change appears in Target files and that implementation design sections explain the changes without listing files to change.

## Agent execution

- State the inputs or starting state, processing or actions, expected outputs or state changes, and verification for the work. Provide enough detail to identify what to inspect or change and how to check the result; distinguish confirmed facts, assumptions and pending decisions.
- Apply this to the current phase: in dual, the requirements document states the required outcomes and conditions; the design document states the actions, expected results and checks against those requirements. Do not invent implementation details before requirements are confirmed.
- Before saving, check that a reader can understand the current document without the conversation, that every actionable change has an expected result and a check, and that diagrams clarify rather than duplicate the surrounding text.
