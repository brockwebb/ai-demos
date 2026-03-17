# 3. Methods

## 3.1 Expression Representation

Candidate series are represented as expression trees over a set of operators and terminals. Each tree defines a function f(k) that maps the integer index k to a term value. The partial sum at depth T is:

$$S(T) = \sum_{k=0}^{T-1} f(k)$$

For Leibniz, f(k) = (-1)^k / (2k+1), and S(T) → π/4 as T → ∞.

*Operators.* Binary operators {+, -, ×, ÷, ^} and unary negation. Division by zero returns 1.0 (safe division). Power overflow (|result| > 10^6) returns 1.0.

*Terminals.* A configurable set always containing the variable k and constants. The minimal set is {k, 1, -1, 2}. Expanded sets add integers following a deterministic pattern described in Section 4.3.

To make the search concrete, consider the target f(k) = (-1)^k / (2k+1). The GP must discover three structural components and compose them correctly. First, oscillation: (-1)^k produces the alternating sign, requiring the terminal -1, the variable k, and the power operator composed as pow(-1, k). Second, odd denominator: 2k+1 produces 1, 3, 5, 7, ..., requiring the terminals 2 and 1, the variable k, and multiplication and addition composed as add(mul(2, k), 1). Third, division: the oscillating numerator divided by the growing denominator produces terms of decreasing magnitude with alternating sign.

With the minimal terminal set {k, 1, -1, 2}, these are essentially the only building blocks available. The GP has limited options for constructing oscillation (only (-1)^k works with the available terminals) and limited options for the denominator (only 2k+1 uses all remaining terminals meaningfully). This constraint is why discovery succeeds: the correct answer is one of few well-formed expressions in the search space.

With 15 terminals, the picture changes. Oscillation can be constructed from (-1)^k, (-3)^k, or various other bases. Denominators can be any polynomial or rational function of k. The number of structurally distinct well-formed expressions grows combinatorially, and most of them are wrong-limit attractors.

## 3.2 Evolutionary Search

We use standard GP with ramped half-and-half initialization (depths 2–5), tournament selection (k=7), subtree crossover (P=0.70), subtree mutation (P=0.20), and elitism (top 5 preserved). Population sizes range from 1,000 to 10,000 depending on the experiment.

Trees are constrained to at most 30 nodes and depth 6. A diversity injection mechanism replaces the worst 100 individuals with fresh random trees when the top 20 fitness values become identical, preventing premature convergence to a single attractor.

No domain-specific operators (such as "alternating sign" or "odd number generator") are included. The search must assemble oscillating convergent behavior from general-purpose arithmetic alone.

## 3.3 Fitness Functions

### 3.3.1 Convergence-Aware Fitness (First-Order)

The convergence-aware fitness rewards expressions whose partial sums approach π/4 with decreasing error at successive evaluation checkpoints T ∈ {5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000}.

$$\text{fitness}_{\text{conv}} = \text{accuracy} + \alpha \cdot \text{convergence\_bonus} - \lambda_p \cdot \text{nodes}$$

where accuracy = -mean(|S(T) - π/4|) across checkpoints, convergence_bonus = fraction of consecutive checkpoint pairs where error decreases by at least 5%, and nodes is the expression tree size (parsimony pressure).

This asks a first-order question: *is the error shrinking?* Many processes exhibit shrinking error over some range. The convergence bonus rewards sustained shrinkage, but any monotonically converging series, regardless of its limit, can score well.

### 3.3.2 Log-Precision Fitness (Second-Order)

The log-precision fitness measures precision in bits:

$$\text{prec}(T) = -\log_2 |S(T) - \pi/4|$$

The quantity -log₂(|error|) has the same mathematical form as Shannon's self-information, though it is not entropy in the information-theoretic sense — it measures precision of a single estimate, not uncertainty over a distribution. Leibniz at T=10 has precision approximately 4.4 bits; at T=10,000, approximately 15.3 bits.

The fitness combines three components:

$$\text{fitness}_{\text{prec}} = w_1 \frac{\text{prec}(T_{\max})}{50} + w_2 \cdot \text{monotonicity} + w_3 \frac{\text{mean\_rate}}{5} - \lambda_p \cdot \text{nodes}$$

where monotonicity = fraction of consecutive checkpoints with ≥ 0.5 bit gain, and mean_rate = precision gain in bits per decade of summation depth. Weights: w_1 = 0.02, w_2 = 0.04, w_3 = 0.03, λ_p = 0.005.

This asks a second-order question: *is precision gain sustained at a constant rate across scales?* Leibniz gains exactly log₂(10) ≈ {{result:info_rate_3_32:value}} bits per decade, a straight line on a log-log plot. The constant rate is the signature of second-order kinetics (Section 6.1), and fewer processes satisfy it than satisfy the first-order "is error shrinking?" criterion.

### 3.3.3 Why the Second-Order Question Is More Selective

Many series exhibit decreasing error. Rational functions like 5/((6+4k)(k-2)) converge monotonically to a finite limit and score well on the convergence-aware fitness. Their precision gain rate is not constant across scales: it accelerates as the series approaches its limit, then plateaus.

Leibniz is unusual: its precision gain rate is constant because its error decays as 1/(2T+1). Plotting 1/error vs T yields a straight line, the integrated form of a second-order rate law. The log-precision fitness selects for this specific convergence structure, making it more discriminating than the convergence-aware fitness. Empirically, the log-precision fitness discovers Leibniz at population 1,000 ({{result:entropy_minimal_5_5:value}}/5 seeds), while the convergence-aware fitness requires population 2,000 for the same reliability.
