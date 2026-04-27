# Threshold Sensitivity Results
**Date:** 2026-03-26
**Status:** Sweeps 1 and 3 complete. Sweep 2 (t=6 boundary test) still running.

---

## Results Table

| Fitness Function | Threshold Param | Value | t | Pop | Seeds Found | Notes |
|---|---|---|---|---|---|---|
| Log-precision | MIN_GAIN | 0.1 | 4 | 1000 | 2/5 | lower than baseline — reduced selectivity |
| Log-precision | MIN_GAIN | 0.5 (baseline) | 4 | 1000 | 5/5 | from prior data |
| Log-precision | MIN_GAIN | 1.0 | 4 | 1000 | 1/5 | higher than baseline — too strict |
| Log-precision | MIN_GAIN | 2.0 | 4 | 1000 | 0/5 | fitness collapses to trivial expressions |
| Log-precision | MIN_GAIN | 0.1 | 6 | 1000 | (running) | ~2.5h; background PID 85063 |
| Log-precision | MIN_GAIN | 0.5 (baseline) | 6 | 1000 | 1/5 | from scaling grid data |
| Conv-aware | conv_threshold | 0.01 (1%) | 4 | 1000 | 3/5 | slightly higher than baseline |
| Conv-aware | conv_threshold | 0.05 (5%, baseline) | 4 | 1000 | 2/5 | from prior data |
| Conv-aware | conv_threshold | 0.20 (20%) | 4 | 1000 | 2/5 | same as baseline |

---

## Per-Seed Details

### Log-precision MIN_GAIN=0.1 (t=4)
- Seed 0 (val=42): **equiv=True** — `((-1 ^ k) / (1 + (k + k)))`
- Seed 1 (val=7): **equiv=True** — `((-1 ^ k) / ((k + 1) + k))`
- Seed 2 (val=137): equiv=False — `(-(((1 / ((2 - k) * 2)) / 2) / 2))`
- Seed 3 (val=2718): equiv=False — `(((((2 ^ 2) * 2) * k) - 2) ^ -1)`
- Seed 4 (val=31415): equiv=False — `(((2 / k) - k) ^ ((k ^ k) - 2))`

### Log-precision MIN_GAIN=1.0 (t=4)
- Seed 0 (val=42): equiv=False — `(-(-1 ^ k))`
- Seed 1 (val=7): **equiv=True** — `((-(-1 ^ k)) / (-1 - (k + k)))`
- Seed 2 (val=137): equiv=False — `(2 / ((2 + k) * (1 - k)))`
- Seed 3 (val=2718): equiv=False — `(-1 / (((2 / k) + k) * (1 - k)))`
- Seed 4 (val=31415): equiv=False — `(2 / ((2 + k) * (1 - k)))`

### Log-precision MIN_GAIN=2.0 (t=4)
All 5 seeds: equiv=False. Best expressions are trivial constants: `(-1 - -1)`, `(-1 + 1)`, `(1 + -1)`, `(k - k)`. Fitness collapsed to near-zero expressions (W2 term contributes 0 because Leibniz's ~1.0 bit/step gain never reaches 2.0 bit threshold). The fitness function no longer discriminates meaningfully.

### Convergence-aware thresh=0.01 (1%, CONV_THRESHOLD=0.99)
- Seed 0 (val=42): **equiv=True** — `((-1 ^ k) / ((k + k) - -1))`
- Seed 1 (val=7): equiv=False — `((((2 + k) + (1 / 2)) / (-k)) ^ (-k))`
- Seed 2 (val=137): **equiv=True** — `(((1 + (2 * k)) * (-1 ^ k)) ^ -1)`
- Seed 3 (val=2718): **equiv=True** — `((-1 ^ k) / (k + (k - -1)))`
- Seed 4 (val=31415): equiv=False — `((-1 / 2) / ((k + k) * (k * 2)))`

### Convergence-aware thresh=0.20 (20%, CONV_THRESHOLD=0.80)
- Seed 0 (val=42): **equiv=True** — `((-1 ^ k) / ((k + k) - -1))`
- Seed 1 (val=7): equiv=False — `((-1 - (k + (2 ^ (-k)))) ^ (-2))`
- Seed 2 (val=137): **equiv=True** — `((-1 ^ k) / (1 + (k * 2)))`
- Seed 3 (val=2718): equiv=False — `((1 - k) ^ (-1 - 2))`
- Seed 4 (val=31415): equiv=False — `(((-1 - 2) - k) ^ (-k))`

---

## Analysis

### 1. Does changing MIN_GAIN affect discovery rate at t=4?

**Yes — and strongly.** Discovery is NOT insensitive to MIN_GAIN.

The baseline value of 0.5 appears near-optimal for this problem:
- MIN_GAIN=0.1 (lower): 2/5. Reduced selectivity — the monotonicity score is easier for wrong-limit attractors to achieve, weakening selection pressure toward Leibniz.
- MIN_GAIN=0.5 (baseline): 5/5.
- MIN_GAIN=1.0 (higher): 1/5. Leibniz gains approximately 1.0 bit per checkpoint step, so MIN_GAIN=1.0 is at the edge of what Leibniz satisfies. Partial monotonicity credit; fitness landscape is flatter.
- MIN_GAIN=2.0 (very high): 0/5. Leibniz never achieves 2.0 bit gain per step. W2 (monotonicity) term contributes zero for Leibniz. The fitness collapses to trivial zero expressions that minimize parsimony. Discovery is impossible because Leibniz has no advantage.

**Implication for paper:** The paper's choice of MIN_GAIN=0.5 is not arbitrary. It is calibrated to Leibniz's natural gain rate (~1.0 bit/step). Values below 0.5 reduce selectivity; values above Leibniz's actual gain rate destroy the signal. The parameter sits in a meaningful range relative to the physics of the problem. This should be documented.

### 2. Does changing MIN_GAIN affect discovery rate at t=6? (Boundary test — still running)

Results pending. See `logprec_mingain_0.1_t6_data.json` when complete.
Baseline: 1/5 (from scaling_heatmap_t6_p1000_data.json).

### 3. Does changing convergence threshold affect discovery rate at t=4?

**Modestly — within 1 seed of baseline.** The 5-seed sample is too small to distinguish 2/5 vs 3/5 statistically, but the qualitative pattern is:
- threshold=0.01 (1%): 3/5 — slightly easier requirement, marginally more seeds succeed
- threshold=0.05 (5%, baseline): 2/5
- threshold=0.20 (20%): 2/5 — more stringent requirement, same result

The convergence-aware fitness appears relatively insensitive to this threshold within the tested range. The 5% vs 1% difference does not change which expressions win the search (seeds 0 and 2 find Leibniz in both cases; the 3rd success at threshold=0.01 comes from seed 3 which just barely converges).

### 4. Expressions found: any qualitative differences?

All Leibniz-equivalent expressions found across all sweeps are structurally correct variants of (-1)^k / (2k+1), as expected. No novel alternative series were discovered. Wrong-limit attractors appear consistently when discovery fails.

### 5. Overall conclusion

**Log-precision MIN_GAIN: Sensitive.** The threshold must be calibrated to the target's gain rate. Too low → reduced selectivity, wrong attractors compete with Leibniz. Too high (exceeding Leibniz's gain rate) → W2 term contributes 0 for Leibniz, fitness collapses.

**Convergence-aware threshold: Insensitive** within the tested range (1%–20%). Discovery rates vary by at most 1 seed (within noise for 5 seeds).

---

## Draft sentence for paper (if appropriate)

For Methods §3.3.2 (if sensitivity is notable):
> The monotonicity threshold (MIN_GAIN=0.5 bits) is calibrated to Leibniz's natural precision gain rate of approximately 1.0 bit per checkpoint step. Values below 0.5 reduce selectivity by allowing wrong-limit attractors to achieve full monotonicity credit; values above 1.0 eliminate the signal because Leibniz itself fails the criterion.

**Flag for Brock:** The sensitivity result is stronger than expected. MIN_GAIN is not a free parameter — it is physically meaningful relative to Leibniz's convergence rate. The paper currently treats it as a hyper-parameter without justification. This result provides that justification and may warrant a sentence in Methods or Discussion.

---

## Files

- `threshold_mingain_0.1_data.json` — MIN_GAIN=0.1, t=4 raw data
- `threshold_mingain_0.1_results.txt` — MIN_GAIN=0.1, t=4 TEVV report
- `threshold_mingain_1.0_data.json` — MIN_GAIN=1.0, t=4 raw data
- `threshold_mingain_1.0_results.txt` — MIN_GAIN=1.0, t=4 TEVV report
- `threshold_mingain_2.0_data.json` — MIN_GAIN=2.0, t=4 raw data
- `threshold_mingain_2.0_results.txt` — MIN_GAIN=2.0, t=4 TEVV report
- `threshold_mingain_0.1_t6_data.json` — MIN_GAIN=0.1, t=6 raw data (when complete)
- `threshold_mingain_0.1_t6_results.txt` — MIN_GAIN=0.1, t=6 TEVV report (when complete)
- `threshold_mingain_0.1_t6_log.txt` — stdout log for background run

Convergence-aware data in `gp-leibniz-v3/threshold_sweep/`:
- `threshold_convaware_0.01_data.json`
- `threshold_convaware_0.01_results.txt`
- `threshold_convaware_0.20_data.json`
- `threshold_convaware_0.20_results.txt`
