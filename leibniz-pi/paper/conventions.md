# Writing Conventions — General Template

Reusable conventions for academic/research writing. Derived from three iterations
of the FCSM pragmatics paper. Copy to your paper directory and add paper-specific
rules at the bottom.

Machine-checkable rules are also codified in `paper_qc_config.yaml` (Tier 2)
and `paper_style_config.yaml` (Tier 3). This document is the human-readable
reference for authors and AI editors.

---

## Terminology

- **"Confabulation" not "hallucination."** Consistent with NIST AI 600-1. Hallucination implies perception; confabulation implies constructing false knowledge presented as real.
- **"Novel" is banned.** Everything is novel to someone. Say what makes it different.
- **No em dashes.** Zero tolerance. Use commas, semicolons, colons, or restructure.

## Formatting

- **Bold: headings, labels, and almost nothing else.** In academic writing, bold is reserved for document structure (headings, subheadings, table/figure captions) and occasionally key terms on first introduction. No bold in running prose.
- **No bold pseudo-headers in prose.** If content warrants sub-structure, use a proper subheading. If not, write a strong topic sentence.
- **Italic run-in heads for labeled-list prose.** Limitations, future work, enumerated conditions: `*Label.* The evaluation was conducted...` (APA Level 4 convention).
- **Italics for emphasis:** Standard convention. Use on the key contrast word or phrase, sparingly.
- **No bullet points in prose sections.** Write in paragraphs.

## Structure

- **Lead with the point.** The value proposition or key finding opens the section. Supporting evidence follows.
- **Exception:** When the conclusion is more credible as a discovery than an assertion — persuading a resistant audience. Build the case first, then land it.
- **Specificity is kindness.** Name the chapter, the section, the number. If you can be more specific, be more specific.

## Claims and Framing

- **Don't attribute errors to tools when you made the error.** "We made this error, caught it, and corrected it" is more credible.
- **Distinguish threat models from demonstrated attacks.** "Could enable" not "can enable" for threat-model scenarios.
- **Scope verification claims precisely.** Name what the evidence actually shows, not what you wish it showed.

## Prose Quality

- **No throat-clearing.** Delete "It is worth noting that" and similar preambles. Start with the point.
- **No redundant framing.** One statement, then evidence or implication.
- **No hedging stacks.** One hedge per claim maximum. "May suggest" fine. "May potentially be considered to suggest" not.
- **No self-congratulation.** Delete "remarkably," "notably," "strikingly," "importantly." Results speak.
- **Sentence length.** 35 words max. Split or find the clause that can stand alone.
- **Prefer active voice.** "We tested" not "It was tested." Passive OK when actor is irrelevant.
- **Prefer short declarative sentences.** Do not join independent thoughts with semicolons or commas when periods work.
- **One idea per paragraph.** Two distinct points = two paragraphs.
- **Minimum two sentences per paragraph.** Single sentences are transitions or underdeveloped ideas. Definitions exempt.
- **Avoid nominalizations.** "Explains" not "provides an explanation of."
- **Pronoun antecedents must be unambiguous.** "This finding" not "This."
- **Tense consistency.** Results: past. Claims about the system/framework: present. Don't mix within a paragraph.
- **First-person: "we" throughout.** Not "the authors," "one," or "the paper."

---

## Paper-Specific Rules

### Terminology

- **"Wrong-limit attractor"** is our coined term. Define on first use. Use consistently thereafter. Do not write "deceptive series," "false positive," or "spurious convergent."
- **"Discovery"** means the GP found a Leibniz-equivalent expression from random initialization. Not "rediscovery" (implies prior knowledge). Not "recovery" (implies reconstruction).
- **"Evaluation horizon"** is the maximum T at which partial sums are checked. Not "evaluation window" or "test range."
- **"Coverage"** refers to the fraction of structurally distinct building blocks present in the population. Not "diversity" (which has a specific GP meaning related to fitness variance).
- **"Log-precision fitness"** is the correct term for the fitness that measures -log₂(|error|). Do not write "entropy fitness" or "information-theoretic fitness" — these imply a connection to Shannon information theory that does not exist. The fitness measures log-scale precision, not entropy.
- **"Convergence-aware fitness"** for the first-order variant. Not "GP fitness" or "rate fitness."
- **"Slime mold"** may appear at most once as an analogy for the parallel search mechanism. After any such introductory mention, use "convergence-aware fitness" exclusively. Do not repeat "slime mold" elsewhere in the paper.
- **"Phase transition"** for the sharp boundary between discoverable and non-discoverable regions. Use "degradation" if data shows the boundary is gradual rather than sharp.

### Numbers and References

- All research numbers use Seldon references: `{{result:NAME:value}}`. Never write a literal number for a measured or computed result.
- GP engine parameters (P_CROSS=0.70, TOURNAMENT_K=7, etc.) can be literal since they are fixed experimental conditions.
- Mathematical constants (π/4, log₂(10)) can be literal.

### Framing

- The injection confound is our mistake. Frame it as "we made this error, caught it, and corrected it." Do not blame the tooling.
- The Hillar and Sommer (2012) parallel to our injection confound is a narrative strength. Use it.
- Wrong-limit attractors are the central finding. They are not failures of the fitness function. They are coverage failures exploiting the evaluation horizon.
- The second-order kinetics connection is analogical, not rigorous. Present as "observation" in Discussion, not as a proven result.

