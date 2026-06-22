from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from coupling.schema import CouplingIndex


class FrontMatterError(ValueError):
    pass


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise FrontMatterError("report must start with YAML front matter")

    try:
        _, yaml_text, body = text.split("---\n", 2)
    except ValueError as exc:
        raise FrontMatterError("report front matter is not closed") from exc

    data = yaml.safe_load(yaml_text) or {}
    if not isinstance(data, dict):
        raise FrontMatterError("report front matter must be a mapping")
    return data, body.lstrip("\n")


def load_index(path: str | Path) -> CouplingIndex:
    report_path = Path(path)
    data, _body = split_front_matter(report_path.read_text(encoding="utf-8"))
    return CouplingIndex.model_validate(data)


def dump_front_matter(index: CouplingIndex) -> str:
    yaml_text = yaml.safe_dump(
        index.as_plain_data(),
        allow_unicode=False,
        sort_keys=False,
        width=100,
    )
    return f"---\n{yaml_text}---\n"

