from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_pipeline_differential import compare_pipeline
from isaacmap.basement2_pipeline import (
    BASEMENT2_TREASURE_STATUS,
    EXTERNAL_VALIDATION,
    generate_basement2_through_treasure,
)
from isaacmap.basement2_pipeline_reference import (
    generate_basement2_through_treasure_reference,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.resources import load_stb
from isaacmap.room_config import entries_from_definitions


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


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 7, 27))
def test_basement2_through_treasure_matches_reference(
    seed: int, difficulty: str
) -> None:
    clean = generate_basement2_through_treasure(
        seed,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    reference = generate_basement2_through_treasure_reference(
        seed,
        difficulty,
        boss_entries=BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    compare_pipeline(clean, reference)
    assert clean.completed
    assert clean.generation_status == BASEMENT2_TREASURE_STATUS
    assert clean.external_validation == EXTERNAL_VALIDATION
    assert clean.replayed_basement1.next_run_state.next_level_stage == 2
    assert len(clean.permanent_removed_bosses) == 1
    assert len(clean.pending_boss_blacklist) == 1
    assert clean.pending_boss_blacklist[0] not in clean.permanent_removed_bosses


def test_basement2_boundary_does_not_commit_current_attempt_boss() -> None:
    result = generate_basement2_through_treasure(
        7,
        "NORMAL",
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    assert result.permanent_removed_bosses == (84,)
    assert result.pending_boss_blacklist == (56,)


def test_basement2_entry_resets_only_current_room_config_stage() -> None:
    result = generate_basement2_through_treasure(
        7,
        "NORMAL",
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    entry = dict(result.entry_room_config_weights)
    inherited = dict(result.replayed_basement1.next_run_state.room_config_weights)
    for config in entries_from_definitions(BASEMENT, stage=1):
        assert entry[config.key] == config.initial_weight
    for config in entries_from_definitions(SPECIAL, stage=0):
        assert entry[config.key] == inherited[config.key]
