# Glossary — Controlled Vocabulary

Authoritative term definitions for this paper. All sections must use these terms
consistently. Banned synonyms are listed explicitly. When in doubt, use the term
as defined here.

This file is both a human reference and a machine-checkable constraint.
Run `python paper/check_glossary.py` to scan sections for banned synonyms.

---

## Core Concepts

**Leibniz series**
: The infinite series π/4 = Σ (-1)^k / (2k+1). The target of all discovery experiments.
: Do not write: "Leibniz formula" (it is a series, not a closed-form formula), "Gregory-Leibniz series" (unnecessary attribution chain for our purposes).

**Discovery**
: The GP found a Leibniz-equivalent expression from random initialization, with no prior knowledge of the target formula.
: Do not write: "rediscovery" (implies prior knowledge), "recovery" (implies reconstruction from known components).
: EXEMPT: "partial recovery" (acceptable when describing a pattern in scaling grid results — recovery in discovery rate, not the GP finding Leibniz)

**Wrong-limit attractor**
: A series whose partial sums converge to a finite value near π/4 within the evaluation horizon, but whose true limit is not π/4. Structurally simpler than Leibniz. Cannot be eliminated by fitness engineering.
: Do not write: "deceptive series", "false positive", "spurious convergent", "false attractor".

**Evaluation horizon**
: The maximum summation depth T_max at which partial sums are evaluated by the fitness function. Creates an inherent ambiguity: expressions converging to nearby but distinct limits are indistinguishable within any finite horizon.
: Do not write: "evaluation window", "test range", "evaluation length".

**Evaluation horizon trap**
: The structural property that any finite evaluation horizon creates a class of wrong-limit attractors indistinguishable from the correct answer within that horizon. Not a limitation of a specific fitness function; a property of finite evaluation of infinite-horizon processes.

**Coverage**
: The fraction of structurally distinct building blocks present in the population at any generation. Determines whether the correct sub-expressions can be assembled by genetic operators.
: Do not write: "diversity" (has a specific GP meaning: variance in fitness values, not structural variety).
: EXEMPT: "diversity injection" (proper noun for the GP mechanism that replaces worst individuals with random trees, not the general population concept)

**Phase transition**
: The sharp boundary between terminal set sizes where discovery succeeds and where it fails. Located between t=8 and t=10 for populations up to 5,000.
: Use "degradation" only if data shows the boundary is gradual rather than sharp (our data shows it is sharp).

**Building blocks**
: Sub-expressions (subtrees) that can be composed by crossover or mutation to form the correct expression. For Leibniz: oscillation (-1)^k, odd denominator (2k+1), and their division.
: Do not write: "components" (too vague), "motifs" (implies a pattern-matching framework we don't use).

## Fitness Functions

**Log-precision fitness**
: Fitness function measuring -log₂(|S(T) - π/4|) across 11 checkpoints spanning three decades (T = 5 to 10,000). Rewards constant precision gain per decade of summation depth. The "second-order" fitness.
: Do not write: "entropy fitness", "information-theoretic fitness" (no connection to Shannon information theory). The name was changed from 'entropy' to 'log-precision' during writing to avoid this confusion.

**Convergence-aware fitness**
: Fitness function rewarding expressions whose partial sums decrease in error between evaluation checkpoints. The "first-order" fitness. Uses 5 checkpoints (T = 10, 50, 200, 1000, 5000).
: Do not write: "GP fitness" (ambiguous), "rate fitness" (ambiguous).

**First-order / second-order (kinetics analogy)**
: By analogy to chemical reaction kinetics. First-order: "is error shrinking?" (convergence-aware fitness asks this). Second-order: "is precision gain sustained at a constant rate across scales?" (log-precision fitness asks this). Leibniz's 1/T error decay is the integrated form of a second-order rate law.
: Present as analogy/observation, not proven result. The analogy is structural, not rigorous.

**Parsimony pressure (λ_p)**
: A penalty term that penalizes larger expression trees. Subtracts λ_p × (number of nodes) from the fitness score. Keeps evolved expressions simple by making the GP prefer shorter solutions. Standard GP technique.
: Synonyms in literature: complexity penalty, bloat control, size penalty.
: In this paper: use "parsimony pressure" on first mention with definition, then "size penalty" or "parsimony" as shorthand.
: Do not write: "complexity penalty" (conflicts with the common use of 'complexity' for expression tree size).

## GP Terminology

**Scaling grid**
: The 7 × 4 matrix of experiments crossing terminal set sizes (N = 4, 6, 8, 10, 12, 15, 20) with population sizes (1,000; 2,000; 5,000; 10,000). Five seeds per cell, 140 runs total. The primary experimental instrument for characterizing the phase transition.

**Checkpoint**
: A specific evaluation depth T at which a fitness function evaluates partial sums. The log-precision fitness uses 11 checkpoints (T = 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000). The convergence-aware fitness uses 5 checkpoints (T = 10, 50, 200, 1000, 5000).
: Do not write: "evaluation point", "sample point", "test depth".

**Terminal set**
: The set of leaf values available to the GP: the variable k plus integer constants. Size denoted as t or N depending on context (be consistent within a section).
: The minimal set is {k, 1, -1, 2}. Expanded sets follow the deterministic construction in Section 4.3.

**Expression tree**
: The tree representation of a candidate series term f(k). Operators are internal nodes; terminals are leaves. Tree size measured in nodes.

**Injection confound**
: The v2 error where Leibniz was seeded into the initial population and survived via elitism, creating the illusion of discovery. Caught and corrected; all v3 experiments use random initialization.
: Frame as: "We made this error, caught it, and corrected it."

**Elitism**
: Preserving the top N individuals across generations unchanged. N_ELITE = 5 in all experiments.

**Diversity injection**
: Mechanism that replaces the worst 100 individuals with fresh random trees when the top 20 fitness values become identical (to six decimal places). Prevents premature convergence to a single attractor.

## Measurement

**Precision (bits)**
: -log₂(|S(T) - π/4|). Measures how many binary digits of π/4 the partial sum has resolved. Not to be confused with machine precision or numerical precision.

**Precision gain rate**
: Bits of precision gained per decade of summation depth. Leibniz gains log₂(10) ≈ 3.32 bits/decade. Constant rate is the signature the log-precision fitness selects for.
: Do not write: "information rate" (information-theoretic connotation; use 'precision gain rate' throughout).

**Monotonicity**
: Fraction of consecutive checkpoint pairs where precision increases by at least 0.5 bits. A component of the log-precision fitness.

## Framing

**Confabulation**
: Preferred over "hallucination" per NIST AI 600-1. Used analogically: wrong-limit attractors are the series-domain analog of confabulation in language models. Both produce outputs that appear correct within a finite evaluation horizon but fail under asymptotic scrutiny.
: Do not write: "hallucination".

**Design provenance**
: The thermodynamic/crystallization intuition that motivated the log-precision fitness design. Honest about the inspiration; does not claim the fitness measures any thermodynamic quantity.
: The phrase "thermodynamic entropy" may appear once in Discussion 6.5 when describing the design origin. Elsewhere use "log-precision fitness" exclusively.
