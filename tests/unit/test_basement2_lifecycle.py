from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement2_full_pipeline import generate_basement2_full
from isaacmap.basement2_full_pipeline_reference import generate_basement2_full_reference
from isaacmap.basement2_lifecycle import (
    BASEMENT2_LIFECYCLE_STATUS,
    generate_basement2_lifecycle,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.post_layout_lifecycle import run_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config import entries_from_definitions
from isaacmap.room_config_reference import entries_from_definitions_reference


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
ENTRIES = (
    entries_from_definitions(SPECIAL, stage=0)
    + entries_from_definitions(BASEMENT, stage=1)
    + entries_from_definitions(BLUE_WOMB, stage=13)
)
REFERENCE_ENTRIES = (
    entries_from_definitions_reference(SPECIAL, stage=0)
    + entries_from_definitions_reference(BASEMENT, stage=1)
    + entries_from_definitions_reference(BLUE_WOMB, stage=13)
)


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 7, 23))
def test_basement2_post_layout_tail_matches_reference(
    seed: int, difficulty: str
) -> None:
    clean_layout = generate_basement2_full(
        seed,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    reference_layout = generate_basement2_full_reference(
        seed,
        difficulty,
        boss_entries=BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    compare_basement1_full(clean_layout, reference_layout)
    clean = run_post_layout_lifecycle(
        level_rng_state=clean_layout.final_level_rng_state,
        entries=ENTRIES,
        room_config_weights=clean_layout.final_room_config_weights,
        special_room_used_bits=clean_layout.final_special_room_used_bits,
        level_stage=2,
    )
    reference = run_post_layout_lifecycle_reference(
        level_rng_state=reference_layout.final_level,
        entries=REFERENCE_ENTRIES,
        room_config_weights=reference_layout.weights,
        special_room_used_bits=reference_layout.used_bits,
        level_stage=2,
    )
    compare_post_layout_lifecycle(clean, reference)
    assert clean.persistent_level_draw_count == 28
    assert tuple(item.grid_index for item in clean.assignments) == (
        -2, -6, -4, -5, -7, -8, -13, -18,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_basement2_lifecycle_builds_stage_three_handoff(difficulty: str) -> None:
    result = generate_basement2_lifecycle(
        7,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    assert result.completed
    assert result.generation_status == BASEMENT2_LIFECYCLE_STATUS
    assert result.next_run_state.completed_level_stage == 2
    assert result.next_run_state.next_level_stage == 3
    assert len(result.next_run_state.permanent_removed_bosses) == 2
    assert result.next_run_state.boss_pool_rng_states[1] == result.layout.final_boss_pool_state
    assert result.next_run_state.last_floor_level_rng_state == result.post_layout.final_level_rng_state
    assert result.next_run_state.lifecycle == "basement2-success-tail-complete"
