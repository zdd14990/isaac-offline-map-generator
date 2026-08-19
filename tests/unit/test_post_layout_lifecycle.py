from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline import generate_basement1_full
from isaacmap.basement1_lifecycle import (
    BASEMENT1_LIFECYCLE_STATUS,
    generate_basement1_lifecycle,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.post_layout_lifecycle import run_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_differential import (
    compare_post_layout_lifecycle,
)
from isaacmap.post_layout_lifecycle_reference import (
    run_post_layout_lifecycle_reference,
)
from isaacmap.resources import load_stb
from isaacmap.rng import IsaacRNG
from isaacmap.room_config import entries_from_definitions
from isaacmap.room_config_reference import (
    RoomConfigKey as ReferenceKey,
    entries_from_definitions_reference,
)


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
BOSSES = load_boss_pool_xml(ROOT / "bosspools.xml")["basement"]
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


def _accepted(seed: int, difficulty: str):
    return generate_basement1_full(
        seed,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 7, 10))
def test_post_layout_tail_matches_reference(seed: int, difficulty: str) -> None:
    accepted = _accepted(seed, difficulty)
    clean = run_post_layout_lifecycle(
        level_rng_state=accepted.final_level_rng_state,
        entries=ENTRIES,
        room_config_weights=accepted.final_room_config_weights,
        special_room_used_bits=accepted.final_special_room_used_bits,
    )
    reference = run_post_layout_lifecycle_reference(
        level_rng_state=accepted.final_level_rng_state,
        entries=REFERENCE_ENTRIES,
        room_config_weights=tuple(
            (ReferenceKey(key.stage, key.mode, key.resource_index), value)
            for key, value in accepted.final_room_config_weights
        ),
        special_room_used_bits=accepted.final_special_room_used_bits,
    )
    compare_post_layout_lifecycle(clean, reference)

    assert clean.persistent_level_draw_count == 28
    assert tuple(item.grid_index for item in clean.assignments) == (
        -2, -6, -4, -5, -7, -8, -13, -18,
    )
    assert tuple(item.room_type for item in clean.assignments) == (
        3, 22, 16, 17, 5, 1, 2, 15,
    )
    assert all(item.config is not None for item in clean.assignments)

    replay = IsaacRNG.game_constructor(accepted.final_level_rng_state, 35)
    for _ in range(28):
        replay.next()
    assert clean.final_level_rng_state == replay.seed


def test_tail_clears_used_bits_30_and_31_only() -> None:
    accepted = _accepted(1, "NORMAL")
    result = run_post_layout_lifecycle(
        level_rng_state=accepted.final_level_rng_state,
        entries=ENTRIES,
        room_config_weights=accepted.final_room_config_weights,
        special_room_used_bits=(6, 30, 31),
    )
    assert result.final_special_room_used_bits == (6,)


def test_basement1_lifecycle_builds_floor_two_handoff() -> None:
    result = generate_basement1_lifecycle(
        1,
        "NORMAL",
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    assert result.completed
    assert result.generation_status == BASEMENT1_LIFECYCLE_STATUS
    assert result.next_run_state.completed_level_stage == 1
    assert result.next_run_state.next_level_stage == 2
    assert len(result.next_run_state.boss_pool_rng_states) == 37
    assert result.next_run_state.boss_pool_rng_states[1] == (
        result.layout.final_boss_pool_state
    )
    assert result.next_run_state.last_floor_level_rng_state == (
        result.post_layout.final_level_rng_state
    )
    assert result.next_run_state.lifecycle == "basement1-success-tail-complete"


@pytest.mark.parametrize(
    "kwargs",
    (
        {"level_stage": 3},
        {"stage_type": 1},
        {"room_config_stage": 2},
        {"collectible_ids": frozenset((550,))},
        {"player_collectible_count": 1},
        {"special_counter": 1},
    ),
)
def test_tail_rejects_noncanonical_profile(kwargs: dict[str, object]) -> None:
    accepted = _accepted(1, "NORMAL")
    with pytest.raises(ValueError, match="outside the canonical"):
        run_post_layout_lifecycle(
            level_rng_state=accepted.final_level_rng_state,
            entries=ENTRIES,
            room_config_weights=accepted.final_room_config_weights,
            **kwargs,
        )
