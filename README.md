# Repo to Position Coupling Index

Tags each portfolio repo with the investing-thesis pillar it implicitly bets
on or against. A repo's traction (or death) becomes a soft signal on the
coupled pillar. A pillar invalidation auto-flags the coupled repos for
re-thesis.

## What this is

A small monthly map between two systems the user already maintains:

- The build portfolio (~20 repos, each with an explicit current thesis).
- The investing thesis pillars (~6-12 falsifiable claims tracked
  monthly in thesis-pillar-tracker).

Every repo gets tagged with zero or more pillars and a `direction`
(bets-on / bets-against / hedged / orphan). Every pillar gets tagged
with the coupled repos. The output is a single Markdown index per month
plus a flagged-misalignments section that names:

- Pillars with no coupled repo (idea-orphans).
- Repos with no coupled pillar (build-orphans).
- Repos whose thesis is alive but whose pillar is invalidated
  (re-thesis the repo).
- Pillars marked confirming but whose coupled repos died
  (re-examine the pillar — was the win really evidence?).

## Status

v0 scaffold. No coupling engine, no historical evidence ingestion. Spec
0001 defines the schema, the orphan-detection rules, and the gates that
land in spec 0002.

## How to run

Placeholder. Spec 0002 will ship the CLI:

```bash
uv run coupling new --month 2026-M07
uv run coupling diff --from 2026-M06 --to 2026-M07
uv run coupling flag --month 2026-M07
```

For now read `specs/0001-foundation/` and `docs/first-pr.md`.

## Layout

```
.
├── AGENTS.md
├── LICENSE
├── README.md
├── docs/
│   └── first-pr.md
└── specs/
    └── 0001-foundation/
        ├── acceptance.md
        ├── design.md
        ├── requirements.md
        └── tasks.md
```

Planned directories:

- `coupling_index/` — `<YYYY>-M<nn>.md` per month.
- `src/coupling/` — schema, CLI, flagger.
- `config/`
  - `repos.yaml` — refs into the portfolio repo registry.
  - `pillars.yaml` — refs into thesis-pillar-tracker.
- `tests/` — schema + orphan-detection tests.

## Why this exists

The user is one of the few people running both an explicit build
portfolio AND an explicit investing portfolio with named theses on each
side. Both sides change month by month. Without this index the
couplings are implicit; with it, a pillar invalidation triggers an
explicit re-thesis queue on the build side, and a repo death triggers
an explicit re-examination queue on the investing side.

## License

MIT. See `LICENSE`.
