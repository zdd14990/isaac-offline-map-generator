"""Binary-like early post-topology reference for Basement I.

The recovered slice is deliberately limited to the true first two room
operations: Boss, then RoomType 8 (Super Secret).  It preserves the stable
dead-end erases and all persistent/temporary RNG identities.  Shop, Treasure,
Secret and later operations are not implemented here, so the public generator
must continue to fail closed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import struct
from typing import Iterable

from .boss_pool_reference import (
    BossPoolEntryReference,
    FreshBossSelectionReference,
    pick_fresh_basement_boss_reference,
)
from .resources import RoomDefinition
from .room_config_reference import room_definition_door_mask
from .special_room_geometry_reference import reshape_end_room_reference


UINT32_MASK = 0xFFFFFFFF
LEVEL_SHIFT_INDEX = 35
LEVEL_SHIFTS = (5, 9, 7)
BOSS_CONFIG_SHIFT_INDEX = 39
BOSS_CONFIG_SHIFTS = (5, 15, 17)
TYPE8_SHIFT_INDEX = 9
TYPE8_SHIFTS = (2, 5, 15)
ROOM_CONFIG_SHIFT_INDEX = 7
ROOM_CONFIG_SHIFTS = (1, 21, 20)
GRID_WIDTH = 13
GRID_HEIGHT = 13

_SHAPE_OFFSETS = (
    (), ((0, 0),), ((0, 0),), ((0, 0),),
    ((0, 0), (0, 1)), ((0, 0), (0, 1)),
    ((0, 0), (1, 0)), ((0, 0), (1, 0)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
    ((1, 0), (0, 1), (1, 1)),
    ((0, 0), (0, 1), (1, 1)),
    ((0, 0), (1, 0), (1, 1)),
    ((0, 0), (1, 0), (0, 1)),
)
_SHAPE_DIMENSIONS = (
    (0, 0), (1, 1), (1, 1), (1, 1), (1, 2), (1, 2),
    (2, 1), (2, 1), (2, 2), (2, 2), (2, 2), (2, 2), (2, 2),
)


def _f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


_FLOAT_SCALE = struct.unpack("<f", struct.pack("<I", 0x2F7FFFFE))[0]


def _advance(state: int, shifts: tuple[int, int, int]) -> int:
    if state == 0:
        raise ValueError("the profiled binary asserts before drawing a zero RNG state")
    state ^= state >> shifts[0]
    state ^= (state << shifts[1]) & UINT32_MASK
    state ^= state >> shifts[2]
    return state & UINT32_MASK


def _unit_float(state: int) -> float:
    return _f32(_f32(float(state & UINT32_MASK)) * _FLOAT_SCALE)


def _in_bounds(column: int, line: int) -> bool:
    return 0 <= column < GRID_WIDTH and 0 <= line < GRID_HEIGHT


def _grid_index(column: int, line: int) -> int:
    return line * GRID_WIDTH + column if _in_bounds(column, line) else -1


def _has_slot(shape: int, slot: int) -> bool:
    width, height = _SHAPE_DIMENSIONS[shape]
    if height == 1 and slot in (4, 6):
        return False
    if width == 1 and slot in (5, 7):
        return False
    if shape in (3, 5) and slot in (0, 2, 4, 6):
        return False
    if shape in (2, 7) and slot in (1, 3, 5, 7):
        return False
    return True


def _door_target(column: int, line: int, shape: int, slot: int) -> tuple[int, int]:
    if not _has_slot(shape, slot):
        return -1, -1
    width, height = _SHAPE_DIMENSIONS[shape]
    table = (
        (column - 1, line), (column, line - 1), (column + width, line),
        (column, line + height), (column - 1, line + 1),
        (column + 1, line - 1), (column + width, line + 1),
        (column + 1, line + height),
    )
    if shape == 9:
        table = ((column, line), (column, line), (column + 2, line),
                 (column, line + 2), (column - 1, line + 1),
                 (column + 1, line - 1), (column + 2, line + 1),
                 (column + 1, line + 2))
    elif shape == 10:
        table = ((column - 1, line), (column, line - 1), (column + 1, line),
                 (column, line + 2), (column - 1, line + 1),
                 (column + 1, line), (column + 2, line + 1),
                 (column + 1, line + 2))
    elif shape == 11:
        table = ((column - 1, line), (column, line - 1), (column + 2, line),
                 (column, line + 1), (column, line + 1),
                 (column + 1, line - 1), (column + 2, line + 1),
                 (column + 1, line + 2))
    elif shape == 12:
        table = ((column - 1, line), (column, line - 1), (column + 2, line),
                 (column, line + 2), (column - 1, line + 1),
                 (column + 1, line - 1), (column + 1, line + 1),
                 (column + 1, line + 1))
    return table[slot]


@dataclass
class PostRoomReference:
    generation_index: int
    column: int
    line: int
    shape: int
    origin_direction: int
    link_column: int
    link_line: int
    distance_from_start: int
    doors: int = 0
    neighbors: set[int] = field(default_factory=set)
    room_type: int = 1
    variant: int = -1
    subtype: int = -1

    @property
    def cells(self) -> tuple[tuple[int, int], ...]:
        return tuple((self.column + x, self.line + y) for x, y in _SHAPE_OFFSETS[self.shape])


@dataclass(frozen=True)
class ConfigReference:
    resource_index: int
    room_type: int
    variant: int
    subtype: int
    difficulty: int
    shape: int
    initial_weight: float
    door_mask: int


@dataclass(frozen=True)
class SpecialDrawReference:
    sequence: int
    binary_rva: int
    object_identity: str
    shift_index: int
    shifts: tuple[int, int, int]
    pre_state: int
    post_state: int
    reason: str
    usage: str


@dataclass(frozen=True)
class CandidateEventReference:
    operation: str
    candidate_order: tuple[int, ...]
    tested_room: int
    accepted: bool
    dead_ends_after: tuple[int, ...]


@dataclass
class PostTopologyStateReference:
    rooms: list[PostRoomReference]
    room_map: list[int]
    dead_ends: list[int]
    level_rng_state: int
    room_config_weights: dict[int, float]
    rng_ledger: list[SpecialDrawReference] = field(default_factory=list)
    candidate_events: list[CandidateEventReference] = field(default_factory=list)


@dataclass(frozen=True)
class BossThenType8ReferenceResult:
    completed: bool
    abort_operation: str | None
    boss: FreshBossSelectionReference
    boss_room: int
    type8_rooms: tuple[int, ...]
    rooms: tuple[PostRoomReference, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    final_level_rng_state: int
    room_config_weights: tuple[tuple[int, float], ...]
    rng_ledger: tuple[SpecialDrawReference, ...]
    candidate_events: tuple[CandidateEventReference, ...]


def _door_mask(room: RoomDefinition) -> int:
    # Double-trouble Boss configs (variants 3700..3849) must remain in the
    # weighted pool because selecting and rejecting one consumes RNG and
    # decays its weight.  Their door masks are never passed to the end-room
    # matcher in this scoped path.
    return room_definition_door_mask(room)


def configs_from_room_definitions_reference(
    rooms: Iterable[RoomDefinition],
) -> tuple[ConfigReference, ...]:
    result: list[ConfigReference] = []
    for index, room in enumerate(rooms):
        result.append(
            ConfigReference(index, room.room_type, room.variant, room.subtype,
                            room.difficulty, room.shape, _f32(room.weight), _door_mask(room))
        )
    return tuple(result)


def state_from_topology_reference(topology: object, level_rng_state: int) -> PostTopologyStateReference:
    rooms = [
        PostRoomReference(
            generation_index=int(room.generation_index),
            column=int(room.column), line=int(room.line), shape=int(room.shape),
            origin_direction=int(room.origin_neighbor_connect_dir),
            link_column=int(room.link_column), link_line=int(room.link_line),
            distance_from_start=int(room.distance_from_start),
            doors=int(room.doors), neighbors=set(room.neighbors),
        )
        for room in topology.rooms
    ]
    return PostTopologyStateReference(
        rooms=rooms,
        room_map=list(topology.room_map),
        dead_ends=list(topology.dead_ends),
        level_rng_state=level_rng_state,
        room_config_weights={},
    )


def _record_draw(
    state: PostTopologyStateReference, *, rva: int, identity: str,
    shift_index: int, shifts: tuple[int, int, int], pre: int, post: int,
    reason: str, usage: str,
) -> None:
    state.rng_ledger.append(
        SpecialDrawReference(len(state.rng_ledger), rva, identity, shift_index,
                             shifts, pre, post, reason, usage)
    )


def _select_config(
    state: PostTopologyStateReference,
    seed: int,
    configs: tuple[ConfigReference, ...],
    *, room_type: int, subtype: int,
) -> tuple[ConfigReference, int]:
    candidates = [
        config for config in configs
        if config.room_type == room_type
        and (subtype < 0 or config.subtype == subtype)
        and 1 <= config.difficulty <= 10
    ]
    if not candidates:
        raise ValueError(f"no RoomConfig candidates for type={room_type}, subtype={subtype}")
    total = _f32(0.0)
    for config in candidates:
        total = _f32(total + state.room_config_weights.get(
            config.resource_index, config.initial_weight
        ))
    post = _advance(seed, ROOM_CONFIG_SHIFTS)
    _record_draw(
        state, rva=0x0042CBDE,
        identity=f"RoomConfig::GetRandomRoom.local(seed=0x{seed:08X})",
        shift_index=ROOM_CONFIG_SHIFT_INDEX, shifts=ROOM_CONFIG_SHIFTS,
        pre=seed, post=post, reason="weighted concrete STB entry selection",
        usage=f"ROOMTYPE {room_type} cumulative-weight threshold",
    )
    threshold = _f32(_unit_float(post) * total)
    cumulative = _f32(0.0)
    selected = candidates[-1]
    for config in candidates:
        cumulative = _f32(cumulative + state.room_config_weights.get(
            config.resource_index, config.initial_weight
        ))
        if threshold < cumulative:
            selected = config
            break
    old_weight = state.room_config_weights.get(selected.resource_index, selected.initial_weight)
    state.room_config_weights[selected.resource_index] = max(
        _f32(old_weight * _f32(0.1)), _f32(1.0e-7)
    )
    return selected, post


def _rebuild_connections(state: PostTopologyStateReference) -> None:
    for room in state.rooms:
        room.doors = 0
        room.neighbors.clear()
        slot = 0
        bit = 1
        while slot < 8:
            column, line = _door_target(room.column, room.line, room.shape, slot)
            index = _grid_index(column, line)
            if index >= 0:
                neighbor = state.room_map[index]
                if neighbor >= 0 and neighbor != room.generation_index:
                    room.doors |= bit
                    room.neighbors.add(neighbor)
            slot += 1
            bit <<= 1


def _try_shape1_match(
    state: PostTopologyStateReference, room_id: int, required_doors: int
) -> bool:
    return reshape_end_room_reference(state, room_id, 1, required_doors)


def _get_new_end_room(
    state: PostTopologyStateReference,
    config: ConfigReference,
    operation: str,
    *, boss_distance_filter: bool,
) -> int:
    order = tuple(state.dead_ends)
    position = 0
    while position < len(state.dead_ends):
        room_id = state.dead_ends[position]
        accepted = (
            (not boss_distance_filter or state.rooms[room_id].distance_from_start > 1)
            and reshape_end_room_reference(
                state, room_id, config.shape, config.door_mask
            )
        )
        if accepted:
            del state.dead_ends[position]
            state.candidate_events.append(
                CandidateEventReference(operation, order, room_id, True, tuple(state.dead_ends))
            )
            return room_id
        state.candidate_events.append(
            CandidateEventReference(operation, order, room_id, False, tuple(state.dead_ends))
        )
        position += 1
    return -1


def run_boss_then_type8_reference(
    topology: object,
    *, game_start_seed: int,
    level_rng_state: int,
    boss_entries: tuple[BossPoolEntryReference, ...],
    special_configs: tuple[ConfigReference, ...],
    collectible_589_owned: bool = False,
) -> BossThenType8ReferenceResult:
    state = state_from_topology_reference(topology, level_rng_state)
    boss = pick_fresh_basement_boss_reference(game_start_seed, boss_entries)

    pre = state.level_rng_state
    state.level_rng_state = _advance(pre, LEVEL_SHIFTS)
    _record_draw(
        state, rva=0x003394A4, identity="Level._generationRNG",
        shift_index=LEVEL_SHIFT_INDEX, shifts=LEVEL_SHIFTS,
        pre=pre, post=state.level_rng_state,
        reason="seed Boss RoomConfig selector", usage="temporary (5,15,17) RNG seed",
    )
    boss_local = _advance(state.level_rng_state, BOSS_CONFIG_SHIFTS)
    _record_draw(
        state, rva=0x0033930E,
        identity="Level::select_boss_room_config.local",
        shift_index=BOSS_CONFIG_SHIFT_INDEX, shifts=BOSS_CONFIG_SHIFTS,
        pre=state.level_rng_state, post=boss_local,
        reason="Boss RoomConfig retry iteration", usage="RoomConfig weighted-selector seed",
    )
    boss_config, _ = _select_config(
        state, boss_local, special_configs, room_type=5, subtype=abs(boss.boss_id)
    )
    retry = 50
    while boss_config.room_type == 5 and 3700 <= boss_config.variant < 3850 and retry > 0:
        pre_local = boss_local
        boss_local = _advance(boss_local, BOSS_CONFIG_SHIFTS)
        _record_draw(
            state, rva=0x0033930E,
            identity="Level::select_boss_room_config.local",
            shift_index=BOSS_CONFIG_SHIFT_INDEX, shifts=BOSS_CONFIG_SHIFTS,
            pre=pre_local, post=boss_local,
            reason="rejected double-room variant retry", usage="next RoomConfig seed",
        )
        boss_config, _ = _select_config(
            state, boss_local, special_configs, room_type=5, subtype=abs(boss.boss_id)
        )
        retry -= 1

    boss_room = _get_new_end_room(
        state, boss_config, "DetermineBossRoom", boss_distance_filter=True
    )
    if boss_room < 0:
        # LevelGenerator::post_topology_dispatch returns null.  Its caller
        # tears down the partial Level and retries the outer generation loop;
        # the Level, LevelGenerator and BossPool RNG objects are not rewound.
        return BossThenType8ReferenceResult(
            completed=False, abort_operation="Boss",
            boss=boss, boss_room=-1, type8_rooms=(),
            rooms=tuple(state.rooms), room_map=tuple(state.room_map),
            dead_ends=tuple(state.dead_ends),
            final_level_rng_state=state.level_rng_state,
            room_config_weights=tuple(sorted(state.room_config_weights.items())),
            rng_ledger=tuple(state.rng_ledger),
            candidate_events=tuple(state.candidate_events),
        )
    # post_topology_dispatch validates the selected room with the same matcher again.
    if not reshape_end_room_reference(
        state, boss_room, boss_config.shape, boss_config.door_mask
    ):
        return BossThenType8ReferenceResult(
            completed=False, abort_operation="Boss validation",
            boss=boss, boss_room=boss_room, type8_rooms=(),
            rooms=tuple(state.rooms), room_map=tuple(state.room_map),
            dead_ends=tuple(state.dead_ends),
            final_level_rng_state=state.level_rng_state,
            room_config_weights=tuple(sorted(state.room_config_weights.items())),
            rng_ledger=tuple(state.rng_ledger),
            candidate_events=tuple(state.candidate_events),
        )
    room = state.rooms[boss_room]
    room.room_type = 5
    room.variant = boss_config.variant
    room.subtype = boss_config.subtype

    pre = state.level_rng_state
    state.level_rng_state = _advance(pre, LEVEL_SHIFTS)
    _record_draw(
        state, rva=0x00339A87, identity="Level._generationRNG",
        shift_index=LEVEL_SHIFT_INDEX, shifts=LEVEL_SHIFTS,
        pre=pre, post=state.level_rng_state,
        reason="seed RoomType 8 private selector", usage="temporary (2,5,15) RNG seed",
    )
    private = state.level_rng_state
    placed: list[int] = []
    wanted = 2 if collectible_589_owned else 1
    iteration = 0
    while iteration < wanted:
        private_pre = private
        private = _advance(private, TYPE8_SHIFTS)
        _record_draw(
            state, rva=0x00339B1E,
            identity="post-topology RoomType8.local",
            shift_index=TYPE8_SHIFT_INDEX, shifts=TYPE8_SHIFTS,
            pre=private_pre, post=private,
            reason=f"RoomType 8 iteration {iteration}", usage="RoomConfig selector seed",
        )
        config, _ = _select_config(
            state, private, special_configs, room_type=8, subtype=-1
        )
        selected = _get_new_end_room(
            state, config, "GetNewEndRoom(RoomType8)", boss_distance_filter=False
        )
        if selected < 0:
            if iteration == 0:
                return BossThenType8ReferenceResult(
                    completed=False, abort_operation="RoomType8",
                    boss=boss, boss_room=boss_room, type8_rooms=(),
                    rooms=tuple(state.rooms), room_map=tuple(state.room_map),
                    dead_ends=tuple(state.dead_ends),
                    final_level_rng_state=state.level_rng_state,
                    room_config_weights=tuple(sorted(state.room_config_weights.items())),
                    rng_ledger=tuple(state.rng_ledger),
                    candidate_events=tuple(state.candidate_events),
                )
            break
        selected_room = state.rooms[selected]
        selected_room.room_type = 8
        selected_room.variant = config.variant
        selected_room.subtype = config.subtype
        placed.append(selected)
        iteration += 1

    return BossThenType8ReferenceResult(
        completed=True,
        abort_operation=None,
        boss=boss,
        boss_room=boss_room,
        type8_rooms=tuple(placed),
        rooms=tuple(state.rooms), room_map=tuple(state.room_map),
        dead_ends=tuple(state.dead_ends),
        final_level_rng_state=state.level_rng_state,
        room_config_weights=tuple(sorted(state.room_config_weights.items())),
        rng_ledger=tuple(state.rng_ledger),
        candidate_events=tuple(state.candidate_events),
    )
