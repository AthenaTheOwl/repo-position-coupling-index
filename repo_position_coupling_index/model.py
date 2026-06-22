from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

MONTH_PATTERN = r"^[0-9]{4}-M(0[1-9]|1[0-2])$"
REPO_PATTERN = r"^[a-z0-9][a-z0-9-]*$"
PILLAR_PATTERN = r"^[A-Z0-9][A-Z0-9-]*$"


class Direction(StrEnum):
    BETS_ON = "bets-on"
    BETS_AGAINST = "bets-against"
    HEDGED = "hedged"
    ORPHAN = "orphan"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AliveStatus(StrEnum):
    ALIVE = "alive"
    QUIET = "quiet"
    DEAD = "dead"


class PillarVerdict(StrEnum):
    CONFIRMING = "confirming"
    WEAKENING = "weakening"
    INVALIDATED = "invalidated"


class FlagType(StrEnum):
    BUILD_ORPHAN = "build-orphan"
    IDEA_ORPHAN = "idea-orphan"
    RE_THESIS_REPO = "re-thesis-repo"
    RE_EXAMINE_PILLAR = "re-examine-pillar"
    HEDGE_FIRED = "hedge-fired"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class CouplingRow(StrictModel):
    repo_slug: str = Field(pattern=REPO_PATTERN)
    pillar_id: str = Field(pattern=PILLAR_PATTERN)
    direction: Direction
    mechanism: str = Field(min_length=12)
    confidence: Confidence
    created_month: str = Field(pattern=MONTH_PATTERN)

    @field_validator("mechanism")
    @classmethod
    def mechanism_has_bounded_sentences(cls, value: str) -> str:
        text = " ".join(value.split())
        sentence_count = sum(text.endswith(mark) for mark in [".", "?", "!"])
        sentence_count += sum(text.count(f"{mark} ") for mark in [".", "?", "!"])
        if sentence_count < 1 or sentence_count > 3:
            raise ValueError("mechanism must be 1-3 sentences")
        return text


class RepoState(StrictModel):
    repo_slug: str = Field(pattern=REPO_PATTERN)
    alive_status: AliveStatus


class PillarState(StrictModel):
    pillar_id: str = Field(pattern=PILLAR_PATTERN)
    current_verdict: PillarVerdict


class Flag(StrictModel):
    flag: FlagType
    reason: str = Field(min_length=8)
    prompt: str = Field(min_length=8)
    repo_slug: str | None = Field(default=None, pattern=REPO_PATTERN)
    pillar_id: str | None = Field(default=None, pattern=PILLAR_PATTERN)

    @model_validator(mode="after")
    def has_target(self) -> "Flag":
        if self.repo_slug is None and self.pillar_id is None:
            raise ValueError("flag must target a repo_slug, a pillar_id, or both")
        return self


class CouplingIndex(StrictModel):
    month: str = Field(pattern=MONTH_PATTERN)
    repo_states: list[RepoState]
    pillar_states: list[PillarState]
    couplings: list[CouplingRow]
    flagged: list[Flag]

    @model_validator(mode="after")
    def references_known_nodes(self) -> "CouplingIndex":
        repo_slugs = {state.repo_slug for state in self.repo_states}
        pillar_ids = {state.pillar_id for state in self.pillar_states}
        errors: list[str] = []

        for row in self.couplings:
            if row.repo_slug not in repo_slugs:
                errors.append(f"unknown repo_slug in coupling: {row.repo_slug}")
            if row.pillar_id not in pillar_ids:
                errors.append(f"unknown pillar_id in coupling: {row.pillar_id}")

        for flag in self.flagged:
            if flag.repo_slug is not None and flag.repo_slug not in repo_slugs:
                errors.append(f"unknown repo_slug in flag: {flag.repo_slug}")
            if flag.pillar_id is not None and flag.pillar_id not in pillar_ids:
                errors.append(f"unknown pillar_id in flag: {flag.pillar_id}")

        if errors:
            raise ValueError("; ".join(errors))
        return self

    def as_plain_data(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)
