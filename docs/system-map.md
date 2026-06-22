# System Map

## Inputs

`config/repos.yaml` is a flat list of repo slugs. The monthly report records the
manual `alive_status` for each repo.

`config/pillars.yaml` is a flat list of pillar ids. The monthly report records
the manual `current_verdict` for each pillar.

`coupling_index/<YYYY>-M<nn>.md` stores YAML front matter that matches
`schemas/coupling_index.schema.json`.

## Core modules

- `coupling.schema` defines the Pydantic mirrors for rows, reports, and flags.
- `coupling.frontmatter` parses and writes Markdown files with YAML front matter.
- `coupling.flagger` computes flags from a report model.
- `coupling.render` renders a validated report back to Markdown.
- `coupling.diff` renders a Markdown change set between two reports.
- `coupling.cli` wires `new`, `flag`, `diff`, `render`, and `validate`.

## Gates

- `python -m uv run pytest`
- `python scripts/voice_lint.py`
- `python scripts/spec_check.py`
- `python scripts/validate_coupling_index.py`

The scripts do not mutate files. `coupling flag` mutates the selected report by
replacing `flagged` with the deterministic flagger output.

