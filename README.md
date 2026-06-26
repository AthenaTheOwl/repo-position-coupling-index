# repo-position-coupling-index

Four investing pillars on the board this month. One of them, PILLAR-UNMAPPED-CAPITAL,
has zero repos betting on it and exposure zero — a thesis nobody is actually building
toward. One repo, repo-delta, is coupled to no live pillar at all. The index is what
notices both.

## What it does

You keep two registries by hand: the repos you build, and the investing-thesis pillars
you say you believe. They drift apart quietly. A repo goes quiet and the pillar it was
the only evidence for keeps reading "confirming." A pillar weakens and three repos go on
betting on it. Nobody added the two lists up, so the gap stays hidden until a quarter
later when it's a sunk one.

This adds them up, once a month. Each monthly report is a Markdown file with YAML front
matter holding repo states, pillar states, and the coupling rows between them; the body
is readable git-review output. A flagger walks the join and emits five rule types —
`build-orphan`, `idea-orphan`, `re-thesis-repo`, `re-examine-pillar`, `hedge-fired` —
each one a decision someone has to make on purpose. It does not crawl GitHub, infer
causation, or import your tracker for you. It tells you where the two stories you're
telling yourself have stopped matching.

## Try it

A no-arg `show` verb prints a ranked, readable view of the committed report:

```bash
python -m repo_position_coupling_index show
python -m uv run coupling show
```

```
coupling index - 2026-M07
5 couplings, 6 repos, 4 pillars, 2 flags

pillars by live build exposure (most-bet-on first):
pillar                        verdict     repos  exposure
----------------------------  ----------  -----  --------
PILLAR-THESIS-TRACEABILITY    confirming  3      4       
PILLAR-AGENT-OPERATING-LOOPS  confirming  1      2       
PILLAR-CREATIVE-IP            weakening   1      1       
PILLAR-UNMAPPED-CAPITAL       weakening   0      0       

open flags:
flag          repo        pillar                   reason                                 
------------  ----------  -----------------------  ---------------------------------------
build-orphan  repo-delta  -                        Repo has no non-orphan pillar coupling.
idea-orphan   -           PILLAR-UNMAPPED-CAPITAL  Pillar has no non-orphan repo coupling.

2026-M07: PILLAR-THESIS-TRACEABILITY carries the most live build exposure (exposure 4, 3 repos), verdict confirming. 2 pillar(s) softening: PILLAR-CREATIVE-IP, PILLAR-UNMAPPED-CAPITAL. 2 open flag(s) need a decision.
```

Pillars rank by live build exposure: alive repos betting on a pillar, weighted by
confidence. The two flags at the bottom are the orphans — a repo with nothing to test,
a pillar with nobody testing it.

## Live demo

The browser version is the same report you can poke: the ranked pillars, the couplings,
the open flags, no network and no secrets.

```bash
python -m uv run --with streamlit streamlit run streamlit_app.py
```

Streamlit Cloud deploy: repo `AthenaTheOwl/repo-position-coupling-index`, branch
`main`, main file `streamlit_app.py`.

<!-- live-url: (paste the Streamlit Cloud URL here once deployed) -->

## How it connects

- [thesis-pillar-tracker](https://github.com/AthenaTheOwl/thesis-pillar-tracker) — the
  registry that decides whether each pillar is confirming, weakening, or invalidated.
  This index links repo slugs to those pillar ids; it deliberately does not auto-import
  them, so the ids stay manual until an adapter exists.
- [grid-silicon](https://github.com/AthenaTheOwl/grid-silicon) and the
  [starforge demos](https://github.com/AthenaTheOwl?tab=repositories&q=starforge) are
  among the builds that show up as repo slugs on the board — the actual bets the pillars
  are scored against.

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

Without uv, run it from the repo root:

```bash
python -m pytest
$env:PYTHONPATH='src'
python -m coupling.cli validate coupling_index/2026-M07.md
```

## Layout

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

## License

MIT. See `LICENSE`.
