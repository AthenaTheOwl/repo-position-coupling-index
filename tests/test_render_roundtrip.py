from __future__ import annotations

from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.render import render_index


def test_rendered_index_round_trips(tmp_path) -> None:
    source = load_index("examples/2026-M07-EXAMPLE.md")
    target = tmp_path / "report.md"

    target.write_text(render_index(source), encoding="utf-8")
    reparsed = load_index(target)

    assert reparsed.as_plain_data() == source.as_plain_data()


def test_rendered_body_pins_headings_and_table_columns() -> None:
    # load_index discards the body, so the round-trip test above never sees the
    # rendered Markdown. Pin the body directly so a column reorder or heading
    # change fails here.
    source = load_index("examples/2026-M07-EXAMPLE.md")
    output = render_index(source)

    assert "# Coupling Index - 2026-M07" in output
    assert "## Repo states" in output
    assert "## Pillar states" in output
    assert "## Couplings" in output
    assert "## Flagged misalignments" in output

    # column order: Repo | Pillar | Direction | Confidence | Mechanism
    assert "| Repo | Pillar | Direction | Confidence | Mechanism |" in output
    assert (
        "| `repo-alpha` | `PILLAR-001` | bets-on | high | "
        "Repo alpha tests whether a small workflow can keep a manual record accurate. |"
    ) in output

    # a repo-states row, a pillar-states row, and a flag row
    assert "| `repo-gamma` | dead |" in output
    assert "| `PILLAR-002` | invalidated |" in output
    assert (
        "| re-thesis-repo | `repo-alpha` | `PILLAR-002` | "
        "Repo is alive while its coupled pillar is invalidated. | "
        "Open the repo thesis and decide what still holds. |"
    ) in output
