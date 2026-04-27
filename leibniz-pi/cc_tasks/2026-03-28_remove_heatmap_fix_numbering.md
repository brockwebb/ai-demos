# CC Task: Remove Heatmap Figure, Fix Unnumbered Sections

**Date:** 2026-03-28
**Priority:** High — formatting and content fixes

---

## Problems

1. Figure 2 (scaling heatmap) duplicates Table 5. The heatmap is mostly zeros and adds no insight beyond what the table already shows. Remove the figure; the table stays.
2. "8 References" and "9 Appendix A: Expression Catalog" are numbered sections. They should be unnumbered.

---

## Pre-Flight

1. Read `paper/sections/05_results.md`
2. Read `paper/sections/08_references.md`
3. Read `paper/sections/09_appendix_expressions.md`
4. Read `paper/conventions.md`

---

## Step 1: Remove heatmap figure from Section 05

In `paper/sections/05_results.md`, find and remove these lines (the image embed and its caption):

```
![Discovery rate across terminal set sizes and population sizes](figures/fig1_scaling_heatmap.png)

**Figure 2:** Discovery rate across terminal set sizes and population sizes. The dashed red line marks the phase transition between t=8 and t=10. The anomalous partial recovery at t=15, pop=10,000 is visible.
```

Do NOT remove Table 5 (the markdown table with `{{result:...}}` references) — that stays. Only remove the image embed and its caption.

After removal, check that the prose following the figure still flows. The paragraph starting "At t=4, discovery is reliable..." should follow directly after Table 5.

Also: renumber any remaining figure references in the paper. With the heatmap gone:
- What was "Figure 1" (precision trajectories) stays as Figure 1
- What was "Figure 3" (parsimony collapse) becomes Figure 2
- What was "Figure 4" (second-order kinetics) becomes Figure 3
- What was "Figure 4b" (log-log kinetics) becomes Figure 4 (if referenced)

Search ALL section files for "Figure 2", "Figure 3", "Figure 4" references in prose and update the numbers. Also update figure captions in the markdown.

---

## Step 2: Make References and Appendix unnumbered

In `paper/sections/08_references.md`, change:
```
# References
```
to:
```
# References {.unnumbered}
```

In `paper/sections/09_appendix_expressions.md`, change:
```
# Appendix A: Expression Catalog
```
to:
```
# Appendix A: Expression Catalog {.unnumbered}
```

Also check if there are any subsections in the appendix (e.g., `## 9.1 Leibniz-Equivalent Expressions`). If so, strip their manual numbers and add `{.unnumbered}`:
- `## 9.1 Leibniz-Equivalent Expressions` → `## Leibniz-Equivalent Expressions {.unnumbered}`
- Same for any other subsections in the appendix

---

## Step 3: Post-Flight

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
```

Verify in the rendered PDF:
- No heatmap figure appears
- Table 5 (scaling grid) is present and readable
- Figure numbers are sequential (1, 2, 3...) with no gaps
- References section is unnumbered
- Appendix is unnumbered
- Appendix subsections are unnumbered

---

## Do NOT

- Do not remove Table 5 (the scaling grid table)
- Do not delete the heatmap image files from `paper/figures/` (they're tracked by Seldon)
- Do not modify any prose content beyond figure number updates
- Do not modify existing CC task files
- Do not modify _quarto.yml or frontmatter.yml
