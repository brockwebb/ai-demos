# Handoff: Editorial Cuts Complete, Final QC Remains

**Date:** 2026-04-01
**From:** Claude Desktop (editorial cut session)
**To:** Next Claude thread (final QC + PDF render)

---

## Status: All content and editorial work complete. Final QC pass and PDF render remain.

---

## What Was Accomplished This Session

### Crystallization / Design Provenance Purge
- Removed crystallization paragraph from Section 3.3.2 (Methods, Log-Precision Fitness)
- Deleted Section 6.5 (Design Provenance and Disciplinary Lens) entirely, nothing salvaged
- Removed defensive disclaimer paragraph from Section 6.1 ("We present this as a structural observation recognized after the experiment...")
- Removed self-congratulatory paragraph from Section 6.1 ("The design intuition and the kinetics mathematics arrived at the same place...")
- Section 6.1 now ends with the math: second-order question, constant bits-per-decade, fewer processes satisfy this criterion

### "Encodes Domain Knowledge" Language Killed
- Last sentence of Section 5.6 replaced: "encodes domain knowledge about the target process's convergence rate" replaced with plain language ("The threshold must be set below the target process's natural gain rate. It is constrained by the problem, not freely tunable.")

### Conclusion Paragraph 3 Replaced
- Old: re-explained the combinatorial mechanism for the sixth time, bare assertion "feature selection matters more than model architecture"
- New: concrete outward connections (prompt specificity constrains LLM search space, training data curation removes irrelevant primitives) without re-explaining the mechanism the reader already knows
- No em dashes in replacement text

### Redundancy Audit
The combinatorial explosion argument appeared in six places (Introduction, Background 2.3, Results 5.3, Results 5.5, Discussion 6.2, Conclusion). Introduction and Conclusion bookends are fine. Background defining the concept is fine. Results stating diagnosis against data is fine. The Conclusion was the offender, re-explaining for four sentences before connecting outward. Fixed.

### Kinetics Labels Preserved
"First-order" and "second-order" labels remain in Sections 3.3.1, 3.3.2, and 6.1. They are compact shorthand for "is error shrinking?" vs "is precision gain constant?" and carry analytical weight backed by the data. No changes.

---

## What Still Needs Doing

### High priority

| Task | Notes |
|------|-------|
| Final PDF render + visual verification | Confirm abstract unnumbered, Source Sans Pro (or Palatino fallback), Census disclaimer, section numbering, figures, tables, bibliography |
| Final `prose_qc` run | `python paper/prose_qc.py` and `python paper/check_glossary.py` against all sections after all edits |

### Medium priority

| Task | Notes |
|------|-------|
| Title review | Current: "The Evaluation Horizon Trap: Why Search Space Structure Dominates Fitness Design" -- may want to tighten or reconsider |
| Font issue | Known: Palatino rendering instead of Source Sans Pro due to TeX Live version mismatch, requires manual resolution |

### Low priority

| Task | Notes |
|------|-------|
| Medium article | Summary linking to preprint. Not started. Deprioritized. |
| Seldon DataFile registration | 20+ DataFile artifacts in proposed state. Not blocking. |
| Heatmap figure cleanup | `fig1_scaling_heatmap.{png,pdf}` still in `paper/figures/` but unreferenced. Can delete or leave. |

---

## Section Status

| Section | Status |
|---------|--------|
| 00 Abstract | Done -- ~170 words, in YAML frontmatter via Seldon build |
| 01 Introduction | Done |
| 02 Background | Done |
| 03 Methods | Done -- crystallization paragraph removed from 3.3.2 |
| 04 Experimental Design | Done |
| 05 Results | Done -- 5.6 last sentence cleaned up |
| 06 Discussion | Done -- 6.5 deleted, 6.1 trimmed (two paragraphs removed) |
| 07 Conclusion | Done -- paragraph 3 replaced with outward connections |
| 08 References | Done |
| 09 Appendix | Done |

---

## CC Tasks Created This Session

| Task | Status |
|------|--------|
| `2026-03-28_cut_crystallization_from_methods.md` | Complete -- cuts in 03, 05, 06 |
| `2026-03-28_conclusion_paragraph3_replace.md` | Complete -- conclusion paragraph 3 |

---

## Key Principles (Unchanged)

- All implementation through CC task files in `cc_tasks/`
- Never overwrite existing CC task files (write addendums instead)
- After any edit: `check_glossary.py` -> `seldon paper sync` -> `seldon paper build --no-render` -> `quarto render paper/paper.qmd --to pdf`
- No em dashes (use commas). "Log-precision fitness." "Discovery." "Coverage." "We" throughout.
- Paper is about structural limits of finite evaluation, not about GP.
- Reference QUARTO_SPEC at `central_library/templates/quarto/QUARTO_SPEC.md` for formatting standards.

---

## Key Files

| File | Contents |
|------|---------|
| `paper/frontmatter.yml` | YAML frontmatter: title, author, date, thanks, fonts, LaTeX config |
| `paper/sections/00_abstract.md` | Abstract source (injected into YAML by Seldon build) |
| `paper/sections/*.md` | All paper sections (10 files, 00-09) |
| `paper/figures/*.{pdf,png}` | Publication figures (Fig 1-3 active, heatmap files orphaned) |
| `paper/_quarto.yml` | Quarto build config |
| `central_library/templates/quarto/QUARTO_SPEC.md` | Canonical formatting spec |

---

## Do NOT

- Do not rerun any experiments
- Do not modify existing CC task files
- Do not hardcode values
- Do not use "entropy fitness" -- use "log-precision fitness"
- Do not frame the paper as being about GP
- Do not use em dashes
- Do not re-add crystallization, design provenance, or "domain knowledge encoding" language
