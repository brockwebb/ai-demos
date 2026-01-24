# Handoff: AI Agents 101 Class Materials Development

**Date:** 2026-01-24  
**From:** Speaker notes development session  
**To:** Class materials development session

---

## What Exists

**Location:** `/Users/brock/Documents/GitHub/ai-demos/ai_agents_101/`

**Speaker Notes (Complete):**
```
chapters/
├── 00_front_matter.md      # Purpose, disclaimers
├── 01_exec_summary.md      # Core message, what you'll learn
├── 02_introduction.md      # Problem framing, Salesforce example, journey diagram
├── 03_vocabulary.md        # Workflow, agent, agency, agentic, The Loop, context, memory
├── 04_pipeline_basics.md   # Recipe workflow example with full prompt
├── 05_simple_script.md     # Prompt-as-script pattern, shadow IT reality
├── 06_case_study.md        # FSCM pipeline (dual-model, confidence routing, arbitration)
├── 07_design_principles.md # Six principles + quick reference cards
├── 08_tools_landscape.md   # Chat interfaces, APIs, frameworks, federal considerations
├── 09_resources.md         # Links, citations
├── 10_appendix_research.md # 2025-2026 research findings, source validation
├── 11_appendix_templates.md # Implementation templates (mission, process map, checklists)
```

**Key artifacts inside speaker notes:**
- Full recipe workflow prompt (ch 04) — copy-paste runnable
- Prompt-as-script template: ROLE / CONTEXT / WORKFLOW / TOOLS / OUTPUT / GUARDRAILS (ch 05)
- "Describing an Agent" fill-in-the-blank (ch 07)
- "Reviewing Agent Behavior" four questions (ch 07)
- Mermaid diagrams throughout (all verified working)

**Case study source code:** `github.com/brockwebb/federal-survey-concept-mapper`

---

## What the Speaker Notes Are

Source material for the instructor to draw from. More depth than any single session can cover. Not student-facing.

Reviewer feedback confirmed: "strong, coherent source material, exactly where someone should be before distillation."

---

## What We Need Now: Class Materials

Materials suited for students/learners. Things you can actually run a class with.

**Target format:** 1-hour webinar (40 min content, 10 min demo, 10 min Q&A)

**Instructor's stated plan:**
1. Concepts & terms (with repetition for retention)
2. One basic example (recipe workflow, live demo)
3. Light FSCM reference (gloss, not deep dive)
4. End on design principles

**What class materials might include:**
- Slide deck or visual outline (not text-heavy)
- Student handout (1-2 pages max, what they leave with)
- Demo script (what to show, what to say, where to pause)
- Discussion prompts or reflection questions
- Maybe: short exercises they can try during or after

**What class materials should NOT be:**
- The full speaker notes reformatted
- Text-heavy reference documents
- Anything requiring installation or technical setup (audience can't)

---

## Audience Constraints

- Federal/enterprise staff
- Cannot install software on work computers
- No API access, no dev environments
- May have personal Claude/ChatGPT accounts
- Need to evaluate and specify agent systems, not build production code
- Skeptical of hype, value defensibility and explainability

---

## Core Message to Preserve

**"Bounded agency beats autonomous agents."**

Supporting principles:
1. Design quality bounds output quality
2. Autonomy is governance, not upgrade
3. Most problems don't need agents
4. The skill is specification and recognition
5. Design for uncertainty
6. Break tasks into digestible chunks

---

## Differentiation from "Vibe Coding" Content

Ben's Bites / similar content: Gets non-technical people to try building with AI. Celebrates shipping, exploration, "autonomy high, let it rip."

This content: Teaches critical thinking about when and how to use agents. Emphasizes constraints, human oversight, knowing when NOT to use agents.

These are sequential, not opposed. We're writing the "here's when rigor matters" follow-up for people who've been introduced elsewhere.

---

## Suggested Approach for New Thread

1. Define deliverables explicitly (slide deck? handout? both?)
2. Decide what to cut vs. keep from speaker notes for student-facing materials
3. Create the distilled artifacts
4. Review for "can I actually teach from this?" quality

---

## Files to Reference

- Speaker notes: `/Users/brock/Documents/GitHub/ai-demos/ai_agents_101/chapters/`
- This handoff: `/Users/brock/Documents/GitHub/ai-demos/ai_agents_101/HANDOFF_2026-01-24_class_materials.md`
- Project docs in Claude project context (critical thinking workshop notes, research docs)

---

## Open Questions for New Thread

- Slide deck: PowerPoint/Google Slides, or something else?
- Student handout: PDF? Markdown they can print?
- Exercises: During session or take-home?
- Do you want a "facilitator guide" (what to say when) or just the materials?

---

*Ready for distillation.*
