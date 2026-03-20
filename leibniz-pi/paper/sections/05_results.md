# 5. Results

## 5.1 Discovery Under Minimal Terminals

With the minimal terminal set {k, 1, -1, 2} and no injection, the log-precision fitness achieves {{result:logprec_minimal_5_5:value}}/5 discovery across five seeds. The convergence-aware fitness achieves {{result:gp_minimal_2_5:value}}/5 at population 1,000 and {{result:gp_pop2000_5_5:value}}/5 at population 2,000. Total runtime for the complete log-precision run across all five seeds was {{result:logprec_minimal_runtime:value}} seconds.

| Fitness | Pop | Seeds Found | Mean Generations |
|---|---|---|---|
| Log-precision | 1,000 | {{result:logprec_minimal_5_5:value}}/5 | {{result:logprec_minimal_mean_gen:value}} |
| Convergence-aware | 1,000 | {{result:gp_minimal_2_5:value}}/5 | n/a |
| Convergence-aware | 2,000 | {{result:gp_pop2000_5_5:value}}/5 | n/a |

All discovered expressions are algebraically equivalent to (-1)^k / (2k+1), verified identical at k=100,000 with zero divergence. The structural variants that appear across seeds are shown below.

| Seed | Expression | Nodes | Notes |
|---|---|---|---|
| 42 | (-(-1^k)) / ((-k) - (k - -1)) | 11 | bloated form |
| 7 | (-(-1^k)) / ((-1 - k) - k) | 10 | bloated form |
| 137 | (-(-1^k)) / ((-1 - k) - k) | 10 | same form as seed 7 |
| 2718 | (-1^k) / (k + (1 + k)) | 9 | canonical minimal form |
| 31415 | (-1^k) / ((k × 2) - -1) | 9 | canonical minimal form |

The canonical 9-node form (-1)^k / (2k+1) is not always found: bloated algebraic equivalents appear in 3/5 seeds. Parsimony pressure at λ_p = 0.005 is insufficient to drive canonical form but does not impair discovery. Increasing parsimony to λ_p ≥ 0.01 destroys discovery entirely (Section 5.4).

## 5.2 Failure Under Expanded Terminals

With 15 terminals at population 1,000, no seeds find Leibniz: {{result:logprec_stress_l1_0_5:value}}/5. The dominant failure mode is wrong-limit attractors, rational functions whose partial sums converge to finite values near π/4.

Seed 42 found the expression 5/((6+4k)(k-2)), which achieves {{result:wrong_limit_ti_15_93:value}} bits of precision at T=10,000, exceeding Leibniz's {{result:leibniz_ti_15_29:value}} bits, with perfect monotonicity. This expression is not Leibniz. Its partial sums converge to a value that appears closer to π/4 than Leibniz within the evaluation horizon, but at T→∞, Leibniz converges exactly while this attractor converges to a different value.
<!-- EDITORIAL REVIEW: What did the other seeds (7, 137, 2718, 31415) find at 15 terminals?
     If data exists, consider adding: "Other seeds found [similar/different] attractors"
     to establish whether the wrong-limit attractor pattern is universal or seed-specific.
     —Review item #7 -->

## 5.3 The Scaling Boundary

The 7 × 4 scaling grid reveals a phase transition between t=8 and t=10 for population sizes up to 5,000. Discovery results across the full grid are as follows.

| t (terminals) | pop=1000 | pop=2000 | pop=5000 | pop=10000 |
|---|---|---|---|---|
| 4 | {{result:logprec_minimal_5_5:value}}/5 | {{result:scaling_grid_t4_p2000:value}}/5 | {{result:scaling_grid_t4_p5000:value}}/5 | {{result:scaling_grid_t4_p10000:value}}/5 |
| 6 | {{result:scaling_grid_t6_p1000:value}}/5 | {{result:scaling_grid_t6_p2000:value}}/5 | {{result:scaling_grid_t6_p5000:value}}/5 | {{result:scaling_grid_t6_p10000:value}}/5 |
| 8 | {{result:scaling_grid_t8_p1000:value}}/5 | {{result:scaling_grid_t8_p2000:value}}/5 | {{result:scaling_grid_t8_p5000:value}}/5 | {{result:scaling_grid_t8_p10000:value}}/5 |
| 10 | {{result:scaling_grid_t10_p1000:value}}/5 | {{result:scaling_grid_t10_p2000:value}}/5 | {{result:scaling_grid_t10_p5000:value}}/5 | {{result:scaling_grid_t10_p10000:value}}/5 |
| 12 | {{result:scaling_grid_t12_p1000:value}}/5 | {{result:scaling_grid_t12_p2000:value}}/5 | {{result:scaling_grid_t12_p5000:value}}/5 | {{result:scaling_grid_t12_p10000:value}}/5 |
| 15 | {{result:logprec_stress_l1_0_5:value}}/5 | {{result:scaling_grid_t15_p2000:value}}/5 | {{result:scaling_grid_t15_p5000:value}}/5 | {{result:scaling_grid_t15_p10000:value}}/5 |
| 20 | {{result:scaling_grid_t20_p1000:value}}/5 | {{result:scaling_grid_t20_p2000:value}}/5 | {{result:scaling_grid_t20_p5000:value}}/5 | {{result:scaling_grid_t20_p10000:value}}/5 |

At t=4, discovery is reliable across all population sizes. At t=6 and t=8, success drops but remains nonzero. At t=10 and above, discovery fails completely except for one anomaly: at t=15 with pop=10,000, 2/5 seeds succeed. This partial recovery is absent at t=10, t=12, and t=20.

<!-- EDITORIAL REVIEW: The following explanation is speculative without evidence.
     Options: (1) Remove and say "we do not have a mechanistic account" and stop,
     (2) Weaken to "one possibility is..." with explicit caveat that 5 seeds is a pilot,
     (3) Keep as-is. The 2/5 at t=15/p=10000 could be noise. —Review item #5 -->
We do not have a confirmed mechanistic account of this non-monotonicity. The most plausible explanation is that at t=15 the search space contains fewer wrong-limit attractors than at t=10 or t=12, allowing a large population to occasionally maintain sufficient structural coverage.

The boundary between t=8 and t=10 holds for populations up to 5,000. Increasing population from 1,000 to 10,000 does not shift this boundary: it provides marginal gains at t=6 and t=8 and produces the anomalous partial recovery at t=15, but the t=10 wall remains intact. This confirms that coverage, not fitness landscape quality, limits discovery.

## 5.4 Size Penalty

GP parsimony pressure penalizes larger expression trees by subtracting λ_p × (node count) from fitness. This size penalty keeps solutions simple but creates a ceiling on viable tree complexity.

| λ_p | Seeds Found | Dominant Form | Notes |
|---|---|---|---|
| 0.005 (baseline) | 5/5 | 9–11 node Leibniz equivalents | Working |
| 0.01 | 0/5 | 3-node zero constants (k-k, 1+-1) | Penalty dominates |
| 0.02 | 0/5 | 1-node constant (-1) | Leibniz ejected from top 10% |
| 0.05 | 0/5 | 1-node constant (-1) | Fitness ordering inverted |

The transition is sharp. At λ_p = 0.005, the 9-node Leibniz tree scores {{result:parsimony_leibniz_fitness_baseline:value}} fitness. At λ_p = 0.01, the same tree scores {{result:parsimony_leibniz_fitness_0_01:value}}. The score is still nominally better than the zero-constant attractor at {{result:parsimony_zero_constant_fitness:value}}, but the margin is too small for selection pressure to overcome the initialization disadvantage within the time budget.

The log-precision fitness terms (w_1·ti + w_2·mono + w_3·rate) sum to {{result:logprec_max_fitness_leibniz:value}} for a Leibniz expression. At 9 nodes and λ_p=0.005, the parsimony penalty is λ_p × 9 < {{result:logprec_max_fitness_leibniz:value}}, which requires λ_p < 0.0073 for discovery to succeed. The baseline operates near but below this ceiling.

## 5.5 Fitness Modifications Cannot Rescue Large Terminal Sets

We tested seven modifications to the log-precision fitness on the 15-terminal configuration. None achieved reliable discovery.

| Modification | Seeds Found | Notes |
|---|---|---|
| Extended checkpoints | 0/5 | Additional T values beyond 10,000 |
| Large-T penalty w=0.1 | {{result:fitness_largeT_w0_1:value}}/5 | Penalizes series that plateau before T_max |
| Large-T penalty w=0.5 | 0/5 | Penalty too heavy, kills borderline expressions |
| Rate consistency | 0/5 | Penalizes deviation from constant bits/decade |
| Pure gradient magnitude | 0/5 | Rewards only precision gain rate, ignores terminal value |
| Hybrid scalar×uniformity | 0/5 | Combined rate and uniformity signal |
| Min-component bottleneck | 0/5 | Requires all fitness terms above threshold |

The alpha parameter sweep (reducing α from 1.0 to 0.5 in the convergence-aware fitness) produced {{result:gp_alpha_0_5_4_5:value}}/5 on the minimal terminal set, comparable to the baseline. No modification achieved better than 1/5 on 15 terminals.

<!-- EDITORIAL REVIEW: "The bottleneck is coverage, not fitness landscape quality"
     appears here, in 5.3, in Discussion, and in Conclusion. Reviewer says once in
     Results is sufficient. Decide which instance(s) to keep. —Review item #9 -->
The consistent failure confirms the diagnosis: the bottleneck is coverage, not fitness landscape quality. The fitness correctly ranks Leibniz as optimal when Leibniz-equivalent subtrees are present in the population. Presence requires the population to contain the right building blocks, and the probability of assembling them decreases sharply with terminal set size.

<!-- EDITORIAL REVIEW: Missing from Results:
     (1) GP convergence-aware vs log-precision comparison grid at p=5000 and p=10000.
         Data exists in handoff notes. Consider adding Section 5.6 "Fitness Function Comparison."
     (2) Extended time test: GP convergence-aware at t=10, p=5000, 2hr/seed: 1/5 (same seed
         as 30-min run). Other 4 found same wrong-limit attractors. Strong evidence that time
         isn't the bottleneck. Currently not presented.
     Both support the coverage thesis. —Review items #10, #11 -->
<!-- EDITORIAL REVIEW: Figures not yet created or captured:
     - Scaling grid heatmap visualization (Table 3 as color-coded grid)
     - Precision vs T plot (Leibniz vs wrong-limit attractor trajectories)
     - Parsimony collapse plot (fitness vs λ_p for Leibniz tree)
     - Convergence rate plot (for Discussion 6.1, but data comes from Results)
     These are listed in evidence_map.md Key Figures table as TBD. -->
