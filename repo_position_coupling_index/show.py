from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.model import (
    AliveStatus,
    Confidence,
    CouplingIndex,
    Direction,
)

DEFAULT_REPORT = "coupling_index/2026-M07.md"

CONFIDENCE_WEIGHT = {
    Confidence.LOW.value: 1,
    Confidence.MEDIUM.value: 2,
    Confidence.HIGH.value: 3,
}


def default_report_path() -> Path:
    """Locate the committed report, whether run from repo root or elsewhere."""
    here = Path(__file__).resolve().parent.parent
    candidate = here / DEFAULT_REPORT
    if candidate.exists():
        return candidate
    return Path(DEFAULT_REPORT)


def rank_pillars(index: CouplingIndex) -> list[dict[str, object]]:
    """Rank pillars by live exposure: alive repos betting on them, weighted by confidence."""
    alive = {s.repo_slug: AliveStatus(s.alive_status) for s in index.repo_states}
    verdict = {s.pillar_id: s.current_verdict for s in index.pillar_states}

    repos_for: dict[str, set[str]] = defaultdict(set)
    exposure: dict[str, int] = defaultdict(int)
    for row in index.couplings:
        if Direction(row.direction) == Direction.ORPHAN:
            continue
        repos_for[row.pillar_id].add(row.repo_slug)
        if alive.get(row.repo_slug) == AliveStatus.ALIVE:
            exposure[row.pillar_id] += CONFIDENCE_WEIGHT.get(row.confidence, 1)

    rows: list[dict[str, object]] = []
    for state in index.pillar_states:
        pid = state.pillar_id
        rows.append(
            {
                "pillar_id": pid,
                "verdict": verdict.get(pid, "-"),
                "repos": len(repos_for.get(pid, set())),
                "exposure": exposure.get(pid, 0),
            }
        )
    rows.sort(key=lambda r: (-int(r["exposure"]), -int(r["repos"]), str(r["pillar_id"])))
    return rows


def headline(index: CouplingIndex, ranked: list[dict[str, object]]) -> str:
    n_flags = len(index.flagged)
    if not ranked:
        return f"{index.month}: no pillars tracked, {n_flags} open flags."
    top = ranked[0]
    weakening = [r for r in ranked if r["verdict"] in ("weakening", "invalidated")]
    weak_clause = ""
    if weakening:
        names = ", ".join(str(r["pillar_id"]) for r in weakening)
        weak_clause = f" {len(weakening)} pillar(s) softening: {names}."
    return (
        f"{index.month}: {top['pillar_id']} carries the most live build exposure "
        f"(exposure {top['exposure']}, {top['repos']} repos), verdict {top['verdict']}."
        f"{weak_clause} {n_flags} open flag(s) need a decision."
    )


def _table(rows: list[list[str]], headers: list[str]) -> str:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    line = lambda cells: "  ".join(c.ljust(widths[i]) for i, c in enumerate(cells))
    out = [line(headers), line(["-" * w for w in widths])]
    out.extend(line(r) for r in rows)
    return "\n".join(out)


def render_show(index: CouplingIndex) -> str:
    ranked = rank_pillars(index)
    pillar_rows = [
        [
            str(r["pillar_id"]),
            str(r["verdict"]),
            str(r["repos"]),
            str(r["exposure"]),
        ]
        for r in ranked
    ]
    pillar_table = _table(pillar_rows, ["pillar", "verdict", "repos", "exposure"])

    flag_rows = [
        [f.flag, f.repo_slug or "-", f.pillar_id or "-", f.reason]
        for f in index.flagged
    ]
    if flag_rows:
        flag_table = _table(flag_rows, ["flag", "repo", "pillar", "reason"])
    else:
        flag_table = "(no open flags)"

    parts = [
        f"coupling index - {index.month}",
        f"{len(index.couplings)} couplings, {len(index.repo_states)} repos, "
        f"{len(index.pillar_states)} pillars, {len(index.flagged)} flags",
        "",
        "pillars by live build exposure (most-bet-on first):",
        pillar_table,
        "",
        "open flags:",
        flag_table,
        "",
        headline(index, ranked),
    ]
    return "\n".join(parts) + "\n"


def show_report(path: str | Path | None = None) -> str:
    report_path = Path(path) if path else default_report_path()
    index = load_index(report_path)
    return render_show(index)
