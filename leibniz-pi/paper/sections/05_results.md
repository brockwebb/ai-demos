# Results

## Discovery Under Minimal Terminals

With the minimal terminal set {k, 1, -1, 2} and no injection, the log-precision fitness achieves {{result:logprec_minimal_5_5:value}}/5 discovery across five seeds. The convergence-aware fitness achieves {{result:gp_minimal_2_5:value}}/5 at population 1,000 and {{result:gp_pop2000_5_5:value}}/5 at population 2,000. Total runtime for the complete log-precision run across all five seeds was {{result:logprec_minimal_runtime:value}} seconds.

| Fitness | Pop | Seeds Found | Mean Generations |
|---|---|---|---|
| Log-precision | 1,000 | {{result:logprec_minimal_5_5:value}}/5 | {{result:logprec_minimal_mean_gen:value}} |
| Convergence-aware | 1,000 | {{result:gp_minimal_2_5:value}}/5 | n/a |
| Convergence-aware | 2,000 | {{result:gp_pop2000_5_5:value}}/5 | n/a |

: Table 3: Discovery rates under minimal terminals (N=4) by fitness function and population size.

All discovered expressions are algebraically equivalent to (-1)^k / (2k+1), verified identical at k=100,000 with zero divergence. The structural variants that appear across seeds are shown below.

| Seed | Expression | Nodes | Notes |
|---|---|---|---|
| 42 | (-(-1^k)) / ((-k) - (k - -1)) | 11 | bloated form |
| 7 | (-(-1^k)) / ((-1 - k) - k) | 10 | bloated form |
| 137 | (-(-1^k)) / ((-1 - k) - k) | 10 | same form as seed 7 |
| 2718 | (-1^k) / (k + (1 + k)) | 9 | canonical minimal form |
| 31415 | (-1^k) / ((k × 2) - -1) | 9 | canonical minimal form |

: Table 4: Structural variants of the Leibniz series discovered across five seeds.

The canonical 9-node form (-1)^k / (2k+1) is not always found: bloated algebraic equivalents appear in 3/5 seeds. Parsimony pressure at λ_p = 0.005 is insufficient to drive canonical form but does not impair discovery. Increasing parsimony to λ_p ≥ 0.01 destroys discovery entirely (Section 5.4).

## Failure Under Expanded Terminals

With 15 terminals at population 1,000, no seeds find Leibniz ({{result:logprec_stress_l1_0_5:value}}/5). The failure modes split into two categories: trivial collapse to constants (4/5 seeds) and convergence to a wrong-limit attractor (1/5 seeds). Seeds 7 and 31415 collapsed to the constant 0, seed 137 to a small constant expression, and seed 2718 to a low-precision rational function (4.80 bits at T=10,000). Wrong-limit attractors become the dominant failure mode at larger terminal counts and populations. At t=20 with pop=10,000, all five seeds converged to a power-law decay family (Appendix A.3).

Seed 42 produced the strongest wrong-limit attractor: 5/((6+4k)(k-2)), which achieves {{result:wrong_limit_ti_15_93:value}} bits of precision at T=10,000, exceeding Leibniz's {{result:leibniz_ti_15_29:value}} bits, with perfect monotonicity. This expression is not Leibniz. Within the evaluation horizon, its partial sums converge to a value that appears closer to π/4 than Leibniz. At T→∞, Leibniz converges exactly while this attractor converges to a different value.

![Log-precision trajectories for the Leibniz series and the strongest wrong-limit attractor](figures/fig2_precision_vs_T.png)

**Figure 1:** Log-precision trajectories for the Leibniz series and the strongest wrong-limit attractor (seed 42, 15 terminals). The attractor exceeds Leibniz precision within the evaluation horizon (T <= 10,000) but converges to a different limit.

## The Scaling Boundary

The 7 × 4 scaling grid reveals a phase transition between t=8 and t=10 for all population sizes tested. Discovery results across the full grid are as follows.

| t (terminals) | pop=1000 | pop=2000 | pop=5000 | pop=10000 |
|---|---|---|---|---|
| 4 | {{result:logprec_minimal_5_5:value}}/5 | {{result:scaling_grid_t4_p2000:value}}/5 | {{result:scaling_grid_t4_p5000:value}}/5 | {{result:scaling_grid_t4_p10000:value}}/5 |
| 6 | {{result:scaling_grid_t6_p1000:value}}/5 | {{result:scaling_grid_t6_p2000:value}}/5 | {{result:scaling_grid_t6_p5000:value}}/5 | {{result:scaling_grid_t6_p10000:value}}/5 |
| 8 | {{result:scaling_grid_t8_p1000:value}}/5 | {{result:scaling_grid_t8_p2000:value}}/5 | {{result:scaling_grid_t8_p5000:value}}/5 | {{result:scaling_grid_t8_p10000:value}}/5 |
| 10 | {{result:scaling_grid_t10_p1000:value}}/5 | {{result:scaling_grid_t10_p2000:value}}/5 | {{result:scaling_grid_t10_p5000:value}}/5 | {{result:scaling_grid_t10_p10000:value}}/5 |
| 12 | {{result:scaling_grid_t12_p1000:value}}/5 | {{result:scaling_grid_t12_p2000:value}}/5 | {{result:scaling_grid_t12_p5000:value}}/5 | {{result:scaling_grid_t12_p10000:value}}/5 |
| 15 | {{result:logprec_stress_l1_0_5:value}}/5 | {{result:scaling_grid_t15_p2000:value}}/5 | {{result:scaling_grid_t15_p5000:value}}/5 | {{result:scaling_grid_t15_p10000:value}}/5 |
| 20 | {{result:scaling_grid_t20_p1000:value}}/5 | {{result:scaling_grid_t20_p2000:value}}/5 | {{result:scaling_grid_t20_p5000:value}}/5 | {{result:scaling_grid_t20_p10000:value}}/5 |

: Table 5: Discovery rate (seeds found / 5) across terminal set sizes and population sizes. The phase transition between t=8 and t=10 holds across all population sizes.

At t=4, discovery is reliable across all population sizes. At t=6 and t=8, success drops but remains nonzero. At t=10 and above, discovery fails completely except for one anomaly: at t=15 with pop=10,000, 2/5 seeds succeed. This partial recovery is absent at t=10, t=12, and t=20. We do not have a mechanistic account of this non-monotonicity.

The boundary between t=8 and t=10 holds for all population sizes tested. Increasing population from 1,000 to 10,000 does not shift this boundary. Larger populations provide marginal gains at t=6 and t=8 and produce the anomalous partial recovery at t=15, but the t=10 wall remains intact. This pattern is consistent with a coverage limitation rather than a fitness landscape limitation.

## Size Penalty

GP parsimony pressure penalizes larger expression trees by subtracting λ_p × (node count) from fitness. This size penalty keeps solutions simple but creates a ceiling on viable tree complexity.

| λ_p | Seeds Found | Dominant Form | Notes |
|---|---|---|---|
| 0.005 (baseline) | 5/5 | 9–11 node Leibniz equivalents | Working |
| 0.01 | 0/5 | 3-node zero constants (k-k, 1+-1) | Penalty dominates |
| 0.02 | 0/5 | 1-node constant (-1) | Leibniz ejected from top 10% |
| 0.05 | 0/5 | 1-node constant (-1) | Fitness ordering inverted |

: Table 6: Effect of parsimony pressure on discovery. The transition from full discovery to complete failure occurs between lambda_p = 0.005 and lambda_p = 0.01.

The transition is sharp. At λ_p = 0.005, the 9-node Leibniz tree scores {{result:parsimony_leibniz_fitness_baseline:value}} fitness. At λ_p = 0.01, the same tree scores {{result:parsimony_leibniz_fitness_0_01:value}}. The score is still nominally better than the zero-constant attractor at {{result:parsimony_zero_constant_fitness:value}}, but the margin is too small for selection pressure to overcome the initialization disadvantage within the time budget.

The log-precision fitness terms (w_1·ti + w_2·mono + w_3·rate) sum to {{result:logprec_max_fitness_leibniz:value}} for a Leibniz expression. At 9 nodes and λ_p=0.005, the parsimony penalty is λ_p × 9 < {{result:logprec_max_fitness_leibniz:value}}, which requires λ_p < 0.0073 for discovery to succeed. The baseline operates near but below this ceiling.

This threshold sensitivity is consistent with prior findings that parsimony pressure has a narrow effective range. Too weak and it fails to control bloat. Too strong and it collapses the population to trivial solutions [@Poli2008ParsimonyEasy; @Soule1998CodeGrowth]. Our contribution is the quantitative demonstration of the crossover point where the Leibniz tree's fitness falls below the zero-constant attractor.

![Fitness score as a function of parsimony coefficient for the 9-node Leibniz tree and the 3-node zero-constant attractor](figures/fig3_parsimony_collapse.png)

**Figure 2:** Fitness score as a function of parsimony coefficient (lambda_p) for the 9-node Leibniz tree and the 3-node zero-constant attractor. The crossover at lambda_p approximately 0.0110 marks where the zero-constant becomes fitter than Leibniz.

## Fitness Modifications Cannot Rescue Large Terminal Sets

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

: Table 7: Fitness function modifications tested on the 15-terminal configuration. No modification achieved reliable discovery.

The alpha parameter sweep (reducing α from 1.0 to 0.5 in the convergence-aware fitness) produced {{result:gp_alpha_0_5_4_5:value}}/5 on the minimal terminal set, comparable to the baseline. No modification achieved better than 1/5 on 15 terminals.

The consistent failure confirms the diagnosis: the bottleneck is coverage, not fitness landscape quality. The fitness correctly ranks Leibniz as optimal when Leibniz-equivalent subtrees are present in the population. Presence requires the population to contain the right building blocks, and the probability of assembling them decreases sharply with terminal set size.

We also ran the convergence-aware fitness at t=10 and population 5,000 with 7,200 seconds per seed, four times the standard budget. Only {{result:gp_extended_t10_p5000_1_5:value}} of 5 seeds found Leibniz, the same seed (val=7) that succeeded under the standard budget. The remaining four seeds did not find Leibniz-equivalent expressions. Extending the time budget by a factor of four does not rescue discovery at t=10.

## Threshold Sensitivity

The log-precision fitness uses a monotonicity threshold (MIN_GAIN) that defines how many bits of precision gain a checkpoint pair must show to count as monotonically improving. The baseline value of 0.5 bits was a design choice. We tested whether discovery rates depend on this threshold.

| MIN_GAIN (bits) | Seeds Found | Notes |
|---|---|---|
| 0.1 | {{result:threshold_mingain_0.1_t4:value}}/5 | Too permissive: wrong-limit attractors achieve full monotonicity credit |
| 0.5 (baseline) | {{result:logprec_minimal_5_5:value}}/5 | Below Leibniz's natural gain rate |
| 1.0 | {{result:threshold_mingain_1.0_t4:value}}/5 | At Leibniz's gain rate: Leibniz barely qualifies |
| 2.0 | {{result:threshold_mingain_2.0_t4:value}}/5 | Above Leibniz's gain rate: fitness collapses to trivial constants |

: Table 8: Log-precision monotonicity threshold sensitivity at t=4, pop=1,000. Leibniz gains approximately 1.0 bit per checkpoint step.

The threshold is not a free parameter. It must be set below the target process's natural precision gain rate. Leibniz gains approximately 1.0 bit per checkpoint step. At MIN_GAIN=0.5, the threshold is comfortably below this rate, and all seeds succeed. At MIN_GAIN=1.0, Leibniz itself barely satisfies the criterion, and discovery drops to {{result:threshold_mingain_1.0_t4:value}}/5. At MIN_GAIN=2.0, Leibniz never achieves the required gain, the W_2 (monotonicity) term contributes zero, and the fitness collapses to trivial zero-constant expressions. At the phase transition boundary (t=6), reducing MIN_GAIN to 0.1 did not change the discovery rate ({{result:threshold_mingain_0.1_t6:value}}/5), suggesting the threshold matters only in the regime where coverage is sufficient.

The convergence-aware fitness threshold (5% error reduction between checkpoints) is less sensitive. Varying the threshold from 1% to 20% produced discovery rates between 2/5 and 3/5, within noise for a five-seed sample.

The threshold must be set below the target process's natural gain rate. The threshold is constrained by the problem, not freely tunable.
