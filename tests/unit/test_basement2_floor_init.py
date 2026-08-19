from __future__ import annotations

import pytest

from isaacmap.floor_init import derive_basement2_topology_inputs
from isaacmap.floor_init_reference import (
    derive_basement2_topology_inputs_reference,
)


def _signature(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.level_rng_draws,
        value.copied_rng_draws,
        value.curse_rate_denominator,
        value.curse_gate_succeeded,
        value.curse_selector,
        value.effective_curse_mask,
        value.generator_seed,
        value.target_room_count,
        value.required_dead_ends,
        value.allowed_shapes_mask,
        value.room_config_min_difficulty,
        value.room_config_max_difficulty,
    )


def _reference_signature(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.level_draws,
        value.copied_draws,
        value.curse_rate,
        value.curse_gate,
        value.curse_selector,
        value.curse_mask,
        value.generator_seed,
        value.target,
        value.dead_ends,
        value.shapes,
        value.minimum_difficulty,
        value.maximum_difficulty,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_basement2_initialization_matches_reference(difficulty: str) -> None:
    saw_gate = False
    saw_rejected_labyrinth = False
    for seed in range(1, 10_001):
        clean = derive_basement2_topology_inputs(seed, difficulty)
        reference = derive_basement2_topology_inputs_reference(seed, difficulty)
        assert _signature(clean) == _reference_signature(reference)
        saw_gate |= clean.curse_gate_succeeded
        saw_rejected_labyrinth |= (
            clean.curse_selector is not None
            and clean.curse_selector % 6 == 0
            and clean.effective_curse_mask == 0
        )
    assert saw_gate
    assert saw_rejected_labyrinth


def test_basement2_stage_specific_constants() -> None:
    normal = derive_basement2_topology_inputs(1, "NORMAL")
    hard = derive_basement2_topology_inputs(1, "HARD")
    assert normal.required_dead_ends == hard.required_dead_ends == 6
    assert normal.allowed_shapes_mask == hard.allowed_shapes_mask == 0x1FFE
    assert (normal.room_config_min_difficulty, normal.room_config_max_difficulty) == (5, 10)
    assert (hard.room_config_min_difficulty, hard.room_config_max_difficulty) == (10, 15)
    assert normal.curse_rate_denominator == 80
    assert hard.curse_rate_denominator == 40


def test_basement2_rejects_unsupported_difficulty() -> None:
    with pytest.raises(ValueError, match="NORMAL or HARD"):
        derive_basement2_topology_inputs(1, "GREED")
