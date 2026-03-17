# Appendix: Seed Registry

All random seeds used across experiments. Seeds control `random.seed()` and `np.random.seed()` for deterministic reproducibility.

## Seed Source

Config: `entropy-leibniz-v3/config/scaling_heatmap_config.json`
Values: [42, 7, 137, 2718, 31415]

All experiments use this same set. The scaling heatmap runner loads them directly from that config file. All other experiments hardcode the same five values in their scripts. Source column reflects this distinction: "config" = loaded from file; "hardcoded" = same values, written directly into the script.

Note: the scaling heatmap config sets `max_seed_seconds = 1800`. All other experiments use `MAX_SEED = 360` hardcoded in their respective scripts, except the GP extended run which used a larger budget.

---

## Scaling Heatmap (Entropy Fitness)

27 cells: terminals in {4, 6, 8, 10, 12, 15, 20} x population in {1000, 2000, 5000, 10000}.
Note: the t15_p1000 cell is absent from the data files (missing from the heatmap run).

| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| scaling_heatmap_t4_p1000 | Entropy | 4 | 1000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t4_p2000 | Entropy | 4 | 2000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t4_p5000 | Entropy | 4 | 5000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t4_p10000 | Entropy | 4 | 10000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t6_p1000 | Entropy | 6 | 1000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t6_p2000 | Entropy | 6 | 2000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t6_p5000 | Entropy | 6 | 5000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t6_p10000 | Entropy | 6 | 10000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t8_p1000 | Entropy | 8 | 1000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t8_p2000 | Entropy | 8 | 2000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t8_p5000 | Entropy | 8 | 5000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t8_p10000 | Entropy | 8 | 10000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t10_p1000 | Entropy | 10 | 1000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t10_p2000 | Entropy | 10 | 2000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t10_p5000 | Entropy | 10 | 5000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t10_p10000 | Entropy | 10 | 10000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t12_p1000 | Entropy | 12 | 1000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t12_p2000 | Entropy | 12 | 2000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t12_p5000 | Entropy | 12 | 5000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t12_p10000 | Entropy | 12 | 10000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t15_p2000 | Entropy | 15 | 2000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t15_p5000 | Entropy | 15 | 5000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t15_p10000 | Entropy | 15 | 10000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t20_p1000 | Entropy | 20 | 1000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t20_p2000 | Entropy | 20 | 2000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t20_p5000 | Entropy | 20 | 5000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |
| scaling_heatmap_t20_p10000 | Entropy | 20 | 10000 | 42, 7, 137, 2718, 31415 | 1800s (config) | config |

Note: cells where all seeds finished before the time limit (t4, t6 at some populations) still used 1800s as the per-seed ceiling. Actual elapsed varies by cell.

---

## Scaling Column (GP Convergence-Aware, p=5000)

7 files in `gp-leibniz-v3/results_gp_scaling_p5000/`.

| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| gp_scaling_t4_p5000 | GP convergence-aware | 4 | 5000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |
| gp_scaling_t6_p5000 | GP convergence-aware | 6 | 5000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |
| gp_scaling_t8_p5000 | GP convergence-aware | 8 | 5000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |
| gp_scaling_t10_p5000 | GP convergence-aware | 10 | 5000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |
| gp_scaling_t12_p5000 | GP convergence-aware | 12 | 5000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |
| gp_scaling_t15_p5000 | GP convergence-aware | 15 | 5000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |
| gp_scaling_t20_p5000 | GP convergence-aware | 20 | 5000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |

---

## Scaling Column (GP Convergence-Aware, p=10000)

7 files in `gp-leibniz-v3/results_gp_scaling_p10000/`.

| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| gp_scaling_t4_p10000 | GP convergence-aware | 4 | 10000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |
| gp_scaling_t6_p10000 | GP convergence-aware | 6 | 10000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |
| gp_scaling_t8_p10000 | GP convergence-aware | 8 | 10000 | 42, 7, 137, 2718, 31415 | 1800s | hardcoded |
| gp_scaling_t10_p10000 | GP convergence-aware | 10 | 10000 | 42, 7, 137, 2718, 31415 | 1801s | hardcoded |
| gp_scaling_t12_p10000 | GP convergence-aware | 12 | 10000 | 42, 7, 137, 2718, 31415 | 1801s | hardcoded |
| gp_scaling_t15_p10000 | GP convergence-aware | 15 | 10000 | 42, 7, 137, 2718, 31415 | 1801s | hardcoded |
| gp_scaling_t20_p10000 | GP convergence-aware | 20 | 10000 | 42, 7, 137, 2718, 31415 | 1801s | hardcoded |

Note: the 1801s budget values are observed maximums from elapsed fields; the nominal limit is 1800s with minor timing overshoot.

---

## Extended Time Test (GP Convergence-Aware, t=10, p=5000)

1 file in `gp-leibniz-v3/results_gp_extended_t10_p5000/`.

| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| gp_extended_t10_p5000 | GP convergence-aware | 10 | 5000 | 42, 7, 137, 2718, 31415 | 7200s (nominal); seed 137 ran to 7873s before total budget cut | hardcoded |

Observed elapsed by seed: 42=7200s, 7=7200s, 137=7873s, 2718=6864s, 31415=6864s (seed 31415 stopped by total budget limit).

---

## Other Experiments

### Entropy Minimal Baseline

| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| entropy_data_minimal | Entropy | 4 | 1000 | 42, 7, 137, 2718, 31415 | 360s (hardcoded MAX_SEED) | hardcoded |

Note: all 5 seeds converged early (elapsed 20s to 153s); no seeds hit the time limit.

### Parsimony Pressure Sweep

Three runs varying `lambda_p` (parsimony coefficient). Terminals: 4 {k, 1, -1, 2}, pop=1000.

| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| parsimony_lp0.01 | Entropy (lambda_p=0.01) | 4 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |
| parsimony_lp0.02 | Entropy (lambda_p=0.02) | 4 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |
| parsimony_lp0.05 | Entropy (lambda_p=0.05) | 4 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |

### Stress Test (L1 Moderate)

| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| stress_L1 (moderate) | Entropy | 15 (4 fixed + 11 ephemerals) | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |

Terminal composition: fixed={k, 1, -1, 2}, ephemerals={-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5}. All 5 seeds ran to exactly ~360s.

### Fitness Sensitivity (Approaches 1, 2, 4)

Four variants of the entropy fitness function. Terminals: 4 {k, 1, -1, 2}, pop=1000.

| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| fitness_approach1 (large-T penalty, weight=0.1, k_max=50000) | Entropy variant | 4 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |
| fitness_approach2_w0.1 (rate consistency, weight=0.1) | Entropy variant | 4 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |
| fitness_approach2_w0.5 (rate consistency, weight=0.5) | Entropy variant | 4 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |
| fitness_approach4 (extended checkpoints, weight=0.1, k_max=10000) | Entropy variant | 4 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |

### Gradient-Based Selection (Approaches A, B, C, orig_pop2000)

No structured JSON data files exist for the gradient experiments; results are in `.txt` files only. Seed values confirmed from text output.

| Experiment | Fitness | Terminals | Pop | Seeds | Budget/seed | Source |
|---|---|---|---|---|---|---|
| gradient_approach_A (n_perturbations=5) | Entropy + gradient magnitude + CV | 15 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |
| gradient_approach_B (n_perturbations=5) | Entropy + gradient magnitude + CV | 15 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |
| gradient_approach_C (n_perturbations=5) | Entropy + gradient magnitude + CV | 15 | 1000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |
| gradient_approach_orig_pop2000 | Entropy (original fitness, larger pop) | 15 | 2000 | 42, 7, 137, 2718, 31415 | 360s | hardcoded |

---

## Nonstandard Seeds

**None.** Every experiment across all 46 data files (27 heatmap cells + 7 GP p5000 + 7 GP p10000 + 1 GP extended + 1 entropy minimal + 3 parsimony + 1 stress + 4 fitness sensitivity) plus 4 gradient text files uses exactly [42, 7, 137, 2718, 31415].

The seed set is fully consistent across the entire experiment corpus. The only variation is in how seeds are sourced: the scaling heatmap runner reads them from `entropy-leibniz-v3/config/scaling_heatmap_config.json` at runtime; all other experiments hardcode the same values directly in their Python scripts.
