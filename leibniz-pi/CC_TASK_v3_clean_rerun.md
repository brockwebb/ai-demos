# Claude Code Task: Clean Hostile v3 Rerun (No Leibniz Injection)

## Problem
The v3 hostile variants (both GP and Entropy) produced 5/5 Leibniz results, BUT the `make_leibniz_tree()` function injects a literal Leibniz tree containing `Node(value=2)` into the gen 0 population. In the hostile variant where 2 is excluded from the terminal set, this smuggles the forbidden constant back in. The test is not clean.

The wide pool variants also have this injection. While less problematic (2 is available in their ephemeral pool anyway), the injection still means the algorithm isn't discovering Leibniz from scratch — it's being handed it and asked to confirm.

## What to Do
Rerun ALL FOUR v3 variants with the Leibniz injection removed. This is the honest version. The algorithm starts from a pure random population with no planted answer.

### Steps:
1. In each of the four v3 scripts, find the `make_leibniz_tree()` function and everywhere it's called
2. Remove or comment out the injection — wherever a Leibniz tree is inserted into the initial population
3. Do NOT remove `make_leibniz_tree()` itself if it's used only for post-run comparison/reporting. Only remove its use in population initialization.
4. Look for any other place where a hand-built tree is injected into the population at gen 0 (e.g., diversity injection, seeding). If it uses constants not in the terminal set, remove it too.
5. The fitness function, GP parameters, terminal sets — everything else stays the same as the current v3 variants.

### Scripts to modify and rerun:
- `gp-leibniz-v3/gp_leibniz_v3_wide.py`
- `gp-leibniz-v3/gp_leibniz_v3_hostile.py`
- `entropy-leibniz-v3/entropy_leibniz_v3_wide.py`
- `entropy-leibniz-v3/entropy_leibniz_v3_hostile.py`

### What to check for specifically:
- Search for `make_leibniz_tree` — find all call sites
- Search for `leibniz` in the population initialization code
- Search for `inject` or `seed` or `elite` in the initial population setup
- Any place a hand-constructed tree enters the gene pool

### After modification, verify:
- `grep -n 'make_leibniz_tree' <file>` — should only appear in reporting/comparison code, NOT in population init
- The initial population should be 100% randomly generated trees

## Run All Four
Each takes ~5 min (5 seeds × 55s). Run in parallel.

## After Runs Complete
Update `v3_results_summary.md` with the clean results. Key questions:
1. Did any variant still find Leibniz 5/5?
2. Did any variant find it at all (even 1/5)?
3. For hostile variants: what expression did it find? Did it manufacture 2?
4. How many generations did it take compared to the injected version?
5. If it DIDN'T find Leibniz, what did it find instead? What's the best expression?

A failure to find Leibniz is interesting data, not a problem. Report whatever happens honestly.
