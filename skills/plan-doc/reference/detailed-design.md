# Detailed Design

Use a **Detailed design** section (详细设计 in Chinese) for every document type. Place it in the single plan or, for dual, in `how-to-do.md`; keep `what-to-do.md` focused on requirements and constraints.

## Design content

- Explain the proposed logic, flows, component responsibilities and boundaries, data and execution order. Link requirements to the relevant design explanations and show how the design respects applicable constraints. Keep file-change inventories in the separate Target files section.
- Apply the relevant type-specific focus; combine these in one Detailed design section for mixed tasks:
  - **New functionality**: describe the flow and affected entry points, components and data; for a new project, explain component responsibilities and relationships.
  - **Existing functionality change**: describe proposed changes against the current flows, requirements and constraints.
  - **Code refactoring**: describe proposed responsibilities, boundaries and order of changes, including interface effects on callers while preserving required behavior and contracts.
  - **Operations and delivery**: describe configuration or infrastructure changes and their order, including rollout and appropriate recovery or rollback steps.
  - **General**: describe the key logic, flow and execution steps.

## Interface design

- Include a separate **Interface design** subsection (接口设计 in Chinese) within Detailed design. Cover interfaces introduced, changed or needed to understand the planned behavior, including internal component boundaries where relevant. If no interfaces apply, retain the subsection and state why it is not applicable.
- Define each interface's **contract**: purpose, caller and provider responsibilities, operation or signature, concrete input and output types, field meanings and constraints, preconditions, postconditions, and failure outcomes. Identify contracts that remain unchanged and specify any changes and their effects on callers.
- Define each interface's **behavior**: what valid inputs cause, relevant branches and boundary cases, observable outputs, state changes or side effects, and how callers handle failure outcomes. Specify ordering, idempotency or retry semantics when the planned flow depends on them. Give concrete input-to-result examples where prose alone leaves the behavior ambiguous.
- Before saving, check that each interface's contract and behavior agree with the surrounding flow and link to acceptance or verification checks for its success and failure outcomes.
