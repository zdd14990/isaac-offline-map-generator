from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from isaacmap.basement1_ultra_pipeline import generate_basement1_through_ultra
from isaacmap.basement1_ultra_pipeline_differential import compare_ultra_pipeline
from isaacmap.basement1_ultra_pipeline_reference import (
    generate_basement1_through_ultra_reference,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.resources import load_stb
from isaacmap.rng import IsaacRNG
from isaacmap.room_config import RoomConfigEntry, RoomConfigKey
from isaacmap.special_rooms import GeneratedRoom
from isaacmap.topology_geometry import RoomShape
from isaacmap.ultra_secret import (
    UltraGeometryState,
    build_ultra_forbidden_indices,
    place_ultra_secret_room,
)
from isaacmap.ultra_secret_reference import (
    UltraReferenceState,
    build_ultra_forbidden_indices_reference,
    place_ultra_secret_room_reference,
)


ROOT = Path("research/input/extracted_resources/merged/resources")
BOSSES = load_boss_pool_xml(ROOT / "bosspools.xml")["basement"]
BOSS_REFS = tuple(
    BossPoolEntryReference(
        item.boss_id,
        item.weight,
        item.initial_weight,
        item.achievement,
        item.alternate_boss_id,
    )
    for item in BOSSES
)
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))


def _room(room_id: int, column: int, row: int) -> GeneratedRoom:
    return GeneratedRoom(
        room_id,
        column,
        row,
        RoomShape.ROOMSHAPE_1x1,
        -1,
        -1,
        -1,
        0,
    )


def _entry(room_type: int, *, door_mask: int) -> RoomConfigEntry:
    return RoomConfigEntry(
        RoomConfigKey(0, 0, room_type),
        room_type,
        0,
        0,
        1,
        1,
        1.0,
        door_mask,
    )


def _geometry_fixture(seed: int = 123) -> UltraGeometryState:
    rooms = (_room(0, 4, 6), _room(1, 6, 4), _room(2, 8, 6))
    room_map = [-1] * 169
    for room in rooms:
        room_map[room.line * 13 + room.column] = room.generation_index
    blocked = [True] * 169
    for index in (84, 83, 71, 85, 97):
        blocked[index] = False
    return UltraGeometryState(
        [replace(room, neighbors=set()) for room in rooms],
        room_map,
        blocked,
        IsaacRNG.game_constructor(seed, 35),
    )


def _reference_signature(result: object) -> tuple[object, ...]:
    return (
        result.room_id,
        result.grid_index,
        result.forbidden,
        result.best,
        result.best_score,
        tuple(
            (
                item.index,
                item.occupied,
                item.forbidden,
                item.blocked,
                item.base,
                item.immediate_mask,
                item.ring_mask,
                item.count,
                item.invalid_targets,
                item.score,
                item.action,
            )
            for item in result.evaluations
        ),
        result.transitions,
        result.final_rng,
        result.red_writes,
        tuple(
            (
                room.generation_index,
                room.column,
                room.line,
                int(room.shape),
                room.doors,
                tuple(sorted(room.neighbors)),
            )
            for room in result.rooms
        ),
        result.room_map,
    )


def _clean_signature(result: object, state: UltraGeometryState) -> tuple[object, ...]:
    return (
        result.room_id,
        result.grid_index,
        result.forbidden_indices,
        result.best_candidates,
        result.best_score,
        tuple(
            (
                item.grid_index,
                item.occupied,
                item.forbidden,
                item.blocked,
                item.base_score,
                item.immediate_mask,
                item.outer_neighbor_mask,
                item.adjacency_count,
                item.invalid_red_door_targets,
                item.final_score,
                item.best_action,
            )
            for item in result.evaluations
        ),
        tuple(
            (item.pre_state, item.post_state, "selection" if "select among" in item.reason else "candidate", item.result)
            for item in result.rng_transitions
        ),
        result.final_generator_rng_state,
        tuple(
            (item.room_id, item.door_slot, item.target_grid_index, item.ultra_grid_index)
            for item in result.red_door_writes
        ),
        tuple(
            (
                room.generation_index,
                room.column,
                room.line,
                int(room.shape),
                room.doors,
                tuple(sorted(room.neighbors)),
            )
            for room in state.rooms
        ),
        tuple(state.room_map),
    )


def test_red_exclusion_set_uses_config_doors_and_forced_room_types() -> None:
    normal = _room(0, 6, 6)
    curse = _room(1, 3, 3)
    configs = {0: _entry(2, door_mask=0b0101), 1: _entry(10, door_mask=0xFF)}
    clean = build_ultra_forbidden_indices([normal, curse], configs)
    reference = build_ultra_forbidden_indices_reference([normal, curse], configs)
    assert clean == reference
    # Normal room forbids its missing up/down doors; Curse forces all four.
    assert {71, 97, 41, 29, 43, 55} <= set(clean)
    assert 83 not in clean and 85 not in clean


@pytest.mark.parametrize("seed", [1, 2, 3, 0x12345678, 0xFFFFFFFF])
def test_clean_geometry_matches_mechanical_reference(seed: int) -> None:
    clean_state = _geometry_fixture(seed)
    reference_state = UltraReferenceState(
        [replace(room, neighbors=set(room.neighbors)) for room in clean_state.rooms],
        list(clean_state.room_map),
        list(clean_state.blocked_positions),
        IsaacRNG.game_constructor(seed, 35),
    )
    clean = place_ultra_secret_room(clean_state, ())
    reference = place_ultra_secret_room_reference(reference_state, ())
    assert _clean_signature(clean, clean_state) == _reference_signature(reference)


def test_ultra_is_new_1x1_room_and_writes_red_door_slots() -> None:
    state = _geometry_fixture()
    before_rooms = len(state.rooms)
    result = place_ultra_secret_room(state, ())
    assert result.grid_index == 84
    assert result.room_id == before_rooms
    assert len(state.rooms) == before_rooms + 1
    assert state.room_map[84] == result.room_id
    assert state.rooms[result.room_id].shape == RoomShape.ROOMSHAPE_1x1
    assert state.rooms[result.room_id].doors == 0
    assert {(item.room_id, item.door_slot) for item in result.red_door_writes} == {
        (0, 2),
        (1, 3),
        (2, 0),
    }


def test_forbidden_red_door_target_rejects_outer_neighbor() -> None:
    state = _geometry_fixture()
    result = place_ultra_secret_room(state, (83,))
    evaluation = result.evaluations[84]
    assert evaluation.invalid_red_door_targets == (83,)
    assert evaluation.final_score is None


def test_no_candidate_is_supported_without_final_selection_draw() -> None:
    state = UltraGeometryState([], [-1] * 169, [True] * 169, IsaacRNG.game_constructor(1, 35))
    result = place_ultra_secret_room(state, ())
    assert result.room_id == -1
    assert result.rng_transitions == ()
    assert result.final_generator_rng_state == 1


@pytest.mark.parametrize("difficulty", ["NORMAL", "HARD"])
def test_canonical_pipeline_reaches_type29_pre_late_boundary(difficulty: str) -> None:
    result = generate_basement1_through_ultra(
        1,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )
    assert result.boundary_completed and result.final is not None
    final = result.final
    assert final.ultra_config is not None
    assert final.ultra_config_rng.shift_index == 71
    assert all(
        draw.shift_index == 35 for draw in final.ultra_geometry.rng_transitions
    )
    if final.ultra_room >= 0:
        assert final.rooms[final.ultra_room].room_type == 29
        assert final.room_map[final.ultra_geometry.grid_index] == final.ultra_room
        assert final.ultra_descriptor.created


@pytest.mark.parametrize("difficulty", ["NORMAL", "HARD"])
def test_first_ten_ultra_pipelines_match_independent_reference(
    difficulty: str,
) -> None:
    for seed in range(1, 11):
        clean = generate_basement1_through_ultra(
            seed,
            difficulty,
            boss_entries=BOSSES,
            special_definitions=SPECIAL,
            basement_definitions=BASEMENT,
        )
        reference = generate_basement1_through_ultra_reference(
            seed,
            difficulty,
            boss_entries=BOSS_REFS,
            special_definitions=SPECIAL,
            basement_definitions=BASEMENT,
        )
        compare_ultra_pipeline(clean, reference)
