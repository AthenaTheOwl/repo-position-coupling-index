# Spec 0002 - Design

## Ledger entries

| Requirement | Design decision |
|---|---|
| R-RPC-011 | Use setuptools with a `src/` layout and expose `coupling = coupling.cli:main`. |
| R-RPC-012 | Use Pydantic v2 models with string enums so YAML, JSON Schema, and CLI output stay aligned. |
| R-RPC-013 | Treat YAML front matter as canonical and regenerate the Markdown body from model data. |
| R-RPC-014 | Sort generated flags by rule order, then repo slug or pillar id, so diffs are stable. |
| R-RPC-015 | Compare couplings by `(repo_slug, pillar_id)` and report direction changes separately from adds/removes. |
| R-RPC-016 | Keep scripts small and local; they call the package code rather than duplicating report parsing. |
| R-RPC-017 | Use a seed monthly report with low-confidence rows where live pillar ids are not yet imported. |

## CLI surface

```bash
coupling validate coupling_index/2026-M07.md
coupling flag --month 2026-M07
coupling diff --from 2026-M07 --to 2026-M08-EXAMPLE
coupling render coupling_index/2026-M07.md
coupling new --month 2026-M08 --from-month 2026-M07
```

The month resolver checks `coupling_index/` first and `examples/` second. A
direct Markdown path is also accepted.

## Flag ordering

Flags are emitted in this order:

1. `build-orphan`
2. `idea-orphan`
3. `re-thesis-repo`
4. `re-examine-pillar`
5. `hedge-fired`

This follows the action order from R-RPC-004 and keeps `coupling flag` idempotent.

