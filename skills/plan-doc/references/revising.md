## Revising Plan Documents

### Feedback Before Confirmation

Trace each requested change into the code, the constraints, and the other requirements before editing, because edits made first are hard to unwind once they have spread through the document.

- **A consequence breaks feasibility or contradicts a constraint**: it is a blocker. Ask first, in the blocker format, and leave the affected lines as they are until the user answers; requested edits that raise no conflict may be applied now. Then edit the rest.
- **Otherwise**: edit the same file in place. Change only what was asked and every place that mentions it (background, requirements, criteria, impact). Keep the status Draft and keep IDs stable. Record each consequence that needs a decision as a Decisions row with options and a recommended default.

The reply summarizes the change in a line or two, names the document, and asks the user to review and confirm.

### Change After the Design Exists

Update `requirements.md` first, then only the design items that cite the changed requirement IDs. Say which items changed and which were left alone.
