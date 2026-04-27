# Prose QC Report


## 01_introduction.md
### Tier 2 (1)
- **[PQ-02]** line 11: Paragraph has 1 sentence(s) (min 2)
  > `We study this through a clean, controlled case: can genetic programming rediscover the Leibniz serie`
### Heuristic (5)
- **[PQ-06]** line 3: Possible passive voice
  > `Every AI system is evaluated within a finite horizon.`
- **[PQ-07]** line 3: Possible ambiguous pronoun
  > `This is not a defect in any particular architecture.`
- **[PQ-07]** line 3: Possible ambiguous pronoun
  > `It is a structural property of how we build and test all of them.`
- **[PQ-06]** line 9: Possible passive voice
  > `They are not evaluation function errors: the evaluation correctly ranks the right answer above them `
- **[PQ-06]** line 9: Possible passive voice
  > `Wrong-limit attractors arise because the gap between finite observation and infinite-horizon behavio`

## 02_background.md
### Heuristic (13)
- **[PQ-06]** line 7: Possible passive voice
  > `Their result was widely interpreted as evidence that symbolic regression extracts natural laws witho`
- **[PQ-06]** line 7: Possible passive voice
  > `The "laws" were not discovered from scratch; the fitness measure already contained classical mechani`
- **[PQ-06]** line 7: Possible passive voice
  > `Seeding the initial population with the target formula created the illusion of discovery; the formul`
- **[PQ-06]** line 14: Possible passive voice
  > `The standard symbolic regression fitness is root-mean-square error between predicted and observed ou`
- **[PQ-06]** line 16: Possible passive voice
  > `Is the rate of improvement sustained?`
- **[PQ-06]** line 18: Possible passive voice
  > `The closest analog is time-series forecasting, where models are evaluated on multi-step-ahead predic`
- **[PQ-06]** line 20: Possible passive voice
  > `Their fitness is still pointwise: SR expressions are evaluated against sampled data, not against con`
- **[PQ-06]** line 26: Possible passive voice
  > `The fitness function correctly ranks Leibniz above any wrong-limit attractor when both are present.`
- **[PQ-06]** line 28: Possible passive voice
  > `The concept is related to deceptive attractors in genetic algorithms [@Goldberg1989GA; @Deb1993Decep`
- **[PQ-06]** line 28: Possible passive voice
  > `Deceptive attractors are defined by misleading fitness gradients in genotype space.`
- **[PQ-06]** line 28: Possible passive voice
  > `Wrong-limit attractors are defined by indistinguishable behavior within a finite evaluation horizon.`
- **[PQ-06]** line 30: Possible passive voice
  > `A related question is how large a GP population must be for selection to reliably propagate correct `
- **[PQ-06]** line 30: Possible passive voice
  > `Population-sizing theory for GP [@Sastry2005PopulationSizing] shows that the required population gro`

## 03_methods.md
### Heuristic (5)
- **[PQ-06]** line 5: Possible passive voice
  > `Candidate series are represented as expression trees over a set of operators and terminals.`
- **[PQ-06]** line 47: Possible passive voice
  > `The denser checkpoint set (compared to the five checkpoints used by the convergence-aware fitness) p`
- **[PQ-06]** line 57: Possible passive voice
  > `The 0.5 bit gain threshold is calibrated to Leibniz's natural gain rate (see Section 5.6).`
- **[PQ-06]** line 59: Possible passive voice
  > `By the same kinetics analogy, this asks a "second-order" question: *is precision gain sustained at a`
- **[PQ-06]** line 63: Possible passive voice
  > `Their precision gain rate is not constant across scales: it accelerates as the series approaches its`

## 04_experimental_design.md
### Heuristic (10)
- **[PQ-06]** line 5: Possible passive voice
  > `Both fitness functions reported {{result:v2_confounded_5_5:value}}/5 discovery, but subsequent analy`
- **[PQ-06]** line 5: Possible passive voice
  > `The injected tree survived through elitism, never being lost to selection pressure.`
- **[PQ-06]** line 5: Possible passive voice
  > `The tree was *retained*, not *discovered*.`
- **[PQ-06]** line 9: Possible passive voice
  > `Our injection confound is the same class of error: when the target is present in the initial populat`
- **[PQ-06]** line 13: Possible passive voice
  > `Each configuration is evaluated across five seeds (42, 7, 137, 2718, 31415).`
- **[PQ-06]** line 15: Possible passive voice
  > `Time budgets are pragmatic compute constraints, not theoretically motivated.`
- **[PQ-06]** line 33: Possible passive voice
  > `Safe division returns 1.0 when the denominator is at or below 10^-10. Power overflow returns 1.0 whe`
- **[PQ-06]** line 35: Possible passive voice
  > `At each size N, terminal sets are constructed deterministically.`
- **[PQ-06]** line 53: Possible passive voice
  > `All runs use log-precision fitness; time budgets are specified in Section 4.2.`
- **[PQ-06]** line 55: Possible passive voice
  > `Second, where is the boundary beyond which no tested population size achieves reliable discovery?`

## 05_results.md
### Heuristic (9)
- **[PQ-06]** line 15: Possible passive voice
  > `All discovered expressions are algebraically equivalent to (-1)^k / (2k+1), verified identical at k=`
- **[PQ-06]** line 27: Possible passive voice
  > `The canonical 9-node form (-1)^k / (2k+1) is not always found: bloated algebraic equivalents appear `
- **[PQ-06]** line 33: Possible passive voice
  > `The wrong-limit attractor failure mode was seed-specific at this configuration, not universal.`
- **[PQ-06]** line 74: Possible passive voice
  > `At 9 nodes and λ_p=0.005, the parsimony penalty is λ_p × 9 < {{result:logprec_max_fitness_leibniz:va`
- **[PQ-06]** line 100: Possible passive voice
  > `The fitness correctly ranks Leibniz as optimal when Leibniz-equivalent subtrees are present in the p`
- **[PQ-06]** line 117: Possible passive voice
  > `At MIN_GAIN=0.5, the threshold is comfortably below this rate, and all seeds succeed.`
- **[PQ-06]** line 119: Possible passive voice
  > `The convergence-aware fitness threshold (5% error reduction between checkpoints) is less sensitive.`
- **[PQ-06]** line 121: Possible passive voice
  > `It is constrained by the problem, not freely tunable.`
- **[PQ-07]** line 121: Possible ambiguous pronoun
  > `It is constrained by the problem, not freely tunable.`

## 06_discussion.md
### Heuristic (3)
- **[PQ-06]** line 13: Possible passive voice
  > `The constant rate is the integrated form of the second-order rate law.`
- **[PQ-06]** line 13: Possible passive voice
  > `The convergence-aware fitness asks a first-order question: "is error shrinking between checkpoints?"`
- **[PQ-06]** line 17: Possible passive voice
  > `The unifying result across all experiments can be stated as a proportionality: P(discovery) scales w`

## 07_conclusion.md
### Heuristic (2)
- **[PQ-07]** line 7: Possible ambiguous pronoun
  > `This is not specific to genetic programming.`
- **[PQ-06]** line 7: Possible passive voice
  > `Our scaling grid is a controlled demonstration: same algorithm, same fitness, same target, success o`

---

**SUMMARY:** Tier 2=1  Heuristic=47  Tier3=0
