# 3. Methods

## 3.1 Expression Representation

Candidate series are represented as expression trees over a set of operators and terminals. Each tree defines a function f(k) that maps the integer index k to a term value. The partial sum at depth T is:

$$S(T) = \sum_{k=0}^{T-1} f(k)$$

For Leibniz, f(k) = (-1)^k / (2k+1), and S(T) → π/4 as T → ∞.

*Operators.* Binary operators {+, -, ×, ÷, ^} and unary negation. Division by zero returns 1.0 (safe division). The power operator rounds its exponent to the nearest integer before evaluation, constraining the search to integer powers. Power overflow (|result| > 10^6) returns 1.0.

*Terminals.* A configurable set always containing the variable k and constants. The minimal set is {k, 1, -1, 2}. Expanded sets add integers following a deterministic pattern described in Section 4.3.

To make the search concrete, consider the target f(k) = (-1)^k / (2k+1). The GP must discover three structural building blocks and compose them correctly. First, oscillation: (-1)^k produces the alternating sign, requiring the terminal -1, the variable k, and the power operator composed as pow(-1, k). Second, odd denominator: 2k+1 produces 1, 3, 5, 7, ..., requiring the terminals 2 and 1, the variable k, and multiplication and addition composed as add(mul(2, k), 1). Third, division: the oscillating numerator divided by the growing denominator produces terms of decreasing magnitude with alternating sign.

With the minimal terminal set {k, 1, -1, 2}, these are essentially the only building blocks available. The GP has limited options for constructing oscillation (only (-1)^k works with the available terminals) and limited options for the denominator (only 2k+1 uses all remaining terminals meaningfully). This constraint is why discovery succeeds: the correct answer is one of few well-formed expressions in the search space.

With 15 terminals, the picture changes. Oscillation can be constructed from (-1)^k, (-3)^k, or various other bases. Denominators can be any polynomial or rational function of k. The number of structurally distinct well-formed expressions grows combinatorially, and most of them are wrong-limit attractors.

## 3.2 Evolutionary Search

We use standard GP with ramped half-and-half initialization (depths 2–5), tournament selection (k=7), subtree crossover (P=0.70), subtree mutation (P=0.20), reproduction (P=0.10), and elitism (top 5 preserved). Population sizes range from 1,000 to 10,000 depending on the experiment. Each seed runs for at most 360 seconds, with a 1,800-second total budget per configuration.

Trees are constrained to at most 30 nodes. The depth limit of 6 applies during initialization; genetic operators enforce only the node count constraint. Mutation subtrees are generated with maximum depth 3. A diversity injection mechanism replaces the worst 100 individuals with fresh random trees when the top 20 fitness values become identical (to six decimal places), preventing premature convergence to a single attractor.

No domain-specific operators (such as "alternating sign" or "odd number generator") are included. The search must assemble oscillating convergent behavior from general-purpose arithmetic alone.

*Stopping criteria.* Each run terminates when the time budget is exhausted. The log-precision fitness also triggers early stopping after 100 generations of no improvement once the best expression exceeds 13.0 bits of precision with stable monotonicity. Time budgets vary by experiment: 360 seconds per seed for minimal terminal runs, 1,800 seconds per seed for the scaling grid (Section 4).

*Discovery criterion.* An expression counts as a discovery if its first 20 terms match the Leibniz series to within 10^-6 absolute error per term, verified at k = 0, 1, ..., 19. This post-hoc criterion is applied after the run completes. During the run, the fitness function guides selection, but the discovery determination is independent of the fitness score.

## 3.3 Fitness Functions

### 3.3.1 Convergence-Aware Fitness (First-Order)

The convergence-aware fitness rewards expressions whose partial sums approach π/4 with decreasing error at successive evaluation checkpoints T ∈ {10, 50, 200, 1000, 5000}.

$$\text{fitness}_{\text{conv}} = \text{accuracy} + \alpha \cdot \text{convergence\_bonus} - \lambda_p \cdot \text{nodes}$$

where accuracy = -mean(|S(T) - π/4|) across checkpoints, convergence_bonus = fraction of consecutive checkpoint pairs where error decreases by at least 5%, and nodes is the expression tree size (parsimony pressure — λ_p, a size penalty on expression trees). Weights: α = 0.05, λ_p = 0.005.

We label this a "first-order" fitness by analogy to reaction kinetics (Section 6.1): it asks whether error is shrinking, the simplest convergence question. Many processes exhibit shrinking error over some range. The convergence bonus rewards shrinkage across consecutive checkpoint pairs, but any monotonically converging series, regardless of its limit, can score well.

### 3.3.2 Log-Precision Fitness (Second-Order)

The log-precision fitness evaluates partial sums at 11 checkpoints spanning three decades: T ∈ {5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000}. The denser checkpoint set (compared to the five checkpoints used by the convergence-aware fitness) provides finer-grained measurement of precision gain rate and extends the evaluation horizon to T = 10,000. The fitness measures precision in bits:

$$\text{prec}(T) = -\log_2 |S(T) - \pi/4|$$

The quantity -log₂(|error|) has the same mathematical form as Shannon's self-information, though it is not entropy in the information-theoretic sense: it measures precision of a single estimate, not uncertainty over a distribution. Leibniz at T=10 has precision approximately 4.4 bits; at T=10,000, {{result:leibniz_ti_15_29:value}} bits.

The design came from a chemical engineering perspective on process dynamics. The guiding analogy was crystallization: perfect order reconstructed from disorder along the slowest, most sustained path. Each step adds a small, constant increment of order. Leibniz does the same: each term adds a constant increment of precision about π/4, forever, at a rate that never accelerates or decelerates. The design question was not "which series converges fastest?" but "which series reduces uncertainty at the most constant rate?" That question led to measuring precision on a log scale and rewarding constant gain per decade. We later observed that -log₂(|error|) has the same mathematical structure as the integrated form of a second-order rate law. This connection is discussed in Section 6.1.

The fitness combines three terms:

$$\text{fitness}_{\text{prec}} = w_1 \frac{\text{prec}(T_{\max})}{50} + w_2 \cdot \text{monotonicity} + w_3 \frac{\text{mean\_rate}}{5} - \lambda_p \cdot \text{nodes}$$

where monotonicity = fraction of consecutive checkpoints with ≥ 0.5 bit gain, and mean_rate = precision gain in bits per decade of summation depth. Weights: w_1 = 0.02, w_2 = 0.04, w_3 = 0.03, λ_p = 0.005.

By the same kinetics analogy, this asks a "second-order" question: *is precision gain sustained at a constant rate across scales?* Leibniz gains log₂(10) ≈ {{result:info_rate_3_32:value}} bits per decade. On a log-log plot, this is a straight line. The constant rate is the signature of second-order kinetics (Section 6.1). Fewer processes satisfy this criterion than satisfy first-order error shrinkage.

### 3.3.3 Why the Second-Order Question Is More Selective

Many series exhibit decreasing error. Rational functions like 5/((6+4k)(k-2)) converge monotonically to a finite limit and score well on the convergence-aware fitness. Their precision gain rate is not constant across scales: it accelerates as the series approaches its limit, then plateaus.

Leibniz is unusual: its precision gain rate is constant because its error decays as 1/(2T+1). Plotting 1/error vs T yields a straight line, the integrated form of a second-order rate law. The log-precision fitness selects for this specific convergence structure, making it more discriminating than the convergence-aware fitness. Empirically, the log-precision fitness discovers Leibniz at population 1,000 ({{result:logprec_minimal_5_5:value}}/5 seeds), while the convergence-aware fitness requires population 2,000 for the same reliability.
