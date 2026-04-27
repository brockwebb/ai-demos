# CC Task: Citation Fixes from Fact-Check Pass

**Date:** 2026-03-25
**Scope:** Add missing .bib entries, fix Hillar/Sommer characterization in Section 2
**Sections affected:** references.bib, 02_background.md

---

## Pre-Flight

1. Read current state of `paper/references.bib`.
2. Read current state of `paper/sections/02_background.md`.

---

## Task 1: Add missing .bib entries

Add these two entries to `paper/references.bib`. Place them in the appropriate sections.

```bibtex
@inproceedings{Li2023GFlowNet,
  title     = {{GFN-SR}: Symbolic Regression with Generative Flow Networks},
  author    = {Li, Sida and Marinescu, Ioana and Musslick, Sebastian},
  booktitle = {NeurIPS 2023 AI for Science Workshop},
  year      = {2023},
  url       = {https://arxiv.org/abs/2312.00396}
}

@article{Jiang2025EGGSR,
  title   = {{EGG-SR}: Embedding Symbolic Equivalence into Symbolic Regression via Equality Graph},
  author  = {Jiang, Nan and Wang, Ziyi and Xue, Yexiang},
  journal = {arXiv preprint arXiv:2511.05849},
  year    = {2025},
  url     = {https://arxiv.org/abs/2511.05849}
}
```

Also verify that the existing Kamienny and Shojaee entries are present and correct. If missing, add:

```bibtex
@inproceedings{Kamienny2023MCTS,
  title     = {Deep Generative Symbolic Regression with {Monte-Carlo-Tree-Search}},
  author    = {Kamienny, Pierre-Alexandre and Lample, Guillaume and Lamprier, Sylvain and Virgolin, Marco},
  booktitle = {Proceedings of the 40th International Conference on Machine Learning (ICML)},
  pages     = {15655--15668},
  year      = {2023},
  publisher = {PMLR}
}

@inproceedings{Shojaee2023TPSR,
  title     = {Transformer-based Planning for Symbolic Regression},
  author    = {Shojaee, Parshin and Meidani, Kazem and Barati Farimani, Amir and Reddy, Chandan},
  booktitle = {Advances in Neural Information Processing Systems 36 (NeurIPS)},
  pages     = {45907--45919},
  year      = {2023}
}
```

---

## Task 2: Fix Hillar/Sommer characterization in Section 2.1

**Current text (approximate):**
> "Hillar and Sommer (2012) subsequently demonstrated that the operator set and fitness structure implicitly encoded physical priors."

**Problem:** Hillar and Sommer's critique was specifically about the **fitness function** encoding Hamilton's equations and Newton's second law, not about the operator set. The operator set framing is inaccurate.

**Replace with:**
> Hillar and Sommer (2012) subsequently demonstrated that the fitness function implicitly encoded Hamilton's equations, so that high-fitness expressions were Hamiltonians by construction. The "laws" were not discovered from scratch; the fitness measure already contained classical mechanics.

**Instructions:** Read `02_background.md` first. Find the exact sentence about Hillar and Sommer. Replace only that sentence and the one following it if needed. Do not alter surrounding text.

---

## Task 3: Verify citation keys match prose

Search `paper/sections/*.md` for every instance of "Li et al." and "Jiang et al." to confirm the citation keys will resolve. The prose currently uses parenthetical citations like "(Li et al., 2023)" — verify these match the .bib keys added above. If the paper uses a different citation format (e.g., `\cite{}`), adjust accordingly.

Also check: the paper cites "Li et al., 2023" twice in Section 2.1 — once for "neural-symbolic" and once for "generative flow." Both refer to the same paper (GFN-SR). This is fine if the paper is listed once in references. But if the paper text implies two different papers by "Li et al., 2023," that needs to be fixed. GFN-SR is a generative flow approach, not neural-symbolic. If "neural-symbolic (Li et al., 2023)" refers to a different paper, find and verify that paper. If it cannot be found, remove the "neural-symbolic" attribution to Li.

---

## Post-Flight

1. Run `seldon paper sync`.
2. Run `seldon paper build --no-render`.
3. Report: entries added, characterization fix applied, any citation resolution issues.

## Do NOT

- Do not modify any text outside the specific changes described.
- Do not rewrite paragraphs.
- Read current file state before every edit.
