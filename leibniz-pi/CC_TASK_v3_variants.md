# Claude Code Task: Create and Run Leibniz GP v3 Variants

## Context
We have two genetic programming experiments that rediscover the Leibniz series for π/4:
- `gp-leibniz-v2/gp_leibniz_v2.py` — convergence-aware fitness
- `entropy-leibniz/entropy_leibniz.py` — information-theoretic fitness

Both use the same primitive (parts bin) configuration:
```python
FUNC_ARITIES = {"add": 2, "sub": 2, "mul": 2, "div": 2, "pow": 2, "neg": 1}
TERM_FIXED = ["k", 1, 2, -1]
EPHEMERALS = list(range(-5, 6))
ALL_TERMINALS = TERM_FIXED + EPHEMERALS
```

A valid criticism is that the terminal set is "primed" — it includes the exact constants Leibniz needs (-1, 1, 2). We need to test whether Leibniz still emerges from a larger, less favorable parts bin.

## What to Build
Create **four** v3 variant scripts — two for each fitness function, testing two terminal configurations:

### Variant A: "Wide Pool"
- `TERM_FIXED = ["k", 1]`
- `EPHEMERALS = list(range(-20, 21))`
- The constants -1 and 2 are available but buried in 41 ephemeral options
- Tests whether Leibniz emerges when the correct constants aren't privileged

### Variant B: "Hostile Pool"  
- `TERM_FIXED = ["k", 1, 3, -1]`
- `EPHEMERALS = [x for x in range(-20, 21) if x != 2]`
- The constant 2 is NOT available anywhere. The algorithm must manufacture it (e.g., `add(1,1)` or `sub(3,1)`)
- Tests whether Leibniz emerges when a required constant is missing entirely

### The four scripts:
1. `gp-leibniz-v3/gp_leibniz_v3_wide.py` — GP convergence fitness + wide pool
2. `gp-leibniz-v3/gp_leibniz_v3_hostile.py` — GP convergence fitness + hostile pool
3. `entropy-leibniz-v3/entropy_leibniz_v3_wide.py` — Entropy fitness + wide pool
4. `entropy-leibniz-v3/entropy_leibniz_v3_hostile.py` — Entropy fitness + hostile pool

## How to Build Them
1. Create directories `gp-leibniz-v3/` and `entropy-leibniz-v3/` under `leibniz-pi/`
2. Copy the v2 source files into the v3 directories
3. For each copy, change ONLY these lines:
   - `TERM_FIXED = ...` (as specified above per variant)
   - `EPHEMERALS = ...` (as specified above per variant)
4. For GP variants only: rename output files from `_v2` suffix to `_v3` suffix:
   - `evolution_data_v2.json` → `evolution_data_v3.json`
   - `convergence_v2.csv` → `convergence_v3.csv`
   - `results_v2.txt` → `results_v3.txt`
5. Entropy output filenames (`entropy_data.json`, `convergence.csv`, `results.txt`) are fine as-is since they're in separate directories

## CRITICAL: Do NOT change anything else
- Same fitness functions
- Same GP hyperparameters (pop size, tournament, crossover, mutation, parsimony)
- Same evaluation checkpoints (T_EVAL)
- Same stopping criteria
- Same number of seeds (5)
- Same max time per seed (55s)

The ONLY change is the parts bin. That's the whole point of the experiment.

## Verification
After creating the scripts, verify:
1. `grep 'TERM_FIXED\|EPHEMERALS' <each_file>` shows the correct values
2. For hostile variants: confirm `2` does NOT appear in TERM_FIXED or EPHEMERALS
3. The scripts run without import errors (just test `python3 <script> --help` or a quick syntax check)

## Running
Run all four. Each takes ~5 minutes (5 seeds × 55 seconds). Run in parallel if possible.

After each completes, check the `results_v3.txt` or `results.txt` for:
- Did any seed find Leibniz equivalent? (`Equivalent to Leibniz: True/False`)
- What expression did it find?
- For hostile variants: did it manufacture 2? (look for `add(1, 1)` or `sub(3, 1)` in the expression)

## Expected Outcomes
- **Wide pool:** Should find Leibniz (same 9-node expression). May take more generations since the search space is larger.
- **Hostile pool:** May find a structurally equivalent but longer expression like `(-1)^k / (add(1,1)*k + 1)` — 11+ nodes. Or may find Leibniz via `sub(3,1)` for the 2. Or may fail entirely — which is also interesting data.

## Output
After all four runs complete, create a summary file `leibniz-pi/v3_results_summary.md` with:
- Which variants found Leibniz
- The expressions found
- Node counts
- Number of generations needed
- Comparison to v2 results (v2 found Leibniz in ~1300 generations with 9 nodes)
