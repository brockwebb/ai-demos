# Claude Code Task: Entropy Fitness Sensitivity Analysis — Fix the Wrong-Limit Problem

## Context
Entropy fitness finds Leibniz 5/5 with 4 terminals {k, 1, -1, 2} but 0/5 with 15 terminals {k, 1, -1, 2} + [-5..5]. The failure mode: rational functions like `5/((6+4k)(k-2))` that converge to a value NEAR π/4 but not TO π/4. Seed 0 scored ti=15.93, mo=1.00, rate=4.31 — BETTER than Leibniz on fitness metrics — while converging to the wrong limit.

The fitness function knows π/4 (it's the target). But it only measures error at finite checkpoints (T=5 through T=10000). A formula whose partial sums pass near π/4 at those checkpoints can score well even if its actual limit is wrong.

## The Goal
Find a fitness modification that lets entropy discover Leibniz from 15 terminals. Use the Level 1 config (TERM_FIXED=["k",1,-1,2], EPHEMERALS=list(range(-5,6))) as the test bed. This is the config that failed 0/5. If a modification gets it to 3/5 or better, that's a win.

## Approaches to Test

Run each as a separate configuration, 5 seeds, same seed values (42, 7, 137, 2718, 31415). MAX_SEED=360s. Start from `entropy-leibniz-v3/entropy_stress_test.py` or `entropy_leibniz_v3_minimal.py`, whichever is cleaner to modify.

### Approach 1: Push checkpoints further out
Add T=20000 and T=50000 to the checkpoint list. Wrong-limit attractors that look good at T=10000 should be exposed at T=50000 because their error stops shrinking (they've reached their wrong limit). The current T_CHECKPOINTS likely stops at 10000. Push it out.

Note: this means evaluating more terms per candidate. May slow each generation. That's fine — we're testing whether the approach works, not optimizing speed.

### Approach 2: Heavy penalty on large-T error
Add an explicit term to the fitness that heavily penalizes the absolute error at the LARGEST checkpoint. Something like:

```python
# After computing existing fitness components:
largest_T_error = errors[-1]  # error at the last (largest) checkpoint
limit_penalty = -0.1 * largest_T_error  # or some weight
fitness += limit_penalty
```

This directly uses π/4 knowledge: "your partial sum at T=50000 should be VERY close to π/4, not just closer than it was at T=10000." Tune the weight — try 0.05, 0.1, 0.5.

### Approach 3: Extrapolation check
Fit a simple model to the errors at checkpoints and estimate the projected limit. If the projected limit isn't within some tolerance of π/4, penalize. This is fancier but may be overkill — try approaches 1 and 2 first.

### Approach 4: Rate consistency across scales
The current rate metric averages across all checkpoint pairs. Instead, check that the rate is consistent: the bits gained from T=100→1000 should be similar to bits gained from T=1000→10000. Wrong-limit attractors have high early rate that collapses later. Leibniz has constant rate. Penalize rate variance.

## Implementation
- Create a new script or parameterize the existing stress test script
- For each approach, change ONLY the fitness function (and checkpoint list for Approach 1)
- Do NOT change terminals, population size, GP parameters, or anything else
- Label output files clearly by approach

## Priority Order
1. Approach 1 (push checkpoints) — simplest change
2. Approach 2 (large-T penalty) — next simplest
3. Approach 4 (rate consistency) — if 1 and 2 don't work
4. Approach 3 (extrapolation) — last resort

Stop if any approach hits 3/5 or better. That proves the concept. Then run that winning approach on the harder terminal sets (wide, hostile, extreme) to see how far it scales.

## Output
Create `entropy-leibniz-v3/fitness_sensitivity_results.md` with:

| Approach | Config | Seeds Found | Best Wrong-Limit Score | Leibniz Score | Notes |
|---|---|---|---|---|---|
| baseline (L1 failure) | T up to 10000 | 0/5 | 15.93 (Seed 0) | — | wrong limits outscore |
| 1: extended checkpoints | T up to 50000 | ?/5 | ... | ... | ... |
| 2: large-T penalty (w=0.1) | ... | ?/5 | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

## Key Metric
The winning approach should make Leibniz score HIGHER than the wrong-limit attractors. Currently wrong-limit attractors outscore Leibniz — that's the core problem. The fix should invert that ranking.
