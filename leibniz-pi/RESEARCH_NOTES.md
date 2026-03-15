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
| Entropy-GP v2 | GP with info-theoretic fitness | 5/5 (injection was load-bearing — see v3) |
| GP v3 wide (clean) | 42 terminals, no injection | 0/5 |
| GP v3 hostile (clean) | 44 terminals, no 2, no injection | 0/5 |
| Entropy v3 wide (clean) | 42 terminals, no injection | 0/5 |
| Entropy v3 hostile (clean) | 44 terminals, no 2, no injection | 0/5 |
| GP v3 minimal | {k,1,-1,2}, no injection, pop=1000 | 2/5 at 360s/seed |
| GP v3 pop=2000 | {k,1,-1,2}, no injection, pop=2000 | 5/5 |
| GP sensitivity | alpha=0.5 | 4/5 |
| GP sensitivity | tournament_k=3 | 3/5 (faster: ~2500 gens) |
| GP sensitivity | parsimony changes | minimal effect |
| Entropy v3 minimal | {k,1,-1,2}, no injection, pop=1000 | 5/5 (~6 min total) |
| Entropy stress L1 | 15 terminals, no injection | 0/5 — wrong-limit attractors |
| Entropy fitness fix: extended checkpoints | T up to 50000 | 0/5 |
| Entropy fitness fix: large-T penalty w=0.1 | penalize T=10000 error | 1/5 (best result) |
| Entropy fitness fix: large-T penalty w=0.5 | heavier penalty | 0/5 |
| Entropy fitness fix: rate consistency | penalize rate variance | 0/5 |
| Gradient fitness: pure gradient magnitude | minimize gradient norm | 0/5 |
| Gradient fitness: hybrid scalar × uniformity | scalar × gradient balance | 0/5 |
| Gradient fitness: min-component bottleneck | worst dimension as score | 0/5 |
| Entropy pop=2000 on 15 terminals | coverage control | 0/5 |
| Parsimony: LAMBDA_P=0.01 | 2x parsimony | (see parsimony_test_results.md) |
| Parsimony: LAMBDA_P=0.02 | 4x parsimony | (see parsimony_test_results.md) |
| Parsimony: LAMBDA_P=0.05 | 10x parsimony | (see parsimony_test_results.md) |

---

## Key Scientific Findings

### The injection confound
GP v2 and Entropy v2 "5/5" results were artifacts of injecting the Leibniz tree at gen 0. The tree survived through elitism — it was retained, not discovered. Clean runs (no injection) go 0/5 with the original 55s budget. The injection also smuggled the constant 2 into the hostile terminal set, invalidating that experiment entirely.

### Entropy discovers Leibniz from scratch
With minimal terminal set {k, 1, -1, 2} and no injection, entropy fitness finds Leibniz 5/5 in ~6 minutes. Five seeds, five different algebraic forms, all verified identical to Leibniz at k=100,000 with zero divergence:
- Seed 0: `(-(-1^k)) / ((-k) - (k - -1))` — 11 nodes
- Seed 1: `(-(-1^k)) / ((-1 - k) - k)` — 10 nodes
- Seed 2: same as Seed 1
- Seed 3: `(-1^k) / (k + (1 + k))` — 9 nodes
- Seed 4: `(-1^k) / ((k * 2) - -1)` — 9 nodes

### GP convergence fitness also discovers from scratch
With pop=2000, GP convergence fitness achieves 5/5 on minimal terminals. At pop=1000, only 2/5 — it's a coverage problem, not a fitness landscape problem.

### Terminal set is the critical variable
Entropy breaks sharply at 15 terminals. With 4 terminals, (-1)^k is essentially the only oscillating structure available. With 15, rational attractors like `5/((6+4k)(k-2))` are cheaper, more monotone, and accidentally close to π/4. The fitness can't distinguish "converges to π/4" from "converges near π/4 within the evaluation window."

### Unifying finding: discovery = fitness quality × coverage / search space
All failures are coverage failures. The fitness functions correctly rank Leibniz as optimal when both Leibniz and wrong-limit attractors are present. The problem is whether the initial population contains enough structural building blocks for Leibniz to be assembled through breeding. This is a combinatorial relationship — search space grows exponentially with terminal count, coverage grows linearly with population.

### Fitness modifications cannot rescue large terminal sets
Extended checkpoints, heavy large-T penalties, rate consistency checks, and gradient-based thermodynamic selection all failed to crack 15 terminals at pop=1000. The fitness function isn't the bottleneck. The wrong-limit attractors act as exploration scaffolding — penalizing them harder causes the population to collapse to zero rather than finding Leibniz.

---

## Confabulation Analogy
The project frames wrong-limit series as analogues of LLM confabulation:
- ACO/RL = confabulation (sounds right, diverges under scrutiny)
- GP v1 = miscalibration (hits a plausible value, stops learning)
- Leibniz = calibrated (infinite improvement, constant information gain rate)

---

## Second-Order Kinetics / Thermodynamic Connection

Leibniz's error decays as 1/(2T+1). That's 1/T behavior. Plot 1/error vs T — straight line. That's the signature of a second-order process.

In reaction kinetics:
- First-order reaction: exponential decay, concentration drops by constant fraction per unit time. Rate depends only on current concentration. One reactant.
- Second-order reaction: decay like 1/t. Rate depends on square of concentration, or on two reactants. Plot of 1/[A] vs time gives a straight line.

Leibniz has second-order structure. Each term's correction depends on TWO things: the position k (which determines magnitude) and the alternating sign (which determines direction). One thing decaying would give exponential convergence. Two things interacting gives 1/T convergence. That's why Leibniz is slow — it's fundamentally second-order.

The entropy fitness measures information gain: log(1/error) = log(2T+1). On a log-log plot, that's a straight line with constant slope. That's the integrated form of the second-order rate law.

**The entropy fitness is literally the integrated second-order rate law applied to convergence.** It's selecting for processes that obey second-order kinetics. Leibniz is the simplest process that does.

### Why entropy fitness works better than GP convergence
- GP convergence asks: "Is error shrinking between checkpoints?" — first-order question. Many things shrink.
- Entropy asks: "Is 1/error growing linearly?" — second-order question. Unique answer.
- The second-order question is more selective because fewer processes satisfy it.

### Thermodynamic framing
The entropy fitness measures the free energy of the system — how much "order" (precision about π/4) has been extracted from "disorder" (uncertainty). The 3.32 bits/decade is a constant rate of entropy reduction. A steady-state dissipation rate.

Systems that minimize free energy at a constant rate are at steady-state far from equilibrium. Not at equilibrium (that would be π/4 exactly, which Leibniz never reaches). Constantly dissipating — each term reduces uncertainty at a steady rate, forever.

### Efficiency framing (unexplored)
The most fundamental fitness might be: minimum work (operations) per unit of uncertainty reduced. Operations per bit. Leibniz uses 3 operations per term and gains 3.32 bits per decade. An 11-node bloated equivalent uses 5 operations per term for the same 3.32 bits. An efficiency fitness would naturally prefer the canonical 9-node form AND would be more physically grounded.

This was discussed but not implemented as an experiment.

### Gradient / vector space approach (explored, failed)
Attempted to use the gradient across fitness components as a selection criterion — minimize gradient magnitude (closest to balanced steady state). Three approaches tested on 15 terminals: pure gradient magnitude, hybrid scalar × uniformity, min-component bottleneck. All failed (0/5). The failure confirmed the diagnosis: it's a coverage problem, not a fitness problem. Even theoretically superior fitness functions can't compensate for insufficient search coverage.

---

## Preprint Paper Outline (Draft)

### Working Title
"Reverse Engineering Leibniz: Evolutionary Discovery of π/4 Series from Arithmetic Primitives"

### Sections
1. **Introduction** — Leibniz series, why it's special, what "rediscovery" means
2. **Background** — GP, symbolic regression, information-theoretic fitness, prior work on formula discovery
3. **The Mechanism** — How GP builds formulas from primitives. The parts bin, breeding, selection. Concrete examples. This is the "Recipe for PI-saster" section from the article draft.
4. **Two Fitness Functions** — Convergence-aware (first-order) and information-theoretic (second-order). Mathematical definitions. The slime mold and entropy framings.
5. **Experimental Design** — Terminal sets, injection confound, v3 clean protocol, seed values, time budgets
6. **Results** — The full progression from v2 through v3. Discovery rates, scaling, wrong-limit attractors, parameter sensitivity, fitness modifications.
7. **The Scaling Boundary** — Terminal count vs discovery rate. The phase transition. Why finite evaluation windows create wrong-limit attractors.
8. **Discussion** — Second-order kinetics connection. Thermodynamic interpretation. "Leibniz is inevitable" vs "Leibniz is discoverable under constraints."
9. **Conclusion** — What the fitness function defines vs what the search can find. The question is harder than the answer.

### Figures needed
- Discovery rate vs terminal count (need more data points: 6, 8, 10, 12 terminals)
- GP parameter sensitivity heatmap
- Error comparison table (Leibniz vs discovered expressions)
- Information profile plot (bits vs T on log scale, 3.32 bits/decade line)
- Wrong-limit attractor examples (what the algorithm finds when it fails)

---

## Open Questions / Potential Experiments

### Terminal count scaling curve
Run entropy at pop=1000 with 4, 6, 8, 10, 12, 15, 20 terminals to map the phase transition. This produces a figure for the paper.

### Population × terminal count grid
For a few terminal counts (4, 10, 15), sweep population (1000, 2000, 5000) to characterize the coverage relationship.

### Efficiency fitness
Test bits-per-operation as a fitness function. Would naturally prefer canonical 9-node form over bloated equivalents. Not yet implemented.
