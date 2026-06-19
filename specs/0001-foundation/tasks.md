# Spec 0001 — Tasks

Ordered for the first 2-3 PRs.

## PR 1 — schemas and config

- [ ] Write `schemas/coupling_row.schema.json` (R-RPC-002).
- [ ] Write `schemas/coupling_index.schema.json` (R-RPC-003).
- [ ] Write `src/coupling/schema.py` Pydantic mirrors.
- [ ] Write `config/repos.yaml` with placeholder slugs (R-RPC-005).
- [ ] Write `config/pillars.yaml` with placeholder pillar ids.
- [ ] Write `examples/2026-M07-EXAMPLE.md` (R-RPC-007).
- [ ] Write `tests/test_schemas.py`.

## PR 2 — flagger and render

- [ ] Write `src/coupling/flagger.py` (the five rules from
      R-RPC-004).
- [ ] Write `src/coupling/render.py` (round-trippable front matter,
      R-RPC-006).
- [ ] Write `src/coupling/diff.py`.
- [ ] Write `tests/test_flagger.py` covering all five rules.
- [ ] Write `tests/test_render_roundtrip.py`.
- [ ] CLI wires `coupling flag`, `coupling render`, `coupling diff`.

## PR 3 — gates and the first real monthly index

- [ ] Copy `scripts/voice_lint.py` from portfolio (R-RPC-008).
- [ ] Write `scripts/spec_check.py` (R-RPC-009).
- [ ] Write `pyproject.toml`.
- [ ] Build the first real `coupling_index/2026-M07.md` against the
      live repo + pillar registries.
- [ ] Confirm gates exit zero.
