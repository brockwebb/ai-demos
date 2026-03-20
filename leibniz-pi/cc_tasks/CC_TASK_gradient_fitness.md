# Claude Code Task: Gradient-Based Fitness — Thermodynamic Selection

## The Idea
Instead of scoring candidates by a weighted sum of fitness components (total_info, monotonicity, mean_rate, parsimony), score them by the **uniformity of their gradient across all fitness dimensions**. 

The principle: a candidate at thermodynamic steady state has a gradient that is small and uniform across all dimensions. No single dimension is doing all the work. Wrong-limit attractors have asymmetric gradients — they score high on some dimensions and flat on others. Leibniz has a balanced gradient — it improves uniformly across all criteria.

The selection criterion becomes: **minimize gradient magnitude** (closest to balanced steady state), not **maximize fitness sum**.

## Background — Why This Might Work
The 15-terminal entropy experiment (Level 1) failed 0/5 because wrong-limit attractors like `5/((6+4k)(k-2))` scored BETTER than Leibniz on the scalar fitness. That formula had ti=15.93, mo=1.00, rate=4.31 — beating Leibniz on every individual metric. But it converges to the wrong limit. Its fitness profile is asymmetric: high info, high monotonicity, but only because it's converging fast to the wrong place.

Leibniz converges SLOWER but MORE UNIFORMLY. Its gradient across fitness dimensions is balanced. The hypothesis: selecting for gradient uniformity will prefer Leibniz over wrong-limit attractors because Leibniz is the formula closest to steady-state across all dimensions simultaneously.

## Implementation

### Step 1: Define the fitness component vector
For each candidate, compute a vector of normalized fitness components:

```python
components = [
    total_info / INFO_CAP,        # normalized information (0-1)
    monotonicity,                  # already 0-1
    mean_rate / RATE_CAP,          # normalized rate (0-1, pick a reasonable cap like 5.0)
    1.0 - (node_count / MAX_NODES) # parsimony as efficiency (1=minimal, 0=bloated)
]
```

### Step 2: Compute the gradient via perturbation
For each candidate tree, generate N small perturbations (mutants). For each mutant, compute the same component vector. The gradient is estimated as the mean direction of fitness change across perturbations.

Specifically:
```python
# For candidate with component vector V:
gradients = []
for _ in range(N_PERTURBATIONS):  # try 5-10 perturbations
    mutant = mutate(candidate.copy())
    mutant_components = compute_components(mutant)
    delta = mutant_components - V
    gradients.append(delta)

# Mean gradient vector
mean_gradient = np.mean(gradients, axis=0)

# Gradient magnitude (L2 norm) — LOWER is better (closer to steady state)
gradient_magnitude = np.linalg.norm(mean_gradient)

# Gradient uniformity — how balanced the gradient is across dimensions
# Use coefficient of variation of absolute gradient components
# LOWER is better (more uniform)
gradient_cv = np.std(np.abs(mean_gradient)) / (np.mean(np.abs(mean_gradient)) + 1e-10)
```

### Step 3: Fitness function
Two approaches to test — try both:

**Approach A: Pure gradient magnitude (minimize)**
```python
# Negate because GP maximizes fitness
fitness = -gradient_magnitude - LAMBDA_P * node_count
```
Problem: this might select for formulas that are in a flat region of fitness space (local minima) rather than the true steady state. May need a floor — only consider candidates that have minimum baseline fitness.

**Approach B: Hybrid — scalar fitness weighted by gradient uniformity**
```python
base_fitness = (W1 * total_info/INFO_CAP + W2 * monotonicity + 
                W3 * mean_rate/RATE_CAP - LAMBDA_P * node_count)
uniformity_bonus = 1.0 / (1.0 + gradient_cv)  # 1.0 when perfectly uniform, → 0 when asymmetric
fitness = base_fitness * uniformity_bonus
```
This keeps the original fitness as a baseline but scales it by how uniform the gradient is. A wrong-limit attractor with high base fitness but asymmetric gradient gets penalized. Leibniz with moderate base fitness but uniform gradient gets boosted.

**Approach C: Minimum component (bottleneck) for comparison baseline**
```python
fitness = min(total_info/INFO_CAP, monotonicity, mean_rate/RATE_CAP, 
              1.0 - node_count/MAX_NODES)
```
This is the simple bottleneck approach. Include it as a comparison point — if the gradient approach doesn't beat this, we know the geometry doesn't matter and the bottleneck was sufficient.

## Test Configuration
- Terminal set: TERM_FIXED=["k", 1, -1, 2], EPHEMERALS=list(range(-5,6)) — the 15-terminal config that failed 0/5
- Population: 1000 (same as before, don't increase — we want to know if the FITNESS change helps, not the population change)
- No injection
- MAX_SEED = 360s
- 5 seeds, same seed values (42, 7, 137, 2718, 31415)
- N_PERTURBATIONS = 5 per candidate (balance between accuracy and compute cost — this will slow each generation, keep it reasonable)

### Run all three approaches:
1. Approach A: Pure gradient magnitude
2. Approach B: Hybrid scalar × uniformity
3. Approach C: Min-component bottleneck (comparison baseline)

### Also run for reference:
4. Original entropy fitness with pop=2000, 15 terminals (to confirm whether coverage alone fixes it)

## Practical Concerns
- The gradient computation via perturbation adds ~5x overhead per candidate evaluation. With pop=1000 and 5 perturbations, that's 5000 extra evaluations per generation. Monitor generation time — if it's too slow (>1s/gen), reduce N_PERTURBATIONS to 3.
- The perturbation should use the SAME mutation operator the GP already uses. Don't invent a special perturbation — use the existing mutate() function. That way the gradient measures change along the directions the GP actually explores.
- Cache management: the existing fitness cache won't help with perturbations since each mutant is unique. Consider disabling or limiting the cache for perturbations.

## Output
Create `entropy-leibniz-v3/gradient_fitness_results.md` with:

| Approach | Seeds Found | Best Expression | Gradient Mag (Leibniz) | Gradient Mag (Best Wrong-Limit) | Notes |
|---|---|---|---|---|---|
| Original (baseline, 0/5) | 0/5 | 5/((6+4k)(k-2)) | — | — | from stress test |
| A: Pure gradient | ?/5 | ... | ... | ... | ... |
| B: Hybrid | ?/5 | ... | ... | ... | ... |
| C: Min-component | ?/5 | ... | ... | ... | ... |
| Pop=2000 original | ?/5 | ... | — | — | coverage control |

### Key diagnostic to include:
For each approach, compute and report the gradient magnitude and gradient CV for:
1. The Leibniz formula (use make_leibniz_tree for reference)
2. The best wrong-limit attractor found
3. The zero expression (degenerate baseline)

This tells us whether the gradient-based fitness CORRECTLY ranks Leibniz above wrong-limit attractors in principle, independent of whether the search finds it.

## What Success Looks Like
- Approach B hits 3/5 or better on 15 terminals at pop=1000
- The gradient magnitude for Leibniz is lower than for wrong-limit attractors (confirming the steady-state hypothesis)
- The gradient is more uniform for Leibniz than for wrong-limit attractors (confirming the thermodynamic selection principle)

If Approach B works: we have evidence that thermodynamic selection (gradient uniformity) is a more fundamental fitness principle than scalar optimization. The article gets a physics-grounded explanation for why entropy fitness works.

If none work but pop=2000 does: the coverage explanation holds and the gradient approach is theoretically interesting but practically unnecessary. Still worth reporting.

If nothing works: we've exhausted this line and should report the minimal-terminal result (5/5 at 4 terminals) as the clean finding and move on to writing the article.
