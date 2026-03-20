# CC Task: Background Section (02) Review Edits

**Date:** 2026-03-18
**Scope:** `paper/sections/02_background.md`
**Constraint:** Follow `paper/conventions.md` and `paper/glossary.md`. No hardcoded research values.

---

## Pre-flight

1. `seldon go --brief --project-dir /Users/brock/Documents/GitHub/ai-demos/leibniz-pi`
2. Read `paper/conventions.md` and `paper/glossary.md` before writing any prose.
3. Read current state of `paper/sections/02_background.md`.

---

## Task 1: Compress literature list in 2.1

Paragraph 3 of 2.1 currently lists six symbolic regression systems, each in its own sentence, with no analytical connective tissue:

> "Modern symbolic regression systems span several paradigms. PySR (Cranmer, 2023) uses multi-population evolutionary search with a Pareto front trading accuracy against complexity. SymbolicGPT (Valipour et al., 2021) uses transformers to predict symbolic expressions. DySymNet (Li et al., 2023) combines neural networks with symbolic search. GFlowNet-based methods (Li et al., 2023) frame symbolic regression as a generative flow problem. MCTS approaches (Kamienny et al., 2023; Shojaee et al., 2023) use tree search with learned value functions. EGG-SR (Jiang et al., 2025) applies equality saturation for canonicalization."

This reads as a checklist. Compress to one or two sentences that name the paradigm categories with parenthetical citations. Let the contrast paragraph that follows ("All of these systems optimize pointwise fitness") do the analytical work. Something like:

> "Modern symbolic regression spans evolutionary (Cranmer, 2023), transformer-based (Valipour et al., 2021), neural-symbolic (Li et al., 2023), generative flow (Li et al., 2023), tree-search (Kamienny et al., 2023; Shojaee et al., 2023), and equality saturation approaches (Jiang et al., 2025)."

One sentence, citation-heavy, then directly into the contrast.

---

## Task 2: Cut one "to our knowledge"

"To our knowledge" appears in both 2.2 and 2.3. Cut the instance in 2.2. The novelty claim in 2.3 (wrong-limit attractors as a distinct failure mode) is the stronger one and should carry the "to our knowledge" flag.

In 2.2, replace:

> "To our knowledge, no prior work designs fitness functions for this objective class."

with a direct claim:

> "No prior work that we are aware of designs fitness functions for this objective class."

Actually, that's the same thing reworded. Better: just make the claim directly.

> "Prior symbolic regression work does not address fitness design for this objective class."

Simpler, no hedging stack, still accurate.

---

## Task 3: Develop or cut time-series forecasting analogy in 2.2

The current text says:

> "The closest analog is time-series forecasting, where models are evaluated on multi-step-ahead prediction quality rather than single-point accuracy. The Leibniz problem differs in that it requires evaluation at geometrically spaced depths (5, 10, 20, 50, ..., 10000 terms), not sequential future steps."

This is a dangling comparison. It introduces a related domain and immediately dismisses it without explaining why the analogy is useful or what the reader should take from it. Two options:

**Option A (preferred):** Cut it. The paragraph works without it. The point (pointwise fitness is insufficient, process-level evaluation is needed) is already made by the preceding sentences.

**Option B:** Add one sentence explaining what the analogy illuminates. Something like: "Both require evaluating trajectory behavior rather than endpoint accuracy, but the Leibniz problem evaluates convergence structure across geometric scales rather than sequential forecast accuracy."

Implement Option A unless the resulting paragraph feels too short (minimum two sentences per paragraph per conventions).

---

## Task 4: Soften "infinitely many" claim in 2.3

The current text states:

> "Infinitely many rational functions P(k)/Q(k) have partial sums converging to finite values near any target."

This is a mathematical claim with no citation or argument. A referee could challenge it. Soften to avoid the burden of proof:

> "A large class of rational functions P(k)/Q(k) have partial sums converging to finite values near any target, and the density of such functions grows with the available terminal set."

Or, if you can find a brief supporting argument in `RESEARCH_NOTES.md` or `RESEARCH_NOTES_SUPP_core_finding.md`, add it as a parenthetical. The partial fractions argument (any rational with simple poles yields a convergent partial sum) would suffice.

---

## Task 5: Add bloat citation in 2.3

The current text says:

> "The symbolic regression literature extensively discusses *bloat*: the tendency of GP to produce increasingly complex expressions that overfit without improving generalization."

This invokes bloat as a well-known phenomenon but cites nothing. Add a citation. Standard references:

- Koza (1992) for the original GP book
- Poli, Langdon, and McPhee (2008) "A Field Guide to Genetic Programming"
- Luke and Panait (2006) for bloat analysis

Check `paper/references.bib` for which of these are already present. If none are, add the most appropriate one to `references.bib` and cite it here. If any are already present, use the existing citation.

---

## Task 6: Standardize π/4 representation in 2.4 and verify graph consistency

Section 2.4 uses the truncated decimal 0.7854 as an approximation of π/4. This value is π/4 for the Leibniz series. It should be represented consistently as π/4 throughout the paper, not as a truncated decimal.

**Steps:**

1. Replace all instances of 0.7854 (and variants like 0.78540) in Section 2.4 with π/4 written symbolically.
2. Search all other paper sections for truncated decimal representations of π/4 (0.785, 0.7854, 0.78540, etc.). Replace with π/4 symbolically wherever found.
3. Verify that π/4 has proper provenance in the Seldon graph. If it is not already registered as an artifact or constant with provenance, register it. This is the convergence target for the Leibniz series and should be tracked like any other value in the system.
4. Update the graph to reflect consistent representation across all sections.

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

- Do not edit any section file other than `paper/sections/02_background.md` and (if needed) `paper/references.bib`.
- Do not hardcode any research values.
- Do not overwrite any existing CC task files.
- Do not add bold in prose. Do not use em dashes. Follow `conventions.md`.
- Do not restructure or reorder subsections. 2.4 stays separate from 2.3.
