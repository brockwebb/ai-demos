# Audit: 05_results.md — 2026-03-17

## 1. Current {{result:...}} References

References found in 05_results.md, cross-checked against registered results:

| Reference | Location (line) | Registered Value | Units | State | Status |
|---|---|---|---|---|---|
| `{{result:logprec_minimal_5_5:value}}` | Lines 5, 9 | 1.0 | discovery_r | verified | VALID |
| `{{result:gp_minimal_2_5:value}}` | Lines 5, 10 | 0.4 | discovery_r | verified | VALID (0.4 = 2/5) |
| `{{result:gp_pop2000_5_5:value}}` | Lines 5, 11 | 1.0 | discovery_r | verified | VALID (1.0 = 5/5) |
| `{{result:logprec_minimal_runtime:value}}` | Line 5 | 369.9 | seconds | verified | VALID |
| `{{result:logprec_minimal_mean_gen:value}}` | Line 9 | 2981.0 | generations | verified | VALID |
| `{{result:logprec_stress_l1_0_5:value}}` | Line 26 | 0.0 | discovery_r | verified | VALID |
| `{{result:wrong_limit_ti_15_93:value}}` | Line 28 | 15.93 | bits | verified | VALID |
| `{{result:leibniz_ti_15_29:value}}` | Line 28 | 15.29 | bits | verified | VALID |
| `{{result:fitness_largeT_w0_1:value}}` | Line 70 | 0.2 | discovery_r | verified | VALID (0.2 = 1/5) |
| `{{result:gp_alpha_0_5_4_5:value}}` | Line 77 | 0.8 | discovery_r | verified | VALID (0.8 = 4/5) |

Notes on value rendering:
- `gp_minimal_2_5` resolves to 0.4, but the surrounding text reads "{{result:gp_minimal_2_5:value}}/5" which will render as "0.4/5" — ambiguous. The evidence map lists this as "2/5". The registered units are `discovery_r` (decimal). The display "0.4/5" is grammatically and numerically confusing. See Section 7 (Structural Issues).
- `gp_pop2000_5_5` resolves to 1.0, renders as "1.0/5" — same issue.
- `logprec_minimal_5_5` resolves to 1.0, renders as "1.0/5" — same issue.
- `logprec_stress_l1_0_5` resolves to 0.0, renders as "0.0/5" — same issue.
- `fitness_largeT_w0_1` resolves to 0.2, renders as "0.2/5" — same issue.
- `gp_alpha_0_5_4_5` resolves to 0.8, renders as "0.8/5" — same issue.

All 10 {{result:...}} references resolve to registered, verified results. No broken or missing references.

---

## 2. Literal Numbers Not Registered

All literal numbers found in 05_results.md, in order of appearance:

| Line | Literal | Context | Assessment |
|---|---|---|---|
| 5 | 1,000 | "at population 1,000" | Acceptable — experimental parameter, not a result |
| 5 | 2,000 | "at population 2,000" | Acceptable — experimental parameter, not a result |
| 9 | 1,000 | Table: "Pop" column value | Acceptable — experimental parameter |
| 10 | 1,000 | Table: "Pop" column value | Acceptable — experimental parameter |
| 11 | 2,000 | Table: "Pop" column value | Acceptable — experimental parameter |
| 13 | 100,000 | "verified identical at k=100,000 with zero divergence" | Flag for human — this is a verification depth, not currently registered |
| 17 | 11 | "11 nodes" (Table 2) | Flag for human — structural measurement; should register or accept as table data |
| 18 | 10 | "10 nodes" (Table 2) | Flag for human — structural measurement; should register or accept as table data |
| 19 | 9 | "9 nodes" (Table 2) | Flag for human — structural measurement (×2 seeds) |
| 20 | 9 | "9 nodes" (Table 2) | Flag for human — structural measurement (×2 seeds) |
| 22 | 9 | "canonical 9-node form" | Flag for human — structural count |
| 22 | 3/5 | "bloated algebraic equivalents appear in 3/5 seeds" | FLAG — this is a derived result claim not registered and not representable as a {{result:...}} reference currently. Directly contradicts Table 2 (Table 2 shows 4 seeds found, and 3 of 4 are bloated; but logprec_minimal_5_5 = 5/5). Needs clarification: does 3/5 refer to 3 of 5 seeds or 3 of 4 discovered? |
| 22 | 0.005 | "λ_p = 0.005 is insufficient" | Acceptable — experimental parameter |
| 22 | 0.01 | "Increasing parsimony to λ_p ≥ 0.01 destroys discovery" | Acceptable — threshold reported in section 5.4 also |
| 26 | 1,000 | "at population 1,000" | Acceptable — experimental parameter |
| 26 | 15 | "With 15 terminals" | Acceptable — experimental parameter |
| 28 | 42 | "Seed 42 found the expression" | Acceptable — seed identifier |
| 28 | 10,000 | "at T=10,000" (twice in line 28) | Acceptable — evaluation horizon parameter |
| 32 | 7 | "The 7 × 4 scaling grid" | Acceptable — describes table dimensions |
| 32 | 4 | "The 7 × 4 scaling grid" | Acceptable — describes table dimensions |
| 32 | 8 | "phase transition between t=8 and t=10" | Acceptable — describes experimental observation |
| 32 | 10 | "phase transition between t=8 and t=10" | Acceptable — describes experimental observation |
| 34–42 | All grid cell values (5/5, 1/5, etc.) | Table 3 scaling grid | FLAG — entire table uses literal fractions; no {{result:...}} references anywhere in this table. See Section 4 below. |
| 44 | 4 | "At t=4" | Acceptable — terminal count |
| 44 | 6 | "At t=6 and t=8" | Acceptable — terminal count |
| 44 | 8 | "At t=6 and t=8" | Acceptable — terminal count |
| 44 | 10 | "At t=10 and above" | Acceptable — terminal count |
| 44 | 2/5 | "at t=15 with pop=10,000, 2/5 seeds succeed" | FLAG — unregistered result claim from scaling grid anomaly |
| 44 | 15 | "at t=15 with pop=10,000" | Acceptable — terminal count |
| 44 | 10,000 | "pop=10,000" | Acceptable — population parameter |
| 48 | 1,000 | "from 1,000 to 10,000" | Acceptable — experimental parameter |
| 48 | 10,000 | "from 1,000 to 10,000" | Acceptable — experimental parameter |
| 48 | 5,000 | "for populations up to 5,000" | Acceptable — experimental parameter |
| 54 | 5/5 | Parsimony table (Table 4) | Acceptable — table cell, λ_p=0.005 row |
| 55 | 0/5 | Parsimony table (Table 4) | Acceptable — table cell, λ_p=0.01 row |
| 56 | 0/5 | Parsimony table (Table 4) | Acceptable — table cell, λ_p=0.02 row |
| 57 | 0/5 | Parsimony table (Table 4) | Acceptable — table cell, λ_p=0.05 row |
| 54 | 9–11 | "9–11 node Leibniz equivalents" | Acceptable — structural range observation |
| 59 | 0.021 | "scores approximately 0.021 fitness" | FLAG — unregistered result; see Section 5 |
| 59 | -0.024 | "scores approximately -0.024" | FLAG — unregistered result; see Section 5 |
| 59 | -0.030 | "approximately -0.030" | FLAG — unregistered result; see Section 5 |
| 61 | 0.07 | "sum to at most approximately 0.07" | FLAG — unregistered result; see Section 5 |
| 61 | 9 | "λ_p × 9 < 0.07" | Acceptable — references 9-node count already established |
| 61 | 0.008 | "λ_p < 0.008" | FLAG — derived analytical bound, unregistered |
| 65 | 7 | "We tested seven modifications" | Acceptable — count corroborated by table rows |
| 69 | 0/5 | Table 5 cell | Acceptable — table data |
| 70 | 0.1 | "Large-T penalty w=0.1" | Acceptable — experimental parameter |
| 71 | 0/5 | Table 5 cell | Acceptable — table data |
| 71 | 0.5 | "Large-T penalty w=0.5" | Acceptable — experimental parameter |
| 72 | 0/5 | Table 5 cell | Acceptable — table data |
| 73 | 0/5 | Table 5 cell | Acceptable — table data |
| 74 | 0/5 | Table 5 cell | Acceptable — table data |
| 75 | 0/5 | Table 5 cell | Acceptable — table data |
| 77 | 1.0 | "reducing α from 1.0 to 0.5" | Acceptable — experimental parameter |
| 77 | 0.5 | "reducing α from 1.0 to 0.5" | Acceptable — experimental parameter |
| 77 | 1/5 | "No modification achieved better than 1/5 on 15 terminals" | FLAG — this claim needs verification against Table 5. fitness_largeT_w0_1 = 0.2 = 1/5, but table shows the alpha sweep produced 0.8/5 on minimal terminals, not on 15. The claim "No modification achieved better than 1/5 on 15 terminals" is asserted as a literal, not registered. |

---

## 3. Table 2 — Seed Coverage

Table 2 appears at lines 15–20.

Seeds present in Table 2: 42, 7, 2718, 31415

Seeds NOT present: **137 is absent from Table 2.**

logprec_minimal_5_5 = 1.0 (5/5 discovery), meaning all 5 seeds found Leibniz. Only 4 seeds appear in Table 2. This is a structural gap: one successful seed (presumably 137) is missing from the structural variants table.

Line 13 states: "Table 2 shows the structural variants that appear across seeds." If 5/5 seeds found the expression, Table 2 should show 5 rows but shows only 4.

Line 22 states: "bloated algebraic equivalents appear in 3/5 seeds." With Table 2 showing only 4 seeds (3 with 9–11 nodes bloated, 1 with 9-node canonical), this "3/5" claim is inconsistent with 5/5 success unless seed 137's form is being excluded (possibly it is identical to one already shown). This ambiguity is unresolved and potentially misleading.

Summary:
- Seeds shown: 42 (11 nodes), 7 (10 nodes), 2718 (9 nodes), 31415 (9 nodes)
- Seed 137: ABSENT
- If logprec_minimal_5_5 = 5/5 is accurate, a row for seed 137 is missing from Table 2
- The "3/5 bloated" claim on line 22 does not add up with Table 2 as shown

---

## 4. Scaling Grid — Reference Coverage

The 7×4 scaling grid appears at lines 34–42. None of the 28 data cells use `{{result:...}}` references. All values are bare literals.

| t (terminals) | pop=1000 | pop=2000 | pop=5000 | pop=10000 | Any {{result:}} ref? |
|---|---|---|---|---|---|
| 4 | 5/5 | 4/5 | 5/5 | 5/5 | None |
| 6 | 1/5 | 2/5 | 1/5 | 1/5 | None |
| 8 | 1/5 | 1/5 | 1/5 | 0/5 | None |
| 10 | 0/5 | 0/5 | 0/5 | 0/5 | None |
| 12 | 0/5 | 0/5 | 0/5 | 0/5 | None |
| 15 | 0/5 | 0/5 | 0/5 | 2/5 | None |
| 20 | 0/5 | 0/5 | 0/5 | 0/5 | None |

Registered results that correspond to specific cells:
- `logprec_minimal_5_5` (5/5) corresponds to t=4, pop=1000 ✓ (cell shows 5/5, consistent)
- `logprec_stress_l1_0_5` (0/5) corresponds to t=15, pop=1000 ✓ (cell shows 0/5, consistent)
- `gp_minimal_2_5` is convergence-aware fitness, NOT the log-precision scaling grid. Different experiment.

The 26 remaining cells are all unregistered literals. This is a large body of experimental data in the paper with no graph provenance coverage. The t=15, pop=10000 anomaly cell (2/5) is specifically notable: it is called out explicitly in lines 44–46 and referenced in the evidence map claim "Phase transition between t=8 and t=10" but has no corresponding registered result.

Cells with the highest claim-importance that are unregistered:
- t=6, pop=1000: 1/5 (supports "nonzero success drops")
- t=8, pop=1000: 1/5 (supports phase transition claim)
- t=10, pop=1000: 0/5 (supports phase transition claim)
- t=15, pop=10000: 2/5 (the anomaly — most discussed unregistered value)

---

## 5. Parsimony Section — Literals Assessment

Literal values in section 5.4 (lines 59–61):

| Literal | Context | Line | Assessment |
|---|---|---|---|
| 0.021 | "9-node Leibniz tree scores approximately 0.021 fitness" at λ_p=0.005 | 59 | Unregistered. Quantitative fitness score. Should register if citable. The word "approximately" signals a measured value, not a parameter. |
| -0.024 | "same tree scores approximately -0.024" at λ_p=0.01 | 59 | Unregistered. Same as above. |
| -0.030 | "zero-constant attractor at approximately -0.030" | 59 | Unregistered. Measured comparator value. Should register if citable. |
| 0.07 | "fitness terms...sum to at most approximately 0.07 for Leibniz" | 61 | Unregistered. This appears to be an analytical bound derived from the fitness function formula, not a measured result. May be acceptable as an analytical statement rather than a registered result, but the word "approximately" complicates that — if approximate, it was measured. |
| 0.008 | "λ_p < 0.008" | 61 | Unregistered. Derived threshold from λ_p × 9 < 0.07. If 0.07 is registered, this is a pure algebraic derivation (9 × λ_p < max_fitness_sum → λ_p < 0.007...). May be acceptable as analytical. |

The analytical derivation on line 61 — "λ_p × 9 < 0.07, so λ_p < 0.008" — is borderline. It is derived from a measured-ish bound (0.07) via multiplication by a structural constant (9 nodes). The conclusion (0.008) is arithmetically incorrect: 0.07/9 = 0.00778, which rounds to 0.008. This is a valid approximation, but the primary input (0.07) being unregistered weakens the provenance chain.

---

## 6. Terminology Violations

Scanning 05_results.md against glossary banned terms:

| Term Found | Line | Glossary Status | Correct Term |
|---|---|---|---|
| "information rate" (implicit) | 73 | Potentially ambiguous — line 73 reads "Rewards only information rate, ignores terminal value" | Glossary entry for "Information rate / precision gain rate" uses both forms. "Information rate" is listed as a valid alternative in the header. However, in 5.5 context, this refers to a fitness modification name; usage appears acceptable as shorthand. Monitor for consistency. |
| "partial recovery" | 44 | EXEMPT per glossary | No violation — glossary explicitly exempts "partial recovery" when describing the scaling grid anomaly. |
| "diversity" | n/a | Not found in 05_results.md | No violation. |
| "rediscovery" | n/a | Not found | No violation. |
| "recovery" (non-exempt) | n/a | Not found | No violation. |
| "deceptive series" | n/a | Not found | No violation. |
| "false positive" | n/a | Not found | No violation. |
| "evaluation window" | n/a | Not found | No violation. |
| "complexity penalty" | n/a | Not found | No violation. |
| "components" | n/a | Not found | No violation. |
| "hallucination" | n/a | Not found | No violation. |
| "entropy fitness" | n/a | Not found | No violation. |
| "information-theoretic fitness" | n/a | Not found | No violation. |

One potential concern: line 73 uses "information rate" as a modifier inside the fitness modification table ("Pure gradient magnitude — Rewards only information rate"). The glossary entry header is "Information rate / precision gain rate" suggesting either form is acceptable. No violation, but note for consistency: Section 3.3.2 and Section 6.1 should also use "information rate" if that is the preferred form (glossary prefers "precision gain rate" as the primary description but allows both).

No clear terminology violations in 05_results.md.

---

## 7. Structural Issues

### 7.1 Double Reference in 5.1 (Line 5)

Line 5 uses `{{result:logprec_minimal_5_5:value}}` twice in the same sentence:

> "the log-precision fitness achieves {{result:logprec_minimal_5_5:value}}/5 discovery across five seeds ... Total runtime for the {{result:logprec_minimal_5_5:value}}/5 log-precision run across all five seeds was {{result:logprec_minimal_runtime:value}} seconds."

The second use ("the {{result:logprec_minimal_5_5:value}}/5 log-precision run") is redundant — the reader already knows 5/5 succeeded from the first mention. This is stylistically weak but not a data error.

Additionally, `{{result:gp_minimal_2_5:value}}` appears in line 5 (prose) and line 10 (table). `{{result:gp_pop2000_5_5:value}}` appears in line 5 (prose) and line 11 (table). These are appropriate cross-references, not double-reference issues.

### 7.2 Discovery Rate Display Format (Lines 5, 9, 10, 11, 26, 70, 77)

All discovery_rate results are stored as decimals (0.4, 1.0, 0.0, etc.) but displayed in context as "X/5". The pattern `{{result:NAME:value}}/5` will render as "0.4/5", "1.0/5", "0.0/5" — which is numerically confusing. Readers expect "2/5", "5/5", "0/5". This is a systematic rendering issue affecting all discovery_rate references.

Affected lines: 5 (×3), 9, 10, 11, 26, 70, 77.

### 7.3 Missing Seed in Table 2

As detailed in Section 3, seed 137 is absent from Table 2. The table header claims to show "structural variants that appear across seeds" but shows only 4 of 5 successful seeds. This gap is unexplained in the section text. Either Table 2 is incomplete, or seed 137 produced a duplicate form (same as one of the 4 shown) and the text should say so.

### 7.4 Inconsistency: "3/5 seeds bloated" vs Table 2

Line 22: "bloated algebraic equivalents appear in 3/5 seeds." Table 2 shows 4 seeds, of which seeds 42 (11 nodes) and 7 (10 nodes) are clearly bloated, while seeds 2718 and 31415 (both 9 nodes) are the canonical minimal form. That would be 2/4 bloated in Table 2. If 5/5 seeds discovered Leibniz (logprec_minimal_5_5 = 5/5), the "3/5" claim implies 3 of 5 seeds produced bloated forms — but with seed 137 missing from Table 2, we cannot verify this from the table as presented.

### 7.5 Arithmetic Check: λ_p Ceiling (Line 61)

"λ_p × 9 < 0.07, so λ_p < 0.008"

Calculation: 0.07 / 9 = 0.00778. Rounded up: 0.008. The stated threshold is correct as an approximation, but the derivation assumes the 9-node count is canonical, which is a simplification (the section earlier notes 9–11 node forms exist). This is a minor analytical caveat but should be flagged for human review.

---

## 8. Evidence Map Comparison

Comparing evidence_map.md claims table against section 05_results.md:

| Evidence Map Claim | Evidence Map Evidence | Present in 05_results.md? | Notes |
|---|---|---|---|
| Discovery succeeds with minimal terminals (Abstract, Conclusion) | `logprec_minimal_5_5` = 5/5 | YES — line 5, 9 | Consistent |
| Discovery fails at 15 terminals (Abstract, Conclusion) | `logprec_stress_l1_0_5` = 0/5 | YES — line 26 | Consistent |
| Phase transition between t=8 and t=10 (Results 5.3, Conclusion) | Scaling grid Table 3 | YES — lines 32, 44–48 | Supported by literal table values; no registered results for individual cells |
| Fitness is not the bottleneck (Conclusion) | 7 modifications all fail at t=15 (Table 5) | YES — line 65, Table 5 (lines 68–75) | Table 5 shows 6 modifications as 0/5, 1 as 1/5; claim is largely supported |
| Parsimony collapses discovery above threshold (Results 5.4) | λ_p ≥ 0.01 → 0/5 (Table 4) | YES — line 55 (Table 4) | Consistent |
| Wrong-limit attractors outscore Leibniz (Results 5.2) | `wrong_limit_ti_15_93` > `leibniz_ti_15_29` | YES — line 28 | Consistent |
| Leibniz gains 3.32 bits/decade (Methods, Discussion) | `info_rate_3_32` = 3.32 | NOT IN 05_results.md | Evidence map lists sections 3.3.2 and 6.1 for this result. Correct — not expected in Section 5. |
| Second-order kinetics analogy (Discussion 6.1) | Structural observation | NOT IN 05_results.md | Correct — belongs in Discussion. |
| Injection confound caught and corrected (Exp Design 4.1) | `v2_confounded_5_5` vs v3 results | NOT IN 05_results.md | Correct — belongs in Section 4. |

Evidence map references `logprec_minimal_mean_gen` is NOT listed in the evidence map's Results table, but the reference appears in 05_results.md (line 9). This is a provenance gap: `logprec_minimal_mean_gen` (2981.0 generations) is a registered result used in the paper but not listed in the evidence map.

Evidence map lists `gp_minimal_2_5` value as "2/5" but the registered value is 0.4. The evidence map uses the human-readable fraction form; the registry uses decimal. No data inconsistency but a display convention mismatch worth noting for the evidence map.

Same issue for `gp_pop2000_5_5`: evidence map shows "5/5", registry is 1.0; `v2_confounded_5_5` shows "5/5", registry is 1.0; `fitness_largeT_w0_1` shows "1/5", registry is 0.2; `gp_alpha_0_5_4_5` shows "4/5", registry is 0.8.

---

## 9. Human Decision Items

The following items require Brock's judgment. Do NOT auto-fix.

**9.1 Seed 137 in Table 2**
Determine whether seed 137 produced a distinct structural form that is absent from Table 2, or whether it duplicated an existing form (in which case Table 2 should note this explicitly). If it was a duplicate, line 22's "3/5 seeds bloated" becomes "3/5 discovered seeds produced bloated forms" — a different denominator from 5/5 total.

**9.2 "3/5 seeds bloated" claim (line 22)**
Decide the precise claim: 3 of 5 total seeds produced bloated forms? Or 3 of 4 unique structural forms found? Verify against raw experimental data.

**9.3 Discovery rate rendering format**
Decide whether to store discovery rates as decimals (0.4) and accept the "0.4/5" rendering, or change the registered values to strings ("2/5") or counts (2, with denominator 5 implied). The current rendering is ambiguous to a reader. Options:
- Change result values in registry from decimal to integer (2, 5, etc.) and adjust display context
- Add a `:fraction` field to results that stores "2/5" directly
- Accept the current format as-is with a note in paper conventions

**9.4 Scaling grid registration strategy**
Decide whether to register individual scaling grid cells as results. The entire 7×4 table (28 cells) is currently unregistered. Key candidates:
- t=4, pop=1000: 5/5 (same as logprec_minimal_5_5 — possible duplicate)
- t=15, pop=10000: 2/5 (the anomaly, discussed substantively)
- t=10 boundary cells: 0/5 (supports phase transition claim)
At minimum the anomaly cell (t=15, pop=10000 = 2/5) warrants registration given how much text discusses it.

**9.5 Parsimony fitness scores (0.021, -0.024, -0.030, 0.07)**
Decide whether these approximate fitness score measurements should be formally registered as results. They are presented as "approximately" values and support the parsimony ceiling analysis. If the analysis is being cited, they should be registered with appropriate uncertainty notation.

**9.6 Analytical bound λ_p < 0.008 (line 61)**
Decide whether this is a registered result (derived from registered inputs) or a discursive derivation acceptable in prose. If 0.07 gets registered, consider whether 0.008 should also be registered as a derived result.

**9.7 Evidence map: missing logprec_minimal_mean_gen entry**
The result `logprec_minimal_mean_gen` (2981.0 generations) is used in the paper (Table 1, line 9) but is absent from the evidence map's results table. Either add it to the evidence map or confirm it is intentionally excluded.

---

## 10. Summary Checklist

Items that can be fixed without human judgment (implementable by CC):

- [ ] Add `logprec_minimal_mean_gen` to evidence map Results table (currently missing; used in paper but not listed)
- [ ] Fix evidence map display: update "2/5", "5/5" etc. in the Value column to match the registry's decimal format (0.4, 1.0) OR note the display convention explicitly

Items requiring human decision before fix:

- [ ] **[H9.1]** Determine what seed 137 found — add to Table 2 or add explanatory prose
- [ ] **[H9.2]** Verify "3/5 seeds bloated" claim against raw data; fix denominator if needed
- [ ] **[H9.3]** Decide discovery rate display format and implement consistently
- [ ] **[H9.4]** Decide whether to register scaling grid cells as results (especially t=15, pop=10000 anomaly)
- [ ] **[H9.5]** Decide whether to register parsimony fitness scores (0.021, -0.024, -0.030, 0.07)
- [ ] **[H9.6]** Decide status of λ_p < 0.008 derivation
- [ ] **[H9.7]** Add `logprec_minimal_mean_gen` to evidence map after decision on H9.1

Confirmed non-issues:
- All 10 `{{result:...}}` references resolve to verified, registered results
- No banned terminology found in 05_results.md
- No broken reference names
- Evidence map claims all supported by section content
- Arithmetic in parsimony analysis is correct (0.07/9 ≈ 0.008)

---

*Audit produced by Claude Code, 2026-03-17. Read: 05_results.md, evidence_map.md, glossary.md. Did not modify any paper files.*
