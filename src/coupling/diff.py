from __future__ import annotations

from dataclasses import dataclass

from coupling.schema import CouplingIndex, CouplingRow, Flag


@dataclass(frozen=True)
class CouplingKey:
    repo_slug: str
    pillar_id: str


@dataclass(frozen=True)
class FlagKey:
    flag: str
    repo_slug: str | None
    pillar_id: str | None


def _coupling_map(index: CouplingIndex) -> dict[CouplingKey, CouplingRow]:
    return {CouplingKey(row.repo_slug, row.pillar_id): row for row in index.couplings}


def _flag_map(index: CouplingIndex) -> dict[FlagKey, Flag]:
    return {FlagKey(flag.flag, flag.repo_slug, flag.pillar_id): flag for flag in index.flagged}


def render_diff(previous: CouplingIndex, current: CouplingIndex) -> str:
    previous_couplings = _coupling_map(previous)
    current_couplings = _coupling_map(current)
    previous_flags = _flag_map(previous)
    current_flags = _flag_map(current)

    added = sorted(set(current_couplings) - set(previous_couplings), key=lambda key: (key.repo_slug, key.pillar_id))
    removed = sorted(set(previous_couplings) - set(current_couplings), key=lambda key: (key.repo_slug, key.pillar_id))
    shared = sorted(set(previous_couplings) & set(current_couplings), key=lambda key: (key.repo_slug, key.pillar_id))
    changed = [
        key
        for key in shared
        if previous_couplings[key].direction != current_couplings[key].direction
    ]

    flags_added = sorted(
        set(current_flags) - set(previous_flags),
        key=lambda key: (key.flag, key.repo_slug or "", key.pillar_id or ""),
    )
    flags_cleared = sorted(
        set(previous_flags) - set(current_flags),
        key=lambda key: (key.flag, key.repo_slug or "", key.pillar_id or ""),
    )

    lines = [f"# Coupling Diff - {previous.month} to {current.month}", ""]
    lines.extend(_section("Added couplings", (_format_coupling(current_couplings[key]) for key in added)))
    lines.extend(
        _section("Removed couplings", (_format_coupling(previous_couplings[key]) for key in removed))
    )
    lines.extend(
        _section(
            "Direction changes",
            (
                f"- `{key.repo_slug}` -> `{key.pillar_id}`: "
                f"{previous_couplings[key].direction} -> {current_couplings[key].direction}"
                for key in changed
            ),
        )
    )
    lines.extend(_section("Added flags", (_format_flag(current_flags[key]) for key in flags_added)))
    lines.extend(_section("Cleared flags", (_format_flag(previous_flags[key]) for key in flags_cleared)))
    return "\n".join(lines).rstrip() + "\n"


def _section(title: str, rows: object) -> list[str]:
    items = list(rows)
    output = [f"## {title}", ""]
    if items:
        output.extend(str(item) for item in items)
    else:
        output.append("- none")
    output.append("")
    return output


def _format_coupling(row: CouplingRow) -> str:
    return f"- `{row.repo_slug}` -> `{row.pillar_id}` ({row.direction}, {row.confidence})"


def _format_flag(flag: Flag) -> str:
    repo = flag.repo_slug or "-"
    pillar = flag.pillar_id or "-"
    return f"- {flag.flag}: repo `{repo}`, pillar `{pillar}`"
