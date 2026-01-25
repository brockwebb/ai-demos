# AI Agents 101

**Bounded agency over autonomous agents.**

A practical course for teams evaluating AI agents — common vocabulary, working examples, and design principles that cut through the hype.

---

## What This Is

A 40-60 minute course that teaches:
- Shared vocabulary (workflow, agent, agency, agentic)
- The Observe-Decide-Act-Check loop
- How to specify and evaluate agent behavior
- When agents help vs. when they're overkill

**Who it's for:** Anyone making decisions about AI agents — technical or not. No coding required.

**What it's not:** A framework tutorial. A "build fast and ship" guide. A celebration of autonomy.

---

## Course Materials

| File | What It Is | Who Uses It |
|------|------------|-------------|
| `student_handout.md` | Quick reference: vocab, templates, checklists | Attendees |
| `slides.md` / `slides.pdf` | Presentation deck (Marp format) | Presenter |
| `exercises.md` | Post-session practice prompts | Attendees |
| `facilitator_guide.md` | Timing, tips, common questions | Anyone teaching this |
| `course_notes.md` | Full speaker notes and reference | Presenter prep |

### Want to teach this at your org?

Go for it. The facilitator guide has timing, tips, and audience adaptations. No permission needed.

---

## Quick Start

**Just want to learn?**
- Read `student_handout.md` for the essentials
- Try the prompts in `exercises.md`

**Want to teach it?**
- Read `facilitator_guide.md` for timing and tips
- Use `slides.pdf` for presentation
- Reference `course_notes.md` for depth

**Want to adapt or contribute?**
- Edit files in `chapters/`
- Run build scripts to regenerate outputs

---

## Project Structure

```
ai_agents_101/
├── README.md                # You are here
├── student_handout.md       # Quick reference for attendees
├── slides.md                # Marp presentation source
├── slides.pdf               # GENERATED presentation
├── exercises.md             # Post-session practice
├── facilitator_guide.md     # Teaching guide
├── course_notes.md          # GENERATED full speaker notes
│
├── chapters/                # Source material (edit these)
│   ├── 00_front_matter.md
│   ├── 01_exec_summary.md
│   ├── 02_introduction.md
│   ├── 03_vocabulary.md
│   ├── 04_pipeline_basics.md
│   ├── 05_simple_script.md
│   ├── 06_case_study.md
│   ├── 07_design_principles.md
│   ├── 08_tools_landscape.md
│   ├── 09_resources.md
│   ├── 10_appendix_research.md
│   └── 11_appendix_templates.md
│
├── diagrams/                # Mermaid source files (.mmd)
├── img/                     # GENERATED diagram images
│
└── scripts/
    ├── build_materials.py   # Main build script
    ├── cleanup.py           # Remove deprecated files
    ├── pdf-config.json      # PDF generation config
    └── pdf-style.css        # PDF styling
```

---

## Building Outputs

### Requirements

```bash
npm install -g @mermaid-js/mermaid-cli   # mmdc - diagram rendering
npm install -g @marp-team/marp-cli       # marp - slide generation
npm install -g md-to-pdf                 # markdown to PDF
```

### Build Commands

```bash
# Build everything
python scripts/build_materials.py --all

# Or build selectively:
python scripts/build_materials.py --slides     # Diagrams + slides.pdf
python scripts/build_materials.py --notes      # course_notes.md + PDF
python scripts/build_materials.py --handouts   # student_handout.pdf, exercises.pdf, facilitator_guide.pdf
python scripts/build_materials.py --diagrams   # Just render Mermaid diagrams
```

### ⚠️ Edit Sources, Not Outputs

- ✅ Edit files in `chapters/` and `diagrams/`
- ❌ Don't edit `course_notes.md`, `slides.pdf`, or `img/` directly

Generated files get overwritten on rebuild.

---

## The Core Idea

The hype says: autonomous agents will handle everything.

The reality: production systems treat agents as bounded, auditable components with explicit constraints, confidence thresholds, and human oversight.

This course teaches the reality.

---

## Case Study

The course references the Multi-Survey Concept Mapper — a real project that classified 6,987 survey questions using dual-model cross-validation, confidence-based routing, and human review flags.

Code: [github.com/brockwebb/federal-survey-concept-mapper](https://github.com/brockwebb/federal-survey-concept-mapper)

---

## License

MIT — adapt, teach, share. Attribution appreciated but not required.

---

## Disclaimers

- Views are the author's own
- Product/company names are not endorsements
- This is a living document

See `chapters/00_front_matter.md` for full disclaimers.
