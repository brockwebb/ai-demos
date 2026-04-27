# CC Task: Add Threshold Sensitivity Results to Paper

**Date:** 2026-03-26
**Priority:** High (new finding from audit)
**Depends on:** Threshold sweep results in `entropy-leibniz-v3/threshold_sweep/threshold_sensitivity_results.md`

---

## Objective

Add the MIN_GAIN threshold sensitivity finding to the paper. This is a meaningful result: the log-precision fitness threshold is not an arbitrary engineering choice but is physically constrained by Leibniz's convergence rate.

---

## Pre-Flight

1. Read `paper/conventions.md`
2. Read `entropy-leibniz-v3/threshold_sweep/threshold_sensitivity_results.md` for the full results
3. Check if the t=6 boundary test has completed. Look for `entropy-leibniz-v3/threshold_sweep/threshold_mingain_0.1_t6_data.json`. If it exists and is non-empty, read `threshold_mingain_0.1_t6_results.txt` for the result and incorporate it.
4. Read each section file BEFORE editing it

---

## Step 1: Add threshold sensitivity table and paragraph to Section 5 (05_results.md)

Read `paper/sections/05_results.md`.

Add a new subsection **5.6 Threshold Sensitivity** after Section 5.5. Content:

```
## 5.6 Threshold Sensitivity

The log-precision fitness uses a monotonicity threshold (MIN_GAIN) that defines how many bits of precision gain a checkpoint pair must show to count as monotonically improving. The baseline value of 0.5 bits was a design choice. We tested whether discovery rates depend on this threshold.

**Table 8:** Log-precision monotonicity threshold sensitivity at t=4, pop=1,000. Leibniz gains approximately 1.0 bit per checkpoint step.

| MIN_GAIN (bits) | Seeds Found | Notes |
|---|---|---|
| 0.1 | 2/5 | Too permissive: wrong-limit attractors achieve full monotonicity credit |
| 0.5 (baseline) | 5/5 | Below Leibniz's natural gain rate |
| 1.0 | 1/5 | At Leibniz's gain rate: Leibniz barely qualifies |
| 2.0 | 0/5 | Above Leibniz's gain rate: fitness collapses to trivial constants |

The threshold is not a free parameter. It must be set below the target process's natural precision gain rate. Leibniz gains approximately 1.0 bit per checkpoint step. At MIN_GAIN=0.5, the threshold is comfortably below this rate, and all seeds succeed. At MIN_GAIN=1.0, Leibniz itself barely satisfies the criterion, and discovery drops to 1/5. At MIN_GAIN=2.0, Leibniz never achieves the required gain, the W_2 (monotonicity) term contributes zero, and the fitness collapses to trivial zero-constant expressions.

The convergence-aware fitness threshold (5% error reduction between checkpoints) is less sensitive. Varying the threshold from 1% to 20% produced discovery rates between 2/5 and 3/5, within noise for a five-seed sample.

This sensitivity confirms that the log-precision fitness encodes domain knowledge about the target process's convergence rate. The threshold is constrained by the physics of the problem, not freely tunable.
```

If the t=6 boundary test is complete, add one additional sentence after the table:

If MIN_GAIN=0.1 at t=6 produces a DIFFERENT result than baseline (1/5):
```
At the phase transition boundary (t=6), reducing MIN_GAIN to 0.1 [increased/decreased] discovery from 1/5 to [N]/5, [confirming that the threshold also affects the location of the phase transition / suggesting the threshold effect is limited to the reliable-discovery regime].
```

If MIN_GAIN=0.1 at t=6 produces the SAME result (1/5):
```
At the phase transition boundary (t=6), reducing MIN_GAIN to 0.1 did not change the discovery rate (1/5), suggesting the threshold matters only in the regime where coverage is sufficient.
```

---

## Step 2: Add context sentence to Section 3.3.2 (03_methods.md)

Read `paper/sections/03_methods.md`.

In Section 3.3.2, find the sentence:
```
where monotonicity = fraction of consecutive checkpoints with ≥ 0.5 bit gain
```

Add a parenthetical or follow-up sentence. Change to:
```
where monotonicity = fraction of consecutive checkpoints with ≥ 0.5 bit gain (this threshold is calibrated to Leibniz's natural gain rate; see Section 5.6 for sensitivity analysis)
```

---

## Step 3: Connect to design provenance in Section 6.5 (06_discussion.md)

Read `paper/sections/06_discussion.md`.

In Section 6.5 (Design Provenance and Disciplinary Lens), find the sentence:
```
That question, not the specific mathematical form of the fitness, is the transferable contribution.
```

Add before that sentence:
```
The threshold sensitivity analysis (Section 5.6) reinforces this point: the monotonicity threshold is not a free hyperparameter but is constrained by the convergence rate of the target process.
```

---

## Step 4: Register new results with Seldon

Register the threshold sensitivity results:

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi

# Register key results from the sweep
seldon result register --name "threshold_mingain_0.1_t4" --value "2" \
  --units "seeds_discovered" \
  --description "Log-precision discovery at MIN_GAIN=0.1, t=4, pop=1000. 2/5 seeds. Threshold too permissive." \
  --source "entropy-leibniz-v3/threshold_sweep/threshold_mingain_0.1_data.json"

seldon result register --name "threshold_mingain_1.0_t4" --value "1" \
  --units "seeds_discovered" \
  --description "Log-precision discovery at MIN_GAIN=1.0, t=4, pop=1000. 1/5 seeds. Threshold at Leibniz gain rate edge." \
  --source "entropy-leibniz-v3/threshold_sweep/threshold_mingain_1.0_data.json"

seldon result register --name "threshold_mingain_2.0_t4" --value "0" \
  --units "seeds_discovered" \
  --description "Log-precision discovery at MIN_GAIN=2.0, t=4, pop=1000. 0/5 seeds. Threshold exceeds Leibniz gain rate, fitness collapses." \
  --source "entropy-leibniz-v3/threshold_sweep/threshold_mingain_2.0_data.json"
```

If the t=6 result is available, also register:
```bash
seldon result register --name "threshold_mingain_0.1_t6" --value "VALUE" \
  --units "seeds_discovered" \
  --description "Log-precision discovery at MIN_GAIN=0.1, t=6, pop=1000. VALUE/5 seeds. Boundary test." \
  --source "entropy-leibniz-v3/threshold_sweep/threshold_mingain_0.1_t6_data.json"
```

---

## Post-Flight

1. Run: `cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi && python paper/prose_qc.py` — confirm Tier 2 = 0
2. Run: `python paper/check_glossary.py` — confirm 0 violations
3. Run: `seldon paper sync`
4. Run: `seldon paper build --no-render`
5. Rebuild PDF:
```bash
cd paper
quarto render paper.qmd --to pdf
cp paper.pdf ../leibniz-pi-draft.pdf
```

---

## Do NOT

- Do not modify any existing experiment scripts or data
- Do not overwrite any existing CC task files
- Do not hardcode values in the prose if Seldon result references are available — use `{{result:NAME:value}}` format for the new results once registered
- Do not change any other section content beyond the three additions above
- Do not modify the threshold sweep results file
