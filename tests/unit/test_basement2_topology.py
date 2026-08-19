from __future__ import annotations

import pytest

from isaacmap.basement2_topology import (
    BASEMENT2_TOPOLOGY_STATUS,
    generate_basement2_topology,
)
from isaacmap.floor_init import derive_basement2_topology_inputs
from isaacmap.floor_init_reference import (
    derive_basement2_topology_inputs_reference,
)
from isaacmap.topology_differential import compare_topology_results
from isaacmap.topology_reference import generate_topology_reference


def _entry_signature(clean, reference) -> None:
    assert clean.stage_seed == reference.stage_seed
    assert clean.level_rng_draws == reference.level_draws
    assert clean.copied_rng_draws == reference.copied_draws
    assert clean.curse_rate_denominator == reference.curse_rate
    assert clean.curse_gate_succeeded == reference.curse_gate
    assert clean.curse_selector == reference.curse_selector
    assert clean.effective_curse_mask == reference.curse_mask
    assert clean.generator_seed == reference.generator_seed
    assert clean.target_room_count == reference.target
    assert clean.required_dead_ends == reference.dead_ends
    assert clean.allowed_shapes_mask == reference.shapes


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 7, 29, 113, 997))
def test_basement2_topology_matches_reference(seed: int, difficulty: str) -> None:
    inputs = derive_basement2_topology_inputs(seed, difficulty)
    reference_inputs = derive_basement2_topology_inputs_reference(seed, difficulty)
    _entry_signature(inputs, reference_inputs)
    reference = generate_topology_reference(inputs)
    compare_topology_results(inputs, reference)


def test_basement2_topology_wrapper() -> None:
    result = generate_basement2_topology(1, "NORMAL")
    assert result.generation_status == BASEMENT2_TOPOLOGY_STATUS
    assert len(result.topology.dead_ends) >= result.inputs.required_dead_ends
    assert result.topology.room_map[84] >= 0
