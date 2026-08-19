"""True clean-vs-reference differential for the Depths I accepted layout + tail."""

from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement2_lifecycle import generate_basement2_lifecycle
from isaacmap.boss_pool import DEPTHS_POOL_INDEX, load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.caves1_lifecycle import generate_caves1_lifecycle
from isaacmap.caves2_lifecycle import generate_caves2_lifecycle
from isaacmap.depths1_full_pipeline_reference import generate_depths1_full_reference
from isaacmap.depths1_lifecycle import generate_depths1_lifecycle
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config_reference import entries_from_definitions_reference


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))
CAVES = tuple(load_stb(ROOT / "rooms/04.caves.stb"))
DEPTHS = tuple(load_stb(ROOT / "rooms/07.depths.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
_POOLS = load_boss_pool_xml(ROOT / "bosspools.xml")
BASEMENT_BOSSES = _POOLS["basement"]
CAVES_BOSSES = _POOLS["caves"]
DEPTHS_BOSSES = _POOLS["depths"]


def _refs(entries) -> tuple[BossPoolEntryReference, ...]:
    return tuple(
        BossPoolEntryReference(
            item.boss_id, item.weight, item.initial_weight, item.achievement, item.alternate_boss_id
        )
        for item in entries
    )


BASEMENT_BOSS_REFS = _refs(BASEMENT_BOSSES)
CAVES_BOSS_REFS = _refs(CAVES_BOSSES)
DEPTHS_BOSS_REFS = _refs(DEPTHS_BOSSES)
TAIL_REF_ENTRIES = (
    entries_from_definitions_reference(SPECIAL, stage=0)
    + entries_from_definitions_reference(DEPTHS, stage=7)
    + entries_from_definitions_reference(BLUE_WOMB, stage=13)
)


def _caves2(seed: int, difficulty: str):
    b2 = generate_basement2_lifecycle(
        seed, difficulty, boss_entries=BASEMENT_BOSSES,
        special_definitions=SPECIAL, basement_definitions=BASEMENT, blue_womb_definitions=BLUE_WOMB,
    )
    c1 = generate_caves1_lifecycle(
        b2, basement_boss_entries=BASEMENT_BOSSES, caves_boss_entries=CAVES_BOSSES,
        special_definitions=SPECIAL, basement_definitions=BASEMENT, caves_definitions=CAVES,
        blue_womb_definitions=BLUE_WOMB,
    )
    return generate_caves2_lifecycle(
        c1, basement_boss_entries=BASEMENT_BOSSES, caves_boss_entries=CAVES_BOSSES,
        special_definitions=SPECIAL, basement_definitions=BASEMENT, caves_definitions=CAVES,
        blue_womb_definitions=BLUE_WOMB,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7, 11, 23, 47, 71))
def test_depths1_clean_matches_reference(seed: int, difficulty: str) -> None:
    c2 = _caves2(seed, difficulty)
    d1 = generate_depths1_lifecycle(
        c2,
        depths_boss_entries=DEPTHS_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        blue_womb_definitions=BLUE_WOMB,
    )

    reference = generate_depths1_full_reference(
        seed,
        difficulty,
        basement_boss_entries=BASEMENT_BOSS_REFS,
        caves_boss_entries=CAVES_BOSS_REFS,
        depths_boss_entries=DEPTHS_BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        blue_womb_definitions=BLUE_WOMB,
    )

    compare_basement1_full(d1.layout, reference)

    reference_tail = run_post_layout_lifecycle_reference(
        level_rng_state=reference.final_level,
        entries=TAIL_REF_ENTRIES,
        room_config_weights=reference.weights,
        special_room_used_bits=reference.used_bits,
        level_stage=5,
        room_config_stage=7,
    )
    compare_post_layout_lifecycle(d1.post_layout, reference_tail)

    assert d1.next_run_state.completed_level_stage == 5
    assert d1.next_run_state.next_level_stage == 6
    assert d1.next_run_state.boss_pool_rng_states[DEPTHS_POOL_INDEX] == reference.final_boss


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (75, 125))
def test_depths1_xl_clean_matches_reference(seed: int, difficulty: str) -> None:
    c2 = _caves2(seed, difficulty)
    d1 = generate_depths1_lifecycle(
        c2,
        depths_boss_entries=DEPTHS_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        blue_womb_definitions=BLUE_WOMB,
    )
    # 4 floors + XL second boss = fixed Mom (level 6 switch), which the binary
    # returns before the pool selection, so Mom never joins the removed set.
    assert len(d1.layout.permanent_removed_bosses) == 5
