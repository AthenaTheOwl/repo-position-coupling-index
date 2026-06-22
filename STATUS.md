# Status

## Current state

- v0.1 has JSON Schemas, Pydantic mirrors, a Markdown front-matter renderer, a deterministic flagger, a month diff, and an argparse CLI.
- `coupling_index/2026-M07.md` is checked in as the first report artifact.
- The gate scripts validate report data, spec references, and coupling report voice constraints.

## Known limits

- Repo and pillar registries are still hand-maintained YAML arrays.
- The CLI does not import data from the portfolio registry or thesis-pillar-tracker.
- Historical outcome scoring is not implemented; the diff is month-to-month only.

## Next feature queue

- Add a guided `coupling new` flow that carries the latest report forward and opens blanks for new repos and pillars.
- Add a report-to-report history ledger that records when a flag first appeared and when it cleared.
- Add an adapter that reads exported thesis-pillar-tracker IDs without mutating either registry.

- Resolve factory defect: missing PRODUCT_BRIEF.md,SYSTEM_MAP.md
- Resolve factory defect: missing reports/*.jsonl
- Resolve factory defect: PRODUCT_BRIEF.md is required for active repos
- Resolve factory defect: SYSTEM_MAP.md is required for active repos
- Resolve factory defect: expected file 'PRODUCT_BRIEF.md' is missing
- Resolve factory defect: expected file 'SYSTEM_MAP.md' is missing
- Resolve factory defect: expected file 'repo_position_coupling_index/cli.py' is missing
- Resolve factory defect: expected glob 'reports/*.jsonl' matched no files
- Resolve factory defect: module 'cli' declares source 'repo_position_coupling_index/cli.py', but it is missing
- Resolve factory defect: module 'model' declares source 'repo_position_coupling_index/model.py', but it is missing
- Resolve factory defect: module 'report' declares source 'repo_position_coupling_index/scoring.py', but it is missing
- Resolve factory defect: claude_code review requested patch; inspect defect log
