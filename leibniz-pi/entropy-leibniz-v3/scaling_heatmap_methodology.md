# Scaling Heat Map Experiment — Methodology

**Experiment:** Terminals × Population → Discovery Rate  
**Date:** 2026-03-15  
**Repo:** `ai-demos/leibniz-pi`  
**Script:** `entropy-leibniz-v3/scaling_heatmap.py`  
**Config:** `entropy-leibniz-v3/config/scaling_heatmap_config.json`  

---

## Objective

Characterize the phase transition boundary between "Leibniz discoverable" and "Leibniz not discoverable" as a function of terminal set size and GP population size. This produces a 2D heat map that becomes a key figure in the preprint.

## Hypothesis

Discovery rate degrades as terminal count increases (larger search space) and improves as population size increases (better coverage). There exists a phase boundary separating the discoverable region from the non-discoverable region. The boundary's shape characterizes the relationship between search space size and coverage requirements.

## Prior Results Informing Design

| Experiment | Terminals | Pop | Result | Source |
|---|---|---|---|---|
| Entropy v3 minimal | 4 | 1000 | 5/5 | entropy_leibniz_v3_minimal.py |
| Entropy stress L1 | 15 | 1000 | 0/5 | entropy_stress_test.py |
| GP v3 pop=2000 | 4 | 2000 | 5/5 | gp_sensitivity_sweep.py |
| Entropy v3 wide | 42 | 1000 | 0/5 | entropy_leibniz_v3_wide.py |

The phase transition lies somewhere between 4 and 15 terminals at pop=1000. Higher populations may shift the boundary.

---

## Experimental Design

### Independent Variables

**Terminal count (7 levels):** 4, 6, 8, 10, 12, 15, 20

**Population size (3 levels):** 1000, 2000, 5000

**Total grid:** 7 × 3 = 21 cells. Two cells use prior results (t=4/p=1000, t=15/p=1000), so 19 cells are run.

### Dependent Variable

**Discovery rate:** number of seeds (out of 5) that find a Leibniz-equivalent expression. An expression is "Leibniz-equivalent" if its first 20 terms match the Leibniz series `(-1)^k / (2k+1)` to within 1e-6 absolute error per term.

### Terminal Set Construction (Option A — Expanding)

At each terminal count N, the set is constructed as:

1. **Fixed base (always present):** `{k, 1, -1, 2}` — guarantees Leibniz is constructible from the available primitives
2. **Expansion:** integers added in the pattern 3, -2, 4, -3, 5, -4, 6, -5, ... (alternating positive then negative, expanding outward from the base set)
3. **No 0** — multiplying by 0 kills subtrees, creating degenerate search dynamics
4. **No duplicates** of base terminals

Exact terminal sets:

| N | Terminal Set |
|---|---|
| 4 | {k, 1, -1, 2} |
| 6 | {k, 1, -1, 2, 3, -2} |
| 8 | {k, 1, -1, 2, 3, -2, 4, -3} |
| 10 | {k, 1, -1, 2, 3, -2, 4, -3, 5, -4} |
| 12 | {k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5} |
| 15 | {k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8} |
| 20 | {k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8, -7, 9, -8, 10, -9} |

**Design rationale:** Option A controls for primitive availability (Leibniz's building blocks {k, 1, -1, 2} are always present), isolating the effect of search space expansion on discovery rate. The expansion pattern avoids bias toward any particular range.

### Seeds

Five seeds per cell: 42, 7, 137, 2718, 31415. These are the same seeds used across all v3 experiments for comparability.

### Time Budgets

- **MAX_SEED:** 1800s (30 min) per seed — extended from the v3 minimal 360s budget to allow adequate search time at higher terminal counts and population sizes
- **MAX_TOTAL:** 10800s (3 hours) per cell — accommodates 5 seeds at 30 min each plus overhead

**Rationale for 30-min seed budget:** The v3 minimal experiment found Leibniz in 21–153s at pop=1000/4 terminals. At pop=5000, generation time is ~5× slower. At higher terminal counts, more generations may be needed. 30 minutes provides a generous ceiling without making the experiment impractically long.

### Parallelism

- **MAX_WORKERS:** 5 concurrent cells (on 8-core machine)
- Implementation: `multiprocessing.Pool(processes=5)` with in-process execution (no subprocesses)
- Cells execute as function calls within pool workers, not as spawned subprocess scripts
- This ensures clean termination when the parent process is killed

### Stop Conditions (per seed)

Each seed terminates for one of three reasons, recorded in results:

1. **`early_stop_converged`** — best individual has info ≥ 13.0 bits at T=10000, is monotone, and has been unchanged for PATIENCE=100 generations. This indicates Leibniz (or equivalent) was found.
2. **`time_limit_seed`** — MAX_SEED elapsed without convergence.
3. **`time_limit_total`** — MAX_TOTAL for the cell elapsed.

**All stop reasons are valid experimental outcomes.** Time-limit stops with a non-Leibniz best individual are "failure to discover" data points, not errors.

---

## Fixed GP Engine Parameters

These are constants from the v3 minimal experiment, unchanged across all cells. They are hardcoded in the script (not in the config file) because they are experimental conditions, not tunable knobs for this experiment.

### GP Hyperparameters

| Parameter | Value | Description |
|---|---|---|
| MAX_DEPTH | 6 | Maximum tree depth during generation |
| MAX_NODES | 30 | Maximum nodes per tree |
| TOURNAMENT_K | 7 | Tournament selection size |
| P_CROSS | 0.70 | Crossover probability |
| P_MUT | 0.20 | Mutation probability |
| N_ELITE | 5 | Elite individuals preserved per generation |
| PATIENCE | 100 | Generations without improvement before early-stop check |
| DIV_INJECT | 100 | Number of random individuals injected on diversity collapse |

### Operators

Binary: add, sub, mul, div, pow  
Unary: neg

**Safe operations:** `div(a, 0) → 1.0`, `pow` overflow → 1.0 (with 1e6 magnitude cap)

### Fitness Function (Log-Precision)

The fitness measures log-scale precision: -log₂(|error|) gives bits of precision about π/4. It does not measure entropy or information in the Shannon sense.

```
precision(T) = -log₂(|partial_sum(T) - π/4|)    (capped at 50 bits)

fitness = W1 × (total_precision / INFO_NORM)
        + W2 × monotonicity
        + W3 × (mean_rate / RATE_NORM)
        - LAMBDA_P × node_count
```

| Weight | Value | Component |
|---|---|---|
| W1 | 0.02 | Total precision at T=10000 (normalized by 50) |
| W2 | 0.04 | Fraction of consecutive checkpoint pairs with ≥0.5 bit gain |
| W3 | 0.03 | Mean precision gain rate in bits/decade (normalized by 5) |
| LAMBDA_P | 0.005 | Parsimony penalty per node |

**T_CHECKPOINTS:** [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]

**K_MAX:** 10000 (evaluation window for partial sums)

### Initialization

Ramped half-and-half (depths 2–5). No injection of Leibniz or any known solution. Pure random initialization.

### Diversity Mechanism

When the top 20 individuals have identical fitness (rounded to 6 decimal places), the worst 100 individuals are replaced with fresh random trees.

---

## Equivalence Testing

An expression is "Leibniz-equivalent" if:

```python
leibniz_terms = [(-1)**k / (2*k + 1) for k in range(20)]
agent_terms = [float(evaluate(expression, k)) for k in range(20)]
all(abs(agent_terms[k] - leibniz_terms[k]) < 1e-6 for k in range(20))
```

This catches algebraically equivalent but structurally different expressions (e.g., `(-(-1^k)) / ((-k) - (k - -1))` which simplifies to Leibniz). Prior experiments showed entropy produces bloated equivalents at 9–11 nodes; all verified identical at k=100,000.

---

## Output Files

### Per-cell
- `scaling_heatmap_t{N}_p{P}.txt` — human-readable results with stop reason per seed
- `scaling_heatmap_t{N}_p{P}_data.json` — machine-readable results
- `scaling_heatmap_t{N}_p{P}.log` — full run log (stdout capture)

### Summary
- `scaling_heatmap_results.md` — grid table, phase transition analysis, wrong-limit attractors

### Configuration
- `config/scaling_heatmap_config.json` — experiment parameters

---

## Known Limitations

1. **Evaluation window finite:** Fitness evaluated at T ≤ 10000. Expressions converging to values near π/4 (but not equal) can score well within this window. This is the "wrong-limit attractor" problem documented in stress test results.

2. **Terminal set includes Leibniz primitives at all levels:** By design (Option A), {k, 1, -1, 2} are always present. This means Leibniz is always constructible. The experiment measures whether it's *findable*, not whether it's *constructible*.

3. **Single fitness function:** Only log-precision fitness is tested. GP convergence fitness was shown to work at pop=2000/4 terminals but is not included in this grid. This is a deliberate scope decision — log-precision fitness is the primary result for the preprint.

4. **No replication beyond 5 seeds:** Statistical power is limited. 5/5 vs 0/5 is clear; 2/5 vs 3/5 is not distinguishable from noise. The heat map should be interpreted as approximate boundary characterization, not precise rate estimation.

5. **Parallelism affects timing:** With 5 concurrent cells sharing CPU, per-generation wall-clock time may be inflated compared to single-process runs. Discovery rates (found/not found) are unaffected, but elapsed times and generation counts are not directly comparable to the single-process v3 minimal baseline.
