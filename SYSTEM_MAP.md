# System Map

## Inputs

`config/repos.yaml` is a flat list of repo slugs. The monthly report records the
manual `alive_status` for each repo.

`config/pillars.yaml` is a flat list of pillar ids. The monthly report records
the manual `current_verdict` for each pillar.

`coupling_index/<YYYY>-M<nn>.md` stores YAML front matter that matches
`schemas/coupling_index.schema.json`.

## Core modules

- `repo_position_coupling_index.model` defines the Pydantic mirrors for rows,
  reports, and flags.
- `repo_position_coupling_index.frontmatter` parses and writes Markdown files
  with YAML front matter.
- `repo_position_coupling_index.scoring` computes flags from a report model.
- `repo_position_coupling_index.render` renders a validated report back to
  Markdown.
- `repo_position_coupling_index.diff` renders a Markdown change set between two
  reports.
- `repo_position_coupling_index.cli` wires `new`, `flag`, `diff`, `render`, and
  `validate`.

## Gates

- `python -m uv run pytest`
- `python scripts/voice_lint.py`
- `python scripts/spec_check.py`
- `python scripts/validate_coupling_index.py`

The scripts do not mutate files. `coupling flag` mutates the selected report by
replacing `flagged` with the deterministic flagger output.
