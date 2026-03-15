# The World's Longest Line to Pi

Happy Pi Day, 2026.

The Leibniz series is often considered one of the most beautiful formulas in mathematics. For calculating π, it is also one of the most impractical.

π/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - …

You need about 5 billion terms to get 10 digits of π (Leibniz formula for π, n.d.). Far better algorithms exist. Leibniz is not famous because it is efficient. It is famous because it is perfect in a way that efficiency cannot measure.

## A Look Under the PI-roscope

Leibniz is a process that only reaches its final value at infinity. A long series of terms are added together, each in an attempt to correct the error the previous one introduced. The first term overshoots π/4. The second drops below. The third overshoots by less. The fourth corrects, also by less. The sum swings around π/4, its amplitude shrinking each step. A wave that settles but never quite stops.

A thermostat is a useful analogy. Set the target to π/4, and the partial sums act like the thermostat's measurement. The value swings above and then below, each swing smaller than the last. It gets closer to equilibrium but never quite reaches it. At every step, the partial sum is not equal to π/4. At every step, it is less wrong than before.

The defining property of Leibniz is not the value it converges to but the structure of how it converges. Alternating signs. Decreasing amplitude. A single rule applied identically at every position: term(k) = (-1)^k / (2k+1). Infinite, regular, harmonious, and never finished.

## The Opti-pization Paradox

Traditional optimization seeks to maximize some efficiency goal under constraints like maximizing package deliveries using the shortest possible route. If we approached this problem as the most efficient route to π/4, we'd end up with the fastest convergence to a close enough approximation and stop.

Those solutions seem numerically superior but are mathematically empty. They converge near π/4, not to π/4 itself, and stop improving. After 10 terms, they outperform Leibniz. By 5,000 terms, precision has not increased by a single digit. They reached the wrong address and parked.

Leibniz is the most harmoniously inefficient path to π. Reproducing it computationally requires a different kind of optimization. You cannot reward proximity to the answer. You have to reward the properties of a process that never ends: sustained convergence, structural regularity, and minimal complexity. The question changes from "how close are you?" to "are you still getting closer, and will you always be?"

## Two Slices of π

We approached Leibniz from two different directions.

**Moldy PI?** 
Slime molds are organisms that can solve optimization problems without a brain or centralized control system. They explore many paths in parallel and reinforce the most efficient ones for obtaining food. The structure that emerges is always the simplest one that works. The same principle applies to searching for mathematical rules. Start with a population of random mathematical expressions built from basic parts: addition, multiplication, division, exponents, constants, and the variable k. A candidate formula might be k / (k + 3). Another might be (-1)^k * k. Neither is useful. But cross them, take the sign-flipping mechanism from one and the denominator structure from the other, and the offspring might score better than either parent. Mutate a constant, swap an operator, and test again. The algorithm does not know about π. It cannot look up the answer. It breeds, mutates, and selects based on a single fitness score.

It turns out that, for this type of optimization problem, two properties matter the most: simplicity and constant improvement. Simplicity, in this case, means the fewest operations needed to define the rule. The Leibniz formula uses just three to create a highly compact formula for generating an infinite series: raise -1 to the power k, the 2k+1 denominator, and divide. Constant improvement means that the solution at each step is closer to the final answer than the one before. Not just the first few steps, but at 50 terms, 200 terms, 5,000 terms, forever.

It's interesting that neither property explicitly mentions alternating signs or odd denominators. Those emerge on their own because oscillating correction turns out to be the simplest mechanism that converges to π/4 forever. Under these two constraints, Leibniz is what you get. (-1)^k / (2k+1). The simplest rule that never stops converging.

**Information Super-piway.** 
The second approach uses the same evolutionary search but replaces the fitness function entirely. Instead of rewarding simplicity and sustained convergence, it rewards information gain. If we define the precision at step T as the bits of information the partial sum has captured about π/4:

info(T) = -log₂(|error at T|)

When you start plugging away the numbers on this log scale, every power of 10 turns out to be a difference of 3.32 bits. In other words, this is not an empirical observation, but a direct computation of the rate of change that remains constant. Essentially, Leibniz is a straight line on a log scale that gains information at a constant rate with no upper bound.

## Not to be PI-dantic

Both approaches found Leibniz. Five out of five random seeds, each time producing the exact expression (-1)^k / (2k+1). The convergence-aware search and the information-theoretic search arrived at the same formula independently. Neither objective mentioned π.

| | T=10 | T=50 | T=200 | T=1,000 | T=5,000 |
|---|---|---|---|---|---|
| Leibniz | 0.02494 | 0.00500 | 0.00125 | 0.00025 | 0.00005 |
| GP v2 (convergence) | 0.02494 | 0.00500 | 0.00125 | 0.00025 | 0.00005 |
| Entropy GP | 0.02494 | 0.00500 | 0.00125 | 0.00025 | 0.00005 |

Every cell matches. Not approximately. Exactly.

That is the result, but it is not the insight. The insight is that "find a series that sums to π/4" does not produce Leibniz. It produces shortcuts that get close and stop improving. Defining success as proximity to a target gets you solutions that arrive and park.

"Find the simplest rule that never stops converging" produces Leibniz. The formula was not hard to find. Knowing what to ask for was the hard part.

That generalizes. Define success as hitting a target, and you get solutions that stop learning once they arrive. Define success as the properties a good answer should have at every scale, and you get solutions that keep improving. The discipline is not in finding answers. It is in asking better questions.

Leibniz's formula never reaches π/4. It approaches forever, each term a smaller correction, the wave always collapsing, yet never collapsed. The knowledge it holds at any step is finite. The boundary of what remains is not.

Happy Pi Day.

The code and full analysis are on [GitHub](https://github.com/brockwebb/ai-demos/tree/main/leibniz-pi).

## References

Leibniz formula for π. (n.d.). Wikipedia. https://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80
