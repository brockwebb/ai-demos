# CC Task: Namespace Cleanup — Seldon Result References

## Date: 2026-03-17

## Context

The terminology rename from "entropy fitness" to "log-precision fitness" was applied to research notes and documentation (CC_TASK_rename_entropy.md). However, the Seldon result registry still uses `entropy_` prefixed names. These names leak into the paper through `{{result:NAME:value}}` references. The paper should not contain "entropy" anywhere, including in reference plumbing.

This task renames the Seldon result artifacts and updates all paper section references to match.

## Scope

1. Query all Result artifacts in the Seldon graph: `seldon result list`
2. For each result with an `entropy_` prefix, rename to `logprec_` prefix
3. Update every `{{result:entropy_*}}` reference in `paper/sections/*.md` to use the new name
4. Verify all references still resolve: `seldon paper build --no-render`

## Rename Map

Determine the exact mapping by running `seldon result list` first. Expected renames (confirm before applying):

| Old Name | New Name |
|----------|----------|
| `entropy_minimal_5_5` | `logprec_minimal_5_5` |
| `entropy_minimal_runtime` | `logprec_minimal_runtime` |
| `entropy_stress_l1_0_5` | `logprec_stress_l1_0_5` |

Any other `entropy_*` results should follow the same pattern. Results that don't have `entropy_` prefix (e.g., `info_rate_3_32`, `wrong_limit_ti_15_93`, `leibniz_ti_15_29`) stay as-is.

## Steps

1. Run `seldon result list` and capture all current result names
2. Identify all results with `entropy_` prefix
3. For each, use the appropriate seldon CLI command to rename (check `seldon result --help` for rename capability; if no rename command exists, delete and re-register with new name, preserving value, state, and provenance links)
4. Search all `paper/sections/*.md` files for `{{result:entropy_` and replace with `{{result:logprec_`
5. Search `paper/sections/*.md` for any remaining literal "entropy" — flag but do not auto-fix (some may be legitimate references to Shannon entropy in the Background section)
6. Run `seldon paper build --no-render` to verify all references resolve
7. Run `seldon paper audit paper/sections/*.md` to check for other issues

## Files to Edit

- All files in `paper/sections/` containing `{{result:entropy_*}}` references
- Seldon Neo4j graph (Result artifact names)

## Files NOT to Edit

- Research notes (already handled by CC_TASK_rename_entropy.md)
- Python scripts or data files
- `paper/conventions.md` (no result references there)

## Verification

After completion:
- `seldon result list` shows no `entropy_` prefixed names
- `grep -r "entropy" paper/sections/` returns only legitimate uses (Shannon entropy discussion in Background, if any)
- `seldon paper build --no-render` passes with no unresolved references
