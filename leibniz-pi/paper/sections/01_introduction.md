# 1. Introduction

The Leibniz series

$$\frac{\pi}{4} = \sum_{k=0}^{\infty} \frac{(-1)^k}{2k+1} = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \cdots$$

converges to π/4 but does so slowly: roughly 5 billion terms are required for 10 digits of precision. Far more efficient algorithms exist for computing π. The series is famous not for its efficiency but for its structural elegance, a process that approaches its target monotonically, each term a smaller correction than the last, improving forever without arriving.

This paper asks a constructive question: given only arithmetic primitives and a fitness criterion that rewards sustained convergence, can an evolutionary search discover Leibniz from scratch? The answer is conditionally yes. The conditions under which discovery fails are more instructive than the conditions under which it succeeds.

Symbolic regression typically searches for equations that fit observed data points. The Leibniz problem differs: there are no data points. The fitness must evaluate a *process*, a generating rule applied at every integer k. The question is whether that process exhibits the convergence properties characteristic of a series summing to a mathematical constant. This shifts the optimization objective from pointwise accuracy to process-level behavior: not "how close is the output?" but "is the output still improving, and will it always be?"

We develop two fitness functions for this objective. The first, convergence-aware fitness, rewards expressions whose partial sums decrease in error between evaluation checkpoints. By analogy to reaction kinetics (see Section 6.1), we call this a first-order question: is error shrinking? The second, log-precision fitness, rewards expressions that gain bits of precision about π/4 at a constant rate across orders of magnitude of summation depth. By the same analogy, this asks a second-order question: is precision gain sustained at a constant rate across scales? Both discover Leibniz under favorable conditions. The log-precision fitness is more reliable, succeeding at half the population size.

The central finding is not that Leibniz can be discovered, but that discovery exhibits a sharp phase transition as the search space grows. With 4 terminals, discovery is reliable. With 15, it fails completely. The fitness function does not break; it correctly identifies Leibniz as optimal when Leibniz is present. The failure is that the search space becomes populated with wrong-limit attractors. These are series that converge to values near π/4 within any finite evaluation horizon and score well on the fitness criteria. Wrong-limit attractors are structurally simpler than Leibniz. No improvement to the fitness function can eliminate them, because no finite evaluation can distinguish "converges to π/4" from "converges to a nearby value."

This evaluation horizon trap has implications beyond the Leibniz problem. Any fitness-guided search over infinite-horizon processes faces the same constraint. The difficulty of discovery is not in the fitness landscape, which places Leibniz at or near its global optimum. The difficulty is in coverage: whether the search explores enough of the space for correct building blocks to assemble before wrong-limit attractors dominate the population.
