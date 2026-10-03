## Read Files in Bounded Sections

### What

When reading files for a task, first locate the relevant definitions and relationships with `rg`, then read explicit, bounded line ranges. Preserve the context needed to interpret the content and track which portions have been read completely.

### Why

Large outputs can hide relevant content through truncation. Locating the relevant sections and reading them in manageable ranges keeps the evidence inspectable. Tracking coverage prevents missing content from being mistaken for absent definitions or a complete review.

### How

#### 1. Locate Definitions and Uses

Use `rg --files` with relevant roots and filename globs to identify candidate files. Search those files with `rg -n` for the task's objects, tables, trigger entry points, and callers, as applicable. Record the file paths and line numbers for both definitions and uses.

If search output is truncated, retain the fully displayed matches and narrow the search to uncovered files or line ranges. Recover any partially displayed match as well. Treat a capped search as incomplete evidence; a match missing from the displayed portion does not establish its absence.

Complete location when the relevant definitions and uses have been identified, or the remaining search gaps have been recorded for follow-up.

#### 2. Read Complete Semantic Units in Bounded Ranges

Read explicit line ranges around the matches, for example with `sed -n '120,180p' path/to/file`. Choose the range and tool output budget together, accounting for long lines. Keep each response small enough to inspect completely; read unrelated ranges separately.

Read adjacent ranges until the relevant semantic unit is complete. Include the surrounding declaration, conditions, error handling, and related configuration needed to interpret it. Follow referenced definitions and callers with another scoped `rg -n` search and bounded read.

After each response, record the fully read ranges and any unread gaps. Preserve context from completed ranges; overlap only the small boundary portion needed to recover incomplete content or resolve an ambiguous connection. If a response is truncated, recover the gap using the next procedure before treating the semantic unit as complete.

Complete a semantic unit when all content required to interpret it has been read without unresolved gaps.

#### 3. Continue from the Truncation Point

When a file read is truncated, retain the fully displayed content and identify the first missing or partially displayed line. Continue from that position in smaller ranges. Fill omitted gaps when the tool preserves both a prefix and a suffix. Do not restart the original range or reread completed sections solely because truncation occurred.

If the truncation position is unclear, use a narrow, line-numbered read to locate the gap. For a single oversized line, use a format-aware reader to extract the missing fields or structure and label the extraction's scope.

Complete recovery when the omitted content has been read and the coverage record has been updated. If access or another constraint prevents recovery, retain the gap for the final coverage check.

#### 4. Verify Coverage Before Drawing Conclusions

Check the completed ranges and unread gaps against the definitions, triggers, callers, and context required by the task. Retain the supporting file paths and line numbers, and recheck locations after edits.

Claim a full-file or complete call-chain review only when every required portion has been read without unresolved gaps. If a gap remains, identify the unread context and limit the conclusion to the evidence actually inspected.

Complete the reading task when the required context has been read in full, or when remaining gaps and their effect on the conclusion have been explicitly reported.

### Example

Adapt the roots, patterns, ranges, and output budget to the task. In this sequence, the first read is truncated after line 156; lines 120–156 remain complete, so reading continues at line 157:

```bash
rg --files src migrations -g '*.ts' -g '*.sql'
rg -n 'OrderService|orders|CREATE TRIGGER|submitOrder' src migrations
sed -n '120,180p' src/orders.ts
# Retain completed lines 120–156 and recover the missing range:
sed -n '157,168p' src/orders.ts
sed -n '169,180p' src/orders.ts
# If the semantic unit continues past line 180, read its adjacent range next.
```
