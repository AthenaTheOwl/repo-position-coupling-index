from __future__ import annotations

from pathlib import Path

import pytest

from repo_position_coupling_index.cli import latest_month, main
from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.render import render_index


def write_source_report(index_dir: Path, month: str = "2026-M07") -> Path:
    index_dir.mkdir()
    source = load_index("coupling_index/2026-M07.md")
    source_path = index_dir / f"{month}.md"
    source_path.write_text(render_index(source), encoding="utf-8")
    return source_path


def test_cmd_new_creates_next_month_with_carried_couplings(tmp_path) -> None:
    index_dir = tmp_path / "coupling_index"
    write_source_report(index_dir)

    code = main(
        [
            "new",
            "--month",
            "2026-M08",
            "--from-month",
            "2026-M07",
            "--index-dir",
            str(index_dir),
        ]
    )

    created = load_index(index_dir / "2026-M08.md")
    source = load_index(index_dir / "2026-M07.md")
    assert code == 0
    assert created.month == "2026-M08"
    assert created.flagged == []
    assert created.as_plain_data()["couplings"] == source.as_plain_data()["couplings"]


def test_cmd_new_refuses_to_overwrite_existing_report(tmp_path) -> None:
    index_dir = tmp_path / "coupling_index"
    write_source_report(index_dir)
    args = [
        "new",
        "--month",
        "2026-M08",
        "--from-month",
        "2026-M07",
        "--index-dir",
        str(index_dir),
    ]

    assert main(args) == 0
    with pytest.raises(SystemExit) as exc:
        main(args)

    assert "report already exists" in str(exc.value)
    assert str(index_dir / "2026-M08.md") in str(exc.value)


def test_latest_month_picks_newest_report_stem(tmp_path) -> None:
    index_dir = tmp_path / "coupling_index"
    index_dir.mkdir()
    (index_dir / "2026-M07.md").write_text("", encoding="utf-8")
    (index_dir / "2026-M08.md").write_text("", encoding="utf-8")

    assert latest_month(index_dir) == "2026-M08"


def test_committed_second_period_render_is_deterministic() -> None:
    report_path = Path("coupling_index/2026-M08.md")

    assert render_index(load_index(report_path)) == report_path.read_text(encoding="utf-8")
