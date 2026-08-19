from __future__ import annotations

from pathlib import Path
import struct

import pytest

from isaacmap.basement1_secret_pipeline_differential import compare_secret_pipeline
from isaacmap.basement2_secret_pipeline import (
    BASEMENT2_SECRET_STATUS,
    EXTERNAL_VALIDATION,
    generate_basement2_through_secret,
)
from isaacmap.basement2_secret_pipeline_reference import (
    generate_basement2_through_secret_reference,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.generation_state import BASEMENT2_PLANETARIUM_CHANCE_F32
from isaacmap.resources import load_stb


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
BOSSES = load_boss_pool_xml(ROOT / "bosspools.xml")["basement"]
BOSS_REFS = tuple(
    BossPoolEntryReference(
        entry.boss_id,
        entry.weight,
        entry.initial_weight,
        entry.achievement,
        entry.alternate_boss_id,
    )
    for entry in BOSSES
)


def _clean(seed: int, difficulty: str):
    return generate_basement2_through_secret(
        seed,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )


def _reference(seed: int, difficulty: str):
    return generate_basement2_through_secret_reference(
        seed,
        difficulty,
        boss_entries=BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 3, 5, 7, 23))
def test_basement2_through_secret_matches_independent_reference(
    seed: int, difficulty: str
) -> None:
    clean = _clean(seed, difficulty)
    compare_secret_pipeline(clean, _reference(seed, difficulty))
    assert clean.boundary_completed
    assert clean.generation_status == BASEMENT2_SECRET_STATUS
    assert clean.external_validation == EXTERNAL_VALIDATION
    assert clean.replayed_basement1.next_run_state.next_level_stage == 2
    assert len(clean.permanent_removed_bosses) == 1
    assert len(clean.pending_boss_blacklist) == 1
    assert clean.pending_boss_blacklist[0] not in clean.permanent_removed_bosses
    assert clean.rooms == clean.attempts[-1].through_secret.rooms


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize(
    ("seed", "room_type"),
    ((2, 20), (3, 6), (5, 24), (7, 11)),
)
def test_stage_two_special_room_branch_examples(
    seed: int, room_type: int, difficulty: str
) -> None:
    result = _clean(seed, difficulty)
    assert any(room.room_type == room_type for room in result.rooms)


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_retry_result_exposes_only_accepted_stage_two_attempt(
    difficulty: str,
) -> None:
    result = _clean(23, difficulty)
    assert len(result.attempts) == 2
    assert result.attempts[0].through_secret is None
    assert result.attempts[1].through_secret is not None
    assert result.rooms == result.attempts[1].through_secret.rooms


def test_stage_two_planetarium_chance_preserves_binary_float32_order() -> None:
    assert struct.pack("<f", BASEMENT2_PLANETARIUM_CHANCE_F32).hex() == "3e0a573e"
    assert struct.pack("<f", 0.21).hex() == "3d0a573e"
