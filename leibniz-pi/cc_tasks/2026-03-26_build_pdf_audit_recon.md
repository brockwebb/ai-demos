# CC Task: Build PDF + Audit Reconnaissance

**Date:** 2026-03-26
**Priority:** High
**Depends on:** `2026-03-26_table_figure_captions.md` (run that first)

---

## Objective

1. Build the paper as a PDF via Quarto
2. Run mechanical consistency checks and report results
3. Query Seldon for cross-section relationships useful for audit

---

## Pre-Flight

1. Confirm the table/figure caption task has been completed (check that Section 05 has `**Table 3:**` etc.)
2. Read `paper/conventions.md`
3. Run `cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi && seldon paper sync`

---

## Step 1: Add Quarto PDF config

Create `/Users/brock/Documents/GitHub/ai-demos/leibniz-pi/paper/_quarto.yml` with:

```yaml
project:
  type: default

format:
  pdf:
    documentclass: article
    papersize: letter
    margin-left: 1in
    margin-right: 1in
    margin-top: 1in
    margin-bottom: 1in
    fontsize: 11pt
    linestretch: 1.15
    toc: true
    toc-depth: 3
    number-sections: true
    colorlinks: true
    bibliography: references.bib
    csl: https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl
  html:
    toc: true
    toc-depth: 3
    number-sections: true
    bibliography: references.bib
```

## Step 2: Build the PDF

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon paper sync
seldon paper build --no-render
cd paper
quarto render paper.qmd --to pdf
```

If quarto render fails due to LaTeX issues, try:
```bash
quarto render paper.qmd --to html
```
And note the error in the report.

Copy the output PDF to project root for easy access:
```bash
cp paper/paper.pdf ./leibniz-pi-draft.pdf 2>/dev/null || echo "PDF build failed, see errors above"
```

## Step 3: Run mechanical consistency checks

### 3a. Prose QC
```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
python paper/prose_qc.py
```
Report: number of violations, which sections, what kind.

### 3b. Glossary check
```bash
python paper/check_glossary.py
```
Report: any violations.

### 3c. Seldon result reference audit
Write and run a script that:
- Reads all `paper/sections/*.md` files
- Extracts every `{{result:NAME:value}}` pattern
- Lists all unique result names
- For each, runs `seldon result show NAME` to verify it resolves
- Reports any unresolved references

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi

# Extract all result references
grep -ohE '\{\{result:[^}]+\}\}' paper/sections/*.md | sort -u > /tmp/result_refs.txt
echo "=== All result references ==="
cat /tmp/result_refs.txt
echo ""
echo "=== Count ==="
wc -l /tmp/result_refs.txt

# Check each one resolves
while IFS= read -r ref; do
  name=$(echo "$ref" | sed 's/{{result:\(.*\):value}}/\1/')
  result=$(seldon result show "$name" 2>&1)
  if echo "$result" | grep -qi "error\|not found\|unknown"; then
    echo "UNRESOLVED: $name"
  fi
done < /tmp/result_refs.txt
```

### 3d. Cross-reference check
Write and run a script that checks all "Section X.Y" references in the prose resolve to actual section headers:

```bash
# Extract all section cross-references
grep -ohE 'Section [0-9]+\.[0-9]+' paper/sections/*.md | sort -u > /tmp/section_refs.txt
echo "=== All section cross-references ==="
cat /tmp/section_refs.txt

# Extract all actual section headers
grep -ohE '^#{1,3} [0-9]+\.[0-9]+' paper/sections/*.md | sed 's/^#* //' > /tmp/section_headers.txt
echo ""
echo "=== All section headers ==="
cat /tmp/section_headers.txt

# Find references to non-existent sections
echo ""
echo "=== Unresolved cross-references ==="
while IFS= read -r ref; do
  num=$(echo "$ref" | sed 's/Section //')
  if ! grep -q "^$num" /tmp/section_headers.txt; then
    echo "MISSING: $ref"
  fi
done < /tmp/section_refs.txt
```

### 3e. Citation cross-check
```bash
# All in-text citations (parenthetical and narrative)
grep -ohE '[A-Z][a-z]+ et al\.\s*\(?[0-9]{4}\)?' paper/sections/*.md | sort -u > /tmp/intext_cites.txt
grep -ohE '[A-Z][a-z]+ and [A-Z][a-z]+\s*\(?[0-9]{4}\)?' paper/sections/*.md | sort -u >> /tmp/intext_cites.txt
grep -ohE '[A-Z][a-z]+\s*\(?[0-9]{4}\)?' paper/sections/*.md | sort -u >> /tmp/intext_cites.txt

echo "=== In-text citations ==="
sort -u /tmp/intext_cites.txt

echo ""
echo "=== .bib keys ==="
grep -ohE '^@[a-z]+\{[^,]+' paper/references.bib | sed 's/@[a-z]*{//'

echo ""
echo "=== Manual check needed: verify each in-text citation has a .bib entry ==="
```

### 3f. Seldon graph query (cross-section relationships)
```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon artifact list 2>/dev/null || echo "seldon artifact list not available"
seldon task list --open 2>/dev/null || echo "seldon task list not available"
```

## Step 4: Write report

Create `audits/2026-03-26_build_recon_report.md` with:

1. PDF build status (success/failure, any warnings)
2. Prose QC results (violation count and details)
3. Glossary check results
4. Unresolved `{{result:...}}` references (if any)
5. Unresolved section cross-references (if any)
6. Citation cross-check results (in-text vs .bib mismatches)
7. Seldon artifact/task state
8. Any other issues discovered

---

## Post-Flight

1. Ensure `audits/` directory exists (create if needed)
2. Report file written to `audits/2026-03-26_build_recon_report.md`
3. PDF (if built) at `leibniz-pi-draft.pdf` in project root

---

## Do NOT

- Do not modify any prose content
- Do not fix any issues found — just report them
- Do not overwrite any existing CC task files
- Do not modify the caption task file
