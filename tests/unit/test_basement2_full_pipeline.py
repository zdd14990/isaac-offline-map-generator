from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement2_full_pipeline import (
    BASEMENT2_LAYOUT_STATUS,
    EXTERNAL_VALIDATION,
    generate_basement2_full,
)
from isaacmap.basement2_full_pipeline_reference import generate_basement2_full_reference
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
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
    return generate_basement2_full(
        seed,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )


def _reference(seed: int, difficulty: str):
    return generate_basement2_full_reference(
        seed,
        difficulty,
        boss_entries=BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7, 23, 27))
def test_basement2_accepted_layout_matches_independent_reference(
    seed: int, difficulty: str
) -> None:
    clean = _clean(seed, difficulty)
    compare_basement1_full(clean, _reference(seed, difficulty))
    assert clean.completed
    assert clean.generation_status == BASEMENT2_LAYOUT_STATUS
    assert clean.external_validation == EXTERNAL_VALIDATION
    assert clean.accepted_attempt_index == len(clean.attempts) - 1
    assert clean.rooms == clean.attempts[-1].late_default.rooms
    assert clean.descriptor_configs == clean.attempts[-1].late_default.descriptor_configs
    assert len(clean.descriptor_configs) == len(clean.rooms)
    assert len(clean.permanent_removed_bosses) == 2
    assert clean.pending_boss_blacklist == ()


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_basement2_retry_does_not_leak_failed_attempt_layout(
    difficulty: str,
) -> None:
    result = _clean(23, difficulty)
    assert len(result.attempts) == 2
    assert result.attempts[0].late_default is None
    assert result.rooms == result.attempts[1].late_default.rooms
    assert result.room_map == result.attempts[1].through_ultra.room_map


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_basement2_ultra_uses_final_stage_two_descriptor_collection(
    difficulty: str,
) -> None:
    result = _clean(1, difficulty)
    ultra = result.attempts[-1].through_ultra
    assert ultra is not None
    assert ultra.ultra_room >= 0
    assert result.rooms[ultra.ultra_room].room_type == 29
