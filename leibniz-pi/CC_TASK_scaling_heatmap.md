# Claude Code Task: Scaling Heat Map — Terminals × Population → Discovery Rate

## Goal
Produce a 2D grid showing discovery rate (out of 5 seeds) as a function of terminal count and population size. This characterizes the phase transition boundary between "discoverable" and "not discoverable" and becomes a key figure in the preprint.

## Design

**Fitness function:** Entropy (information-theoretic) — the stronger of the two. Use the same fitness as `entropy_leibniz_v3_minimal.py`.

**No injection.** Pure random init. Same convention as all v3 experiments.

**Terminal set construction (Option A):**
At each terminal count N, the set is:
- Fixed: {k, 1, -1, 2} (always present — guarantees Leibniz is constructible)
- Expansion: add integers starting from 3, 4, 5, ... and -2, -3, -4, ... alternating positive/negative to fill to size N
- Example at N=4: {k, 1, -1, 2} — just the fixed set
- Example at N=6: {k, 1, -1, 2, 3, -2}
- Example at N=8: {k, 1, -1, 2, 3, -2, 4, -3}
- Example at N=10: {k, 1, -1, 2, 3, -2, 4, -3, 5, -4}
- Example at N=12: {k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5}
- Example at N=15: {k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8}
- Example at N=20: {k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8, -7, 9, -8, 10, -9}

Use TERM_FIXED for the full set at each level. EPHEMERALS = [] (empty). This way ALL_TERMINALS = TERM_FIXED exactly.

Document the exact terminal set used at each level in the results.

**Grid dimensions:**
- Terminal counts: 4, 6, 8, 10, 12, 15, 20
- Population sizes: 1000, 2000, 5000
- Total cells: 7 × 3 = 21

**Per cell:**
- 5 seeds: 42, 7, 137, 2718, 31415
- MAX_SEED = 360s
- MAX_TOTAL = 1800s
- Record: found Leibniz (yes/no per seed), expression found, node count, generations, elapsed time

**Total runs:** 21 cells × 5 seeds = 105 runs. Worst case 105 × 360s = 10.5 hours. Most seeds will early-stop or fail fast.

## Implementation

Create a single parameterized script: `entropy-leibniz-v3/scaling_heatmap.py`

It should accept arguments:
```
python3 scaling_heatmap.py --terminals N --pop_size P
```

Or run the full grid:
```
python3 scaling_heatmap.py --full-grid
```

The full grid mode should:
1. Run all 21 cells
2. Parallelize across cells where possible (each cell is independent)
3. Write per-cell results to `scaling_heatmap_t{N}_p{P}.txt`
4. After all cells complete, write the summary table to `scaling_heatmap_results.md`

### Base the script on `entropy_leibniz_v3_minimal.py`
Changes from minimal:
- TERM_FIXED is parameterized by --terminals
- POP_SIZE is parameterized by --pop_size
- EPHEMERALS = [] (always empty)
- No injection (already removed in v3 minimal)
- Output files named by terminal count and population

### Existing data points we already have (DO NOT rerun these):
- terminals=4, pop=1000: 5/5 (from entropy_v3_minimal)
- terminals=15, pop=1000: 0/5 (from entropy stress test L1)

Include these in the results table but don't rerun them. That saves 10 runs.

## Output

### Per-cell files
`scaling_heatmap_t{N}_p{P}.txt` — standard TEVV format results

### Summary table: `scaling_heatmap_results.md`

```
# Scaling Heat Map: Terminals × Population → Discovery Rate

| Terminals | Pop=1000 | Pop=2000 | Pop=5000 |
|-----------|----------|----------|----------|
| 4         | 5/5*     | ?/5      | ?/5      |
| 6         | ?/5      | ?/5      | ?/5      |
| 8         | ?/5      | ?/5      | ?/5      |
| 10        | ?/5      | ?/5      | ?/5      |
| 12        | ?/5      | ?/5      | ?/5      |
| 15        | 0/5*     | ?/5      | ?/5      |
| 20        | ?/5      | ?/5      | ?/5      |

* = from prior experiment, not rerun
```

Also include for each cell: mean generations for successful seeds, mean elapsed time, and the most common wrong-limit attractor expression for failed seeds.

### Terminal sets used
Document the exact terminal set at each level in the results file.

## What to look for
- Is there a sharp phase transition or a gradual decline?
- Does pop=5000 rescue terminal counts that pop=1000 can't handle?
- At what terminal count does pop=2000 break? Pop=5000?
- What wrong-limit attractors appear at each terminal count? Do they change character as the terminal set grows?

## Note on equation bloat
Prior experiments showed entropy seeds produce algebraically equivalent but bloated expressions (e.g., 11-node `(-(-1^k)) / ((-k) - (k - -1))` instead of 9-node `(-1^k) / ((2*k) + 1)`). All such expressions were verified identical to Leibniz at k=100,000 with zero divergence. For this experiment, count any algebraically equivalent expression as "found Leibniz." The bloat issue is documented in RESEARCH_NOTES.md and will be discussed in the paper separately.
