# CC Task: Landscape Orientation for Wide Appendix Tables + Rebuild PDF

**Date:** 2026-03-26
**Priority:** High
**Context:** Tables A.1 and A.2 in section 09_appendix_expressions.md are too wide for portrait orientation. They need landscape pages in the PDF output.

---

## Pre-Flight

1. Read `paper/sections/09_appendix_expressions.md` before editing.
2. Read `paper/_quarto.yml` to check current LaTeX config.

---

## Step 1: Add lscape package to _quarto.yml

Edit `paper/_quarto.yml` to include the lscape LaTeX package. Add these lines under the `pdf:` format section:

```yaml
    include-in-header:
      - text: |
          \usepackage{lscape}
          \usepackage{longtable}
```

The full `pdf:` section should look like:

```yaml
  pdf:
    documentclass: article
    papersize: letter
    margin-left: 1in
    margin-right: 1in
    margin-top: 1in
    margin-bottom: 1in
    fontsize: 11pt
    linestretch: 1.15
    toc: false
    number-sections: false
    colorlinks: true
    bibliography: references.bib
    csl: https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl
    include-in-header:
      - text: |
          \usepackage{lscape}
```

---

## Step 2: Wrap wide tables in landscape blocks

In `paper/sections/09_appendix_expressions.md`, add raw LaTeX landscape markers around the two wide tables.

### Table A.1 (Leibniz-Equivalent Expressions)

Find the line:
```
| Seed | Raw Form | Nodes | Fitness | Fitness Function | t | Pop | Experiment |
```

Add BEFORE the table header row (but after the prose paragraph above it):
```
\begin{landscape}
```

Find the LAST row of the A.1 table (the row ending with `fitness\_approach2\_w0.1 |`).

Add AFTER that last row:
```
\end{landscape}
```

### Table A.2 (Notable Wrong-Limit Attractors)

Find the line:
```
| Seed | Raw Form | Nodes | Fitness | t | Experiment | Simplified | Notes |
```

Add BEFORE the table header row (but after the prose paragraph above it):
```
\begin{landscape}
```

Find the LAST row of the A.2 table (the row ending with `Canonical 5/((6+4k)(k-2)) attractor |`).

Add AFTER that last row:
```
\end{landscape}
```

### Table A.4 (Trivial Expressions) — check if this one also overflows

The A.4 table has 6 columns. If it fits in portrait, leave it. If it also overflows, wrap it the same way.

---

## Step 3: Also consider font size reduction

If landscape alone is not enough (the Raw Form column has very long expression strings), add a `\small` or `\footnotesize` command inside the landscape block, before the table:

```
\begin{landscape}
\small
| Seed | Raw Form | ...
```

Try `\small` first. If still overflowing, use `\footnotesize`.

---

## Step 4: Rebuild

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon paper sync
seldon paper build --no-render
cd paper
quarto render paper.qmd --to pdf
cp paper.pdf ../leibniz-pi-draft.pdf
echo "PDF rebuilt at leibniz-pi-draft.pdf"
```

---

## Step 5: Verify

Open the PDF and confirm:
- [ ] A.1 table renders on landscape pages, no column overflow
- [ ] A.2 table renders on landscape pages, no column overflow
- [ ] Rest of the paper remains portrait
- [ ] No other formatting regressions (references still populated, figures still render, no double numbering)

If landscape + \small is still too wide, report which columns overflow and by how much.

---

## Do NOT

- Do not modify any prose content or table data
- Do not reorder or restructure the appendix
- Do not change any other section files
- Do not overwrite existing CC task files
