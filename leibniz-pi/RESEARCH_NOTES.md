# Research Notes — Leibniz-Pi Project

Working notes, findings, theoretical observations, and editorial ideas accumulated during the research phase. This is not a polished document — it's a capture file for the preprint.

---

## Experiment Progression

| Experiment | Method | Result |
|---|---|---|
| RL v1/v2 | Policy gradient on term sequences | Diverges after T>20 |
| ACO | Pheromone-guided symbolic search | Collapses after T>40 |
| GP v1 | GP with naive convergence reward | Finds wrong-limit series (flatlines) |
| GP v2 | GP with convergence-rate fitness | 5/5 (injection was load-bearing — see v3) |
| Log-precision GP v2 | GP with log-precision fitness | 5/5 (injection was load-bearing — see v3) |
| GP v3 wide (clean) | 42 terminals, no injection | 0/5 |
| GP v3 hostile (clean) | 44 terminals, no 2, no injection | 0/5 |
| Log-precision v3 wide (clean) | 42 terminals, no injection | 0/5 |
| Log-precision v3 hostile (clean) | 44 terminals, no 2, no injection | 0/5 |
| GP v3 minimal | {k,1,-1,2}, no injection, pop=1000 | 2/5 at 360s/seed |
| GP v3 pop=2000 | {k,1,-1,2}, no injection, pop=2000 | 5/5 |
| GP sensitivity | alpha=0.5 | 4/5 |
| GP sensitivity | tournament_k=3 | 3/5 (faster: ~2500 gens) |
| GP sensitivity | parsimony changes | minimal effect |
| Log-precision v3 minimal | {k,1,-1,2}, no injection, pop=1000 | 5/5 (~6 min total) |
| Log-precision stress L1 | 15 terminals, no injection | 0/5 — wrong-limit attractors |
| Log-precision fitness fix: extended checkpoints | T up to 50000 | 0/5 |
| Log-precision fitness fix: large-T penalty w=0.1 | penalize T=10000 error | 1/5 (best result) |
| Log-precision fitness fix: large-T penalty w=0.5 | heavier penalty | 0/5 |
| Log-precision fitness fix: rate consistency | penalize rate variance | 0/5 |
| Gradient fitness: pure gradient magnitude | minimize gradient norm | 0/5 |
| Gradient fitness: hybrid scalar × uniformity | scalar × gradient balance | 0/5 |
| Gradient fitness: min-component bottleneck | worst dimension as score | 0/5 |
| Log-precision pop=2000 on 15 terminals | coverage control | 0/5 |
| Parsimony: LAMBDA_P=0.01 | 2x parsimony | (see parsimony_test_results.md) |
| Parsimony: LAMBDA_P=0.02 | 4x parsimony | (see parsimony_test_results.md) |
| Parsimony: LAMBDA_P=0.05 | 10x parsimony | (see parsimony_test_results.md) |
| Scaling grid: 7×4 (log-precision) | terminals × population heat map | see below |
| GP conv-aware: p=5000 column | all terminal counts | see below |
| GP conv-aware: p=10000 column | all terminal counts | see below |
| GP conv-aware: extended time | t=10, p=5000, 2hr/seed | PENDING |

---

## Key Scientific Findings

### The injection confound
GP v2 and Entropy v2 "5/5" results were artifacts of injecting the Leibniz tree at gen 0. The tree survived through elitism — it was retained, not discovered. Clean runs (no injection) go 0/5 with the original 55s budget. The injection also smuggled the constant 2 into the hostile terminal set, invalidating that experiment entirely.

### Log-precision fitness discovers Leibniz from scratch
With minimal terminal set {k, 1, -1, 2} and no injection, log-precision fitness finds Leibniz 5/5 in ~6 minutes. Five seeds, five different algebraic forms, all verified identical to Leibniz at k=100,000 with zero divergence:
- Seed 0: `(-(-1^k)) / ((-k) - (k - -1))` — 11 nodes
- Seed 1: `(-(-1^k)) / ((-1 - k) - k)` — 10 nodes
- Seed 2: same as Seed 1
- Seed 3: `(-1^k) / (k + (1 + k))` — 9 nodes
- Seed 4: `(-1^k) / ((k * 2) - -1)` — 9 nodes

### GP convergence fitness also discovers from scratch
With pop=2000, GP convergence fitness achieves 5/5 on minimal terminals. At pop=1000, only 2/5 — it's a coverage problem, not a fitness landscape problem.

### Terminal set is the critical variable
Log-precision fitness breaks sharply at 15 terminals. With 4 terminals, (-1)^k is essentially the only oscillating structure available. With 15, rational attractors like `5/((6+4k)(k-2))` are cheaper, more monotone, and accidentally close to π/4. The fitness can't distinguish "converges to π/4" from "converges near π/4 within the evaluation window."

### Unifying finding: discovery = fitness quality × coverage / search space
All failures are coverage failures. The fitness functions correctly rank Leibniz as optimal when both Leibniz and wrong-limit attractors are present. The problem is whether the initial population contains enough structural building blocks for Leibniz to be assembled through breeding. This is a combinatorial relationship — search space grows exponentially with terminal count, coverage grows linearly with population.

### Fitness modifications cannot rescue large terminal sets
Extended checkpoints, heavy large-T penalties, rate consistency checks, and gradient-based selection all failed to crack 15 terminals at pop=1000. The fitness function isn't the bottleneck. The wrong-limit attractors act as exploration scaffolding — penalizing them harder causes the population to collapse to zero rather than finding Leibniz.

---

## Scaling Heat Map Results (2026-03-15, log-precision fitness)

### Grid: 7 terminal counts × 4 population sizes

| Terminals | Pop=1000 | Pop=2000 | Pop=5000 | Pop=10000 |
|-----------|----------|----------|----------|-----------|
| 4         | 5/5*     | 4/5      | 5/5      | 5/5       |
| 6         | 1/5      | 2/5      | 1/5      | 1/5       |
| 8         | 1/5      | 1/5      | 1/5      | 0/5       |
| 10        | 0/5      | 0/5      | 0/5      | 0/5       |
| 12        | 0/5      | 0/5      | 0/5      | 0/5       |
| 15        | 0/5*     | 0/5      | 0/5      | 2/5       |
| 20        | 0/5      | 0/5      | 0/5      | 0/5       |

\* = from prior experiment

### Three regimes, not a sharp transition

The data does not support a simple phase transition. It shows three regimes:

1. **Reliable discovery (t=4).** 5/5 at pop=1000 and above (one anomalous 4/5 at pop=2000, analyzed below).
2. **Transition zone (t=6 through t=8).** Discovery is unreliable: 1/5 to 2/5 across all population sizes. Population does not help monotonically.
3. **Dead zone (t=10 through t=20).** 0/5 at all population sizes up to 5000, with one anomalous partial recovery at t=15/p=10000 (2/5).

Population size in the 1k–5k range does not shift the boundary. The phase boundary sits between t=8 and t=10 for all three population sizes. At pop=10000, two anomalies appear: t=8 drops to 0/5 (worse than lower populations), and t=15 recovers to 2/5 (better than lower populations).

### The t=15/p=10000 recovery

Seeds 2 (val=137) and 3 (val=2718) both found the canonical 9-node form `(-1^k) / (1 + (k*2))` at pop=10000. Seeds 0, 1, 4 timed out on wrong-limit attractors.

This suggests the attractor landscape at t=15 has a different structure than at t=10 or t=12. At pop=10000, the initial population is large enough that in 2/5 seeds, the correct building blocks appeared and were assembled before attractors dominated. This effect is absent at t=10–12, where either the attractor density is higher or the search space topology is qualitatively different. At t=20, even pop=10000 is insufficient.

The recovery is partial and stochastic. It does not undermine the coverage interpretation. It refines it: coverage at pop=10000 occasionally exceeds the threshold at t=15 but never at t=10–12 or t=20.

### The t=8/p=10000 inversion

At t=8, pop=10000 produced 0/5 while pop=1000/2000/5000 each produced 1/5. The dominant attractor was `(4 - (4-(-3))^-2 - k/(-3))^-2` and variants, with seed 1 achieving ti=20.66 bits, five bits better than Leibniz's 15.29 at T=10000. The attractor converges faster than Leibniz within the evaluation horizon.

More population = more chances to find this strong attractor early, which then dominates through selection before Leibniz building blocks can be assembled. Wrong-limit attractors benefit from larger populations just as the correct answer does. Population increase is not a monotonic advantage when strong attractors exist.

### The Grandi-Leibniz attractor (t=4, p=2000, seed 4)

Seed 4 (val=31415) at t=4/p=2000 found `(-1^k) * (-k) / ((1/2) - (-k))` with ti=15.29, mo=1.00. Early-stopped as converged. The equivalence test correctly rejected it (term 0 = 0, Leibniz term 0 = 1).

**Algebraic decomposition.** The expression simplifies to `(-1)^(k+1) * 2k/(2k+1)`. Each term decomposes as:

```
2k/(2k+1) = 1 - 1/(2k+1)
```

So each term equals `(-1)^(k+1) * (1 - 1/(2k+1))` = `-(-1)^k + (-1)^k/(2k+1)`.

The partial sum is:

```
S_att(T) = S_Leibniz(T) - G(T)
```

where G(T) = Σ_{k=0}^{T-1} (-1)^k is the Grandi series partial sum: 1 when T is odd, 0 when T is even.

**Consequence at even T:** S_att(T) = S_Leibniz(T) exactly. Not approximately. Mathematically identical.

**Consequence at odd T:** S_att(T) = S_Leibniz(T) - 1. Differs by exactly 1.

The series does not converge in the standard sense. It oscillates between two subsequential limits: the even-indexed partial sums converge to π/4, the odd-indexed to π/4 - 1.

**Why the fitness was blind to it.** The evaluation checkpoints are T ∈ {5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000}. Ten of eleven values are even. At every even checkpoint, S_att = S_Leibniz exactly. The single odd checkpoint (T=5) is an outlier washed out by ten identical-to-Leibniz values. The total info at T=10000 (even) is 15.29 bits, identical to Leibniz.

The mean_rate of 4.61 bits/decade (vs Leibniz's 3.32) is the only detectable difference. The T=5 outlier followed by T=10 (Leibniz-identical) creates a steeper apparent slope at the low end.

**What the GP actually did.** The GP assembled `(-1)^k * (-k) / (1/2 + k)` from scratch via crossover and mutation, with no representation of either Leibniz or the Grandi series. The decomposition into "Leibniz minus Grandi" is our analytical observation, not something the GP encoded.

**Is this "finding π"?** No. The even-subsequence convergence to π/4 is a structural consequence of the algebraic relationship to Leibniz. The attractor does not encode new information about π. It encodes a rearrangement of Leibniz that happens to be invisible to a mostly-even checkpoint grid.

**Significance.** This is the strongest example of the evaluation horizon trap in the entire project. The trap is not just about finite T. It is about the specific structure of the evaluation grid. A checkpoint set with more odd values (or all odd: 5, 11, 21, 51, ...) would immediately distinguish this attractor. The attractor exploits the particular checkpoints chosen, not just their finiteness.

### Wrong-limit attractor families by terminal count

The grid revealed distinct attractor families at different terminal counts:

**t=6:** `((k/3 + c)^-2)` family. The terminal 3 enables k/3, creating a family of converging rational expressions with finite limits.

**t=8:** `((k/(-3) + c)^-2)` family. Also nested rationals like `1/k / (k - 4/(k - 2/k))`. Some achieve ti > 20 bits, outscoring Leibniz on the finite evaluation.

**t=10+:** More diverse attractors. Additional terminals create more partial-fraction decompositions and telescoping series.

**t=15 failures (pop=10000):** `(-5/(-5+k))^7` (decaying power), `(7^7) * (-1^(k/-3))` (exponential constant times period-3 oscillator), `(-4 + k/(-3))^-2` (k/3 family).

---

## GP Convergence-Aware Scaling Results (2026-03-16, supplementary)

### Combined fitness comparison table

| Terminals | GP Conv p=5000 | GP Conv p=10000 | Log-precision p=5000 | Log-precision p=10000 |
|-----------|----------------|-----------------|----------------|-----------------|
| 4         | 4/5            | 5/5             | 5/5            | 5/5             |
| 6         | 1/5            | 4/5             | 1/5            | 1/5             |
| 8         | 0/5            | 0/5             | 1/5            | 0/5             |
| 10        | 1/5            | 0/5             | 0/5            | 0/5             |
| 12        | 0/5            | 0/5             | 0/5            | 0/5             |
| 15        | 1/5            | 0/5             | 0/5            | 2/5             |
| 20        | 0/5            | 0/5             | 0/5            | 0/5             |

### What the data shows

Neither fitness function is uniformly better. They differ at specific terminal counts and population sizes. But this comparison must be interpreted carefully.

**What we can say:**

The t=8 wall is real. Both fitness functions hit it. No tested population breaks through at t=8 for either fitness. At t=10 and above, both are in the dead zone with only sporadic single-seed hits that do not replicate.

At t=4, both fitness functions reliably discover Leibniz with sufficient population. Log-precision fitness achieves this at lower population (5/5 at p=1000) while convergence-aware needs more (5/5 at p=10000). This is consistent with the second-order signal being more efficient at exploiting available coverage.

At t=6, GP convergence at p=10000 (4/5) outperforms entropy at any tested population (max 2/5 at p=2000). This is the one data point where the convergence-aware fitness clearly does better.

**What we cannot say:**

We cannot claim the fitness functions have "complementary sweet spots" or that one is systematically better in certain regimes. Five seeds per cell is a pilot study. At 1/5, the 95% confidence interval for the true discovery rate spans roughly 0.5% to 72% (Clopper-Pearson). The difference between 0/5 and 1/5 is not statistically meaningful. Even 4/5 vs 1/5 has overlapping confidence intervals.

The GP convergence hits at t=10/p=5000 (1/5) and t=15/p=5000 (1/5) did not replicate at p=10000. These were likely lucky initializations, not a real signal about the fitness function's capability at those terminal counts.

**What this means for the paper:**

The honest framing: we observe interactions between fitness function, terminal count, and population size that we cannot fully characterize with 5 seeds per condition. A larger sensitivity analysis (50+ seeds per cell, finer population grid) would be needed to map the interaction surface. That is beyond the computational scope of this project.

What we can claim: (1) the t=8 boundary is robust across both fitness functions and all tested populations, (2) log-precision fitness is more sample-efficient at low terminal counts (requires less population for reliable discovery), (3) there exist conditions (t=6/p=10000) where convergence-aware fitness outperforms log-precision fitness, suggesting the interaction between fitness gradient steepness, attractor landscape, and coverage has structure we have not fully explored, and (4) the combinatorial ceiling dominates both fitness functions at t≥10.

The supplementary GP convergence data strengthens the paper by showing the findings are not fitness-function-specific. The wall at t=8, the combinatorial explosion, and the wrong-limit attractor phenomenon all hold regardless of whether the fitness asks a first-order or second-order question.

### Extended time test (t=10, p=5000, GP convergence)

[PENDING — Part 2 of CC_TASK_gp_scaling_extended.md. Tests whether giving 2 hours per seed (vs 30 min) rescues additional seeds at t=10. If only seed 7 succeeds again, it confirms the bottleneck is coverage (initialization luck), not time.]

---

## Combinatorial Coverage Analysis

### Why population can't fix the terminal count problem

The search space for expression trees grows exponentially with the number of terminals. For a tree with L leaf positions, each leaf can hold any of N terminals, giving N^L leaf configurations. Using the Leibniz tree (9 nodes, ~5 leaves) as a reference:

| Terminals (N) | N^5 (leaf configs) | N^9 (full tree scale) | Pop=5000 / N^9 |
|---------------|-------------------|-----------------------|-----------------|
| 4             | 1,024             | 262,144               | 1.9%            |
| 6             | 7,776             | 10,077,696            | 0.050%          |
| 8             | 32,768            | 134,217,728           | 0.0037%         |
| 10            | 100,000           | 1,000,000,000         | 0.00050%        |
| 12            | 248,832           | 5,159,780,352         | 0.000097%       |
| 15            | 759,375           | 38,443,359,375        | 0.000013%       |
| 20            | 3,200,000         | 512,000,000,000       | 0.00000098%     |

From t=4 to t=20, the search space grows by a factor of ~2 million. From pop=1000 to pop=10000, coverage grows by 10x. The population would need to reach hundreds of millions to maintain the same coverage ratio at t=20 that pop=1000 has at t=4.

### This applies equally to both fitness functions

The combinatorial explosion is a property of the search space, not the fitness function. Log-precision fitness has a steeper gradient than convergence-aware fitness, so it exploits whatever coverage exists more efficiently. But both are linear tools against an exponential problem. Log-precision fitness at t=10/p=5000 has 0.00050% coverage and goes 0/5. Convergence-aware at the same condition went 1/5 (one lucky seed, not replicated at p=10000).

### The t=15/p=10000 recovery in context

At t=15, N^9 ≈ 38 billion. Pop=10000 covers 0.000013%. In 2 of 5 random initializations (entropy), the right subtrees happened to be present. In 3, they weren't. This is what 0.000013% coverage looks like: the outcome is dominated by initialization luck, not by fitness function quality or population dynamics.

### Implication for the paper

The formula `discovery = fitness quality × coverage / search space` can be made quantitative. Coverage is O(population). Search space is O(N^L) where N is terminal count and L is tree size. The ratio population/N^L drops below any fixed threshold as N increases, regardless of fitness function quality. No fitness function can compensate for exponentially insufficient coverage.

This also explains why the phase boundary (t=8→t=10) is the same for pop=1000, pop=2000, and pop=5000. Going from pop=1000 to pop=5000 multiplies coverage by 5x. But the search space at t=10 is 4x larger than at t=8 (N^9 ratio: 10^9/8^9 ≈ 7.5x). The 5x population increase doesn't even cover the 7.5x space increase from two additional terminals. The boundary doesn't move because the linear and exponential terms are on the same order of magnitude in that range — and the exponential wins at t=10.

---

## Confabulation Analogy
The project frames wrong-limit series as analogues of LLM confabulation:
- ACO/RL = confabulation (sounds right, diverges under scrutiny)
- GP v1 = miscalibration (hits a plausible value, stops learning)
- Leibniz = calibrated (infinite improvement, constant precision gain rate)

---

## Second-Order Kinetics Connection

Leibniz's error decays as 1/(2T+1). That's 1/T behavior. Plot 1/error vs T — straight line. That's the signature of a second-order process.

In reaction kinetics:
- First-order reaction: exponential decay, concentration drops by constant fraction per unit time. Rate depends only on current concentration. One reactant.
- Second-order reaction: decay like 1/t. Rate depends on square of concentration, or on two reactants. Plot of 1/[A] vs time gives a straight line.

Leibniz has second-order structure. Each term's correction depends on TWO things: the position k (which determines magnitude) and the alternating sign (which determines direction). One thing decaying would give exponential convergence. Two things interacting gives 1/T convergence. That's why Leibniz is slow — it's fundamentally second-order.

The log-precision fitness measures how fast error decreases on a log scale: log(1/error) = log(2T+1). On a log-log plot, that's a straight line with constant slope. That's the integrated form of the second-order rate law. The constant rate of 3.32 bits per decade (= log₂(10)) is a property of Leibniz's 1/(2T+1) error decay, not of any thermodynamic process.

**The log-precision fitness is the integrated second-order rate law applied to convergence.** It selects for processes that obey second-order kinetics. Leibniz is the simplest process that does.

### Why log-precision fitness works better than GP convergence
- GP convergence asks: "Is error shrinking between checkpoints?" — first-order question. Many things shrink.
- Log-precision asks: "Is 1/error growing linearly?" — second-order question. Unique answer.
- The second-order question is more selective because fewer processes satisfy it.

### Efficiency framing (unexplored)
The most fundamental fitness might be: minimum work (operations) per unit of uncertainty reduced. Operations per bit. Leibniz uses 3 operations per term and gains 3.32 bits per decade. An 11-node bloated equivalent uses 5 operations per term for the same 3.32 bits. An efficiency fitness would naturally prefer the canonical 9-node form AND would be more physically grounded.

This was discussed but not implemented as an experiment.

### Gradient / vector space approach (explored, failed)
Attempted to use the gradient across fitness components as a selection criterion — minimize gradient magnitude (closest to balanced state). Three approaches tested on 15 terminals: pure gradient magnitude, hybrid scalar × uniformity, min-component bottleneck. All failed (0/5). The failure confirmed the diagnosis: it's a coverage problem, not a fitness problem. Even theoretically superior fitness functions can't compensate for insufficient search coverage.

---

## Preprint Paper Outline (Draft)

### Working Title
"Reverse Engineering Leibniz: Evolutionary Discovery of π/4 Series from Arithmetic Primitives"

### Sections
1. **Introduction** — Leibniz series, why it's special, what "rediscovery" means
2. **Background** — GP, symbolic regression, log-precision fitness, prior work on formula discovery
3. **The Mechanism** — How GP builds formulas from primitives. The parts bin, breeding, selection. Concrete examples.
4. **Two Fitness Functions** — Convergence-aware (first-order) and log-precision (second-order). Mathematical definitions.
5. **Experimental Design** — Terminal sets, injection confound, v3 clean protocol, seed values, time budgets
6. **Results** — Discovery rates, scaling grid (log-precision), GP convergence comparison, wrong-limit attractors, parameter sensitivity, fitness modifications, Grandi-Leibniz attractor analysis.
7. **The Scaling Boundary** — Three regimes (reliable / transition / dead zone). Combinatorial coverage analysis. Fitness function interactions we cannot fully characterize at 5 seeds/cell.
8. **Discussion** — Second-order kinetics connection (analogical, not rigorous). Evaluation horizon trap (checkpoint-structure-dependent, not just T-dependent). Linear vs exponential: why no fitness function can compensate. Limitations of 5-seed design.
9. **Conclusion** — What the fitness function defines vs what the search can find. The question is harder than the answer.

### Figures needed (updated)
- Heat map: discovery rate vs terminal count × population size (log-precision 7×4 grid)
- GP convergence comparison column (side-by-side with log-precision at p=5000 and p=10000)
- The Grandi-Leibniz attractor: checkpoint-by-checkpoint comparison showing identical values at even T, divergence at odd T
- Wrong-limit attractor info profiles at t=8: showing ti=20.66 exceeding Leibniz's 15.29
- Error decay comparison: Leibniz vs top wrong-limit attractors at each terminal count
- Information profile plot (bits vs T on log scale, 3.32 bits/decade line)
- Coverage ratio (population / N^L) vs terminal count, with discovery rate overlay

---

## Open Questions / Potential Experiments

### Checkpoint sensitivity
Would changing the checkpoint set to all-odd values (5, 11, 21, 51, 101, ...) change the discovery rate? The Grandi-Leibniz attractor would be immediately rejected. But would new attractors exploiting the odd structure appear?

### Attractor density vs terminal count
The non-monotonic behavior (dead at t=10-12, partial recovery at t=15) suggests attractor density is not a simple function of terminal count. What determines the attractor landscape? The specific integers available? The number of ways to construct converging rational functions? Formalizing this is a potential paper extension.

### Larger sensitivity study
The fitness function × terminal count × population interaction surface needs 50+ seeds per cell and finer population steps to characterize properly. This is computationally expensive but would resolve whether the t=6/p=10000 GP convergence result (4/5 vs entropy's 1/5) is a real interaction or noise.

### Efficiency fitness
Test bits-per-operation as a fitness function. Would naturally prefer canonical 9-node form over bloated equivalents. Not yet implemented.
