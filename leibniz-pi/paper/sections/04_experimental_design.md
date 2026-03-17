# 4. Experimental Design

## 4.1 The Injection Confound

Early experiments (v2) seeded the initial population with a copy of the Leibniz expression tree. Both fitness functions reported {{result:v2_confounded_5_5:value}}/5 discovery. Subsequent analysis revealed this was an artifact: the injected tree survived through elitism, never being lost to selection pressure. The injected tree was *retained*, not *discovered*.

We made this error, caught it, and corrected it. All results presented in this paper (v3 onward) use pure random initialization with no injection. The confound is documented here because it mirrors the Hillar and Sommer (2012) critique of Schmidt and Lipson (2009): implicit encoding of the answer in the search structure can create the illusion of emergent discovery.

## 4.2 Clean Protocol (v3)

All v3 experiments use ramped half-and-half initialization with no injection. Each configuration is evaluated across five seeds: 42, 7, 137, 2718, and 31415. The time budget per seed is 360 seconds for minimal terminal experiments and 1800 seconds for the scaling grid. An expression is counted as a discovery if its first 20 terms match Leibniz to within 10^-6 absolute error per term.

## 4.3 Terminal Set Construction

Terminal sets are constructed deterministically at each size N. The base set {k, 1, -1, 2} is always present, ensuring Leibniz is constructible regardless of N. Additional integers are added in the pattern 3, -2, 4, -3, 5, -4, ... (alternating positive and negative, no zero, no duplicates of base terminals). This construction controls for primitive availability: the experiment isolates the effect of search space expansion on discovery rate, not whether the correct building blocks exist.

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

The scaling grid spans seven terminal counts (t = 4, 6, 8, 10, 12, 15, 20) and four population sizes (1000, 2000, 5000, 10000), with five seeds per cell, yielding 140 individual runs. The log-precision fitness is used throughout the grid. Time budget per seed is 1800 seconds. This design tests whether increasing population size can compensate for expanding terminal sets, and identifies the boundary beyond which no tested population size achieves reliable discovery.
