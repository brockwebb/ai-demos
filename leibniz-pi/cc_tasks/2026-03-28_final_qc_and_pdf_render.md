# CC Task: Final QC Pass and PDF Render

**Date:** 2026-03-28
**Scope:** Run all quality checks after abstract/title/conclusion/refs edits, then render final PDF
**Depends on:** `2026-03-28_abstract_title_conclusion_refs.md` must be completed first

---

## Pre-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi

# Verify the prior task completed -- check for updated abstract
head -5 paper/sections/00_abstract.md
# Should start with "# Abstract" and second line should mention "evaluation window" not "evaluation horizon"

# Verify title was updated
grep "title:" paper/frontmatter.yml
# Should show "The Evaluation Horizon Trap: Why Search Space Structure Dominates Fitness Design"

# Verify refs div was added
cat paper/sections/08_references.md
# Should contain "::: {#refs}" and ":::"

# Verify conclusion was updated
grep -c "combinatorially outnumbered" paper/sections/07_conclusion.md
# Should return 1
```

If any of these checks fail, STOP. The prior task has not completed. Do not proceed.

---

## Step 1: Run check_glossary.py

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/check_glossary.py
```

Review output. Report any new violations. Known acceptable violations:
- Single-sentence paragraphs adjacent to LaTeX formula blocks are accepted

---

## Step 2: Run prose_qc.py

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/prose_qc.py
```

This generates `paper/prose_qc_report.md`. Review the report and compare against the prior report. Focus on:
- Any NEW Tier 2 violations in sections 00 (abstract), 07 (conclusion), 08 (references)
- Any banned words introduced (check Tier 3)
- Em dash violations (zero tolerance)
- "entropy fitness" usage (should be "log-precision fitness")
- "novel", "robust", "leverage", "utilize" (banned)

Report all new violations. Do NOT fix them -- just report.

---

## Step 3: Seldon Sync and Build

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon paper sync
seldon paper build --no-render
```

Verify:
1. `seldon paper sync` shows updated content hashes for sections 00, 07, 08
2. `seldon paper build --no-render` resolves all `{{result:NAME:value}}` references without errors
3. No warnings about unresolved references or missing files

---

## Step 4: Render Final PDF

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi/paper
quarto render paper.qmd --to pdf
```

If the render fails, capture the full error output and report it.

If the render succeeds, verify the output file exists:
```bash
ls -la paper.pdf
```

---

## Step 5: Verify PDF Content (checklist)

Open or inspect the generated PDF and verify:

1. **Title page:** Shows "The Evaluation Horizon Trap: Why Search Space Structure Dominates Fitness Design"
2. **Author:** Brock Webb
3. **Census disclaimer:** Present (from `thanks:` field)
4. **Font:** Source Sans Pro (NOT Palatino). If Palatino appears, report this -- paper.qmd may need frontmatter sync.
5. **Abstract:** Appears before Section 1, is unnumbered, contains three paragraphs starting with "Finite evaluation..."
6. **Section numbering:** Sections 1-7 are numbered. References and Appendix A are unnumbered.
7. **References:** Bibliography entries appear UNDER the "References" heading, NOT after the Appendix. This is the critical fix from the refs task.
8. **Figures:** Three figures present (Fig 1: precision trajectories, Fig 2: parsimony, Fig 3: kinetics)
9. **Tables:** All tables render with booktabs formatting
10. **No orphaned page numbers or blank pages between References and Appendix**

Report the status of each item. If any fail, describe what you see.

---

## Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon status
```

Report:
1. Full prose_qc report (new violations only, compared to prior run)
2. Seldon status summary
3. PDF verification checklist results
4. Any issues found

---

## Do NOT

- Do not fix any QC violations -- report only. Fixes go in a separate task if needed.
- Do not modify any section files
- Do not modify existing CC task files
- Do not rerun experiments
- Do not change fonts, formatting, or frontmatter unless reporting a discrepancy
