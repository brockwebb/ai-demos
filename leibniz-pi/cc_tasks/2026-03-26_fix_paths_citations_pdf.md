# CC Task: Fix Figure Paths + Convert Citations to Pandoc Format + Build PDF

**Date:** 2026-03-26
**Priority:** High (blocks PDF build)

---

## Objective

1. Fix figure image paths in section files so Quarto can resolve them
2. Convert all in-text citations from `(Author, Year)` to Pandoc `[@key]` format
3. Rebuild the paper as PDF

---

## Pre-Flight

1. Read `paper/conventions.md`
2. Read `paper/references.bib` — extract all BibTeX keys for the citation conversion map
3. Read each section file BEFORE editing

---

## Step 1: Fix Figure Paths

In `paper/sections/05_results.md` and `paper/sections/06_discussion.md`, change all figure image paths from `../figures/` to `figures/`.

Find and replace in 05_results.md:
- `../figures/fig2_precision_vs_T.png` → `figures/fig2_precision_vs_T.png`
- `../figures/fig1_scaling_heatmap.png` → `figures/fig1_scaling_heatmap.png`
- `../figures/fig3_parsimony_collapse.png` → `figures/fig3_parsimony_collapse.png`

Find and replace in 06_discussion.md:
- `../figures/fig4_second_order_kinetics.png` → `figures/fig4_second_order_kinetics.png`
- `../figures/fig4b_second_order_loglog.png` → `figures/fig4b_second_order_loglog.png` (if present)

**Verification:** After editing, confirm each path exists:
```bash
ls -la /Users/brock/Documents/GitHub/ai-demos/leibniz-pi/paper/figures/fig*.png
```

---

## Step 2: Convert Citations to Pandoc Format

Convert all in-text citations to Pandoc `[@key]` format. The mapping below is authoritative — read from `references.bib`.

### Citation Conversion Map

**Narrative citations** (Author name is part of the sentence): use `@key` (no brackets)
**Parenthetical citations** (Author name is in parentheses): use `[@key]`
**Multiple authors in one parenthetical**: use `[@key1; @key2]`

| In-text form | BibTeX key | Pandoc form |
|---|---|---|
| Schmidt and Lipson (2009) | Schmidt2009Distilling | @Schmidt2009Distilling |
| Hillar and Sommer (2012) | Hillar2012Comment | @Hillar2012Comment |
| Goldberg, 1989 | Goldberg1989GA | @Goldberg1989GA |
| Deb and Goldberg, 1993 | Deb1993Deceptive | @Deb1993Deceptive |
| Cranmer, 2023 | Cranmer2023PySR | @Cranmer2023PySR |
| Valipour et al., 2021 | Valipour2021SymbolicGPT | @Valipour2021SymbolicGPT |
| Li et al., 2023 | Li2023GFlowNet | @Li2023GFlowNet |
| Kamienny et al., 2023 | Kamienny2023MCTS | @Kamienny2023MCTS |
| Shojaee et al., 2023 | Shojaee2023TPSR | @Shojaee2023TPSR |
| Jiang et al., 2025 | Jiang2025EGGSR | @Jiang2025EGGSR |
| Abdusalamov et al. (2023) | Abdusalamov2023Asymptotic | @Abdusalamov2023Asymptotic |
| Poli, Langdon, and McPhee, 2008 | Poli2008FieldGuide | @Poli2008FieldGuide |
| Poli, Langdon, and McPhee (2008) | Poli2008ParsimonyEasy | Check context — may be FieldGuide or ParsimonyEasy |
| Soule and Foster, 1998 | Soule1998CodeGrowth | @Soule1998CodeGrowth |
| Sastry (2005) | Sastry2005PopulationSizing | @Sastry2005PopulationSizing |
| Murphy et al. | Murphy2019GEFS | @Murphy2019GEFS |
| Luke et al. (2003) | Luke2003PopulationSizing | @Luke2003PopulationSizing |

### Rules for conversion

1. Read each section file before editing.
2. For each citation found, determine if it is narrative or parenthetical:
   - **Narrative:** "Schmidt and Lipson (2009) showed that..." → "@Schmidt2009Distilling showed that..."
   - **Parenthetical:** "...(Schmidt and Lipson, 2009)" → "...[@Schmidt2009Distilling]"
   - **Parenthetical multi:** "...(Poli, Langdon, and McPhee, 2008; Soule and Foster, 1998)" → "...[@Poli2008ParsimonyEasy; @Soule1998CodeGrowth]"
3. **Disambiguation:** "Poli, Langdon, and McPhee" appears as both FieldGuide and ParsimonyEasy. Check context:
   - If discussing bloat/field guide basics → `Poli2008FieldGuide`
   - If discussing parsimony pressure specifically → `Poli2008ParsimonyEasy`
   - The section 2.3 reference about bloat = FieldGuide
   - The section 5.4 reference about parsimony threshold = ParsimonyEasy
4. After conversion, do a grep to confirm NO unconverted `(Author, YYYY)` patterns remain.

**Verification:**
```bash
# Should return 0 results after conversion
grep -nE '\([A-Z][a-z]+ (and |et al)[^)]*[0-9]{4}\)' paper/sections/*.md
grep -nE '[A-Z][a-z]+ and [A-Z][a-z]+ \([0-9]{4}\)' paper/sections/*.md
grep -nE '[A-Z][a-z]+ et al\. \([0-9]{4}\)' paper/sections/*.md
```

---

## Step 3: Rebuild

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon paper sync
seldon paper build --no-render
cd paper
quarto render paper.qmd --to pdf
cp paper.pdf ../leibniz-pi-draft.pdf
echo "PDF built at leibniz-pi-draft.pdf"
```

If PDF build fails, capture the error and also build HTML:
```bash
quarto render paper.qmd --to html
echo "HTML fallback built at paper.html"
```

---

## Step 4: Orphan .bib Check

After citation conversion, check for .bib entries with no `@key` reference in any section:

```bash
# Extract all .bib keys
grep -ohE '^@[a-z]+\{[^,]+' paper/references.bib | sed 's/@[a-z]*{//' | sort > /tmp/bib_keys.txt

# Extract all @key references in sections
grep -ohE '@[A-Za-z0-9_]+' paper/sections/*.md | sed 's/^@//' | sort -u > /tmp/cited_keys.txt

# Find orphans
echo "=== Orphan .bib entries (in .bib but never cited) ==="
comm -23 /tmp/bib_keys.txt /tmp/cited_keys.txt
```

Report orphans but do not remove them.

---

## Post-Flight

1. Run `python paper/prose_qc.py` — confirm Tier 2 = 0
2. Run `python paper/check_glossary.py` — confirm 0 violations
3. Confirm PDF exists at `leibniz-pi-draft.pdf`
4. Report: PDF status, orphan .bib count, any remaining issues

---

## Do NOT

- Do not modify prose content beyond citation format changes and figure path fixes
- Do not remove any .bib entries (report orphans only)
- Do not overwrite any existing CC task files
- Do not change any `{{result:...}}` references
