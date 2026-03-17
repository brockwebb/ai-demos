# 4. Experimental Design

## 4.1 The Injection Confound

Early experiments (v2) seeded the initial population with a copy of the Leibniz expression tree. Both fitness functions reported {{result:v2_confounded_5_5:value}}/5 discovery, but subsequent analysis showed this was an artifact. The injected tree survived through elitism, never being lost to selection pressure. The tree was *retained*, not *discovered*.

We made this error, caught it, and corrected it. All results in this paper (v3 onward) use pure random initialization with no injection.

We document the confound here because it mirrors a known failure mode. Hillar and Sommer (2012) showed that Schmidt and Lipson (2009) implicitly encoded the answer in the search structure, creating the illusion of emergent discovery. Our injection confound is the same class of error: when the target is present in the initial population, survival through elitism is indistinguishable from discovery.

## 4.2 Clean Protocol (v3)

All v3 experiments use ramped half-and-half initialization with no injection. Each configuration is evaluated across five seeds (42, 7, 137, 2718, 31415).

The time budget per seed is 360 seconds for minimal terminal runs and 1,800 seconds for the scaling grid. An expression counts as a discovery if its first 20 terms match the Leibniz series to within 10^-6 absolute error per term (Section 3.2).

## 4.3 Terminal Set Construction

Terminal sets are constructed deterministically at each size N. The base set {k, 1, -1, 2} is always present, ensuring Leibniz is constructible regardless of N. Additional integers follow the pattern 3, -2, 4, -3, 5, -4, ..., alternating positive and negative with no zero and no duplicates of base terminals.

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

The scaling grid crosses seven terminal counts (N = 4, 6, 8, 10, 12, 15, 20) with four population sizes (1,000, 2,000, 5,000, 10,000). Five seeds per cell yield 140 individual runs. All runs use log-precision fitness with a 1,800-second time budget per seed.

The design answers two questions. First, can increasing population size compensate for expanding terminal sets? Second, where is the boundary beyond which no tested population size achieves reliable discovery?
