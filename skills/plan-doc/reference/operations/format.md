## Operations and Delivery Document

**Purpose**: define an operational or delivery change and how to carry it out and verify it. As the primary type, it always uses one document; as a secondary type, it follows the primary type's organization.

Write these sections in order after the header:

1. **Operational objectives and scope**: environment, desired state, affected services or operators, and requirement IDs.
2. **Current operational state and prerequisites**: inspected resources, dependencies, constraints and sources, plus conditions required before execution.
3. **Execution and recovery plan**: configuration or infrastructure changes and their order; list inspected or new targets with requirement IDs. Include rollout and appropriate recovery or rollback steps.
4. **Acceptance criteria and operational verification**: observable states and practical checks for the change and recovery where applicable. Use commands or inspections supported by the environment; automated tests are not mandatory when operational checks suffice.
5. **Decisions**: follow [Plan Decisions](../decisions.md).

Use stable requirement IDs (R1, R2, ...); never reuse a removed ID. Link acceptance criteria and verification checks to their requirements or applicable constraints; map requirements that necessitate a change to inspected or new targets.
