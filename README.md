# Repo Position Coupling Index

Monthly index linking two registries the user already maintains:

- repo portfolio slugs
- investing thesis pillar ids

Each monthly report is a Markdown file with YAML front matter. The front matter
stores repo states, pillar states, coupling rows, and generated flags. The body
is readable git review output.

## What ships in v0.1

- JSON Schemas for coupling rows and monthly reports.
- Pydantic runtime models under `src/coupling/`.
- `coupling` CLI for validation, rendering, flagging, report creation, and
  month diffs.
- Gate scripts for voice lint, spec references, and report validation.
- `coupling_index/2026-M07.md` as the first checked-in report artifact.
- Example reports in `examples/` for tests and diff output.

## Install and run

```bash
python -m uv run pytest
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/validate_coupling_index.py
```

Useful CLI commands:

```bash
python -m uv run coupling validate coupling_index/2026-M07.md
python -m uv run coupling flag --month 2026-M07 --check
python -m uv run coupling diff --from 2026-M07-EXAMPLE --to 2026-M08-EXAMPLE
python -m uv run coupling render coupling_index/2026-M07.md
python -m uv run coupling new --month 2026-M08 --from-month 2026-M07
```

Without uv, the package can still be run from the repo root with:

```bash
python -m pytest
$env:PYTHONPATH='src'
python -m coupling.cli validate coupling_index/2026-M07.md
```

## Report shape

```text
coupling_index/
  2026-M07.md
examples/
  2026-M07-EXAMPLE.md
  2026-M08-EXAMPLE.md
src/coupling/
  cli.py
  diff.py
  flagger.py
  frontmatter.py
  render.py
  schema.py
```

The flagger emits five rule types:

- `build-orphan`
- `idea-orphan`
- `re-thesis-repo`
- `re-examine-pillar`
- `hedge-fired`

## Boundaries

- No causal inference machinery.
- No GitHub activity crawl.
- No auto-import from thesis-pillar-tracker.
- No multi-user workflow.

## License

MIT. See `LICENSE`.
