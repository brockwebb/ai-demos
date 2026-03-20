# Research Notes — Supplementary: The Core Finding

**Tag:** `RESEARCH_NOTES_SUPP_core_finding`
**Date:** 2026-03-16
**Context:** The single most important takeaway from the entire project, distilled. This should be the thesis of the paper.

---

## The Finding

Constrain your search space to the primitives that matter.

The GP found Leibniz at 4 terminals and couldn't at 15. Not because the fitness broke, not because the algorithm failed, but because irrelevant primitives drown out the signal. The narrower the solution space, the better. That's what the data says.

## Why It Matters Beyond This Project

This maps to machine learning directly: feature selection matters more than model architecture. Throwing more parameters at a problem doesn't help if most of them are noise terminals. The signal gets pushed to the tail of the distribution. Regularization can't fix it past a threshold. The parsimony experiment proved that.

The project demonstrated this with mathematical precision:
- At 4 terminals, 5/5 seeds found the answer. The search space was small enough that the correct generator was reachable.
- At 15 terminals, 0/5 seeds found the answer. The same correct generator still existed. The same fitness function still ranked it as optimal. But irrelevant primitives expanded the search space exponentially, pushing the correct answer into the tail of the distribution where no achievable population size could find it.
- No fitness function fixed this. Not log-precision. Not convergence-aware. Not gradient-based. Not extended checkpoints. Not heavier penalties. The fitness was never the bottleneck. The search space was.
- Parsimony pressure (the GP equivalent of regularization) couldn't fix it either. Above a narrow threshold, parsimony collapsed the population to trivial solutions rather than driving it toward the correct compact answer. Weight decay in ML behaves the same way.

## The Implication

The lesson is not "use better algorithms." The lesson is "use fewer, better-chosen primitives." The quality of the search space dominates the quality of the search. A perfect fitness function in a bloated search space loses to a mediocre fitness function in a constrained search space.

For ML: a smaller model with well-chosen features will find the generalizing function. A larger model with noisy features will find wrong-limit attractors (overfitting solutions that score well on the training set but converge to the wrong limit). More data, more compute, and more regularization cannot compensate for a search space full of irrelevant dimensions.

This is the experimental version of Occam's Razor, demonstrated with controlled experiments and quantified with combinatorial analysis.
