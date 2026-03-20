# Research Notes — Supplementary: Design Motivation and Intellectual Path

**Tag:** `RESEARCH_NOTES_SUPP_design_motivation`
**Date:** 2026-03-16
**Context:** Documents the actual intellectual path that led to the log-precision fitness design and the min-gradient experiment. This is the honest origin story for the paper's methods section.

---

## The Chemical Engineering Lens

The lead author's background is chemical engineering. This is not incidental. The entire intellectual arc of the fitness design — from thermodynamic intuition through crystallization analogy to the post-hoc recognition of second-order kinetics — follows a ChemE reasoning path. A computer scientist approaching the same problem would likely have reached for information theory (Shannon entropy, mutual information). A physicist might have reached for variational methods or Lagrangian mechanics.

The ChemE lens produced a specific set of questions:
- How does the "reaction" (convergence) proceed? What order is it?
- What is the rate law? Is it constant, accelerating, or decelerating?
- What does the process look like at steady state?
- Where is the equilibrium, and how far are we from it?

These questions led directly to the log-precision fitness: measure the rate of precision gain on a log scale, reward constancy. A CS-derived fitness would more likely have optimized pointwise error (RMSE) or complexity-penalized accuracy (Pareto front). The ChemE lens asked about *process dynamics*, not *output accuracy*, and that difference is what made the fitness work for this problem class.

This is a methodological point for the paper: interdisciplinary lenses produce different fitness designs, and the design matters more than the optimization algorithm. The GP engine is standard. The fitness is not. The fitness came from ChemE thinking.

---

## The Thermodynamic Intuition (what actually motivated the design)

The log-precision fitness was not derived from first principles or from the information theory literature. It came from thinking about entropy in the thermodynamic sense: the second law, the arrow from order to disorder.

The core question was: Leibniz reconstructs precision (order) from uncertainty (disorder) along the slowest possible path. What fitness function selects for that?

The analogy was crystallization. A crystal is perfect order, built incrementally from a disordered state. The process is slow, steady, and sustained. Each step adds a small amount of order. The rate of ordering is constant over time. Leibniz does the same thing: each term adds a small, constant increment of precision about π/4, forever. It never finishes. It never accelerates. It never decelerates. It is the mathematical equivalent of a crystal growing one layer at a time.

The fitness was designed to find the process that reduces disorder (uncertainty about π/4) at the most constant, most sustained rate. Not the fastest convergence. Not the closest final value. The steadiest rate of improvement. That led to measuring precision on a log scale and rewarding constant gain per decade.

---

## The Min-Gradient Experiment (what the thermodynamic thinking actually produced)

The gradient fitness experiments asked for the MINIMUM gradient across the multi-dimensional fitness space, not the maximum. This was not arbitrary. The idea: treat the fitness components (precision, monotonicity, rate) as dimensions of a state space. Leibniz should sit at the point where no single dimension dominates. It's the most balanced, most uniformly excellent process. The minimum gradient in this space corresponds to the flattest, most equilibrated point — the process closest to steady-state in all dimensions simultaneously.

Three variants were tested on 15 terminals:
- Pure gradient magnitude (minimize the norm of the fitness gradient vector)
- Hybrid scalar × uniformity (balance between total fitness and evenness across components)
- Min-component bottleneck (optimize the worst-performing dimension)

All failed (0/5). The failure was a coverage problem, not a fitness design problem. But the intuition behind the experiment was genuinely thermodynamic: find the minimum-energy configuration in fitness space, the point where the system is most uniformly at steady state.

---

## What to say in the paper

The intellectual path is worth one paragraph in the methods section:

"The fitness was motivated by a chemical engineering perspective on process dynamics: the reconstruction of order from disorder along the slowest, most sustained path, analogous to crystallization. This led us to reward constant precision gain rate on a log scale rather than raw proximity to the target value. The resulting fitness, -log₂(|error|), measures how many doublings of precision the partial sum achieves. We later recognized that this corresponds mathematically to the integrated form of a second-order rate law, connecting the design to the reaction kinetics framework that originally inspired it (Section N)."

The ChemE lens is also worth a sentence in the Discussion: "The log-precision fitness emerged from chemical engineering intuition about rate laws and ordering processes. A standard symbolic regression approach would optimize pointwise accuracy. The process-dynamics perspective — asking about convergence rate and order rather than output proximity — produced a qualitatively different and more effective fitness for this problem class."

---

## What NOT to say in the paper

- Do not call the fitness "entropy fitness" or "information-theoretic fitness"
- Do not claim the fitness measures entropy, free energy, or any thermodynamic quantity
- Do not present the thermodynamic analogy as a theoretical result
- Do not overstate the crystallization metaphor — it motivated the design, it does not explain the math

## The distinction

- ChemE lens → real (this is the disciplinary perspective that produced the design)
- Thermodynamic inspiration → real (crystallization, rate laws, steady state)
- Thermodynamic claim about the fitness → not supported (the fitness is -log₂(error), not entropy)
- Second-order kinetics connection → real math (1/T decay, integrated rate law)
- The arc: ChemE background → thermodynamic intuition → crystallization analogy → log-precision fitness → post-hoc kinetics recognition → full circle back to ChemE
