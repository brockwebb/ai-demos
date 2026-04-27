# Handoff: Abstract Final, Formatting Fixed, Heatmap Removed

**Date:** 2026-03-28
**From:** Claude Desktop (abstract + formatting + cleanup session)
**To:** Next Claude thread (final QC + Medium article)

---

## Status: Paper content complete. Formatting aligned to QUARTO_SPEC. Final QC pass remains.

---

## What Was Accomplished This Session

### Abstract Rewritten (Multiple Rounds)
- Original abstract was ~300 words, GP-centric, old framing
- Went through 4 iterations: Brock pushed for tighter, less academic prose
- Final version: ~170 words, 3 paragraphs, no throat-clearing
- Leads with the structural problem (finite evaluation of infinite-horizon processes)
- Names both fitness functions, includes threshold sensitivity finding, names second-order convergence
- Closer mirrors the conclusion: "The evaluation function is not the bottleneck. The search space is."

### Seldon Paper Build Fixed (3 tasks in Seldon repo)
- `seldon paper build` now extracts `00_abstract.md` content and injects it as the YAML `abstract:` field in frontmatter
- 3 new private helpers in `seldon/paper/build.py`: `_extract_abstract_text`, `_inject_abstract_into_frontmatter`, `_build_minimal_frontmatter`
- 8 new unit tests, full suite at 349 passed
- Seldon also fixed to preserve font stack from `frontmatter.yml` through sync (no post-sync patching needed)

### Paper Formatting Aligned to QUARTO_SPEC
- `paper/frontmatter.yml` created with Source Sans Pro font stack per QUARTO_SPEC
- Title, author, date, Census disclaimer (`thanks:` field) all in frontmatter
- Keywords added
- `xelatex` engine, `number-sections: true`, booktabs, widow/orphan control
- Reference: `/Users/brock/Documents/GitHub/central_library/templates/quarto/QUARTO_SPEC.md`

### Heatmap Figure Removed
- Figure 2 (scaling heatmap) removed from Section 05 -- Table 5 already has the same data
- Remaining figures renumbered: Fig 1 (precision trajectories) unchanged, Fig 3→2 (parsimony), Fig 4→3 (kinetics)
- All cross-references in prose updated

### References and Appendix Unnumbered
- `# References` → `# References {.unnumbered}`
- `# Appendix A: Expression Catalog` → `# Appendix A: Expression Catalog {.unnumbered}`
- All 11 appendix subsections also marked `{.unnumbered}`

### Heatmap Figure Redesigned (Census Standards)
- CC task ran to fix the heatmap to Census Bureau data viz standards (sequential blue palette, text color bug fixed)
- Figure file still exists in `paper/figures/` but is no longer referenced in the paper

---

## What Still Needs Doing

### High priority

| Task | Notes |
|------|-------|
| Final PDF render + visual verification | Confirm abstract is unnumbered, Source Sans Pro, Census disclaimer, section numbering, figures, tables, bibliography |
| Final `prose_qc` run | After all edits, confirm no new violations from abstract or section number changes |

### Medium priority

| Task | Notes |
|------|-------|
| Title review | Current: "Wrong-Limit Attractors: Why Constraining the Search Space Dominates Fitness Engineering for Discovery of Convergent Processes" -- may want to tighten |
| `\bibliography{references}` cleanup | May still be in paper.qmd at line 363, harmlessly ignored by Pandoc |

### Low priority

| Task | Notes |
|------|-------|
| Medium article | Summary linking to preprint. Not started. |
| Seldon DataFile registration | 20+ DataFile artifacts in proposed state. Not blocking. |
| Open Seldon proposed tasks | 7 RED TEAM tasks -- most addressed in audit |
| Heatmap figure cleanup | `fig1_scaling_heatmap.{png,pdf}` still in `paper/figures/` but unreferenced. Can delete or leave. |

---

## Section Status After This Session

| Section | Status |
|---------|--------|
| 00 Abstract | DONE -- ~170 words, in YAML frontmatter via Seldon build |
| 01 Introduction | Done (rewritten previous session) |
| 02 Background | Done |
| 03 Methods | Done |
| 04 Experimental Design | Done |
| 05 Results | Done -- heatmap removed, figures renumbered |
| 06 Discussion | Done |
| 07 Conclusion | Done |
| 08 References | Done -- marked {.unnumbered} |
| 09 Appendix | Done -- marked {.unnumbered} with all subsections |

---

## CC Tasks Created This Session

| Task | Status |
|------|--------|
| `2026-03-27_abstract_rewrite_and_pdf.md` | Done (superseded by final version) |
| `2026-03-27_fix_heatmap_census_standards.md` | Done |
| `2026-03-27_census_paper_formatting.md` | Done |
| `2026-03-27_abstract_tighten.md` | Done (superseded by final version) |
| `2026-03-27_abstract_final.md` | Done |
| `2026-03-28_fix_formatting_quarto_spec.md` | Superseded by Seldon-side fix |
| `2026-03-28_remove_heatmap_fix_numbering.md` | Done |

---

## Key Principles (Unchanged)

- All implementation through CC task files in `cc_tasks/`
- Never overwrite existing CC task files
- All research numbers use `{{result:NAME:value}}` references
- After any edit: `check_glossary.py` → `seldon paper sync` → `seldon paper build --no-render`
- No em dashes. "Log-precision fitness." "Discovery." "Coverage." "We" throughout.
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
| `paper/conventions.md` | Writing rules |
| `paper/_quarto.yml` | Quarto build config (may be overridden by frontmatter.yml) |
| `central_library/templates/quarto/QUARTO_SPEC.md` | Canonical formatting spec |

---

## Do NOT

- Do not rerun any experiments
- Do not modify existing CC task files
- Do not hardcode values
- Do not use "entropy fitness" -- use "log-precision fitness"
- Do not frame the paper as being about GP
- Do not make direct file changes to Seldon-managed repos from Claude Desktop
- Do not use Palatino -- Source Sans Pro is the canonical font per QUARTO_SPEC
