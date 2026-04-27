# Handoff: Audit Complete, Introduction Rewritten, Abstract Next

**Date:** 2026-03-27
**From:** Claude Desktop (audit + intro rewrite session)
**To:** Next Claude thread (abstract + final assembly)

---

## Status: All Body Sections Audited and Remediated. Introduction Rewritten. Abstract Remains.

---

## What Was Accomplished This Session

### Table Captions and Figure Placement
- Tables 1-7 captioned across sections 04 and 05
- Figures 1-5 placed with captions in sections 05 and 06
- Figure paths fixed from `../figures/` to `figures/` for Quarto resolution

### Citation Conversion
- All in-text citations converted from `(Author, Year)` to Pandoc `[@key]` format
- Two confabulated citations identified and confirmed non-existent via Perplexity:
  - `Luke2003PopulationSizing` — does not exist; the population sizing paper is Sastry (already in .bib)
  - `Murphy2019GEFS` — does not exist; closest real paper is Ali et al. GECCO 2022
  - Neither citation appeared in section files or .bib, so no broken references to fix

### PDF Build Pipeline
- `_quarto.yml` created with `toc: false`, `number-sections: false`, `bibliography: references.bib`
- PDF builds successfully via `quarto render paper.qmd --to pdf`
- Wide appendix tables (A.1, A.2) wrapped in `\begin{landscape}` with `\small` font
- `\bibliography{references}` in 08_references.md removed; Pandoc generates bibliography from YAML config

### Full Paper Audit
- Audit file: `audits/2026-03-26_full_paper_audit.md`
- Recon report: `audits/2026-03-26_build_recon_report.md`
- Cross-section inconsistencies identified and fixed
- 9 orphan .bib entries removed
- All RED TEAM tasks addressed or explicitly accepted

### Threshold Sensitivity Sweep (NEW FINDING)
- Results: `entropy-leibniz-v3/threshold_sweep/threshold_sensitivity_results.md`
- **Key finding:** Log-precision MIN_GAIN threshold is NOT a free parameter. It must be calibrated to the target's natural precision gain rate.
  - MIN_GAIN=0.1: 2/5 (too permissive)
  - MIN_GAIN=0.5 (baseline): 5/5
  - MIN_GAIN=1.0: 1/5 (at Leibniz's gain rate edge)
  - MIN_GAIN=2.0: 0/5 (above Leibniz's gain rate, fitness collapses)
- Convergence-aware threshold (1%-20%) is insensitive (2-3/5 across all values)
- t=6 boundary test may still be running — check for `threshold_mingain_0.1_t6_data.json`
- CC task `2026-03-26_threshold_sensitivity_paper_addition.md` adds Section 5.6 and connects to 3.3.2 and 6.5

### Introduction Rewrite
- Complete rewrite of Section 01 approved by Brock
- Leads with "why should anyone care" (finite evaluation of infinite-horizon processes)
- Names wrong-limit attractors in paragraph 2 before introducing the experiment
- Connects to RL reward hacking, LLM confabulation, and SR in paragraph 5
- Leibniz and GP positioned as laboratory, not subject
- Key framing: "You cannot close that gap by designing a better test. You can only manage it by constraining the search space."

### Audit Remediation Applied
- Conclusion: "every seed" → "19 of 20 seeds" 
- Conclusion: paragraph structure fixed (First/Second/Third parallel)
- Section 3.3.2: checkpoint sensitivity sentence added
- Section 4.3: safe division implicit terminal clarification added
- Section 2.3: Sastry population sizing previewed
- Section 6.2: "coverage scales linearly" softened

### CC Tasks Executed This Session

| Task | Status | Summary |
|------|--------|---------|
| `2026-03-26_table_figure_captions.md` | Done | Tables 1-7, Figures 1-5 |
| `2026-03-26_build_pdf_audit_recon.md` | Done | First build + recon report |
| `2026-03-26_fix_paths_citations_pdf.md` | Done | Figure paths, citation conversion, PDF |
| `2026-03-26_rebuild_pdf_final.md` | Done | TOC/numbering/references fixes |
| `2026-03-26_appendix_landscape_tables.md` | Done | Landscape tables + rebuild |
| `2026-03-26_audit_remediation_batch1.md` | Done | 5 audit fixes |
| `2026-03-26_audit_remediation_batch2.md` | Done | Sastry preview + coverage softening |
| `2026-03-26_threshold_sensitivity_sweep.md` | Done | Monotonicity threshold experiments |
| `2026-03-26_threshold_sensitivity_paper_addition.md` | Ready | Adds Section 5.6 + connections |
| `2026-03-27_introduction_rewrite.md` | Ready | Full intro replacement |

---

## What Still Needs Doing

### High priority (run these CC tasks in order)

| # | Task | Notes |
|---|------|-------|
| 1 | `2026-03-27_introduction_rewrite.md` | Replace intro with approved rewrite |
| 2 | `2026-03-26_threshold_sensitivity_paper_addition.md` | Add Section 5.6, connect to 3.3.2 and 6.5. Check if t=6 boundary test completed. |
| 3 | **Write abstract (00)** | Must be written last. Constraints below. |
| 4 | **Final PDF build** | `seldon paper sync` → `quarto render paper.qmd --to pdf` |

### Abstract constraints (unchanged + updated)

- Must mirror the conclusion
- Not GP-centric — GP is the laboratory, not the subject
- Must name both fitness functions
- Must include the second-order kinetics connection
- Must include the threshold sensitivity finding
- No formula detail
- No Shannon/entropy language
- Lead with the evaluation horizon trap / wrong-limit attractor framing
- Connect to RL, LLM confabulation, SR implications
- "You cannot close the gap by designing a better test. You can only manage it by constraining the search space."

### Medium priority

| Task | Notes |
|------|-------|
| `\bibliography{references}` in paper.qmd | Still present at line 363, harmlessly ignored by Pandoc. Add a post-sync sed strip if it causes issues. |
| Final prose_qc re-run | After all edits, confirm Tier 2 = 0. New intro may flag sentence length. |

### Low priority

| Task | Notes |
|------|-------|
| Medium article | Summary linking to preprint. Not started. |
| Seldon DataFile registration | 20+ DataFile artifacts in proposed state. Not blocking. |
| Open Seldon proposed tasks | 7 RED TEAM tasks — most addressed in audit. Close or accept. |

---

## Section Status After This Session

| Section | Status |
|---------|--------|
| 00 Abstract | NOT WRITTEN — do last |
| 01 Introduction | REWRITTEN — CC task ready to apply |
| 02 Background | Audited, Sastry preview added ✓ |
| 03 Methods | Audited, checkpoint sensitivity sentence added ✓ |
| 04 Experimental Design | Audited, safe division clarification added ✓ |
| 05 Results | Audited, all tables captioned, figures placed. Section 5.6 pending (threshold sensitivity) |
| 06 Discussion | Audited, coverage softened ✓. Threshold connection to 6.5 pending |
| 07 Conclusion | Audited, "19 of 20" fix applied, parallel structure fixed ✓ |
| 08 References | Orphans removed, citations converted ✓ |
| 09 Appendix | Landscape tables applied ✓ |

---

## Key Principles (Unchanged)

### Seldon awareness
- All implementation goes through CC task files in `cc_tasks/`
- All research numbers use `{{result:NAME:value}}` references
- After any edit: `python paper/check_glossary.py` → `seldon paper sync` → `seldon paper build --no-render`
- **NEVER make direct file changes to a Seldon-managed repo from Claude Desktop**

### CC task discipline
- Never overwrite an existing CC task file
- Never hardcode values in CC tasks
- Read before editing

### Writing conventions
- Read `paper/conventions.md` before writing any prose
- No em dashes. No bold in prose. No "novel." Max 35 words per sentence. "We" throughout.
- "Log-precision fitness" not "entropy fitness"
- "Discovery" not "rediscovery"
- "Coverage" not "diversity"

### Paper framing (UPDATED)
- The paper is NOT about GP. GP is the laboratory.
- The paper is NOT about Leibniz. Leibniz is the test case.
- The paper IS about the structural constraint of finite evaluation of infinite-horizon processes
- Wrong-limit attractors are the central finding
- The evaluation horizon trap is the general principle
- "You cannot close the gap by designing a better test. You can only manage it by constraining the search space."
- Connect to RL reward hacking, LLM confabulation, SR — these are the same structural problem

### New finding this session
- Threshold sensitivity: MIN_GAIN is physically meaningful, not an arbitrary hyperparameter
- Must be calibrated to target process convergence rate
- Adds to the "fitness encodes domain knowledge" narrative in Section 6.5

---

## Key Files

| File | Contents |
|------|---------|
| `paper/sections/*.md` | All paper sections (10 files, 00-09) |
| `paper/figures/*.{pdf,png}` | Publication figures (5 files) |
| `paper/conventions.md` | Writing rules |
| `paper/_quarto.yml` | Quarto build config (PDF + HTML) |
| `paper/prose_qc.py` | Automated Tier 2 prose checker |
| `paper/references.bib` | BibTeX (cleaned this session, ~12 entries) |
| `paper/evidence_map.md` | Results → claims mapping |
| `audits/2026-03-26_full_paper_audit.md` | Complete paper audit |
| `audits/2026-03-26_build_recon_report.md` | Build + mechanical check report |
| `entropy-leibniz-v3/threshold_sweep/threshold_sensitivity_results.md` | Sweep results |
| `cc_tasks/2026-03-24_fact_check_queries.md` | Perplexity query reference |
| `RESEARCH_NOTES.md` | Master findings |

---

## Do NOT

- Do not rerun any experiments (threshold sweep is complete)
- Do not modify existing CC task files
- Do not hardcode values
- Do not use "entropy fitness" — use "log-precision fitness"
- Do not frame the paper as being about GP
- Do not fabricate provenance
- Do not make direct file changes to Seldon-managed repos from Claude Desktop
