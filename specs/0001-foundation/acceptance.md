# Spec 0001 — Acceptance

v0 is done when the following hold.

## Repo shape

- README, LICENSE, AGENTS.md, .gitignore at the root.
- `specs/0001-foundation/` complete.
- `docs/first-pr.md` is concrete and file-level.

## Commands

After PR 1-3 land:

```bash
uv run pytest
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/validate_coupling_index.py examples/2026-M07-EXAMPLE.md
python -m coupling flag --month 2026-M07-EXAMPLE
```

All five exit zero.

## Functional gates

- The example index validates against the coupling_index schema and
  contains at least one flag of each of these types: `build-orphan`,
  `re-thesis-repo`.
- `coupling flag` on the example index produces a deterministic set
  of flags matching the example's `flagged[]` section.
- `coupling diff` between two example months produces a Markdown
  change set with at least one added coupling and one cleared flag.
- `spec_check.py` confirms every `R-RPC-NNN` reference is defined.

## Out of scope for v0 acceptance

- Causal interpretation of the coupling graph.
- Sync with thesis-pillar-tracker.
- Historical scoring.

Those land in later specs.
