# Spec 0001 — Design

## Shape

A bipartite graph stored as flat YAML, rendered to Markdown once per
month. The shape is intentionally tiny.

```
schemas/
  coupling_row.schema.json     # R-RPC-002
  coupling_index.schema.json   # R-RPC-003
config/
  repos.yaml                   # R-RPC-005
  pillars.yaml                 # R-RPC-005
src/coupling/
  cli.py                       # new / diff / flag / render
  schema.py                    # Pydantic mirrors
  flagger.py                   # the five rules (R-RPC-004)
  diff.py                      # month-over-month delta
  render.py                    # coupling_index -> Markdown
coupling_index/                # <YYYY>-M<nn>.md per month (R-RPC-006)
examples/
  2026-M07-EXAMPLE.md          # R-RPC-007
scripts/
  voice_lint.py
  spec_check.py
tests/
  test_schemas.py
  test_flagger.py
  test_diff.py
  test_render_roundtrip.py
```

## Data flow

1. User edits `config/repos.yaml` and `config/pillars.yaml` to reflect
   the current month's reality (manual alive_status; manual
   current_verdict).
2. `coupling new --month 2026-Mnn` scaffolds a new index file by
   copying the prior month's couplings forward; the user edits in any
   new couplings.
3. `coupling flag --month 2026-Mnn` runs the five flagging rules
   (R-RPC-004) and writes them into the flagged[] section.
4. `coupling diff --from 2026-Mxx --to 2026-Myy` renders a Markdown
   change set (couplings added, removed, direction-flipped; flags
   added, cleared).

## Why a bipartite graph and not a matrix

A repo can couple to multiple pillars; a pillar can couple to multiple
repos; many cells will be empty. A matrix wastes diff resolution. A
bipartite edge list keeps the diff small and the cause readable.

## The five flagging rules

The rules in R-RPC-004 are the entire decision logic. They are
deliberately small. Each rule maps to one concrete user action:

| Flag | User action |
|---|---|
| `build-orphan` | Decide if the repo deserves a coupled pillar or is genuinely uncoupled |
| `idea-orphan` | Decide if the pillar is real if no repo bets on it |
| `re-thesis-repo` | Open the repo's spec and rewrite the thesis |
| `re-examine-pillar` | Open the pillar tracker and check whether the verdict was lucky |
| `hedge-fired` | Decide whether the hedge worked or the position should change |

A flag without a named user action would be noise; v0 refuses to add
rules that do not name an action.

## What is not in spec 0001

- Historical coupling-vs-outcome scoring (spec 0003).
- Auto-sync with thesis-pillar-tracker (spec 0004).
- Visual rendering beyond Markdown (out of scope indefinitely).

Spec 0002 lands the flagger plus the first real monthly index.
