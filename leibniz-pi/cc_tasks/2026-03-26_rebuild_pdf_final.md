# CC Task: Rebuild PDF With Formatting Fixes

**Date:** 2026-03-26
**Priority:** High
**Context:** _quarto.yml and 08_references.md were updated to fix three PDF issues: (1) remove TOC, (2) remove double section numbering, (3) fix empty references section. seldon paper sync has been run. This task just rebuilds.

---

## Pre-Flight

1. Verify `paper/_quarto.yml` has `toc: false` and `number-sections: false`
2. Verify `paper/sections/08_references.md` contains only `# References` (no `\bibliography` command)
3. Verify `paper/paper.qmd` does NOT contain `\bibliography{references}` anywhere

---

## Step 1: Build PDF

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi/paper
quarto render paper.qmd --to pdf
cp paper.pdf ../leibniz-pi-draft.pdf
echo "PDF built at leibniz-pi-draft.pdf"
```

If the build fails, capture the full error output and report it. Do not attempt fixes.

---

## Step 2: Verify the PDF

Open the PDF and confirm:
- [ ] No table of contents at the start
- [ ] Abstract is the first content after the title
- [ ] Section headers show "7. Conclusion" NOT "8 7. Conclusion" (no double numbering)
- [ ] References section at the end contains actual bibliography entries (not empty)
- [ ] Figures render in sections 5.2, 5.3, 5.4, and 6.1

Report results.

---

## Do NOT

- Do not modify any files. This task is build-only.
- Do not run seldon paper sync again (already done).
