# 5. Results

## 5.1 Discovery Under Minimal Terminals

With the minimal terminal set {k, 1, -1, 2} and no injection, the log-precision fitness achieves {{result:entropy_minimal_5_5:value}}/5 discovery across five seeds. The convergence-aware fitness achieves {{result:gp_minimal_2_5:value}}/5 at population 1,000 and {{result:gp_pop2000_5_5:value}}/5 at population 2,000. Total runtime for the {{result:entropy_minimal_5_5:value}}/5 log-precision run across all five seeds was {{result:entropy_minimal_runtime:value}} seconds.

| Fitness | Pop | Seeds Found | Mean Generations |
|---|---|---|---|
| Log-precision | 1,000 | {{result:entropy_minimal_5_5:value}}/5 | 2,981 |
| Convergence-aware | 1,000 | {{result:gp_minimal_2_5:value}}/5 | — |
| Convergence-aware | 2,000 | {{result:gp_pop2000_5_5:value}}/5 | — |

All discovered expressions are algebraically equivalent to (-1)^k / (2k+1), verified identical at k=100,000 with zero divergence. Table 2 shows the structural variants that appear across seeds.

| Seed | Expression | Nodes |
|---|---|---|
| 42 | (-(-1^k)) / ((-k) - (k - -1)) | 11 |
| 7 | (-(-1^k)) / ((-1 - k) - k) | 10 |
| 2718 | (-1^k) / (k + (1 + k)) | 9 |
| 31415 | (-1^k) / ((k × 2) - -1) | 9 |

The canonical 9-node form (-1)^k / (2k+1) is not always found: bloated algebraic equivalents appear in 3/5 seeds. Parsimony pressure at λ_p = 0.005 is insufficient to drive canonical form but does not impair discovery. Increasing parsimony to λ_p ≥ 0.01 destroys discovery entirely (Section 5.4).

## 5.2 Failure Under Expanded Terminals

With 15 terminals at population 1,000, no seeds find Leibniz: {{result:entropy_stress_l1_0_5:value}}/5. The dominant failure mode is wrong-limit attractors, rational functions whose partial sums converge to finite values near π/4.

Seed 42 found the expression 5/((6+4k)(k-2)), which achieves {{result:wrong_limit_ti_15_93:value}} bits of precision at T=10,000, exceeding Leibniz's {{result:leibniz_ti_15_29:value}} bits, with perfect monotonicity. This expression is not Leibniz. Its partial sums converge to a value that appears closer to π/4 than Leibniz within the evaluation horizon, but at T→∞, Leibniz converges exactly while this attractor converges to a different value.

## 5.3 The Scaling Boundary

The 7 × 4 scaling grid reveals a phase transition between t=8 and t=10 for population sizes up to 5,000. Discovery results across the full grid are as follows.

| t (terminals) | pop=1000 | pop=2000 | pop=5000 | pop=10000 |
|---|---|---|---|---|
| 4 | 5/5 | 4/5 | 5/5 | 5/5 |
| 6 | 1/5 | 2/5 | 1/5 | 1/5 |
| 8 | 1/5 | 1/5 | 1/5 | 0/5 |
| 10 | 0/5 | 0/5 | 0/5 | 0/5 |
| 12 | 0/5 | 0/5 | 0/5 | 0/5 |
| 15 | 0/5 | 0/5 | 0/5 | 2/5 |
| 20 | 0/5 | 0/5 | 0/5 | 0/5 |

At t=4, discovery is reliable across all population sizes. At t=6 and t=8, success drops but remains nonzero. At t=10 and above, discovery fails completely except for one anomaly: at t=15 with pop=10,000, 2/5 seeds succeed. This partial recovery is absent at t=10, t=12, and t=20.

We do not have a confirmed mechanistic account of this non-monotonicity. The most plausible explanation is that at t=15 the search space contains fewer wrong-limit attractors than at t=10 or t=12, allowing a large population to occasionally maintain sufficient structural coverage.

The boundary between t=8 and t=10 holds for populations up to 5,000. Increasing population from 1,000 to 10,000 does not shift this boundary: it provides marginal gains at t=6 and t=8 and produces the anomalous partial recovery at t=15, but the t=10 wall remains intact. This confirms that coverage, not fitness landscape quality, limits discovery.

## 5.4 Parsimony Pressure

| λ_p | Seeds Found | Dominant Form | Notes |
|---|---|---|---|
| 0.005 (baseline) | 5/5 | 9–11 node Leibniz equivalents | Working |
| 0.01 | 0/5 | 3-node zero constants (k-k, 1+-1) | Penalty dominates |
| 0.02 | 0/5 | 1-node constant (-1) | Leibniz ejected from top 10% |
| 0.05 | 0/5 | 1-node constant (-1) | Fitness ordering inverted |

The transition is sharp. At λ_p = 0.005, the 9-node Leibniz tree scores approximately 0.021 fitness. At λ_p = 0.01, the same tree scores approximately -0.024. The score is still nominally better than the zero-constant attractor at approximately -0.030, but the margin is too small for selection pressure to overcome the initialization disadvantage within the time budget.

The log-precision fitness components (w_1·ti + w_2·mono + w_3·rate) sum to at most approximately 0.07 for Leibniz, placing a hard ceiling on viable parsimony: λ_p × 9 < 0.07, so λ_p < 0.008. The baseline operates near but below this ceiling.

## 5.5 Fitness Modifications Cannot Rescue Large Terminal Sets

We tested seven modifications to the log-precision fitness on the 15-terminal configuration. None achieved reliable discovery.

| Modification | Seeds Found | Notes |
|---|---|---|
| Extended checkpoints | 0/5 | Additional T values beyond 10,000 |
| Large-T penalty w=0.1 | {{result:fitness_largeT_w0_1:value}}/5 | Penalizes series that plateau before T_max |
| Large-T penalty w=0.5 | 0/5 | Penalty too heavy, kills borderline expressions |
| Rate consistency | 0/5 | Penalizes deviation from constant bits/decade |
| Pure gradient magnitude | 0/5 | Rewards only information rate, ignores terminal value |
| Hybrid scalar×uniformity | 0/5 | Combined rate and uniformity signal |
| Min-component bottleneck | 0/5 | Requires all fitness components above threshold |

The alpha parameter sweep (reducing α from 1.0 to 0.5 in the convergence-aware fitness) produced {{result:gp_alpha_0_5_4_5:value}}/5 on the minimal terminal set, comparable to the baseline. No modification achieved better than 1/5 on 15 terminals.

The consistent failure confirms the diagnosis: the bottleneck is coverage, not fitness landscape quality. The fitness correctly ranks Leibniz as optimal when Leibniz-equivalent subtrees are present in the population. Presence requires the population to contain the right building blocks, and the probability of assembling them decreases sharply with terminal set size.
