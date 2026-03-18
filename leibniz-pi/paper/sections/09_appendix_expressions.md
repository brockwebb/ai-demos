# Appendix A: Expression Catalog

This appendix documents all Leibniz-equivalent expressions discovered across 52 experiment files,
alongside the most notable wrong-limit attractors. The full machine-readable catalog is in
`paper/expression_catalog.json` (260 records; 52 Leibniz-equivalent, 179 wrong-limit attractors,
29 trivial).

## A.1 Leibniz-Equivalent Expressions

All 52 expressions below verified equivalent to (-1)^k / (2k+1) at k=100,000 with zero divergence.
Sympy simplification confirms every raw form reduces to -1/(2*k+1), which equals (-1)^k/(2k+1)
up to the sign convention absorbed into the alternating factor.
The canonical 9-node form appears in 42 of 52 cases; remaining 10 cases carry one extra negation node.

| Seed | Raw Form | Nodes | Fitness | Fitness Function | t | Pop | Experiment |
|------|----------|-------|---------|-----------------|---|-----|------------|
| 42 | `((-(-1 ^ k)) / ((-k) - (k - -1)))` | 9 | 0.01102 | log-precision | 4 | 1000 | scaling\_heatmap\_t4\_p1000 |
| 7 | `((-(-1 ^ k)) / ((-1 - k) - k))` | 10 | 0.01602 | log-precision | 4 | 1000 | scaling\_heatmap\_t4\_p1000 |
| 137 | `((-(-1 ^ k)) / ((-1 - k) - k))` | 10 | 0.01602 | log-precision | 4 | 1000 | scaling\_heatmap\_t4\_p1000 |
| 2718 | `((-1 ^ k) / (k + (1 + k)))` | 9 | 0.02102 | log-precision | 4 | 1000 | scaling\_heatmap\_t4\_p1000 |
| 31415 | `((-1 ^ k) / ((k * 2) - -1))` | 9 | 0.02102 | log-precision | 4 | 1000 | scaling\_heatmap\_t4\_p1000 |
| 42 | `((-1 ^ k) / (k + (k - -1)))` | 9 | 0.02102 | log-precision | 4 | 2000 | scaling\_heatmap\_t4\_p2000 |
| 7 | `((-1 ^ k) / (1 + (k * 2)))` | 9 | 0.02102 | log-precision | 4 | 2000 | scaling\_heatmap\_t4\_p2000 |
| 137 | `((-1 ^ k) / ((k - -1) + k))` | 9 | 0.02102 | log-precision | 4 | 2000 | scaling\_heatmap\_t4\_p2000 |
| 2718 | `(((1 + (k + k)) * (-1 ^ k)) ^ -1)` | 11 | 0.01102 | log-precision | 4 | 2000 | scaling\_heatmap\_t4\_p2000 |
| 42 | `((-1 ^ k) / (k - (-1 - k)))` | 9 | -0.00130 | convergence-aware | 4 | 5000 | gp\_scaling\_t4\_p5000 |
| 7 | `((-1 ^ k) / (k - (-1 - k)))` | 9 | -0.00130 | convergence-aware | 4 | 5000 | gp\_scaling\_t4\_p5000 |
| 137 | `((-1 ^ k) / ((k * 2) - -1))` | 9 | -0.00130 | convergence-aware | 4 | 5000 | gp\_scaling\_t4\_p5000 |
| 31415 | `((-1 ^ k) / (1 + (k + k)))` | 9 | -0.00130 | convergence-aware | 4 | 5000 | gp\_scaling\_t4\_p5000 |
| 42 | `((-1 ^ k) / ((2 * k) + 1))` | 9 | 0.02102 | log-precision | 4 | 5000 | scaling\_heatmap\_t4\_p5000 |
| 7 | `((-1 ^ k) / ((k * 2) - -1))` | 9 | 0.02102 | log-precision | 4 | 5000 | scaling\_heatmap\_t4\_p5000 |
| 137 | `((-1 ^ k) / ((k * 2) + 1))` | 9 | 0.02102 | log-precision | 4 | 5000 | scaling\_heatmap\_t4\_p5000 |
| 2718 | `((-1 ^ k) / (k - (-1 - k)))` | 9 | 0.02102 | log-precision | 4 | 5000 | scaling\_heatmap\_t4\_p5000 |
| 31415 | `((-1 ^ k) / (k - (-1 - k)))` | 9 | 0.02102 | log-precision | 4 | 5000 | scaling\_heatmap\_t4\_p5000 |
| 42 | `((-1 ^ k) / (k + (1 + k)))` | 9 | -0.00130 | convergence-aware | 4 | 10000 | gp\_scaling\_t4\_p10000 |
| 7 | `((-1 ^ k) / ((k + k) - -1))` | 9 | -0.00130 | convergence-aware | 4 | 10000 | gp\_scaling\_t4\_p10000 |
| 137 | `((-1 ^ k) / ((2 * k) - -1))` | 9 | -0.00130 | convergence-aware | 4 | 10000 | gp\_scaling\_t4\_p10000 |
| 2718 | `((-1 ^ k) / ((k + 1) + k))` | 9 | -0.00130 | convergence-aware | 4 | 10000 | gp\_scaling\_t4\_p10000 |
| 31415 | `((-1 ^ k) / ((2 * k) - -1))` | 9 | -0.00130 | convergence-aware | 4 | 10000 | gp\_scaling\_t4\_p10000 |
| 42 | `((-1 ^ k) / (1 + (2 * k)))` | 9 | 0.02102 | log-precision | 4 | 10000 | scaling\_heatmap\_t4\_p10000 |
| 7 | `((-1 ^ k) / ((2 * k) - -1))` | 9 | 0.02102 | log-precision | 4 | 10000 | scaling\_heatmap\_t4\_p10000 |
| 137 | `((-1 ^ k) / (1 + (k * 2)))` | 9 | 0.02102 | log-precision | 4 | 10000 | scaling\_heatmap\_t4\_p10000 |
| 2718 | `((-(-1 ^ k)) / (-1 - (k + k)))` | 10 | 0.01602 | log-precision | 4 | 10000 | scaling\_heatmap\_t4\_p10000 |
| 31415 | `(-((-1 ^ k) / (-1 - (k + k))))` | 10 | 0.01602 | log-precision | 4 | 10000 | scaling\_heatmap\_t4\_p10000 |
| 137 | `((-1 ^ k) / (k - (-1 - k)))` | 9 | 0.02102 | log-precision | 6 | 1000 | scaling\_heatmap\_t6\_p1000 |
| 42 | `((-1 ^ k) / (k + (k + 1)))` | 9 | 0.02102 | log-precision | 6 | 2000 | scaling\_heatmap\_t6\_p2000 |
| 137 | `((-1 ^ k) / (1 + (k * 2)))` | 9 | 0.02102 | log-precision | 6 | 2000 | scaling\_heatmap\_t6\_p2000 |
| 137 | `((-(-1 ^ k)) / (-1 - (k * 2)))` | 10 | 0.01602 | log-precision | 6 | 5000 | scaling\_heatmap\_t6\_p5000 |
| 2718 | `((-1 ^ k) / ((k + 1) + k))` | 9 | -0.00130 | convergence-aware | 6 | 5000 | gp\_scaling\_t6\_p5000 |
| 7 | `((-1 ^ k) / (1 - (k * -2)))` | 9 | -0.00130 | convergence-aware | 6 | 10000 | gp\_scaling\_t6\_p10000 |
| 137 | `((-1 ^ k) / ((k + k) + 1))` | 9 | -0.00130 | convergence-aware | 6 | 10000 | gp\_scaling\_t6\_p10000 |
| 2718 | `((-1 ^ k) / (k + (k + 1)))` | 9 | -0.00130 | convergence-aware | 6 | 10000 | gp\_scaling\_t6\_p10000 |
| 31415 | `((-1 ^ k) / ((k - -1) + k))` | 9 | -0.00130 | convergence-aware | 6 | 10000 | gp\_scaling\_t6\_p10000 |
| 31415 | `((-1 ^ k) / ((2 * k) - -1))` | 9 | 0.02102 | log-precision | 6 | 10000 | scaling\_heatmap\_t6\_p10000 |
| 7 | `((-1 ^ k) / (k - (-(1 + k))))` | 10 | 0.01602 | log-precision | 8 | 1000 | scaling\_heatmap\_t8\_p1000 |
| 7 | `((-1 ^ k) / (k + (k + 1)))` | 9 | 0.02102 | log-precision | 8 | 2000 | scaling\_heatmap\_t8\_p2000 |
| 2718 | `((-1 ^ k) / (-(-1 - (k + k))))` | 10 | 0.01602 | log-precision | 8 | 5000 | scaling\_heatmap\_t8\_p5000 |
| 7 | `((-1 ^ k) / ((1 + k) + k))` | 9 | -0.00130 | convergence-aware | 10 | 5000 | gp\_extended\_t10\_p5000 |
| 7 | `((-1 ^ k) / ((1 + k) + k))` | 9 | -0.00130 | convergence-aware | 10 | 5000 | gp\_scaling\_t10\_p5000 |
| 137 | `((-1 ^ k) / (k + (k + 1)))` | 9 | -0.00130 | convergence-aware | 15 | 5000 | gp\_scaling\_t15\_p5000 |
| 137 | `((-1 ^ k) / (1 + (k * 2)))` | 9 | 0.02102 | log-precision | 15 | 10000 | scaling\_heatmap\_t15\_p10000 |
| 2718 | `((-1 ^ k) / (1 + (k * 2)))` | 9 | 0.02102 | log-precision | 15 | 10000 | scaling\_heatmap\_t15\_p10000 |
| 42 | `((-1 ^ k) / ((2 * k) + 1))` | 9 | 0.02102 | log-precision | ~42 | 1000 | entropy\_v1\_wide |
| 7 | `((-1 ^ k) / ((2 * k) + 1))` | 9 | 0.02102 | log-precision | ~42 | 1000 | entropy\_v1\_wide |
| 137 | `((-1 ^ k) / ((2 * k) + 1))` | 9 | 0.02102 | log-precision | ~42 | 1000 | entropy\_v1\_wide |
| 2718 | `((-1 ^ k) / ((2 * k) + 1))` | 9 | 0.02102 | log-precision | ~42 | 1000 | entropy\_v1\_wide |
| 31415 | `((-1 ^ k) / ((2 * k) + 1))` | 9 | 0.02102 | log-precision | ~42 | 1000 | entropy\_v1\_wide |
| 137 | `(-1 / (((-1 - k) - k) / (-1 ^ k)))` | 11 | 0.01102 | log-precision | ~4 | 1000 | fitness\_approach2\_w0.1 |

Note: entropy\_v1\_wide (v2-era experiment) used a 42-terminal set and injected Leibniz at generation 0.
Results are valid as "recognition" tests but not as discovery tests. See Section 4 for the injection confound.
The fitness\_approach2\_w0.1 experiment used the minimal terminal set with a modified log-precision weight.

## A.2 Notable Wrong-Limit Attractors

The table shows the 10 highest-fitness wrong-limit attractors plus the canonical `5/((6+4k)(k-2))`
attractor from the stress test. Section A.2.1 discusses the canonical attractor in detail.

| Seed | Raw Form | Nodes | Fitness | t | Experiment | Notes |
|------|----------|-------|---------|---|------------|-------|
| 31415 | `(-3 / ((7 + k) * (k + -3)))` | 9 | 0.0232 | 15 | scaling\_heatmap\_t15\_p2000 | Partial fraction near pi/4 |
| 7 | `(((-1 / (k ^ 10)) ^ k) * (7 ^ 7))` | 11 | 0.0230 | 20 | scaling\_heatmap\_t20\_p1000 | Decaying oscillation times constant |
| 31415 | `((7 ^ 7) * ((-(k ^ 10)) ^ (-k)))` | 9 | 0.0230 | 20 | scaling\_heatmap\_t20\_p2000 | Variant of above |
| 42 | `(((k - 4) / -4) ^ -9)` | 7 | 0.0157 | 20 | scaling\_heatmap\_t20\_p10000 | Power-law decay family |
| 7 | `(((k + -4) / -4) ^ -9)` | 7 | 0.0157 | 20 | scaling\_heatmap\_t20\_p10000 | Power-law decay family |
| 31415 | `(((k - 4) / -4) ^ -9)` | 7 | 0.0157 | 20 | scaling\_heatmap\_t20\_p10000 | Power-law decay family |
| 137 | `(((4 - k) / 4) ^ -9)` | 7 | 0.0157 | 20 | scaling\_heatmap\_t20\_p1000 | Power-law decay family |
| 137 | `(((-4 + k) / -4) ^ -9)` | 7 | 0.0157 | 20 | scaling\_heatmap\_t20\_p2000 | Power-law decay family |
| 2718 | `((-4 / (k - 4)) ^ 9)` | 7 | 0.0157 | 20 | scaling\_heatmap\_t20\_p2000 | Power-law decay family |
| 42 | `(((k + -4) / -4) ^ -9)` | 7 | 0.0157 | 20 | scaling\_heatmap\_t20\_p5000 | Power-law decay family |
| 42 | `(5 / (((1 + 5) + (k * 4)) * (k + -2)))` | 13 | 0.0073 | 15 | stress\_L1 | Canonical 5/((6+4k)(k-2)) attractor |

### A.2.1 The 5/((6+4k)(k-2)) Attractor

The expression `5/((6+4k)(k-2))` found by seed 42 in the stress test (15-terminal set) achieves
{{result:wrong_limit_ti_15_93:value}} bits of precision at T=10,000, exceeding Leibniz's
{{result:leibniz_ti_15_29:value}} bits. The 5/((6+4k)(k-2)) expression is the clearest example of
the evaluation horizon trap in the dataset.

The partial sum of this series converges, but to a limit different from pi/4. Within the evaluation horizon (T up to 10,000), the convergence curve is steeper than Leibniz's. The log-precision fitness
assigns it a higher raw information score: {{result:wrong_limit_ti_15_93:value}} bits versus
{{result:leibniz_ti_15_29:value}} bits. The attractor's mean rate is ~4.31 bits/decade versus
{{result:info_rate_3_32:value}} bits/decade for Leibniz. Leibniz wins under the full fitness only
because parsimony penalizes the 13-node attractor against the 9-node Leibniz form.

The narrow margin shows the fitness function correctly ranks Leibniz above the attractor when both
are present. The failure at 15 terminals is a coverage failure, not a fitness landscape failure.
The 15-terminal search space is large enough that strong attractors appear before Leibniz building
blocks assemble.

### A.2.2 Power-Law Decay Family (t=20)

At t=20 with log-precision fitness, the dominant attractor family is `((k-4)/(-4))^-9` and
variants. This expression has 7 nodes and converges monotonically to zero, not pi/4. Within the
evaluation horizon, its partial-sum curve looks like rapid convergence to a small positive constant.
All five seeds at pop=10000 converged to this family. The power-law attractor dominated before
Leibniz building blocks could be assembled in the 20-terminal search space.

## A.3 Expressions by Terminal Count

### A.3.1 t=4 (Minimal Terminal Set)

With four terminals {k, 1, -1, 2}, (-1)^k is the only oscillating structure constructible from
the available primitives. This makes the fitness landscape nearly unimodal: the single basin of
attraction corresponds to Leibniz variants. We found 28 of 30 seeds (93%) discovered
Leibniz-equivalent expressions across the two t=4 population sweeps. Two t=4 seeds from
scaling\_heatmap\_t4\_p2000 failed; the Grandi-Leibniz attractor analysis in the research notes
covers seed 31415's anomalous result.

All 28 successful t=4 expressions simplify to -1/(2k+1) under sympy. Node count is 9 in 21 cases
and 10 or 11 in the remaining 7 cases, reflecting how many negation nodes the GP included in the
final tree.

### A.3.2 t=6

With six terminals, the search space expands but (-1)^k remains the easiest oscillating structure.
We found 10 of 30 seeds (33%) discovered Leibniz across the t=6 population and fitness-function
sweep. Log-precision fitness found Leibniz at pop=1000 (1 seed) and pop=2000 (2 seeds). Both
fitness functions succeeded at pop=10000: 4 seeds convergence-aware, 1 seed log-precision, plus
1 seed log-precision at pop=5000. The remaining 20 seeds converged to wrong-limit attractors.
The dominant family was rational expressions with a pole near k=0 or small constants.

### A.3.3 t=8

Only 3 of 30 seeds (10%) discovered Leibniz at t=8, all from the log-precision fitness. The
dominant wrong-limit attractor at t=8 is `((4-((4--3)^-2) - k/(-3))^-2)` and its variants,
appearing in 8 of 30 seeds. This attractor achieves ~20.66 bits of precision at T=10,000, roughly
5 bits better than Leibniz's {{result:leibniz_ti_15_29:value}} bits at the same horizon. At
pop=10000, 0/5 seeds found Leibniz while smaller populations each found 1/5. Larger populations
find strong attractors faster, which illustrates the population inversion effect.

### A.3.4 t>=10 (Failure Regime)

We found 5 Leibniz-equivalent expressions at t>=10, all anomalous. Two appeared at t=10 with
convergence-aware fitness (same seed 7 in two overlapping experiments). One appeared at t=15 with
convergence-aware fitness (seed 137, pop=5000). Two appeared at t=15 with log-precision fitness
(seeds 137 and 2718, pop=10000). No expressions were found at t=12 or t=20.

The t=10 and t=15 discoveries are consistent with lucky initializations rather than systematic
search. At t=10, seed 7 appears twice because `gp_extended_t10_p5000` and `gp_scaling_t10_p5000`
ran the same seed with the same engine. Both found `((-1 ^ k) / ((1 + k) + k))`.
The t=15/p=10000 result (2/5 seeds) is discussed in Section 5.

## A.4 Trivial and Parsimony-Collapsed Expressions

Several experimental conditions produced trivial expressions: either the constant zero or
small numerical constants with no k dependence. These appeared primarily in three contexts.

The fitness\_approach1 and fitness\_approach4 experiments each produced zero (0) as the
best expression for all five seeds. Approach B (gradient uniformity bonus) amplified the
zero constant because a constant expression achieves near-perfect uniformity under mutation,
trivially satisfying the gradient-uniformity objective. Approach D (gradient magnitude negated)
similarly found the flattest point in the fitness landscape.

The stress\_L1 file (15-terminal set, single stress level) produced zero in two of five seeds,
the canonical 5/((6+4k)(k-2)) attractor in one seed, and small rational constants in the
remaining two seeds. None found Leibniz. The 15-terminal failure persists across fitness
formulations tested here, confirming it is not specific to the original log-precision fitness.

| Seed | Raw Form | Nodes | Fitness | t | Experiment |
|------|----------|-------|---------|---|------------|
| 42 | `0` | 1 | -0.00486 | n/a | fitness\_approach1 |
| 7 | `0` | 1 | -0.00486 | n/a | fitness\_approach1 |
| 137 | `0` | 1 | -0.00486 | n/a | fitness\_approach1 |
| 2718 | `0` | 1 | -0.00486 | n/a | fitness\_approach1 |
| 31415 | `0` | 1 | -0.00486 | n/a | fitness\_approach1 |
| 42 | `0` | 1 | -0.00486 | n/a | fitness\_approach4 |
| 7 | `0` | 1 | -0.00486 | n/a | fitness\_approach4 |
| 137 | `0` | 1 | -0.00486 | n/a | fitness\_approach4 |
| 2718 | `0` | 1 | -0.00486 | n/a | fitness\_approach4 |
| 31415 | `0` | 1 | -0.00486 | n/a | fitness\_approach4 |
| 7 | `0` | 1 | -0.00486 | 15 | stress\_L1 |
| 31415 | `0` | 1 | -0.00486 | 15 | stress\_L1 |
| 137 | `((-5 ^ -5) / -4)` | 5 | -0.00411 | 15 | stress\_L1 |
| 7 | `((-5 ^ -5) / -4)` | 5 | -0.00558 | n/a | fitness\_approach2\_w0.1 |
| 2718 | `(4 / ((3 * -5) ^ 4))` | 7 | -0.01098 | n/a | fitness\_approach2\_w0.1 |
