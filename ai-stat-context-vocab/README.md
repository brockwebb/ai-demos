# FSS AI Context Vocabulary

A plain-language, authoritatively-sourced glossary of **artificial-intelligence terms for the U.S. Federal Statistical System (FSS)** — and a small demonstration of what a purpose-built knowledge graph can do.

## What this is

This vocabulary is a **demonstration artifact**. It came out of a larger knowledge graph (KG) I built over a substantial corpus of documents relevant to the federal statistical system — statutes, OMB directives and AI memoranda, executive orders, NIST frameworks, FCSM and CNSTAT methodology, Census quality standards, and more. The KG was built for a paper I'm working on; this 42-term vocabulary was simply a **test case to prove out the graph's utility** — to show that the corpus could ground a real, useful work product, with every claim traceable back to source documents.

It turned out useful enough to share on its own.

## Why you might want it

It's designed to be **handed to an LLM as context** when you're using AI tools to work with federal-statistical material — reviewing documents, drafting, or evaluating AI use cases "with an AI lens." Drop `fss_ai_vocabulary.json` into the model's context window and it gains:

- **Authoritative, FSS-contextualized AI definitions** — so the model isn't guessing what "data asset," "inference," or "differential privacy" means in *this* world.
- **Two honest layers per term.** Layer 1 is the official definition with its source; Layer 2 is what the term means *inside* the FSS — and that second layer is **typed**, so the model (and you) can tell the difference between *"the corpus says so, here's the cited document"* and *"a practitioner's best read."*
- **False-friend flags** for the terms that mean something different in AI than in FSS practice (e.g. *inference*, *bias*, *validity*, *data asset*) — the highest-value entries.

`fss_ai_vocabulary.pdf` is the human-readable version: a clean, scannable reference for a reader who is expert in federal statistics but new to AI.

## Files

| file | for |
|------|-----|
| `fss_ai_vocabulary.json` | machines — drop into an LLM context window, or parse programmatically |
| `fss_ai_vocabulary.pdf` | humans — a designed, readable reference document |

## Sourcing

Every definition comes from a **public, freely-accessible source** — U.S. federal (NIST, statutes, OMB), the NIST AIRC "Language of Trustworthy AI" glossary, the U.S. Census Bureau Statistical Quality Standards, or open references where no federal definition exists. **No paywalled sources.** Where there is no U.S.-federal definition of a term, the record says so rather than dressing up another source as federal. The FSS context layer is grounded against the knowledge graph, with the specific source documents cited.

## License

This work is licensed under a **Creative Commons Attribution 4.0 International License (CC BY 4.0)**. You are free to share and adapt it for any purpose, including commercially, as long as you give appropriate credit. See `LICENSE` or <https://creativecommons.org/licenses/by/4.0/>.

**Attribution:** Brock Webb, *FSS AI Context Vocabulary* (2026), CC BY 4.0.

## Disclaimer

The views expressed are the author's own and do not necessarily represent the views of the U.S. Census Bureau or the U.S. Department of Commerce. AI writing and research tools were used in the preparation of this work.
