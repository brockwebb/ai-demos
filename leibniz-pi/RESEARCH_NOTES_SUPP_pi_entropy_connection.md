# Research Notes — Supplementary: π and Entropy — An Open Question

**Tag:** `RESEARCH_NOTES_SUPP_pi_entropy_connection`
**Date:** 2026-03-16
**Context:** The relationship between π and entropy is mathematically real but its connection to this project's fitness design is speculative. This note documents both the established math and the open question, clearly separated.

---

## Established Mathematical Connections Between π and Entropy

These are real, proven relationships. They are not analogies.

**1. Gaussian maximum entropy.** The Gaussian distribution maximizes Shannon differential entropy for a given variance. Its density function contains √(2π) as a normalization constant. The differential entropy of a Gaussian is H = ½ ln(2πeσ²). π appears because the maximum-entropy distribution for a second-moment constraint has Gaussian form, and the Gaussian integral evaluates to √π.

**2. Stirling's approximation.** n! ≈ √(2πn)(n/e)^n. Boltzmann entropy S = k_B ln(Ω) requires counting microstates, which involves factorials. The √(2π) in Stirling arises from the central limit theorem: as n grows, the discrete binomial approaches the continuous Gaussian.

**3. Phase space volume.** The volume of an n-dimensional hypersphere is V_n(R) = π^(n/2) / Γ(n/2 + 1) × R^n. Thermodynamic entropy is proportional to the log of the accessible phase space volume, so π enters entropy through high-dimensional geometry.

**4. Heisenberg uncertainty.** ΔxΔp ≥ h/(4π). The minimal phase space cell has area h, with π setting the geometric bound. Von Neumann entropy of quantum systems inherits this.

---

## What Our Fitness Function Actually Does

Our fitness computes -log₂(|S(T) - π/4|) at evaluation checkpoints. This is:
- A single-point measurement, not an expectation over a distribution
- A log transformation of error, not Shannon entropy
- Applied to a deterministic series, not a probabilistic system
- Targeted at π/4, a specific value, not at a geometric constant emerging from an integral

The fitness function does not compute entropy. It does not involve Gaussian distributions, phase spaces, or uncertainty principles. It measures how many powers of 2 the error has decreased by.

---

## The Open Question

π appears in the normalization of the maximum entropy distribution. We found the series that converges to π/4 by rewarding constant precision gain on a log scale — a metric with the same mathematical form as self-information.

Is there a structural reason why a log-precision fitness selects for convergence to a value (π/4) that appears in entropy formulas? Or is this a coincidence arising from the fact that π appears everywhere in mathematics?

We do not know. We have not established a formal connection. The following observations are suggestive but not probative:

- The fitness rewards second-order convergence (constant rate on log scale). The Gaussian, which contains π, is also characterized by second-order structure (quadratic exponent, second-moment constraint).
- Leibniz is the simplest series satisfying the log-precision criterion. The Gaussian is the simplest (maximum entropy) distribution satisfying the variance constraint. Both are "simplest under a second-order constraint" in their respective domains.
- The fitness measures -log₂(|error|). Differential entropy of the Gaussian is ½ ln(2πeσ²). Both involve logarithms of quantities that contain π, but for entirely different mathematical reasons.

These parallels may reflect a deep structural connection between second-order constraints and π, or they may reflect the ubiquity of π in analysis. We cannot distinguish these possibilities from our experimental results.

---

## For the Paper

This belongs in a "Further Connections" or "Speculation" subsection at the end of the Discussion, clearly labeled as an open question. One paragraph. Do not develop it into a claim. Do not use it to retroactively justify calling the fitness "entropy" or "information-theoretic."

Suggested framing: "We note without claiming a formal connection that π appears in the maximum entropy distribution for second-moment constraints, and our log-precision fitness — which rewards second-order convergence structure — reliably discovers the series converging to π/4. Whether this reflects a deeper relationship between second-order constraints and π, or simply the ubiquity of π in analysis, remains an open question."
