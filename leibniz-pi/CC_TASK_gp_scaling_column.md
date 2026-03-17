# CC Task: Convergence-Aware (Slime Mold) Fitness — p=5000, All Terminal Counts

## Context

The scaling heat map used entropy (information-theoretic) fitness only. This is a curiosity run: same grid structure but using the convergence-aware fitness (the "slime mold" approach from `gp-leibniz-v3/gp_sensitivity_sweep.py`), at pop=5000 only, across all 7 terminal counts.

This is NOT a primary experiment for the paper. It's supplementary. Don't over-engineer it.

## What to Build

Create `gp-leibniz-v3/gp_scaling_column.py`. Fork from `entropy-leibniz-v3/scaling_heatmap.py` with these changes:

### 1. Replace the fitness function

Swap out the entropy fitness for the convergence-aware fitness from `gp-leibniz-v3/gp_sensitivity_sweep.py`:

```python
# Convergence-aware fitness
# accuracy = -mean(|partial_sum(T) - π/4| for T in T_EVAL)
# convergence_bonus = fraction of consecutive T-pairs with >5% error reduction
# fitness = accuracy + ALPHA * convergence_bonus - LAMBDA_P * node_count
```

Use the exact same fitness logic as `gp_sensitivity_sweep.py`, including:
- T_EVAL = [10, 50, 200, 1000, 5000]
- K_MAX = 5000
- ALPHA = 0.05
- LAMBDA_P = 0.005

### 2. Parameterize terminals

Use the same `make_terminals(n)` function from the entropy scaling heatmap. Same terminal sets at each N.

### 3. Fixed configuration

- Pop size: 5000 (hardcoded, this is a single-column run)
- Terminal counts: [4, 6, 8, 10, 12, 15, 20]
- Seeds: [42, 7, 137, 2718, 31415]
- MAX_SEED = 1800s
- MAX_TOTAL = 10800s
- No injection

### 4. Parallelism

Use the same in-process Pool pattern from the entropy scaling heatmap. Load max_workers from `entropy-leibniz-v3/config/scaling_heatmap_config.json` (it's 5).

### 5. Output — ALL results go to a dedicated directory

Create `gp-leibniz-v3/results_gp_scaling_p5000/` and write ALL output there:

```
gp-leibniz-v3/results_gp_scaling_p5000/
├── gp_scaling_t4_p5000.txt
├── gp_scaling_t4_p5000_data.json
├── gp_scaling_t4_p5000.log
├── gp_scaling_t6_p5000.txt
├── gp_scaling_t6_p5000_data.json
├── gp_scaling_t6_p5000.log
├── ... (all 7 terminal counts)
├── gp_scaling_results.md          (summary table)
└── gp_scaling_column_config.txt   (record of all parameters used)
```

The config record file should dump every parameter value: fitness function name, ALPHA, LAMBDA_P, T_EVAL, K_MAX, POP_SIZE, MAX_SEED, MAX_TOTAL, terminal counts, seeds, max_workers, and the terminal set at each N.

The summary table should compare against entropy results:

```
| Terminals | GP Conv p=5000 | Entropy p=5000 |
|-----------|----------------|----------------|
| 4         | ?/5            | 5/5            |
| 6         | ?/5            | 1/5            |
| 8         | ?/5            | 1/5            |
| 10        | ?/5            | 0/5            |
| 12        | ?/5            | 0/5            |
| 15        | ?/5            | 0/5            |
| 20        | ?/5            | 0/5            |
```

Pull the entropy column from `entropy-leibniz-v3/scaling_heatmap_results.md`.

### 6. Equivalence test

Same as entropy: first 20 terms match Leibniz to 1e-6 per term.

### 7. Track stop reason

Same as entropy scaling heatmap: early_stop_converged, time_limit_seed, time_limit_total.

## Run It

```bash
cd ~/Documents/GitHub/ai-demos/leibniz-pi/gp-leibniz-v3
python3 gp_scaling_column.py
```

## Do NOT

- Do not modify any existing scripts
- Do not run the entropy fitness — it's already done
- Do not change the terminal set construction — use the same make_terminals() as the entropy version
- Do not add a config file for this — it's a one-off curiosity run
- Do not write ANY output files outside of `gp-leibniz-v3/results_gp_scaling_p5000/`
