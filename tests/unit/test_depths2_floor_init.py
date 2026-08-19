from __future__ import annotations

import pytest

from isaacmap.floor_init import derive_depths2_topology_inputs
from isaacmap.floor_init_reference import derive_depths2_topology_inputs_reference


def _clean(value) -> tuple[object, ...]:
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


def _reference(value) -> tuple[object, ...]:
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
def test_depths2_initialization_matches_independent_reference(difficulty: str) -> None:
    masks: set[int] = set()
    for seed in range(1, 10_001):
        clean = derive_depths2_topology_inputs(seed, difficulty)
        reference = derive_depths2_topology_inputs_reference(seed, difficulty)
        assert _clean(clean) == _reference(reference)
        masks.add(clean.effective_curse_mask)
        assert not clean.is_xl
    assert masks == {0, 1, 4, 8, 32, 64}


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_depths2_stage_constants(difficulty: str) -> None:
    inputs = derive_depths2_topology_inputs(1, difficulty)
    assert inputs.room_config_stage == 7
    assert inputs.required_dead_ends == 6
    assert inputs.allowed_shapes_mask == 0x1FFE
    assert not inputs.is_xl
    if difficulty == "NORMAL":
        assert (inputs.room_config_min_difficulty, inputs.room_config_max_difficulty) == (5, 10)
    else:
        assert (inputs.room_config_min_difficulty, inputs.room_config_max_difficulty) == (10, 15)


def test_depths2_rejects_unsupported_difficulty() -> None:
    with pytest.raises(ValueError, match="NORMAL or HARD"):
        derive_depths2_topology_inputs(1, "GREED")
