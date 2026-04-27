# CC Task: Audit Remediation Batch 2 (Items 8 and 9)

**Date:** 2026-03-26
**Priority:** Medium
**Source:** `audits/2026-03-26_full_paper_audit.md`

---

## Pre-Flight

1. Read `paper/conventions.md`
2. Read each section file listed below BEFORE editing it

---

## Item 8: Preview Sastry population sizing in Section 2 (02_background.md)

Read `paper/sections/02_background.md`.

In Section 2.3 (Wrong-Limit Attractors), find the last paragraph that ends with:
```
To our knowledge, no prior work analyzes this failure mode as distinct from bloat or overfitting in symbolic regression.
```

Add a new paragraph AFTER that one (still within Section 2.3, before Section 2.4):
```
A related question is how large a GP population must be for selection to reliably propagate correct building blocks. @Sastry2005PopulationSizing derive a population-sizing relationship based on building-block decision making, showing that the required population grows with problem difficulty, bloat, and the number of building blocks that must be simultaneously present. We return to this framework in Section 6.2 when analyzing why population increases fail to rescue discovery at large terminal counts.
```

---

## Item 9: Soften "coverage scales linearly" in Section 6.2 (06_discussion.md)

Read `paper/sections/06_discussion.md`.

In Section 6.2, find:
```
Coverage scales linearly with population size. @Sastry2005PopulationSizing derived a population-sizing relationship for GP from building-block decision-making theory, formalizing the intuition that the required population scales with the number of building blocks that must be simultaneously present. Doubling the population roughly doubles the initial coverage.
```

Replace with:
```
Coverage increases with population size, but the relationship is not simple. @Sastry2005PopulationSizing derived a population-sizing relationship for GP from building-block decision-making theory, showing that the required population grows with the number of building blocks that must be simultaneously present and the difficulty of distinguishing them under selection.
```

---

## Post-Flight

1. Run: `cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi && python paper/prose_qc.py` — confirm Tier 2 = 0
2. Run: `python paper/check_glossary.py` — confirm 0 violations
3. Run: `seldon paper sync`
4. Run: `seldon paper build --no-render`

---

## Do NOT

- Do not modify any prose content beyond the two specific changes above
- Do not overwrite any existing CC task files
- Do not change any `{{result:...}}` references
