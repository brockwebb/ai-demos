# CC Task: AD-020 Review Pipeline — Leibniz-Pi Paper (Dogfood Run)

**Date:** 2026-04-02
**Project:** leibniz-pi
**Reference:** AD-020 (Iterative Content Review Pipeline), document_type: `academic_paper`
**Purpose:** First dogfood test of the AD-020 multi-lens review pipeline on a complete paper. Calibration run — evaluate whether the gates surface real issues or noise.

---

## Context

The leibniz-pi paper is complete and waiting for a final read before submission. ~63KB across 8 sections (abstract through conclusion + appendix). The whole paper fits in one context window — no agent team needed. This is a single-session run of all three tiers, producing a synthesis document the author can work through serially.

Document type: `academic_paper`
Audience: GP/evolutionary computation researchers, AI safety researchers
Stress test persona: Reviewer 2 (skeptical, looking for holes in the argument)

## Instructions

### Step 0: Load the paper

Read all sections in order:
```
sections/00_abstract.md
sections/01_introduction.md
sections/02_background.md
sections/03_methods.md
sections/04_experimental_design.md
sections/05_results.md
sections/06_discussion.md
sections/07_conclusion.md
sections/09_appendix_expressions.md
```

Also read:
- `glossary.md` — controlled vocabulary (use for terminology checks)
- `evidence_map.md` — claims→evidence mapping (use for argument completeness)
- `references.bib` — existing citations

### Step 1: Tier 1 — Correctness Audit (AD-019, adapted)

Run the content auditor protocol on the paper. For an academic paper, this means:
- Classify every substantive assertion as fact/judgment/conjecture
- Check citation coverage — every factual claim should have a citation
- Check terminology against `glossary.md`
- Check evidence claims against `evidence_map.md` — are all cited results actually in the evidence map? Are there evidence map entries not cited in the paper?
- Check cross-section consistency — do the abstract, introduction, results, and conclusion agree on the numbers?

Write output to `audits/paper_content_audit.yaml` using the AD-019 YAML format.

**Note:** This paper already has a glossary checker (`check_glossary.py`) and prose QC (`prose_qc.py`). Run both first to catch mechanical issues:
```bash
python paper/check_glossary.py
python paper/prose_qc.py
```
Focus the manual audit on content-level issues these tools don't catch.

### Step 2: Tier 2a — Reviewer Stress Test

Persona: Reviewer 2 at GECCO or a GP workshop. Skeptical. Looking for:
- Unstated assumptions
- Alternative explanations not considered
- Missing baselines or controls
- Claims that don't follow from the evidence
- Scope limitations not acknowledged

Generate 8-10 questions Reviewer 2 would ask. For each:
1. Attempt to answer from the paper material only
2. Score: fully answerable / partially answerable / not answerable
3. For partial/not: describe the gap

Example questions (generated, not prescribed — the agent should generate its own):
- "You claim fitness engineering can't overcome the phase transition. Did you try X?"
- "How do you know the wrong-limit attractors aren't just an artifact of your specific GP configuration?"
- "What happens at terminal set sizes between 8 and 10? You jump from 'succeeds' to 'fails' — where's the boundary?"
- "The kinetics analogy in the Discussion — is this just hand-waving or does it predict anything testable?"

Write output to `audits/paper_reviewer_stress_test.yaml`:
```yaml
stress_test:
  file: "paper (all sections)"
  document_type: academic_paper
  persona: "Reviewer 2 — GP/EC venue"
  date: "[ISO date]"

  questions:
    - id: 1
      question: "[the question]"
      answerable: "fully | partially | not"
      answer_from_material: "[what the paper says, if anything]"
      gap: "[what's missing, if partially or not answerable]"
      affected_sections: ["[section files]"]
```

### Step 3: Tier 2b — Argument Completeness Check

For `academic_paper`, this replaces the Bloom taxonomy check. Walk the argument chain:

1. For each major claim in the paper (abstract claims, introduction framing, results assertions, discussion interpretations, conclusion statements):
   - Is there evidence cited for this claim?
   - Does the evidence actually support the claim, or is there a logical gap?
   - Are there unstated assumptions bridging evidence to claim?

2. For each piece of evidence (experimental results, figures, tables):
   - Is it cited by at least one claim?
   - Is it cited in the right section?
   - Does the claim accurately represent the evidence, or does it overstate/understate?

3. Cross-section consistency:
   - Do abstract claims match conclusion claims?
   - Do results numbers match what's cited in discussion?
   - Are limitations stated in discussion reflected in the conclusion's scope?

Write output to `audits/paper_argument_completeness.yaml`:
```yaml
argument_check:
  file: "paper (all sections)"
  date: "[ISO date]"

  claims_without_evidence: []
  evidence_without_claims: []
  logical_gaps: []
  overstated_claims: []
  cross_section_inconsistencies: []
```

### Step 4: Tier 3 — Secondary Lens Sweep (Blended)

Single pass. Tag each finding with its lens. Don't repeat what Tiers 1-2 already flagged.

Lenses for `academic_paper`:
- **[narrative]**: Does the paper have an argument arc? Does each section earn its place? Is there a clear "so what?"
- **[clarity]**: Where would a reviewer or reader outside the immediate subfield get lost? Jargon without definition? Implicit knowledge not stated?
- **[visual]**: Where would a figure or table communicate faster than prose? Are existing figures well-referenced in the text?
- **[motivation]**: Light touch — does the introduction make clear why this matters beyond the GP community? (The wrong-limit attractor concept has implications for RL, LLMs, symbolic regression — is that connection made clearly enough?)

Write output to `audits/paper_secondary_sweep.yaml`:
```yaml
secondary_sweep:
  file: "paper (all sections)"
  date: "[ISO date]"

  findings:
    - lens: "[narrative | clarity | visual | motivation]"
      section: "[section file]"
      finding: "[description]"
      suggested_scope: "[what to do about it]"
```

### Step 5: Synthesis

Read all four audit outputs. Produce a single synthesis document:

1. Group findings by topic cluster (not by gate)
2. Count convergence (how many lenses flagged each cluster)
3. Write suggested scope for each cluster (not edits — scope)
4. Order by convergence, highest first
5. Make each cluster self-contained — the author reads one, addresses it, moves to next

Write output to `audits/paper_review_synthesis.yaml` using the format from AD-020 §2.3.

Cap at 8 clusters. If more than 8, group the remainder under `unclustered` as lower-priority items.

## Output Files

- `audits/paper_content_audit.yaml` — Tier 1 correctness
- `audits/paper_reviewer_stress_test.yaml` — Tier 2a reviewer questions
- `audits/paper_argument_completeness.yaml` — Tier 2b argument chain
- `audits/paper_secondary_sweep.yaml` — Tier 3 blended lenses
- `audits/paper_review_synthesis.yaml` — final clustered synthesis

## Do NOT

- Edit any paper sections
- Rewrite prose
- Change the glossary, evidence map, or references
- Run more than one iteration — this is a single diagnostic pass, not a refinement loop
- Chase perfection — the goal is to surface the top issues the author should consider before final read

## Meta: Calibration Questions

After producing the synthesis, note at the bottom of the synthesis file:
1. Which gate produced the most useful findings?
2. Which gate produced the most noise?
3. Did the `academic_paper` calibration feel right, or should gates be adjusted?
4. Was the clustering useful, or did it obscure things?

This is calibration data for AD-020 itself.
