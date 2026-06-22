from __future__ import annotations

from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.render import render_index


def test_rendered_index_round_trips(tmp_path) -> None:
    source = load_index("examples/2026-M07-EXAMPLE.md")
    target = tmp_path / "report.md"

    target.write_text(render_index(source), encoding="utf-8")
    reparsed = load_index(target)

    assert reparsed.as_plain_data() == source.as_plain_data()
