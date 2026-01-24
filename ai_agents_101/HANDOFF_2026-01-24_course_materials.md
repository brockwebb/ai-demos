# Handoff: AI Agents 101 Course Materials Development

**Date:** 2026-01-24  
**From:** Speaker notes development session  
**To:** Course materials creation session

---

## What Exists

**Location:** `/Users/brock/Documents/GitHub/ai-demos/ai_agents_101/`

**Speaker Notes (complete):**
```
chapters/
├── 00_front_matter.md      # Purpose, disclaimers
├── 01_exec_summary.md      # Core message, what you'll learn
├── 02_introduction.md      # Problem framing, Salesforce example, journey map
├── 03_vocabulary.md        # Workflow, agent, agency, agentic, tools, context, memory, The Loop
├── 04_pipeline_basics.md   # Recipe workflow example with full prompt
├── 05_simple_script.md     # Prompt-as-script pattern, portable template
├── 06_case_study.md        # FSCM: dual-model, confidence routing, bounded agency at scale
├── 07_design_principles.md # 6 principles + quick reference cards for describing/reviewing agents
├── 08_tools_landscape.md   # Chat interfaces, APIs, frameworks, no-code, federal considerations
├── 09_resources.md         # Links, citations
├── 10_appendix_research.md # 2025-2026 research validation (cleaned sources)
├── 11_appendix_templates.md # Implementation templates for practitioners
```

**Key artifacts within the notes:**
- Mermaid diagrams throughout (all validated, rendering correctly)
- Copy-paste ready recipe prompt (chapter 04)
- Prompt-as-script template: ROLE/CONTEXT/WORKFLOW/TOOLS/OUTPUT/GUARDRAILS (chapter 05)
- "Describing an Agent" fill-in-the-blank template (chapter 07)
- "Reviewing Agent Behavior" 4-question checklist (chapter 07)
- Full implementation templates (appendix 11)

**Related project files:**
- FSCM case study source: `/Users/brock/Documents/GitHub/federal-survey-concept-mapper`
- Build script: `build.sh` (concatenates chapters into handout.md)

---

## What the Speaker Notes Are

Source material for the instructor. Contains more depth than any single session can cover. Organized for selective use—not meant to be delivered linearly or in full.

**Validated against 2025-2026 research.** Core claims align with industry consensus:
- Bounded agency over autonomous agents
- Confidence thresholds for human routing (0.7-0.9 range)
- Risk-tiered autonomy
- "Start at lowest sophistication that solves the problem"
- Workflow-first design
- Teaching specification skills over framework mechanics

---

## What Needs to Be Created

**Course materials for a 40-60 minute webinar.** These are student-facing, not instructor-facing.

Brock's stated delivery plan:
1. Concepts & terms (with repetition)
2. One basic example (recipe workflow, live demo)
3. Light FSCM reference (gloss over, not deep dive)
4. End on design principles

### Suggested deliverables:

**1. Slide deck or visual outline**
- Not a wall of text
- Key concepts with visuals
- Prompts for live demo moments
- ~15-20 slides max for 40 min content

**2. Student handout (1-2 pages)**
- Vocabulary quick reference
- The Loop diagram
- "Describing an Agent" template
- "Reviewing Agent Behavior" checklist
- Maybe: the 6 principles as one-liners

**3. Exercise prompts (optional but useful)**
- 2-3 prompts students can run themselves post-session
- Tied to the recipe example or a work-relevant variant

**4. Facilitator guide (optional)**
- Timing for each section
- Where to pause for Q&A
- What to skip if running short

---

## Constraints to Remember

**Audience:**
- Federal and enterprise staff
- Non-technical or semi-technical
- Cannot install software on work computers
- May have personal Claude/ChatGPT accounts
- Need to make governance decisions, not ship code
- Skeptical of hype, want practical grounding

**Tone:**
- Blunt, cuts through hype
- Not dismissive of technology, but appropriately skeptical
- Emphasizes constraints and bounded agency
- "Would I sign my name under this action?"

**What this is NOT:**
- Not teaching people to vibe-code or ship fast
- Not celebrating autonomy or "let it rip"
- Not a Ben's Bites style "you can build anything" pitch
- It's the corrective: when constraints matter, how to think critically

---

## Context from This Session

**Key decisions made:**
- Renamed document to "Speaker Notes & Reference Material" (not standalone course)
- Fixed broken Mermaid diagram in chapter 02
- Cleaned weak sources from research appendix (removed SEO blogs, kept institutional/practitioner sources)
- Added "When Frameworks Earn Their Place" section to chapter 05 (balanced, not dismissive)
- Integrated quick reference cards into chapter 07 (Handout A & B from Perplexity research)

**Feedback received (via ChatGPT evaluation):**
- Strong content and voice, usable as handout
- Needs tightening for course delivery
- Too long for handout, too unstructured for standalone course
- Works well as source material for instructor to draw from
- Delivery plan aligns with what's written

**Positioning relative to other content:**
- Ben's Bites "Become Technical in 1 Day" = getting non-technical people to try building with AI agents
- This material = what comes next, when stakes get higher and constraints matter
- Sequential, not opposed—but different audience, different goals

---

## Suggested Starting Point for New Thread

> I have completed speaker notes for a 40-60 minute AI agents webinar. The source material is at `/Users/brock/Documents/GitHub/ai-demos/ai_agents_101/`. 
>
> Now I need to create actual course materials: a concise student handout, and optionally a slide outline or facilitator guide.
>
> My delivery plan: concepts/terms with repetition → one live demo (recipe workflow) → light FSCM case study reference → end on design principles.
>
> Audience: federal/enterprise, non-technical, can't install software, need governance/evaluation skills not coding skills. Tone: blunt, skeptical of hype, emphasizes bounded agency and constraints.
>
> Please review the speaker notes and help me distill them into student-facing materials.

---

## Files to Reference

Essential reading for new thread:
- `chapters/03_vocabulary.md` (terms)
- `chapters/04_pipeline_basics.md` (demo prompt)
- `chapters/07_design_principles.md` (principles + quick reference cards)

Skim for context:
- `chapters/01_exec_summary.md`
- `chapters/06_case_study.md`

Can skip unless needed:
- Appendices (10, 11) — practitioner reference, not student-facing
- `chapters/08_tools_landscape.md` — awareness only, probably not in live delivery
