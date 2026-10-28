# Writing Plan Documents

Apply these rules together with the selected type's format. Write for both the person reviewing the plan and the agent executing it.

## Human understanding

- Make each document self-contained for its phase: state the goal, scope, essential context and constraints, explaining task-specific terms and assumptions. In dual, the design may link to the confirmed requirements, but summarize the essential context needed to understand its approach.
- Write requirements as the outcomes or behaviors the task must deliver. Put limits the work must respect under constraints, including prohibitions and behaviors or contracts that must remain unchanged; put excluded work under scope. Do not rephrase these as requirements. Verify applicable constraints separately from requirements.
- Organize requirements from the overall outcome to areas or flows and then to concrete requirements and relevant conditions. For a complex document, add a brief key-points overview before the detailed sections.
- Use Mermaid diagrams where a flow, relationship or state change is easier to understand visually. Each diagram should explain one meaningful part with enough context and relationships to be useful; if it covers too much to follow, split it by area or level and connect the parts in the text. Prefer prose or a table when a diagram would add little. Place each diagram beside the explanation it supports.

## Agent execution

- State the inputs or starting state, processing or actions, expected outputs or state changes, and verification for the work. Provide enough detail to identify what to inspect or change and how to check the result; distinguish confirmed facts, assumptions and pending decisions.
- Apply this to the current phase: in dual, the requirements document states the required outcomes and conditions; the design document states the actions, expected results and checks against those requirements. Do not invent implementation details before requirements are confirmed.
- Before saving, check that a reader can understand the current document without the conversation, that every actionable change has an expected result and a check, and that diagrams clarify rather than duplicate the surrounding text.
