## Read Files in Bounded Sections

Before reading file contents, locate the relevant definitions and relationships with `rg`, then read bounded line ranges. Preserve semantic context while keeping each tool response within its output limit.

1. Use `rg --files` with relevant roots and filename globs to identify candidate files. Search those files with `rg -n` for the task's objects, tables, trigger entry points, and callers, as applicable. Locate both definitions and uses; record file paths and line numbers.
2. If search output is truncated, retain the visible matches and continue searching the uncovered files or line ranges with a narrower scope. Treat a capped search as incomplete evidence; missing matches in the displayed portion do not prove absence.
3. Read explicit line ranges around the matches, for example with `sed -n '120,180p' path/to/file`. Choose the range and output budget together, accounting for long lines. Keep each response small enough to inspect completely rather than concatenating many files or unrelated ranges into one output.
4. Read adjacent ranges until the relevant semantic unit is complete. Include the surrounding declaration, conditions, error handling, and related configuration needed to interpret it. Preserve context from the completed ranges; overlap only the small boundary portion needed to recover incomplete content or resolve an ambiguous connection. Follow referenced definitions and callers with another scoped `rg -n` search and bounded read.
5. On truncation, retain the fully displayed content, identify the first missing or partially displayed line, and continue from that position in smaller ranges. Fill omitted gaps if the tool preserves both a prefix and a suffix. Do not restart the original range or reread completed sections just because the response was truncated. If the truncation position is unclear, use line-numbered output to locate the gap with a narrow read. For a single oversized line, use a format-aware reader to extract the missing fields or structure and label the extraction's scope.
6. Track completed ranges and unread gaps, along with the files and line numbers supporting the conclusion. Recheck line numbers after edits. Claim full-file or complete call-chain review only when every required portion has been read without unresolved gaps.

Example sequence; adapt the roots, patterns, and ranges to the task:

```bash
rg --files src migrations -g '*.ts' -g '*.sql'
rg -n 'OrderService|orders|CREATE TRIGGER|submitOrder' src migrations
sed -n '120,180p' src/orders.ts
# If line 156 is the last complete line shown, continue with smaller ranges:
sed -n '157,168p' src/orders.ts
sed -n '169,180p' src/orders.ts
```

Complete when the relevant definitions, triggers, and callers have been located and their required context has been read in full, or when unread context is explicitly identified as a limit on the conclusion.
