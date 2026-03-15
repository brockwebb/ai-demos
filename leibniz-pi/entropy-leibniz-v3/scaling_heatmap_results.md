# Scaling Heat Map: Terminals × Population → Discovery Rate

Experiment: entropy-leibniz-v3 minimal, no injection, 5 seeds per cell.
Budget: MAX_SEED=1800s, MAX_TOTAL=10800s per cell.

## Discovery Rate Table (seeds found / 5)

| Terminals | Terminal Set | Pop=1000 | Pop=2000 | Pop=5000 | Pop=10000 |
|-----------|-------------|----------|----------|----------|-----------|
| 4         | `{k, 1, -1, 2}`            | 5/5*     | 4/5      | 5/5      | 5/5       |
| 6         | `{k, 1, -1, 2, 3, -2}`     | 1/5      | 2/5      | 1/5      | 1/5       |
| 8         | `{k, 1, -1, 2, 3, -2, 4, -3}` | 1/5      | 1/5      | 1/5      | 0/5       |
| 10        | `{k, 1, -1, 2, 3, -2, 4, -3, 5, -4}` | 0/5      | 0/5      | 0/5      | 0/5       |
| 12        | `{k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5}` | 0/5      | 0/5      | 0/5      | 0/5       |
| 15        | `{k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8}` | 0/5*     | 0/5      | 0/5      | **2/5**   |
| 20        | `{k, 1, -1, 2, 3, -2, 4, -3, 5, -4, 6, -5, 7, -6, 8, -7, 9, -8, 10, -9}` | 0/5      | 0/5      | 0/5      | 0/5       |

\* = from prior experiment (not re-run)

## Mean Generations (successful seeds only)

| Terminals | Pop=1000 | Pop=2000 | Pop=5000 | Pop=10000 |
|-----------|----------|----------|----------|-----------|
| 4         | 2981     | 5951     | 2856     | ~2000     |
| 6         | 22819    | 20446    | 1632     | 3247      |
| 8         | 10467    | 8353     | 9695     | —         |
| 10        | —        | —        | —        | —         |
| 12        | —        | —        | —        | —         |
| 15        | —        | —        | —        | 1052      |
| 20        | —        | —        | —        | —         |

## Mean Elapsed Time / successful seed (seconds)

| Terminals | Pop=1000 | Pop=2000 | Pop=5000 | Pop=10000 |
|-----------|----------|----------|----------|-----------|
| 4         | 74s      | 319s     | 322s     | ~200s     |
| 6         | 561s     | 961s     | 166s     | 748s      |
| 8         | 272s     | 381s     | 1037s    | —         |
| 10        | —        | —        | —        | —         |
| 12        | —        | —        | —        | —         |
| 15        | —        | —        | —        | 389s      |
| 20        | —        | —        | —        | —         |

## Phase Transition Analysis

At what terminal count does each population size fail (0/5)?

- Pop=1000:  last success at t=8, first 0/5 at t=10
- Pop=2000:  last success at t=8, first 0/5 at t=10
- Pop=5000:  last success at t=8, first 0/5 at t=10
- Pop=10000: last success at t=6 in the 6–12 range, **anomalous 2/5 at t=15**

## Wrong-Limit Attractors

Top expressions dominating failed cells:

- (×3) `((((4 - -3) ^ -2) - (4 - (k / -3))) ^ -2)`
- (×2) `((((k / -3) + ((-3 + -4) ^ -2)) + -4) ^ -2)`
- (×2) `((((-4 + -3) ^ -2) + (-4 + (k / -3))) ^ -2)`
- (×2) `(((k + -4) / -4) ^ (-4 - 5))`
- (×2) `((-5 / 6) ^ (k - 2))`
- (×2) `((7 ^ 7) / (-1 ^ (k / -3)))`
- (×2) `((7 ^ 7) * (-1 ^ (k / 3)))`
- (×2) `(((4 - k) / 4) ^ -9)`

## Conclusions

### Is there a sharp phase boundary?

The boundary is the same (t=8→t=10) for all tested population sizes from 1000 to 5000.
Population size in the 1k–5k range does not shift the boundary.

### Does pop=10000 extend the boundary?

Partially, and non-monotonically:
- t=8: 0/5 at pop=10000 (worse than 1/5 at lower populations — likely noise)
- t=10–12: 0/5 (no improvement)
- t=15: **2/5 at pop=10000** despite 0/5 at pop=1k/2k/5k — a surprise
- t=20: 0/5 (no improvement)

The t=15 recovery at pop=10000 suggests the landscape is not uniformly harder at
higher terminal counts. At t=15, the additional diversity from a 10x larger population
occasionally allows the search to escape wrong-limit attractors. This effect is absent
at t=8–12 and t=20, where either the wrong-limit attractors are stronger or the
search space structure is qualitatively different.

### Summary

- Grid: 7 terminal counts × 4 pop sizes = 28 cells (21 new + 2 prior + 5 pop=10000 extra)
- Cells with ≥1 discovery: 11/28
- Clean discovery boundary: t ≤ 8 (at any tested population)
- Anomaly: t=15 recovers partially at pop=10000

The entropy information-theoretic fitness creates a search landscape where discovery
rate degrades as the terminal set grows. The primary driver is not population size
but terminal count: wrong-limit attractors that score better than Leibniz on finite
evaluation windows become more numerous and harder to escape as the search space grows.
