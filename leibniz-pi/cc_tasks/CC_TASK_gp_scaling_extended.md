# CC Task: GP Convergence-Aware Fitness — p=10000 Column + Extended Time Test

## Context

The GP convergence-aware scaling column at p=5000 produced surprises: 1/5 at t=10 and t=15, where entropy at p=5000 went 0/5. This follow-up has two parts.

Seeds MUST come from the config file at `entropy-leibniz-v3/config/scaling_heatmap_config.json` (key: `"seeds"`). Do NOT hardcode seed values in the script. Load them from config. This applies to both Part 1 and Part 2.

## Part 1: p=10000 Column (all 7 terminal counts)

Same structure as the p=5000 run, but with pop=10000.

Fork `gp-leibniz-v3/gp_scaling_column.py` or modify it to accept `--pop_size` as an argument. If modifying, keep the default at 5000 and add the flag.

### Configuration
- Pop size: 10000
- Terminal counts: from config `["grid"]["terminal_counts"]`
- Seeds: from config `["seeds"]` — do NOT hardcode
- MAX_SEED = from config `["time_budgets"]["max_seed_seconds"]`
- MAX_TOTAL = from config `["time_budgets"]["max_total_seconds"]`
- Same convergence-aware fitness (ALPHA=0.05, LAMBDA_P=0.005)
- Max workers: from config `["parallelism"]["max_workers"]`

### Output
All output to `gp-leibniz-v3/results_gp_scaling_p10000/`:
- Per-cell files: `gp_scaling_t{N}_p10000.txt`, `_data.json`, `.log`
- Summary: `gp_scaling_results.md` — include comparison columns for entropy p=10000 AND GP conv p=5000

The comparison table should be:

```
| Terminals | GP Conv p=5000 | GP Conv p=10000 | Entropy p=5000 | Entropy p=10000 |
|-----------|----------------|-----------------|----------------|-----------------|
| 4         | 4/5            | ?/5             | 5/5            | 5/5             |
| 6         | 1/5            | ?/5             | 1/5            | 1/5             |
| 8         | 0/5            | ?/5             | 1/5            | 0/5             |
| 10        | 1/5            | ?/5             | 0/5            | 0/5             |
| 12        | 0/5            | ?/5             | 0/5            | 0/5             |
| 15        | 1/5            | ?/5             | 0/5            | 2/5             |
| 20        | 0/5            | ?/5             | 0/5            | 0/5             |
```

Pull entropy p=5000 from `entropy-leibniz-v3/scaling_heatmap_results.md`.
Pull entropy p=10000 from the same file (the extra column).
Pull GP conv p=5000 from `gp-leibniz-v3/results_gp_scaling_p5000/gp_scaling_results.md`.

## Part 2: Extended Time Test — t=10, p=5000, GP convergence-aware

Single condition: terminals=10, pop=5000, convergence-aware fitness.
MAX_SEED = 7200s (2 hours per seed).
MAX_TOTAL = 36000s (10 hours).
Seeds: from config `["seeds"]` — do NOT hardcode.

At p=5000/t=10 in the 30-min run, seed 1 (val=7) found Leibniz. This test asks: with 4x the time budget, do any additional seeds find it?

### Output
All output to `gp-leibniz-v3/results_gp_extended_t10_p5000/`:
- `gp_extended_t10_p5000.txt`
- `gp_extended_t10_p5000_data.json`
- `gp_extended_t10_p5000.log`
- `gp_extended_config.txt` (all parameters)

### Run Order

Run Part 1 first (p=10000 column). When that completes, run Part 2 (extended time test). Do not run them simultaneously — Part 2 is long and would compete for CPU.

## Part 3: After ALL runs complete, generate the master seed table

After both Part 1 and Part 2 are done, generate `paper/appendix_seed_table.md`. This table documents every seed used across every experiment in the project, for the paper appendix.

Scan all `_data.json` files across the entire repo:
- `entropy-leibniz-v3/scaling_heatmap_t*_p*_data.json`
- `entropy-leibniz-v3/entropy_data_minimal.json`
- `gp-leibniz-v3/results_gp_scaling_p5000/gp_scaling_t*_p5000_data.json`
- `gp-leibniz-v3/results_gp_scaling_p10000/gp_scaling_t*_p10000_data.json`
- `gp-leibniz-v3/results_gp_extended_t10_p5000/gp_extended_t10_p5000_data.json`
- `entropy-leibniz-v3/parsimony_lp*_data.json`
- `entropy-leibniz-v3/stress_L1_data.json`
- `entropy-leibniz-v3/fitness_approach*_data.json`
- `entropy-leibniz-v3/gradient_approach*_results.txt` (parse if structured)

For each experiment, extract:
- Experiment name / label
- Fitness function (entropy or convergence-aware)
- Terminal count
- Population size
- Seed values used (list of all seed_val)
- MAX_SEED budget
- Source config file (if any) or "hardcoded"

Format as a markdown table:

```
# Appendix: Seed Registry

All random seeds used across experiments. Seeds control `random.seed()` and
`np.random.seed()` for deterministic reproducibility.

## Seed Source
Config: `entropy-leibniz-v3/config/scaling_heatmap_config.json`
Values: [42, 7, 137, 2718, 31415]

## Experiments Using Config Seeds
| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | [42,7,137,2718,31415] | 1800s | config |

## Experiments Using Hardcoded Seeds
| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | [42,7,137,2718,31415] | 360s | hardcoded |
```

Also flag any experiment where seeds DON'T match [42, 7, 137, 2718, 31415]. There shouldn't be any, but verify.

## Do NOT

- Do not modify the entropy scaling heatmap results
- Do not overwrite the p=5000 results
- Do not write output files outside the designated results directories
- Do not run Part 2 until Part 1 is complete
- Do not hardcode seed values — always load from config
