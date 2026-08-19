from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_secret_pipeline import generate_basement1_through_secret
from isaacmap.basement1_secret_pipeline_differential import compare_secret_pipeline
from isaacmap.basement1_secret_pipeline_reference import generate_basement1_through_secret_reference
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.resources import load_stb
from isaacmap.rng import IsaacRNG
from isaacmap.secret import SecretGeometryState, place_secret_room
from isaacmap.secret_reference import ReferenceSecretGeometryState, place_secret_room_reference
from isaacmap.special_rooms import GeneratedRoom
from isaacmap.topology_geometry import RoomShape


ROOT = Path("research/input/extracted_resources/merged/resources")
BOSSES = load_boss_pool_xml(ROOT / "bosspools.xml")["basement"]
BOSS_REFS = tuple(BossPoolEntryReference(x.boss_id, x.weight, x.initial_weight, x.achievement, x.alternate_boss_id) for x in BOSSES)
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))


def _clean(seed: int, difficulty: str):
    return generate_basement1_through_secret(seed, difficulty, boss_entries=BOSSES, special_definitions=SPECIAL, basement_definitions=BASEMENT)


def _reference(seed: int, difficulty: str):
    return generate_basement1_through_secret_reference(seed, difficulty, boss_entries=BOSS_REFS, special_definitions=SPECIAL, basement_definitions=BASEMENT)


@pytest.mark.parametrize("difficulty", ["NORMAL", "HARD"])
def test_first_twenty_m6_attempts_match_independent_reference(difficulty):
    for seed in range(1, 21):
        compare_secret_pipeline(_clean(seed, difficulty), _reference(seed, difficulty))


def test_binary_block_order_and_route_blocks_are_retained():
    result = _clean(0xCAE, "NORMAL")
    m6 = result.attempts[-1].through_secret
    assert m6 is not None
    assert [block.operation for block in m6.blocks] == [
        "Planetarium", "Sacrifice", "Library", "Curse",
        "MiniBoss", "Challenge", "Arcade", "Isaac",
    ]
    assert [condition.value for condition in m6.conditions] == [False, False, False, False]
    assert all(condition.consequence.startswith("skip") for condition in m6.conditions)


def test_secret_is_new_room_and_does_not_consume_dead_end_candidate():
    result = _clean(0xCAE, "NORMAL")
    attempt = result.attempts[-1]
    assert attempt.through_treasure is not None and attempt.through_secret is not None
    m5, m6 = attempt.through_treasure, attempt.through_secret
    assert m6.secret_room == len(m5.rooms)
    assert m6.rooms[m6.secret_room].room_type == 7
    assert m6.room_map[m6.secret_geometry.grid_index] == m6.secret_room
    assert m6.dead_ends == m6.blocks[-1].candidate_after


def test_pre_ultra_boundary_does_not_commit_boss_blacklist():
    result = _clean(0xCAE, "NORMAL")
    assert result.boundary_completed
    assert result.permanent_removed_bosses == ()
    assert result.pending_boss_blacklist


def test_every_eligible_empty_cell_draws_before_best_tie_selection():
    rooms = [
        GeneratedRoom(0, 6, 6, RoomShape.ROOMSHAPE_1x1, -1, -1, -1, 0),
        GeneratedRoom(1, 5, 5, RoomShape.ROOMSHAPE_1x1, -1, -1, -1, 0),
        GeneratedRoom(2, 7, 5, RoomShape.ROOMSHAPE_1x1, -1, -1, -1, 0),
    ]
    room_map = [-1] * 169
    for room in rooms: room_map[room.line * 13 + room.column] = room.generation_index
    clean_state = SecretGeometryState([GeneratedRoom(**{**room.__dict__, "neighbors": set()}) for room in rooms], list(room_map), [False] * 169, IsaacRNG.game_constructor(123, 35))
    ref_state = ReferenceSecretGeometryState([GeneratedRoom(**{**room.__dict__, "neighbors": set()}) for room in rooms], list(room_map), [False] * 169, 123)
    clean = place_secret_room(clean_state, ())
    reference = place_secret_room_reference(ref_state, ())
    assert clean == reference
    eligible = sum(not item.occupied for item in clean.evaluations)
    assert len(clean.rng_transitions) == eligible + (1 if clean.best_candidates else 0)


def test_no_candidate_is_allowed_and_has_no_final_selection_draw():
    rooms = [GeneratedRoom(i, i % 13, i // 13, RoomShape.ROOMSHAPE_1x1, -1, -1, -1, 0) for i in range(169)]
    state = SecretGeometryState(rooms, list(range(169)), [False] * 169, IsaacRNG.game_constructor(1, 35))
    result = place_secret_room(state, ())
    assert result.room_id == -1
    assert result.rng_transitions == ()
    assert result.final_generator_rng_state == 1
