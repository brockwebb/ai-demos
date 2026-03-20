# CC Task: Methods Section (03) Verification and Minor Edits

**Date:** 2026-03-20
**Scope:** `paper/sections/03_methods.md`
**Constraint:** All numbers must be discovered from source scripts or data files. No hardcoded values. Follow `paper/conventions.md` and `paper/glossary.md`.

---

## Pre-flight

1. `seldon go --brief --project-dir /Users/brock/Documents/GitHub/ai-demos/leibniz-pi`
2. Read `paper/conventions.md` and `paper/glossary.md` before writing any prose.
3. Read current state of `paper/sections/03_methods.md`.
4. Read current state of `paper/sections/04_experimental_design.md` (reference for cross-referencing; do not edit).

---

## Task 1: Reframe discovery criterion in 3.2

The current text reads:

> "An expression counts as a discovery if its first 20 terms match the Leibniz series to within 10^-6 absolute error per term, verified at k = 0, 1, ..., 19."

Section 4.2 was updated (cc task `2026-03-17_experimental_design_review.md`) to reframe the discovery criterion as a term-by-term comparison against precomputed Leibniz values, with the tolerance as floating point accommodation. Section 3.2 is the formal definition and must match.

Reframe to emphasize that the check compares candidate f(k) against the known Leibniz values (-1)^k/(2k+1) at each k. The tolerance accommodates floating point arithmetic. The question is "does this produce the same term sequence as Leibniz?"

**Discover from source:** Find the actual verification function in both `gp-leibniz-v3/gp_leibniz_v3_minimal.py` and `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py`. Confirm the number of terms checked and the tolerance value. The values in the paper must match what the code does. If they don't match, flag the discrepancy — do not silently fix it.

---

## Task 2: Replace duplicated time budgets in 3.2 with cross-reference

Section 3.2 currently states time budgets in two places:
- "Each seed runs for at most 360 seconds, with a 1,800-second total budget per configuration."
- Stopping criteria paragraph: "Time budgets vary by experiment: 360 seconds per seed for minimal terminal runs, 1,800 seconds per seed for the scaling grid (Section 4)."

The experimental design task consolidated all time budget information into Section 4.2. Section 3.2 should not duplicate these values. Replace both instances with a cross-reference: "Time budgets vary by experiment (Section 4.2)."

Keep the stopping criteria description (early stopping after 100 generations of no improvement, etc.) since that is method, not experimental design.

---

## Task 3: Verify "approximately 4.4 bits" at T=10 from source

Section 3.3.2 states:

> "Leibniz at T=10 has precision approximately 4.4 bits"

**Discover this value from source.** Compute or find -log₂(|S(10) - π/4|) where S(10) is the Leibniz partial sum at T=10. Check if this value exists in any `_data.json` files, result logs, or can be computed from `LEIBNIZ_REFS` in the source scripts.

If the value is verified from source: check whether it already exists as a Seldon result. If not, register it with provenance to the source.

If the value CANNOT be verified from source: flag it as an unverifiable literal. Do not invent provenance. Report the discrepancy so it can be resolved.

Replace the bare literal in the paper with a `{{result:NAME:value}}` reference once verified and registered.

---

## Task 4: Reorder crystallization paragraph in 3.3.2

The crystallization design motivation paragraph currently sits between the precision formula and the fitness formula, interrupting the technical flow. The paragraph begins "The design came from a chemical engineering perspective..." and ends "...This connection is discussed in Section 6.1."

Move this paragraph to after the fitness formula and its parameter description. The technical flow should be: precision definition → fitness formula → weights and parameters → then the design motivation paragraph explaining where the idea came from.

Do not cut or alter the paragraph content. Only move it.

---

## Task 5: Verify the wrong-limit attractor expression in 3.3.3

Section 3.3.3 uses the expression `5/((6+4k)(k-2))` as an example of a wrong-limit attractor. This expression also appears in Section 5.2.

**Discover from source:** Find this expression in the experiment data (check `_data.json` files in `entropy-leibniz-v3/`, particularly the stress test or scaling heatmap runs). Verify it matches exactly.

Check whether this expression is registered in Seldon. If not, register with provenance to the data file where it was found.

If the expression CANNOT be found in any source data: flag it as unverifiable. Do not fabricate provenance.

Ensure the expression is consistent between 3.3.3 and 5.2.

---

## Task 6: Verify configuration literals in 3.2 from source

Section 3.2 contains several configuration values that should be verified against source scripts:

- Early stopping: "100 generations of no improvement" — discover from source
- Early stopping precision threshold: "13.0 bits" — discover from source
- Diversity injection: "worst 100 individuals" — discover from source
- Diversity injection trigger: "top 20 fitness values become identical (to six decimal places)" — discover from source
- Mutation subtree max depth: "3" — discover from source
- Max nodes: "30" — discover from source
- Initialization depth range: "2–5" — discover from source

For each: find the actual value in `gp-leibniz-v3/gp_leibniz_v3_minimal.py` and `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py`. Confirm the paper matches the code. If both scripts use the same values, good. If they differ, flag it.

These are fixed engine parameters (not measured results), so they may remain as literals per conventions. But they must be verified against source. Any value that cannot be found in source is an unverifiable claim and must be flagged.

---

## Post-flight

After all edits:

```bash
python paper/check_glossary.py
seldon paper sync
seldon paper build --no-render
```

Verify Tier 1 clean. Report any new warnings.

Report a summary of:
- Values verified from source (with file and line)
- Values that could NOT be verified (flag for manual review)
- Any discrepancies between paper and source

---

## Do NOT

- Do not edit any section file other than `paper/sections/03_methods.md`.
- Do not assume any value is correct. Verify everything from source.
- Do not register results without provenance. If source cannot be found, flag it — do not fabricate.
- Do not overwrite any existing CC task files.
- Do not add bold in prose. Do not use em dashes. Follow `conventions.md`.
- Do not alter the crystallization paragraph content (Task 4). Move only.
