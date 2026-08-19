"""True clean-vs-reference differentials for the Womb I/II accepted layouts + tails."""

from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement2_lifecycle import generate_basement2_lifecycle
from isaacmap.boss_pool import WOMB_POOL_INDEX, load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.caves1_lifecycle import generate_caves1_lifecycle
from isaacmap.caves2_lifecycle import generate_caves2_lifecycle
from isaacmap.depths1_lifecycle import generate_depths1_lifecycle
from isaacmap.depths2_lifecycle import generate_depths2_lifecycle
from isaacmap.floor_init import derive_womb1_topology_inputs, derive_womb2_topology_inputs
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config_reference import entries_from_definitions_reference
from isaacmap.womb1_full_pipeline_reference import generate_womb1_full_reference
from isaacmap.womb1_lifecycle import generate_womb1_lifecycle
from isaacmap.womb2_full_pipeline_reference import generate_womb2_full_reference
from isaacmap.womb2_lifecycle import generate_womb2_lifecycle


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))
CAVES = tuple(load_stb(ROOT / "rooms/04.caves.stb"))
DEPTHS = tuple(load_stb(ROOT / "rooms/07.depths.stb"))
WOMB = tuple(load_stb(ROOT / "rooms/10.womb.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
_POOLS = load_boss_pool_xml(ROOT / "bosspools.xml")
BASEMENT_BOSSES = _POOLS["basement"]
CAVES_BOSSES = _POOLS["caves"]
DEPTHS_BOSSES = _POOLS["depths"]
WOMB_BOSSES = _POOLS["womb"]


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
WOMB_BOSS_REFS = _refs(WOMB_BOSSES)
TAIL_REF_ENTRIES = (
    entries_from_definitions_reference(SPECIAL, stage=0)
    + entries_from_definitions_reference(DEPTHS, stage=7)
    + entries_from_definitions_reference(WOMB, stage=10)
    + entries_from_definitions_reference(BLUE_WOMB, stage=13)
)


def _depths2(seed: int, difficulty: str):
    b2 = generate_basement2_lifecycle(
        seed, difficulty, boss_entries=BASEMENT_BOSSES,
        special_definitions=SPECIAL, basement_definitions=BASEMENT, blue_womb_definitions=BLUE_WOMB,
    )
    c1 = generate_caves1_lifecycle(
        b2, basement_boss_entries=BASEMENT_BOSSES, caves_boss_entries=CAVES_BOSSES,
        special_definitions=SPECIAL, basement_definitions=BASEMENT, caves_definitions=CAVES,
        blue_womb_definitions=BLUE_WOMB,
    )
    c2 = generate_caves2_lifecycle(
        c1, basement_boss_entries=BASEMENT_BOSSES, caves_boss_entries=CAVES_BOSSES,
        special_definitions=SPECIAL, basement_definitions=BASEMENT, caves_definitions=CAVES,
        blue_womb_definitions=BLUE_WOMB,
    )
    d1 = generate_depths1_lifecycle(
        c2, depths_boss_entries=DEPTHS_BOSSES,
        special_definitions=SPECIAL, basement_definitions=BASEMENT, caves_definitions=CAVES,
        depths_definitions=DEPTHS, blue_womb_definitions=BLUE_WOMB,
    )
    return generate_depths2_lifecycle(
        d1, depths_boss_entries=DEPTHS_BOSSES,
        special_definitions=SPECIAL, basement_definitions=BASEMENT, caves_definitions=CAVES,
        depths_definitions=DEPTHS, blue_womb_definitions=BLUE_WOMB,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7, 11))
def test_womb1_clean_matches_reference(seed: int, difficulty: str) -> None:
    d2 = _depths2(seed, difficulty)
    w1 = generate_womb1_lifecycle(
        d2,
        womb_boss_entries=WOMB_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        womb_definitions=WOMB,
        blue_womb_definitions=BLUE_WOMB,
    )

    reference = generate_womb1_full_reference(
        seed,
        difficulty,
        basement_boss_entries=BASEMENT_BOSS_REFS,
        caves_boss_entries=CAVES_BOSS_REFS,
        depths_boss_entries=DEPTHS_BOSS_REFS,
        womb_boss_entries=WOMB_BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        womb_definitions=WOMB,
        blue_womb_definitions=BLUE_WOMB,
    )

    compare_basement1_full(w1.layout, reference)

    reference_tail = run_post_layout_lifecycle_reference(
        level_rng_state=reference.final_level,
        entries=TAIL_REF_ENTRIES,
        room_config_weights=reference.weights,
        special_room_used_bits=reference.used_bits,
        level_stage=7,
        room_config_stage=10,
    )
    compare_post_layout_lifecycle(w1.post_layout, reference_tail)

    assert w1.next_run_state.completed_level_stage == 7
    assert w1.next_run_state.next_level_stage == 8
    assert w1.next_run_state.boss_pool_rng_states[WOMB_POOL_INDEX] == reference.final_boss


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7, 11))
def test_womb2_clean_matches_reference(seed: int, difficulty: str) -> None:
    d2 = _depths2(seed, difficulty)
    w1 = generate_womb1_lifecycle(
        d2,
        womb_boss_entries=WOMB_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        womb_definitions=WOMB,
        blue_womb_definitions=BLUE_WOMB,
    )
    w2 = generate_womb2_lifecycle(
        w1,
        womb_boss_entries=WOMB_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        womb_definitions=WOMB,
        blue_womb_definitions=BLUE_WOMB,
    )
    reference = generate_womb2_full_reference(
        seed,
        difficulty,
        basement_boss_entries=BASEMENT_BOSS_REFS,
        caves_boss_entries=CAVES_BOSS_REFS,
        depths_boss_entries=DEPTHS_BOSS_REFS,
        womb_boss_entries=WOMB_BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        womb_definitions=WOMB,
        blue_womb_definitions=BLUE_WOMB,
    )

    compare_basement1_full(w2.layout, reference)

    reference_tail = run_post_layout_lifecycle_reference(
        level_rng_state=reference.final_level,
        entries=TAIL_REF_ENTRIES,
        room_config_weights=reference.weights,
        special_room_used_bits=reference.used_bits,
        level_stage=8,
        room_config_stage=10,
    )
    compare_post_layout_lifecycle(w2.post_layout, reference_tail)

    assert w2.next_run_state.completed_level_stage == 8
    assert w2.next_run_state.next_level_stage == 9
    assert w2.next_run_state.boss_pool_rng_states[WOMB_POOL_INDEX] == reference.final_boss


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_womb1_xl_seed_matches_reference(difficulty: str) -> None:
    """Targeted XL Womb I: a Labyrinth-curse seed found by scanning."""
    xl_seed = next(
        (seed for seed in range(1, 10_001)
         if derive_womb1_topology_inputs(seed, difficulty).is_xl),
        None,
    )
    if xl_seed is None:
        raise AssertionError(f"no XL Womb I seed found in {difficulty}")
    inputs = derive_womb1_topology_inputs(xl_seed, difficulty)
    if difficulty == "NORMAL":
        assert inputs.target_room_count == 36
    else:
        assert inputs.target_room_count in (38, 39)
    assert inputs.required_dead_ends == 7
    d2 = _depths2(xl_seed, difficulty)
    w1 = generate_womb1_lifecycle(
        d2,
        womb_boss_entries=WOMB_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        womb_definitions=WOMB,
        blue_womb_definitions=BLUE_WOMB,
    )
    reference = generate_womb1_full_reference(
        xl_seed,
        difficulty,
        basement_boss_entries=BASEMENT_BOSS_REFS,
        caves_boss_entries=CAVES_BOSS_REFS,
        depths_boss_entries=DEPTHS_BOSS_REFS,
        womb_boss_entries=WOMB_BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        depths_definitions=DEPTHS,
        womb_definitions=WOMB,
        blue_womb_definitions=BLUE_WOMB,
    )
    compare_basement1_full(w1.layout, reference)


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_womb2_never_xl(difficulty: str) -> None:
    for seed in range(1, 10_001):
        assert not derive_womb2_topology_inputs(seed, difficulty).is_xl
