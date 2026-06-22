# Spec 0002 - Acceptance

v0.1 is accepted when these commands exit zero:

```bash
python -m uv run pytest
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/validate_coupling_index.py
```

The checked-in report must satisfy R-RPC-017. `STATUS.md` must keep these H2
sections exactly:

```markdown
## Current state
## Known limits
## Next feature queue
```

