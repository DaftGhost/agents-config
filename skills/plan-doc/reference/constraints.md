# Constraints

Use an **Applicable constraints** section (约束 in Chinese) for every document type. Place it in the single plan or, for dual, in `what-to-do.md`; the Detailed design in `how-to-do.md` must respect these constraints.

## Classification

Before assigning requirement IDs, classify each part of the request by its meaning:

- **Requirements** state outcomes or behavior the task must deliver. A request to remove or stop existing behavior is a requirement when that change is a required outcome.
- **Constraints** state what this task must not implement, change or do: excluded logic or work, flows or call paths that must remain unchanged, and prohibited behavior or side effects. Express preserved behavior or contracts as concrete boundaries on what may change.
- **Scope** describes the users, areas and flows covered by the task. Record explicit exclusions in Constraints rather than repeating them in Scope or Requirements.
- **Current context and prerequisites** describe existing facts, dependencies and conditions required before execution; keep them in the relevant context or prerequisites section.

## Writing constraints

- State each constraint as a concrete prohibition: identify the affected logic, component, flow, contract, data or behavior, the change or action excluded, and any conditions under which the prohibition applies. Name affected callers or internal components when needed to make the boundary clear.
- Use constraints stated by the user or established by applicable project rules and inspected evidence; cite supporting sources where relevant. Mark unresolved boundaries using [Plan Decisions](decisions.md), rather than inventing additional prohibitions.
- For example: “Do not migrate historical order data”; “Do not change the payment callback's validation or retry flow”; “Do not send notifications when previewing a quote.” Replace vague statements such as “avoid affecting other logic” with the specific protected flow or behavior.
- Keep each constraint in this section once. Detailed design and verification may refer to it without redefining it. If no applicable constraints are identified, state that explicitly.
- Before saving, check that every explicit exclusion and protected flow is accounted for, the design respects each constraint, and verification includes a check or inspection showing that the prohibited change or behavior does not occur. Verify constraints separately from requirement outcomes.
