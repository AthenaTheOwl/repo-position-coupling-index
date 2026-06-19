# Spec 0001 — Foundation

## R-RPC-001 — repo scaffold
Repo at `e:/claude_code/random-apps/repo-position-coupling-index`. MIT
license. README, AGENTS.md, LICENSE, .gitignore at the root.

## R-RPC-002 — coupling row schema
`schemas/coupling_row.schema.json` defines a single coupling:
`repo_slug`, `pillar_id`, `direction` (bets-on / bets-against /
hedged), `mechanism` (1-3 sentences naming the shared causal
mechanism), `confidence` (low / medium / high), `created_month`.

## R-RPC-003 — monthly index schema
`schemas/coupling_index.schema.json` defines the monthly map:
`month` (YYYY-Mnn), `repo_states[]` with `repo_slug` and
`alive_status` (alive / quiet / dead), `pillar_states[]` with
`pillar_id` and `current_verdict` (confirming / weakening /
invalidated), `couplings[]`, `flagged[]` (orphans + misalignments).

## R-RPC-004 — orphan-detection rules
- Repo with zero couplings is `flag: build-orphan`.
- Pillar with zero couplings is `flag: idea-orphan`.
- Repo `alive` + coupled pillar `invalidated` is
  `flag: re-thesis-repo`.
- Pillar `confirming` + all coupled repos `dead` is
  `flag: re-examine-pillar`.
- Repo `bets-against` a pillar AND pillar `confirming` is
  `flag: hedge-fired`.

## R-RPC-005 — registry refs
`config/repos.yaml` lists repo slugs with the same slugs used in the
portfolio repo registry; `config/pillars.yaml` lists pillar ids using
the same ids used in thesis-pillar-tracker. Both files are flat
arrays and round-trip through Pydantic.

## R-RPC-006 — file naming
Monthly indices live at `coupling_index/<year>-M<nn>.md` with a
front-matter block that round-trips through coupling_index schema.

## R-RPC-007 — example index
`examples/2026-M07-EXAMPLE.md` ships a worked example: 4 repos, 3
pillars, 5 couplings, 2 flagged misalignments (one build-orphan, one
re-thesis-repo).

## R-RPC-008 — voice lint stub
`scripts/voice_lint.py` (portfolio copy) runs over
`coupling_index/*.md`.

## R-RPC-009 — spec check
`scripts/spec_check.py` confirms every `R-RPC-NNN` referenced in
`design.md` and `tasks.md` is defined here.

## R-RPC-010 — manual alive_status only
v0 does not crawl GitHub for commit recency, repo activity, or any
other proxy. The `alive_status` per repo is a manually maintained
field; the user is honest about death.
