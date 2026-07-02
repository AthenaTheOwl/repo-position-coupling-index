from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest
from pydantic import ValidationError

from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.model import CouplingIndex, CouplingRow
from repo_position_coupling_index.cli import main


def test_json_schemas_are_valid() -> None:
    for path in Path("schemas").glob("*.schema.json"):
        jsonschema.Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))


def test_example_round_trips_through_model() -> None:
    index = load_index("examples/2026-M07-EXAMPLE.md")

    reparsed = CouplingIndex.model_validate(index.as_plain_data())

    assert reparsed.month == "2026-M07"
    assert len(reparsed.couplings) == 5
    assert {flag.flag for flag in reparsed.flagged} == {"build-orphan", "re-thesis-repo"}


def test_cli_validate_defaults_to_canonical_report(capsys) -> None:
    assert main(["validate"]) == 0

    out = capsys.readouterr().out
    assert "validated coupling_index" in out
    assert "couplings" in out


def test_row_rejects_unknown_direction() -> None:
    with pytest.raises(ValidationError):
        CouplingRow.model_validate(
            {
                "repo_slug": "repo-alpha",
                "pillar_id": "PILLAR-001",
                "direction": "aligned",
                "mechanism": "This row has a concrete mechanism.",
                "confidence": "low",
                "created_month": "2026-M07",
            }
        )


def test_row_rejects_mechanism_over_three_sentences() -> None:
    with pytest.raises(ValidationError, match="1-3 sentences"):
        CouplingRow.model_validate(
            {
                "repo_slug": "repo-alpha",
                "pillar_id": "PILLAR-001",
                "direction": "bets-on",
                "mechanism": "A sentence. B sentence. C sentence. D sentence.",
                "confidence": "low",
                "created_month": "2026-M07",
            }
        )


def test_index_rejects_unknown_repo_reference() -> None:
    data = load_index("examples/2026-M07-EXAMPLE.md").as_plain_data()
    data["couplings"][0]["repo_slug"] = "missing-repo"

    with pytest.raises(ValidationError):
        CouplingIndex.model_validate(data)
