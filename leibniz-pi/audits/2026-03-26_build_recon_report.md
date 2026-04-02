# Build Reconnaissance Report

**Date:** 2026-03-26
**Task:** `cc_tasks/2026-03-26_build_pdf_audit_recon.md`

---

## 1. PDF Build Status

**Result: FAILED** (HTML fallback: SUCCESS)

**Error:** LaTeX image path resolution failure. The section files reference figures as `../figures/FILENAME.png` (relative to `paper/sections/`), but Quarto resolves included-file image paths relative to `paper.qmd`'s directory (`paper/`), so `../figures/` resolves to the project root rather than `paper/figures/` where the files live.

```
Package luatex.def Error: File `../figures/fig2_precision_vs_T.png' not found
```

**Root cause:** Figure paths in section files use `../figures/` which is correct from `paper/sections/` but wrong from Quarto's working directory (`paper/`). Correct path for Quarto rendering: `figures/FILENAME.png`.

**Affected figures:** All 4 inserted figure references (fig2, fig1, fig3, fig4 — in sections 05 and 06).

**HTML render:** Succeeded. `paper/paper.html` was generated successfully. HTML resolves paths differently and does not exhibit this error.

**PDF output:** Not produced. `leibniz-pi-draft.pdf` does not exist.

**Action required:** Fix figure paths in section files from `../figures/` to `figures/`. Separate task.

---

## 2. Prose QC (prose_qc.py)

**Result: PASS**

```
SUMMARY: Tier 2=0  Heuristic=41  Tier3=0
```

- **Tier 2 violations:** 0 (PQ-01 sentence length, PQ-02 paragraph size, PQ-03 em dash, PQ-05 semicolons) — clean
- **Heuristic (PQ-06/PQ-07):** 41 (passive voice and ambiguous pronoun flags — report-only, not blocking)
- **Tier 3:** 0 (banned words/phrases)

---

## 3. Glossary Check (check_glossary.py)

**Result: PASS**

```
No banned synonym violations found.
```

Three glossary terms appear unused in sections:
- `First-order / second-order (kinetics analogy)` — used in prose but the exact glossary form doesn't match the concordance pattern
- `Parsimony pressure (λ_p)` — present in text but matched by symbol, not string
- `Precision (bits)` — used extensively but not matching the concordance pattern

These are concordance matching gaps, not missing content.

---

## 4. Result Reference Audit (`{{result:NAME:value}}`)

**Method:** `seldon paper build --no-render` (authoritative resolution check)
**Result: PASS** — Build: SUCCESS (see Section 7)

**Reference count:** 46 unique `{{result:NAME:VALUE}}` references across sections.

**Note on CLI audit:** The `seldon result show NAME` CLI command accepts artifact IDs (short hex), not symbolic names. The shell script check using that command produced false UNRESOLVED flags for all 46 references. The authoritative check is the build step, which resolves all references against the graph and produced BUILD: SUCCESS. All references are valid.

**Result names referenced in sections (46 total):**
- Core: `logprec_minimal_5_5`, `logprec_minimal_runtime`, `logprec_minimal_mean_gen`, `logprec_stress_l1_0_5`, `v2_confounded_5_5`, `info_rate_3_32`
- Wrong-limit attractor: `wrong_limit_ti_15_93`, `leibniz_ti_15_29`, `leibniz_prec_t5`
- Grandi/comparison: `grandi_leibniz_mean_rate_4_61`, `grandi_leibniz_ti_t5_0_07`
- GP baselines: `gp_minimal_2_5`, `gp_pop2000_5_5`, `gp_alpha_0_5_4_5`, `gp_extended_t10_p5000_1_5`
- Parsimony: `parsimony_leibniz_fitness_baseline`, `parsimony_leibniz_fitness_0_01`, `parsimony_zero_constant_fitness`, `logprec_max_fitness_leibniz`
- Fitness mods: `fitness_largeT_w0_1`
- Scaling grid: 26 `scaling_grid_tN_pM` references

---

## 5. Section Cross-Reference Check

**Result: PASS — 0 unresolved cross-references**

References found in prose:

| Referenced | Exists? |
|---|---|
| Section 3.1 | Yes |
| Section 3.2 | Yes |
| Section 4.1 | Yes |
| Section 4.2 | Yes |
| Section 4.3 | Yes |
| Section 5.4 | Yes |
| Section 6.1 | Yes |
| Section 6.3 | Yes |

All 8 referenced sections have corresponding headers.

---

## 6. Citation Cross-Check

**In-text citations extracted from prose:**

| In-text citation | .bib key | Status |
|---|---|---|
| Deb and Goldberg, 1993 | `Deb1993Deceptive` | OK |
| Jiang et al., 2025 | `Jiang2025EGGSR` | OK |
| Kamienny et al., 2023 | `Kamienny2023MCTS` | OK |
| Li et al., 2023 | `Li2023GFlowNet` | OK |
| Lipson (2009) | `Schmidt2009Distilling` | OK (partial match — grep captured second author only from "Schmidt and Lipson (2009)") |
| Sommer (2012) | `Hillar2012Comment` | OK (partial match — grep captured second author only from "Hillar and Sommer (2012)") |
| Sastry (2005) | `Sastry2005PopulationSizing` | OK |
| Shojaee et al., 2023 | `Shojaee2023TPSR` | OK |
| Soule and Foster, 1998 | `Soule1998CodeGrowth` | OK |
| Valipour et al., 2021 | `Valipour2021SymbolicGPT` | OK |

**Additional in-text citations not captured by grep patterns** (require manual verification):
- Schmidt and Lipson (2009) — `Schmidt2009Distilling` ✓ (confirmed present in Section 2.1 prose)
- Hillar and Sommer (2012) — `Hillar2012Comment` ✓
- Goldberg (1989) — `Goldberg1989GA` ✓
- Poli, Langdon, and McPhee (2008) — `Poli2008ParsimonyEasy` ✓
- Cranmer (2023) — `Cranmer2023PySR` ✓
- Abdusalamov et al. (2023) — `Abdusalamov2023Asymptotic` ✓

**BibTeX entries not referenced in-text** (in .bib but no clear in-text citation found):
- `Brunton2016SINDy` — possibly cited in Section 2 prose not captured by grep
- `Rudy2017DataDriven` — same
- `deSilva2020Discovery` — same
- `Durasevic2020Fitness` — same
- `Haghighat2015AvoidingOverfitting` — same
- `Keijzer2011ScalingDeceptive` — same
- `LaCasse2022BayesianBloat` — same
- `Langdon2002GPConvergence` — same
- `Muldoon2023ErrorCorrelation` — same
- `Poli2008FieldGuide` — same

**Note:** These may be cited via narrative forms not captured by the grep patterns (e.g., "Brunton et al." in a longer clause). Manual review recommended against Section 8 (references list) which enumerates all cited works.

---

## 7. Seldon Graph State

### Paper Build

```
seldon paper sync: 10 unchanged
seldon paper build --no-render: BUILD: SUCCESS
  TIER 1: Structural Integrity — pass
  TIER 2: Prose Quality — 46 violations (pre-existing; includes PQ-08 citation format)
  TIER 3: Style — 277 findings (pre-existing SP-03 repeated words in appendix)
```

### Artifact State

- **AgentRole artifacts:** 7 total (1 rejected, 6 active)
- **DataFile artifacts:** 20+ (all `proposed` state — not yet verified/registered)
- **Result artifacts:** 46 verified results (all resolved by build step)

### Open Tasks (all in `proposed` state)

Notable open tasks relevant to paper:

| ID | Description |
|---|---|
| `a8bf0d31` | RED TEAM: Section 5.1 references 'Table ...' |
| `e667be45` | RED TEAM: Literal X/5 values in prose |
| `317e16ab` | RED TEAM: Search space size argument |
| `aefdde16` | RED TEAM: Checkpoint count confound |
| `73260b47` | RED TEAM: Safe division and power overflow |
| `5a502dc1` | RED TEAM: Monotonicity thresholds |
| `005af871` | RED TEAM: Confabulation analogy |
| `1817bc93` | Rewrite medium draft closing section |
| `ba6e8f9f` | Write academic paper targeting GECCO/Evo |
| `a804bac0` | Register v3 wide/hostile clean rerun results |

**Note:** Task `a8bf0d31` ("Section 5.1 references 'Table'") — Tables 3 and 4 were added to Section 5.1 in this session. This red team task may now be resolved; manual verification recommended.

---

## 8. Issues Found (Do Not Fix — Report Only)

1. **Figure path error (PDF blocking):** Section files use `../figures/` paths; Quarto resolves relative to `paper/`, not `paper/sections/`. All 4 figure references in sections 05 and 06 have wrong paths for PDF rendering. Correct path: `figures/FILENAME.png`. Requires prose edit to 05_results.md and 06_discussion.md.

2. **PQ-08 citation format (pre-existing):** 46 Seldon Tier 2 violations for sections lacking `[@key]` citation tokens. Paper uses plain `(Author, Year)` format throughout. Requires a paper-wide citation format conversion to Pandoc `[@key]` syntax. Pre-existing issue; not introduced in this session.

3. **DataFile artifacts in `proposed` state:** 20+ DataFile artifacts remain unverified in Seldon. These represent experiment data files not yet formally registered. Not blocking for paper submission but relevant for reproducibility traceability.

4. **4 open RED TEAM tasks:** Tasks `317e16ab`, `aefdde16`, `73260b47`, `5a502dc1` flag potential methodological challenges in the paper. These should be addressed or explicitly scoped out before submission.

5. **Uncited .bib entries:** 10 references in `references.bib` were not clearly matched by in-text citation grep. Manual verification against Section 8 references list recommended. These may represent background reading included in the bib but not directly cited in prose.

---

*Report generated by CC task `2026-03-26_build_pdf_audit_recon.md`*
