# CC Task: Results Section (05) Editorial Decisions

**Date:** 2026-03-20
**Scope:** `paper/sections/05_results.md`
**Constraint:** All numbers must be discovered from source scripts or data files. No hardcoded values. Follow `paper/conventions.md` and `paper/glossary.md`.

---

## Pre-flight

1. `seldon go --brief --project-dir /Users/brock/Documents/GitHub/ai-demos/leibniz-pi`
2. Read `paper/conventions.md` and `paper/glossary.md` before writing any prose.
3. Read current state of `paper/sections/05_results.md`.

---

## Task 1: Discover what all five seeds found at t=15 (Review Item #7, Section 5.2)

Currently only seed 42's wrong-limit attractor is described. The data for all five seeds should exist in the stress test data files.

**Discover from source:** Check `entropy-leibniz-v3/stress_L1_data.json` (or whichever data file corresponds to the 15-terminal stress test at p=1000). For each of the five seeds (42, 7, 137, 2718, 31415), find:
- The best expression found
- Its fitness score
- Whether it is a wrong-limit attractor, trivial collapse, or something else

Add one or two sentences after the seed 42 description summarizing the pattern across all five seeds. The point is to establish whether the wrong-limit attractor failure mode is universal or seed-specific at 15 terminals.

If any seed produced an expression worth noting individually (structurally different attractor, unusually high or low fitness), mention it. Otherwise, a summary sentence is sufficient.

If the data cannot be found for any seed, flag it as missing. Do not fabricate.

Remove the `<!-- EDITORIAL REVIEW ... Review item #7 -->` comment once addressed.

---

## Task 2: Cut speculation in 5.3 (Review Item #5)

The current text after the scaling grid table includes speculative explanation for the t=15/p=10000 non-monotonicity:

> "We do not have a confirmed mechanistic account of this non-monotonicity. The most plausible explanation is that at t=15 the search space contains fewer wrong-limit attractors than at t=10 or t=12, allowing a large population to occasionally maintain sufficient structural coverage."

Replace both sentences with a single sentence:

> "We do not have a mechanistic account of this non-monotonicity."

Cut the speculation entirely. Five seeds is too few to speculate about attractor density differences. If a reviewer asks, it can be addressed in revision.

Remove the `<!-- EDITORIAL REVIEW ... Review item #5 -->` comment once addressed.

---

## Task 3: Soften coverage thesis in 5.3 (Review Item #9)

The final sentence of 5.3 currently reads:

> "This confirms that coverage, not fitness landscape quality, limits discovery."

This is the fourth instance of this claim across the paper. The strong versions should be in 5.5 and the Conclusion. Soften this instance to something like:

> "This pattern is consistent with a coverage limitation rather than a fitness landscape limitation."

Same idea, less declarative. Saves the definitive statement for 5.5 where the fitness modification evidence earns it.

Remove the `<!-- EDITORIAL REVIEW ... Review item #9 -->` comment from 5.5 once addressed. (Note: the discussion task may have already added editorial comments here. Check current state before editing. Do not duplicate comments.)

---

## Task 4: Add extended time test paragraph to 5.5 (Review Items #10, #11)

The extended time test result is referenced in Section 4.2 as a design consideration, but the actual result needs to be presented in Results.

**Discover from source:** Check `gp-leibniz-v3/results_gp_extended_t10_p5000/` for the extended time test data. Find:
- Per-seed time budget used (believed to be 7200s but must be verified from source)
- Number of seeds that discovered Leibniz
- Total seeds run
- Whether the successful seed was the same seed that succeeded in the standard-budget run
- What the other seeds found (wrong-limit attractors? same ones as standard run?)

If a Seldon result already exists for this (`gp_extended_t10_p5000_1_5` was registered by the experimental design task), verify it matches the source data.

Add a brief paragraph at the end of 5.5 (after the fitness modifications table discussion, before the editorial comments). Something like:

> "As a further test, we ran the convergence-aware fitness at t=10, p=5000 with [discovered] seconds per seed, [X] times the standard budget. Discovery was [discovered]/5, [describe whether same seed]. The remaining seeds found [discover from data]. Extending the time budget does not rescue discovery when the terminal set exceeds the coverage threshold."

All values discovered from source. If data cannot be found, flag it. Do not fabricate.

Remove the `<!-- EDITORIAL REVIEW ... Review items #10, #11 -->` comment once addressed.

---

## Task 5: Remove resolved editorial comments

After completing Tasks 1-4, verify that all addressed editorial review comments have been removed from the file. Any remaining `<!-- EDITORIAL REVIEW -->` comments that were NOT addressed by this task (e.g., the figures TBD comment) should remain in place.

---

## Post-flight

After all edits:

```bash
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
```

Verify Tier 1 clean. Report Tier 2 violation count and whether any new violations were introduced.

Report a summary of:
- Values discovered from source (with file and line/key)
- Values that could NOT be found (flag for manual review)
- Editorial comments removed vs remaining

---

## Do NOT

- Do not edit any section file other than `paper/sections/05_results.md`.
- Do not hardcode any values. All numbers come from source data files.
- Do not fabricate provenance. If data is missing, flag it.
- Do not overwrite any existing CC task files.
- Do not add bold in prose. Do not use em dashes. Follow `conventions.md`.
- Do not add or remove sections. No new subsections (5.6, etc.) in this task.
- Do not address the figures TBD comment. That is a separate task.
- Do not speculate. If data doesn't support a claim, cut the claim.
