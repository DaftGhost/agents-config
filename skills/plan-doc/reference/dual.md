# Dual Workflow

Dual splits the selected document type's format into two documents. After choosing dual, read the split for the primary type and for each secondary type in a mixed task:

- [New functionality](new-functionality/dual.md)
- [Existing functionality change](existing-functionality/dual.md)
- [Code refactoring](refactoring/dual.md)
- [General](general/dual.md)
- [Operations and delivery](operations/dual.md), only as a secondary type

Use the selected type's format for section content and its split for placement. Preserve the section order within each document; for mixed tasks, incorporate secondary content without duplicating sections.

1. Complete the investigation needed to establish feasibility, then write `what-to-do.md` as Draft. Stop for user confirmation even if both documents were requested. Tell the user that design follows confirmation.
2. When the user confirms decisions, apply [Plan Decisions](decisions.md) before proceeding. Once the user has confirmed the requirements and no decisions in `what-to-do.md` remain pending, mark it Confirmed. Recheck relevant project context if missing or changed, then write `how-to-do.md` as Draft. If a requirement cannot be met or a newly discovered impact changes scope, ask before changing the confirmed requirements.
