# The Wave That Never Collapses

Happy Pi Day.

The Leibniz series is one of the most beautiful formulas in mathematics and one of the most impractical.

π/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...

You need about 5 billion terms to get 10 digits of π. Vastly better algorithms exist. Leibniz is not famous because it is efficient. It is famous because it is perfect in a way efficiency cannot measure.

## A Wave, Not a Number

Leibniz is not a value. It is a process. Each term is a correction. The first term overshoots π/4. The second corrects back below it. The third overshoots again, less. The fourth corrects, less still. A wave, damping toward a limit it never reaches.

Think of a thermostat. Set point: π/4. The system swings high, swings low, swings high, swings low. Each swing smaller than the last. The oscillation damps. The system approaches equilibrium but never arrives. At every step, the partial sum is wrong. At every step, it is less wrong than the step before.

This is the defining property. Not the value it converges to. The structure of how it converges. Alternating signs. Decreasing amplitude. A single rule applied identically at every position: term(k) = (-1)^k / (2k+1). Infinite, regular, harmonious, and never finished.

## The Optimization Paradox

Traditional optimization cannot see Leibniz. By definition, optimization seeks the shortest path. Given a target value and a set of arithmetic building blocks, any optimizer will find the fastest route to 0.7854 and take it. Compact expressions exist that reach the right neighborhood in fewer steps with less error at any finite checkpoint.

Those solutions are numerically superior and mathematically empty. They converge to a value near π/4, not to π/4 itself. They hit the number and stop improving. At 10 terms, they look better. At 5,000 terms, they have not gained a single additional digit of precision. They arrived at the wrong address and parked.

Leibniz never parks. It keeps driving. At 10 terms, it is less accurate than the shortcuts. At 5,000 terms, it has passed them all, and it is still accelerating. The most harmoniously inefficient path to π is also, in the limit, the only one that gets there.

To reproduce Leibniz computationally, you cannot optimize for proximity to the answer. You have to optimize for the properties of a process that never ends: sustained convergence, structural regularity, minimal complexity. You have to reframe what "good" means. Not "how close are you?" but "are you still getting closer, and will you always be?"

## Two Lenses

Two different framings, drawn from unrelated fields, both capture this.

*Convergence as shortest path.* Slime molds solve optimization problems without a brain. They explore in parallel and reinforce whatever path connects food sources most efficiently. The structure that emerges is always the simplest one that works.

Applied to Leibniz: search over symbolic rules, not sequences of terms. Small expression trees, not lists of fractions. Reward two things. First, true convergence: the error must keep decreasing at T=10, 50, 200, 1,000, 5,000. If it flatlines anywhere, the rule has converged to a wrong limit. Second, parsimony: every node in the expression tree costs fitness. The simplest rule that truly converges wins.

Under these two pressures, Leibniz emerges. (-1)^k / (2k+1). The simplest rule that never stops converging. The shortest path that stays alive.

*Convergence as information gain.* Define precision at step T as bits of information captured about π/4:

info(T) = -log₂(|error at T|)

Leibniz at T=10: about 5 bits. At T=1,000: about 12 bits. At T=5,000: about 14 bits. The rate: 3.32 bits per tenfold increase in terms. Where does that number come from? The Leibniz error at T terms is bounded by 1/(2T+1). So info = log₂(2T+1). On a log-T axis, the slope is log₂(10) = 3.32. The rate is not an empirical observation. It is a mathematical consequence of the convergence order.

The rate is constant. There is no ceiling. Every decade of additional terms buys exactly 3.32 more bits of precision, forever.

Shortcut solutions spike early and collapse. Wrong-limit solutions flatline. Leibniz is a straight line on a log scale, gaining information at a constant rate, with no upper bound. The signature of a process that is always learning and never done.

Reward sustained information gain, penalize complexity, and Leibniz emerges again. Same answer. Different lens.

## The Point

Neither lens required any knowledge of Leibniz's structure. No hint about alternating signs or odd denominators. The formula emerged because it is the simplest rule whose convergence properties satisfy three constraints: infinite improvement, constant information gain rate, and minimal description length.

The work was not in the algorithm. The work was in defining what we were looking for. "Find a series that sums to π/4" produces shortcuts. "Find the simplest rule that generates infinite, structured, damped oscillation toward π/4" produces Leibniz. The first specifies an answer. The second specifies a process. Leibniz lives in the process, not the answer.

This generalizes. Any time you define success as proximity to a target, you get solutions that hit the target and stop learning. The discipline is in asking what properties a good answer has beyond being correct. What should still be true at twice the scale? Ten times? Infinity?

Leibniz's formula never reaches π/4. It approaches forever, each term a smaller correction, the wave always collapsing, never collapsed. Finite volume of knowledge. Infinite surface area of what remains unknown.

Happy Pi Day. The code and full analysis are on [GitHub](link).
