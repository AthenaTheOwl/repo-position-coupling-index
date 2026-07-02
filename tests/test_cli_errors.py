from __future__ import annotations

import pytest

from repo_position_coupling_index.cli import main


def test_show_missing_path_exits_with_message(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["show", "does-not-exist.md"])

    assert exc.value.code != 0
    assert "cannot read report does-not-exist.md" in str(exc.value)


def test_render_directory_path_exits_with_message() -> None:
    # a directory instead of a file: OSError from read_text
    with pytest.raises(SystemExit) as exc:
        main(["render", "examples"])

    assert exc.value.code != 0
    assert "cannot read report examples" in str(exc.value)


def test_validate_non_front_matter_exits_with_message() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["validate", "README.md"])

    assert exc.value.code != 0
    assert "invalid report README.md" in str(exc.value)
    assert "must start with YAML front matter" in str(exc.value)


def test_render_schema_invalid_report_exits_with_message(tmp_path) -> None:
    bad = tmp_path / "bad.md"
    bad.write_text(
        "---\n"
        "month: not-a-month\n"
        "repo_states: []\n"
        "pillar_states: []\n"
        "couplings: []\n"
        "flagged: []\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit) as exc:
        main(["render", str(bad)])

    assert exc.value.code != 0
    assert "invalid report" in str(exc.value)
    assert "month" in str(exc.value)
