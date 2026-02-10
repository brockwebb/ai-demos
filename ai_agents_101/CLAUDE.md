# CLAUDE.md — AI Agents 101

## Project Overview

Training materials for a 40-60 minute course: "AI Agents 101: Bounded Agency Over Autonomous Agents."
Target audience: federal statisticians, data scientists, evaluators/decision-makers (not builders).

## Folder Structure

```
docs/                            # Readable markdown (browse on GitHub)
  course_companion_index.md      # Chapter index for course companion
  course_companion/              # 12 chapters (00–12)
  student_handout.md
  exercises.md
  facilitator_guide.md

slides/                          # Presentation
  slides.md                      # Browsable on GitHub
  slides.qmd                     # Quarto revealjs source (for building)

pdf/                             # Built PDFs (committed, downloadable)
  AI-Agents-101_course-companion.pdf
  student_handout.pdf
  exercises.pdf
  facilitator_guide.pdf
  slides.pdf

img/                             # Rendered diagram PNGs
diagrams/                        # Mermaid source (.mmd)
scripts/                         # Build tooling
notes/                           # Development notes, drafts (gitignored)
```

## Build System

```bash
python scripts/build.py all        # Everything
python scripts/build.py book       # Course companion PDF via Quarto book
python scripts/build.py slides     # Slides PDF (Beamer) + revealjs HTML
python scripts/build.py handouts   # Handout PDFs
python scripts/build.py diagrams   # Mermaid → PNG
python scripts/build.py clean      # Remove scattered artifacts
```

Dependencies: Python 3, quarto, @mermaid-js/mermaid-cli (npm global), LaTeX with Beamer

## Key Files at Root (build infrastructure — not user-facing)
- `_quarto.yml` — Quarto book config, points to docs/course_companion/ chapters
- `index.qmd` — Book preface/front matter

## Disclaimer
All deliverables include:
"The views expressed are the author's own and do not necessarily represent the views of the U.S. Census Bureau or the U.S. Department of Commerce."

## Content Conventions
- No employer mentions, no endorsements, no emojis
- Write like talking, but clean
- Grounded tone — not cheerleading or fear-mongering
- Minimize em-dash usage

## Edit Workflow
1. Edit source .md files in docs/ and docs/course_companion/
2. Edit slides in slides/slides.qmd (or slides/slides.md for browsable version)
3. Run ./scripts/build.sh all
4. Commit both source and pdf/ changes
