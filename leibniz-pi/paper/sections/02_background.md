# 2. Background and Related Work

## 2.1 Symbolic Regression

Symbolic regression searches for mathematical expressions that fit data, simultaneously discovering both the functional form and its parameters. Unlike conventional regression, which assumes a model structure and optimizes coefficients, symbolic regression explores the space of all compositions of a given operator and terminal set.

The foundational work of Schmidt and Lipson (2009) demonstrated that GP-based symbolic regression could rediscover Hamiltonians and Lagrangians from experimental data, including conservation laws not explicitly present in the fitness objective. This result was widely interpreted as evidence that symbolic regression could extract natural laws from data without domain knowledge. Hillar and Sommer (2012) subsequently showed that the operator set and fitness structure implicitly encoded physical priors: the "laws" were partially baked into the search space. This critique parallels our own injection confound (Section 5.1), where seeding the initial population with the target formula created the illusion of discovery when the formula was merely preserved through elitism.

Modern symbolic regression systems include PySR (Cranmer, 2023), which uses multi-population evolutionary search with a Pareto front trading accuracy against complexity. Neural-guided approaches include SymbolicGPT (Valipour et al., 2021), which uses transformers to predict symbolic expressions, and DySymNet (Li et al., 2023), which combines neural networks with symbolic search. GFlowNet-based methods (Li et al., 2023) frame symbolic regression as a generative flow problem. MCTS approaches (Kamienny et al., 2023; Shojaee et al., 2023) use tree search with learned value functions. EGG-SR (Jiang et al., 2025) applies equality saturation for canonicalization. All of these systems optimize pointwise fitness, minimizing error between predicted and observed values at discrete (x, y) pairs. None address the problem class we consider: evaluating the convergence properties of an infinite-horizon generating process against a known limit.

## 2.2 Fitness Design for Convergent Processes

The standard symbolic regression fitness is root-mean-square error between predicted and observed outputs. Pareto-based approaches add complexity as a second objective. Parsimony pressure, penalizing expression size, is the simplest form.

For infinite-horizon convergent processes, pointwise fitness is insufficient. A series that sums to 0.7851 (close to π/4 ≈ 0.7854) at T=10,000 terms would score well on pointwise accuracy but has no structural relationship to Leibniz. The fitness must instead evaluate how partial sums *behave* across evaluation depth: whether error decreases monotonically, whether the rate of improvement is sustained, whether the information gain follows a predictable scaling law.

We are not aware of prior work that designs fitness functions for this objective class. The closest analog is in time-series forecasting, where models are evaluated on multi-step-ahead prediction quality rather than single-point accuracy. The Leibniz problem requires evaluation at geometrically spaced depths (5, 10, 20, 50, ..., 10000 terms), not sequential future steps.

## 2.3 Wrong-Limit Attractors

The symbolic regression literature extensively discusses *bloat*, the tendency of GP to produce increasingly complex expressions that overfit without improving generalization. Our failure mode is distinct: wrong-limit attractors are structurally *simpler* than the correct answer and converge to a finite limit. They score well on the fitness function because their limit happens to fall near π/4 within the evaluation horizon.

Wrong-limit attractors exploit a fundamental asymmetry: there are infinitely many rational functions P(k)/Q(k) whose partial sums converge to finite values near any target, and only one Leibniz. As the terminal set grows, the density of accessible wrong-limit attractors increases combinatorially while the correct answer remains a single point in the expression space. The fitness function correctly ranks Leibniz above any wrong-limit attractor when both are present, but the search must first assemble the correct building blocks, which becomes exponentially less likely as the search space expands. We are not aware of prior work that analyzes wrong-limit attractors as a distinct failure mode in symbolic regression, separate from bloat or overfitting.

## 2.4 The Evaluation Horizon Trap

Any finite evaluation horizon T_max creates a class of expressions indistinguishable from the correct answer within that horizon. Extending T_max does not eliminate this class: it shifts the attractor landscape. At T_max = 10,000, an expression converging to 0.7854 (vs π/4 ≈ 0.78540) scores nearly identically to Leibniz. At T_max = 100,000, that expression would be distinguishable, but new attractors, converging to values even closer to π/4, would take its place.

The evaluation horizon trap is not a limitation of our specific fitness function but a structural property of any finite evaluation of infinite-horizon processes. We document it as a constraint on fitness-guided search in this problem class.
