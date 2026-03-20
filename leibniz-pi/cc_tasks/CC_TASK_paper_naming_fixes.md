# CC Task: Paper Naming Fixes — Post-Skeleton Corrections

## Context

The paper skeleton task (CC_TASK_paper_skeleton.md) is already running. Do NOT modify that file. This task applies corrections AFTER the skeleton is written.

Run CC_TASK_rename_entropy.md FIRST (it handles the bulk rename across research notes). Then run this task to fix anything in the paper sections that the skeleton task wrote with the old terminology.

## Changes to Apply to paper/sections/*.md

### 1. Fitness function naming

Search and replace in all paper section files:

| Wrong | Correct |
|-------|---------|
| entropy fitness | log-precision fitness |
| information-theoretic fitness | log-precision fitness |
| entropy / info-theoretic (as fitness name) | log-precision |
| information gain rate | precision gain rate |
| information gain | precision gain |

Keep "bits" and "bits/decade" — those are accurate units of -log₂(error).

### 2. Slime mold

One mention is allowed, in 03_methods.md or 01_introduction.md, as the pedagogical inspiration for the parallel search approach. Example: "The evolutionary search operates like a slime mold exploring paths in parallel, reinforcing the most efficient structures — but we refer to this as the convergence-aware fitness throughout."

After that single introductory mention, use "convergence-aware fitness" exclusively. The word "slime mold" should not appear again in any other section.

### 3. Strip thermodynamic framing

If the skeleton task wrote any of these in 06_discussion.md or elsewhere, remove them:
- "free energy"
- "steady-state dissipation"
- "far from equilibrium"
- "entropy reduction"
- "thermodynamic interpretation" (as a subsection)

The second-order kinetics observation is real math and stays: 1/T error decay, straight line on 1/error vs T, the integrated rate law structure. But present it as a property of Leibniz's convergence, not as thermodynamics.

Replace any "thermodynamic interpretation" subsection with a brief note: "The log-precision fitness measures -log₂(|error|). The constant rate of 3.32 bits per decade equals log₂(10), a property of the 1/(2T+1) error decay, not of any thermodynamic process."

### 4. Update paper/conventions.md terminology section

If the skeleton task wrote conventions with the old names, fix the terminology entries:

- Remove any entry for "Information-theoretic fitness" or "entropy fitness" as acceptable terms
- Add: **"Log-precision fitness"** for the fitness function that measures -log₂(|error|). Not "entropy fitness," "information-theoretic fitness," or "info fitness." The function is not entropy.
- Add: **"Slime mold"** may appear once as an analogy for the parallel search mechanism. After that, use "convergence-aware fitness" exclusively.

### 5. Update banned terms

In paper/paper_style_config.yaml, add to the paper_specific banned_phrases section:

```yaml
  paper_specific:
    - "hallucination"
    - "ablation"
    - "entropy fitness"
    - "information-theoretic fitness"
    - "thermodynamic interpretation"
    - "free energy"
    - "steady-state dissipation"
```

## Verification

After all edits, in paper/sections/*.md:
- "entropy fitness" should appear zero times
- "information-theoretic fitness" should appear zero times (except when citing external literature that uses the term)
- "log-precision fitness" should appear in every section that discusses the fitness function
- "slime mold" should appear at most once, in one section
- "free energy" should appear zero times
- "thermodynamic" should appear zero times (or only in the context of "this is not a thermodynamic claim")
- "convergence-aware fitness" should be the only name used for the first-order fitness after any introductory mention

## Do NOT

- Do not modify CC_TASK_paper_skeleton.md
- Do not modify any Python scripts
- Do not modify any _data.json or results files
- Do not modify RESEARCH_NOTES.md (that's handled by CC_TASK_rename_entropy.md)
