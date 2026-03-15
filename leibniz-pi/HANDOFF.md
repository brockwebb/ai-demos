# Thread Handoff: Medium Article "The World's Longest Line to Pi"

## Status
Draft is nearly final. In editing pass. Article is on the user's filesystem at:
`/Users/brock/Documents/GitHub/ai-demos/leibniz-pi/medium_draft_final.md`

## What This Article Is
A Medium piece (~900 words) about the Leibniz series for π/4. Not a tutorial. Not a lab report. An exploration of what makes Leibniz special: it's the most harmoniously inefficient path to π, and reproducing it computationally requires rewarding simplicity and constant improvement rather than accuracy.

## What Was Done (don't rehash in the article)
Six experiments across four repos explored whether optimization could rediscover Leibniz:
- RL v1, v2 (failed: degenerate term sequences)
- ACO (failed: 440x better numerically, collapses at T>40)
- GP v1 (failed: converges to wrong limit)
- GP v2 (SUCCESS: 5/5 seeds found Leibniz via convergence-aware fitness)
- Entropy GP (SUCCESS: 5/5 seeds found Leibniz via information-theoretic fitness)

The article does NOT walk through these experiments. It presents the insights only.

## Current Section Structure
1. **Title:** "The World's Longest Line to Pi"
2. **A Look Under the PI-roscope** — Leibniz as a damped wave/thermostat, the rule term(k) = (-1)^k / (2k+1)
3. **The Opti-pization Paradox** — Why traditional optimization misses Leibniz
4. **Two Slices of π** — Two approaches:
   - **Moldy PI?** — Slime mold principle: simplicity + constant improvement → Leibniz emerges, oscillation as emergent property
   - **Information Super-piway** — Information theory: 3.32 bits per decade, constant rate, derived from error bound 1/(2T+1)
5. **Not to be PI-dantic** (The Point) — NEEDS REWRITE. See below.

## What Needs Doing
The closing section "Not to be PI-dantic" (previously "The Point") needs a rewrite. Current version:
- Incorrectly lists three properties when the article established two (simplicity and constant improvement)
- Has redundant restatements
- Needs to land on: the two properties, the problem-definition insight, and the poetic closer

The two properties established in the article are:
1. **Simplicity** — fewest operations to define the rule (Leibniz uses three)
2. **Constant improvement** — error shrinks at every scale, forever

The closer that works (keep this): "Leibniz's formula never reaches π/4. It approaches forever, each term a smaller correction, the wave always collapsing, yet never collapsed. The knowledge it holds at any step is finite. The boundary of what remains is not."

## Writing Conventions
- Zero em dashes
- No throat-clearing ("It is worth noting...")
- No self-congratulation ("remarkably," "notably")
- No bold in prose except sub-section headers
- Prefer periods over semicolons for independent clauses
- One idea per paragraph
- Sentences under 35 words
- Active voice preferred
- "Confabulation" not "hallucination" (if it comes up)
- This is a blog, not academic writing. 9-10th grade reading level.
- Puns in section headers are intentional and match the article's tone

## Repos
- Main article + successful experiments: `/Users/brock/Documents/GitHub/ai-demos/leibniz-pi/`
- Coprime Pi (separate newsletter piece, already published): `/Users/brock/Documents/GitHub/ai-demos/coprime-pi/`
- EDA (failed experiments, not in article): `/Users/brock/Documents/GitHub/ai-demos/leibniz-pi/EDA/`

## GitHub
https://github.com/brockwebb/ai-demos/tree/main/leibniz-pi
