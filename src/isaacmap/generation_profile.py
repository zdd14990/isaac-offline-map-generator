"""Explicit, reproducible inputs that affect floor generation."""

from __future__ import annotations

from dataclasses import dataclass
import os


GENERATION_PROFILE_ENV = "ISAAC_MAP_GENERATION_PROFILE"


@dataclass(frozen=True)
class RunGenerationProfile:
    """Binary-confirmed curse-rate tier for one reproducible run profile.

    The executable contains all four denominator pairs below. Their exact
    save-flag names are not fully mapped, so profiles are named by the values
    they supply rather than by inferred achievement labels.
    """

    name: str
    normal_curse_rate: int
    hard_curse_rate: int

    @property
    def fingerprint(self) -> str:
        return f"{self.name}:{self.normal_curse_rate}:{self.hard_curse_rate}"

    def curse_rate(self, difficulty: str) -> int:
        if difficulty == "NORMAL":
            return self.normal_curse_rate
        if difficulty == "HARD":
            return self.hard_curse_rate
        raise ValueError("difficulty must be NORMAL or HARD")


BASE_80_40 = RunGenerationProfile("BASE_80_40", 80, 40)
RATE_30_20 = RunGenerationProfile("RATE_30_20", 30, 20)
RATE_10_6 = RunGenerationProfile("RATE_10_6", 10, 6)
RATE_5_3 = RunGenerationProfile("RATE_5_3", 5, 3)

RUN_GENERATION_PROFILES = {
    profile.name: profile
    for profile in (BASE_80_40, RATE_30_20, RATE_10_6, RATE_5_3)
}
DEFAULT_RUN_GENERATION_PROFILE = BASE_80_40


def resolve_run_generation_profile(
    value: RunGenerationProfile | str | None = None,
) -> RunGenerationProfile:
    """Resolve an explicit profile or the process-level configured profile."""

    if isinstance(value, RunGenerationProfile):
        return value
    name = value
    if name is None:
        name = os.environ.get(
            GENERATION_PROFILE_ENV, DEFAULT_RUN_GENERATION_PROFILE.name
        )
    normalized = str(name).strip().upper()
    profile = RUN_GENERATION_PROFILES.get(normalized)
    if profile is None:
        supported = ", ".join(RUN_GENERATION_PROFILES)
        raise ValueError(
            f"unknown {GENERATION_PROFILE_ENV} {name!r}; expected one of: {supported}"
        )
    return profile
