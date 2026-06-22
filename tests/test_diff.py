from __future__ import annotations

from repo_position_coupling_index.diff import render_diff
from repo_position_coupling_index.frontmatter import load_index


def test_diff_names_added_coupling_and_cleared_flag() -> None:
    previous = load_index("examples/2026-M07-EXAMPLE.md")
    current = load_index("examples/2026-M08-EXAMPLE.md")

    output = render_diff(previous, current)

    assert "`repo-delta` -> `PILLAR-002`" in output
    assert "build-orphan: repo `repo-delta`, pillar `-`" in output
    assert "bets-on -> hedged" in output
