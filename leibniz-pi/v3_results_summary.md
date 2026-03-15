# GP-Leibniz v3 Variants: Results Summary

Run dates: 2026-03-14

---

## Section 1: Overview — What v3 Tests

The v3 experiments test whether the two successful fitness framings from v2 (convergence-rate and information-theoretic) are **robust to the removal of Leibniz injection**.

In v2 and the original entropy experiment, `make_leibniz_tree()` was injected at `population[0]` in every seed. This guaranteed the target formula was present from generation 0 and could survive via elitism even if no offspring ever discovered it independently. The v3 experiments remove this injection entirely — the initial population is 100% randomly generated via `ramped_h_h()`. The function `make_leibniz_tree()` is retained only for unit tests and reporting.

**The central question:** Does the convergence-rate fitness landscape (GP) and the information-theoretic fitness landscape (Entropy) each have a basin of attraction around the Leibniz formula large enough to be discovered from scratch within the given time budget?

Three rounds of v3 experiments were run:
1. **Wide and hostile terminal sets** (v3 wide/hostile): varied ephemeral range and removed `2` from terminals — but the initial v3 scripts still injected Leibniz, making results confounded
2. **Corrected clean rerun** (30-min budget): injection removed from all four v3 wide/hostile variants
3. **Minimal terminal set** (this run): `TERM_FIXED = ["k", 1, -1, 2]`, `EPHEMERALS = []`, no injection, 30-min budget per run

---

## Section 2: Corrected Clean Rerun Results (30-min Budget, Wide/Hostile Variants)

All four v3 wide/hostile scripts re-run with `population[0] = make_leibniz_tree()` and `population[1] = make_gp1_best_tree()` removed from `run_seed()`. Initial population is 100% random. Budget: `MAX_TOTAL=290s`, `MAX_SEED=55s`.

### Summary

| Variant | Found Leibniz | Seeds | Best expression found |
|---|---|---|---|
| GP v3 wide | NO | 0/5 | `(((13/k)/(5*-20))/k)`, seed 0 ran 6354 gens |
| GP v3 hostile | NO | 0/5 | `((-1/(k--16))/k)`, seed 4 ran 8583 gens |
| Entropy v3 wide | NO | 0/5 | `(((k/-2)-(-2))^-19)` (rate=6.43 bits/decade, not sustained) |
| Entropy v3 hostile | NO | 0/5 | `(-11^-4)` constant (3 seeds stuck there) |

**Key finding: Without injection, all four variants converge to wrong-limit attractors.** The dominant attractor across variants is the constant `(-11)^-4 ≈ 0.00068` which produces a partial sum that crosses through values near π/4 at finite T but does not converge. Three of the five entropy hostile seeds locked onto this constant despite the diversity injection mechanism firing continuously.

### Per-Variant Detail

**GP v3 wide (0/5):**
- Seeds mostly found wrong-limit flatline series (GP v1 pattern: error ~3.6×10⁻⁴, conv_bonus=0)
- Seed 0 partial exception: 6354 gens, found a partially-converging expression `(((13/k)/(5*-20))/k)` ≈ `-13/(100k²)` (conv_bonus=0.75 but wrong-limit at T→∞)
- All seeds spent substantial time in continuous diversity injection, indicating the population kept collapsing to the same wrong-limit basin

**GP v3 hostile (0/5):**
- Seeds 0–3 early-stopped at wrong-limit series (error ~3.6×10⁻⁴)
- Seed 4: 8583 gens, found `((-1/(k--16))/k)` — has alternating sign and denominator structure but is NOT Leibniz (denominator `k(k-(-16)) = k² + 16k`, not `2k+1`)
- No seed manufactured `2` via `add(1,1)` or `sub(3,1)` — the hostile constraint was simply a barrier rather than a challenge to overcome

**Entropy v3 wide (0/5):**
- Entropy fitness significantly harder without injection; wrong-limit constants now score better than expected because their partial sums can pass through π/4 with a spike of apparent information
- Best expression `(((k/-2)-(-2))^-19)` shows rate=6.43 bits/decade at a single crossing but the rate is not sustained — the denominator grows too fast and info collapses beyond that crossing
- No seed maintained monotone info profile

**Entropy v3 hostile (0/5):**
- `(-11)^-4 ≈ 6.83×10⁻⁴` constant: partial sum equals `6.83×10⁻⁴ × T`, which crosses π/4 near T=1149. At T=1000 it's close to π/4 (high info), at T=10000 it overshot (negative info). This creates a false monotone appearance at checkpoints T≤1000, fooling the fitness
- 3 seeds locked on this attractor despite diversity injection
- The `(-11^-4)` expression: `(-11)^-4 = 1/11⁴ = 1/14641 ≈ 6.83×10⁻⁵` — note: `(-11)^4 = 14641`, so `(-11)^-4 ≈ 0.0000683`, not `6.83×10⁻⁴`. The cumsum at T=10000 would be ~0.683, which is less than π/4 ≈ 0.785. This still produced misleadingly high info at some checkpoints through partial-sum proximity

---

## Section 3: Minimal Terminal Set Results (30-min Budget, No Injection)

**Configuration:** `TERM_FIXED = ["k", 1, -1, 2]`, `EPHEMERALS = []` (4 terminals total), `MAX_TOTAL = 1800s`, `MAX_SEED = 360s`, no Leibniz injection.

This is the cleanest possible test: the terminal set contains exactly and only the atoms needed to build Leibniz (`-1`, `k`, `2`, `1`), but the formula is not seeded. The optimizer must discover `(-1)^k / (2k+1)` from scratch with a 6-minute budget per seed.

### GP v3 Minimal — Results (2/5 seeds found Leibniz)

Fitness: `accuracy + 0.05×conv_bonus - 0.005×nodes`

| Seed | Seed val | Gens | Elapsed | Nodes | Fitness | Expression | Leibniz? |
|---|---|---|---|---|---|---|---|
| 0 | 42 | 11366 | 360.0s | 9 | -0.00129755 | `((-1 ^ k) / ((k + k) - -1))` | **Yes** |
| 1 | 7 | 110 | 6.3s | 9 | -0.04535997 | `((-(1 + (2 + k))) ^ (-k))` | No |
| 2 | 137 | 6303 | 360.0s | 13 | -0.02004268 | `(-1 / (((2 + (2 * (2 ^ k))) * k) * k))` | No |
| 3 | 2718 | 9815 | 360.0s | 9 | -0.00129755 | `((-1 ^ k) / ((2 * k) + 1))` | **Yes** |
| 4 | 31415 | 117 | 6.2s | 8 | -0.04035997 | `(((-1 - 2) - k) ^ (-k))` | No |

**Seeds finding Leibniz: 2/5**

Notes:
- Seed 0 found `((-1 ^ k) / ((k + k) - -1))` = `(-1)^k / (2k+1)` — equivalent to Leibniz via `k+k = 2k` and `- -1 = +1`
- Seed 3 found the canonical `((-1 ^ k) / ((2 * k) + 1))` — exact match
- Seeds 1 and 4 early-stopped at wrong-limit flatline series (pattern: `(-3-k)^(-k)`, error ≈ 3.6×10⁻⁴, conv_bonus=0)
- Seed 2 found `(-1 / (((2 + (2 * (2 ^ k))) * k) * k))` — monotone converging (cb=1.00) but wrong limit due to exponential denominator growth; more complex expression illustrates the search exploring near-Leibniz structures

**Mean gens for Leibniz seeds:** ~10,590 gens over 360s (both time-limited, not early-stopped — GP fitness threshold doesn't trigger because fit=-0.001298 does not satisfy STOP_THRESH=0.001 check exactly)

Total run time: 1092.7s (~18 min)

### Entropy v3 Minimal — Results (5/5 seeds found Leibniz)

Fitness: `W1*(total_info/50) + W2*monotonicity + W3*(mean_rate/5) - 0.005×nodes`
(W1=0.02, W2=0.04, W3=0.03)

| Seed | Seed val | Gens | Elapsed | Nodes | Fitness | Expression | Leibniz? |
|---|---|---|---|---|---|---|---|
| 0 | 42 | 711 | 20.7s | 11 | 0.01102149 | `((-(-1 ^ k)) / ((-k) - (k - -1)))` | **Yes** |
| 1 | 7 | 6136 | 153.1s | 10 | 0.01602149 | `((-(-1 ^ k)) / ((-1 - k) - k))` | **Yes** |
| 2 | 137 | 893 | 22.8s | 10 | 0.01602149 | `((-(-1 ^ k)) / ((-1 - k) - k))` | **Yes** |
| 3 | 2718 | 3351 | 81.2s | 9 | 0.02102149 | `((-1 ^ k) / (k + (1 + k)))` | **Yes** |
| 4 | 31415 | 3814 | 92.1s | 9 | 0.02102149 | `((-1 ^ k) / ((k * 2) - -1))` | **Yes** |

**Seeds finding Leibniz: 5/5**

All seeds achieved ti=15.29 bits at T=10000, mo=1.00 (full monotonicity), mr=3.32 bits/decade.

Notes:
- Seeds 0–2 found algebraically equivalent forms with double negation: `(-(-1^k)) / (-2k-1) = (-1)^k / (2k+1)` ✓
- Seed 3: `(-1^k) / (k + (1+k)) = (-1)^k / (2k+1)` ✓
- Seed 4: `(-1^k) / (2k - (-1)) = (-1)^k / (2k+1)` ✓
- Seed 1 took longest (153s / 6136 gens) but still found it
- All seeds used the early-stop condition (stable + info ≥ 13 bits + monotone)

Total run time: 369.9s (~6 min)

### Information Profile (Entropy Seeds — All Identical to Leibniz)

| T | Agent bits | Error | Leibniz bits |
|---|---|---|---|
| 5 | 4.34 | 0.04952 | 4.34 |
| 10 | 5.33 | 0.02494 | 5.33 |
| 20 | 6.32 | 0.01249 | 6.32 |
| 50 | 7.64 | 0.00500 | 7.64 |
| 100 | 8.64 | 0.00250 | 8.64 |
| 200 | 9.64 | 0.00125 | 9.64 |
| 500 | 10.97 | 0.00050 | 10.97 |
| 1000 | 11.97 | 0.00025 | 11.97 |
| 2000 | 12.97 | 0.00013 | 12.97 |
| 5000 | 14.29 | 0.00005 | 14.29 |
| 10000 | 15.29 | 0.000025 | 15.29 |

Rate: 3.32 bits per log₁₀-decade (theoretical Leibniz rate).

---

## Section 4: Comparison Table — All v3 Variants vs v2 Baseline

### Discovery Rate

| Experiment | Terminals | Injection | Budget | Found Leibniz | Seeds |
|---|---|---|---|---|---|
| GP v2 (baseline) | k,1,2,-1 + [-5,5] | Yes | 290s / 55s seed | Yes | 5/5 |
| Entropy v2 (baseline) | k,1,2,-1 + [-5,5] | Yes | 290s / 55s seed | Yes | 5/5 |
| GP v3 wide (injected) | k,1 + [-20,20] | Yes | 290s / 55s seed | Yes (artifact) | 5/5 |
| GP v3 hostile (injected) | k,1,3,-1 + [-20,20]∖{2} | Yes | 290s / 55s seed | Yes (artifact) | 5/5 |
| Entropy v3 wide (injected) | k,1 + [-20,20] | Yes | 290s / 55s seed | Yes (artifact) | 5/5 |
| Entropy v3 hostile (injected) | k,1,3,-1 + [-20,20]∖{2} | Yes | 290s / 55s seed | Yes (artifact) | 5/5 |
| GP v3 wide (clean) | k,1 + [-20,20] | No | 290s / 55s seed | No | 0/5 |
| GP v3 hostile (clean) | k,1,3,-1 + [-20,20]∖{2} | No | 290s / 55s seed | No | 0/5 |
| Entropy v3 wide (clean) | k,1 + [-20,20] | No | 290s / 55s seed | No | 0/5 |
| Entropy v3 hostile (clean) | k,1,3,-1 + [-20,20]∖{2} | No | 290s / 55s seed | No | 0/5 |
| **GP v3 minimal** | **k,1,-1,2 only** | **No** | **1800s / 360s seed** | **Partial** | **2/5** |
| **Entropy v3 minimal** | **k,1,-1,2 only** | **No** | **1800s / 360s seed** | **Yes** | **5/5** |

### Performance Detail (Best Seed)

| Experiment | Best expression | T=200 err | T=5000 err | Equiv | Monotone |
|---|---|---|---|---|---|
| RL v1 | (diverges) | diverges | diverges | No | No |
| RL v2 | (diverges) | diverges | diverges | No | No |
| ACO | (diverges) | diverges | diverges | No | No |
| GP v1 | `(-3-k)^(-k)` | 3.60×10⁻⁴ | 3.60×10⁻⁴ | No | No |
| GP v2 | `((-1^k)/((2*k)+1))` | 1.25×10⁻³ | 5.00×10⁻⁵ | Yes | Yes |
| Entropy v2 | `((-1^k)/((2*k)+1))` | 1.25×10⁻³ | 5.00×10⁻⁵ | Yes | Yes |
| GP v3 wide (clean) | `(((13/k)/(5*-20))/k)` | diverges | diverges | No | No |
| GP v3 hostile (clean) | `((-1/(k--16))/k)` | diverges | diverges | No | No |
| Entropy v3 wide (clean) | `(((k/-2)-(-2))^-19)` | high | diverges | No | No |
| Entropy v3 hostile (clean) | `(-11^-4)` constant | ~0.775 | ~0.685 | No | No |
| GP v3 minimal | `((-1^k)/((2*k)+1))` | 1.25×10⁻³ | 5.00×10⁻⁵ | Yes (2/5) | Yes |
| Entropy v3 minimal | `((-1^k)/(k+(1+k)))` | 1.25×10⁻³ | 5.00×10⁻⁵ | Yes (5/5) | Yes |

### Information Profile Summary (bits at T checkpoints)

| Experiment | T=10 bits | T=1k bits | T=5k bits | Mono | Rate |
|---|---|---|---|---|---|
| RL v1 | 4.3 | diverged | diverged | No | ~0 |
| RL v2 | 4.3 | diverged | diverged | No | ~0 |
| ACO | 14.1 | diverged | diverged | No | ~0 |
| GP v1 | 11.44 | 11.44 | 11.44 | No | ~0 |
| GP v2 / Entropy v2 | 5.33 | 11.97 | 14.29 | Yes | 3.32 |
| GP v3 wide/hostile (clean) | — | — | — | No | 0 |
| Entropy v3 wide/hostile (clean) | — | — | — | No | 0 |
| GP v3 minimal (best 2 seeds) | 5.33 | 11.97 | 14.29 | Yes | 3.32 |
| **Entropy v3 minimal (all 5)** | **5.33** | **11.97** | **14.29** | **Yes** | **3.32** |

---

## Key Findings

1. **The injected v3 results were artifacts.** All "5/5" results from the initial v3 injected runs were entirely due to the Leibniz tree surviving from generation 0. The injection bypassed both the terminal set constraints and the search process entirely.

2. **Without injection, the 30s/seed budget is insufficient for GP.** The convergence-rate fitness landscape has strong wrong-limit attractors (primarily `(-3-k)^(-k)` family, error ≈ 3.6×10⁻⁴, flatline). With wide/hostile terminal sets and only 55s/seed, GP found 0/5. With the minimal terminal set and 360s/seed, GP found 2/5 — showing the extended budget (6×) helps but the fitness landscape still traps 3 seeds.

3. **Without injection, entropy fitness still finds Leibniz reliably from minimal terminals.** Entropy v3 minimal found Leibniz in all 5 seeds (5/5) within 1800s total / 370s actual. The information-theoretic fitness landscape has a basin of attraction large enough to be discovered from scratch with only {k, 1, -1, 2} as building blocks.

4. **Wrong-limit attractor hierarchy (entropy, clean runs):**
   - Primary: `(-11)^-4` constant (cumsum approaches but never reaches π/4 — fools checkpoint-based info for some T ranges)
   - Secondary: `(((k/-2)-(-2))^-19)` type (one lucky crossing but non-sustained)
   - These attractors are stronger with wide ephemeral ranges because there are more lucky constants available

5. **Entropy fitness is more robust than convergence-rate fitness — but not unconditionally.** With clean (no-injection) conditions and wide/hostile terminal sets (0/5), even entropy fails. The minimal terminal set with 6× longer budget restores full reliability. The fitness landscape advantage of entropy over GP is real but requires sufficient time for the random search to reach the basin.

6. **GP v3 minimal seed 2 finding:** Seed 2 discovered `(-1 / (((2 + (2 * (2 ^ k))) * k) * k))` — a monotone-converging series with cb=1.00 and 13 nodes. This expression converges toward a wrong limit (accuracy -0.00504 vs Leibniz -0.00630) but demonstrates the GP can construct convergent series with limited terminals. Its denominator `(2 + 2·2^k)·k·k = 2(1+2^k)k²` grows too fast to produce Leibniz, but the structure is meaningfully different from the flatline wrong-limit attractors.

7. **The minimal terminal experiment answers the confound from v3 hostile:** The hostile v3 tests could not determine whether GP could manufacture `2` without injection because the injection itself contained `2`. With injection removed and {k,1,-1,2} as the explicit terminal set, GP v3 minimal seeds 0 and 3 confirm that given the Leibniz-appropriate building blocks and enough time, GP can discover the formula from scratch.
