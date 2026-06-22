from __future__ import annotations

from repo_position_coupling_index.frontmatter import dump_front_matter
from repo_position_coupling_index.model import CouplingIndex


def render_index(index: CouplingIndex) -> str:
    lines: list[str] = [dump_front_matter(index).rstrip(), "", f"# Coupling Index - {index.month}", ""]

    lines.extend(
        [
            "## Repo states",
            "",
            "| Repo | Alive status |",
            "|---|---|",
        ]
    )
    for state in index.repo_states:
        lines.append(f"| `{state.repo_slug}` | {state.alive_status} |")

    lines.extend(
        [
            "",
            "## Pillar states",
            "",
            "| Pillar | Current verdict |",
            "|---|---|",
        ]
    )
    for state in index.pillar_states:
        lines.append(f"| `{state.pillar_id}` | {state.current_verdict} |")

    lines.extend(
        [
            "",
            "## Couplings",
            "",
            "| Repo | Pillar | Direction | Confidence | Mechanism |",
            "|---|---|---|---|---|",
        ]
    )
    for row in index.couplings:
        mechanism = row.mechanism.replace("|", "\\|")
        lines.append(
            f"| `{row.repo_slug}` | `{row.pillar_id}` | {row.direction} | "
            f"{row.confidence} | {mechanism} |"
        )

    lines.extend(
        [
            "",
            "## Flagged misalignments",
            "",
            "| Flag | Repo | Pillar | Reason | Prompt |",
            "|---|---|---|---|---|",
        ]
    )
    if index.flagged:
        for flag in index.flagged:
            repo = f"`{flag.repo_slug}`" if flag.repo_slug else ""
            pillar = f"`{flag.pillar_id}`" if flag.pillar_id else ""
            reason = flag.reason.replace("|", "\\|")
            prompt = flag.prompt.replace("|", "\\|")
            lines.append(f"| {flag.flag} | {repo} | {pillar} | {reason} | {prompt} |")
    else:
        lines.append("| none |  |  | No flags from the current rule set. | No action. |")

    return "\n".join(lines).rstrip() + "\n"
