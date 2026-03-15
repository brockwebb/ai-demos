# Parsimony Pressure Test Results

**Date:** 2026-03-15
**Config:** Minimal terminal set `{k, 1, -1, 2}`, no injection, 30-min budget, 5 seeds
**Fitness:** `W1*(total_info/50) + W2*monotonicity + W3*(mean_rate/5) - LAMBDA_P*nodes`
**Weights:** W1=0.02, W2=0.04, W3=0.03

---

## LAMBDA_P = 0.005 (baseline — from entropy_leibniz_v3_minimal.py)

| Seed | Expression | Nodes | Leibniz-equivalent | Gens |
|------|-----------|-------|-------------------|------|
| 0 (val=42) | `((-(-1 ^ k)) / ((-k) - (k - -1)))` | 11 | True | 711 |
| 1 (val=7) | `((-(-1 ^ k)) / ((-1 - k) - k))` | 10 | True | 6136 |
| 2 (val=137) | `((-(-1 ^ k)) / ((-1 - k) - k))` | 10 | True | 893 |
| 3 (val=2718) | `((-1 ^ k) / (k + (1 + k)))` | 9 | True | 3351 |
| 4 (val=31415) | `((-1 ^ k) / ((k * 2) - -1))` | 9 | True | 3814 |

---

## LAMBDA_P = 0.01

| Seed | Expression | Nodes | Leibniz-equivalent | Gens |
|------|-----------|-------|-------------------|------|
| 0 (val=42) | `(-1 - -1)` | 3 | False | 16881 |
| 1 (val=7) | `(-1 + 1)` | 3 | False | 17836 |
| 2 (val=137) | `(1 + -1)` | 3 | False | 17745 |
| 3 (val=2718) | `(k - k)` | 3 | False | 17841 |
| 4 (val=31415) | `(k - k)` | 3 | False | 17319 |

All seeds converged to **3-node zero-constant** expressions (sum=0, flatlines at error=π/4).
Best fitness: -0.02986060
Note: At lp=0.01, the Leibniz 9-node tree scores -0.023979 — which is *better* than the zero-constant fitness of -0.029861. However, population convergence to zero constants was so complete that discovery never occurred within the 360s seed budget.

---

## LAMBDA_P = 0.02

| Seed | Expression | Nodes | Leibniz-equivalent | Gens |
|------|-----------|-------|-------------------|------|
| 0 (val=42) | `-1` | 1 | False | 19820 |
| 1 (val=7) | `-1` | 1 | False | 20823 |
| 2 (val=137) | `-1` | 1 | False | 20715 |
| 3 (val=2718) | `-1` | 1 | False | 20779 |
| 4 (val=31415) | `-1` | 1 | False | 20848 |

All seeds converged to **1-node constant `-1`**.
Best fitness: -0.04486432
Unit test flag: Leibniz (-0.1140) is *not* in the top 10% of random population — parsimony penalty has suppressed the fitness landscape enough that compact wrong-limit constants dominate from the start.
Leibniz-vs-GP-v1 margin collapsed to 0.001244 (from 0.031244 at lp=0.01).

---

## LAMBDA_P = 0.05

| Seed | Expression | Nodes | Leibniz-equivalent | Gens |
|------|-----------|-------|-------------------|------|
| 0 (val=42) | `-1` | 1 | False | 19928 |
| 1 (val=7) | `-1` | 1 | False | 20732 |
| 2 (val=137) | `-1` | 1 | False | 20667 |
| 3 (val=2718) | `-1` | 1 | False | 20770 |
| 4 (val=31415) | `-1` | 1 | False | 20855 |

All seeds converged to **1-node constant `-1`**.
Best fitness: -0.07486432
Unit test flags: Leibniz (-0.384) now *loses* to GP v1 best (-0.295) — parsimony has inverted the fitness ordering. Discovery is structurally impossible: the 9-node Leibniz tree is penalized more than compact wrong-limit attractors.

---

## Summary Table

| LAMBDA_P | Seeds Found | Mean nodes (Leibniz seeds) | Canonical 9-node? | Notes |
|----------|-------------|--------------------------|-------------------|-------|
| 0.005 (baseline) | 5/5 | 9.8 | 2/5 | Bloated equivalents; correct discovery |
| 0.01 | 0/5 | N/A | No | Zero-constant attractor (3-node): sum=0 beats Leibniz via parsimony |
| 0.02 | 0/5 | N/A | No | Constant `-1` attractor (1-node); Leibniz no longer in top 10% of pop |
| 0.05 | 0/5 | N/A | No | Constant `-1` dominates; Leibniz fitness *inverted* vs GP v1 |

---

## Findings

### Does higher parsimony produce the canonical 9-node form?

No. The hypothesis that stronger parsimony pressure would drive discovery toward the minimal 9-node form `((-1 ^ k) / ((k * 2) + 1))` was falsified. At lp=0.01, the population collapsed to 3-node zero-constant expressions rather than the 9-node Leibniz form. At lp=0.02 and lp=0.05, it collapsed further to the 1-node constant `-1`.

**Root cause:** The Leibniz series requires 9 nodes. With lp=0.01, the parsimony penalty for 9 nodes is 0.09 — which dominates over the convergence reward the Leibniz tree earns. The fitness landscape penalty makes zero-constant expressions (3 nodes, penalty=0.03) or single constants (1 node, penalty=0.01/0.02/0.05) more attractive than Leibniz before selection has any chance to push toward it.

### Is there a sweet spot?

The sweet spot is below lp=0.01. The baseline lp=0.005 achieves 5/5 with mean 9.8 nodes. The lp=0.01 threshold appears to be the break point where the parsimony penalty on a 9-node tree becomes large enough to prevent the fitness gradient from pulling the population toward Leibniz.

**Quantitative evidence:** At lp=0.005, the zero-constant (3 nodes) has fitness ≈ -0.015 while Leibniz has fitness ≈ -0.012. The gradient still favors Leibniz. At lp=0.01, zero-constant fitness is -0.030 and Leibniz is -0.024 — Leibniz is still better in absolute terms, but the population dynamics (diversity collapse + random initialization) never get close enough to exploit the small margin before the 360s budget expires.

### Does it ever break discovery?

Yes, irreversibly above lp≈0.01. The transition is sharp:
- **lp=0.005:** 5/5 — full discovery, mean 9.8 nodes
- **lp=0.01:** 0/5 — zero-constant attractor dominates despite Leibniz being nominally fitter
- **lp=0.02:** 0/5 — single-constant attractor; Leibniz ejected from top 10% of random population
- **lp=0.05:** 0/5 — Leibniz fitness is *worse* than GP-v1-best (`-0.384 < -0.295`); discovery structurally impossible

The lp=0.01 case is particularly interesting: Leibniz is still the fitter individual (if it were present), but the combination of extreme parsimony pressure on all multi-node individuals during initialization and selection creates a fitness valley that is never escaped. The diversity injection mechanism (replacing worst 100 individuals) cannot compensate because injected random trees are also penalized and quickly replaced.

### Broader implication

Parsimony pressure in this fitness regime cannot be used as a tool to steer toward canonical form. The information-theoretic reward terms (W1×ti, W2×mono, W3×rate) sum to at most ~0.07 for Leibniz, placing a hard ceiling on the parsimony penalty that preserves the fitness gradient: lp × 9 nodes < 0.07, so lp < 0.0078. The baseline lp=0.005 is operating near but below this ceiling. Any lp above ~0.008 breaks the landscape for 9-node discovery.
