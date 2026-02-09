# AI Agents 101

**Bounded agency over autonomous agents.**

A practical course for teams evaluating AI agents — common vocabulary, working examples, and design principles that cut through the hype.

---

## 📖 Read Online (Markdown)

Click any link to read on GitHub:

| Document | Description |
|----------|-------------|
| [Student Handout](docs/student_handout.md) | Vocabulary, templates, checklists, copy-paste recipe prompt |
| [Exercises](docs/exercises.md) | Post-session practice — try it yourself |
| [Facilitator Guide](docs/facilitator_guide.md) | Timing, tips, audience adaptations, common Q&A |
| [Slides](slides/slides.md) | Presentation deck (Markdown source) |

**Full course notes** (speaker prep — 12 chapters): [docs/course_notes/](docs/course_notes/)

| Chapter | Topic |
|---------|-------|
| [01](docs/course_notes/01_exec_summary.md) | Executive Summary |
| [02](docs/course_notes/02_introduction.md) | Introduction |
| [03](docs/course_notes/03_vocabulary.md) | Vocabulary |
| [04](docs/course_notes/04_pipeline_basics.md) | Pipeline Basics |
| [05](docs/course_notes/05_simple_script.md) | Simple Script |
| [06](docs/course_notes/06_case_study.md) | Case Study |
| [07](docs/course_notes/07_design_principles.md) | Design Principles |
| [08](docs/course_notes/08_tools_landscape.md) | Tools Landscape |
| [09](docs/course_notes/09_resources.md) | Resources |
| [10](docs/course_notes/10_appendix_research.md) | Appendix: Research |
| [11](docs/course_notes/11_appendix_templates.md) | Appendix: Templates |
| [12](docs/course_notes/12_extended_glossary.md) | Appendix: Glossary |

---

## 📥 Download PDFs

Built PDFs are in the **[pdf/](pdf/)** folder:

| File | Contents |
|------|----------|
| `student_handout.pdf` | Quick reference for attendees |
| `exercises.pdf` | Practice prompts |
| `facilitator_guide.pdf` | Teaching guide |
| `slides.pdf` | Presentation slides |
| `AI-Agents-101.pdf` | Full course notes (all chapters) |

---

## Quick Paths

**Just want to learn?** Read the [student handout](docs/student_handout.md), then try the [exercises](docs/exercises.md).

**Want to teach it?** Read the [facilitator guide](docs/facilitator_guide.md). Present with the slides. Distribute the handout and exercises.

**Want to adapt?** Edit files in `docs/` and `slides/`, then rebuild. No permission needed.

---

## What This Course Covers

- Shared vocabulary: workflow, agent, agency, agentic, tool
- The Observe → Decide → Act → Check loop
- Live demo: a recipe workflow prompt with bounded agency
- Case study: 6,987 survey questions classified at 99.5% accuracy for ~$15
- Six design principles for evaluating agent systems
- What goes wrong when you ignore them (Microsoft AI Red Team failure modes)

**Who it's for:** Anyone making decisions about AI agents — technical or not. No coding required.

**Core message:** Start simple. Add complexity only when justified. Design for uncertainty. Keep humans in the loop where it matters.

---

## Building from Source

### Requirements

- [Quarto](https://quarto.org)
- `npm install -g @mermaid-js/mermaid-cli`

### Commands

```bash
chmod +x scripts/build.sh
./scripts/build.sh all        # Everything
./scripts/build.sh book       # Course notes PDF
./scripts/build.sh slides     # Slide deck
./scripts/build.sh handouts   # Handout PDFs
./scripts/build.sh diagrams   # Mermaid → PNG
```

---

## Case Study

References the Multi-Survey Concept Mapper — a real project that classified 6,987 survey questions using dual-model cross-validation, confidence-based routing, and human review flags.

Code: [github.com/brockwebb/federal-survey-concept-mapper](https://github.com/brockwebb/federal-survey-concept-mapper)

---

## License

MIT — adapt, teach, share. Attribution appreciated but not required.

*Views are the author's own. Product/company names are not endorsements. This is a living document.*
