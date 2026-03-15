# Gradient-Based Fitness — Thermodynamic Selection Results

**Date:** 2026-03-15
**Config:** 15 terminals `['k', 1, -1, 2, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]`, no injection, MAX_SEED=360s, MAX_TOTAL=1800s, n_perturbations=5

---

## 1. Calibration Table

All four approaches correctly rank Leibniz above the wrong-limit attractor `5/((6+4k)(k-2))`.

| Approach | Leibniz Fitness | Wrong-Limit Fitness | Zero Fitness | Leibniz > Wrong-Limit? | Margin |
|---|---|---|---|---|---|
| A: Pure gradient | -1.2914 | -1.4239 | -0.1119 | **True** | +0.1324 |
| B: Hybrid | 0.012842 | 0.004142 | -0.002031 | **True** | +0.0087 |
| C: Min-component | 0.260754 | 0.253529 | -0.005000 | **True** | +0.0072 |
| orig_pop2000 | 0.021021 | 0.007253 | -0.004861 | **True** | +0.0138 |

**Gradient diagnostics for calibration trees:**

| Tree | Entropy fitness | Grad magnitude | CV |
|---|---|---|---|
| Leibniz `(-1)^k/(2k+1)` | 0.02102 | ~1.24 | ~0.69 |
| Wrong-limit `5/((6+4k)(k-2))` | 0.00725 | ~1.32 | ~0.67 |
| Zero constant `0` | -0.00486 | ~0.11 | ~1.5 |

Key observation: the wrong-limit attractor has **higher total_info (15.93 bits vs 15.29)** and **higher mean_rate (4.31 vs 3.32 bits/decade)** under raw entropy components. It also has slightly larger gradient magnitude. The entropy fitness function correctly ranks Leibniz higher only because of parsimony (wrong-limit uses more nodes: 13 vs 9). This narrow margin (+0.014 in orig_pop2000) is the fundamental weakness with 15 terminals.

---

## 2. Summary Results Table

| Approach | Seeds Found | Best Expression(s) | Notes |
|---|---|---|---|
| Original (0/5 baseline) | 0/5 | `5/((6+4k)(k-2))` | from stress test |
| A: Pure gradient | 0/5 | `5/4` (constant) | Collapsed to low-node attractor |
| B: Hybrid | 0/5 | `(((k/3)+4)^-2)` seed 0; `0` seeds 1-4 | Zero constant dominates 4/5 seeds |
| C: Min-component | 0/5 | Various low-parsimony expressions | Found deep-converging but wrong-limit series |
| orig_pop2000: Coverage control | 0/5 | `(((k/3)+4)^-2)` | Same wrong-limit attractors, 0/5 |

**All approaches: 0/5 Leibniz recovery on the 15-terminal set.**

---

## 3. Per-Seed Details

### Approach A — Pure Gradient Magnitude

Fitness = `-magnitude - 0.005 * node_count`

All 5 seeds converged to **`(5 / 4)`** — a 3-node constant with fitness -0.015.

| Seed | Gens | Expression | Approach-A Fit | Entropy Fit | ti | mono |
|---|---|---|---|---|---|---|
| 0 (42) | 3518 | `(5 / 4)` | -0.0150 | -0.0407 | -13.61 | 0.00 |
| 1 (7) | 3587 | `(5 / 4)` | -0.0150 | -0.0407 | -13.61 | 0.00 |
| 2 (137) | 3618 | `(5 / 4)` | -0.0150 | -0.0407 | -13.61 | 0.00 |
| 3 (2718) | 3585 | `(5 / 4)` | -0.0150 | -0.0407 | -13.61 | 0.00 |
| 4 (31415) | 3397 | `(5 / 4)` | -0.0150 | -0.0407 | -13.61 | 0.00 |

**Diagnosis:** The pure gradient approach rewards small gradient magnitude — the GP maximizes by minimizing magnitude. A constant like `5/4` has near-zero gradient (mutations barely change it), so it becomes a local maximum. This is the fundamental inversion: the objective was to find high-information series, but negating magnitude means finding *flat* regions of landscape, not *steep* ones.

### Approach B — Hybrid (Entropy × Uniformity Bonus)

Fitness = `base_entropy_fitness * (1 / (1 + cv))`

| Seed | Gens | Expression | Approach-B Fit | Entropy Fit | ti | mono |
|---|---|---|---|---|---|---|
| 0 (42) | 2937 | `(((k/3)+4)^-2)` | 0.007831 | 0.012949 | 7.90 | 0.80 |
| 1 (7) | 3651 | `0` | -0.002031 | -0.004861 | 0.35 | 0.00 |
| 2 (137) | 3613 | `0` | -0.002031 | -0.004861 | 0.35 | 0.00 |
| 3 (2718) | 3723 | `0` | -0.002031 | -0.004861 | 0.35 | 0.00 |
| 4 (31415) | 3871 | `0` | -0.002031 | -0.004861 | 0.35 | 0.00 |

**Diagnosis:** 4/5 seeds collapsed to the zero constant. The uniformity bonus `1/(1+cv)` is maximized when gradient changes are perfectly uniform across components — the zero constant achieves this trivially (all mutations produce near-identical near-zero changes). Approach B failed even worse than the original: the wrong-limit attractor is suppressed too much by its modestly uneven gradient, while the zero constant receives a near-perfect uniformity bonus of ~0.41 (cv≈1.45). Seed 0 found a monotone partial-sum series `(k/3+4)^-2` that converges — but to the wrong limit.

### Approach C — Min-Component Bottleneck

Fitness = `min(V[0..3]) - 0.005 * node_count` where V = [total_info/50, monotonicity, mean_rate/5, parsimony_eff]

| Seed | Gens | Expression | C-Fit | Entropy Fit | ti | mono |
|---|---|---|---|---|---|---|
| 0 (42) | 3695 | `((((((2/-5)/5)+-5)^-2)/k)/(k+-5))` | 0.3023 | 0.00288 | 18.86 | 0.90 |
| 1 (7) | 974 | `(((((-3-4)^-3)-4)/(k/2))/((4--3)*(2-k)))` | 0.2496 | -0.01967 | 17.23 | 1.00 |
| 2 (137) | 1440 | `((2/(k+-5))/((2/(4+(5/4)))+(5*4)))` | 0.2150 | -0.03579 | 16.77 | 0.30 |
| 3 (2718) | 1745 | `(-3/((((1-k)+2)*((k-1)+(5--3)))/-1))` | 0.1813 | -0.01679 | 13.31 | 1.00 |
| 4 (31415) | 2185 | `((4^-5)/(((2^-1)+(((2+4)^-2)+3))^2))` | 0.1150 | -0.05443 | 10.46 | 0.20 |

**Diagnosis:** Approach C found the most interesting (but wrong) expressions. The min-component objective forces balance: every component must be high for high fitness. Seeds 0 and 1 found series converging to near π/4 with ~17-19 bits of precision at T=10000, but none are Leibniz. These are partial-fraction decompositions that happen to sum near π/4 — new wrong-limit attractors discovered by the bottleneck pressure. The min-component objective successfully avoids the zero-constant collapse but trades it for a different set of attractors that are high in all 4 components simultaneously.

### Approach orig_pop2000 — Original Entropy Fitness, POP_SIZE=2000

| Seed | Gens | Expression | Entropy Fit | ti | mono |
|---|---|---|---|---|---|
| 0 (42) | 7090 | `(((k/3)+4)^-2)` | 0.01295 | 7.90 | 0.80 |
| 1 (7) | 6805 | `((5/-4)^(k/-5))` | -0.00467 | 7.04 | 0.40 |
| 2 (137) | 5796 | `((5^-5)/4)` | -0.00411 | 6.10 | 0.20 |
| 3 (2718) | 3737 | `((-5^-5)/-4)` | -0.00411 | 6.10 | 0.20 |
| 4 (31415) | 5590 | `((5^-5)/4)` | -0.00411 | 6.10 | 0.20 |

**Diagnosis:** The coverage control confirms the problem is the 15-terminal set, not search volume. Even with pop=2000 running ~6000-7000 generations per seed, every seed converges to small wrong-limit constants or near-constant partial series. No seed found Leibniz. This extends the earlier stress test result (0/5 at pop=1000) — the 15-terminal landscape failure is robust to doubling population.

---

## 4. Gradient Diagnostics

### Why approach A fails: gradient inversion

The gradient magnitude for Leibniz is ~1.24 and for the wrong-limit attractor ~1.32. The zero constant has magnitude ~0.11. Negating magnitude means the GP selects for **minimum change under mutation** — constants win because their gradient is near zero. The approach is inverted: it finds the *flattest* part of the landscape, not the most informative.

### Why approach B fails: cv attractor

The zero constant has CV ~1.5 (very non-uniform gradient). But the GP still converges to it because the uniformity bonus is `1/(1+cv)`. With `cv=1.5`, uniformity = 0.40. Meanwhile, the base entropy fitness of zero is -0.00486, giving a product of ~-0.002. Any non-zero expression with worse entropy fitness and worse CV ends up lower. The zero constant wins not because it's genuinely uniform, but because it avoids the large negative base fitness of poor series while maintaining a cv-penalty floor.

### Why approach C finds something but not Leibniz

The min-component vector forces all of [ti/50, mono, rate/5, parsimony_eff] to be non-zero simultaneously. This successfully avoids collapse. But the 15-terminal set still produces rational partial-fraction attractors (seed 0: 18.86 bits at T=10000 but wrong limit) that score highly on all 4 components. The min-component principle is sound, but the wrong-limit attractors in the 15-terminal landscape also satisfy it.

---

## 5. Findings

### Does thermodynamic selection work?

**No.** None of the three gradient approaches (A, B, C) found Leibniz. All 4 conditions — including the coverage control — scored 0/5.

- **Approach A (pure gradient magnitude)** is fatally inverted: minimizing gradient magnitude selects for flat landscape regions (constants), not informative series.
- **Approach B (hybrid × uniformity)** reduces to the zero attractor in 4/5 seeds. The uniformity bonus doesn't provide meaningful gradient toward Leibniz.
- **Approach C (min-component bottleneck)** is conceptually the most interesting and discovers non-trivial series (18+ bits of precision at T=10000!), but always wrong-limit attractors. The 15-terminal set is too rich in rational expressions that accidentally satisfy all four components.

### Does coverage explain it all?

**Yes, this confirms coverage is the dominant variable.** The `orig_pop2000` control (entropy fitness, pop=2000, 15 terminals) scored 0/5 — matching the previous stress test result at pop=1000. Doubling population to 2000 doesn't help with 15 terminals. Compare:

- 4 terminals (minimal set), entropy fitness, pop=1000 → **5/5** (from entropy_leibniz_v3_minimal)
- 15 terminals, entropy fitness, pop=1000 → **0/5** (stress test level 1)
- 15 terminals, entropy fitness, pop=2000 → **0/5** (this experiment)
- 15 terminals, any gradient approach, pop=1000 → **0/5** (this experiment)

The 15-terminal landscape contains wrong-limit attractors (`5/((6+4k)(k-2))` and variants) that are **locally better than Leibniz** under the entropy fitness when parsimony is loose. With 4 terminals, `(-1)^k` is essentially the only oscillating structure — the fitness landscape has a single dominant basin. With 15 terminals, many rational expressions can accidentally converge near π/4 within a finite evaluation window.

### Key asymmetry

The wrong-limit attractor has **higher raw information** (15.93 vs 15.29 bits at T=10000) and **higher rate** (4.31 vs 3.32 bits/decade) than Leibniz. Leibniz wins under the entropy fitness only because it uses fewer nodes (9 vs 13, saving 0.02 parsimony). With 15 terminals, the search space is large enough that many such compact rational attractors exist, and the fitness landscape is not well-separated enough for the correct gradient to dominate.

### Recommendation

The gradient/thermodynamic selection approaches do not solve the 15-terminal problem. The root cause is a **fitness landscape issue**, not a search dynamics issue. A more promising direction would be:
1. Extending the evaluation window beyond T=10000 so wrong-limit series expose themselves (they flatten or diverge beyond the partial sum horizon)
2. Adding direct convergence verification at T=50000 or T=100000 as part of fitness
3. Re-examining whether a tighter parsimony penalty could break the wrong-limit basin

---

## Files

- `gradient_fitness_test.py` — Script implementing all 4 approaches
- `gradient_approach_A_results.txt` — Approach A per-seed results
- `gradient_approach_B_results.txt` — Approach B per-seed results
- `gradient_approach_C_results.txt` — Approach C per-seed results
- `gradient_approach_orig_pop2000_results.txt` — Coverage control results
