# Entropy-Leibniz v3 — Stress Test Results
## Progressive Terminal Set Difficulty

**Date:** 2026-03-14
**Script:** `entropy_stress_test.py`
**Baseline reference:** `entropy_leibniz_v3_minimal.py` (seeds 42, 7, 137, 2718, 31415; 5/5 Leibniz found)

---

## Summary Table

| Level | Terminal config | Total terms | Seeds Found | Fastest | Slowest | Notes |
|---|---|---|---|---|---|---|
| baseline (minimal) | {k, 1, -1, 2} | 4 | 5/5 | 21s/711gen | 153s/6136gen | from v3 minimal |
| 1: moderate | {k,1,-1,2}+[-5..5] | 15 | 0/5 | — | — | see below |
| 2: wide | {k,1}+[-20..20] | 42 | not run | — | — | stopped after L1=0/5 |
| 3: hostile | {k,1,3,-1}+[-20..20\2] | 44 | not run | — | — | stopped after L1=0/5 |
| 4: extreme | {k,1}+[-20..20\{2,-1}] | 41 | not run | — | — | stopped after L1=0/5 |

> Levels 2–4 were not executed because Level 1 returned 0/5, per the stop-on-first-failure protocol.

---

## Level 1 Detail: Moderate (15 terminals)

**Config:** `TERM_FIXED=["k",1,-1,2]`, `EPHEMERALS=list(range(-5,6))` → 15 terminals
**Budget:** 360s/seed, 1800s total, 5 seeds, NO injection

### Per-seed Results

| Seed | Val | Gens | Elapsed | Expression | Equiv | ti | mono | rate | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 42 | 18466 | 360s | `(5 / (((1 + 5) + (k * 4)) * (k + -2)))` | No | 15.93 | 1.00 | 4.31 | Partial-fraction attractor |
| 1 | 7 | 22027 | 360s | `0` | No | 0.35 | 0.00 | 0.00 | Collapsed to zero |
| 2 | 137 | 18973 | 360s | `((-5 ^ -5) / -4)` | No | 6.10 | 0.20 | 1.74 | Constant term (wrong limit) |
| 3 | 2718 | 16727 | 360s | `(-5 / (k * (2 - k)))` | No | 4.80 | 0.50 | 1.63 | Partial-fraction, flatlines |
| 4 | 31415 | 22027 | 360s | `0` | No | 0.35 | 0.00 | 0.00 | Collapsed to zero |

**RESULT: level=1 seeds_found=0/5**

### Info Profiles

**Seed 0 — best performer** `(5 / (((1 + 5) + (k * 4)) * (k + -2)))`
This is equivalent to `5 / ((6 + 4k)(k - 2))` — a rational function of k.
It achieves ti=15.93 bits at T=10000, monotone=1.0, rate=4.31 bits/decade.
This looks almost Leibniz-quality by the fitness metrics, yet is NOT equivalent.

| T | info (bits) | error |
|---|---|---|
| 5 | 1.69 | 0.31065 |
| 10 | 2.87 | 0.13653 |
| 20 | 3.94 | 0.06499 |
| 50 | 5.31 | 0.02528 |
| 100 | 6.32 | 0.01249 |
| 200 | 7.34 | 0.00616 |
| 500 | 8.71 | 0.00239 |
| 1000 | 9.77 | 0.00114 |
| 2000 | 10.92 | 0.00052 |
| 5000 | 12.79 | 0.00014 |
| 10000 | 15.93 | 0.000016 |

**Seed 2** `((-5^-5) / -4)` — constant ≈ 0.000320 per term
Sum at T=10000 ≈ 3.2, far from π/4=0.7854. The "convergence" is spurious: a constant term accumulates, then drifts away slowly. Fits `is_monotone=True` because the error barely changes (the sum keeps growing away from π/4 at a slow constant rate, but at T=10000 happens to land near the target).

**Seed 3** `(-5 / (k * (2 - k)))` — partial-fraction
Converges to a fixed value (flatlines). Achieves ti≈4.8 bits at T=10000 then stops improving. Classic wrong-limit attractor: the series sums to a finite constant, not π/4.

**Seeds 1, 4** — collapsed to the zero expression
All terms = 0, partial sums = 0 for all T. Error stays at π/4 = 0.78539..., giving only 0.35 bits at every checkpoint. Represents total fitness failure (the diversity injector kept firing but couldn't escape).

---

## Findings

### What happened at Level 1

Adding just 11 ephemerals (-5..5) to the baseline terminal set caused complete failure (0/5 vs 5/5 baseline). The failure modes:

1. **Wrong-limit rational attractors** (Seeds 0, 3): The GP found partial-fraction expressions like `5/((6+4k)(k-2))` that genuinely converge — the partial sums decrease monotonically toward some finite limit, earning high monotonicity and total_info scores. Seed 0 reached ti=15.93, mo=1.00, nearly identical to a Leibniz run's metrics, but the limit is NOT π/4. The entropy fitness cannot distinguish "converges fast to wrong value" from "converges fast to right value" if the wrong value happens to be close to π/4 at large T.

2. **Zero collapse** (Seeds 1, 4): The GP converged to the constant 0. Partial sum = 0 for all T, error = π/4 ≈ 0.785 at all checkpoints, yielding only 0.35 bits. This is a global attractor when no better structure is found — a neutral low-energy state.

3. **Constant-term wrong-limit** (Seed 2): The expression `(-5^-5)/-4 ≈ 3.2e-4` is a constant. Summing a constant T times gives T × 3.2e-4, which at T=10000 ≈ 3.2. The error |3.2 - 0.785| is large, so this actually scores poorly (ti=6.10). The monotone flag is misleading; the partial sum is just a steadily growing line.

### Why baseline (4 terminals) succeeds but moderate (15) fails

With only `{k, 1, -1, 2}` the search space is narrow enough that:
- The alternating sign `(-1)^k` is essentially the only way to produce an oscillating series (needs `-1` and `k` in a pow)
- The denominator `2k+1` uses all remaining terminals (`2`, `k`, `1`)
- There are few wrong-limit attractors to get trapped in

With 15 terminals including integers -5..5, the GP gains access to many partial-fraction expressions of the form `c / (ak + b)(ck + d)` that telescope or converge to finite limits. These score well on the entropy fitness (monotone partial sums approaching some limit) while never being Leibniz.

### The core problem: proximity doesn't imply correctness

Seed 0's result `5 / ((6+4k)(k-2))` is the clearest example. Its partial sums approach some finite limit near π/4 by the time T reaches 10000, earning a better fitness score than many seeds in the baseline run. The entropy fitness rewards **how many bits of precision you gain per decade** — but if you start near π/4 and stay near it (because your limit happens to be close), you score well without being Leibniz.

The fundamental attractor in larger terminal sets is the class of rational functions `P(k)/Q(k)` whose series telescope to a value that lands near π/4. These are much more accessible than the alternating sign structure of Leibniz.

### What level entropy can handle

- **4 terminals `{k,1,-1,2}`**: 5/5 success, robust
- **15 terminals `{k,1,-1,2}+[-5..5]`**: 0/5 failure — the search space gain creates far more wrong-limit attractors than useful building blocks
- **Levels 2–4**: not tested, almost certainly fail since Level 1 already collapsed

### What breaks it

The entropy fitness breaks when the terminal set contains enough integer constants that partial-fraction expressions `c/(ak+b)` can be freely constructed. Such expressions:
- Are structurally simpler than Leibniz (fewer nodes → smaller parsimony penalty)
- Can converge monotonically (earning full monotonicity score)
- Can land close to π/4 by coincidence at large T (earning high total_info)

The fitness function has no mechanism to distinguish "converges to π/4" from "converges to something close to π/4." Without injection seeding the population with the correct structure, the GP explores the wrong basin.

---

## Raw Output Reference

| File | Contents |
|---|---|
| `stress_L1_results.txt` | Full per-seed TEVV text report |
| `stress_L1_data.json` | Machine-readable seed data, info profiles, histories |
| `stress_L1_convergence.csv` | Per-generation convergence data for all seeds |
