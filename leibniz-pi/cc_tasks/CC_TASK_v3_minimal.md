# Claude Code Task: Minimal Terminal Set v3 (No Injection)

## Context
The wide pool (41 terminals) and hostile pool (40 terminals) both went 0/20. The search space was too large and the algorithm got trapped in wrong-limit attractors. The Leibniz injection in v2 was completely load-bearing.

We want to test whether the algorithm can discover Leibniz from scratch with the SMALLEST possible parts bin — just 4 terminals, no ephemerals, no injection.

## What to Build
Two scripts — one for each fitness function. Minimal terminal set. No injection.

### Terminal configuration (BOTH scripts):
```python
TERM_FIXED = ["k", 1, -1, 2]
EPHEMERALS = []
ALL_TERMINALS = TERM_FIXED + EPHEMERALS
```

That's it. Four terminals: k, 1, -1, 2. Six operators: add, sub, mul, div, pow, neg. Nothing else.

### Scripts to create:
1. `gp-leibniz-v3/gp_leibniz_v3_minimal.py` — fork of `gp_leibniz_v2.py`
2. `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py` — fork of `entropy_leibniz.py`

### Changes from v2 source (ONLY these changes):
1. `TERM_FIXED = ["k", 1, -1, 2]`
2. `EPHEMERALS = []`
3. Remove ALL Leibniz injection into the population:
   - Find `make_leibniz_tree()` — remove every call site that puts it into the initial population or any generation's population
   - Search for any hand-built tree being inserted into the gene pool (diversity injection, seeding, elitism shortcuts)
   - `make_leibniz_tree()` can remain as a function IF it's only used in post-run comparison/reporting — just remove it from population init
4. For GP script only: rename output files from `_v2` to `_v3_minimal` suffix
5. Time budget: `MAX_TOTAL = 1800.0`, `MAX_SEED = 360.0` (same 30-min budget as the other v3 runs)

### Do NOT change:
- Fitness functions
- Population size
- Tournament size, crossover rate, mutation rate
- Parsimony weight (LAMBDA_P)
- Convergence bonus weight (ALPHA)
- Evaluation checkpoints (T_EVAL)
- Number of seeds (5)
- Any other GP parameters

## Verify Before Running
1. `grep -n 'TERM_FIXED\|EPHEMERALS\|ALL_TERMINALS' <file>` — should show exactly 4 terminals, empty ephemerals
2. `grep -n 'make_leibniz_tree' <file>` — should NOT appear in any population initialization code. OK if it appears only in reporting/comparison.
3. Search for any other injection: `grep -n 'inject\|seed.*pop\|insert.*pop\|pop.*append\|pop.*insert' <file>` — verify no hand-built trees enter the population

## Run
Run both in parallel. 30-minute budget.

## Report
After runs complete, report:
- How many seeds found Leibniz (equivalent expression)?
- What expressions were found?
- Node counts
- Generations needed
- If Leibniz not found: what was the best expression? What was its convergence bonus?
- Compare to v2 (which had injection and found it 5/5 in ~1300 gens)

Update `v3_results_summary.md` with these results in a new section.
