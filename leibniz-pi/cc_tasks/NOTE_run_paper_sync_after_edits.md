# Editing Workflow Note: Paper Sync Required

**Date:** 2026-03-17

After any CC task that modifies paper section files (`paper/sections/*.md`) or renames/updates Result artifacts referenced by sections, you must run:

```bash
cd /Users/brock/Documents/GitHub/ai-demos/leibniz-pi
seldon paper sync
```

This reconciles the graph with your edits: updates content hashes, adds/removes `cites` edges for changed `{{result:...}}` references, and transitions modified sections to `stale` if they were in `review` or `published` state.

The full loop is: **edit → sync → build**.

If a task registers new Result artifacts that sections reference, or renames existing ones (like the `entropy_*` → `logprec_*` rename), the sync must follow to keep edges correct.

`seldon paper sync --dry-run` to preview changes without writing.
