# Handoff: Full Paper Review Pass

**Date:** 2026-03-20
**From:** Claude Desktop (paper review thread)
**To:** Next Claude thread (abstract, figures, Tier 2 cleanup, final)

---

## Status: All Body Sections Reviewed, Cleanup Complete, Abstract and Figures Remain

---

## What Was Accomplished This Session

### Full review pass across all body sections (01-07)

Every section was read, reviewed for structural, factual, and stylistic issues, and a CC task written and executed. Reviews covered prose quality, conventions compliance, Seldon provenance, cross-reference consistency, and editorial decisions.

### CC tasks executed (7 total)

| Task file | Sections | Summary |
|-----------|----------|---------|
| `2026-03-17_experimental_design_review.md` | 04 | Discovery criterion reframed, terminal expansion rationale, consolidated primitives table, time budgets unified, operator cross-reference, safe division documented |
| `2026-03-18_introduction_review.md` | 01 | Anthropomorphizing fixed, conditions named, kinetics simplified, wrong-limit attractor and coverage defined on first use, confabulation preview, injection confound mention, roadmap added |
| `2026-03-18_discussion_review.md` | 06 | Coverage thesis repetition flagged, editorial comments added to 05 |
| `2026-03-18_background_review.md` | 02 | Literature dump compressed, "to our knowledge" deduplicated, bloat citation added, "infinitely many" softened, π/4 standardized |
| `2026-03-20_methods_verification.md` | 03 | Discovery criterion matched to 4.2, time budgets cross-referenced, "4.4 bits" flagged as wrong from source, config literals verified |
| `2026-03-20_results_editorial_decisions.md` | 05 | All five seeds at t=15 described, speculation cut, coverage thesis softened in 5.3, extended time test added to 5.5, editorial comments cleaned |
| `2026-03-20_consolidated_cleanup.md` | 02, 03, 06 | "0.7851" → symbolic π/4, "4.4 bits" → verified 4.34 at T=5, crystallization paragraph position confirmed, thermodynamic language stripped from 6.2, "calibrated behavior" → "sustained refinement" in 6.3, non-GP paragraph thinned |

### Seldon results registered this session

| Result | Value | Source |
|--------|-------|--------|
| `gp_extended_t10_p5000_1_5` | 1/5 | Extended time test, 7200s/seed |
| `leibniz_prec_t5` | 4.34 bits | -log₂(\|S(5) - π/4\|) from LEIBNIZ_REFS |
| `leibniz_prec_t10` | 5.33 bits | -log₂(\|S(10) - π/4\|) from LEIBNIZ_REFS |
| `gp_engine_safe_div_spec` | (artifact) | Safe division spec with provenance |

### Build status

- Tier 1: Clean (0 violations)
- Tier 2: 23 violations (pre-existing, none introduced this session)

---

## What Still Needs Doing

### High priority

| Task | Notes |
|------|-------|
| **Abstract (00)** | Must be written last, after all body sections stable. Should mirror the conclusion. Not GP-centric. Must name both fitness functions. Must include second-order kinetics connection. No formula detail. No Shannon/entropy language. |
| **Figures** | Four figures TBD (editorial comment remains in 05_results.md): scaling grid heatmap, precision vs T plot, parsimony collapse plot, convergence rate plot. Data exists; figures not yet created. Scope as a dedicated CC task. |
| **Tier 2 cleanup** | 23 violations across the paper. Do a single pass after abstract is written and figures are placed. Likely sentence length and passive voice issues. |

### Medium priority

| Task | Notes |
|------|-------|
| **References (08)** | Not reviewed this session. Low risk but should be audited for completeness (all citations in text present in .bib, no orphan entries). |
| **Appendix (09) verification** | Created previous session, marked done. Worth a quick verify pass. |
| **Seldon open tasks** | Run `seldon task list --open` to check remaining red team tasks. Some may have been resolved by this session's edits. |

### Low priority

| Task | Notes |
|------|-------|
| **Medium article** | Becomes a summary linking to preprint once paper is complete. Not started. |

---

## Section Status After This Session

| Section | Status |
|---------|--------|
| 00 Abstract | NOT WRITTEN — do last |
| 01 Introduction | Reviewed and edited ✓ |
| 02 Background | Reviewed and edited ✓ |
| 03 Methods | Verified and edited ✓ |
| 04 Experimental Design | Reviewed and edited ✓ |
| 05 Results | Editorial decisions resolved ✓ (figures TBD) |
| 06 Discussion | Reviewed and edited ✓ |
| 07 Conclusion | Done (previous session) ✓ |
| 08 References | Not reviewed |
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
- **If a value cannot be verified from source, flag it.** Do not fabricate provenance. Do not register without source. Missing source is a problem to surface, not paper over.
- **Read before editing.** Always read current file state before any edit.

### Writing conventions
- Read `paper/conventions.md` before writing any prose.
- No em dashes. No bold in prose. No "novel." Max 35 words per sentence. "We" throughout.
- "Log-precision fitness" not "entropy fitness." "Discovery" not "rediscovery." "Coverage" not "diversity."
- Thermodynamic framing belongs only in Section 6.5. Kinetics framing belongs in 3.3 and 6.1.

### Brock's working style
- Discuss before executing. Do not edit files without explicit approval.
- Do not waste context on discovery work CC can do. Write the task, let CC discover.
- Lead with findings, not process.

---

## Key Files (Unchanged)

| File | Contents |
|------|---------|
| `paper/sections/*.md` | All paper sections (10 files, 00-09) |
| `paper/conventions.md` | Writing rules |
| `paper/paper_qc_config.yaml` | Machine-checkable prose rules (Tier 2) |
| `paper/paper_style_config.yaml` | Banned words and clichés (Tier 3) |
| `paper/expression_catalog.json` | 260 expressions, machine-readable |
| `paper/references.bib` | BibTeX |
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
