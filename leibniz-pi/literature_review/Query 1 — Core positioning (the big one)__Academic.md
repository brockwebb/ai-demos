<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Query 1 — Core positioning (the big one):

Academic literature on genetic programming or symbolic regression used to discover mathematical series or convergent infinite series from primitives. Specifically: (1) fitness functions designed for evaluating convergence properties of infinite-horizon processes rather than pointwise data fitting, (2) "wrong-limit" or "deceptive" attractors in symbolic regression where structurally simpler expressions converge to incorrect limits but score well on finite evaluation, (3) phase transitions in GP discovery rate as search space (terminal set) size increases. Key papers: Schmidt \& Lipson 2009 Science "Distilling free-form natural laws", Hillar \& Sommer 2012 critique, Cranmer 2023 PySR, Brunton et al 2016 SINDy. Looking for BibTeX entries and any work addressing process-level fitness design for series convergence rather than static equation fitting.

Schmidt \& Lipson, Hillar \& Sommer, PySR, and SINDy all focus on finite-horizon data-fitting, and I could not find work that directly designs GP/symbolic-regression fitness around series convergence of infinite-horizon processes; however, there are nearby ideas (stability, long-horizon trajectory error, deceptive fitness, and search-space phase-transition phenomena) that you can likely adapt.[^1][^2][^3][^4][^5][^6]

Below I’ll (1) give BibTeX for the four key papers you named, (2) point to literature most relevant to your three sub‑questions, and (3) flag some concrete techniques for implementing convergence‑aware fitness and avoiding “wrong-limit” attractors.

***

## BibTeX for key papers

```bibtex
@article{Schmidt2009Distilling,
  title   = {Distilling free-form natural laws from experimental data},
  author  = {Schmidt, Michael and Lipson, Hod},
  journal = {Science},
  volume  = {324},
  number  = {5923},
  pages   = {81--85},
  year    = {2009},
  doi     = {10.1126/science.1165893}
}
```

```bibtex
@article{Hillar2012Comment,
  title   = {Comment on the article ``Distilling free-form natural laws from experimental data''},
  author  = {Hillar, Christopher and Sommer, Friedrich},
  journal = {arXiv preprint arXiv:1210.7273},
  year    = {2012},
  url     = {https://arxiv.org/abs/1210.7273}
}
```

```bibtex
@article{Brunton2016SINDy,
  title   = {Discovering governing equations from data by sparse identification of nonlinear dynamical systems},
  author  = {Brunton, Steven L and Proctor, Joshua L and Kutz, J Nathan},
  journal = {Proceedings of the National Academy of Sciences},
  volume  = {113},
  number  = {15},
  pages   = {3932--3937},
  year    = {2016},
  doi     = {10.1073/pnas.1517384113}
}
```

```bibtex
@article{Cranmer2023PySR,
  title   = {Interpretable machine learning for science with PySR and SymbolicRegression.jl},
  author  = {Cranmer, Miles},
  journal = {arXiv preprint arXiv:2305.01582},
  year    = {2023},
  url     = {https://arxiv.org/abs/2305.01582}
}
```

For broader scientific‐discovery context that frequently references Schmidt–Lipson and SINDy:

```bibtex
@article{Rudy2017DataDriven,
  title   = {Data-driven discovery of partial differential equations},
  author  = {Rudy, Samuel H and Brunton, Steven L and Proctor, Joshua L and Kutz, J Nathan},
  journal = {Science Advances},
  volume  = {3},
  number  = {4},
  pages   = {e1602614},
  year    = {2017},
  doi     = {10.1126/sciadv.1602614}
}
```

```bibtex
@article{deSilva2020Discovery,
  title   = {Discovery of physics from data: Universal laws and discrepancies},
  author  = {de Silva, Brian M and Brunton, Steven L and Clark, Jr, Richard W and others},
  journal = {Frontiers in Artificial Intelligence},
  volume  = {3},
  pages   = {25},
  year    = {2020},
  doi     = {10.3389/frai.2020.00025}
}
```


***

## (1) Fitness for infinite-horizon convergence

I did not find symbolic-regression papers that explicitly define fitness in terms of convergence properties of an infinite series or infinite-horizon limit, as opposed to finite sampling error.  Dominant practice:[^3][^5][^7]

- Schmidt \& Lipson: fitness based on how well an expression conserves quantities or predicts trajectories on a finite dataset; no explicit series‑convergence criteria.[^2][^5]
- SINDy: regression of time-derivative data against a sparse library, with error measured over a finite time window (sometimes including multi-step prediction); again no explicit asymptotic or infinite‑horizon term.[^8][^5][^7]
- PySR: flexible loss, usually standard regression losses on finite datasets, possibly plus complexity penalties; convergence is not modeled as such.[^3]

Closest relevant strands you can borrow from:

- Long-horizon trajectory loss: some SINDy follow‑ups evaluate models by rolling out trajectories and comparing attractor statistics rather than one-step error, which implicitly rewards correct long‑term behavior over “good local fits.”[^9][^5][^7]
- Stability or Lyapunov-based constraints: work on physics‑guided system ID and PDE discovery sometimes adds constraints or regularization to enforce physically stable dynamics, which is conceptually similar to preferring convergent series over divergent but locally accurate ones.[^10][^11][^7]

A convergence-aware fitness for symbolic regression over series could be:

- Evaluate partial sums $S_N(x)$ of the candidate series and penalize dependence on $N$ beyond some tolerance across ranges of $N$ and $x$.
- Test for known convergence diagnostics (ratio test proxy numerically, boundedness of tail estimates) as regularization terms.
- Include multi-resolution grids in $x$ and in truncation depth $N$, with higher weight for agreement between deep truncations and a numerical ground truth function.

These ideas are not, as far as I can see, standard in the GP/symbolic‑regression literature, but they’re compatible with existing frameworks like PySR, which lets you plug in arbitrary custom loss functions.[^3]

***

## (2) “Wrong-limit” / deceptive attractors

In symbolic regression, your “wrong-limit but locally great” expressions are essentially deceptive fitness attractors: simple expressions that match a finite sample yet disagree on the true asymptotic behavior. This is well studied in GA theory but usually on synthetic trap functions rather than series.[^12][^1]

Relevant pieces:

- Deceptive functions in evolutionary computation: “trap” functions are designed so that intermediate optima look attractive (e.g., many 1s) but are far from the global optimum, and they drive analyses of selection pressure and linkage learning.[^1][^12]
- Scalable GP with gene-pool optimal mixing: Bosman and colleagues study deceptive attractors in GP, using trap-like problems to evaluate how recombination strategies avoid or get stuck in them.[^12][^1]
- GP convergence work (Langdon): analyses of how populations drift and converge in GP, including the role of selection pressure and the explosion of equivalent phenotypes, which contributes to bloat rather than correct generalization.[^4]

To mitigate wrong-limit attractors in series discovery, techniques suggested by that body of work and by SINDy/SR practice include:

- Explicit out-of-domain evaluation: add fitness points at very large (or complex) values of the independent variable, tailored to stress the asymptotic regime.[^5][^7]
- Multi-fidelity or curriculum fitness: gradually increase the weight of asymptotic-region points so that early search can exploit easy local fits, but later it must satisfy asymptotics to continue improving.[^7][^5]
- Complexity‑aware penalties: many SR frameworks already penalize expression complexity; you can pair this with constraints (e.g., preclude a family of “simple but wrong-limit” forms if you can characterize them), or explicitly reward known correct asymptotics when you have theoretical prior.[^7][^3]

None of the major SR papers I saw provide a dedicated taxonomy or experimental study of “wrong-limit” symbolic attractors, but the mechanisms are in line with deceptive landscapes and overfitting concerns discussed in the broader GP/SR literature.[^4][^1][^7]

***

## (3) Phase transitions vs terminal-set size

Your third point—**phase transitions** in GP discovery as the terminal set grows—is partially addressed in work on GP convergence, bloat, and scalability, but often not framed explicitly as critical phase transitions.[^1][^4]

Some relevant angles:

- Langdon’s “Genetic Programming Convergence”: discusses how, in continuous domains like symbolic regression, the enormous set of possible fitness values delays total convergence, and how selection and crossover interact to drive bloat and loss of diversity.  While not about terminal-set size per se, the analysis is about how search-space richness affects convergence and selection pressure.[^4]
- Scalable GP / gene-pool optimal mixing: shows how problem structure, representation, and recombination strategies affect scalability on deceptive problems, implicitly reflecting how enlarging the search space (e.g., more terminals and primitives) can break simple evolutionary dynamics.[^12][^1]
- Terminal normalization work: in dynamic flexible job-shop scheduling with GP hyper-heuristics, researchers study how terminal magnitudes distort search and propose normalization strategies, which indirectly speaks to how properties of the terminal set can strongly influence GP behavior.[^13]

A concrete way to study transitions in your setting:

- Fix a family of target series, vary terminal set size (e.g., {+,−,×} vs adding /, exp, log, special functions, and more constants), and measure discovery probability vs search budget.
- You may see sharp drops or jumps in success rate as soon as certain primitives enter, analogous to phase transitions studied in SAT and other combinatorial problems.

This is, as far as I can see, not systematically documented for symbolic regression on series, which is an opportunity for an original experimental paper.

***

## Pointers to potentially useful adjacent work

None of these are exactly about series convergence, but they contain ideas about process-level fitness and long-horizon behavior:

- Physics-guided discovery of parametric PDEs: combines SR-like modeling with physical priors and focuses on correctly capturing parametric dependence and boundary conditions, i.e., global structure beyond pointwise fit.[^10]
- Discovery of PDEs with SINDy-BVP: identifies spatial operators for boundary value problems by fitting operator libraries; fitness considers satisfaction of BVP structure, which is a process-level property.[^11]
- Learning fitness functions for program synthesis: treats the fitness function itself as a learned object; while aimed at inductive program synthesis rather than series, this suggests meta‑learning a fitness that rewards desired asymptotics from data.[^14]

If you’d like, I can:

- Sketch an explicit convergence-aware fitness functional for GP over series (including numerical heuristics for divergence detection).
- Propose an experimental setup to quantify “wrong-limit” attractors and their dependence on terminal sets or priors, using something like PySR as the engine.
<span style="display:none">[^15][^16][^17][^18][^19][^20]</span>

<div align="center">⁂</div>

[^1]: https://homepages.cwi.nl/~bosman/publications/2017_scalablegeneticprogramming.pdf

[^2]: https://xaqlab.com/2018/12/21/distilling-free-form-natural-laws-from-experimental-data/

[^3]: https://arxiv.org/abs/2305.01582

[^4]: http://www0.cs.ucl.ac.uk/staff/wlangdon/ftp/papers/langdon_GPEM_gpconv.pdf

[^5]: https://www.pnas.org/doi/10.1073/pnas.1517384113

[^6]: https://arxiv.org/abs/1210.7273

[^7]: https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2020.00025/full

[^8]: https://arxiv.org/abs/1509.03580

[^9]: https://arxiv.org/html/2403.00578v1

[^10]: https://dl.acm.org/doi/abs/10.1145/3580305.3599466

[^11]: https://link.aps.org/doi/10.1103/PhysRevResearch.3.023255

[^12]: https://dl.acm.org/doi/pdf/10.1145/3071178.3071287

[^13]: https://www.sciencedirect.com/science/article/abs/pii/S2210650225001282

[^14]: https://par.nsf.gov/servlets/purl/10320104

[^15]: https://www.lesswrong.com/posts/NT8ev4kBXfW4ATC7m/re-discovering-natural-laws

[^16]: https://pubs.aip.org/aip/jcp/article/159/9/091501/2908710/Determining-best-practices-for-using-genetic

[^17]: https://royalsocietypublishing.org/rspa/article/474/2217/20180305/79999/Robust-data-driven-discovery-of-governing-physical

[^18]: http://ftp.math.utah.edu/pub/bibnet/authors/m/meitner-lise.html

[^19]: https://www.scribd.com/document/317837474/1203-4558-pdf

[^20]: http://ui.adsabs.harvard.edu/abs/2016APS..DFD.L8005B/abstract

