# Research Notes — Supplementary: Future Work and Improvement Directions

**Tag:** `RESEARCH_NOTES_SUPP_future_work`
**Date:** 2026-03-16
**Context:** Promising directions that emerged from the experiments but are beyond the scope of this paper. These are the "fund me" ideas.

---

## 1. Building Block Initialization (highest priority)

Instead of random tree initialization, do a cheap pre-pass over the terminal set to identify structurally promising subtrees. Evaluate all 2-3 node subtrees, classify which ones produce oscillating behavior, growing denominators, bounded convergence. Initialize the population from recombinations of good subtrees rather than purely random trees.

This is not injecting the answer (the v2 confound). It's injecting vocabulary. The difference: injecting Leibniz says "here's the sentence." Injecting good subtrees says "here are words that might be useful." The GP still has to assemble them.

**Why this matters:** The extended time test proved that failed seeds lacked the right building blocks in their initial population, and no amount of additional search time could create them. Better initialization attacks the actual bottleneck.

**Testable:** Run the existing t=15 experiment but seed the population with all valid 3-node subtrees from the terminal set. Compare discovery rate to pure random init.

## 2. MCTS-Guided Search (AlphaGo-style)

Replace uniform population search with Monte Carlo Tree Search plus a learned value function. Instead of evaluating every individual equally, allocate search budget proportional to estimated promise. Go shallow on most branches, go deep on promising subtree structures.

**The key difference from GP:** GP treats all individuals equally. MCTS would identify the 10 most promising *subtree patterns* (not full expressions), then allocate more crossover/mutation budget to recombining those patterns. This is the "work in smaller groups, go shallow first" approach.

**Why this matters:** Our data showed that the GP locks onto wrong-limit attractors early and can't escape. MCTS's exploration/exploitation balance (UCB1 or similar) would maintain exploration of alternative subtree structures even when one attractor dominates.

**Cost:** Requires training a value function to estimate subtree promise, which is a separate learning problem. Not trivial.

## 3. Island Migration Models

Run multiple independent small populations (islands) in parallel. Periodically migrate the best individuals between islands. Each island explores a different region of the search space with different random initialization.

**Why this matters:** We already run 5 seeds independently and some succeed where others fail. Island migration would let successful seeds share their building blocks with unsuccessful ones mid-run, potentially rescuing seeds that have the right *partial* structures but not the complete assembly.

**The insight from our data:** Seed 7 (val=7) found Leibniz at t=10. The other 4 seeds didn't, even with 4x more time. If seed 7 could have migrated its `(-1)^k` subtree to seed 42's population, seed 42 might have combined it with its own denominator structure. Migration enables cross-pollination of building blocks across independent search trajectories.

**Testable with minimal code changes:** Run 5 seeds in parallel, every 500 generations copy the top 5 individuals from each seed into every other seed's population (replacing worst individuals). Compare to independent runs.

## 4. Automated Terminal Set Pruning

Given a large terminal set (say t=20), automatically identify and remove terminals that don't contribute to promising subtrees. Run a short GP pre-pass (1-2 minutes), analyze which terminals appear in the top 10% of individuals, prune terminals that never appear in high-fitness expressions, then run the full search on the pruned set.

**Why this matters:** This is the algorithmic version of what we did manually when we chose {k, 1, -1, 2}. The project's core finding is that constraining primitives matters more than anything else. Automating that constraint is the practical engineering contribution.

**Connection to ML:** This is analogous to feature selection before model training. Run a cheap pre-pass to identify which features carry signal, prune the noise features, then train on the reduced set.

## 5. Simulated Annealing Integration

Add a proper annealing schedule to the GP: accept worse individuals with some probability that decays over time. The current diversity injection mechanism (replace worst 100 when top 20 converge) is a blunt instrument. Annealing would allow controlled escape from attractor basins.

**Why this matters:** Our wrong-limit attractors trap the population in basins. The diversity injector fires but injects random trees that are immediately outcompeted by the attractor. Annealing would temporarily lower selection pressure, allowing random variation to persist long enough to assemble alternative structures.

## 6. Efficiency Fitness (bits per operation)

Test a fitness that measures precision gain per tree node rather than absolute precision. The most fundamental fitness: minimum work (operations) per unit of precision gained. Leibniz uses 3 operations per term. A bloated 11-node equivalent uses 5 operations for the same precision. Efficiency fitness would naturally prefer the canonical 9-node form.

**Why this matters for the paper:** We found bloated algebraic equivalents (9-11 nodes) but couldn't drive toward canonical form with parsimony alone. Efficiency fitness is a different approach — instead of penalizing size, reward compactness per unit of output quality.

**Already discussed in research notes but not implemented.**

---

## For the Paper

Include 2-3 of these in the Future Work section. Recommended:

1. Building block initialization (most directly addresses the core finding)
2. MCTS-guided search or island migration (addresses the attractor lock-in problem)
3. Automated terminal set pruning (the practical engineering application of the core finding)

Frame as: "The core finding — that search space constraint dominates algorithm choice — suggests that future work should focus on smarter initialization and automated primitive selection rather than on improved fitness functions or larger populations."
