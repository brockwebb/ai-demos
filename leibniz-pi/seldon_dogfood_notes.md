# Seldon Dogfood Notes — leibniz-pi (2026-03-15)

## Friction Points

### 1. Auth credential mismatch
**Problem:** Seldon reads `NEO4J_USERNAME` / `NEO4J_PASSWORD` but the existing env vars in this environment are `NEO4J_USER` / `NEO4J_PASS`. The init command silently "succeeded" (created files) but failed Neo4j setup, requiring manual database creation via Python.

**Fix suggestion:** Check both `NEO4J_USER`/`NEO4J_USERNAME` and `NEO4J_PASS`/`NEO4J_PASSWORD` with fallback, or emit a clearer diagnostic pointing to the exact env var names.

### 2. `seldon link create` syntax: positional, not flags
**Problem:** The task doc specified `--from <uuid> --to <uuid> --rel-type <type>` but the actual CLI signature is positional: `seldon link create FROM_ID REL_TYPE TO_ID`.

**Fix suggestion:** Update docs / add `--from`/`--to`/`--rel-type` as aliases.

### 3. `seldon closeout` session window is narrow
**Problem:** `closeout` only counts artifacts created *since the preceding `briefing`*. Running `briefing` near the end of a session (as a verification step) means closeout sees 0 artifacts created — even though 43 were created earlier in the session.

**Fix suggestion:** Either track session start at `init` / first command, or let closeout accept a `--since <timestamp>` flag.

### 4. Graph warnings on empty database
**Minor:** Innocuous `UNRECOGNIZED` GQL warnings from Neo4j on queries against empty labels/properties. Not harmful but noisy in terminal output.

**Fix suggestion:** Suppress or downgrade these to debug-level.

### 5. Result `--script-id` requires UUID, not path
**Problem:** UUID copy-paste workflow is tedious when registering results sequentially. If the script path is already registered, it would be more natural to say `--script-path entropy-leibniz-v3/entropy_leibniz_v3_minimal.py`.

**Fix suggestion:** Add `--script-path` as an alternative to `--script-id` that resolves by artifact path property.

## What Worked Well

- `seldon result verify <uuid>` is clean and clear
- `seldon result trace <uuid>` shows the full upstream provenance chain immediately
- `seldon briefing` output is exactly the right shape — open tasks + stale results + incomplete provenance at a glance
- `seldon status` artifact-by-type breakdown is useful for sanity-checking registrations
- JSONL event log gives full audit trail without extra overhead
- `seldon task create` is zero-friction for capturing research threads

## Key Question: Would briefing have prevented problems on this project?

**Yes, specifically:** The injection confound (v2 results being artifacts of Leibniz injection) was discovered only after running experiments that failed to replicate. If the v2 "5/5" results had been registered in Seldon with `--script-id` pointing to the injection-containing script, a future briefing would have surfaced the incomplete provenance on the v3 runs and prompted earlier scrutiny of what changed.
