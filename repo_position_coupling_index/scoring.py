from __future__ import annotations

from collections import defaultdict

from repo_position_coupling_index.model import (
    AliveStatus,
    CouplingIndex,
    Direction,
    Flag,
    FlagType,
    PillarVerdict,
)


def compute_flags(index: CouplingIndex) -> list[Flag]:
    repo_edges: dict[str, list[tuple[str, Direction]]] = defaultdict(list)
    pillar_edges: dict[str, list[tuple[str, Direction]]] = defaultdict(list)

    for row in index.couplings:
        if row.direction == Direction.ORPHAN:
            continue
        repo_edges[row.repo_slug].append((row.pillar_id, Direction(row.direction)))
        pillar_edges[row.pillar_id].append((row.repo_slug, Direction(row.direction)))

    repo_status = {state.repo_slug: AliveStatus(state.alive_status) for state in index.repo_states}
    pillar_status = {
        state.pillar_id: PillarVerdict(state.current_verdict) for state in index.pillar_states
    }

    flags: list[Flag] = []

    for state in sorted(index.repo_states, key=lambda item: item.repo_slug):
        if not repo_edges.get(state.repo_slug):
            flags.append(
                Flag(
                    flag=FlagType.BUILD_ORPHAN,
                    repo_slug=state.repo_slug,
                    reason="Repo has no non-orphan pillar coupling.",
                    prompt="Decide whether this repo needs a pillar link or should stay uncoupled.",
                )
            )

    for state in sorted(index.pillar_states, key=lambda item: item.pillar_id):
        if not pillar_edges.get(state.pillar_id):
            flags.append(
                Flag(
                    flag=FlagType.IDEA_ORPHAN,
                    pillar_id=state.pillar_id,
                    reason="Pillar has no non-orphan repo coupling.",
                    prompt="Decide whether the pillar is active without a repo testing it.",
                )
            )

    for row in sorted(index.couplings, key=lambda item: (item.repo_slug, item.pillar_id)):
        if row.direction == Direction.ORPHAN:
            continue
        if (
            repo_status[row.repo_slug] == AliveStatus.ALIVE
            and pillar_status[row.pillar_id] == PillarVerdict.INVALIDATED
        ):
            flags.append(
                Flag(
                    flag=FlagType.RE_THESIS_REPO,
                    repo_slug=row.repo_slug,
                    pillar_id=row.pillar_id,
                    reason="Repo is alive while its coupled pillar is invalidated.",
                    prompt="Open the repo thesis and decide what still holds.",
                )
            )

    for state in sorted(index.pillar_states, key=lambda item: item.pillar_id):
        edges = pillar_edges.get(state.pillar_id, [])
        if not edges or pillar_status[state.pillar_id] != PillarVerdict.CONFIRMING:
            continue
        if all(repo_status[repo_slug] == AliveStatus.DEAD for repo_slug, _direction in edges):
            flags.append(
                Flag(
                    flag=FlagType.RE_EXAMINE_PILLAR,
                    pillar_id=state.pillar_id,
                    reason="Pillar is confirming while every coupled repo is dead.",
                    prompt="Check whether the pillar verdict came from evidence outside these repos.",
                )
            )

    for row in sorted(index.couplings, key=lambda item: (item.repo_slug, item.pillar_id)):
        if (
            Direction(row.direction) == Direction.BETS_AGAINST
            and pillar_status[row.pillar_id] == PillarVerdict.CONFIRMING
        ):
            flags.append(
                Flag(
                    flag=FlagType.HEDGE_FIRED,
                    repo_slug=row.repo_slug,
                    pillar_id=row.pillar_id,
                    reason="Repo bets against a pillar that is confirming.",
                    prompt="Decide whether the hedge worked or the position should change.",
                )
            )

    return flags


def with_computed_flags(index: CouplingIndex) -> CouplingIndex:
    data = index.as_plain_data()
    data["flagged"] = [flag.model_dump(mode="json", exclude_none=True) for flag in compute_flags(index)]
    return CouplingIndex.model_validate(data)
