# CC Task: Capture Design Motivation in Paper Methods Section

## Context

The file `RESEARCH_NOTES_SUPP_design_motivation.md` documents the actual intellectual path that led to the log-precision fitness. This task ensures that motivation is captured in the paper's methods section (03_methods.md) and discussion section (06_discussion.md).

Run this AFTER CC_TASK_paper_skeleton.md, CC_TASK_rename_entropy.md, and CC_TASK_paper_naming_fixes.md are all complete.

## What to add to 03_methods.md

In the subsection introducing the log-precision fitness, add one paragraph covering the design motivation. The paragraph should convey:

1. The fitness was motivated by an analogy to crystallization: perfect order reconstructed from disorder along the slowest, most sustained path.
2. The design question was: what selects for the process that reduces uncertainty at the most constant rate, not the fastest?
3. This led to measuring precision on a log scale and rewarding constant gain per decade.
4. The resulting fitness, -log₂(|error|), was later recognized as corresponding to the integrated form of a second-order rate law (discussed in the Discussion section).

Read `RESEARCH_NOTES_SUPP_design_motivation.md` for the full context. Write the paragraph in the paper's voice (following conventions.md). Do not use the word "entropy." Do not overstate the crystallization metaphor — it motivated the design, it does not explain the math.

## What to add to 06_discussion.md

In the second-order kinetics subsection, add a sentence connecting back to the design motivation: the thermodynamic intuition about slowest-path ordering led to a fitness that, by mathematical structure, selects for second-order convergence. The intuition and the math arrived at the same place independently.

Also add a brief mention of the min-gradient experiment and its motivation: the min-gradient approach was the most direct expression of the thermodynamic intuition (find the minimum-energy point in the multi-dimensional fitness space), it failed due to coverage, but the failure confirmed the coverage diagnosis rather than invalidating the intuition.

## What to add to 06_discussion.md or a "Speculation / Future Directions" subsection

Acknowledge that the original thinking involved entropy in the thermodynamic sense: the second law, the arrow from order to disorder, and specifically the reverse process of reconstructing order (precision about π/4) along the slowest sustainable path. The log-precision fitness was an attempt to operationalize that idea. The fitness is not entropy, but the thinking that produced it was thermodynamic. This distinction matters: the inspiration is honest, the mathematical claim would not be.

## Do NOT

- Do not call the fitness "entropy fitness" or "information-theoretic fitness"
- Do not claim the fitness measures entropy or free energy
- Do not modify any existing task files
- Do not modify RESEARCH_NOTES_SUPP_design_motivation.md
- Do not modify any Python scripts or data files
