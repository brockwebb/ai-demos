# 4. Experimental Design

## 4.1 The Injection Confound

Early experiments (v2) seeded the initial population with a copy of the Leibniz expression tree. Both fitness functions reported {{result:v2_confounded_5_5:value}}/5 discovery, but subsequent analysis showed this was an artifact. The injected tree survived through elitism, never being lost to selection pressure. The tree was *retained*, not *discovered*.

We made this error, caught it, and corrected it. All results in this paper (v3 onward) use pure random initialization with no injection.

We document the confound here because it mirrors a known failure mode. Hillar and Sommer (2012) showed that Schmidt and Lipson (2009) implicitly encoded the answer in the search structure, creating the illusion of emergent discovery. Our injection confound is the same class of error: when the target is present in the initial population, survival through elitism is indistinguishable from discovery.

## 4.2 Clean Protocol (v3)

All v3 experiments use ramped half-and-half initialization with no injection. Each configuration is evaluated across five seeds (42, 7, 137, 2718, 31415). The function set (Section 3.1) is held constant across all experiments: binary operators {+, -, ×, ÷, ^} and unary negation.

Time budgets are pragmatic compute constraints, not theoretically motivated. Minimal-terminal runs allocate 360 seconds per seed, with a 1,800-second total budget per configuration. Scaling grid runs allocate 1,800 seconds per seed, with a 10,800-second total budget per cell. An extended run at t=10 and pop=5,000 allocated 7,200 seconds per seed, four times the standard budget. {{result:gp_extended_t10_p5000_1_5:value}}/5 seeds found Leibniz under the extended budget, the same seed (val=7) that succeeded under the standard budget. The time budget is not the binding constraint at t=10.

An expression counts as a discovery if its terms match the Leibniz series term by term. We compute f(k) for k = 0, ..., 19 and compare against precomputed Leibniz values (-1)^k/(2k+1). A tolerance of 10^-6 per term accommodates floating-point arithmetic (Section 3.2).

## 4.3 Terminal Set Construction

The GP primitive set is held constant across all experiments. The table below lists operators and their safe-evaluation behavior.

| Component | Value | Notes |
|-----------|-------|-------|
| Binary operators | +, -, ×, ÷, ^ | Standard arithmetic |
| Unary operators | neg | Negation |
| Safe division (÷ when \|denominator\| ≤ 10^-10) | returns 1.0 | Implicit constant; acts as additional terminal |
| Power overflow (\|result\| > 10^6) | returns 1.0 | Implicit constant; acts as additional terminal |
| Power exponent | Rounded to nearest integer | Constrains search to integer powers |

Safe division returns 1.0 when the denominator is at or below 10^-10. Power overflow returns 1.0 when the result magnitude exceeds 10^6. Both values act as implicit additional terminals in the search space. An expression that triggers either condition at certain k values uses 1.0 as a fallback constant. Researchers counting available terminals should account for these implicit constants.

Terminal sets are constructed deterministically at each size N. The base set {k, 1, -1, 2} is always present, ensuring Leibniz is constructible regardless of N. Additional integers follow the pattern 3, -2, 4, -3, 5, -4, ..., alternating positive and negative with no zero and no duplicates of base terminals. The alternating sign pattern ensures both positive and negative values are available at every terminal count. Additional terminals provide alternative construction paths for the oscillating numerator and odd denominator, not inert noise.

This construction controls for primitive availability. The experiment isolates the effect of search space expansion on discovery rate, not whether the correct building blocks exist.

| N | Terminal Set |
|---|---|
| 4 | {k, 1, -1, 2} |
| 6 | {k, 1, -1, 2, 3, -2} |
| 8 | {k, 1, -1, 2, 3, -2, 4, -3} |
| 10 | {k, 1, -1, 2, 3, -2, 4, -3, 5, -4} |
| 12 | {k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5} |
| 15 | {k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8} |
| 20 | {k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8, -7, 9, -8, 10, -9} |

## 4.4 Scaling Grid

The scaling grid crosses seven terminal counts (N = 4, 6, 8, 10, 12, 15, 20) with four population sizes (1,000, 2,000, 5,000, 10,000). Five seeds per cell yield 140 individual runs. All runs use log-precision fitness; time budgets are specified in Section 4.2.

The design answers two questions. First, can increasing population size compensate for expanding terminal sets? Second, where is the boundary beyond which no tested population size achieves reliable discovery?
