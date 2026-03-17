# 6. Discussion

## 6.1 Second-Order Kinetics Connection

Leibniz's error decays as 1/(2T+1), algebraically 1/T behavior. Plotting 1/error versus T yields a straight line. In chemical kinetics, this is the signature of a second-order reaction: the rate depends on the product of two concentrations, or the square of one.

The analogy is structural. Each Leibniz term's correction depends on two interacting quantities: the position k, which determines the magnitude 1/(2k+1), and the alternating sign (-1)^k, which determines the direction. A process depending on only one quantity would exhibit exponential (first-order) convergence. The interaction of two quantities produces 1/T convergence, fundamentally slower but with a distinctive constant-rate signature on a log scale.

The log-precision fitness measures precision(T) = log₂(2T+1), which grows logarithmically. The rate d(precision)/d(log T) is constant: log₂(10) ≈ {{result:info_rate_3_32:value}} bits per decade. The constant rate is the integrated form of the second-order rate law. The convergence-aware fitness asks a first-order question: "is error shrinking between checkpoints?" The log-precision fitness asks a second-order question: "is 1/error growing linearly?" Fewer processes satisfy the second-order criterion. Leibniz is the simplest among them in the minimal terminal set.

We present this as a structural observation recognized after the experiment, not a design input or proven result. The kinetics analogy is productive for intuition. The mathematical correspondence should not be taken beyond the specific decay-rate relationship described here.

The design intuition and the kinetics mathematics arrived at the same place by independent routes. The fitness was designed to reward constant-rate precision gain along the slowest, most sustained path. The second-order kinetics framework independently characterizes that same convergence structure as a 1/T rate law. That convergence, engineering intuition and mathematical characterization reaching the same criterion, provides stronger grounds for the fitness design than either would alone.

## 6.2 Discovery = Fitness Quality × Coverage / Search Space

The unifying result across all experiments can be stated as a proportionality: P(discovery) scales with fitness quality times coverage, divided by search space size.

$$P(\text{discovery}) \propto \frac{\text{fitness quality} \times \text{coverage}}{\text{search space size}}$$

Fitness quality is fixed: the log-precision fitness correctly identifies Leibniz as optimal in all tested configurations. Improving the fitness function, through extended checkpoints, gradient-based selection, or rate consistency penalties, does not improve discovery rates at 15 terminals. The gradient-based selection variant was the most direct expression of the thermodynamic design intuition. It minimized the gradient norm across fitness dimensions to find the most uniformly balanced process in fitness space, the point closest to steady state in all dimensions simultaneously. It produced 0/5 discovery at 15 terminals. That failure confirmed the coverage diagnosis: the fitness landscape was not the bottleneck, the correct building blocks were absent from the population.

Coverage scales linearly with population size. Doubling the population roughly doubles the initial structural diversity. Search space scales combinatorially with terminal count: adding one terminal multiplies the number of distinct expressions at each tree size. The space grows much faster than coverage.

The phase transition occurs where coverage/search_space drops below the threshold needed for the correct building blocks to appear in the initial population and survive long enough for selection to assemble them. The scaling grid confirms this quantitatively: the t=10 boundary holds across all tested population sizes, and larger populations produce only marginal improvements at t=6 and t=8.

## 6.3 The Confabulation Analogy

The project uses wrong-limit attractors as an analogy for confabulation in language models: outputs that appear correct within a finite evaluation window but fail under asymptotic scrutiny.

*RL and ACO approaches.* These methods produced outputs that pattern-matched superficially to series convergence behavior but diverged under scrutiny, analogous to confabulation: generating plausible-sounding text that does not correspond to correct knowledge.

*GP with convergence-aware fitness.* This produced miscalibration: outputs that approached a plausible value and stopped improving, analogous to a model that gives a confident answer without the capacity for further refinement.

*Leibniz.* This exhibits calibrated behavior: infinite improvement at a constant rate, never fully confident, always refining. The constant-rate precision gain is the series-domain analog of a well-calibrated probability estimate that updates appropriately with evidence.

The analogy is imperfect but productive. Both phenomena arise from optimization against finite evaluation: a fitness function or loss function that rewards local plausibility without the capacity to verify global correctness. The remedy in both cases is not better loss functions but better questions, evaluating process properties (sustained improvement, calibration) rather than output properties (proximity to a target).

## 6.4 Implications for Symbolic Regression

Three findings extend beyond the Leibniz problem, each pointing toward a different aspect of fitness-guided search over infinite-horizon processes.

*Process-level fitness design.* Standard symbolic regression evaluates pointwise accuracy. For problems involving infinite-horizon behavior, such as convergence, stability, or asymptotic scaling, process-level fitness functions that evaluate behavior across evaluation depths may be necessary. The log-precision approach demonstrated here is one such instantiation.

*Wrong-limit attractors are a distinct failure mode.* They are not bloat: they are simpler than the correct answer. They are not overfitting: they genuinely converge. They are not fitness function errors: the fitness ranks them correctly when the correct answer is present. They are coverage failures exploiting the evaluation horizon, and they require a different diagnosis and response than the failure modes typically discussed in symbolic regression.

*The evaluation horizon trap is fundamental.* Any finite evaluation horizon creates exploitable wrong-limit attractors. This constraint applies to any fitness-guided search over infinite-horizon processes, not just GP-based symbolic regression. Extending the horizon shifts the attractor landscape but does not eliminate it.

## 6.5 Design Provenance and Disciplinary Lens

The log-precision fitness was motivated by thinking about entropy in the thermodynamic sense: the second law, the arrow from order to disorder, and the reverse process of reconstructing precision along the slowest sustainable path. The crystallization analogy shaped the design question before any experiments ran. The fitness is not entropy, and it does not measure any thermodynamic quantity. But the thinking that produced it was thermodynamic. The inspiration is honest; the mathematical claim would not be.

This distinction matters for transfer. A researcher approaching the same problem through information theory would likely design a different fitness: one optimizing pointwise entropy reduction or mutual information. A researcher approaching it through optimization theory might design a Pareto front over accuracy and complexity. The chemical engineering lens produced a process-dynamics question: what is the rate order, and is it constant? That question, not the specific mathematical form of the fitness, is the transferable contribution. Fitness design is a form of domain knowledge encoding, and the domain that matters here is the dynamics of the process being searched for, not the search algorithm that finds it.
