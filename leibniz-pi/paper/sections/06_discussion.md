# Discussion

We first analyze the convergence structure that makes Leibniz detectable (6.1), then generalize the discovery mechanism (6.2), draw the analogy to broader AI systems (6.3), and identify implications for the symbolic regression community (6.4).

## Second-Order Kinetics Connection

Leibniz's error decays as 1/(2T+1), algebraically 1/T behavior. Plotting 1/error versus T yields a straight line. In chemical kinetics, this is the signature of a second-order reaction: the rate depends on the product of two concentrations, or the square of one.

![Reciprocal error versus evaluation depth T for the Leibniz series](figures/fig4_second_order_kinetics.png)

**Figure 3:** Reciprocal error (1/|S(T) - pi/4|) versus evaluation depth T for the Leibniz series. The linear relationship confirms second-order convergence structure. The computed values (slope approximately 2) track the theoretical bound 2T+1 with a constant offset due to the alternating series remainder.

The parallel is structural, not rigorous; we do not claim the kinetics framework predicts convergence rates for arbitrary series. Each Leibniz term's correction depends on two interacting quantities: the position k, which determines the magnitude 1/(2k+1), and the alternating sign (-1)^k, which determines the direction. A process depending on only one quantity would exhibit exponential (first-order) convergence. The interaction of two quantities produces 1/T convergence, fundamentally slower but with a distinctive constant-rate signature on a log scale.

The log-precision fitness measures precision(T) = log₂(2T+1), which grows logarithmically. The rate d(precision)/d(log T) is constant: log₂(10) ≈ {{result:info_rate_3_32:value}} bits per decade. The constant rate is the integrated form of the second-order rate law. The convergence-aware fitness asks a first-order question: "is error shrinking between checkpoints?" The log-precision fitness asks a second-order question: "is 1/error growing linearly?" Fewer processes satisfy the second-order criterion. Leibniz is the simplest among them in the minimal terminal set.

## Discovery = Fitness Quality × Coverage / Search Space

The unifying result across all experiments is consistent with a proportionality: P(discovery) scales with fitness quality times coverage, divided by search space size. We propose this as an organizing principle consistent with the data, not a derived result.

$$P(\text{discovery}) \propto \frac{\text{fitness quality} \times \text{coverage}}{\text{search space size}}$$

Fitness quality is fixed: the log-precision fitness correctly identifies Leibniz as optimal in all tested configurations. Improving the fitness function, through extended checkpoints, gradient-based selection, or rate consistency penalties, does not improve discovery rates at 15 terminals. The gradient-based selection variant minimized the gradient norm across fitness dimensions (precision, monotonicity, rate, and parsimony balance), selecting for expressions where perturbing the tree produced the smallest change across all dimensions. It produced 0/5 discovery at 15 terminals. That failure confirmed the coverage diagnosis: the fitness landscape was not the bottleneck, the correct building blocks were absent from the population.

Coverage increases with population size, but the relationship is not simple. @Sastry2005PopulationSizing derived a population-sizing relationship for GP from building-block decision-making theory, showing that the required population grows with the number of building blocks that must be simultaneously present and the difficulty of distinguishing them under selection. Search space scales combinatorially with terminal count: adding one terminal multiplies the number of distinct expressions at each tree size. The space grows much faster than coverage.

The phase transition occurs where coverage/search_space drops below the threshold needed for the correct building blocks to appear in the initial population and survive long enough for selection to assemble them. The scaling grid confirms this quantitatively: the t=10 boundary holds across all tested population sizes, and larger populations produce only marginal improvements at t=6 and t=8. Our population range (1,000 to 10,000) does not reach the scales tested in some GP studies; however, the sharpness of the transition between t=8 and t=10, which holds across a 10x population range, suggests the bottleneck is structural rather than computational.

## The Confabulation Analogy

The project uses wrong-limit attractors as an analogy for confabulation in language models: outputs that appear correct within a finite evaluation horizon but fail under asymptotic scrutiny.

*Non-GP approaches.* Preliminary experiments with reinforcement learning and ant colony optimization (not reported here) produced outputs that pattern-matched to convergence behavior but diverged under extended evaluation, a failure mode analogous to confabulation.

*GP with convergence-aware fitness.* This produced miscalibration: outputs that approached a plausible value and stopped improving, analogous to a model that gives a confident answer without the capacity for further refinement.

*Leibniz.* This exhibits sustained refinement: precision improves at a constant rate without bound, never plateauing, each term contributing a measurable correction. The open-ended precision gain is the series-domain analog of a model that continues to incorporate new evidence without converging prematurely.

A language model that generates a plausible citation to a paper that does not exist exhibits the same structure: the output is locally consistent within the generation horizon (correct formatting, topically relevant author names, reasonable year) but false under verification. The generated citation is a wrong-limit attractor in text space.

The analogy is imperfect but productive. Both phenomena arise from optimization against finite evaluation: a fitness function or loss function that rewards local plausibility without the capacity to verify global correctness. The remedy in both cases is not better loss functions but better questions, evaluating process properties (sustained improvement, calibration) rather than output properties (proximity to a target).

## Implications for Symbolic Regression

Three findings extend beyond the Leibniz problem, each pointing toward a different aspect of fitness-guided search over infinite-horizon processes.

*Process-level fitness design.* Standard symbolic regression evaluates pointwise accuracy. For problems involving infinite-horizon behavior, such as convergence, stability, or asymptotic scaling, process-level fitness functions that evaluate behavior across evaluation depths may be necessary. The log-precision approach demonstrated here is one such instantiation.

*Wrong-limit attractors are a distinct failure mode.* They are not bloat: they are simpler than the correct answer. They are not overfitting: they genuinely converge. They are not fitness function errors: the fitness ranks them correctly when the correct answer is present. They are coverage failures exploiting the evaluation horizon, and they require a different diagnosis and response than the failure modes typically discussed in symbolic regression.

*The evaluation horizon trap is fundamental.* Any finite evaluation horizon creates exploitable wrong-limit attractors. This constraint applies to any fitness-guided search over infinite-horizon processes, not just GP-based symbolic regression. Extending the horizon shifts the attractor landscape but does not eliminate it.

