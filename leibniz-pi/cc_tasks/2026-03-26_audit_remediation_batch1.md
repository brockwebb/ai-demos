# CC Task: Audit Remediation Batch 1 (5 items)

**Date:** 2026-03-26
**Priority:** High (blocks abstract)
**Source:** `audits/2026-03-26_full_paper_audit.md`

---

## Pre-Flight

1. Read `paper/conventions.md`
2. Read each section file listed below BEFORE editing it

---

## Item 1: Conclusion "every seed" overstatement (07_conclusion.md)

Read `paper/sections/07_conclusion.md`.

Find:
```
With four terminals, every seed found Leibniz.
```

Replace with:
```
With four terminals, discovery was reliable: 19 of 20 seeds found Leibniz across all population sizes.
```

---

## Item 2: Conclusion paragraph structure (07_conclusion.md)

In the same file, find:
```
Three directions address the coverage bottleneck: building block initialization that seeds structural vocabulary rather than complete answers, and automated terminal pruning that discards irrelevant primitives before the full search. A third direction, island migration, lets successful subpopulations share building blocks. Each attacks the constraint our experiments identify as primary: not the quality of the search, but the quality of the search space.
```

Replace with:
```
Three directions address the coverage bottleneck. First, building block initialization that seeds structural vocabulary rather than complete answers. Second, automated terminal pruning that discards irrelevant primitives before the full search. Third, island migration that lets successful subpopulations share building blocks. Each attacks the constraint our experiments identify as primary: not the quality of the search, but the quality of the search space.
```

---

## Item 3: Remove 9 orphan .bib entries (references.bib)

Read `paper/references.bib`.

Remove these 9 entries entirely (including their individual comments if any):

1. `Brunton2016SINDy`
2. `Rudy2017DataDriven`
3. `deSilva2020Discovery`
4. `Keijzer2011ScalingDeceptive`
5. `Haghighat2015AvoidingOverfitting`
6. `Durasevic2020Fitness`
7. `Muldoon2023ErrorCorrelation`
8. `LaCasse2022BayesianBloat`
9. `Langdon2002GPConvergence`

Keep section comment headers (the `% ═══` lines) only if other entries remain in that section. Remove section headers if the entire section becomes empty after removal.

**Verification:**
```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
# Count remaining entries
grep -c '^@' paper/references.bib

# Confirm every @key in sections exists in .bib
for key in $(grep -ohE '@[A-Za-z0-9_]+' paper/sections/*.md | sed 's/^@//' | sort -u); do
  if ! grep -q "$key" paper/references.bib; then
    echo "MISSING IN BIB: $key"
  fi
done

# Confirm every .bib key is cited in at least one section
for key in $(grep -ohE '^@[a-z]+\{[^,]+' paper/references.bib | sed 's/@[a-z]*{//'); do
  if ! grep -rq "$key" paper/sections/*.md; then
    echo "ORPHAN IN BIB: $key"
  fi
done
```

---

## Item 4: Checkpoint sensitivity sentence (03_methods.md)

Read `paper/sections/03_methods.md`.

In Section 3.3.2, find the sentence:
```
The denser checkpoint set (compared to the five checkpoints used by the convergence-aware fitness) provides finer-grained measurement of precision gain rate and extends the evaluation horizon to T = 10,000.
```

Add immediately after that sentence:
```
The specific checkpoint values influence which attractors are detectable; an attractor that matches the target at most checkpoints but diverges at others can appear competitive (Appendix A.2.3).
```

---

## Item 5: Safe division implicit terminal clarification (04_experimental_design.md)

Read `paper/sections/04_experimental_design.md`.

In Section 4.3, find the sentence:
```
Researchers counting available terminals should account for these implicit constants.
```

Add immediately after that sentence:
```
Because 1.0 is already in the base terminal set at all sizes, the implicit constants from safe division and power overflow do not increase the effective terminal count.
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

- Do not modify any prose content beyond the five specific changes above
- Do not overwrite any existing CC task files
- Do not change any `{{result:...}}` references
- Do not reorder sections or tables
- Do not add or modify citations beyond the .bib cleanup
