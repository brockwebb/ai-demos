# Fact-Check Query List for Leibniz-π Paper

**Date:** 2026-03-24
**Purpose:** Run these queries in Perplexity to verify external claims, find supporting evidence, and identify potential new citations.
**Instructions:** Copy each query into Perplexity. Note whether results confirm, contradict, or extend the claim. Flag any new citations worth adding to references.bib.

---

## Section 1: Introduction

### Q1.1 — Leibniz convergence rate claim
> "roughly 5 billion terms are required for 10 digits of precision"

**Query:** `How many terms of the Leibniz series for pi/4 are needed for 10 digits of precision?`

**Why:** This is stated as common knowledge but should be verified. The 1/T error decay means ~10^10 terms for 10 decimal digits, which is closer to 10 billion than 5 billion. Need to check if this is off by a factor of 2.

---

### Q1.2 — Confabulation parallel claim
> "The failure mode parallels confabulation in language models: outputs that appear correct within a finite evaluation horizon but do not correspond to the true target"

**Query:** `NIST AI 600-1 definition of confabulation vs hallucination in AI systems`

**Why:** Paper uses "confabulation" per NIST AI 600-1 convention. Verify the definition aligns with how we use the term. Also check if any recent papers (2024-2026) have used "confabulation" in the context of optimization or search processes, not just LLMs.

**Follow-up query:** `Has anyone drawn parallels between wrong-limit attractors in optimization and confabulation or hallucination in language models?`

---

## Section 2: Background and Related Work

### Q2.1 — Schmidt and Lipson (2009) claim
> "Schmidt and Lipson (2009) showed that GP-based symbolic regression could recover Hamiltonians and Lagrangians from experimental data"

**Query:** `Schmidt Lipson 2009 Science distilling natural laws symbolic regression what did they actually discover`

**Why:** Verify the characterization is accurate. Did they recover Hamiltonians specifically, or conservation laws? The distinction matters.

---

### Q2.2 — Hillar and Sommer (2012) critique
> "Hillar and Sommer (2012) subsequently demonstrated that the operator set and fitness structure implicitly encoded physical priors"

**Query:** `Hillar Sommer 2012 critique Schmidt Lipson symbolic regression implicit priors what specifically did they show`

**Why:** Verify this characterization. The paper draws a parallel to our injection confound; need to confirm the Hillar/Sommer critique is about implicit encoding, not something else.

---

### Q2.3 — Modern symbolic regression landscape (2023-2026)
> "Modern symbolic regression spans evolutionary (Cranmer, 2023), transformer-based (Valipour et al., 2021), neural-symbolic (Li et al., 2023), generative flow (Li et al., 2023), tree-search (Kamienny et al., 2023; Shojaee et al., 2023), and equality saturation approaches (Jiang et al., 2025)."

**Query:** `State of symbolic regression 2024 2025 survey major approaches transformer neural GP`

**Why:** Verify we're not missing a major category. Also check if any of these newer approaches address process-level or convergence-based fitness (our claimed gap).

**Follow-up query:** `Kamienny 2023 tree search symbolic regression paper title and main contribution`

**Follow-up query:** `Shojaee 2023 symbolic regression paper title and main contribution`

**Follow-up query:** `Li 2023 neural symbolic regression generative flow paper`

**Follow-up query:** `Jiang 2025 equality saturation symbolic regression paper`

**Why (follow-ups):** These citations were added in a previous lit review pass. Verify each exists and the characterization (tree-search, generative flow, equality saturation) is correct. Confabulated citations are embarrassing.

---

### Q2.4 — No prior work on process-level fitness claim
> "All of these systems optimize pointwise fitness... None address the problem class we consider, evaluating convergence properties of an infinite-horizon generating process against a known limit."

**Query:** `Symbolic regression fitness function for convergent series or asymptotic behavior evaluation rather than pointwise accuracy`

**Why:** This is our novelty claim. If someone has done this, we need to cite them and reframe. Also search for adjacent work in time-series symbolic regression.

**Follow-up query:** `Fitness function design evaluating convergence rate or asymptotic scaling in genetic programming`

---

### Q2.5 — Bloat vs wrong-limit attractors distinction
> "wrong-limit attractors... are structurally simpler than the correct answer and converge to a finite limit. They score well because their limit happens to fall near π/4"

**Query:** `Genetic programming failure modes beyond bloat: simpler expressions that converge to wrong targets in symbolic regression`

**Why:** Verify that wrong-limit attractors are genuinely a new contribution vs. something already described under a different name (e.g., deceptive attractors, local optima, convergent overfitting).

**Follow-up query:** `Deceptive fitness landscapes genetic programming local optima symbolic regression`

---

### Q2.6 — Evaluation horizon trap novelty
> "To our knowledge, no prior work analyzes this failure mode as distinct from bloat or overfitting in symbolic regression."

**Query:** `Evaluation horizon limitations in symbolic regression or genetic programming finite evaluation of infinite processes`

**Why:** Strong novelty claim. Need to verify nobody has formalized this concept.

---

## Section 3: Methods

### Q3.1 — GP parameter choices
> "tournament selection (k=7), subtree crossover (P=0.70), subtree mutation (P=0.20), reproduction (P=0.10), and elitism (top 5 preserved)"

**Query:** `Standard genetic programming parameters tournament size crossover mutation rates Koza Poli field guide`

**Why:** Verify these are within the standard range for GP. The paper doesn't justify them individually; they should be consistent with established practice.

---

### Q3.2 — Log-precision fitness and Shannon self-information
> "The quantity -log₂(|error|) has the same mathematical form as Shannon's self-information, though it is not entropy in the information-theoretic sense"

**Query:** `Shannon self-information formula -log2 probability relationship to precision measurement`

**Why:** Verify the mathematical correspondence is correctly stated. Self-information is -log₂(p) for probability p; our quantity is -log₂(|error|). The structural similarity is real but we need to be precise about what's analogous and what's not.

---

### Q3.3 — Second-order rate law and 1/T convergence
> "Leibniz gains log₂(10) ≈ 3.32 bits per decade. On a log-log plot, this is a straight line. The constant rate is the signature of second-order kinetics."

**Query:** `Second order reaction kinetics integrated rate law 1/concentration vs time linear relationship`

**Why:** Verify the kinetics analogy is correctly stated. In chemical kinetics, second-order integrated rate law gives 1/[A] = kt + 1/[A]₀, which is linear in t. Our claim is that 1/error vs T is linear for Leibniz. Confirm the mathematical correspondence.

**Follow-up query:** `Convergence rate of Leibniz series for pi error bound 1/(2T+1) derivation`

**Why:** Verify the error bound 1/(2T+1) for the Leibniz series. This is the foundation for the second-order kinetics analogy.

---

## Section 4: Experimental Design

### Q4.1 — Hillar/Sommer parallel to injection confound
> "Hillar and Sommer (2012) showed that Schmidt and Lipson (2009) implicitly encoded the answer in the search structure"

**Query:** `Did Hillar and Sommer argue Schmidt Lipson results were due to implicit encoding of physical laws in the operator set`

**Why:** Already queried in Q2.2, but here we're making a stronger parallel claim. Verify the characterization supports the parallel we draw.

---

### Q4.2 — Safe division convention
> "Division by zero returns 1.0 (safe division)"

**Query:** `Protected division in genetic programming what value is returned common conventions`

**Why:** The standard GP convention is to return 1.0 for protected division (some use 0, some use the numerator). Verify our choice is standard or at least defensible.

---

## Section 5: Results

### Q5.1 — Phase transition in GP search spaces
> "The 7×4 scaling grid reveals a phase transition between t=8 and t=10"

**Query:** `Phase transitions in genetic programming search space complexity symbolic regression scaling`

**Why:** The "phase transition" framing borrows from statistical physics. Verify whether others have documented similar sharp transitions in GP discovery rates as search space grows.

---

## Section 6: Discussion

### Q6.1 — Second-order kinetics connection (detailed)
> "In chemical kinetics, this is the signature of a second-order reaction: the rate depends on the product of two concentrations, or the square of one."

**Query:** `Second order kinetics definition rate law depends on product of two concentrations or square of one`

**Why:** Verify the statement is technically correct for a general audience. Second-order can mean bimolecular (two species) or second-order in one species. Both give 1/[A] linearity.

---

### Q6.2 — Coverage/search-space proportionality
> "P(discovery) scales with fitness quality times coverage, divided by search space size"

**Query:** `Building block hypothesis genetic programming schema theorem coverage population size search space`

**Why:** This is related to Goldberg's schema theorem and the building block hypothesis. Verify whether our coverage framing is consistent with or extends existing theory.

**Follow-up query:** `Population sizing in genetic programming theory minimum viable population for building blocks`

---

### Q6.3 — Confabulation analogy in broader literature
> "The remedy in both cases is not better loss functions but better questions"

**Query:** `Confabulation hallucination in AI optimization beyond language models fitness evaluation horizon`

**Why:** Check if anyone else has extended the confabulation concept beyond LLMs to optimization or search. This would either strengthen our contribution or require citation.

---

### Q6.4 — Feature selection as search space constraint
> "Feature selection matters more than model architecture"

**Query:** `Feature selection versus model architecture importance in machine learning empirical evidence`

**Why:** This is stated as a general ML principle in the conclusion. Verify it has empirical backing or is a recognized principle, not just our assertion.

---

### Q6.5 — Wrong-limit attractors as distinct from overfitting
> "They are not overfitting: they genuinely converge."

**Query:** `Difference between overfitting and convergent wrong solutions in optimization local optima vs deceptive attractors`

**Why:** Strengthen the distinction between our failure mode and standard overfitting. Find supporting literature that distinguishes between these failure classes.

---

### Q6.6 — Equality saturation in symbolic regression
> "equality saturation approaches (Jiang et al., 2025)"

**Query:** `Equality saturation symbolic regression 2024 2025 e-graphs program synthesis`

**Why:** Verify this is a real, published approach and that "equality saturation" is the correct term. E-graph-based program synthesis exists but may not have been applied to symbolic regression specifically.

---

## Section 7: Conclusion

### Q7.1 — Building block initialization as future work
> "building block initialization that seeds structural vocabulary rather than complete answers"

**Query:** `Seeding genetic programming with building blocks partial solutions initialization strategies`

**Why:** Check if this has been done already. If so, cite it; if not, it's genuinely future work.

---

### Q7.2 — Automated terminal pruning
> "automated terminal pruning that discards irrelevant primitives before the full search"

**Query:** `Automated feature selection terminal reduction genetic programming symbolic regression before search`

**Why:** Same as above. Check existing work on pre-search terminal/feature pruning in GP.

---

### Q7.3 — Island migration for building block sharing
> "island migration that lets successful subpopulations share building blocks"

**Query:** `Island model genetic programming migration building block transfer subpopulation diversity`

**Why:** Island models are well-established in GP. Verify there's existing literature and cite appropriately. This isn't novel as a concept, so framing as "future work" is fine but we should acknowledge it exists.

---

## Cross-Cutting Queries

### QX.1 — Has anyone used GP to discover known mathematical series?
**Query:** `Genetic programming rediscovery of known mathematical series formulas pi Euler Riemann`

**Why:** Check if anyone has done a similar experiment to ours (using GP to rediscover a known infinite series). If so, we need to cite and differentiate.

---

### QX.2 — Process-level evaluation in any ML context
**Query:** `Evaluating machine learning models on process behavior rather than output accuracy trajectory evaluation`

**Why:** Broader search for the concept of process-level evaluation. Our claim that this is under-explored could be wrong.

---

### QX.3 — Convergent series discovery by any ML method
**Query:** `Machine learning discovery of convergent infinite series neural network genetic algorithm`

**Why:** Widest net. Has any ML method been applied to discovering or rediscovering convergent series?

---

### QX.4 — Parsimony pressure threshold effects
**Query:** `Parsimony pressure threshold genetic programming lambda penalty collapse trivial solutions`

**Why:** Our Section 5.4 shows a sharp threshold. Verify if this sharp-threshold behavior for parsimony is known in the GP literature.

---

### QX.5 — NIST AI 600-1 confabulation definition (verification)
**Query:** `NIST AI 600-1 2024 artificial intelligence risk management confabulation definition text`

**Why:** We cite NIST AI 600-1 for the confabulation/hallucination terminology distinction. Verify the document exists and contains this definition.

---

## Summary: Priority Tiers

### Tier 1 — Must verify (novelty claims at stake)
- Q2.4: No prior work on process-level fitness
- Q2.5: Wrong-limit attractors as new concept
- Q2.6: Evaluation horizon trap novelty
- QX.1: Has anyone used GP for known series?
- QX.3: Any ML method for convergent series?

### Tier 2 — Should verify (accuracy of cited claims)
- Q1.1: 5 billion terms for 10 digits
- Q2.1: Schmidt & Lipson characterization
- Q2.2: Hillar & Sommer characterization
- Q2.3: All follow-up citation verifications (Kamienny, Shojaee, Li, Jiang)
- Q3.2: Shannon self-information analogy
- Q3.3: Second-order rate law correspondence
- QX.5: NIST AI 600-1 exists

### Tier 3 — Nice to have (strengthen or add citations)
- Q1.2: Confabulation in optimization context
- Q3.1: GP parameter standards
- Q4.2: Safe division convention
- Q5.1: Phase transitions in GP
- Q6.2: Building block hypothesis
- Q6.4: Feature selection vs architecture
- Q7.1-Q7.3: Future work prior art
- QX.2: Process-level evaluation in ML
- QX.4: Parsimony threshold effects
