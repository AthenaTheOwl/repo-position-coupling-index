---
month: 2026-M08
repo_states:
- repo_slug: repo-alpha
  alive_status: alive
- repo_slug: repo-beta
  alive_status: quiet
- repo_slug: repo-gamma
  alive_status: dead
- repo_slug: repo-delta
  alive_status: alive
pillar_states:
- pillar_id: PILLAR-001
  current_verdict: confirming
- pillar_id: PILLAR-002
  current_verdict: weakening
- pillar_id: PILLAR-003
  current_verdict: weakening
couplings:
- repo_slug: repo-alpha
  pillar_id: PILLAR-001
  direction: hedged
  mechanism: Repo alpha now treats the record-keeping claim as useful but no longer central.
  confidence: medium
  created_month: 2026-M07
- repo_slug: repo-alpha
  pillar_id: PILLAR-002
  direction: hedged
  mechanism: Repo alpha still depends on the pillar enough that weakening changes its thesis.
  confidence: medium
  created_month: 2026-M07
- repo_slug: repo-beta
  pillar_id: PILLAR-003
  direction: bets-against
  mechanism: Repo beta assumes the pillar weakens when the manual process becomes cheaper.
  confidence: medium
  created_month: 2026-M07
- repo_slug: repo-delta
  pillar_id: PILLAR-002
  direction: bets-on
  mechanism: Repo delta now tests the same review loop with a narrower input set.
  confidence: low
  created_month: 2026-M08
- repo_slug: repo-gamma
  pillar_id: PILLAR-001
  direction: bets-on
  mechanism: Repo gamma repeats the same record-keeping claim in a dormant code path.
  confidence: low
  created_month: 2026-M07
- repo_slug: repo-gamma
  pillar_id: PILLAR-003
  direction: hedged
  mechanism: Repo gamma has weak evidence but still names the same operating constraint.
  confidence: low
  created_month: 2026-M07
flagged: []
---

# Coupling Index - 2026-M08

Worked diff example for tests and review.

