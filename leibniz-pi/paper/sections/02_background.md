# 2. Background and Related Work

## 2.1 Symbolic Regression

Symbolic regression searches for mathematical expressions that fit data, discovering both the functional form and its parameters simultaneously. Unlike conventional regression, which assumes a model structure and optimizes coefficients, symbolic regression explores the full space of compositions over a given operator and terminal set.

Schmidt and Lipson (2009) showed that GP-based symbolic regression could recover Hamiltonians and Lagrangians from experimental data. Their result was widely interpreted as evidence that symbolic regression extracts natural laws without domain knowledge. Hillar and Sommer (2012) subsequently demonstrated that the operator set and fitness structure implicitly encoded physical priors. The "laws" were partially baked into the search space. This critique parallels our own injection confound (Section 4.1). Seeding the initial population with the target formula created the illusion of discovery; the formula was merely preserved through elitism.

Modern symbolic regression spans evolutionary (Cranmer, 2023), transformer-based (Valipour et al., 2021), neural-symbolic (Li et al., 2023), generative flow (Li et al., 2023), tree-search (Kamienny et al., 2023; Shojaee et al., 2023), and equality saturation approaches (Jiang et al., 2025).

All of these systems optimize pointwise fitness: they minimize error between predicted and observed values at discrete (x, y) pairs. None address the problem class we consider, evaluating convergence properties of an infinite-horizon generating process against a known limit.

## 2.2 Fitness Design for Convergent Processes

The standard symbolic regression fitness is root-mean-square error between predicted and observed outputs. Pareto-based approaches add complexity as a second objective. Parsimony pressure (λ_p, a size penalty on expression trees), penalizing expression size, is the simplest form.

For infinite-horizon convergent processes, pointwise fitness is insufficient. A series that sums to 0.7851 (near π/4) at T=10,000 terms would score well on pointwise accuracy but has no structural relationship to Leibniz. The fitness must instead evaluate how partial sums *behave* across evaluation depth. Does error decrease monotonically? Is the rate of improvement sustained? Does the precision gain follow a predictable scaling law?

Prior symbolic regression work does not address fitness design for this objective class. The closest analog is time-series forecasting, where models are evaluated on multi-step-ahead prediction quality rather than single-point accuracy. Both require evaluating trajectory behavior rather than endpoint accuracy, but the Leibniz problem evaluates convergence structure across geometric scales rather than sequential forecast accuracy.

## 2.3 Wrong-Limit Attractors

The symbolic regression literature extensively discusses *bloat*: the tendency of GP to produce increasingly complex expressions that overfit without improving generalization (Poli, Langdon, and McPhee, 2008). Our failure mode is distinct. Wrong-limit attractors are structurally *simpler* than the correct answer and converge to a finite limit. They score well because their limit happens to fall near π/4 within the evaluation horizon.

Wrong-limit attractors exploit a fundamental asymmetry. A large class of rational functions P(k)/Q(k) have partial sums converging to finite values near any target. Only one expression is Leibniz. As the terminal set grows, the density of accessible wrong-limit attractors increases combinatorially. The correct answer remains a single point in the expression space. The fitness function correctly ranks Leibniz above any wrong-limit attractor when both are present. However, the search must first assemble the correct building blocks, and this becomes exponentially less likely as the search space expands. To our knowledge, no prior work analyzes this failure mode as distinct from bloat or overfitting in symbolic regression.

## 2.4 The Evaluation Horizon Trap

Any finite evaluation horizon T_max creates a class of expressions indistinguishable from the correct answer within that horizon. Extending T_max does not eliminate this class; it shifts the attractor landscape. At T_max = 10,000, an expression converging to a value near but not equal to π/4 scores nearly identically to Leibniz. At T_max = 100,000, that expression would be distinguishable. New attractors converging to values even closer to π/4 would take its place.

The evaluation horizon trap is not a limitation of our specific fitness function. The trap is a structural property of any finite evaluation of infinite-horizon processes. We document it as a constraint on fitness-guided search in this problem class.
