# Research Notes — Supplementary: Complexity Ceiling and Constructive Search

**Tag:** `RESEARCH_NOTES_SUPP_complexity_ceiling`
**Date:** 2026-03-15
**Context:** Extends the combinatorial coverage analysis in RESEARCH_NOTES.md

---

## The Complexity Ceiling Is a Property of Constructive Search

The combinatorial explosion documented in the main research notes applies equally to both fitness functions. Log-precision fitness has a better constant factor (steeper gradient from second-order signal), but both are linear tools against an exponential search space. This is not a limitation specific to convergence-aware or log-precision fitness. It is a structural property of constructive symbolic search.

### Second-order fitness and least squares

The reason log-precision fitness outperforms convergence-aware fitness is analogous to why least squares (second-order / quadratic loss) outperforms absolute error (first-order loss) in regression. A quadratic loss surface has gradients that point toward the minimum and steepen as you approach it. Absolute error has a constant gradient that provides no acceleration near the answer.

Log-precision fitness measures log-scale precision, a second-order quantity. Its fitness gradient is steeper near Leibniz and flatter near wrong-limit attractors. The convergence-aware fitness measures whether error is shrinking (first-order). Many things satisfy "error is shrinking." Fewer satisfy "log-precision is growing linearly." The selectivity difference is the same as the difference between L2 and L1 optimization: second-order objectives create better-shaped landscapes.

Both face the same exponential search space. The second-order advantage is in exploitation efficiency, not in coverage.

### Constructive search vs combinatorial optimization

The scaling limitation is specific to *constructive* search: building expressions from parts. It does not apply to all evolutionary or biologically-inspired optimization.

The Physarum polycephalum (slime mold) TSP results (Tero et al. 2010, the Tokyo rail network) demonstrate biological optimization at scale. TSP has n! candidate routes, which is combinatorially explosive. But there are two critical differences:

1. **TSP is routing, not construction.** The cities and distances are given. The slime mold rearranges a fixed set of known elements. GP must *construct* the evaluation function from primitives. The difficulty isn't in evaluating candidates — it's in generating structurally correct ones.

2. **TSP has continuous local structure.** Nearby routes (differing by one swap) have correlated costs. Small changes produce small fitness differences. GP expression trees lack this property. Swapping one terminal in a leaf node can change an expression from Leibniz to overflow. The fitness landscape for symbolic construction is discontinuous and rugged.

The slime mold solves large TSP instances because the search space, while vast, has smooth local structure that gradient-following can exploit. Constructive symbolic search has no such smoothness.

### What this means for the paper's scope

The method works for discovering compact formulas from small primitive sets. This is not a limitation to apologize for — it is a characterization of where evolutionary symbolic search is viable. Fundamental physical laws tend to live in this regime:

- F = ma — 3 symbols
- E = mc² — 4 symbols
- Leibniz — 3 operations (power, multiply, divide)
- Maxwell's equations (individual) — compact operator expressions
- Ideal gas law — 4 symbols

These are all expressible with small terminal sets and shallow trees. The combinatorial ceiling bites when either the terminal set is large (many irrelevant primitives diluting coverage) or the target expression is deep and wide (many nodes requiring coordinated assembly).

Navier-Stokes, for example, requires partial derivatives, vector fields, and tensor products — operators not in our primitive set. Even if they were included, the expression tree would be dozens of nodes deep. At that scale, the search space is astronomical regardless of fitness function quality.

The honest framing: evolutionary symbolic search discovers compact laws from small primitive sets. The scaling boundary is not a failure to fix. It is the regime boundary of the method. The interesting finding is that fundamental constants and identities tend to live inside this boundary.

### The wrong-limit attractor problem also scales with expressiveness

As the primitive set grows, not only does the target become harder to find, but the density of wrong-limit attractors increases. With 4 terminals, there are few ways to construct a converging series. With 15, there are many rational functions P(k)/Q(k) whose series telescope to finite values near any target. The attractors are not noise — they are structurally simpler, genuinely converging expressions that the fitness cannot distinguish from the target within finite evaluation.

This is the dual problem: the correct answer becomes harder to find (coverage drops) AND incorrect answers become more numerous and more competitive (attractor density rises). Both effects are exponential in terminal count. The fitness function fights a war on two fronts, and both fronts are losing.

---

## For the Paper Discussion Section

Frame the complexity ceiling as a structural insight, not a limitation:

1. Evolutionary symbolic search has a well-characterized operating regime: compact expressions, small primitive sets.
2. This regime coincides with where fundamental physical and mathematical laws live.
3. The scaling boundary is a property of constructive search, not of any specific fitness function.
4. Second-order fitness (log-precision) improves exploitation efficiency within this regime but cannot extend the regime itself.
5. Combinatorial optimization (like TSP) operates in a structurally different search space — continuous, with local correlations — which is why biological optimizers can solve large TSP instances but cannot construct complex symbolic expressions.

This positions the paper's contribution clearly: we are not claiming GP can discover arbitrary formulas. We are showing that within the viable regime, the *form of the question* (first-order vs second-order fitness) determines whether discovery succeeds, and characterizing where that regime ends.
