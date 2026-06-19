# First PR after the scaffold

Title: `feat: coupling-row + coupling-index schemas, placeholder registries`

## Scope

This PR lands the schemas, the placeholder registries, the Pydantic
mirrors, the worked example index file, and the schema tests. No
flagger logic yet; no renderer yet; no CLI behavior yet beyond
`--help`.

## Files added

- `schemas/coupling_row.schema.json` — R-RPC-002. Required:
  `repo_slug`, `pillar_id`, `direction` (enum), `mechanism`
  (1-3 sentences), `confidence` (enum), `created_month`.
- `schemas/coupling_index.schema.json` — R-RPC-003. Required:
  `month`, `repo_states[]`, `pillar_states[]`, `couplings[]`,
  `flagged[]`. `flagged[]` entries reference one of the five
  flag types in R-RPC-004 by enum.
- `src/coupling/__init__.py`
- `src/coupling/schema.py` — Pydantic mirrors.
- `config/repos.yaml` — 4-6 placeholder repo entries using slugs
  like `repo-alpha`, `repo-beta`, etc.
- `config/pillars.yaml` — 3-5 placeholder pillar entries using ids
  like `PILLAR-001`, etc.
- `examples/2026-M07-EXAMPLE.md` — R-RPC-007. Markdown body plus
  YAML front matter that round-trips through coupling_index schema.
  Contains 5 couplings, one `build-orphan` flag, one
  `re-thesis-repo` flag.
- `tests/test_schemas.py` — required-field, enum-validation, and
  round-trip tests for both schemas.
- `pyproject.toml` — `pydantic`, `pyyaml`, `jsonschema`, `pytest`,
  `ruff`.

## Files changed

None — first PR after the scaffold.

## Verification

```bash
uv sync
uv run pytest -v
uv run python -c "import json, jsonschema; \
  [jsonschema.Draft202012Validator.check_schema(json.load(open(f))) \
   for f in ['schemas/coupling_row.schema.json', \
             'schemas/coupling_index.schema.json']]"
```

`pytest -v` shows at least 6 passing tests.

## What this PR does not do

- No flagger logic (PR 2 — the five rules in R-RPC-004).
- No renderer (PR 2).
- No diff (PR 2).
- No voice_lint copy (PR 3).
- No real repo or pillar data (placeholder only).

## Review checklist

- [ ] Both JSON Schemas validate against Draft 2020-12.
- [ ] Pydantic mirrors do not drift (round-trip tests pin this).
- [ ] The example index contains exactly the two flag types named in
      this PR's scope so the flagger PR has a concrete target.
- [ ] No real repo slug or pillar id from the live portfolio is
      hard-coded; all references are `repo-alpha`-style placeholders.
