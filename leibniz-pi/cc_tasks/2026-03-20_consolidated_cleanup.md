# CC Task: Consolidated Cleanup — Stragglers from Review Pass

**Date:** 2026-03-20
**Scope:** `paper/sections/02_background.md`, `paper/sections/03_methods.md`, `paper/sections/06_discussion.md`
**Constraint:** All numbers must be discovered from source scripts or data files. No hardcoded values. Follow `paper/conventions.md` and `paper/glossary.md`.

---

## Pre-flight

1. `seldon go --brief --project-dir /Users/brock/Documents/GitHub/ai-demos/leibniz-pi`
2. Read `paper/conventions.md` and `paper/glossary.md`.
3. Read current state of all three files before editing.

---

## Task 1: Replace truncated decimal in 2.2

In `paper/sections/02_background.md`, Section 2.2 contains:

> "A series that sums to 0.7851 (near π/4)"

0.7851 is a truncated decimal approximation of a value near π/4 used illustratively. Replace with symbolic representation. The sentence should convey that a series converging to a value *near but not equal to* π/4 would score well on pointwise accuracy. Rewrite to use π/4 symbolically, e.g.:

> "A series that sums to a value near π/4 at T=10,000 terms would score well on pointwise accuracy but has no structural relationship to Leibniz."

Search all paper sections for any remaining truncated decimal representations of π/4 (0.785, 0.7851, 0.7854, 0.78540, etc.). Replace all with π/4 symbolically. Verify the Seldon graph is consistent.

---

## Task 2: Fix "approximately 4.4 bits" in 3.3.2

In `paper/sections/03_methods.md`, Section 3.3.2 contains:

> "Leibniz at T=10 has precision approximately 4.4 bits"

The previous CC task flagged this as incorrect from source. The editorial comment states:
- T=10 → 5.33 bits (from LEIBNIZ_REFS in source script)
- T=5 → 4.34 bits ≈ 4.4

**Discover from source:** Recompute or confirm both values from the source scripts (`entropy-leibniz-v3/entropy_leibniz_v3_minimal.py` or equivalent). Compute -log₂(|S(T) - π/4|) at T=5 and T=10 using the LEIBNIZ_REFS values.

**Fix:** Change to T=5 with the correct value (~4.3 bits), since 4.4 was clearly intended as T=5. Register the verified value as a Seldon result with provenance to the source computation. Replace the bare literal with `{{result:NAME:value}}`. Also register the T=10 value if not already registered.

If either value cannot be verified from source, flag it. Do not fabricate.

Remove the `<!-- EDITORIAL REVIEW -->` comment once resolved.

---

## Task 3: Reorder crystallization paragraph in 3.3.2

In `paper/sections/03_methods.md`, Section 3.3.2, the crystallization design motivation paragraph currently sits between the precision formula and the fitness formula. It begins "The design came from a chemical engineering perspective..." and ends "...This connection is discussed in Section 6.1."

Move this paragraph to AFTER the fitness formula and its weight/parameter description (the paragraph ending with "λ_p = 0.005"). The technical flow should be:

1. Precision definition (prec(T) formula)
2. Shannon disclaimer sentence
3. Leibniz precision at T=5 and T=10,000 (from Task 2)
4. Fitness formula
5. Weight and parameter definitions
6. THEN the crystallization/design motivation paragraph
7. THEN the "second-order question" paragraph

Do not alter the paragraph content. Move only.

---

## Task 4: Strip thermodynamic language from 6.2

In `paper/sections/06_discussion.md`, Section 6.2 contains:

> "The gradient-based selection variant was the most direct expression of the thermodynamic design intuition. It minimized the gradient norm across fitness dimensions to find the most uniformly balanced process in fitness space, the point closest to steady state in all dimensions simultaneously."

Replace with operational language. Describe what the variant did mechanistically without thermodynamic framing. Something like:

> "The gradient-based selection variant minimized the gradient norm across fitness components, selecting for expressions with the most uniform balance of precision gain, monotonicity, and rate consistency. It produced 0/5 discovery at 15 terminals."

Discover the actual gradient variant specification from source (`entropy-leibniz-v3/gradient_fitness_test.py` or equivalent) to confirm the operational description is accurate. If the source shows different component names, use what the code says.

"Thermodynamic design intuition" and "steady state" belong only in Section 6.5. Remove them from 6.2.

---

## Task 5: Replace "calibrated behavior" in 6.3

In `paper/sections/06_discussion.md`, Section 6.3, the Leibniz paragraph reads:

> "*Leibniz.* This exhibits calibrated behavior: infinite improvement at a constant rate, never fully confident, always refining. The constant-rate precision gain is the series-domain analog of a well-calibrated probability estimate that updates appropriately with evidence."

"Calibrated" has a specific technical meaning in ML (predicted probabilities matching observed frequencies) that does not apply here. Replace with:

> "*Leibniz.* This exhibits sustained refinement: precision improves at a constant rate without bound, never plateauing, each term contributing a measurable correction. The open-ended precision gain is the series-domain analog of a model that continues to incorporate new evidence without converging prematurely."

Preserve the three-tier contrast structure (non-GP → GP convergence-aware → Leibniz). Only change the Leibniz description.

---

## Task 6: Thin the non-GP paragraph in 6.3

In `paper/sections/06_discussion.md`, Section 6.3, the non-GP paragraph reads:

> "*Non-GP approaches.* In preliminary experiments with reinforcement learning and ant colony optimization (not reported here), these methods produced outputs that pattern-matched superficially to series convergence behavior but diverged under scrutiny. The failure mode is analogous to confabulation: generating plausible outputs that do not correspond to correct knowledge."

Compress to one sentence:

> "*Non-GP approaches.* Preliminary experiments with reinforcement learning and ant colony optimization (not reported here) produced outputs that pattern-matched to convergence behavior but diverged under extended evaluation, a failure mode analogous to confabulation."

If the result reads awkwardly in context with the paragraphs around it, cut the non-GP paragraph entirely and start the three-tier contrast at GP convergence-aware.

---

## Post-flight

After all edits:

```bash
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
```

Verify Tier 1 clean. Report Tier 2 violation count and whether any NEW violations were introduced compared to pre-edit baseline.

Report a summary of:
- Values discovered from source (with file and line/key)
- Values that could NOT be found (flag for manual review)
- Edits completed vs skipped

---

## Do NOT

- Do not edit any section files other than `02_background.md`, `03_methods.md`, and `06_discussion.md`.
- Do not hardcode any values. Discover from source.
- Do not fabricate provenance. Flag if source not found.
- Do not overwrite any existing CC task files.
- Do not add bold in prose. Do not use em dashes. Follow `conventions.md`.
- Do not modify Section 6.5 (Design Provenance). It is correct as-is.
- Do not remove the kinetics framing from 6.1. It belongs there.
