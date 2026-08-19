from __future__ import annotations

import pytest

from isaacmap.stage_seed import (
    derive_initial_seed_sequence,
    floor_stage_seed_slot,
    get_initial_floor_stage_seed,
    get_initial_stage_seed,
)


def test_binary_derived_seed_sequence_for_one() -> None:
    sequence = derive_initial_seed_sequence(1)
    assert sequence.stage_seeds == (
        0x00800001,
        0x00100001,
        0x00920001,
        0x00004001,
        0x00804801,
        0x80104141,
        0x2492497B,
        0x0A000051,
        0x26C00048,
        0x02980040,
        0x26CB005B,
        0x0A126055,
        0x24D02C4D,
        0xC24A29A5,
    )
    assert sequence.player_init_seed == 0x92836CD8


def test_stage_index_is_direct_array_index() -> None:
    sequence = derive_initial_seed_sequence(0x12345678)
    assert get_initial_stage_seed(0x12345678, 0) == 0x4BF2DC92
    assert get_initial_stage_seed(0x12345678, 1) == 0xC28C8761
    assert get_initial_stage_seed(0x12345678, 13) == 0xF77B3543
    assert sequence.player_init_seed == 0x1C1453E5


def test_level_init_stage_type_slot_adjustment() -> None:
    assert floor_stage_seed_slot(1, 0) == 1
    assert floor_stage_seed_slot(1, 1) == 1
    assert floor_stage_seed_slot(1, 2) == 1
    assert floor_stage_seed_slot(1, 4) == 2
    assert floor_stage_seed_slot(1, 5) == 2
    assert floor_stage_seed_slot(13, 4) == 13
    assert get_initial_floor_stage_seed(0x12345678, 1, 4) == 0x1C5D1783


@pytest.mark.parametrize("level_stage", [-1, 14])
def test_level_stage_out_of_range_is_rejected(level_stage: int) -> None:
    with pytest.raises(ValueError):
        get_initial_stage_seed(1, level_stage)


@pytest.mark.parametrize("start_seed", [0, -1, 0x1_0000_0000])
def test_invalid_start_seed_is_rejected(start_seed: int) -> None:
    with pytest.raises(ValueError):
        derive_initial_seed_sequence(start_seed)
