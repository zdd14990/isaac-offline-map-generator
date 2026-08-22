"""True clean-vs-reference differential for the Downpour I accepted layout + tail."""

from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.boss_pool import DOWNPOUR_POOL_INDEX, load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.downpour1_full_pipeline_reference import generate_downpour1_full_reference
from isaacmap.downpour1_lifecycle import generate_downpour1_lifecycle
from isaacmap.floor_init import derive_alt_topology_inputs
from isaacmap.generation_profile import GENERATION_PROFILE_ENV
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config_reference import entries_from_definitions_reference
from isaacmap.seed import decode_seed
from isaacmap.topology import generate_topology_research


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
DOWNPOUR = tuple(load_stb(ROOT / "rooms/27.downpour.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
_POOLS = load_boss_pool_xml(ROOT / "bosspools.xml")
DOWNPOUR_BOSSES = _POOLS["downpour"]


def _refs(entries) -> tuple[BossPoolEntryReference, ...]:
    return tuple(
        BossPoolEntryReference(
            item.boss_id, item.weight, item.initial_weight, item.achievement, item.alternate_boss_id
        )
        for item in entries
    )


DOWNPOUR_BOSS_REFS = _refs(DOWNPOUR_BOSSES)
TAIL_REF_ENTRIES = (
    entries_from_definitions_reference(SPECIAL, stage=0)
    + entries_from_definitions_reference(BLUE_WOMB, stage=13)
)


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7, 11, 23, 47, 71))
def test_downpour1_clean_matches_reference(seed: int, difficulty: str) -> None:
    clean = generate_downpour1_lifecycle(
        seed,
        difficulty,
        downpour_boss_entries=DOWNPOUR_BOSSES,
        special_definitions=SPECIAL,
        downpour_definitions=DOWNPOUR,
        blue_womb_definitions=BLUE_WOMB,
    )

    reference = generate_downpour1_full_reference(
        seed,
        difficulty,
        downpour_boss_entries=DOWNPOUR_BOSS_REFS,
        special_definitions=SPECIAL,
        downpour_definitions=DOWNPOUR,
    )

    compare_basement1_full(clean.layout, reference)

    reference_tail = run_post_layout_lifecycle_reference(
        level_rng_state=reference.final_level,
        entries=TAIL_REF_ENTRIES,
        room_config_weights=reference.weights,
        special_room_used_bits=reference.used_bits,
        level_stage=1,
        stage_type=4,
        room_config_stage=27,
    )
    compare_post_layout_lifecycle(clean.post_layout, reference_tail)

    assert clean.next_run_state.completed_level_stage == 1
    assert clean.next_run_state.next_level_stage == 2
    assert clean.next_run_state.boss_pool_rng_states[DOWNPOUR_POOL_INDEX] == reference.final_boss


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_downpour1_xl_seed_matches_reference(difficulty: str) -> None:
    xl_seed = next(
        (seed for seed in range(1, 20_001)
         if derive_alt_topology_inputs(1, 4, seed, difficulty).is_xl),
        None,
    )
    if xl_seed is None:
        raise AssertionError(f"no XL Downpour I seed found in {difficulty}")
    clean = generate_downpour1_lifecycle(
        xl_seed,
        difficulty,
        downpour_boss_entries=DOWNPOUR_BOSSES,
        special_definitions=SPECIAL,
        downpour_definitions=DOWNPOUR,
        blue_womb_definitions=BLUE_WOMB,
    )
    reference = generate_downpour1_full_reference(
        xl_seed,
        difficulty,
        downpour_boss_entries=DOWNPOUR_BOSS_REFS,
        special_definitions=SPECIAL,
        downpour_definitions=DOWNPOUR,
    )
    compare_basement1_full(clean.layout, reference)


def test_dkm_rate3_full_pipeline_uses_xl_topology_state(monkeypatch) -> None:
    """The full pipeline must propagate Labyrinth into LevelGenerator."""

    monkeypatch.setenv(GENERATION_PROFILE_ENV, "RATE_5_3")
    start_seed = decode_seed("DKM8 9MNM")
    inputs = derive_alt_topology_inputs(
        1, 4, start_seed, "HARD", generation_profile="RATE_5_3"
    )
    assert inputs.is_xl

    generated = generate_downpour1_lifecycle(
        start_seed,
        "HARD",
        downpour_boss_entries=DOWNPOUR_BOSSES,
        special_definitions=SPECIAL,
        downpour_definitions=DOWNPOUR,
        blue_womb_definitions=BLUE_WOMB,
    )
    expected = generate_topology_research(inputs)
    actual = generated.layout.attempts[0].topology

    assert actual.final_rng_seed == expected.final_rng_seed
    assert [
        (room.column, room.line, room.shape) for room in actual.rooms
    ] == [
        (room.column, room.line, room.shape) for room in expected.rooms
    ]
