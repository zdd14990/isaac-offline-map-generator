from __future__ import annotations

import pytest

from isaacmap.floor_init import derive_basement1_topology_inputs
from isaacmap.rng import IsaacRNG
from isaacmap.topology import (
    LevelGeneratorResearch,
    LevelGeneratorRoom,
    generate_basement1_topology_research,
)
from isaacmap.topology_geometry import (
    RoomShape,
    door_source_position,
    door_target_position,
    occupied_cells,
)


def test_start_neighbor_builder_consumes_13_draws_per_valid_door() -> None:
    seed = 0x12345678
    generator = LevelGeneratorResearch(seed)
    generator.allowed_shapes = 0x1FFE
    generator.place_room(LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1))
    generator.get_neighbor_candidates(0)

    reference = IsaacRNG.game_constructor(seed, 35)
    for _ in range(4 * 13):
        reference.next()
    assert generator.rng.seed == reference.seed


def test_force_large_override_keeps_draws_and_all_center_candidates() -> None:
    seed = 0x12345678
    generator = LevelGeneratorResearch(seed)
    generator.allowed_shapes = 0x1FFE
    generator.place_room(LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1))
    candidates = generator.get_neighbor_candidates(0, force_all_large=True)
    assert len(candidates) == 4 * 14

    reference = IsaacRNG.game_constructor(seed, 35)
    for _ in range(4 * 13):
        reference.next()
    assert generator.rng.seed == reference.seed


@pytest.mark.parametrize("start_seed,difficulty", [(1, "NORMAL"), (2, "HARD"), (0x12345678, "NORMAL")])
def test_research_topology_internal_invariants(start_seed: int, difficulty: str) -> None:
    inputs = derive_basement1_topology_inputs(start_seed, difficulty)
    result = generate_basement1_topology_research(inputs)
    assert result.rooms[0].grid_index == 84
    assert result.rooms[0].shape == 1
    assert len(result.rooms) >= result.target_room_count + 1
    assert len(result.dead_ends) >= inputs.required_dead_ends

    seen: dict[tuple[int, int], int] = {}
    for room in result.rooms:
        assert room.generation_index < len(result.rooms)
        for cell in occupied_cells(room.column, room.line, room.shape):
            assert 0 <= cell[0] < 13
            assert 0 <= cell[1] < 13
            assert cell not in seen
            seen[cell] = room.generation_index
            assert result.room_map[cell[1] * 13 + cell[0]] == room.generation_index
        assert room.neighbors.issubset(set(range(len(result.rooms))))
        for slot in range(8):
            if not room.doors & (1 << slot):
                continue
            target = door_target_position(room.column, room.line, room.shape, slot)
            neighbor_id = result.room_map[target[1] * 13 + target[0]]
            assert neighbor_id in room.neighbors
            source = door_source_position(room.column, room.line, room.shape, slot)
            neighbor = result.rooms[neighbor_id]
            assert any(
                door_target_position(
                    neighbor.column, neighbor.line, neighbor.shape, return_slot
                )
                == source
                for return_slot in range(8)
            )


def test_research_topology_is_deterministic() -> None:
    inputs = derive_basement1_topology_inputs(0x12345678, "HARD")
    first = generate_basement1_topology_research(inputs)
    second = generate_basement1_topology_research(inputs)
    assert first == second
