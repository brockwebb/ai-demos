# CC Task: Final Introduction QC Fix (1 remaining split)

**Date:** 2026-03-27
**Priority:** High

---

## Pre-Flight

Read `paper/sections/01_introduction.md` before editing.

---

## Fix: Split Discovery paragraph (PQ-02 line 17, 10 sentences)

In the paragraph that begins "Discovery exhibits a sharp phase transition," find:

```
Extending the time budget by 4x did not rescue discovery.
```

Insert a paragraph break (blank line) after that sentence.

This creates:
- Paragraph A (6 sentences): The phase transition and what didn't fix it
- Paragraph B (4 sentences): The diagnosis — bottleneck is coverage, not fitness. Injection confound note. Failure conditions more instructive than success.

---

## Accepted violations (do not attempt to fix)

- PQ-02 single-sentence paragraphs around the LaTeX formula block — structural, unfixable without removing the formula
- SP-03 word repetition ("horizon," "target," "converge," "within") — core subject-matter terms, unavoidable

---

## Post-Flight

1. Run: `cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi && python paper/prose_qc.py`
2. Run: `python paper/check_glossary.py`
3. Run: `seldon paper sync`
4. Run: `seldon paper build --no-render`

Confirm Tier 1 = 0 (excluding the two accepted single-sentence violations around the formula). Report any new violations.

---

## Do NOT

- Do not change any wording
- Do not attempt to fix the formula-adjacent single-sentence paragraphs
- Do not attempt to reduce word repetition for core subject-matter terms
