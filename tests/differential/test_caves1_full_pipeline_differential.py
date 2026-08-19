"""True clean-vs-reference differential for the Caves I accepted layout + tail."""

from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement2_lifecycle import generate_basement2_lifecycle
from isaacmap.boss_pool import CAVES_POOL_INDEX, load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.caves1_full_pipeline_reference import generate_caves1_full_reference
from isaacmap.caves1_lifecycle import generate_caves1_lifecycle
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config_reference import entries_from_definitions_reference


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))
CAVES = tuple(load_stb(ROOT / "rooms/04.caves.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
_POOLS = load_boss_pool_xml(ROOT / "bosspools.xml")
BASEMENT_BOSSES = _POOLS["basement"]
CAVES_BOSSES = _POOLS["caves"]


def _refs(entries) -> tuple[BossPoolEntryReference, ...]:
    return tuple(
        BossPoolEntryReference(
            item.boss_id,
            item.weight,
            item.initial_weight,
            item.achievement,
            item.alternate_boss_id,
        )
        for item in entries
    )


BASEMENT_BOSS_REFS = _refs(BASEMENT_BOSSES)
CAVES_BOSS_REFS = _refs(CAVES_BOSSES)
TAIL_REF_ENTRIES = (
    entries_from_definitions_reference(SPECIAL, stage=0)
    + entries_from_definitions_reference(CAVES, stage=4)
    + entries_from_definitions_reference(BLUE_WOMB, stage=13)
)


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7, 11, 23, 47, 71))
def test_caves1_clean_matches_reference(seed: int, difficulty: str) -> None:
    b2 = generate_basement2_lifecycle(
        seed,
        difficulty,
        boss_entries=BASEMENT_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    c1 = generate_caves1_lifecycle(
        b2,
        basement_boss_entries=BASEMENT_BOSSES,
        caves_boss_entries=CAVES_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        blue_womb_definitions=BLUE_WOMB,
    )

    reference = generate_caves1_full_reference(
        seed,
        difficulty,
        basement_boss_entries=BASEMENT_BOSS_REFS,
        caves_boss_entries=CAVES_BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        blue_womb_definitions=BLUE_WOMB,
    )

    compare_basement1_full(c1.layout, reference)

    reference_tail = run_post_layout_lifecycle_reference(
        level_rng_state=reference.final_level,
        entries=TAIL_REF_ENTRIES,
        room_config_weights=reference.weights,
        special_room_used_bits=reference.used_bits,
        level_stage=3,
        room_config_stage=4,
    )
    compare_post_layout_lifecycle(c1.post_layout, reference_tail)

    # Next-floor snapshot: the Caves pool (4) final state must propagate.
    assert c1.next_run_state.completed_level_stage == 3
    assert c1.next_run_state.next_level_stage == 4
    assert c1.next_run_state.boss_pool_rng_states[CAVES_POOL_INDEX] == reference.final_boss
