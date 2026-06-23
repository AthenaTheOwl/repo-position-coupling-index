from __future__ import annotations

from repo_position_coupling_index.cli import main
from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.show import (
    default_report_path,
    headline,
    rank_pillars,
    render_show,
    show_report,
)


def test_default_report_path_exists() -> None:
    assert default_report_path().exists()


def test_rank_pillars_orders_by_live_exposure() -> None:
    index = load_index(default_report_path())
    ranked = rank_pillars(index)

    assert ranked[0]["pillar_id"] == "PILLAR-THESIS-TRACEABILITY"
    exposures = [int(r["exposure"]) for r in ranked]
    assert exposures == sorted(exposures, reverse=True)


def test_render_show_includes_table_and_headline() -> None:
    index = load_index(default_report_path())
    output = render_show(index)

    assert "coupling index - 2026-M07" in output
    assert "pillars by live build exposure" in output
    assert "PILLAR-THESIS-TRACEABILITY" in output
    assert "build-orphan" in output
    assert headline(index, rank_pillars(index)) in output


def test_show_report_reads_committed_artifact() -> None:
    assert "coupling index" in show_report()


def test_cli_show_exits_zero(capsys) -> None:
    code = main(["show"])
    captured = capsys.readouterr()

    assert code == 0
    assert "coupling index - 2026-M07" in captured.out
