# Plan Decisions

## Format

Use Decisions to resolve open questions about what to do and how to do it. List each pending question as a row in this Markdown table, leaving the Decision cell blank:

| ID | Question | Options | Recommended default | Decision |
| --- | --- | --- | --- | --- |
| Q1 | ... | ... | ... | |

Mark each requirement that depends on a decision `pending Qn`. Write `None` when no decisions remain.

In dual, each document has a Decisions section for the what and how questions identified at its stage. Record a question once in the document where it is identified; do not copy it to the other document.

## When a decision is confirmed

1. Identify the user's confirmed choice. Leave unanswered decisions pending; confirmation of a document alone does not select a decision's default.
2. Remove the confirmed decision's row and update every affected section and related plan document to reflect the choice, including requirements, gaps, scope, approach and verification where applicable. Remove its `pending Qn` markers. Keep unrelated decisions and requirement IDs unchanged.
3. Check that no stale default, decision row or `pending Qn` reference remains and that all affected plan content agrees. If a newly discovered conflict or ambiguity blocks the update, ask before changing the affected content.
