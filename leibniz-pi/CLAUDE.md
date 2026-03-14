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

medium_draft_final.md       # Pi Day article: "The Wave That Never Collapses"
```

## Experiment Progression

| Experiment | Method | Result |
|---|---|---|
| RL v1/v2 | Policy gradient on term sequences | Diverges after T>20 |
| ACO | Pheromone-guided symbolic search | Collapses after T>40 |
| GP v1 | GP with naive convergence reward | Finds wrong-limit series (flatlines) |
| GP v2 | GP with convergence-rate fitness | ✓ 5/5 seeds find Leibniz |
| Entropy-GP | GP with info-theoretic fitness (−log₂\|error\|) | ✓ 5/5 seeds find Leibniz |

## Key Scientific Insight

Two independent fitness framings both recover Leibniz:

1. **Convergence-rate framing** (GP v2): reward series whose error keeps decreasing across checkpoints T=10, 50, 200, 1k, 5k, penalize tree complexity
2. **Information-theoretic framing** (Entropy-GP): reward sustained bits-of-precision gain at ~3.32 bits/log₁₀-decade, penalize complexity

Neither framing encodes Leibniz structure. The formula emerges as the simplest rule satisfying the constraints.

## GP Engine (shared by v2 and Entropy)

- Population 1000, tournament size 7, elitism 5
- Ramped half-and-half initialization, subtree crossover/mutation
- Fitness cache keyed by expression string
- Leibniz tree injected at gen 0 of every seed (calibration baseline)
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
