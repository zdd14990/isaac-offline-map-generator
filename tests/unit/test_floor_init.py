from __future__ import annotations

import pytest

from isaacmap.floor_init import (
    ALL_GENERATED_ROOM_SHAPES_MASK,
    Difficulty,
    derive_basement1_topology_inputs,
)
from isaacmap.floor_init_reference import derive_basement1_topology_inputs_reference
from isaacmap.seed import decode_seed


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


def test_basement1_hard_uses_post_curse_copied_stream_bit() -> None:
    odd = derive_basement1_topology_inputs(1, "HARD")
    even = derive_basement1_topology_inputs(2, "HARD")
    assert odd.copied_rng_draws == (0xAD4AA83F, 0xE809B57C)
    assert odd.target_room_count == 11
    assert even.target_room_count == 10
    assert even.level_rng_draws == (
        0x42A5460A,
        0x2028C80A,
        0x72D1707E,
        0xFF4D61FE,
    )


def test_qqtt_fqpg_hard_floor_init_consumes_curse_gate_before_bonus() -> None:
    start_seed = decode_seed("QQTT FQPG")
    clean = derive_basement1_topology_inputs(start_seed, "HARD")
    reference = derive_basement1_topology_inputs_reference(start_seed, "HARD")

    assert start_seed == 2085383492
    assert clean.stage_seed == 2096979149
    assert clean.level_rng_draws == (
        1256328683,
        583731631,
        2555144393,
        2174232484,
    )
    assert clean.copied_rng_draws == (2555144393, 2174232484)
    assert clean.curse_rate_denominator == 40
    assert clean.curse_gate_succeeded is False
    assert clean.curse_selector is None
    assert clean.effective_curse_mask == 0
    assert clean.is_xl is False
    assert clean.target_room_count == 11
    assert (
        clean.stage_seed,
        clean.level_rng_draws,
        clean.copied_rng_draws,
        clean.curse_rate_denominator,
        clean.curse_gate_succeeded,
        clean.curse_selector,
        clean.effective_curse_mask,
        clean.is_xl,
        clean.generator_seed,
        clean.target_room_count,
        clean.required_dead_ends,
        clean.allowed_shapes_mask,
    ) == (
        reference.stage_seed,
        reference.level_draws,
        reference.copied_draws,
        reference.curse_rate,
        reference.curse_gate,
        reference.curse_selector,
        reference.curse_mask,
        reference.is_xl,
        reference.generator_seed,
        reference.target,
        reference.dead_ends,
        reference.shapes,
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
