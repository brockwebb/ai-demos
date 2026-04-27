# CC Task: Monotonicity Threshold Sensitivity Sweep

**Date:** 2026-03-26
**Priority:** Medium (audit item 7 — could strengthen or weaken the paper)
**Compute budget:** ~4-5 hours total

---

## Objective

Test whether the monotonicity threshold values in both fitness functions affect discovery rates. Currently these are unjustified engineering choices:
- **Log-precision fitness:** `MIN_GAIN = 0.5` bits (consecutive checkpoints must gain ≥ 0.5 bits to count as monotonic)
- **Convergence-aware fitness:** 5% error reduction threshold (consecutive checkpoint pairs must show ≥ 5% error decrease)

## Experimental Design

### Sweep 1: Log-precision MIN_GAIN (4 values)

Run on **minimal terminals (t=4), pop=1000, 5 seeds, 360s/seed**.

| Config | MIN_GAIN value | Script base |
|---|---|---|
| baseline | 0.5 | entropy_leibniz_v3_minimal.py |
| low | 0.1 | fork |
| high | 1.0 | fork |
| very_high | 2.0 | fork |

### Sweep 2: Log-precision MIN_GAIN at boundary (2 values)

Run on **t=6 terminals, pop=1000, 5 seeds, 1800s/seed** (where baseline gets ~1/5).

| Config | MIN_GAIN value |
|---|---|
| baseline | 0.5 |
| low | 0.1 |

This tests whether the threshold matters at the boundary where discovery is fragile.

### Sweep 3: Convergence-aware convergence_bonus threshold (3 values)

Run on **minimal terminals (t=4), pop=1000, 5 seeds, 360s/seed**.

The convergence bonus threshold is the percentage error reduction required between consecutive checkpoints. Baseline is 5% (0.05).

| Config | Threshold | Script base |
|---|---|---|
| baseline | 0.05 (5%) | gp_leibniz_v3_minimal.py |
| low | 0.01 (1%) | fork |
| high | 0.20 (20%) | fork |

---

## Pre-Flight

1. Read `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py` — understand the fitness function, locate `MIN_GAIN`
2. Read `gp-leibniz-v3/gp_leibniz_v3_minimal.py` — understand convergence bonus, locate the threshold
3. Confirm both scripts run successfully with baseline params before forking

---

## Step 1: Create sweep scripts for log-precision MIN_GAIN

Create directory: `entropy-leibniz-v3/threshold_sweep/`

For each MIN_GAIN value (0.1, 1.0, 2.0), create a fork of `entropy_leibniz_v3_minimal.py`:

File naming: `threshold_sweep/logprec_mingain_{value}.py`

Changes from baseline:
- `MIN_GAIN = {value}` (instead of 0.5)
- Output filenames include the MIN_GAIN value: `threshold_mingain_{value}_data.json`, etc.
- All other parameters identical to baseline

---

## Step 2: Create sweep scripts for boundary test (t=6)

For the t=6 test, fork `entropy-leibniz-v3/scaling_heatmap.py` or create a standalone script based on `entropy_leibniz_v3_minimal.py` with:
- Terminal set for t=6: `{k, 1, -1, 2, 3, -2}`
- `MIN_GAIN = 0.1`
- `MAX_SEED = 1800.0` (scaling grid budget)
- Output: `threshold_sweep/logprec_mingain_0.1_t6_data.json`

Also run baseline (MIN_GAIN=0.5) at t=6 if not already available from scaling grid data. Check `scaling_heatmap_t6_p1000_data.json` first — if it exists with the right format, use that as the baseline comparison.

---

## Step 3: Create sweep scripts for convergence-aware threshold

Create directory: `gp-leibniz-v3/threshold_sweep/`

For each threshold value (0.01, 0.20), fork `gp_leibniz_v3_minimal.py`:

File naming: `threshold_sweep/convaware_thresh_{value}.py`

In the convergence bonus calculation, find the line that checks for 5% error reduction (likely something like `if error_ratio < 0.95:` or `if abs(e2) < abs(e1) * 0.95:`). Change the 0.95 to the appropriate value:
- threshold 0.01 → `0.99` (1% reduction)
- threshold 0.20 → `0.80` (20% reduction)

Output filenames include the threshold value.

---

## Step 4: Run all sweeps

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi

# Log-precision sweeps (t=4, ~30 min each)
python3 entropy-leibniz-v3/threshold_sweep/logprec_mingain_0.1.py
python3 entropy-leibniz-v3/threshold_sweep/logprec_mingain_1.0.py
python3 entropy-leibniz-v3/threshold_sweep/logprec_mingain_2.0.py

# Log-precision boundary test (t=6, ~2.5 hours)
python3 entropy-leibniz-v3/threshold_sweep/logprec_mingain_0.1_t6.py

# Convergence-aware sweeps (t=4, ~30 min each)
python3 gp-leibniz-v3/threshold_sweep/convaware_thresh_0.01.py
python3 gp-leibniz-v3/threshold_sweep/convaware_thresh_0.20.py
```

---

## Step 5: Collect results and write report

Create `entropy-leibniz-v3/threshold_sweep/threshold_sensitivity_results.md` with:

### Results table format:

```
| Fitness Function | Threshold Param | Value | t | Pop | Seeds Found | Mean Gens | Notes |
|---|---|---|---|---|---|---|---|
| Log-precision | MIN_GAIN | 0.1 | 4 | 1000 | ?/5 | ? | |
| Log-precision | MIN_GAIN | 0.5 (baseline) | 4 | 1000 | 5/5 | 2981 | from prior data |
| Log-precision | MIN_GAIN | 1.0 | 4 | 1000 | ?/5 | ? | |
| Log-precision | MIN_GAIN | 2.0 | 4 | 1000 | ?/5 | ? | |
| Log-precision | MIN_GAIN | 0.1 | 6 | 1000 | ?/5 | ? | |
| Log-precision | MIN_GAIN | 0.5 (baseline) | 6 | 1000 | 1/5 | ? | from scaling grid |
| Conv-aware | conv_threshold | 0.01 (1%) | 4 | 1000 | ?/5 | ? | |
| Conv-aware | conv_threshold | 0.05 (5%, baseline) | 4 | 1000 | 2/5 | ? | from prior data |
| Conv-aware | conv_threshold | 0.20 (20%) | 4 | 1000 | ?/5 | ? | |
```

### Analysis to include:

1. Does changing MIN_GAIN affect discovery rate at t=4? (Expect: no, since 5/5 is saturated)
2. Does changing MIN_GAIN affect discovery rate at t=6? (This is the interesting test)
3. Does changing convergence threshold affect discovery rate at t=4?
4. For any configuration where discovery changes: what expressions are found/not found?
5. Overall conclusion: "Discovery rates are [insensitive/sensitive] to threshold values within the tested range."

---

## Post-Flight

1. All raw data JSON files saved in the `threshold_sweep/` directories
2. Results report written
3. If results show insensitivity: draft a one-sentence addition for the paper
4. If results show sensitivity: flag for Brock — this needs discussion before paper changes

---

## Do NOT

- Do not modify any existing experiment scripts
- Do not modify any paper section files
- Do not overwrite any existing CC task files
- Do not change baseline parameters — only the specific threshold being swept
- Do not run experiments at t=15 (we already know nothing works there)
