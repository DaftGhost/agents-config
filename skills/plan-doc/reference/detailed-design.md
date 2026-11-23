# Detailed Design

Use a **Detailed design** section (详细设计 in Chinese) for every document type.

## Design content

Explain how the proposed approach achieves the required outcomes and respects applicable constraints. Derive the design topics from the task's behavior, project evidence and unresolved implementation questions, using [Content development](writing.md#content-development).

Use the selected types' questions to begin investigation, then follow what the task reveals:

- **New functionality**: how does the capability fit the existing system, or what responsibilities and relationships does a new project need?
- **Existing functionality change**: where must current behavior change, and how do those changes produce the required behavior?
- **Code refactoring**: how do the proposed responsibilities and boundaries solve the structural problem while preserving behavior and caller contracts?
- **Operations and delivery**: what execution order and prerequisites reach the desired state, and what recovery is needed if execution fails?
- **General**: how do the proposed actions lead from the starting state to the required outcome?

Combine relevant questions for mixed tasks in one Detailed design section.

## Interface design

- Include a separate **Interface design** subsection (接口设计 in Chinese) within Detailed design. Cover interfaces introduced, changed or needed to understand the planned behavior, including internal component boundaries where relevant. If no interfaces apply, retain the subsection and state why it is not applicable.
- Make each covered interface's **contract** clear enough to identify a valid call and the provider's guarantees: its purpose, operation or signature, concrete input and output types with field meanings and constraints, and failure outcomes. Explain caller and provider responsibilities, preconditions and postconditions where needed to establish those guarantees. Reference unchanged contracts; specify changes and their effects on callers.
- Explain each covered interface's **behavior** so a reader can determine the observable result of relevant inputs and how callers handle failure outcomes. Follow the flow to discover which branches, boundary cases, state changes or side effects need explanation; define ordering, idempotency or retries when behavior depends on them.
- Before saving, check that each interface's contract and behavior agree with the surrounding flow and link to acceptance or verification checks for its success and failure outcomes.
