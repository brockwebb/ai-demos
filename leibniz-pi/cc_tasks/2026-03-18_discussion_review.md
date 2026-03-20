# CC Task: Discussion Section (06) Review Edits

**Date:** 2026-03-18
**Scope:** `paper/sections/06_discussion.md`
**Constraint:** All numbers must come from source scripts or data files. No hardcoded values. Follow `paper/conventions.md` and `paper/glossary.md`.

---

## Pre-flight

1. `seldon go --brief --project-dir /Users/brock/Documents/GitHub/ai-demos/leibniz-pi`
2. Read `paper/conventions.md` and `paper/glossary.md` before writing any prose.
3. Read current state of `paper/sections/06_discussion.md`.
4. Read `paper/sections/05_results.md` for cross-reference context. Do not edit.

---

## Task 1: Strip thermodynamic language from gradient variant description in 6.2

The following passage in 6.2 uses thermodynamic framing that the conventions doc prohibits outside of 6.5:

> "The gradient-based selection variant was the most direct expression of the thermodynamic design intuition. It minimized the gradient norm across fitness dimensions to find the most uniformly balanced process in fitness space, the point closest to steady state in all dimensions simultaneously."

Replace with operational language describing what the variant actually did, without thermodynamic framing. Something like:

> "The gradient-based selection variant minimized the gradient norm across fitness components, selecting for expressions with the most uniform balance of precision gain, monotonicity, and rate consistency. It produced 0/5 discovery at 15 terminals."

The point is: describe the mechanism, then state the result. "Thermodynamic design intuition" and "steady state" belong in 6.5, not here. Discover the actual gradient variant specification from the source script if needed (`entropy-leibniz-v3/gradient_fitness_test.py` or similar) to confirm the operational description is accurate.

---

## Task 2: Flag coverage thesis repetition

The sentence "the bottleneck is coverage, not fitness landscape quality" (or close variants) appears in:
- Section 5.3
- Section 5.5
- Section 6.2
- Section 7 (conclusion)

The version in 6.2 is embedded in the proportionality argument and should stay. The version in 7 is the concluding statement and should stay.

**In 06_discussion.md:** No change needed to 6.2 for this item.

**Add editorial comments** in `paper/sections/05_results.md` at the instances in 5.3 and 5.5 suggesting they be thinned or removed in favor of the Discussion and Conclusion versions. Use the format:

```
<!-- EDITORIAL REVIEW: Coverage thesis repetition. This claim also appears in 6.2 and 07_conclusion.
     Consider cutting or softening this instance to avoid redundancy. —Review item #9 -->
```

If similar editorial comments already exist from previous review passes, do not duplicate them.

---

## Task 3: Fix "calibrated behavior" in 6.3

The current text describes Leibniz as exhibiting "calibrated behavior" by analogy to ML probability calibration:

> "*Leibniz.* This exhibits calibrated behavior: infinite improvement at a constant rate, never fully confident, always refining. The constant-rate precision gain is the series-domain analog of a well-calibrated probability estimate that updates appropriately with evidence."

"Calibrated" has a specific technical meaning in ML (predicted probabilities matching observed frequencies) that does not apply here. The analogy is a stretch that could irritate a stats-aware reviewer.

Replace "calibrated behavior" with language that describes what Leibniz actually does without borrowing the calibration term. Something like:

> "*Leibniz.* This exhibits sustained refinement: precision improves at a constant rate without bound, never plateauing, each term contributing a measurable correction. The open-ended precision gain is the series-domain analog of a model that continues to update appropriately with additional evidence."

Preserve the three-tier contrast structure (non-GP → GP convergence-aware → Leibniz). Only change the Leibniz description.

---

## Task 4: Thin the non-GP paragraph in 6.3

The current text reads:

> "*Non-GP approaches.* In preliminary experiments with reinforcement learning and ant colony optimization (not reported here), these methods produced outputs that pattern-matched superficially to series convergence behavior but diverged under scrutiny. The failure mode is analogous to confabulation: generating plausible outputs that do not correspond to correct knowledge."

These experiments are not reported in the paper, so this paragraph carries no evidentiary weight. Two options:

**Option A (preferred):** Compress to one sentence and acknowledge the limitation explicitly:

> "*Non-GP approaches.* Preliminary experiments with reinforcement learning and ant colony optimization (not reported here) produced outputs that pattern-matched to convergence behavior but diverged under extended evaluation, a failure mode analogous to confabulation."

**Option B:** Cut entirely and start the three-tier contrast at GP convergence-aware.

Implement Option A unless it reads awkwardly in context, in which case implement Option B.

---

## Task 5: Split long sentence in 6.1

Paragraph 3 of 6.1 contains:

> "The convergence-aware fitness asks a first-order question: 'is error shrinking between checkpoints?' The log-precision fitness asks a second-order question: 'is 1/error growing linearly?'"

This is actually fine as two sentences. But the sentence immediately before it is long:

> "The rate d(precision)/d(log T) is constant: log₂(10) ≈ {{result:info_rate_3_32:value}} bits per decade."

Check the full paragraph for any sentence exceeding 35 words (conventions limit). Split any that do. The kinetics framing is appropriate in 6.1 (this is where it belongs), so preserve the first-order/second-order language here.

---

## Post-flight

After all edits:

```bash
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
```

Verify Tier 1 clean. Report any new warnings.

---

## Do NOT

- Do not edit any section file other than `paper/sections/06_discussion.md`, except for adding editorial comments to `paper/sections/05_results.md` as specified in Task 2.
- Do not edit `paper/sections/05_results.md` prose. Only add editorial comments.
- Do not hardcode any values.
- Do not overwrite any existing CC task files.
- Do not add bold in prose. Do not use em dashes. Follow `conventions.md`.
- Do not modify Section 6.5 (Design Provenance). It is strong as-is.
- Do not remove the kinetics framing from 6.1. It belongs there.
