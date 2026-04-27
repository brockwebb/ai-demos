# Handoff: Figures Complete, Fact-Check Complete, Tier 2 QC Complete

**Date:** 2026-03-25
**From:** Claude Desktop (figures + fact-check thread)
**To:** Next Claude thread (abstract + final assembly)

---

## Status: All Body Sections Reviewed, Figures Done, Fact-Check Done, Abstract Remains

---

## What Was Accomplished This Session

### Figures (CC task: `2026-03-24_paper_figures.md`)

Four publication-quality figures generated using plotnine/matplotlib with Census Bureau visual standards:

| Figure | File | Section | Shows |
|--------|------|---------|-------|
| Fig 1 | `paper/figures/fig1_scaling_heatmap.{pdf,png}` | 5.3 | 7×4 discovery rate grid, phase transition at t=8→10 |
| Fig 2 | `paper/figures/fig2_precision_vs_T.{pdf,png}` | 5.2 | Leibniz vs wrong-limit attractor precision trajectories |
| Fig 3 | `paper/figures/fig3_parsimony_collapse.{pdf,png}` | 5.4 | Fitness vs λ_p with crossover point |
| Fig 4 | `paper/figures/fig4_second_order_kinetics.{pdf,png}` | 6.1 | 1/error vs T linearity (second-order rate structure) |
| Fig 4b | `paper/figures/fig4b_second_order_loglog.{pdf,png}` | 6.1 | Same as Fig 4, log-log axes |

All figures verified against registered Seldon results. White background, colorblind-friendly palettes, 300 DPI PNG + vector PDF.

### Fact-Check Pass (Tier 1, 2, 3)

**Tier 1 — Novelty claims (via Perplexity):**
- Process-level fitness for convergent series: NOVEL, unexplored in literature
- Wrong-limit attractors as distinct failure mode: NOVEL
- Evaluation horizon trap: NOVEL, not formalized anywhere
- No prior GP work on rediscovering known convergent infinite series

**Tier 2 — Citation verification:**
- Kamienny 2023 (ICML, MCTS): ✓ verified
- Shojaee 2023 (NeurIPS, TPSR): ✓ verified
- Li 2023 (NeurIPS AI4Science, GFN-SR): ✓ verified, was missing from .bib → added
- Jiang 2025 (arXiv, EGG-SR): ✓ verified, was missing from .bib → added
- "5 billion terms for 10 digits": ✓ confirmed via sharper bounds
- NIST AI 600-1 confabulation definition: ✓ confirmed
- Schmidt/Lipson 2009: claimed Hamiltonians, Lagrangians, conservation laws → ✓ accurate
- Hillar/Sommer 2012: critique was about fitness function encoding Hamilton's equations → **characterization in Section 2.1 was corrected** (was "operator set," now "fitness function")

**Tier 3 — Strengthening citations:**
- GP parameters (k=7, crossover/mutation rates, safe division=1.0): all standard per Koza/Poli Field Guide
- Parsimony pressure threshold: supported by Poli & McPhee (2008), Soule & Foster (1998) → cited in Section 5.4
- Population sizing theory: Luke et al. (2003) building-block population sizing → cited in Section 6.2
- Terminal pruning prior art: Murphy et al. GEFS → cited in Section 7
- Phase transitions in GP: not rigorously formalized by anyone; our quantitative data is the contribution
- Feature selection > architecture: well-supported empirically, not controversial
- Process-level evaluation: exists in training dynamics literature but not in SR fitness design

### CC Tasks Executed This Session (7 total)

| Task | Sections | Summary |
|------|----------|---------|
| `2026-03-24_paper_figures.md` | 5.2, 5.3, 5.4, 6.1 | Four publication figures generated |
| `2026-03-24_deception_lit_and_abdusalamov.md` | 02, refs | Deception lit connection + Abdusalamov citation added |
| `2026-03-24_tier2_prose_qc.md` | 01-07 | Tier 2 prose violations scanned and fixed, `prose_qc.py` created |
| `2026-03-24_fact_check_queries.md` | — | Reference document (not a CC task; query list for Perplexity) |
| `2026-03-25_citation_fixes.md` | 02, refs | Li/Jiang .bib entries, Hillar/Sommer fix, double-Li resolution |
| `2026-03-25_tier3_bibliography_expansion.md` | 05, 06, 07, refs | Poli, Soule, Luke, Murphy citations + prose insertions |

### New .bib entries added this session

| Key | Paper |
|-----|-------|
| `Abdusalamov2023Asymptotic` | Asymptotic expansions via SR (Mechanics Research Communications) |
| `Deb1993Deceptive` | Deceptive problems in GAs (Foundations of GA) |
| `Li2023GFlowNet` | GFN-SR (NeurIPS 2023 AI4Science) |
| `Jiang2025EGGSR` | EGG-SR equality saturation (arXiv 2025) |
| `Kamienny2023MCTS` | MCTS for SR (ICML 2023) |
| `Shojaee2023TPSR` | TPSR (NeurIPS 2023) |
| `Poli2008ParsimonyEasy` | Parsimony Pressure Made Easy (GECCO 2008) |
| `Soule1998CodeGrowth` | Code growth and parsimony (Evolutionary Computation) |
| `Luke2003PopulationSizing` | Population sizing for GP (arXiv) |
| `Murphy2019GEFS` | Grammar-based feature selection for SR (GECCO) |

---

## What Still Needs Doing

### High priority

| Task | Notes |
|------|-------|
| **Abstract (00)** | Must be written last. Should mirror the conclusion. Not GP-centric. Must name both fitness functions. Must include the second-order kinetics connection. No formula detail. No Shannon/entropy language. |
| **Figure placement** | Figures exist in `paper/figures/` but are not yet referenced in the section .md files with proper figure tags/captions. Need to add figure references and captions to sections 5.2, 5.3, 5.4, 6.1. |

### Medium priority

| Task | Notes |
|------|-------|
| **References (08)** | Now has ~20+ entries. Should be audited for completeness: all in-text citations present in .bib, no orphan entries. |
| **Appendix (09) verification** | Created in a previous session. Worth a quick verify pass. |
| **Final Tier 2 re-check** | After all edits, re-run `python paper/prose_qc.py` to confirm 0 violations. |
| **Seldon open tasks** | Run `seldon task list --open` to check. |

### Low priority

| Task | Notes |
|------|-------|
| **Medium article** | Becomes a summary linking to preprint once paper is complete. Not started. |

---

## Section Status After This Session

| Section | Status |
|---------|--------|
| 00 Abstract | NOT WRITTEN — do last |
| 01 Introduction | Reviewed, edited, QC'd ✓ |
| 02 Background | Reviewed, edited, QC'd, Hillar/Sommer fixed, Abdusalamov + deception lit added ✓ |
| 03 Methods | Verified, edited, QC'd ✓ |
| 04 Experimental Design | Reviewed, edited, QC'd ✓ |
| 05 Results | Editorial decisions resolved, figures created, parsimony citations added ✓ |
| 06 Discussion | Reviewed, edited, QC'd, coverage citation added ✓ |
| 07 Conclusion | Reviewed, edited, QC'd, GEFS citation added ✓ |
| 08 References | Expanded (10 new entries), needs final audit |
| 09 Appendix | Done (previous session), verify recommended |

---

## Key Principles (Unchanged)

### Seldon awareness
- All implementation goes through CC task files in `cc_tasks/` with naming convention `YYYY-MM-DD_<descriptive_slug>.md`.
- All research numbers use `{{result:NAME:value}}` references. Never write literal measured values.
- After any edit: `python paper/check_glossary.py` → `seldon paper sync` → `seldon paper build --no-render`.

### CC task discipline
- **Never overwrite an existing CC task file.** Write a new one.
- **Never hardcode values in CC tasks.** CC discovers all values from source.
- **Read before editing.** Always read current file state before any edit.

### Writing conventions
- Read `paper/conventions.md` before writing any prose.
- No em dashes. No bold in prose. No "novel." Max 35 words per sentence. "We" throughout.
- "Log-precision fitness" not "entropy fitness." "Discovery" not "rediscovery." "Coverage" not "diversity."
- Thermodynamic framing belongs only in Section 6.5. Kinetics framing belongs in 3.3 and 6.1.

### Brock's working style
- Discuss before executing. Do not edit files without explicit approval.
- Lead with findings, not process.
- Do not waste context on discovery work CC can do.

---

## Key Files

| File | Contents |
|------|---------|
| `paper/sections/*.md` | All paper sections (10 files, 00-09) |
| `paper/figures/*.{pdf,png}` | Publication figures (5 files) |
| `paper/conventions.md` | Writing rules |
| `paper/prose_qc.py` | Automated Tier 2 prose checker (new this session) |
| `paper/paper_qc_config.yaml` | Machine-checkable prose rules (Tier 2) |
| `paper/paper_style_config.yaml` | Banned words and clichés (Tier 3) |
| `paper/expression_catalog.json` | 260 expressions, machine-readable |
| `paper/references.bib` | BibTeX (expanded this session) |
| `paper/evidence_map.md` | Results → claims mapping |
| `cc_tasks/2026-03-24_fact_check_queries.md` | Perplexity query reference doc |
| `RESEARCH_NOTES.md` | Master findings |
| `RESEARCH_NOTES_SUPP_core_finding.md` | The thesis |
| `RESEARCH_NOTES_SUPP_design_motivation.md` | ChemE lens |

---

## Do NOT

- Do not rerun any experiments
- Do not modify existing CC task files without explicit approval
- Do not hardcode values — everything discovered from source
- Do not use "entropy fitness" — use "log-precision fitness"
- Do not frame the paper as being about GP
- Do not fabricate provenance — flag missing source as a problem
