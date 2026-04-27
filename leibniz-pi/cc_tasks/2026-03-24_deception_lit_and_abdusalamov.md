# CC Task: Add Deception Literature Connection and Abdusalamov Citation

**Date:** 2026-03-24
**Scope:** Two targeted additions to the paper based on Perplexity fact-check results. Plus register new citations in references.bib.
**Sections affected:** 02_background.md, references.bib

---

## Pre-Flight

1. Read `paper/conventions.md` for style rules.
2. Read current state of `paper/sections/02_background.md`.
3. Read current state of `paper/references.bib`.

---

## Task 1: Add Abdusalamov et al. (2023) citation to Section 2.2

**Context:** Perplexity identified Abdusalamov et al. (2023) as the closest adjacent work to our process-level fitness design. They use symbolic regression to discover asymptotic series expansions in mechanics problems, but their fitness is still pointwise (error between SR output and exact solution at sampled points). They do not evaluate convergence rate or asymptotic scaling as a fitness criterion. This is the closest thing to what we do, and we should cite it to show we know the landscape.

**Action:** In Section 2.2 ("Fitness Design for Convergent Processes"), after the paragraph that begins "Prior symbolic regression work does not address fitness design for this objective class," add a sentence citing Abdusalamov et al. as the closest adjacent work.

**Proposed insertion** (after "Both require evaluating trajectory behavior rather than endpoint accuracy, but the Leibniz problem evaluates convergence structure across geometric scales rather than sequential forecast accuracy."):

> Abdusalamov et al. (2023) use symbolic regression to discover asymptotic series expansions for problems in mechanics, recovering convergent and divergent series from exact solutions. Their fitness is still pointwise: SR expressions are evaluated against sampled data, not against convergence properties of their partial sums. The Leibniz problem differs in that no target data exist; fitness must evaluate the summation process itself.

**Verify:** Read the current file before editing. Confirm the insertion point exists. Do not alter surrounding text.

---

## Task 2: Connect wrong-limit attractors to deception literature in Section 2.3

**Context:** Perplexity confirmed that deceptive attractors and deceptive fitness landscapes are well-established concepts in GA/GP (Deb, Goldberg, etc.), but nobody has applied them to infinite-horizon process evaluation or formalized the "structurally simpler expression converging to a wrong limit" failure mode. We should connect to this literature explicitly to show we are aware of it and to sharpen the distinction.

**Action:** In Section 2.3 ("Wrong-Limit Attractors"), find the final paragraph that begins "To our knowledge, no prior work analyzes this failure mode as distinct from bloat or overfitting in symbolic regression." Add a sentence connecting to the deception literature before or after this claim.

**Proposed insertion** (before the "To our knowledge" sentence):

> The concept is related to deceptive attractors in genetic algorithms, where low-order schema information draws search toward suboptimal solutions (Goldberg, 1989; Deb and Goldberg, 1993). Deceptive attractors are defined by misleading fitness gradients in genotype space. Wrong-limit attractors are defined by indistinguishable behavior within a finite evaluation horizon: the deception is in the process output, not the search space topology.

**Verify:** Read the current file before editing. Confirm the insertion point exists. The paper already cites Goldberg (1989). Do not alter surrounding text.

---

## Task 3: Register new citations in references.bib

Add the following entries to `paper/references.bib`. Place them in the appropriate sections (create a new section comment if needed).

### Abdusalamov et al. (2023)

```bibtex
@article{Abdusalamov2023Asymptotic,
  title   = {Discovering asymptotic expansions for problems in mechanics using symbolic regression},
  author  = {Abdusalamov, Rasul and Kaplunov, Julius and Itskov, Mikhail},
  journal = {Mechanics Research Communications},
  volume  = {133},
  pages   = {104197},
  year    = {2023},
  doi     = {10.1016/j.mechrescom.2023.104197}
}
```

### Deb and Goldberg (1993)

Verify this citation exists and is correct before adding. The canonical paper on deceptive problems in GAs by Deb and Goldberg. Search for: "Deb Goldberg 1993 deceptive problems genetic algorithms". The likely reference is:

```bibtex
@inproceedings{Deb1993Deceptive,
  title     = {Analyzing Deception in Trap Functions},
  author    = {Deb, Kalyanmoy and Goldberg, David E.},
  booktitle = {Foundations of Genetic Algorithms},
  volume    = {2},
  pages     = {93--108},
  year      = {1993},
  publisher = {Morgan Kaufmann}
}
```

**IMPORTANT:** Before registering this citation, verify the title, year, and venue are correct. Search the web or the paper's own references. If you cannot verify, use only Goldberg (1989) which is already in the .bib file, and adjust the prose accordingly (drop "Deb and Goldberg, 1993" from the inserted text, keep only "Goldberg, 1989").

---

## Post-Flight

1. Run `seldon paper sync` to pick up changes.
2. Run `seldon paper build --no-render` to verify no broken references.
3. Run `seldon paper audit paper/sections/02_background.md` for glossary/style check.
4. Run `python paper/check_glossary.py` for conventions compliance.
5. Report: what was added, what was verified, any issues.

## Do NOT

- Do not modify any text outside the specific insertion points described above.
- Do not rewrite existing paragraphs.
- Do not hardcode any Seldon result values.
- Do not modify any other section files.
- Read the current file state before every edit.
