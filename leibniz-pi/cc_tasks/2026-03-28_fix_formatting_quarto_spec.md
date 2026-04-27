# CC Task: Fix Paper Formatting to Match QUARTO_SPEC

**Date:** 2026-03-28
**Priority:** High — paper renders with wrong formatting

**Reference:** `/Users/brock/Documents/GitHub/central_library/templates/quarto/QUARTO_SPEC.md`

---

## Problems to Fix

1. Abstract renders as "1 Abstract" (numbered section). It must be in the YAML `abstract:` field, not body content.
2. Font is Palatino. QUARTO_SPEC says Source Sans Pro.
3. Date renders as ISO format. Should be human-readable.
4. `seldon paper sync` overwrites paper.qmd, stomping any YAML frontmatter. Need a post-sync injection step.

---

## Pre-Flight

1. Read `/Users/brock/Documents/GitHub/central_library/templates/quarto/QUARTO_SPEC.md`
2. Read `paper/_quarto.yml` (current state)
3. Read `paper/paper.qmd` (first 30 lines, check frontmatter)
4. Read `paper/sections/00_abstract.md`
5. Run `seldon paper sync` and check if it overwrites paper.qmd frontmatter (this tells us the Seldon behavior)

---

## Step 1: Update `_quarto.yml` to match QUARTO_SPEC

Replace `paper/_quarto.yml` with the following. Key changes from current:
- `mainfont` → Source Sans Pro (not Palatino)
- Add `sansfont: "Source Sans Pro"`
- Add `linkcolor: "blue"`
- Move abstract text into YAML `abstract:` field
- Keep `toc: false` (diverges from QUARTO_SPEC default, but this is a preprint where TOC is not standard)
- Keep `thanks:` for Census disclaimer

```yaml
project:
  type: default

format:
  pdf:
    documentclass: article
    papersize: letter
    fontsize: 11pt
    pdf-engine: xelatex
    latex-max-runs: 4
    geometry:
      - margin=1in
    number-sections: true
    toc: false
    colorlinks: true
    linkcolor: "blue"
    linestretch: 1.25
    mainfont: "Source Sans Pro"
    sansfont: "Source Sans Pro"
    monofont: "Source Code Pro"
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

## Step 2: Handle the Abstract as YAML Frontmatter

The abstract must be in the YAML frontmatter of `paper.qmd`, NOT as body content. This means:

### 2a: Create a post-sync script

Create `paper/fix_frontmatter.py` that:
1. Reads `paper/sections/00_abstract.md`, strips the `# Abstract` heading, extracts the body text
2. Reads `paper/paper.qmd` as produced by `seldon paper sync`
3. If `paper.qmd` starts with YAML frontmatter (`---`), updates the `abstract:` field
4. If `paper.qmd` has no YAML frontmatter, prepends a frontmatter block
5. Removes the `# Abstract` section from the body content (since it's now in frontmatter)
6. Writes the updated `paper.qmd`

The frontmatter block should be:

```yaml
---
title: "Wrong-Limit Attractors: Why Constraining the Search Space Dominates Fitness Engineering for Discovery of Convergent Processes"
author: "Brock Webb"
date: "March 2026"
thanks: "The views expressed are the author's own and do not necessarily represent the views of the U.S. Census Bureau or the U.S. Department of Commerce."
abstract: |
  [abstract text extracted from 00_abstract.md, indented 2 spaces per line]
---
```

The script should be idempotent: running it twice produces the same result.

### 2b: Update the post-sync workflow

After running `seldon paper sync`, always run:
```bash
python paper/fix_frontmatter.py
```

This becomes part of the standard pipeline:
```bash
seldon paper sync
python paper/fix_frontmatter.py
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
```

---

## Step 3: Verify Section Numbering

With the abstract moved to YAML frontmatter, the first body section should be Introduction (numbered as Section 1 by Quarto). Check that:
- All section headings in section files do NOT have manual numbers (they should have been stripped by the previous formatting task)
- If they still have manual numbers, strip them now:
  - `# 1. Introduction` → `# Introduction`
  - `# 2. Background` → `# Background`
  - etc.
- Subsection headings (##, ###) should also be stripped of manual numbers if `number-sections: true` handles them

---

## Step 4: Font Availability

Check that Source Sans Pro is installed:
```bash
fc-list | grep -i "source sans"
```

If not installed:
```bash
brew install --cask font-source-sans-3
```

If brew is not available or installation fails, fall back to the QUARTO_SPEC fallback: `mainfont: "Palatino"` and note the failure.

---

## Step 5: Build and Verify

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon paper sync
python paper/fix_frontmatter.py
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
```

Open the PDF and verify:
- Title, author, date on first page (not ISO format)
- Census disclaimer in first-page footnote
- Abstract is unnumbered, bold-centered heading (matching Image 2 / Crosswalk paper style)
- Section 1 is Introduction (not Abstract)
- Font is Source Sans Pro (sans-serif body, distinct from the serif Palatino)
- Sections are auto-numbered correctly
- No doubled numbering
- All figures, tables, bibliography render

---

## Do NOT

- Do not modify abstract prose content (only move it from body to YAML field)
- Do not modify any section file content other than stripping manual section numbers
- Do not modify existing CC task files
- Do not change the abstract text
- Do not delete `paper/sections/00_abstract.md` (Seldon tracks it; just exclude it from body assembly via the fix_frontmatter.py script)
