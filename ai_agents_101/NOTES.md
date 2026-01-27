# Working Notes

Tracking decisions and rationale as we develop this handout.

## Main Ideas (to surface explicitly)

1. Without good judgment in upfront design, junk probability skyrockets
2. Autonomy is a governance choice, not a technical upgrade
3. Most problems don't need agents (and that's fine)
4. The skill is describing what you want and spotting bad design
5. Design for uncertainty:
   - Design for what goes wrong, not just what goes right
   - Build in checkpoints
   - Know when it should stop and ask

## Pedagogical Approach

- Three-pass repetition: vocab → basic example → script → case study
- Vocabulary in "pure" form first, nuance comes through examples
- 80% comprehension target for general audience
- Handout stands alone; talk is the launch event
- Material designed to be stolen and taught by others

## Constraints

- No employer mention
- No endorsements
- Living document disclaimer
- Shadow IT reality: most audience can't access proper tooling at work
- Avoid em-dash overuse
- No emojis

## Style

- Write like talking, but clean
- Grounded, not cheerleading or fear-mongering
- Permission to walk away if not for them
- Show limitations (some temporary, some fundamental)

## Open Questions

- (Add as they arise)

---

## HANDOFF: Lit Review Phase

After completing section drafts, conduct research phase:

### Process
1. Use Perplexity.ai to gather latest research and best practices on AI agents
2. Document findings with citations in an appendix
3. Cross-reference against our content

### Goals
1. **Alignment check:** Ensure content matches latest knowledge
2. **Level check:** Keep appropriate for beginners, show progression paths
3. **Gap analysis:** Find missing pieces worth adding
4. **Pruning candidates:** Identify content to cut or move to appendix

### Appendix Structure (to create)
- `10_appendix_research.md` - Lit review findings with citations
- Or multiple appendices if topics warrant separation

### Citation Format
- Include source, date accessed, key finding
- Note if finding supports, contradicts, or extends our content

---

## Section Status

| Section | Status | Notes |
|---------|--------|-------|
| 00_front_matter | Done | Disclaimers, about doc, acknowledgements |
| 01_exec_summary | Done | |
| 02_introduction | Done | Salesforce story, journey framing |
| 03_vocabulary | Done | Core terms + memory/context |
| 04_pipeline_basics | Done | Recipe workflow example |
| 05_simple_script | Done | Prompt-as-script approach |
| 06_case_study | Done | Federal Survey Concept Mapper |
| 07_design_principles | Done | Six principles + failure mode callouts |
| 08_tools_landscape | Done | Table, no endorsements |
| 09_resources | Done | Vendor guides + Microsoft failure modes paper |
| 10_appendix_research | Done | Lit review findings |
| 11_appendix_templates | Done | Copy-paste templates |
| 12_extended_glossary | Done | Full glossary with guardrails/fail-safes |

---

## Failure Mode Integration (January 2026)

Integrated Microsoft AI Red Team "Taxonomy of Failure Modes in Agentic AI Systems" throughout materials.

**Key insight (from Tam Nguyen's feedback):** The failure modes list is essentially "what happens when you ignore the design principles" — framed that way, not as fear-mongering.

### Changes Made

**Chapter 07 (Design Principles):**
- Added "What ignoring this causes" callouts after each of 6 principles
- Added "The Stakes: What These Principles Prevent" summary section
- Maps principle violations → specific failure modes from Microsoft taxonomy

**Chapter 09 (Resources):**
- Added Microsoft paper under new "What Can Go Wrong: Failure Mode Analysis" subsection

**Chapter 12 (Glossary):**
- Expanded Guardrails entry to include fail-safes and circuit breakers
- "Fail-safe" = general engineering concept (fails in safe state)
- "Circuit breaker" = emerging AI agent terminology (confirmed by Forbes, AccuKnox, practitioners)
- "Control flow control" = Microsoft's term, noted but not oversold

**Chapter 00 (Front Matter):**
- Added Acknowledgements section
- Credits Tam Nguyen for feedback including circuit breaker terminology

**Slides (slides.md, slides_full.md):**
- New "The Stakes: What Ignoring These Causes" slide after Design Principles
- Updated Resources slide with Microsoft paper + vendor guides
- slides_full.md: new Guardrails/Fail-safes backup slide

**Student Handout:**
- Added stakes paragraph after Design Principles table
- Added Further Reading section

**Facilitator Guide:**
- Added Microsoft paper to recommended prep reading
- Updated timing guides to reference Stakes slide
- Added Q&A: "What are the biggest risks with AI agents?"
- Added Q&A: "What's a circuit breaker?"

### Terminology Decisions

- **Fail-safe** = primary term (accurate, universal engineering concept)
- **Circuit breaker** = introduced as emerging AI agent term with real adoption
- **Control flow control** = Microsoft's term, mentioned for completeness
- Did NOT invent terminology — traced origins honestly

### Source

Microsoft AI Red Team, "Taxonomy of Failure Modes in Agentic AI Systems" (2025)  
https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf

