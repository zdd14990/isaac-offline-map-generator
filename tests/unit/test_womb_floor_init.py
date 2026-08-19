from __future__ import annotations

import pytest

from isaacmap.floor_init import derive_womb1_topology_inputs, derive_womb2_topology_inputs
from isaacmap.floor_init_reference import (
    derive_womb1_topology_inputs_reference,
    derive_womb2_topology_inputs_reference,
)


def _clean_womb1(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.level_rng_draws,
        value.copied_rng_draws,
        value.curse_rate_denominator,
        value.curse_gate_succeeded,
        value.curse_selector,
        value.effective_curse_mask,
        value.is_xl,
        value.generator_seed,
        value.target_room_count,
        value.required_dead_ends,
        value.allowed_shapes_mask,
        value.room_config_stage,
        value.room_config_min_difficulty,
        value.room_config_max_difficulty,
    )


def _clean_womb2(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.level_rng_draws,
        value.copied_rng_draws,
        value.curse_rate_denominator,
        value.curse_gate_succeeded,
        value.curse_selector,
        value.effective_curse_mask,
        value.is_xl,
        value.generator_seed,
        value.target_room_count,
        value.required_dead_ends,
        value.allowed_shapes_mask,
        value.room_config_stage,
        value.room_config_min_difficulty,
        value.room_config_max_difficulty,
    )


def _reference_womb1(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.level_draws,
        value.copied_draws,
        value.curse_rate,
        value.curse_gate,
        value.curse_selector,
        value.curse_mask,
        value.is_xl,
        value.generator_seed,
        value.target,
        value.dead_ends,
        value.shapes,
        value.room_config_stage,
        value.minimum_difficulty,
        value.maximum_difficulty,
    )


def _reference_womb2(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.level_draws,
        value.copied_draws,
        value.curse_rate,
        value.curse_gate,
        value.curse_selector,
        value.curse_mask,
        value.is_xl,
        value.generator_seed,
        value.target,
        value.dead_ends,
        value.shapes,
        value.room_config_stage,
        value.minimum_difficulty,
        value.maximum_difficulty,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_womb1_initialization_matches_independent_reference(difficulty: str) -> None:
    masks: set[int] = set()
    xl_seen = False
    for seed in range(1, 10_001):
        clean = derive_womb1_topology_inputs(seed, difficulty)
        reference = derive_womb1_topology_inputs_reference(seed, difficulty)
        assert _clean_womb1(clean) == _reference_womb1(reference)
        masks.add(clean.effective_curse_mask)
        xl_seen |= clean.is_xl
        if clean.is_xl:
            expected = 36 if difficulty == "NORMAL" else (38, 39)
            assert clean.target_room_count in (expected if isinstance(expected, tuple) else (expected,))
            assert clean.required_dead_ends == 7
    assert masks == {0, 1, 2, 4, 8, 32, 64}
    assert xl_seen


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_womb2_initialization_matches_independent_reference(difficulty: str) -> None:
    masks: set[int] = set()
    for seed in range(1, 10_001):
        clean = derive_womb2_topology_inputs(seed, difficulty)
        reference = derive_womb2_topology_inputs_reference(seed, difficulty)
        assert _clean_womb2(clean) == _reference_womb2(reference)
        masks.add(clean.effective_curse_mask)
        assert not clean.is_xl
        assert clean.required_dead_ends == 6
@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_womb_stage_constants(difficulty: str) -> None:
    womb1 = derive_womb1_topology_inputs(1, difficulty)
    womb2 = derive_womb2_topology_inputs(1, difficulty)
    assert womb1.room_config_stage == 10
    assert womb2.room_config_stage == 10
    assert womb1.allowed_shapes_mask == 0x1FFE
    assert womb2.allowed_shapes_mask == 0x1FFE
    if difficulty == "NORMAL":
        assert womb1.target_room_count == 20
        assert womb2.target_room_count == 20
        assert (womb1.room_config_min_difficulty, womb1.room_config_max_difficulty) == (1, 5)
        assert (womb2.room_config_min_difficulty, womb2.room_config_max_difficulty) == (5, 10)
    else:
        assert womb1.target_room_count in (22, 23)
        assert womb2.target_room_count in (22, 23)
        assert (womb1.room_config_min_difficulty, womb1.room_config_max_difficulty) == (5, 10)
        assert (womb2.room_config_min_difficulty, womb2.room_config_max_difficulty) == (10, 15)


def test_womb_rejects_unsupported_difficulty() -> None:
    with pytest.raises(ValueError, match="NORMAL or HARD"):
        derive_womb1_topology_inputs(1, "GREED")
    with pytest.raises(ValueError, match="NORMAL or HARD"):
        derive_womb2_topology_inputs(1, "GREED")
