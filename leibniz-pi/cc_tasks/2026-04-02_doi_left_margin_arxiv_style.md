# CC Task: Add DOI to First Page Left Margin (arXiv Style)

**Date:** 2026-04-02
**Supersedes:** `2026-04-02_doi_first_page_header.md` (do NOT execute that task)
**Purpose:** Add the Zenodo DOI as a rotated vertical identifier in the left margin of the first page, similar to arXiv's identifier placement.

---

## Pre-Flight

1. Read `paper/frontmatter.yml`
2. Review the reference screenshot style: rotated 90° counter-clockwise text in the left margin, running vertically alongside the first page content

---

## Steps

### Step 1: Add rotated left-margin DOI

In `paper/frontmatter.yml`, inside the `include-in-header: text:` block, add:

```latex
\usepackage{fancyhdr}
\usepackage{everypage}
\newcommand{\doimark}{%
  \begin{picture}(0,0)
    \put(-42,-450){\rotatebox{90}{\footnotesize\texttt{DOI:~10.5281/zenodo.19393492}}}
  \end{picture}
}
\fancypagestyle{firstpage}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhead[L]{\doimark}
}
\AtBeginDocument{\thispagestyle{firstpage}}
```

**Positioning notes:** The `\put(-42,-450)` coordinates control horizontal offset from the left edge and vertical position down the page. These values are approximate for letter paper with 1in margins. If the text doesn't align well vertically centered on the first page, adjust:
- First value (horizontal): more negative = further left into margin
- Second value (vertical): more negative = further down the page

An alternative approach using `textpos` if `picture` positioning is unreliable:

```latex
\usepackage{fancyhdr}
\usepackage{textpos}
\usepackage{rotating}
\fancypagestyle{firstpage}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \fancyhead[L]{%
    \begin{textblock*}{1cm}(0.4cm,0.5\textheight)
      \rotatebox{90}{\footnotesize\texttt{DOI:~10.5281/zenodo.19393492}}
    \end{textblock*}
  }
}
\AtBeginDocument{\thispagestyle{firstpage}}
```

Try the `textpos` version first — it's more predictable for positioning.

### Step 2: Verify no fancyhdr conflict

Check that `fancyhdr` is not already loaded elsewhere in the header block. If it is, do not add a duplicate `\usepackage{fancyhdr}`.

---

## Post-Flight

```bash
seldon paper sync
seldon paper build --no-render
quarto render paper/paper.qmd --to pdf
seldon verify --fix
```

Visually confirm:
- DOI text appears in the left margin of page 1 only
- Text is rotated 90° counter-clockwise (reads bottom-to-top)
- Text is vertically centered or near-centered on the page
- Small monospace font
- No header rule visible
- No DOI on any subsequent pages

If positioning is off, adjust the coordinates and re-render until it matches the arXiv-style placement.

---

## Do NOT

- Do not execute the superseded task `2026-04-02_doi_first_page_header.md`
- Do not add the DOI to any other page
- Do not modify any section files
- Do not modify any existing CC task files
- Do not change the font, title, date, or any other frontmatter field
