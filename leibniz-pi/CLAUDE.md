# Leibniz-Pi

A research project exploring whether different optimization paradigms can rediscover the Leibniz series (π/4 = 1 − 1/3 + 1/5 − 1/7 + …) from scratch — without being told what to look for.

## Project Goal

Given only arithmetic building blocks and a convergence objective, can an optimizer find `(-1)^k / (2k+1)`? The challenge: naive optimizers find compact expressions that approximate π/4 at finite T but flatline. Leibniz keeps gaining precision forever. Success requires rewarding *process*, not proximity.

## Structure

```
EDA/                        # Early exploratory experiments (v1)
  rl-leibniz/               # Reinforcement learning approach (v1 + v2)
  aco-leibniz/              # Ant Colony Optimization approach
  gp-leibniz/               # Genetic Programming v1 (convergence-rate fitness)

gp-leibniz-v2/              # GP v2: convergence-aware fitness — 5/5 seeds find Leibniz
entropy-leibniz/            # GP with information-theoretic fitness — 5/5 seeds find Leibniz

gp-leibniz-v3/              # v3 robustness tests: wide/hostile/minimal terminal sets + sensitivity sweep
  gp_leibniz_v3_wide.py     # Wide pool (41 terminals) — 0/5 clean
  gp_leibniz_v3_hostile.py  # Hostile pool (no 2) — 0/5 clean
  gp_leibniz_v3_minimal.py  # Minimal {k,1,-1,2}, no injection — 2/5
  gp_sensitivity_sweep.py   # Parameterized sensitivity sweep (argparse)
  parameter_sensitivity.md  # Sweep results: pop_size=2000 → 5/5

entropy-leibniz-v3/         # Entropy v3 robustness + stress tests
  entropy_leibniz_v3_*.py   # Wide/hostile/minimal variants
  entropy_stress_test.py    # Progressive difficulty levels (argparse --level)
  stress_test_results.md    # Level 1 (15 terminals) → 0/5; stopped

v3_results_summary.md       # Full corrected v3 results (injection confound documented)
medium_draft_final.md       # Pi Day article: "The Wave That Never Collapses"
figures/paperbanana/        # Generated diagram assets
```

## Experiment Progression

| Experiment | Method | Result |
|---|---|---|
| RL v1/v2 | Policy gradient on term sequences | Diverges after T>20 |
| ACO | Pheromone-guided symbolic search | Collapses after T>40 |
| GP v1 | GP with naive convergence reward | Finds wrong-limit series (flatlines) |
| GP v2 | GP with convergence-rate fitness | ✓ 5/5 (injection was load-bearing — see v3) |
| Entropy-GP | GP with info-theoretic fitness (−log₂\|error\|) | ✓ 5/5 (injection was load-bearing — see v3) |
| GP v3 minimal | Convergence fitness, {k,1,-1,2}, no injection | 2/5 at 30min |
| GP v3 pop=2000 | Same + doubled population | ✓ 5/5 (~10k gens, ~30min) |
| Entropy v3 minimal | Entropy fitness, {k,1,-1,2}, no injection | ✓ 5/5 (~6min total) |
| Entropy stress L1 | Entropy fitness, 15 terminals, no injection | 0/5 — wrong-limit attractors |

## Key Scientific Insights

**The injection confound:** GP v2 and Entropy v2 "5/5" results were artifacts of injecting the Leibniz tree at gen 0. The tree survived through elitism — it was retained, not discovered. Clean runs (no injection) both go 0/5 with the original 55s budget.

**Entropy without injection:** With the minimal terminal set {k, 1, -1, 2} and no injection, entropy fitness finds Leibniz 5/5 in ~6 minutes. The fitness landscape has a strong enough gradient. GP (convergence-rate) manages 2/5 in 30 minutes; pop=2000 achieves 5/5.

**Terminal set is the critical variable:** Entropy fitness breaks sharply at 15 terminals. With 4 terminals, `(-1)^k` is essentially the only oscillating structure available. With 15, rational attractors like `5/((6+4k)(k-2))` are cheaper, more monotone, and accidentally close to π/4. The fitness can't distinguish "converges to π/4" from "converges toward π/4 within the evaluation window."

**GP is a search-coverage problem:** Every GP configuration that found Leibniz found the exact formula. Failures converge to wrong-limit attractors (primarily `(-11)^-4`). The dominant fix is population size: doubling from 1000→2000 is enough for 5/5 with 4 terminals.

## GP Engine (shared by v2 and v3 variants)

- Population 1000 (v2/baseline), 2000 (optimal for clean discovery)
- Tournament size 7, elitism 5
- Ramped half-and-half initialization, subtree crossover/mutation
- Fitness cache keyed by expression string
- **v2:** Leibniz tree injected at gen 0 (load-bearing — results were artifact)
- **v3:** No injection — pure random initialization
- Early stopping: stable 100 gens AND info at T_max ≥ 13 bits AND monotone profile

## Entropy Fitness Function

```python
info(T) = -log2(|partial_sum(T) - π/4|)   # bits of precision

fitness = W1*(total_info/50) + W2*monotonicity + W3*(mean_rate/5) - LAMBDA_P*nodes
```

- `total_info` = info at T=10000
- `monotonicity` = fraction of checkpoint pairs with ≥ 0.5 bits gain
- `mean_rate` = endpoint-to-endpoint bits/log₁₀-decade
- Weights: W1=0.02, W2=0.04, W3=0.03, LAMBDA_P=0.005

## Confabulation Analogy

The project frames wrong-limit series as analogues of LLM confabulation:
- ACO/RL = confabulation (sounds right, diverges under scrutiny)
- GP v1 = miscalibration (hits a plausible value, stops learning)
- Leibniz = calibrated (infinite improvement, constant information gain rate)
