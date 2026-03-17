# Research Notes — Supplementary: Applicability and Imagination

**Tag:** `RESEARCH_NOTES_SUPP_applicability`
**Date:** 2026-03-16
**Context:** Where the method and findings transfer beyond Leibniz/π. Organized by strength of transfer: direct application, conceptual transfer, and speculative.

---

## Direct Application (method transfers with minimal adaptation)

### Symbolic regression for dynamical systems

SINDy and PySR fit equations to finite time-series data. Our contribution says: if your target system has asymptotic or steady-state behavior, pointwise fitness over a finite window will find wrong-limit attractors. Process-level fitness is necessary.

This generalizes to any dynamical system identification where long-horizon behavior matters: climate models, population dynamics, epidemiological models, economic equilibrium models. The wrong-limit attractor problem is not specific to Leibniz. Any finite evaluation of an infinite-horizon process creates exploitable attractors.

The practical recommendation: when using GP/SR for dynamical systems, evaluate candidate equations on convergence properties across time scales (precision gain rate, monotonicity of precision, stability of asymptotic behavior), not just pointwise fit on the training window.

### Chemical kinetics rate law discovery

The second-order kinetics connection is not just an analogy. If you wanted to use GP to discover rate laws from concentration-vs-time data, the log-precision fitness framework applies directly. The question "is 1/concentration growing linearly with time?" is the standard test for second-order reactions. Our log-precision fitness is literally asking this question in the convergence domain.

A concrete application: given time-course data from an unknown reaction, use GP with log-precision fitness to search for rate expressions whose integrated form matches the observed behavior across timescales. The fitness would measure bits of precision about the equilibrium concentration gained per decade of observation time. First-order reactions would show exponential convergence (different precision gain signature). Second-order would show the constant bits/decade signature we measured. The fitness function naturally classifies the reaction order.

The wrong-limit attractor problem maps here too: a rate expression that fits the first 10 minutes of data but diverges at steady state is the chemical kinetics equivalent of our t=15 wrong-limit attractors.

### Iterative numerical method design

Iterative solvers (conjugate gradient, GMRES, Newton-Raphson variants, multigrid methods) converge to solutions through repeated application. You could use GP to search for update rules and evaluate them on convergence rate and stability across problem sizes.

The wrong-limit attractor problem is directly relevant: a solver that converges fast on small test problems (the evaluation window) but diverges on larger ones is the same finite-evaluation trap. The log-precision fitness approach — measuring bits of precision gained per iteration across problem scales — would select for solvers with robust convergence properties rather than solvers that overfit to the test suite.

---

## Conceptual Transfer (the attractor taxonomy and coverage analysis transfer, the search method doesn't)

### Protein folding energy landscapes

The energy landscape problem in protein folding shares the wrong-limit attractor structure. Local energy minima (misfolded states / decoy structures) score well on local energy evaluation but aren't the global minimum (native fold). The density of wrong-limit attractors increases with chain length (analogous to our terminal count). The coverage problem — sampling enough of conformational space to find the native fold — is the same linear-vs-exponential challenge.

What transfers: the taxonomy of attractor types (wrong-limit vs bloat vs miscalibration), the observation that stronger optimization can lock onto wrong attractors faster, and the coverage/search-space scaling analysis. The specific GP search method doesn't transfer because protein folding is continuous optimization over atomic coordinates, not constructive symbolic search.

The "population increase is not monotonically beneficial when strong attractors exist" finding may have a parallel in enhanced sampling methods: more aggressive sampling can trap molecular dynamics in deep local minima faster rather than allowing thermal fluctuations to escape them.

### Neural architecture search (NAS)

NAS searches for neural network architectures that perform well on a validation set (the evaluation window). Architectures that overfit to the validation distribution but fail on shifted distributions are wrong-limit attractors. The coverage problem exists: the space of possible architectures grows combinatorially with the number of available operations and layer types.

However, NAS has continuous local structure (nearby architectures have correlated performance), which our analysis says should make it more amenable to search than constructive symbolic problems. The attractor taxonomy transfers conceptually but the scaling ceiling may be less severe.

### LLM training objective design

The first-order vs second-order fitness distinction has a loose parallel in LLM training. Cross-entropy loss on next-token prediction is a pointwise (first-order) objective: "is the next prediction correct?" Evaluation metrics that measure calibration, coherence over long contexts, or consistency of reasoning across problem scales are process-level (second-order) objectives.

The observation that first-order fitness finds answers that satisfy local criteria but fail globally (wrong-limit attractors) maps to the well-documented problem of LLMs that produce locally fluent but globally incoherent or factually wrong text. The "confabulation analogy" in the main research notes is this connection made explicit.

This is speculative. The optimization landscapes are radically different (continuous high-dimensional parameter spaces vs discrete symbolic trees). But the principle — that the form of the evaluation question determines whether you find locally plausible or globally correct solutions — may generalize.

---

## Speculative (interesting to think about, not ready to claim)

### Automated theorem proving

Theorem proving searches for proof trees from axioms and inference rules. The search space is constructive (like GP) and grows combinatorially with the axiom set (like terminal count). "Wrong-limit attractors" would be proof attempts that appear to be making progress (reducing subgoal count) but are headed toward a dead end.

The coverage analysis might explain why automated provers struggle with certain theorem classes: if the proof requires assembling specific lemma combinations from a large axiom set, the coverage/search-space ratio may be below threshold. The log-precision fitness concept could inform heuristic evaluation functions for proof search.

Highly speculative. The structure of proof search is different enough from GP that the mapping may not hold.

### Drug discovery / molecular optimization

Searching for molecules with specific properties (binding affinity, solubility, toxicity profiles) from a library of molecular fragments is structurally similar to GP over terminal sets. The fragments are the terminals. The properties are the fitness. The evaluation horizon trap maps to: molecules that score well on in-vitro assays (finite evaluation) but fail in vivo (the infinite horizon).

The coverage analysis might inform library design: how many fragments are too many before the search becomes dominated by local optima? The wrong-limit attractor concept maps to PAINS compounds (pan-assay interference compounds) that score well across many assays without genuine therapeutic activity.

### Log-precision fitness for any black-box optimization

The broadest generalization: whenever you're optimizing a black-box function and you can measure the convergence properties of your optimization trajectory (not just the current best value), a log-precision fitness that rewards constant precision gain per evaluation step may outperform a fitness based on raw objective value. This is because the log-precision fitness is second-order (measures the rate of improvement) while raw objective value is zero-order (measures the current state).

This is the least specific claim and the hardest to validate. But it's the deepest implication of the log-precision fitness result: asking "how fast are you learning?" is more discriminating than asking "how good are you right now?"

---

## For the Paper

Keep this tight. In the Discussion section, cover chemical kinetics and dynamical system identification (direct application, 1-2 paragraphs). In Future Work or a brief "Broader Applicability" subsection, mention protein folding and iterative solvers as conceptual transfer (one sentence each). Do not include the speculative items in the paper — they belong in a blog post or follow-up work, not in a preprint that needs to be defensible.

The honest scope statement: "The method applies directly to any symbolic regression problem where the target has infinite-horizon convergence behavior. The attractor taxonomy and coverage analysis apply conceptually to any optimization problem with finite evaluation of infinite-horizon properties."
