from __future__ import annotations

from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.model import FlagType
from repo_position_coupling_index.scoring import compute_flags, with_computed_flags


def test_example_flags_are_deterministic() -> None:
    index = load_index("examples/2026-M07-EXAMPLE.md")
    computed = compute_flags(index)

    assert [flag.model_dump(mode="json", exclude_none=True) for flag in computed] == index.as_plain_data()[
        "flagged"
    ]


def test_all_flag_rules() -> None:
    index = load_index("examples/2026-M07-EXAMPLE.md")
    data = index.as_plain_data()
    data["repo_states"] = [
        {"repo_slug": "repo-alpha", "alive_status": "alive"},
        {"repo_slug": "repo-beta", "alive_status": "dead"},
        {"repo_slug": "repo-gamma", "alive_status": "dead"},
        {"repo_slug": "repo-delta", "alive_status": "alive"},
    ]
    data["pillar_states"] = [
        {"pillar_id": "PILLAR-001", "current_verdict": "confirming"},
        {"pillar_id": "PILLAR-002", "current_verdict": "invalidated"},
        {"pillar_id": "PILLAR-003", "current_verdict": "confirming"},
        {"pillar_id": "PILLAR-004", "current_verdict": "weakening"},
    ]
    data["couplings"] = [
        {
            "repo_slug": "repo-alpha",
            "pillar_id": "PILLAR-002",
            "direction": "bets-on",
            "mechanism": "Repo alpha depends on a pillar that has failed.",
            "confidence": "high",
            "created_month": "2026-M07",
        },
        {
            "repo_slug": "repo-beta",
            "pillar_id": "PILLAR-001",
            "direction": "bets-on",
            "mechanism": "Repo beta is dead while this confirming pillar only has dead repos.",
            "confidence": "medium",
            "created_month": "2026-M07",
        },
        {
            "repo_slug": "repo-gamma",
            "pillar_id": "PILLAR-003",
            "direction": "bets-against",
            "mechanism": "Repo gamma hedges against a pillar that is now confirming.",
            "confidence": "medium",
            "created_month": "2026-M07",
        },
    ]
    data["flagged"] = []
    updated = with_computed_flags(index.model_validate(data))

    assert [flag.flag for flag in updated.flagged] == [
        FlagType.BUILD_ORPHAN,
        FlagType.IDEA_ORPHAN,
        FlagType.RE_THESIS_REPO,
        FlagType.RE_EXAMINE_PILLAR,
        FlagType.RE_EXAMINE_PILLAR,
        FlagType.HEDGE_FIRED,
    ]
