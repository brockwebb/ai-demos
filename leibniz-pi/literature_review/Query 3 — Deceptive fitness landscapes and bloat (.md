<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Query 3 — Deceptive fitness landscapes and bloat (narrower):

Deceptive fitness landscapes in genetic programming where incorrect solutions score higher than correct ones on finite evaluation. Distinct from GP bloat — specifically cases where simpler wrong expressions outperform correct complex expressions. Finite evaluation window as a source of deception in symbolic regression. BibTeX entries for key papers.

Finite sampling and usual SR fitness make it easy for structurally simple, wrong expressions to outscore more complex but correct ones, and this has been studied under deceptive landscapes, overfitting, and scaling-induced “scaling-deceptive” behavior; however, most work treats this as overfitting/robustness rather than giving it a separate taxonomy from bloat.  Below are key papers with BibTeX that are close to what you described.[^1][^2][^3][^4]

***

## Fitness landscape analysis and deception in GP/SR

```bibtex
@article{Durasevic2020Fitness,
  title   = {Fitness Landscape Analysis of Dimensionally-Aware Genetic Programming Featuring Feynman Equations},
  author  = {Durasevic, Marko and Jakobovic, Domagoj and Ribeiro Martins, Marcella Scoczynski and Picek, Stjepan and Wagner, Markus},
  journal = {arXiv preprint arXiv:2004.12762},
  year    = {2020},
  url     = {https://arxiv.org/abs/2004.12762}
}
```

Durasevic et al. analyze fitness landscapes for symbolic regression on Feynman equations, comparing standard vs dimensionally-aware GP and showing how additional constraints reshape local optima and ruggedness, i.e., reduce deceptive basins where incorrect-but-simple expressions look attractive.[^2]

```bibtex
@inproceedings{Jiang2023Fitness,
  title     = {Fitness Landscape Analysis of Genetic Programming Search Spaces},
  author    = {Jiang, Eric and others},
  booktitle = {Proceedings of the 2023 Genetic and Evolutionary Computation Conference (GECCO 2023)},
  year      = {2023},
  pages     = {XXX--XXX},
  publisher = {ACM}
}
```

This paper studies GP landscapes on parity, symbolic regression, and artificial ant, using local-search style probes to characterize neutrality, ruggedness, and local optima; symbolic-regression results highlight how many local optima correspond to suboptimal functions that nonetheless score highly on the finite evaluation set.[^1][^5]

***

## Overfitting, scaling, and “scaling-deceptive” behavior

```bibtex
@incollection{Keijzer2011ScalingDeceptive,
  title     = {Improving Symbolic Regression with Affine Arithmetic},
  author    = {Keijzer, Maarten and others},
  booktitle = {Genetic Programming Theory and Practice IX},
  publisher = {Springer},
  year      = {2011},
  pages     = {151--167}
}
```

Keijzer et al. focus on avoiding overfitting and extreme out-of-sample errors in symbolic regression, and explicitly discuss “scaling-deceptive” cases where linear scaling and finite training windows let structurally simple but asymptotically bad formulas look excellent on the training set.[^4]

```bibtex
@inproceedings{Haghighat2015AvoidingOverfitting,
  title     = {Avoiding Overfitting in Symbolic Regression Using the First Order Derivative},
  author    = {Haghighat, Behzad and others},
  booktitle = {Proceedings of the 2015 Genetic and Evolutionary Computation Conference (GECCO 2015)},
  year      = {2015},
  pages     = {1441--1448},
  publisher = {ACM}
}
```

Haghighat et al. add derivative-based terms as a second objective in symbolic regression, reducing overfitting by penalizing functions that match training points but have qualitatively different behavior (e.g., wrong curvature) outside the finite evaluation window, which directly targets deceptive simple solutions.[^3]

```bibtex
@inproceedings{Muldoon2023ErrorCorrelation,
  title     = {Error and Correlation as Fitness Functions for Scaled Symbolic Regression},
  author    = {Muldoon, Conor and O'Neill, Michael and Brabazon, Anthony},
  booktitle = {GECCO 2023 Companion - Proceedings of the 2023 Genetic and Evolutionary Computation Conference Companion},
  year      = {2023},
  pages     = {607--610},
  publisher = {ACM},
  doi       = {10.1145/3583133.3590633}
}
```

Muldoon et al. study how using error versus correlation (with linear scaling) as fitness changes the landscape for symbolic regression; they show that different metrics can favor different regions of the search space, i.e., some metrics prefer smaller but systematically biased models that perform worse off-sample.[^6]

***

## Bayesian / MDL-inspired fitness (wrong simple vs right complex)

```bibtex
@inproceedings{LaCasse2022BayesianBloat,
  title     = {Bayesian Model Selection for Reducing Bloat and Overfitting in Genetic Programming Symbolic Regression},
  author    = {La Casse, Christopher and others},
  booktitle = {Proceedings of the Genetic and Evolutionary Computation Conference (GECCO 2022)},
  year      = {2022},
  pages     = {XXX--XXX},
  publisher = {ACM}
}
```

La Casse et al. introduce a Bayesian/NML-based fitness metric that trades off fit and complexity in symbolic regression, explicitly analyzing scenarios “ripe for overfitting” where overly complex correct models and overly simple wrong models compete under finite data.[^7]

Their results show that standard RMSE-only fitness can prefer simpler but systematically wrong expressions, while the Bayesian metric tends to settle on moderate-complexity models with better generalization, i.e., it reshapes the deceptive landscape that arises from finite evaluation.[^7]

***

## Classic deceptive functions (conceptual backdrop)

While not GP-SR specific, classic GA deception work formalizes the phenomenon you care about (suboptimal solutions having higher observed fitness), and is often cited in GP theory:

```bibtex
@book{Goldberg1989GA,
  title     = {Genetic Algorithms in Search, Optimization and Machine Learning},
  author    = {Goldberg, David E.},
  publisher = {Addison-Wesley},
  year      = {1989}
}
```

Trap functions and deceptive landscapes in Goldberg’s framework provide the standard formal definition where local/global optima have systematically misaligned fitness; symbolic regression with finite windows gives a continuous analogue where “trap-like” simple formulas look optimal on sampled points.[^8]

***

## How these relate to your specific case

- Finite evaluation windows: Keijzer’s affine arithmetic bounds explicitly address expressions that behave well on the training window but blow up or deviate badly outside it, calling this a particularly damaging form of overfitting—essentially the scenario where simpler wrong expressions outperform complex correct ones on the finite sample.[^4]
- Deception vs bloat: La Casse’s Bayesian approach and Haghighat’s derivative objective both show that when you only optimize RMSE on a finite window, you can get either bloated overfitted expressions or deceptively simple-but-wrong formulas; adding complexity-aware or shape-aware terms reshapes this landscape.[^3][^7]
- Symbolic regression landscape work: Durasevic and Jiang demonstrate empirically that SR landscapes have abundant local optima with high but suboptimal fitness corresponding to incorrect models that align with the limited evaluation data but not the underlying function.[^1][^2]

If you’d like, I can next synthesize these into a more formal definition of “finite-window deception” for SR and suggest an experimental benchmark (analogous to trap functions) specifically tailored to your “wrong-limit but simple” series scenario.
<span style="display:none">[^10][^9]</span>

<div align="center">⁂</div>

[^1]: https://dl.acm.org/doi/10.1145/3583133.3596305

[^2]: https://arxiv.org/abs/2004.12762

[^3]: http://www.cmap.polytechnique.fr/~nikolaus.hansen/proceedings/2015/GECCO/companion/p1441.pdf

[^4]: https://research.google.com/pubs/archive/37641.pdf

[^5]: https://openresearch.surrey.ac.uk/esploro/outputs/conferenceProceeding/Fitness-Landscape-Analysis-of-Genetic-Programming/99928603102346

[^6]: https://pure.ul.ie/en/publications/error-and-correlation-as-fitness-functions-for-scaled-symbolic-re/

[^7]: https://ntrs.nasa.gov/api/citations/20220001900/downloads/smcbingo_gecco22.pdf

[^8]: https://cargo.wlu.ca/research_posters_2018/CARGO_Lab_Poster_March_2018_Eric_Jiang.pdf

[^9]: http://www.cmap.polytechnique.fr/~nikolaus.hansen/proceedings/2011/GECCO/proceedings/p1467.pdf

[^10]: http://www.evostar.org/2017/cfp_eurogp.php

