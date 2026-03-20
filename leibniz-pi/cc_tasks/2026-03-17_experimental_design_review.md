# CC Task: Experimental Design Section (04) Review Edits

**Date:** 2026-03-17
**Scope:** `paper/sections/04_experimental_design.md`, `paper/sections/03_methods.md` (read-only reference)
**Constraint:** All numbers must come from source scripts or data files. No hardcoded values.

---

## Pre-flight

1. `seldon go --brief --project-dir /Users/brock/Documents/GitHub/ai-demos/leibniz-pi`
2. Read `paper/conventions.md` and `paper/glossary.md` before writing any prose.
3. Read current state of `paper/sections/04_experimental_design.md`.
4. Read current state of `paper/sections/03_methods.md` (reference only, do not edit).

---

## Task 1: Reframe discovery criterion in 4.2

The current text in 4.2 says:

> An expression counts as a discovery if its first 20 terms match the Leibniz series to within 10^-6 absolute error per term (Section 3.2).

Reframe this to emphasize that the criterion compares candidate partial sums against the known Leibniz partial sums at each index k = 0, ..., 19. The 10^-6 tolerance is floating point tolerance for numerical equivalence, not a modeling choice. The question is "does this expression produce the same term sequence as Leibniz?" not "does this get close to π/4?"

**Replace the sentence above with something like:**

> An expression counts as a discovery if its terms match the Leibniz series term by term. We compute f(k) for k = 0, ..., 19 and compare against the known Leibniz values (-1)^k/(2k+1); a tolerance of 10^-6 per term accommodates floating point arithmetic (Section 3.2).

**Provenance:** Discover the actual values (number of terms checked, tolerance threshold) from the source scripts. Check both:
- `gp-leibniz-v3/gp_leibniz_v3_minimal.py`
- `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py`

Search for the discovery/verification criterion in the code (look for functions that check whether an expression matches Leibniz, and the constants they use). If the scripts define `LEIBNIZ_REFS` or similar precomputed reference values, note that in the edit: the comparison is against precomputed Leibniz partial sums, not against π/4.

If the 20-term and 10^-6 values are defined as constants in the scripts, register them as Seldon results with provenance pointing to the source file and line. If they are hardcoded inline, note the file and line but still register. Use `{{result:NAME:value}}` references in the paper text.

---

## Task 2: Explain the terminal expansion pattern in 4.3

The current text says the alternating positive/negative pattern "controls for primitive availability." This undersells the design rationale.

**After the sentence** "Additional integers follow the pattern 3, -2, 4, -3, 5, -4, ..., alternating positive and negative with no zero and no duplicates of base terminals," **add one sentence:**

The alternating sign pattern ensures that at every terminal count N, the set contains building blocks for both the oscillating numerator (requiring negative bases for (-1)^k) and the odd-indexed denominator (requiring positive integers for 2k+1 variants). Additional terminals provide alternative construction paths for these structural components, not inert noise.

(Rewrite to comply with conventions: max 35 words per sentence, active voice, no bold in prose. May need to split into two sentences.)

---

## Task 3: Consolidated primitives table

Create a new subsection (or expand 4.3) with a consolidated table of all primitives used across experiments. This table must be discovered from the source scripts, not hardcoded.

**Operators:** Discover from the GP engine code. Check `gp-leibniz-v3/gp_leibniz_v3_minimal.py` and `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py` for the operator/function set definitions. Include:
- Each operator name and arity
- Safe division: what value is returned on division by zero? (Find the actual return value in the code.)
- Power operator: what constraints apply? (Integer rounding of exponent? Overflow behavior? Find the actual overflow return value in the code.)

**Note in the prose** that safe division's return value (discover it; believed to be 1.0) acts as an implicit additional terminal. Same for power overflow's return value. A reviewer who counts "4 terminals" should know the effective terminal count is higher due to these implicit constants.

**Terminals:** The table in 4.3 already shows terminal sets at each N. Verify it against the source. Check `entropy-leibniz-v3/scaling_heatmap.py` for the terminal construction logic used in the scaling grid. Confirm that the pattern described in prose matches what the code actually does.

Register any newly discovered design parameters (safe_div_return, pow_overflow_return, pow_exponent_rounding) as Seldon artifacts with provenance to the source file and line.

**Table format suggestion** (adjust as needed):

| Component | Value | Notes |
|-----------|-------|-------|
| Binary operators | +, -, ×, ÷, ^ | Standard arithmetic |
| Unary operators | neg | Negation |
| Safe division (÷ by 0) | → [discover from code] | Implicit terminal |
| Power overflow (\|result\| > [discover threshold]) | → [discover from code] | Implicit terminal |
| Power exponent | Rounded to nearest integer | Constrains search to integer powers |

Then the existing terminal set table by N.

---

## Task 4: Unify time budget language

The current text states two different time budgets in two different subsections:
- 4.2: "360 seconds for minimal terminal runs and 1,800 seconds for the scaling grid"
- 4.4: "1,800-second time budget per seed"

These are actually two different things: per-seed budget vs total budget. Discover the actual values from the source scripts:
- `gp-leibniz-v3/gp_leibniz_v3_minimal.py`: look for `MAX_SEED` and `MAX_TOTAL`
- `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py`: same
- `entropy-leibniz-v3/scaling_heatmap.py`: look for time budget parameters

**Consolidate** all time budget information into one place in 4.2. State clearly:
- Per-seed budget for minimal runs: [discover] seconds
- Per-seed budget for scaling grid runs: [discover] seconds
- Total budget per configuration: [discover] seconds
- Whether these are pragmatic compute constraints (they are) or theoretically motivated

**Add one sentence** referencing the extended time test as evidence that the time budget is not a confound. The extended time test data lives in `gp-leibniz-v3/results_gp_extended_t10_p5000/`. Discover the actual runtime and result (believed to be 2hr/seed, 1/5 discovery, same seed as 30-min run). Register the extended time result if not already a Seldon result.

Remove the time budget mention from 4.4 to avoid duplication (4.4 can reference 4.2 for time budgets).

---

## Task 5: Cross-reference operator set

Section 4 describes terminals exhaustively but never mentions the operator set. The search space depends on both.

**Add one sentence** in 4.2 or 4.3 cross-referencing Section 3.1 for the operator set: "The function set (Section 3.1) is held constant across all experiments: binary {+, -, ×, ÷, ^} and unary negation."

(Exact wording should match what's actually in Section 3.1. Discover from the file.)

---

## Post-flight

After all edits:

```bash
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
```

Verify Tier 1 clean. Report any new warnings.

---

## Do NOT

- Do not edit `paper/sections/03_methods.md`. Read-only reference.
- Do not hardcode any values. All numbers come from source scripts or data files.
- Do not overwrite any existing CC task files.
- Do not change the structure or ordering of sections beyond what's specified here.
- Do not add bold in prose. Do not use em dashes. Follow `conventions.md`.
- Do not add speculative text. Every claim must trace to source.
