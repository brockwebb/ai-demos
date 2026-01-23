# AI Agents 101

A practical guide to understanding AI agents, agentic behavior, and design considerations — aimed at establishing common vocabulary and cutting through hype.

## Quick Start

**Just want to read it?**  
Download `handout.md` or `handout.pdf` from this repo.

**Want to contribute or adapt?**  
Edit the files in `chapters/`, then run the build script.

## Project Structure

```
ai_agents_101/
├── README.md           # You are here
├── NOTES.md            # Working notes, decisions, constraints
├── build.sh            # Assembles chapters into handout.md
├── handout.md          # GENERATED - do not edit directly
├── handout.pdf         # GENERATED - do not edit directly
└── chapters/
    ├── 00_front_matter.md
    ├── 01_exec_summary.md
    ├── 02_introduction.md
    ├── 03_vocabulary.md
    ├── 04_pipeline_basics.md
    ├── 05_simple_script.md
    ├── 06_case_study.md
    ├── 07_design_principles.md
    ├── 08_tools_landscape.md
    ├── 09_resources.md
    └── img/              # Images and diagrams
```

## Building the Handout

### Requirements
- Bash shell
- (Optional) Pandoc or similar for PDF generation

### Build Markdown

```bash
chmod +x build.sh
./build.sh
```

This concatenates all chapter files into `handout.md`.

### Build PDF

If you have Pandoc installed:

```bash
pandoc handout.md -o handout.pdf
```

Or use any Markdown-to-PDF tool of your choice.

## ⚠️ Important: Edit Chapters, Not Output

The `handout.md` and `handout.pdf` files are **generated artifacts**.

- ✅ Edit files in `chapters/`
- ❌ Do not edit `handout.md` directly

If you edit `handout.md` and then run `build.sh`, **your changes will be overwritten**.

## Adapting This Material

This material is designed to be shared and taught. Feel free to:

- Fork this repo
- Adapt content for your audience
- Use it in your own presentations
- Teach from it

Attribution appreciated but not required.

## Disclaimers

- This is a living document, subject to revision
- Views expressed are the author's own
- Product/company names are not endorsements
- No organizational affiliation implied

See `chapters/00_front_matter.md` for full disclaimers.

## License

MIT — See [LICENSE](../LICENSE) in parent repo.
