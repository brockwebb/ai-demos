# CC Task: Tier 3 Bibliography Expansion and Supporting Citations

**Date:** 2026-03-25
**Scope:** Add supporting citations from fact-check Tier 3 results. Surgical prose insertions in Sections 5.4, 6.2, and 7. New .bib entries.
**Principle:** These are strengthening citations, not corrections. Each addition is 1-2 sentences max. We are not rewriting sections.

---

## Pre-Flight

1. Read `paper/references.bib` (current state).
2. Read `paper/sections/05_results.md` (current state).
3. Read `paper/sections/06_discussion.md` (current state).
4. Read `paper/sections/07_conclusion.md` (current state).
5. Read `paper/conventions.md` for style rules.

---

## New .bib Entries

Add all of the following to `paper/references.bib`. Verify each entry via web search before adding. If a title, venue, or year cannot be confirmed, skip that entry and report.

```bibtex
% ═══════════════════════════════════════════════════════════════
% Parsimony pressure and population sizing
% ═══════════════════════════════════════════════════════════════

@inproceedings{Poli2008ParsimonyEasy,
  title     = {Parsimony Pressure Made Easy},
  author    = {Poli, Riccardo and McPhee, Nicholas Freitag},
  booktitle = {Proceedings of the 10th Annual Conference on Genetic and Evolutionary Computation (GECCO 2008)},
  pages     = {1267--1274},
  year      = {2008},
  publisher = {ACM},
  doi       = {10.1145/1389095.1389340}
}

@article{Soule1998CodeGrowth,
  title   = {Effects of Code Growth and Parsimony Pressure on Populations in Genetic Programming},
  author  = {Soule, Terence and Foster, James A.},
  journal = {Evolutionary Computation},
  volume  = {6},
  number  = {4},
  pages   = {293--309},
  year    = {1998},
  doi     = {10.1162/evco.1998.6.4.293}
}

@article{Luke2003PopulationSizing,
  title   = {Population Sizing for Genetic Programming Based Upon Decision Making},
  author  = {Luke, Sean and Panait, Liviu and others},
  journal = {arXiv preprint cs/0502020},
  year    = {2003},
  url     = {https://arxiv.org/abs/cs/0502020}
}

% ═══════════════════════════════════════════════════════════════
% Feature selection and terminal pruning for GP
% ═══════════════════════════════════════════════════════════════

@inproceedings{Murphy2019GEFS,
  title     = {Automated Grammar-based Feature Selection in Symbolic Regression},
  author    = {Murphy, Aidan and Kelleher, John D. and Ryan, Conor},
  booktitle = {Proceedings of the Genetic and Evolutionary Computation Conference (GECCO)},
  year      = {2019},
  publisher = {ACM}
}
```

**IMPORTANT:** Verify the Murphy et al. GEFS paper — confirm the exact title, authors, year, and venue via web search. The description from the fact-check references an approach called "GEFS" using grammar-based feature selection as a preprocessing stage for GE/GP. If the exact paper cannot be confirmed, search for "automated grammar-based feature selection symbolic regression" and use the best match. If nothing is found, skip this entry and note it.

Similarly, verify Luke et al. — the fact-check says "Population Sizing for Genetic Programming Based Upon Decision Making" at arXiv cs/0502020. Confirm.

---

## Prose Insertions

### Section 5.4 — Parsimony pressure context (1-2 sentences)

Find the paragraph that discusses the sharp transition at λ_p = 0.005 to λ_p = 0.01. After the existing discussion of the threshold behavior, add:

> This threshold sensitivity is consistent with prior findings that parsimony pressure has a narrow effective range: too weak and it fails to control bloat, too strong and it collapses the population to trivial solutions (Poli and McPhee, 2008; Soule and Foster, 1998). Our contribution is the quantitative demonstration of the crossover point where the Leibniz tree's fitness falls below the zero-constant attractor.

Read the file first. Find the exact insertion point. Do not alter surrounding text.

### Section 6.2 — Coverage and population sizing (1 sentence)

Find the paragraph discussing "Coverage scales linearly with population size." After that sentence, add:

> Luke et al. (2003) derived a population-sizing relationship for GP from building-block decision-making theory, formalizing the intuition that the required population scales with the number of building blocks that must be simultaneously present.

Read the file first. Do not alter surrounding text.

### Section 7 — Future work prior art acknowledgment (1-2 sentences)

Find the paragraph listing three future directions (building block initialization, automated terminal pruning, island migration). After the sentence about automated terminal pruning, add:

> Grammar-based feature selection methods already demonstrate this principle in a preprocessing stage (Murphy et al., 2019), though they have not been applied to the convergent-series problem class.

Read the file first. Do not alter surrounding text. If the Murphy citation could not be verified in the .bib step, omit this insertion.

---

## Post-Flight

1. Run `python paper/check_glossary.py`.
2. Run `seldon paper sync`.
3. Run `seldon paper build --no-render`.
4. Report: entries added, entries skipped (with reason), prose insertions made, any build issues.

## Do NOT

- Do not rewrite existing paragraphs.
- Do not add more than 2 sentences per insertion point.
- Do not modify sections other than 05, 06, 07, and references.bib.
- Do not alter Seldon result references.
- Read current file state before every edit.
