# CLAUDE.md — AI Agents 101

## Project Overview

Training materials for a 40-60 minute course: "AI Agents 101: Bounded Agency Over Autonomous Agents."
Target audience: federal statisticians, data scientists, evaluators/decision-makers (not builders).

## Folder Structure

```
docs/                        # Readable markdown (browse on GitHub)
  student_handout.md
  exercises.md
  facilitator_guide.md
  course_notes/              # 12 chapters of speaker notes
    00_front_matter.md ... 12_extended_glossary.md

slides/                      # Presentation
  slides.md                  # Browsable on GitHub
  slides.qmd                 # Quarto revealjs source (for building)

pdf/                         # Built PDFs (committed, downloadable)
  student_handout.pdf
  exercises.pdf
  facilitator_guide.pdf
  slides.pdf
  AI-Agents-101.pdf

img/                         # Rendered diagram PNGs
diagrams/                    # Mermaid source (.mmd)
scripts/                     # Build tooling
notes/                       # Development notes, drafts (gitignored)
```

## Build System

```bash
./scripts/build.sh all        # Everything
./scripts/build.sh book       # Course notes PDF via Quarto book
./scripts/build.sh slides     # Slides via Quarto revealjs
./scripts/build.sh handouts   # Handout PDFs
./scripts/build.sh diagrams   # Mermaid → PNG
./scripts/build.sh clean      # Remove scattered artifacts
```

Dependencies: quarto, @mermaid-js/mermaid-cli (npm global)

## Key Files at Root (build infrastructure — not user-facing)
- `_quarto.yml` — Quarto book config, points to docs/course_notes/ chapters
- `index.qmd` — Book preface/front matter

## Notes and Drafts
All development notes, draft ideas, and temporary content go in the `notes/` folder (gitignored).

## Content Conventions
- No employer mentions, no endorsements, no emojis
- Write like talking, but clean
- Grounded tone — not cheerleading or fear-mongering
- Minimize em-dash usage

## Edit Workflow
1. Edit source .md files in docs/ and docs/course_notes/
2. Edit slides in slides/slides.qmd (or slides/slides.md for browsable version)
3. Run ./scripts/build.sh all
4. Commit both source and pdf/ changes
