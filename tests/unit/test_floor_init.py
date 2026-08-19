from __future__ import annotations

import pytest

from isaacmap.floor_init import (
    ALL_GENERATED_ROOM_SHAPES_MASK,
    Difficulty,
    derive_basement1_topology_inputs,
)


def test_basement1_normal_binary_sequence() -> None:
    result = derive_basement1_topology_inputs(1, Difficulty.NORMAL)
    assert result.stage_seed == 0x00100001
    assert result.level_rng_draws == (
        0x2152A305,
        0x91146405,
        0xAD4AA83F,
        0xE809B57C,
    )
    assert result.generator_seed == 0xE809B57C
    assert result.target_room_count == 9
    assert result.required_dead_ends == 5
    assert result.allowed_shapes_mask == 0x1FFE
    assert result.starting_grid_index == 84


def test_basement1_hard_reuses_copied_stream_bit() -> None:
    odd = derive_basement1_topology_inputs(1, "HARD")
    even = derive_basement1_topology_inputs(2, "HARD")
    assert odd.target_room_count == 12
    assert even.target_room_count == 10
    assert even.level_rng_draws == (
        0x42A5460A,
        0x2028C80A,
        0x72D1707E,
        0xFF4D61FE,
    )


def test_normal_count_uses_the_third_draw_low_bit() -> None:
    assert derive_basement1_topology_inputs(1, "NORMAL").target_room_count == 9
    assert derive_basement1_topology_inputs(2, "NORMAL").target_room_count == 8


def test_all_shapes_1_through_12_are_enabled() -> None:
    assert [
        shape
        for shape in range(32)
        if ALL_GENERATED_ROOM_SHAPES_MASK & (1 << shape)
    ] == list(range(1, 13))


def test_invalid_difficulty_is_rejected() -> None:
    with pytest.raises(ValueError):
        derive_basement1_topology_inputs(1, "GREED")
