# CC Task: Dogfood Seldon on leibniz-pi

**Date:** 2026-03-15
**Project:** ~/Documents/GitHub/ai-demos/leibniz-pi
**Seldon repo:** ~/Documents/GitHub/seldon

---

## What This Does

Initializes Seldon on the leibniz-pi research project and batch-registers all known artifacts (scripts, data files, results, paper sections, research tasks) with full provenance linking. Uses a Python bootstrap script that calls Seldon's internal API — no manual UUID copy-paste.

---

## Steps

### 1. Initialize the project

```bash
cd ~/Documents/GitHub/ai-demos/leibniz-pi
seldon init leibniz-pi
```

Verify: `seldon.yaml` exists, `seldon_events.jsonl` created, Neo4j database `seldon-leibniz-pi` online.

### 2. Run the bootstrap script

Copy `seldon_bootstrap.py` to the project root, then:

```bash
cd ~/Documents/GitHub/ai-demos/leibniz-pi
python seldon_bootstrap.py
```

This registers:
- 9 Script artifacts (entropy v3, GP v3, sensitivity sweep, stress test, fitness sensitivity, v2 confounded, RL, ACO)
- 6 DataFile artifacts (JSON data, CSVs, results summaries)
- 15 Result artifacts with provenance links (GENERATED_BY → Script, COMPUTED_FROM → DataFile)
- 7 PaperSection skeletons with CITES links to Results
- 11 ResearchTask artifacts with BLOCKS links to Results/PaperSections
- All results verified (proposed → verified state transition)

### 3. Validate

```bash
seldon briefing        # Does it surface useful session context?
seldon status          # Graph stats: ~48 artifacts, many relationships
seldon result list     # 15 results, all verified
seldon task list --open # 11 open research tasks
seldon result trace <any-result-uuid>   # Full provenance chain
seldon result check-stale               # Should be clean (nothing stale yet)
```

### 4. Closeout

```bash
seldon closeout
```

### 5. Git

Add to tracked files:
```bash
git add seldon.yaml seldon_events.jsonl seldon_bootstrap.py
```

Add to .gitignore:
```
.seldon/
```

---

## Dogfood Notes

Create `seldon_dogfood_notes.md` in project root. Document:
- Did `seldon briefing` tell you what you needed to know?
- What was friction? What was missing?
- Would name-based artifact lookup in the CLI be worth adding?
- Did the provenance chains make sense when traced?
- Any state machine transitions that felt wrong?

---

## If Something Breaks

The bootstrap script uses Seldon's internal Python API (`seldon.core.artifacts`, `seldon.config`). If it fails:

1. Check Neo4j is running: `curl -s http://localhost:7474` 
2. Check seldon is installed: `python -c "import seldon; print('ok')"`
3. Check `seldon.yaml` exists in cwd
4. Check the domain config path: `~/Documents/GitHub/seldon/seldon/domain/research.yaml`

If the state machine rejects a transition (e.g., `proposed → verified` not allowed for Result), check `research.yaml` state machine definitions. The Result state machine is: `proposed → [verified, rejected]`.
