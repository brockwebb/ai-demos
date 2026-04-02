# Paper Audit: Full Section-by-Section Review

**Date:** 2026-03-26
**Auditor:** Claude Desktop
**Scope:** Sections 01–07 (body), 08 (references), 09 (appendix)
**Prior work:** Tier 1/2/3 fact-check complete (2026-03-25 session). This audit focuses on internal consistency, cross-section coherence, RED TEAM resolution, citation completeness, and remaining gaps.

---

## Summary Table

| Category | Count | Details |
|---|---|---|
| Cross-section inconsistencies | 3 | See §A |
| Missing .bib entries | 2 | Luke2003, Murphy2019GEFS — referenced in sections but absent from references.bib |
| Orphan .bib entries | 8 | In .bib but never cited in any section |
| RED TEAM items to address | 4 | Search space, checkpoints, safe division, monotonicity |
| RED TEAM items resolved | 3 | Table refs (done), literal X/5 (acceptable), confabulation preview (done) |
| Structural issues | 2 | See §C |
| Suspect claims | 1 | See §D |
| Perplexity queries needed | 0 | Prior fact-check was thorough; no new external verification needed |

---

## A. Cross-Section Inconsistencies

### A1. Section 3.3.3 vs Section 5.2: Wrong-limit attractor precision values

Section 3.3.3 states the attractor "5/((6+4k)(k-2))" scores well on convergence-aware fitness. Section 5.2 reports this attractor achieves {{result:wrong_limit_ti_15_93:value}} bits under log-precision fitness. These are consistent — the claim in 3.3.3 is about convergence-aware, 5.2 is about log-precision. But 3.3.3 never says what the attractor scores under convergence-aware fitness. It makes a qualitative claim ("score well") without evidence. Either add the convergence-aware score or soften to "would score well."

**Severity:** Low. Qualitative claim is defensible from the definition.

### A2. Section 6.2 cites Sastry (2005) — Section 2 does not mention population sizing literature

Section 6.2 introduces population sizing theory (Sastry 2005, building-block decision-making) as support for the coverage argument. This is a new theoretical framework appearing for the first time in the Discussion, not previewed in Background. A reviewer might flag this as a "surprise citation" — theoretical support should ideally appear or be previewed in Section 2.

**Severity:** Medium. Consider adding one sentence to Section 2.2 or 2.3 previewing population sizing theory as relevant to the coverage question.

### A3. Conclusion claims "every seed found Leibniz" at t=4 — scaling grid shows 4/5 at t=4/pop=2000

Section 7 opens with "With four terminals, every seed found Leibniz." The scaling grid (Section 5.3 Table 5) shows t=4/pop=2000 achieved 4/5, not 5/5. The claim is true for the minimal terminal experiment (5.1, log-precision, pop=1000) but not universally across all t=4 configurations.

**Severity:** Medium-high. An adversarial reviewer will catch this. Options: (a) qualify as "With four terminals and log-precision fitness, every seed found Leibniz" or (b) note that 19/20 seeds found Leibniz at t=4 across the scaling grid, or (c) qualify as referring to the primary result.

---

## B. Citation Completeness

### B1. Missing .bib entries (cited in sections, not in references.bib)

| Citation | Cited in | Status |
|---|---|---|
| Luke et al. (2003) / `Luke2003PopulationSizing` | Section 6.2 | **MISSING from references.bib** — handoff says it was added but it's not in the file |
| Murphy et al. (2019) / `Murphy2019GEFS` | Section 7 | **MISSING from references.bib** — handoff says it was added but it's not in the file |

These were listed as added in the 2026-03-25 handoff but are not present in the current `references.bib`. Either the .bib write failed, was reverted, or the entries were added to a different file. The `[@key]` conversion task may have added `@key` references to sections without verifying the .bib entries exist. This will cause Pandoc citation warnings or [?] markers in the PDF.

**Action:** Add both entries to references.bib. Verified details from prior session:
- Luke, S., Panait, L., Balan, G., et al. (2003). "Population Sizing for GP." arXiv cs/0502020. (Actually Sastry is the population sizing one — need to verify which paper Luke2003 refers to. May be a different Luke paper.)
- Murphy, L., et al. (2019). "Grammar-based Feature Selection for Symbolic Regression." GECCO 2019.

**Perplexity verification needed:** Yes, for Luke2003 specifically — confirm exact title/venue/authors. Murphy2019GEFS was verified in prior session.

### B2. Orphan .bib entries (in .bib, never cited in any section)

| BibTeX Key | Paper | Recommendation |
|---|---|---|
| `Brunton2016SINDy` | SINDy (PNAS 2016) | Remove — relevant to data-driven discovery generally but never cited |
| `Rudy2017DataDriven` | Data-driven PDE discovery | Remove — SINDy follow-up, not cited |
| `deSilva2020Discovery` | Universal laws from data | Remove — not cited |
| `Keijzer2011ScalingDeceptive` | Affine arithmetic for SR | Remove — not cited, title mismatch (about affine arithmetic, not deception) |
| `Haghighat2015AvoidingOverfitting` | First-order derivative for overfitting | Remove — not cited |
| `Durasevic2020Fitness` | Fitness landscape with Feynman eqs | Remove — not cited |
| `Muldoon2023ErrorCorrelation` | Error and correlation fitness | Remove — not cited |
| `LaCasse2022BayesianBloat` | Bayesian model selection for bloat | Remove — not cited |
| `Langdon2002GPConvergence` | GP convergence | Remove — not cited |
| `Sastry2005PopulationSizing` | Population sizing for GP | **KEEP — cited in Section 6.2** (verify @key format in prose) |

Actually let me re-check Sastry — it IS in the .bib. So 9 orphans, not 10.

**Recommendation:** Remove 9 orphan entries. They inflate the bibliography without adding value. If any are borderline (e.g., Brunton2016 as foundational), consider adding a "Further Reading" note rather than keeping them as phantom citations.

---

## C. Structural Issues

### C1. References section rendering

The `\bibliography{references}` command remains in `paper.qmd` line 363 (per CC report). While Pandoc currently ignores it, it's technical debt. If the LaTeX backend changes or a different renderer is used, it could cause duplicate reference sections or errors.

**Action:** Add to a CC task: after `seldon paper sync`, strip `\bibliography{references}` from paper.qmd before rendering.

### C2. Conclusion paragraph structure

Section 7 has three paragraphs. The third starts "Three directions address the coverage bottleneck:" and lists three items using "and" and commas. This is grammatically awkward — "Three directions...building block initialization...and automated terminal pruning...A third direction, island migration..." The phrasing says "three" but structures it as "two...and a third." Either restructure as three parallel items or recount.

**Action:** Rewrite to parallel structure. E.g., "Three directions address the coverage bottleneck. First, building block initialization... Second, automated terminal pruning... Third, island migration..."

---

## D. Suspect Claims

### D1. "coverage scales linearly with population size" (Section 6.2)

The claim that "doubling the population roughly doubles the initial coverage" is stated without evidence from our experiments. The scaling grid doesn't directly measure coverage — it measures discovery rate. The claim is plausible from theory (Sastry 2005) but our data doesn't show linear scaling of coverage. At t=6, going from pop=1000 to pop=10000 (10x) takes discovery from 1/5 to 1/5 — no improvement. At t=4, pop=2000 gets 4/5 while pop=1000 gets 5/5 — worse with more population.

**Severity:** Medium. The claim is theoretically grounded but empirically unsupported by our data. Consider softening to "coverage increases with population size" without claiming linearity, or explicitly noting this is from theory rather than our experiments.

---

## E. RED TEAM Task Resolution

### E1. `a8bf0d31` — Section 5.1 Table references → **RESOLVED**
Tables 3 and 4 added with proper captions this session. Resolved.

### E2. `e667be45` — Literal X/5 values in prose → **ACCEPTABLE**
These are `{{result:NAME:value}}/5` expressions that render as "5/5", "0/5", etc. The "/5" is a literal formatting choice, not a hardcoded result. The result reference resolves correctly. No action needed.

### E3. `005af871` — Confabulation analogy not previewed → **RESOLVED**
Section 1 paragraph 5 now contains: "The failure mode parallels confabulation in language models: outputs that appear correct within a finite evaluation horizon but do not correspond to the true target (Section 6.3)." One-sentence preview as specified. Resolved.

### E4. `317e16ab` — Search space size argument (Methods 3.1) → **NEEDS RESPONSE**
Section 3.1 claims "the number of structurally distinct well-formed expressions grows combinatorially" without quantification. The red team wants a bound or at least a rough count.

**Options:**
(a) Add a footnote with an order-of-magnitude estimate of tree count at depth 6 for t=4 vs t=15
(b) Cite the GP tree enumeration literature (if it exists)
(c) Accept the qualitative claim as sufficient — "combinatorial" is standard language in GP and doesn't require explicit counting

**Recommendation:** Option (a) — a one-sentence footnote with the formula for binary tree count at depth d with t terminals and o operators. This makes the "combinatorial" claim concrete without derailing the narrative.

### E5. `aefdde16` — Checkpoint count confound → **NEEDS RESPONSE**
The log-precision fitness uses 11 checkpoints (T=5 through T=10000). The convergence-aware fitness uses 5. The Grandi-Leibniz attractor (Appendix A.2.3) exploits checkpoint parity — it matches Leibniz at 10 of 11 checkpoints. This raises the question: are results sensitive to checkpoint selection?

**Current state:** The appendix documents this thoroughly. Section 3.3.2 describes the checkpoints. The confound is acknowledged.

**Recommendation:** Add one sentence to Section 3.3.2 noting that checkpoint selection influences which attractors are detectable, with forward reference to Appendix A.2.3. This converts a potential reviewer attack into a documented limitation.

### E6. `73260b47` — Safe division and power overflow as implicit terminals → **NEEDS RESPONSE**
Table 1 (Section 4.3) already documents that safe division and power overflow return 1.0 and "act as additional terminals." The prose also says "researchers counting available terminals should account for these implicit constants."

**Current state:** Documented but not quantified. Does this change the effective terminal count? At t=4, the effective count is t=4 + 1 implicit = 5 (but 1 is already in the base set, so the implicit 1.0 is redundant). At t=15, same — 1.0 is already a terminal.

**Recommendation:** Add one sentence: "Because 1.0 is already in the base terminal set at all sizes, the implicit constants from safe division and power overflow do not increase the effective terminal count." This preempts the objection.

### E7. `5a502dc1` — Monotonicity thresholds → **NEEDS RESPONSE**
Convergence-aware fitness uses 5% error reduction threshold. Log-precision uses 0.5-bit gain threshold. These are different bars, and neither is derived from theory.

**Current state:** Section 3.3.1 states "decreases by at least 5%." Section 3.3.2 states "≥ 0.5 bit gain." Neither explains why these values.

**Recommendation:** Add one sentence to each fitness function description: "The threshold is a design choice; values between X and Y produced similar results in preliminary experiments." Or, if no sensitivity analysis was done, state that directly: "We did not perform a sensitivity analysis on this threshold."

---

## F. Audit Verdict

The paper is in strong shape. The prior fact-check session caught the major issues. What remains:

**Must fix before submission (3 items):**
1. Add missing .bib entries (Luke2003, Murphy2019GEFS) — or remove the citations from prose if entries can't be verified
2. Fix Conclusion "every seed" overstatement (A3)
3. Fix Conclusion paragraph structure (C2)

**Should fix (4 items):**
4. Remove 9 orphan .bib entries
5. Add search space quantification footnote (E4)
6. Add checkpoint sensitivity acknowledgment sentence (E5)
7. Add safe-division-implicit-terminal clarification sentence (E6)

**Nice to have (3 items):**
8. Preview Sastry population sizing in Section 2 (A2)
9. Soften "coverage scales linearly" claim (D1)
10. Add monotonicity threshold justification (E7)
