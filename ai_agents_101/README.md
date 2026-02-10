# AI Agents 101: Bounded Agency Over Autonomous Agents

Practical guidance for teams navigating AI agent hype. This course establishes common vocabulary, demonstrates progressive complexity from simple prompts to bounded agents, and teaches design principles for responsible agent deployment.

*The views expressed are the author's own and do not necessarily represent the views of the U.S. Census Bureau or the U.S. Department of Commerce.*

---

## 📖 Read Online (Markdown)

| Document | Description |
|----------|-------------|
| [Course Companion (chapter index)](docs/course_companion_index.md) | Full course material — 12 chapters covering vocabulary, examples, design principles, and templates |
| [Student Handout](docs/student_handout.md) | One-page quick reference for attendees |
| [Exercises](docs/exercises.md) | Hands-on exercises using any chat interface |
| [Facilitator Guide](docs/facilitator_guide.md) | Notes for instructors adapting this material |
| [Slides](slides/slides.md) | Presentation deck (browsable markdown) |

## 📥 Download PDFs

| Document | File |
|----------|------|
| Course Companion | [AI-Agents-101_course-companion.pdf](pdf/AI-Agents-101_course-companion.pdf) |
| Student Handout | [student_handout.pdf](pdf/student_handout.pdf) |
| Exercises | [exercises.pdf](pdf/exercises.pdf) |
| Facilitator Guide | [facilitator_guide.pdf](pdf/facilitator_guide.pdf) |
| Slides | [slides.pdf](pdf/slides.pdf) |

---

## Building from Source

Requires [Quarto](https://quarto.org) and [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) (`npm install -g @mermaid-js/mermaid-cli`).

```bash
./scripts/build.sh all      # Build everything
./scripts/build.sh diagrams # Just render diagrams
./scripts/build.sh book     # Course companion PDF
./scripts/build.sh slides   # Revealjs HTML
./scripts/build.sh handouts # Handout PDFs
```

## Repository Structure

```
docs/                           # Read on GitHub
  course_companion_index.md     # Chapter index
  course_companion/             # 12 chapters (00–12)
  student_handout.md
  exercises.md
  facilitator_guide.md

slides/                         # Presentation
  slides.md                     # Browsable
  slides.qmd                    # Build source

pdf/                            # Download (committed)
  AI-Agents-101_course-companion.pdf
  student_handout.pdf
  exercises.pdf
  facilitator_guide.pdf
  slides.pdf

diagrams/                       # Mermaid sources (.mmd)
img/                            # Rendered diagram PNGs
scripts/                        # Build tooling
```
