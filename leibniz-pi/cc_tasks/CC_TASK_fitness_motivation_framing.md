# CC Task: Fitness Design Motivation — Framing for Paper Sections

## Context

The log-precision fitness (-log₂(|error|)) was originally called "entropy fitness" and framed as information-theoretic. That framing has been removed (see CC_TASK_rename_entropy.md and CC_TASK_paper_naming_fixes.md) because the fitness is not entropy.

This task provides guidance on how to frame the fitness function's design motivation in the paper. Apply when writing or revising 03_methods.md and 06_discussion.md.

## Primary framing: reaction kinetics (use this)

The log-precision fitness was designed by asking: what convergence signature distinguishes Leibniz from wrong-limit attractors? The answer: constant precision gain per decade on a log scale.

After the fact, we recognized this as the integrated form of a second-order rate law:
- Leibniz error decays as 1/(2T+1), which is 1/T behavior
- Plot 1/error vs T: straight line — the textbook signature of second-order kinetics
- The log-precision fitness measures log₂(1/error) = log₂(2T+1), which grows at a constant rate per decade
- That constant rate (3.32 bits/decade = log₂(10)) is a property of the 1/T decay, not of any thermodynamic process

This is the design story: the fitness asks a second-order question ("is 1/error growing linearly?") rather than a first-order question ("is error shrinking?"). The kinetics analogy explains why the second-order question is more selective — fewer processes satisfy it.

Present the kinetics connection as a mathematical observation, not as a claim about physics. The equations are real. The analogy to chemical kinetics is structural, not physical.

## Secondary framing: information theory acknowledgment (brief, one sentence)

In the methods section, when first introducing -log₂(|error|), it is acceptable to note: "The quantity -log₂(|error|) has the same mathematical form as Shannon's self-information, though it is not entropy in the information-theoretic sense — it measures precision of a single estimate, not uncertainty over a distribution."

This is a one-sentence acknowledgment. Do not develop it further. Do not use it to justify the fitness design. Do not call the fitness "information-theoretic" or "entropy-based."

## What NOT to write

- Do not frame the fitness as "inspired by entropy" or "inspired by information theory"
- Do not write a "thermodynamic interpretation" subsection
- Do not use "free energy," "dissipation," "far from equilibrium"
- Do not claim the fitness measures "information gain" — it measures precision gain
- Do not suggest the kinetics connection was a design input — it was recognized after the fact

## Do NOT

- Do not modify any existing task files
- Do not modify any Python scripts or data files
