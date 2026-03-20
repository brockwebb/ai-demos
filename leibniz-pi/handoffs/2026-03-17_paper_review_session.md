# Handoff: Paper Review and Editing Session

**Date:** 2026-03-17
**From:** Claude Desktop (paper review thread)
**To:** Next Claude thread (continue paper review)

---

## Status: Conclusion Rewritten, Expression Catalog Complete, Body Sections Need Review

---

## What Was Accomplished This Session

### 1. Conclusion rewritten (Section 07)

The old conclusion was a three-paragraph results recap that buried the thesis and never mentioned the ML parallel. The new conclusion leads with the finding from RESEARCH_NOTES_SUPP_core_finding.md:

- **Paragraph 1:** Constrain primitives. 4 terminals works, 15 doesn't. Not the fitness, not the algorithm. The search space.
- **Paragraph 2:** No fitness modification fixed it. Parsimony/regularization has a hard ceiling.
- **Paragraph 3:** The ML transfer. Feature selection > model architecture. Wrong-limit attractors = overfitting. Noise terminals drown signal.
- **Paragraph 4:** Three future directions (building block init, terminal pruning, island migration). Brief, no implementation detail.

File: `paper/sections/07_conclusion.md` — written directly, current version is authoritative.

### 2. Abstract drafted but NOT finalized

Multiple drafts were discussed. Key decisions made:
- Abstract should mirror the conclusion (write conclusion first, abstract matches it)
- Must NOT be GP-centric. GP is the search method, not the subject. Say "evolutionary search" or "search algorithm."
- Must name both fitness functions (convergence-aware and log-precision)
- Must name the second-order kinetics connection explicitly, not bury it
- Must not contain `-log₂(|error|)` formula detail or Shannon disclaimers
- Opening hook direction: "With a handful of arithmetic primitives, a target constant, and the right fitness function, can a machine discover one of mathematics' most famous series from scratch?"
- Brock noted this hook may be more Introduction than Abstract. The abstract needs correct terminology and accurate claims; style is secondary until body stabilizes.

File: `paper/sections/00_abstract.md` — the current file content was updated by CC during namespace cleanup but the prose has NOT been rewritten to match the new conclusion. Still needs rework.

### 3. Expression catalog created (Appendix A)

CC task extracted 260 expressions from 52 JSON files across all experiments:
- 52 Leibniz-equivalent (all verified via sympy, all simplify to (-1)^k/(2k+1))
- 179 wrong-limit attractors
- 29 trivial/parsimony-collapsed

File: `paper/sections/09_appendix_expressions.md`
Machine-readable: `paper/expression_catalog.json`
63 DataFile artifacts registered in Seldon with provenance.

### 4. Grandi-Leibniz attractor added to appendix

CC task discovered all data from source files (no hardcoded values):
- Raw expression from `scaling_heatmap_t4_p2000_data.json`: 13 nodes, fitness 0.00877
- Sympy simplified: `-2k(-1)^k / (2k+1)`
- Algebraic decomposition verified computationally: `S(T) = S_Leibniz(T) - G(T)`
- Checkpoint parity counted from source script: 1 odd, 10 even
- Two new verified results registered: `grandi_leibniz_ti_t5_0_07` and `grandi_leibniz_mean_rate_4_61`
- Section A.2.3 added with full decomposition
- Simplified column added to all A.2 attractor entries via sympy

### 5. Namespace cleanup completed

CC renamed all `entropy_` prefixed Seldon result references to `logprec_` throughout paper sections and the graph. Build passes Tier 1 clean.

### 6. Results section (05) reviewed — issues identified and partially addressed by CC

CC addressed most review items with editorial comments and fixes:
- Missing seed 137 added to Table 2
- Scaling grid now uses `{{result:...}}` references (all 28 cells registered)
- "Table 2" dangling reference fixed
- "information rate" → "precision gain rate" in 5.5
- Parsimony values now use result references
- Section 5.4 renamed to "Size Penalty"

Editorial comments remain in the file for unresolved decisions (marked with `<!-- EDITORIAL REVIEW -->`).

### 7. Glossary bug fixed

Parsimony pressure entry reformatted — inline bold definition format was preventing regex matching.

---

## What Still Needs Doing

### Paper sections not yet reviewed in detail

| Section | Status | Priority |
|---------|--------|----------|
| 00_abstract | Needs rewrite to match new conclusion | HIGH (but do last) |
| 01_introduction | Not reviewed this session | HIGH |
| 02_background | Not reviewed this session | MEDIUM |
| 03_methods | Reviewed by swarm (previous session), fixes applied | LOW (verify only) |
| 04_experimental_design | Not reviewed this session | MEDIUM |
| 05_results | Reviewed, editorial comments pending decisions | HIGH |
| 06_discussion | Not reviewed this session | HIGH |
| 07_conclusion | Rewritten this session | DONE |
| 08_references | Not reviewed | LOW |
| 09_appendix | Created this session | DONE (verify) |

### Open editorial decisions in 05_results

These are marked with `<!-- EDITORIAL REVIEW -->` comments in the file:
1. **Non-monotonicity speculation (5.3):** Cut the speculative explanation for t=15/p=10000 recovery, or weaken it? The 2/5 could be noise at 5 seeds per cell.
2. **Other seeds at t=15 (5.2):** What did seeds 7, 137, 2718, 31415 find at 15 terminals? Data may be in the JSON files.
3. **Repetition of "coverage not fitness" (5.5):** Appears in 5.3, 5.5, Discussion, and Conclusion. Decide which instances to keep.
4. **GP comparison grid missing from Results:** Data exists (handoff 2026-03-16). Consider adding Section 5.6.
5. **Extended time test missing from Results:** GP conv-aware at t=10/p=5000, 2hr/seed, 1/5. Strong evidence time isn't the bottleneck.
6. **Figures not yet created:** Scaling grid heatmap, precision vs T plot, parsimony collapse plot.

### Open Seldon tasks (18 as of session start, some may have been addressed)

Run `seldon task list --open` to get current count. The RED TEAM tasks are the most relevant:
- Literal X/5 values in prose (may be resolved by result reference registration)
- Table 2 cross-reference (resolved)
- Confabulation analogy not previewed in Introduction
- Search space size quantification
- Checkpoint count confound (11 vs 5)
- Safe division return value = implicit terminal
- Monotonicity threshold rationale

---

## Key Principles for Next Thread

### Seldon awareness
- This is a Seldon-managed project. Run `seldon go --brief --project-dir /Users/brock/Documents/GitHub/ai-demos/leibniz-pi` to orient.
- All implementation goes through CC task files in `cc_tasks/` with naming convention `YYYY-MM-DD_<descriptive_slug>.md`.
- Paper sections live in `paper/sections/NN_name.md`.
- All research numbers use `{{result:NAME:value}}` references. Never write literal measured values.

### CC task discipline
- **Never overwrite an existing CC task file.** It may already be running. Write a new one.
- **Never hardcode values in CC tasks.** All numbers, expressions, fitness scores, node counts, checkpoint counts must be discovered from source files (`_data.json`, scripts) or the Seldon graph. The task spec tells CC *what to look for* and *where to look*, not *what the answers are*.
- **Read before editing.** Always read the current file state with `Filesystem:read_text_file` before any edit.

### Writing conventions
- Read `paper/conventions.md` before writing any prose.
- No em dashes. No bold in prose. No "novel." Max 35 words per sentence. "We" throughout.
- "Log-precision fitness" not "entropy fitness." "Discovery" not "rediscovery." "Coverage" not "diversity."
- The paper is NOT about GP. GP is the search method. The paper is about discovery of convergent processes and why it fails.

### Brock's working style
- Discuss before executing. Do not edit files without explicit approval.
- No rah-rah tone. No self-congratulation. No anthropomorphizing algorithms.
- Lead with findings, not process. Don't make the reader watch you make the sausage.
- Unconventional spelling/grammar may be intentional — don't correct.

---

## Key Files

| File | Contents |
|------|---------|
| `paper/sections/*.md` | All paper sections (10 files, 00-09) |
| `paper/conventions.md` | Writing rules — read before any prose work |
| `paper/paper_qc_config.yaml` | Machine-checkable prose rules (Tier 2) |
| `paper/paper_style_config.yaml` | Banned words and clichés (Tier 3) |
| `paper/expression_catalog.json` | 260 expressions, machine-readable |
| `paper/references.bib` | BibTeX (14 entries) |
| `RESEARCH_NOTES.md` | Master findings, all experiment results |
| `RESEARCH_NOTES_SUPP_core_finding.md` | The thesis: constrain primitives, not algorithms |
| `RESEARCH_NOTES_SUPP_design_motivation.md` | ChemE lens, crystallization analogy |
| `handoffs/2026-03-16_experiments_complete_paper_next.md` | Previous handoff |
| `handoffs/2026-03-17_swarm_test_results.md` | Agent swarm test results |

---

## Seldon Status (as of end of session)

- Graph: 62+ nodes (exact count may have increased with expression catalog registration)
- 63 DataFile artifacts registered for expression catalog
- 2 new verified results: `grandi_leibniz_ti_t5_0_07`, `grandi_leibniz_mean_rate_4_61`
- All `entropy_` result references renamed to `logprec_`
- Build: Tier 1 clean
- `seldon paper sync` baseline established

---

## Do NOT

- Do not rerun any experiments — all data is final
- Do not modify existing CC task files — they may already be running
- Do not hardcode values in CC tasks — everything must be discovered from source
- Do not use "entropy fitness" — use "log-precision fitness"
- Do not frame the paper as being about GP — it's about discovery of convergent processes
- Do not write thermodynamic claims about the fitness function
