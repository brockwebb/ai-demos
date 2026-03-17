# CC Task: Rename "Entropy Fitness" Throughout the Project

## Context

The fitness function we've been calling "entropy fitness" or "information-theoretic fitness" is not entropy and is not information-theoretic. It measures -log₂(|error|), which is log-scale precision. Calling it entropy implies a connection to Shannon information theory or thermodynamics that does not exist. This is a confabulation — the exact kind of error this project studies.

The 3.32 bits/decade figure is log₂(10), a property of the logarithm, not of any information process. The "constant rate of entropy reduction" and "steady-state dissipation" framings are analogical hand-waving.

This task renames consistently across all research notes, documentation, and the paper skeleton. It does NOT touch experiment scripts or data files (those are historical artifacts with their own filenames).

## The Rename

| Old term | New term |
|----------|----------|
| entropy fitness | log-precision fitness |
| information-theoretic fitness | log-precision fitness |
| entropy / info-theoretic (when referring to the fitness) | log-precision |
| bits of information about π/4 | bits of precision about π/4 |
| information gain rate | precision gain rate |
| entropy discovers Leibniz | log-precision fitness discovers Leibniz |
| Information Super-piway (medium draft) | leave as-is (it's a pun, not a claim) |

**Keep "bits" and "bits/decade" — those are accurate.** -log₂(error) has units of bits. That's a mathematical fact, not an information-theoretic claim.

**Keep the second-order kinetics observation** — 1/T error decay producing a straight line on 1/error vs T is real math. But present it as a property of Leibniz's convergence structure, not as evidence of thermodynamic behavior.

## Files to Edit

### RESEARCH_NOTES.md

1. Rename all instances of "entropy fitness" to "log-precision fitness"
2. Rename all instances of "information-theoretic fitness" to "log-precision fitness"
3. In the "Second-Order Kinetics / Thermodynamic Connection" section:
   - Keep the second-order kinetics math (1/T decay, straight line, rate law analogy)
   - Remove or reframe the thermodynamic subsection. Replace "entropy fitness measures the free energy" with: "The log-precision fitness measures how fast error decreases on a log scale. The constant rate of 3.32 bits per decade (= log₂(10)) is a property of Leibniz's 1/(2T+1) error decay, not of any thermodynamic process."
   - Remove: "Systems that minimize free energy at a constant rate are at steady-state far from equilibrium"
   - Remove: "steady-state dissipation rate"
   - Keep the comparison: "GP convergence asks first-order question, log-precision asks second-order question"
4. In experiment progression table: rename "Entropy-GP v2" to "Log-precision GP v2", "Entropy v3 minimal" to "Log-precision v3 minimal", etc.
5. In the scaling grid headers: "entropy fitness" → "log-precision fitness"
6. In the combined comparison table section: same rename

### RESEARCH_NOTES_SUPP_complexity_ceiling.md

1. Rename all instances

### RESEARCH_NOTES_SUPP_applicability.md

1. Rename all instances
2. In the chemical kinetics section: the connection to second-order rate law testing is still valid (it's about the math of 1/T decay, not about entropy). Keep it but remove any thermodynamic language.

### paper/conventions.md (if it exists yet)

1. Under paper-specific terminology: add "log-precision fitness" as the correct term. Ban "entropy fitness" and "information-theoretic fitness" as terms for our fitness function.

### paper/paper_qc_config.yaml or paper_style_config.yaml

1. Add "entropy fitness" and "information-theoretic fitness" to banned_phrases (paper_specific section) with note: "Use 'log-precision fitness' — our fitness is not entropy."

### CC_TASK_paper_skeleton.md

1. Rename throughout. Section 4 title changes from "Two Fitness Functions — Convergence-aware (first-order) and information-theoretic (second-order)" to "Two Fitness Functions — Convergence-aware (first-order) and log-precision (second-order)"

### scaling_heatmap_methodology.md (in entropy-leibniz-v3/)

1. Rename in the methodology description. The fitness function section should describe what it actually computes: -log₂(|error|), not "information gain."

### medium_draft_final.md

1. Do NOT rename here. This is a working draft that will be replaced. Leave it as historical.

## Files NOT to Edit

- Any Python script (.py) — filenames like `entropy_leibniz_v3_minimal.py` are historical. Don't rename files or variables in running code.
- Any _data.json or .txt results files — these are experimental records.
- Any .log files
- The config JSON file

## What to Preserve

- "bits" and "bits/decade" — accurate units
- "second-order" characterization of the fitness — refers to the mathematical order of the convergence rate question (is 1/error linear?), not to thermodynamics
- "log-precision" as the new name — it says exactly what the fitness computes
- The comparison between first-order (convergence-aware) and second-order (log-precision) fitness — this is about the mathematical structure of the question each fitness asks, not about thermodynamic order

## Verification

After all edits, search all .md files in the repo for:
- "entropy fitness" — should only appear in historical context ("previously called entropy fitness") or in filenames
- "information-theoretic fitness" — should not appear except in references to external literature (where other authors use the term)
- "free energy" — should not appear
- "dissipation" — should not appear
- "thermodynamic" — should only appear in "the thermodynamic framing was removed because it was not supported by the math"

Report any remaining instances.
