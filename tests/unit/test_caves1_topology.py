from __future__ import annotations

import pytest

from isaacmap.caves1_topology import CAVES1_TOPOLOGY_STATUS, generate_caves1_topology
from isaacmap.floor_init import derive_caves1_topology_inputs
from isaacmap.floor_init_reference import derive_caves1_topology_inputs_reference
from isaacmap.topology_differential import compare_topology_results
from isaacmap.topology_reference import generate_topology_reference


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 7, 29, 113, 997))
def test_caves1_topology_matches_reference(seed: int, difficulty: str) -> None:
    inputs = derive_caves1_topology_inputs(seed, difficulty)
    reference_inputs = derive_caves1_topology_inputs_reference(seed, difficulty)
    assert inputs.stage_seed == reference_inputs.stage_seed
    assert inputs.target_room_count == reference_inputs.target
    assert inputs.is_xl == reference_inputs.is_xl
    reference = generate_topology_reference(inputs)
    compare_topology_results(inputs, reference)


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_caves1_natural_xl_topology_matches_reference(difficulty: str) -> None:
    seed = next(
        seed
        for seed in range(1, 10_001)
        if derive_caves1_topology_inputs(seed, difficulty).is_xl
    )
    inputs = derive_caves1_topology_inputs(seed, difficulty)
    reference = generate_topology_reference(inputs)
    _reference, summary = compare_topology_results(inputs, reference)
    assert inputs.is_xl
    assert summary.room_count >= inputs.target_room_count


def test_caves1_topology_wrapper() -> None:
    result = generate_caves1_topology(1, "NORMAL")
    assert result.generation_status == CAVES1_TOPOLOGY_STATUS
    assert len(result.topology.dead_ends) >= result.inputs.required_dead_ends
    assert result.topology.room_map[84] >= 0
