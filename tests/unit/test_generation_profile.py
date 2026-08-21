from __future__ import annotations

import pytest

from isaacmap.bot_api import _version_token
from isaacmap.generation_profile import (
    BASE_80_40,
    GENERATION_PROFILE_ENV,
    RATE_10_6,
    RATE_30_20,
    RATE_5_3,
    resolve_run_generation_profile,
)


def test_binary_confirmed_curse_rate_tiers() -> None:
    assert (BASE_80_40.curse_rate("NORMAL"), BASE_80_40.curse_rate("HARD")) == (
        80,
        40,
    )
    assert (RATE_30_20.curse_rate("NORMAL"), RATE_30_20.curse_rate("HARD")) == (
        30,
        20,
    )
    assert (RATE_10_6.curse_rate("NORMAL"), RATE_10_6.curse_rate("HARD")) == (
        10,
        6,
    )
    assert (RATE_5_3.curse_rate("NORMAL"), RATE_5_3.curse_rate("HARD")) == (5, 3)


def test_process_profile_is_explicit_and_defaults_to_base(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(GENERATION_PROFILE_ENV, raising=False)
    assert resolve_run_generation_profile() is BASE_80_40
    monkeypatch.setenv(GENERATION_PROFILE_ENV, "rate_5_3")
    assert resolve_run_generation_profile() is RATE_5_3


def test_invalid_process_profile_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(GENERATION_PROFILE_ENV, "UNKNOWN")
    with pytest.raises(ValueError, match="unknown ISAAC_MAP_GENERATION_PROFILE"):
        resolve_run_generation_profile()


def test_generation_profile_changes_cache_version_token() -> None:
    assert _version_token(BASE_80_40) != _version_token(RATE_5_3)
