# Claude Code Task: Entropy Stress Test — Push the Terminal Set

## Context
Entropy v3 minimal found Leibniz 5/5 with {k, 1, -1, 2}, no injection. Completion times ranged from 21s to 153s per seed (~370s total). The information-theoretic fitness creates a strong enough gradient to discover Leibniz from scratch.

Now we want to know: how far can we push it? Can entropy fitness find Leibniz with larger, less favorable terminal sets? The 0/5 failures on wide (41 terminals) and hostile (40 terminals, no 2) were with the old 55s/seed budget. The minimal run proves 360s/seed is enough for 4 terminals. What about bigger sets?

## What to Do
Run a series of entropy experiments with progressively harder terminal configurations. All use the entropy fitness function, no injection, MAX_SEED=360s.

### Configurations to test (in order of increasing difficulty):

**Level 1: Moderate pool**
- `TERM_FIXED = ["k", 1, -1, 2]`
- `EPHEMERALS = list(range(-5, 6))` — this is the original v2 ephemeral range
- 15 total terminals. This is the v2 terminal set but without injection.

**Level 2: Wide pool (retry with longer budget)**
- `TERM_FIXED = ["k", 1]`
- `EPHEMERALS = list(range(-20, 21))`
- 42 total terminals. This failed 0/5 at 55s/seed. Does 360s/seed fix it?

**Level 3: Hostile pool (retry with longer budget)**
- `TERM_FIXED = ["k", 1, 3, -1]`
- `EPHEMERALS = [x for x in range(-20, 21) if x != 2]`
- 44 total terminals, no 2 available. Must manufacture it.

**Level 4: Extreme hostile — no 2, no -1**
- `TERM_FIXED = ["k", 1]`
- `EPHEMERALS = [x for x in range(-20, 21) if x not in (2, -1)]`
- Must manufacture BOTH -1 and 2 from other parts. Can build -1 as neg(1). Can build 2 as add(1,1). Leibniz requires a longer tree.

### Implementation
- Fork `entropy-leibniz-v3/entropy_leibniz_v3_minimal.py` for each level
- Or create one script with command-line args for terminal config
- 5 seeds per level, same seed values (42, 7, 137, 2718, 31415)
- MAX_SEED = 360s, MAX_TOTAL = 1800s
- No injection in any variant

### Output
Create `entropy-leibniz-v3/stress_test_results.md` with:

| Level | Terminals | Total | Seeds Found | Fastest Seed | Slowest Seed | Notes |
|---|---|---|---|---|---|---|
| minimal (baseline) | 4 | 4 | 5/5 | 21s / 711 gen | 153s / 6136 gen | from v3 minimal |
| 1: moderate | 4 + 11 eph | 15 | ?/5 | ... | ... | ... |
| 2: wide | 2 + 41 eph | 42 | ?/5 | ... | ... | ... |
| 3: hostile | 4 + 40 eph | 44 | ?/5 | ... | ... | ... |
| 4: extreme | 2 + 39 eph | 41 | ?/5 | ... | ... | ... |

For each level, also report:
- Expressions found (all seeds)
- Whether hostile variants manufactured the missing constants
- What wrong-limit attractors appeared in failed seeds

### If a level fails 0/5
Stop and report. No need to run harder levels if an easier one fails. But DO report what it found instead — the attractors are interesting data.

### If Level 4 succeeds
That's the headline. The algorithm manufactured BOTH key constants from scratch and still found Leibniz. The parts bin objection is dead at that point.

### Time budget
4 levels × 5 seeds × 360s = 2 hours max. Run levels sequentially (so we can stop early on failure) but seeds within a level in parallel.
