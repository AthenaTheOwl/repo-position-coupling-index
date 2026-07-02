from __future__ import annotations

from repo_position_coupling_index.cli import main
from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.model import CouplingIndex
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


def test_rank_pillars_pins_exact_exposure_numbers() -> None:
    # Pin the CONFIDENCE_WEIGHT arithmetic (HIGH=3/MEDIUM=2/LOW=1) against the
    # committed report. The top pillar has two alive medium-confidence bettors
    # (2 + 2) plus one quiet repo that does not count toward exposure.
    index = load_index(default_report_path())
    ranked = rank_pillars(index)

    by_id = {r["pillar_id"]: r for r in ranked}
    assert by_id["PILLAR-THESIS-TRACEABILITY"]["exposure"] == 4
    assert by_id["PILLAR-THESIS-TRACEABILITY"]["repos"] == 3
    assert by_id["PILLAR-AGENT-OPERATING-LOOPS"]["exposure"] == 2
    assert by_id["PILLAR-CREATIVE-IP"]["exposure"] == 1
    assert by_id["PILLAR-UNMAPPED-CAPITAL"]["exposure"] == 0


def test_headline_literal_text_for_committed_report() -> None:
    index = load_index(default_report_path())
    result = headline(index, rank_pillars(index))

    assert result == (
        "2026-M07: PILLAR-THESIS-TRACEABILITY carries the most live build exposure "
        "(exposure 4, 3 repos), verdict confirming. 2 pillar(s) softening: "
        "PILLAR-CREATIVE-IP, PILLAR-UNMAPPED-CAPITAL. 2 open flag(s) need a decision."
    )


def test_headline_names_invalidated_pillar_in_softening_clause() -> None:
    # The committed report has no invalidated verdicts, so exercise that branch
    # with a hand-built index and pin the softening clause.
    index = CouplingIndex.model_validate(
        {
            "month": "2026-M07",
            "repo_states": [{"repo_slug": "repo-alpha", "alive_status": "alive"}],
            "pillar_states": [
                {"pillar_id": "PILLAR-001", "current_verdict": "invalidated"}
            ],
            "couplings": [
                {
                    "repo_slug": "repo-alpha",
                    "pillar_id": "PILLAR-001",
                    "direction": "bets-on",
                    "mechanism": "Repo alpha bets on a pillar that has failed.",
                    "confidence": "high",
                    "created_month": "2026-M07",
                }
            ],
            "flagged": [],
        }
    )
    result = headline(index, rank_pillars(index))

    assert "1 pillar(s) softening: PILLAR-001." in result
    assert result == (
        "2026-M07: PILLAR-001 carries the most live build exposure "
        "(exposure 3, 1 repos), verdict invalidated. 1 pillar(s) softening: "
        "PILLAR-001. 0 open flag(s) need a decision."
    )


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
