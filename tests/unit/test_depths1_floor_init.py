from __future__ import annotations

import pytest

from isaacmap.floor_init import derive_depths1_topology_inputs
from isaacmap.floor_init_reference import derive_depths1_topology_inputs_reference


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
def test_depths1_initialization_matches_independent_reference(difficulty: str) -> None:
    masks: set[int] = set()
    saw_xl = False
    for seed in range(1, 10_001):
        clean = derive_depths1_topology_inputs(seed, difficulty)
        reference = derive_depths1_topology_inputs_reference(seed, difficulty)
        assert _clean(clean) == _reference(reference)
        masks.add(clean.effective_curse_mask)
        saw_xl |= clean.is_xl
    assert masks == {0, 1, 2, 4, 8, 32, 64}
    assert saw_xl


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_depths1_xl_changes_topology_contract(difficulty: str) -> None:
    xl = next(
        derive_depths1_topology_inputs(seed, difficulty)
        for seed in range(1, 10_001)
        if derive_depths1_topology_inputs(seed, difficulty).is_xl
    )
    assert xl.effective_curse_mask == 2
    assert xl.required_dead_ends == 7
    assert xl.target_room_count in (36, 38, 39)
    assert (xl.room_config_min_difficulty, xl.room_config_max_difficulty) == (
        (5, 15) if difficulty == "HARD" else (1, 10)
    )


def test_depths1_non_xl_stage_constants() -> None:
    normal = next(
        derive_depths1_topology_inputs(seed, "NORMAL")
        for seed in range(1, 100)
        if not derive_depths1_topology_inputs(seed, "NORMAL").is_xl
    )
    hard = next(
        derive_depths1_topology_inputs(seed, "HARD")
        for seed in range(1, 100)
        if not derive_depths1_topology_inputs(seed, "HARD").is_xl
    )
    assert normal.room_config_stage == hard.room_config_stage == 7
    assert normal.required_dead_ends == hard.required_dead_ends == 6
    assert normal.allowed_shapes_mask == hard.allowed_shapes_mask == 0x1FFE
    assert (normal.room_config_min_difficulty, normal.room_config_max_difficulty) == (1, 5)
    assert (hard.room_config_min_difficulty, hard.room_config_max_difficulty) == (5, 10)


def test_depths1_rejects_unsupported_difficulty() -> None:
    with pytest.raises(ValueError, match="NORMAL or HARD"):
        derive_depths1_topology_inputs(1, "GREED")
