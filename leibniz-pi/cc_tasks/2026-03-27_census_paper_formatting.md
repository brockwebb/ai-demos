# CC Task: Apply Census Bureau Paper Formatting Standards

**Date:** 2026-03-27
**Priority:** Medium — formatting alignment before final PDF build

---

## Context

The Leibniz paper's Quarto configuration needs to match the formatting standards established in the Pragmatics paper (`/Users/brock/Documents/GitHub/census-mcp-server/paper/draft_v1.qmd`). Currently the Leibniz paper has a bare `_quarto.yml` with no title/author/date, no Census disclaimer, no professional fonts, no section numbering, and no typographic controls.

## Pre-Flight

1. Read `/Users/brock/Documents/GitHub/census-mcp-server/paper/draft_v1.qmd` (first 50 lines — the YAML frontmatter block)
2. Read `/Users/brock/Documents/GitHub/ai-demos/leibniz-pi/paper/_quarto.yml`
3. Read `/Users/brock/Documents/GitHub/ai-demos/leibniz-pi/paper/paper.qmd` (first 10 lines — check for existing frontmatter)

---

## Step 1: Download APA CSL file

Download the APA citation style file locally so builds don't depend on network access:

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi/paper
curl -o apa.csl https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl
```

---

## Step 2: Update `_quarto.yml`

Replace the contents of `paper/_quarto.yml` with:

```yaml
project:
  type: default

format:
  pdf:
    documentclass: article
    papersize: letter
    fontsize: 11pt
    geometry:
      - margin=1in
    number-sections: true
    toc: false
    pdf-engine: xelatex
    latex-max-runs: 4
    mainfont: "Palatino"
    monofont: "Source Code Pro"
    linestretch: 1.25
    colorlinks: true
    bibliography: references.bib
    csl: apa.csl
    link-citations: true
    include-in-header:
      - text: |
          \usepackage{booktabs}
          \usepackage{needspace}
          \usepackage{longtable}
          \usepackage{array}
          \renewcommand{\arraystretch}{1.4}
          \widowpenalty=10000
          \clubpenalty=10000
          \usepackage{caption}
          \captionsetup{justification=raggedright,singlelinecheck=false}
          \hyphenpenalty=10000
          \exhyphenpenalty=10000
          \raggedbottom
          \usepackage{pdflscape}
          \usepackage{float}
          \floatplacement{figure}{htbp}
          \renewcommand{\floatpagefraction}{0.85}
          \renewcommand{\topfraction}{0.85}
          \renewcommand{\textfraction}{0.1}
  html:
    toc: false
    number-sections: false
    bibliography: references.bib
```

---

## Step 3: Add YAML frontmatter to `paper.qmd`

The `paper.qmd` file currently starts directly with `# Abstract` (no YAML frontmatter). Add a YAML frontmatter block at the very top of `paper.qmd`, BEFORE the `# Abstract` line:

```yaml
---
title: "Wrong-Limit Attractors: Why Constraining the Search Space Dominates Fitness Engineering for Discovery of Convergent Processes"
author: "Brock Webb"
date: "March 2026"
thanks: "The views expressed are the author's own and do not necessarily represent the views of the U.S. Census Bureau or the U.S. Department of Commerce."
---
```

Do NOT modify any content below the frontmatter block. Just prepend this block before the existing `# Abstract` line.

**NOTE:** The title above is a placeholder. If Brock has specified a different title elsewhere, use that. If not, this title captures the paper's core argument. Brock may want to revise it.

---

## Step 4: Remove duplicate section numbers

With `number-sections: true` in `_quarto.yml`, Quarto will auto-number sections. The section files currently have manual numbers in their headings (e.g., `# 1. Introduction`, `# 2. Background`). These will create doubled numbering like "1 1. Introduction".

In each section file in `paper/sections/`, strip the manual number prefix from the top-level heading:
- `# 1. Introduction` → `# Introduction`
- `# 2. Background` → `# Background`
- `# 3. Methods` → `# Methods`
- `# 4. Experimental Design` → `# Experimental Design`
- `# 5. Results` → `# Results`
- `# 6. Discussion` → `# Discussion`
- `# 7. Conclusion` → `# Conclusion`
- `# 8. References` → `# References`

Leave `# Abstract` as-is (abstracts are typically unnumbered; Quarto handles this).
Leave `# 9. Appendix` — check if Quarto auto-numbers appendices. If it does, strip to `# Appendix`.

Do NOT change any subheading numbers (e.g., `## 5.6 Threshold Sensitivity` should keep its number since Quarto will auto-number subsections too — actually, check: if `number-sections: true` handles subsections, strip those too).

**IMPORTANT:** After stripping manual numbers, do a search for any cross-references in prose that say things like "Section 3.3.2" or "Section 6.1" — these are fine because they reference section numbers that Quarto will generate. But confirm the auto-numbering matches the expected numbers.

---

## Step 5: Build and Verify

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon paper sync
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
```

Open the PDF and verify:
- Title page has: title, author, date
- Footer on first page has the Census disclaimer ("The views expressed...")
- Font is Palatino (serif body text), Source Code Pro (monospace)
- Sections are auto-numbered (1, 2, 3... with subsections 5.1, 5.2, etc.)
- No doubled numbering (e.g., not "1 1. Introduction")
- Line spacing is comfortable (1.25)
- Tables use booktabs style (horizontal rules only)
- Landscape tables in appendix still work
- Figures render correctly
- Bibliography renders at end with APA style
- No broken cross-references

---

## Step 6: Font Availability Check

If `xelatex` fails because Palatino or Source Code Pro are not installed, fall back:
- Try `mainfont: "Palatino Linotype"` or `mainfont: "TeX Gyre Pagella"` (TeX's Palatino clone)
- Try `monofont: "Courier New"` if Source Code Pro is unavailable
- Report which fonts worked

---

## Do NOT

- Do not modify any prose content in section files (only strip manual section numbers from headings)
- Do not change the abstract text
- Do not change the bibliography entries
- Do not modify this task file
- Do not change figure files
