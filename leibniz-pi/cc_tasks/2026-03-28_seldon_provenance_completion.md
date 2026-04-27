# CC Task: Complete Seldon Provenance for All Incomplete Artifacts

**Date:** 2026-03-28
**Scope:** Register DataFile artifacts and create GENERATED_BY / COMPUTED_FROM links for all 41 incomplete-provenance items

---

## Pre-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon status
seldon artifact list --type Result --state proposed 2>/dev/null || true
seldon result list 2>/dev/null | head -50
```

Understand the current state before making changes. The goal is to complete provenance chains so every Result artifact has:
- GENERATED_BY → Script (the Python script that produced the data)
- The Script has COMPUTED_FROM → DataFile (the JSON/CSV output file containing the raw value)

---

## Context: What Needs Provenance

There are 41 Result artifacts with incomplete provenance. They fall into these groups:

### Group 1: Scaling Heatmap Grid (28 results)

Discovery counts at each terminal×population combination.

**Script:** `entropy-leibniz-v3/scaling_heatmap.py`
**Data files:** `entropy-leibniz-v3/scaling_heatmap_t{T}_p{POP}_data.json` for each cell

| Terminals | Populations | Data File Pattern |
|-----------|-------------|-------------------|
| 4 | 1000, 2000, 5000, 10000 | `scaling_heatmap_t4_p{POP}_data.json` |
| 6 | 1000, 2000, 5000, 10000 | `scaling_heatmap_t6_p{POP}_data.json` |
| 8 | 1000, 2000, 5000, 10000 | `scaling_heatmap_t8_p{POP}_data.json` |
| 10 | 1000, 2000, 5000, 10000 | `scaling_heatmap_t10_p{POP}_data.json` |
| 12 | 1000, 2000, 5000, 10000 | `scaling_heatmap_t12_p{POP}_data.json` |
| 15 | 2000, 5000, 10000 | `scaling_heatmap_t15_p{POP}_data.json` |
| 20 | 1000, 2000, 5000, 10000 | `scaling_heatmap_t20_p{POP}_data.json` |

Note: t=15 p=1000 may use the baseline experiment data from `entropy-leibniz-v3/entropy_data_hostile.json` or similar. Check which file contains that cell's data.

For each of the 28 Result artifacts:
1. If the DataFile artifact for the corresponding `_data.json` does not exist, register it:
   ```bash
   seldon artifact create --type DataFile --name "scaling_heatmap_t{T}_p{POP}_data" --path "entropy-leibniz-v3/scaling_heatmap_t{T}_p{POP}_data.json"
   ```
2. If the Script artifact for `scaling_heatmap.py` does not exist, register it:
   ```bash
   seldon artifact create --type Script --name "scaling_heatmap_script" --path "entropy-leibniz-v3/scaling_heatmap.py"
   ```
3. Create provenance links:
   ```bash
   seldon link create --from {RESULT_ID} --to {SCRIPT_ID} --type GENERATED_BY
   seldon link create --from {SCRIPT_ID} --to {DATAFILE_ID} --type COMPUTED_FROM
   ```

### Group 2: Parsimony Analysis (3 results)

Values: 0.021021 (baseline λ_p=0.005), -0.023979 (λ_p=0.01), -0.029861 (zero-constant at λ_p=0.01)

**Script:** `entropy-leibniz-v3/parsimony_test.py`
**Data files:** `entropy-leibniz-v3/parsimony_lp0.01_data.json` and the baseline experiment data

For each:
1. Register DataFile artifacts for the parsimony data files if not present
2. Register Script artifact for `parsimony_test.py` if not present
3. Create GENERATED_BY and COMPUTED_FROM links

### Group 3: Grandi-Leibniz Attractor (2 results)

Values: precision=0.0733 at T=5, mean_rate=4.609

**Source data:** `entropy-leibniz-v3/scaling_heatmap_t4_p2000_data.json` (the Grandi-Leibniz attractor appeared in seed 31415 of this cell)
**Script:** `entropy-leibniz-v3/scaling_heatmap.py`

Link these to the same script and data file as the t4_p2000 scaling heatmap result.

### Group 4: Extended Time Test (1 result)

Value: 1.0 (1/5 seeds at t=10, pop=5000, 7200s budget)

**Script:** `gp-leibniz-v3/gp_extended_t10_p5000.py`
**Data files:** Check `gp-leibniz-v3/results_gp_extended_t10_p5000/` directory for JSON data

Register script and data file, create links.

### Group 5: Leibniz Precision Checkpoints (2 results)

Values: 4.34 bits at T=5, 5.33 bits at T=10

These are computed values from the Leibniz series itself -- they may come from the fitness function implementation rather than a specific experiment output. Check if they are derived from `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py` or computed analytically. If analytical, the "script" is the fitness function code.

**Script:** `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py` (most likely source)
**Data:** `entropy-leibniz-v3/entropy_data_minimal.json`

### Group 6: Threshold Sensitivity Sweep (4 results)

Values at MIN_GAIN = 0.1/1.0/2.0 (t=4, pop=1000) and MIN_GAIN=0.1 (t=6, pop=1000)

**Scripts:** `entropy-leibniz-v3/threshold_sweep/logprec_mingain_{GAIN}.py` and `logprec_mingain_0.1_t6.py`
**Data files:** `entropy-leibniz-v3/threshold_sweep/threshold_mingain_{GAIN}_data.json` and `threshold_mingain_0.1_t6_data.json`

For each:
1. Register DataFile for each `_data.json`
2. Register Script for each `.py`
3. Create GENERATED_BY and COMPUTED_FROM links

### Group 7: Log-Precision Fitness Ceiling (1 result)

Value: 0.066021 (sum of fitness terms for canonical 9-node Leibniz)

This is a derived/analytical value. Check if it was computed by a script or derived manually. If computed, find the script. If analytical, document the derivation in the artifact description and link to the fitness function source code.

Most likely source: `entropy-leibniz-v3/parsimony_test.py` or computed inline during parsimony analysis.

---

## Execution Strategy

1. First, list all existing artifacts to avoid duplicates:
   ```bash
   seldon artifact list --type Script
   seldon artifact list --type DataFile
   seldon artifact list --type Result
   ```

2. For each group, check which Script and DataFile artifacts already exist before creating new ones.

3. Work through groups 1-7 in order. For each Result artifact:
   - Find its Seldon ID (from `seldon result list` or `seldon artifact list --type Result`)
   - Find or create the Script artifact
   - Find or create the DataFile artifact
   - Create the GENERATED_BY link (Result → Script)
   - Create the COMPUTED_FROM link (Script → DataFile)

4. Verify after completion:
   ```bash
   seldon status
   ```
   The "Incomplete Provenance" count should drop from 41 to 0 (or near 0 if some are genuinely analytical).

---

## Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon status
seldon result list
```

Verify:
1. Incomplete provenance count is 0 or near 0
2. All Result artifacts have GENERATED_BY links
3. All Script artifacts have COMPUTED_FROM links to DataFiles
4. No new stale artifacts introduced

Report the final status summary.

---

## Do NOT

- Do not modify any experiment scripts or data files
- Do not rerun any experiments
- Do not modify any paper section files
- Do not modify existing CC task files
- Do not delete any artifacts -- only create new ones and add links
- Do not change Result values -- only add provenance links
- Do not guess at provenance -- if a source file cannot be identified, flag it and skip
