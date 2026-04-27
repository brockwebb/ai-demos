# CC Task: Add DOI to First Page Header

**Date:** 2026-04-02
**Purpose:** Add the Zenodo DOI as a right-aligned header on the first page of the paper.

---

## Pre-Flight

1. Read `paper/frontmatter.yml`

---

## Steps

### Step 1: Add DOI header via fancyhdr

In `paper/frontmatter.yml`, inside the `include-in-header: text:` block, add:

```latex
\usepackage{fancyhdr}
\fancypagestyle{firstpage}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhead[R]{\small\texttt{DOI: 10.5281/zenodo.19393492}}
}
\AtBeginDocument{\thispagestyle{firstpage}}
```

Place it after the existing `\usepackage` lines but before `\raggedbottom`.

### Step 2: Verify no fancyhdr conflict

Check that `fancyhdr` is not already loaded elsewhere in the header block. If it is, do not add a duplicate `\usepackage{fancyhdr}` -- just add the `\fancypagestyle` and `\AtBeginDocument` lines.

---

## Post-Flight

```bash
seldon paper sync
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
seldon verify --fix
```

Visually confirm the DOI appears in the top-right of page 1 only, in a small monospace font, with no header rule.

---

## Do NOT

- Do not add the DOI to any other page
- Do not modify any section files
- Do not modify any existing CC task files
- Do not change the font, title, date, or any other frontmatter field
