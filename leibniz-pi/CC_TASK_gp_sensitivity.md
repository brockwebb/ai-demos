# Claude Code Task: GP Parameter Sensitivity Analysis

## Context
GP v3 minimal (convergence-aware fitness) found Leibniz 2/5 seeds with minimal terminals {k, 1, -1, 2}, no injection, 360s/seed. Three seeds got trapped in wrong-limit attractors. The question: is this a fundamental fitness landscape problem, or a parameter tuning problem?

## What to Do
Run a parameter sensitivity analysis on the GP convergence fitness. Start from `gp-leibniz-v3/gp_leibniz_v3_minimal.py` and vary one parameter at a time. Keep terminals at {k, 1, -1, 2}, no ephemerals, no injection.

### Parameters to sweep:

**ALPHA (convergence bonus weight)** — currently 0.05
- Try: 0.1, 0.2, 0.5
- Hypothesis: higher ALPHA penalizes "park and stop" attractors harder, may help escape local optima

**LAMBDA_P (parsimony pressure)** — currently 0.005
- Try: 0.001, 0.01
- Hypothesis: lighter parsimony allows exploration of larger trees; heavier parsimony may prematurely kill promising structures

**POP_SIZE** — currently 1000
- Try: 2000, 5000
- Hypothesis: bigger population = more diverse initial coverage, less likely to collapse to single attractor

**TOURNAMENT_K** — currently 7
- Try: 3, 5
- Hypothesis: lower tournament pressure preserves diversity longer

### Experimental design
- For each parameter variation, run 5 seeds with the same seed values (42, 7, 137, 2718, 31415)
- Keep MAX_SEED = 360s
- Record: seeds finding Leibniz (out of 5), generations needed, expressions found
- Only vary ONE parameter at a time from the baseline (ALPHA=0.05, LAMBDA_P=0.005, POP_SIZE=1000, TOURNAMENT_K=7)

### Implementation
- Don't create separate script files for each parameter value
- Instead, modify the minimal script to accept command-line arguments: `--alpha 0.2` etc.
- Or create one sweep script that loops through parameter values
- Whatever is cleanest

### Output
Create `gp-leibniz-v3/parameter_sensitivity.md` with a table:

| Parameter | Value | Seeds Found | Best Expression | Notes |
|---|---|---|---|---|
| baseline | — | 2/5 | (-1^k)/((2*k)+1) | from v3 minimal run |
| ALPHA | 0.1 | ?/5 | ... | ... |
| ALPHA | 0.2 | ?/5 | ... | ... |
| ... | ... | ... | ... | ... |

If any configuration hits 5/5, that's the headline. If none do, the GP fitness landscape genuinely has a trap problem that parameters can't fix.

### Time budget
Each configuration = 5 seeds × 360s = 30 min max. 9 configurations = ~4.5 hours worst case. Run configurations in parallel if the machine can handle it (each is single-threaded, so CPU cores are the limit).
