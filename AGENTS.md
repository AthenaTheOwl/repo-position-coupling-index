# AGENTS.md — repo-position-coupling-index

Operating contract for AI agents in this repo. Same conventions as the
rest of the portfolio.

## What this repo is

A monthly index linking two registries: the user's repo portfolio and
the user's investing thesis pillars. Output is a Markdown coupling map
plus a flagged-misalignments section with concrete re-thesis prompts.

This is not a portfolio dashboard, a CRM, or a strategy doc. It is the
bipartite-graph diff between two systems that already exist.

## Voice constraints

- No marketing words. Coupling claims must point at concrete shared
  causal mechanisms, not vibes.
- No antithetical reversals as a structural device.
- Plain assertions. A coupling entry says what the shared bet is, not
  that the linkage is "strategic" or "synergistic".
- An entry that cannot name a falsifiable shared mechanism is recorded
  as `direction: hedged` or `direction: orphan`, not as a strong
  coupling.

## Roles in tasks

| Role | What they do |
|---|---|
| `coupler` | Authors new coupling rows; one repo to N pillars |
| `orphan-detector` | Runs the flagging rules each month |
| `diff-runner` | Produces the month-over-month change set |
| `historian` | Owns historical coupling vs realized outcome data |

## Gates (will land in spec 0002)

```bash
uv run pytest
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/validate_coupling_index.py
```

## Out of scope

- Causal inference machinery. v0 records coupling claims and outcomes;
  any causal interpretation is the user's, not the tool's.
- Auto-importing thesis-pillar-tracker contents. v0 references pillar
  ids by string; the user keeps both registries in sync by hand.
- Multi-user portfolios. Single user.
- Quantitative repo-traction scoring. v0 takes a manual `alive_status`
  field per repo: alive / quiet / dead.
