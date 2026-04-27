# CC Task: Rebuild PDF After Formatting Fixes

**Date:** 2026-03-26
**Priority:** High

---

## Objective

Rebuild the PDF after _quarto.yml and references section fixes applied by Claude Desktop.

---

## Pre-Flight

1. Verify `paper/_quarto.yml` has `toc: false` and `number-sections: false`
2. Verify `paper/sections/08_references.md` contains only `# References` with no `\bibliography` command

---

## Step 1: Sync and build

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon paper sync
seldon paper build --no-render
cd paper
quarto render paper.qmd --to pdf
cp paper.pdf ../leibniz-pi-draft.pdf
echo "PDF rebuilt at leibniz-pi-draft.pdf"
```

## Step 2: Verify

Check the PDF:
- No table of contents at the start
- No double section numbering (should show "7. Conclusion" not "8 7. Conclusion")
- References section populated with actual bibliography entries
- Abstract appears as the first content

If references are still empty, check whether `paper.qmd` still contains `\bibliography{references}` after sync. If so, that line needs to be removed from `paper.qmd` manually after sync:

```bash
sed -i '' '/\\bibliography{references}/d' paper/paper.qmd
quarto render paper/paper.qmd --to pdf
cp paper/paper.pdf leibniz-pi-draft.pdf
```

---

## Do NOT

- Do not modify any prose content
- Do not modify any section files other than what's already been changed
