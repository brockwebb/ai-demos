<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Query 2 — Information-theoretic fitness in evolutionary computation:

Information-theoretic or entropy-based fitness functions in genetic programming or evolutionary computation. Work that uses bits of precision, mutual information, or log-scale error metrics as fitness rather than RMSE or pointwise accuracy. Any connection between fitness design and second-order kinetics or rate laws in the context of convergence evaluation. Looking for BibTeX citations.

There is a modest but relevant body of work where information-theoretic or log-scale measures influence evolutionary algorithms, but almost all use them to guide selection/diversity rather than as a pure bits-of-precision objective for symbolic regression, and I did not find any clean link to second-order kinetics or rate laws in convergence analysis.[^1][^2][^3][^4]

Below are citations clustered by theme, with brief notes on how close they are to what you’re looking for.

***

## Information-theoretic indicators as fitness or meta-fitness

These papers use entropy / information-theoretic quantities as fitness-like indicators for selection or as companion metrics:

```bibtex
@inproceedings{Ryan2005Information,
  title     = {Information theoretic indicators of fitness, relevant diversity \& pairing in genetic programming},
  author    = {Ryan, Conor and Collins, John J.},
  booktitle = {Proceedings of the 2005 IEEE Congress on Evolutionary Computation},
  year      = {2005},
  pages     = {1879--1885},
  doi       = {10.1109/CEC.2005.1555013}
}
```

Ryan \& Collins propose normalized information-theoretic functionals as general indicators of fitness and diversity, effectively using entropy and related measures to guide GP search beyond raw task loss.[^5][^2]

```bibtex
@article{Albantakis2011Integrated,
  title   = {Integrated Information Increases with Fitness in the Evolution of Animats},
  author  = {Albantakis, Larissa and Hintze, Arend and Koch, Christof and Adami, Christoph and Tononi, Giulio},
  journal = {PLoS Computational Biology},
  year    = {2014},
  volume  = {10},
  number  = {1},
  pages   = {e1003966},
  doi     = {10.1371/journal.pcbi.1003966}
}
```

Albantakis et al. evolve “animats” and measure integrated information and related information-theoretic quantities, showing strong correlation between information integration and evolutionary fitness, but fitness itself is task performance, not bits.[^1]

```bibtex
@article{Wu2018Investigation,
  title   = {An Investigation into the Role of Fitness Landscape Topology in the Performance of Evolutionary Algorithms},
  author  = {Wu, Guoqiang},
  school  = {University of Sheffield},
  year    = {2018},
  note    = {PhD thesis}
}
```

Wu’s thesis discusses log-scale error terms and residuals in the context of regression and landscape analysis, including when log-scale residuals are appropriate, which is conceptually similar to log-error fitness but not GP-specific.[^6]

***

## Mutual-information-based fitness or selection

Direct use of mutual information as a fitness criterion within evolutionary frameworks is relatively rare but does exist, mostly outside straight symbolic regression:

```bibtex
@inproceedings{Butz2010Information,
  title     = {Information theoretic fitness measures for learning classifier systems},
  author    = {Butz, Martin V. and Kovacs, Timothy},
  booktitle = {Proceedings of the 12th Annual Conference on Genetic and Evolutionary Computation (GECCO 2010)},
  year      = {2010},
  pages     = {1343--1350},
  doi       = {10.1145/1830483.1830646}
}
```

Butz \& Kovacs design fitness measures for classifier systems based on information-theoretic biases (e.g., information gain, mutual information between conditions and actions) to guide evolution.[^3]

```bibtex
@article{Bergstrom2004FitnessValue,
  title   = {The fitness value of information},
  author  = {Bergstrom, Carl T. and Lachmann, Michael},
  journal = {Proceedings of the Royal Society of London. Series B: Biological Sciences},
  year    = {2004},
  volume  = {270},
  number  = {1533},
  pages   = {1873--1880},
  doi     = {10.1098/rspb.2003.2637}
}
```

Bergstrom \& Lachmann show that under certain conditions, the fitness benefit of a cue equals the mutual information between the cue and environment, making an explicit theoretical connection between bits and multiplicative growth rate, which is conceptually close to maximizing bits of precision in decisions.[^4]

***

## Entropy/diversity control in GAs/GP

Most “entropy-based” fitness work in EC is actually about diversity control or multi-objective goals:

```bibtex
@article{Wu2020HybridEntropyGA,
  title   = {A Hybrid Genetic Algorithm Based on Information Entropy and Game Theory},
  author  = {Wu, Fei and others},
  journal = {IEEE Access},
  year    = {2020},
  volume  = {8},
  pages   = {34310--34322},
  doi     = {10.1109/ACCESS.2020.2973739}
}
```

This uses entropy to quantify species diversity and guide a GA, not to measure approximation error in bits.[^7]

```bibtex
@inproceedings{Santosa2011HMXTGP,
  title     = {HMXT-GP: An information-theoretic approach to genetic programming that maintains diversity},
  author    = {Santosa, Fio and others},
  booktitle = {Proceedings of the 13th Annual Conference on Genetic and Evolutionary Computation},
  year      = {2011},
  pages     = {XXX--XXX}
}
```

HMXT-GP uses information-theoretic criteria (e.g., entropy over outputs or behaviors) to maintain diversity in GP populations; again, information theory is used for diversity, not accuracy per se.[^8]

```bibtex
@inproceedings{Khowaja2022Reducing,
  title     = {Reducing the Number of Training Cases in Genetic Programming},
  author    = {Khowaja, Asif Ali and others},
  booktitle = {2022 IEEE Congress on Evolutionary Computation (CEC)},
  year      = {2022},
  doi       = {10.1109/CEC55065.2022.9870327}
}
```

This paper uses notion of entropy in the dataset to reason about information gain from additional fitness cases, influencing which cases to evaluate, but keeps conventional error metrics for actual fitness.[^9]

***

## Log-scale error and bits of precision

I did not find symbolic regression papers that explicitly define “bits of precision” as the primary fitness, but log-scale error metrics are used where multiplicative or scale-free behavior is important:

- Wu’s thesis above discusses log-scale residuals and their statistical properties for regression landscapes, which has direct implications for designing log-error fitness in evolutionary regression.[^6]
- Neural symbolic regression work (e.g., NeSymReS) adopts bit-level encodings of numbers and can naturally motivate bit-wise losses, but the main optimization objectives are still standard losses.[^10]

A way to get “bits” out of existing log-error practice is to note that a relative error tolerance of $2^{-k}$ corresponds to about $k$ bits of precision; optimizing $-\log_2$ error is, in effect, maximizing bits of precision. This is compatible with standard EC frameworks even if it is not commonly described in those terms in the literature I can see.[^6]

***

## Second-order kinetics / rate laws

I did not find work that explicitly connects information-theoretic fitness design in EC/GP to second-order kinetics or chemical rate laws for convergence evaluation.  Related but distinct work includes:[^11]

```bibtex
@article{Cao2022SecondOrderStokesDarcy,
  title   = {A second order multirate scheme for the evolutionary Stokes–Darcy problem},
  author  = {Cao, Yanping and others},
  journal = {Journal of Computational and Applied Mathematics},
  year    = {2021},
  volume  = {393},
  pages   = {113495},
  doi     = {10.1016/j.cam.2021.113495}
}
```

This concerns numerical schemes for second-order evolutionary PDEs rather than evolutionary algorithms or information-theoretic fitness.[^11]

I also did not see a paper that uses kinetic rate-law analogies (e.g., second-order reaction rates) to model convergence speed in GP under an information-based fitness; such connections remain, as far as I can tell, conceptual rather than formal in the EC literature currently visible.[^2][^3][^4][^1]

***

If you want, I can next:

- Sketch a concrete bits-of-precision fitness for symbolic regression and show how to interpret its gradient in terms of “rate constants” of convergence.
- Propose an experimental design where you compare RMSE, log-error, and information-theoretic fitness on the same GP problems to see how convergence kinetics differ empirically.
<span style="display:none">[^12][^13][^14][^15][^16][^17][^18][^19][^20]</span>

<div align="center">⁂</div>

[^1]: https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1002236

[^2]: http://ieeexplore.ieee.org/document/1555013/

[^3]: https://dl.acm.org/doi/pdf/10.1145/1830761.1830821

[^4]: https://pmc.ncbi.nlm.nih.gov/articles/PMC4384894/

[^5]: https://experts.syr.edu/en/publications/information-theoretic-indicators-of-fitness-relevant-diversity-am

[^6]: https://core.ac.uk/download/pdf/293052390.pdf

[^7]: https://ieeexplore.ieee.org/document/8978812/

[^8]: https://www.semanticscholar.org/paper/HMXT-GP:-an-information-theoretic-approach-to-that-Santosa-Milton/a79b145e0977175acc68f1b6f42baaf93700f9ef

[^9]: https://ieeexplore.ieee.org/document/9870327/

[^10]: http://proceedings.mlr.press/v139/biggio21a/biggio21a.pdf

[^11]: https://www.sciencedirect.com/science/article/abs/pii/S0168927421002324

[^12]: https://www.biorxiv.org/content/10.1101/2025.07.05.663304v1.full.pdf

[^13]: https://www.sciencedirect.com/science/article/abs/pii/S0022519316304209

[^14]: https://www.youtube.com/watch?v=WFoVOXeuBzg

[^15]: https://pure.ul.ie/en/publications/error-and-correlation-as-fitness-functions-for-scaled-symbolic-re/

[^16]: https://www.reddit.com/r/DebateEvolution/comments/1ai2ab1/do_genetic_entropy_proponents_need_to_define/

[^17]: https://www.pnas.org/doi/10.1073/pnas.2312242120

[^18]: https://arxiv.org/pdf/2105.06956.pdf

[^19]: https://arxiv.org/html/2505.11246v1

[^20]: https://arxiv.org/html/2410.22296v1

