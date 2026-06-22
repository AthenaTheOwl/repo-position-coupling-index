# Spec 0002 - Design Ledger

## R-RPC-011 - package metadata

`pyproject.toml` declares a package named `repo-position-coupling-index`, a
console script named `coupling`, dev dependencies under `[dependency-groups]`,
and `[tool.uv] package = true`.

## R-RPC-012 - runtime models

`src/coupling/schema.py` defines Pydantic models for repo states, pillar states,
coupling rows, flags, and monthly reports. The models accept only the enum
values used by the JSON Schemas.

## R-RPC-013 - Markdown front matter

Monthly reports are Markdown files whose YAML front matter round-trips through
the monthly report model. Report body text is derived from the front matter and
is not the source of truth.

## R-RPC-014 - deterministic flagger

`coupling flag` computes the five rules from R-RPC-004 in deterministic order
and writes the resulting flags to the selected report.

## R-RPC-015 - month diff

`coupling diff --from <month> --to <month>` renders a Markdown change set with
added couplings, removed couplings, direction changes, added flags, and cleared
flags.

## R-RPC-016 - gate scripts

The repo ships `scripts/voice_lint.py`, `scripts/spec_check.py`, and
`scripts/validate_coupling_index.py`. The scripts exit zero on the checked-in
v0.1 report and examples.

## R-RPC-017 - checked-in report artifact

`coupling_index/2026-M07.md` is a checked-in monthly report artifact that
validates and can be re-flagged without drift.

