"""Readable early post-topology implementation for Basement I research.

This clean port currently stops after the binary-ordered Boss and RoomType 8
passes.  It is intentionally not exposed as an exact-map API while Shop,
Treasure, Secret and the rest of the post-topology pipeline remain incomplete.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Iterable
import struct

from .boss_pool import BossPoolEntry, FreshBossSelection, pick_fresh_basement_boss
from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config_reference import room_definition_door_mask
from .special_room_geometry import EndRoomGeometryEvent, reshape_end_room
from .topology_geometry import (
    GRID_HEIGHT,
    GRID_WIDTH,
    RoomShape,
    door_target_position,
    occupied_cells,
)


LEVEL_SHIFT_INDEX = 35
BOSS_CONFIG_SHIFT_INDEX = 39
TYPE8_SHIFT_INDEX = 9
ROOM_CONFIG_SHIFT_INDEX = 7


def _f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


@dataclass
class GeneratedRoom:
    generation_index: int
    column: int
    line: int
    shape: RoomShape
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
        return occupied_cells(self.column, self.line, self.shape)


@dataclass(frozen=True)
class RoomConfigEntry:
    resource_index: int
    room_type: int
    variant: int
    subtype: int
    difficulty: int
    shape: int
    initial_weight: float
    door_mask: int


@dataclass(frozen=True)
class SpecialRNGTransition:
    object_identity: str
    pre_state: int
    post_state: int
    shift_index: int
    binary_rva: int
    reason: str


@dataclass(frozen=True)
class CandidateTrace:
    operation: str
    candidate_order: tuple[int, ...]
    tested_room: int
    accepted: bool
    dead_ends_after: tuple[int, ...]


@dataclass
class PostTopologyState:
    rooms: list[GeneratedRoom]
    room_map: list[int]
    dead_ends: list[int]
    level_rng: IsaacRNG
    config_weights: dict[int, float] = field(default_factory=dict)
    rng_trace: list[SpecialRNGTransition] = field(default_factory=list)
    candidate_trace: list[CandidateTrace] = field(default_factory=list)
    geometry_trace: list[EndRoomGeometryEvent] = field(default_factory=list)


@dataclass(frozen=True)
class BossThenType8Result:
    completed: bool
    abort_operation: str | None
    boss: FreshBossSelection
    boss_room: int
    type8_rooms: tuple[int, ...]
    rooms: tuple[GeneratedRoom, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    final_level_rng_state: int
    config_weights: tuple[tuple[int, float], ...]
    rng_trace: tuple[SpecialRNGTransition, ...]
    candidate_trace: tuple[CandidateTrace, ...]


def _door_mask(definition: RoomDefinition) -> int:
    return room_definition_door_mask(definition)


def room_configs_from_definitions(
    definitions: Iterable[RoomDefinition],
) -> tuple[RoomConfigEntry, ...]:
    return tuple(
        RoomConfigEntry(
            resource_index=index,
            room_type=room.room_type,
            variant=room.variant,
            subtype=room.subtype,
            difficulty=room.difficulty,
            shape=room.shape,
            initial_weight=_f32(room.weight),
            door_mask=_door_mask(room),
        )
        for index, room in enumerate(definitions)
    )


def state_from_topology(topology: object, level_rng_state: int) -> PostTopologyState:
    return PostTopologyState(
        rooms=[
            GeneratedRoom(
                generation_index=int(room.generation_index),
                column=int(room.column), line=int(room.line),
                shape=RoomShape(int(room.shape)),
                origin_direction=int(room.origin_neighbor_connect_dir),
                link_column=int(room.link_column), link_line=int(room.link_line),
                distance_from_start=int(room.distance_from_start),
                doors=int(room.doors), neighbors=set(room.neighbors),
            )
            for room in topology.rooms
        ],
        room_map=list(topology.room_map),
        dead_ends=list(topology.dead_ends),
        level_rng=IsaacRNG.game_constructor(level_rng_state, LEVEL_SHIFT_INDEX),
    )


def _trace_draw(
    state: PostTopologyState,
    identity: str,
    rng: IsaacRNG,
    shift_index: int,
    binary_rva: int,
    reason: str,
) -> int:
    pre = rng.seed
    post = rng.next()
    state.rng_trace.append(
        SpecialRNGTransition(identity, pre, post, shift_index, binary_rva, reason)
    )
    return post


def _select_config(
    state: PostTopologyState,
    seed: int,
    configs: tuple[RoomConfigEntry, ...],
    *, room_type: int,
    subtype: int,
) -> RoomConfigEntry:
    candidates = tuple(
        config for config in configs
        if config.room_type == room_type
        and (subtype < 0 or config.subtype == subtype)
        and 1 <= config.difficulty <= 10
    )
    if not candidates:
        raise ValueError(f"no RoomConfig candidates for type={room_type}, subtype={subtype}")
    selector = IsaacRNG.game_constructor(seed, ROOM_CONFIG_SHIFT_INDEX)
    unit = _trace_draw(
        state, f"RoomConfig::GetRandomRoom.local(seed=0x{seed:08X})",
        selector, ROOM_CONFIG_SHIFT_INDEX, 0x0042CBDE,
        "weighted concrete STB entry selection",
    )
    # Reconstruct RandomFloat from the already-recorded result without a
    # second draw.
    unit_float = _f32(_f32(float(unit)) * struct.unpack("<f", struct.pack("<I", 0x2F7FFFFE))[0])
    total = _f32(0.0)
    for config in candidates:
        total = _f32(
            total + state.config_weights.get(config.resource_index, config.initial_weight)
        )
    threshold = _f32(unit_float * total)
    cumulative = _f32(0.0)
    selected = candidates[-1]
    for config in candidates:
        cumulative = _f32(
            cumulative + state.config_weights.get(config.resource_index, config.initial_weight)
        )
        if threshold < cumulative:
            selected = config
            break
    current = state.config_weights.get(selected.resource_index, selected.initial_weight)
    state.config_weights[selected.resource_index] = max(
        _f32(current * _f32(0.1)), _f32(1.0e-7)
    )
    return selected


def _rebuild_connections(state: PostTopologyState) -> None:
    for room in state.rooms:
        room.doors = 0
        room.neighbors.clear()
        for slot in range(8):
            target = door_target_position(room.column, room.line, room.shape, slot)
            if not (0 <= target[0] < GRID_WIDTH and 0 <= target[1] < GRID_HEIGHT):
                continue
            neighbor = state.room_map[target[1] * GRID_WIDTH + target[0]]
            if neighbor >= 0 and neighbor != room.generation_index:
                room.doors |= 1 << slot
                room.neighbors.add(neighbor)


def _reshape_to_matching_endroom(
    state: PostTopologyState, room_id: int, config: RoomConfigEntry
) -> bool:
    return reshape_end_room(
        state, room_id, config.shape, config.door_mask, events=state.geometry_trace
    )


def _consume_first_matching_endroom(
    state: PostTopologyState,
    config: RoomConfigEntry,
    operation: str,
    *, minimum_distance: int | None = None,
) -> int:
    original_order = tuple(state.dead_ends)
    for position, room_id in enumerate(state.dead_ends):
        accepted = (
            (minimum_distance is None or state.rooms[room_id].distance_from_start > minimum_distance)
            and _reshape_to_matching_endroom(state, room_id, config)
        )
        state.candidate_trace.append(
            CandidateTrace(operation, original_order, room_id, accepted, tuple(
                state.dead_ends[:position] + state.dead_ends[position + 1:]
                if accepted else state.dead_ends
            ))
        )
        if accepted:
            del state.dead_ends[position]
            return room_id
    return -1


def run_boss_then_type8(
    topology: object,
    *, game_start_seed: int,
    level_rng_state: int,
    boss_entries: tuple[BossPoolEntry, ...],
    special_configs: tuple[RoomConfigEntry, ...],
    collectible_589_owned: bool = False,
) -> BossThenType8Result:
    state = state_from_topology(topology, level_rng_state)
    boss = pick_fresh_basement_boss(game_start_seed, boss_entries)

    boss_seed = _trace_draw(
        state, "Level._generationRNG", state.level_rng, LEVEL_SHIFT_INDEX,
        0x003394A4, "seed Boss RoomConfig selector",
    )
    boss_config_rng = IsaacRNG.game_constructor(boss_seed, BOSS_CONFIG_SHIFT_INDEX)
    boss_config_seed = _trace_draw(
        state, "Level::select_boss_room_config.local", boss_config_rng,
        BOSS_CONFIG_SHIFT_INDEX, 0x0033930E, "Boss RoomConfig retry iteration",
    )
    boss_config = _select_config(
        state, boss_config_seed, special_configs, room_type=5, subtype=abs(boss.boss_id)
    )
    retries_left = 50
    while 3700 <= boss_config.variant < 3850 and retries_left > 0:
        boss_config_seed = _trace_draw(
            state, "Level::select_boss_room_config.local", boss_config_rng,
            BOSS_CONFIG_SHIFT_INDEX, 0x0033930E, "rejected double-room variant retry",
        )
        boss_config = _select_config(
            state, boss_config_seed, special_configs,
            room_type=5, subtype=abs(boss.boss_id),
        )
        retries_left -= 1

    boss_room = _consume_first_matching_endroom(
        state, boss_config, "DetermineBossRoom", minimum_distance=1
    )
    if boss_room < 0:
        return BossThenType8Result(
            completed=False, abort_operation="Boss",
            boss=boss, boss_room=-1, type8_rooms=(),
            rooms=tuple(replace(room, neighbors=set(room.neighbors)) for room in state.rooms),
            room_map=tuple(state.room_map), dead_ends=tuple(state.dead_ends),
            final_level_rng_state=state.level_rng.seed,
            config_weights=tuple(sorted(state.config_weights.items())),
            rng_trace=tuple(state.rng_trace), candidate_trace=tuple(state.candidate_trace),
        )
    if not _reshape_to_matching_endroom(state, boss_room, boss_config):
        return BossThenType8Result(
            completed=False, abort_operation="Boss validation",
            boss=boss, boss_room=boss_room, type8_rooms=(),
            rooms=tuple(replace(room, neighbors=set(room.neighbors)) for room in state.rooms),
            room_map=tuple(state.room_map), dead_ends=tuple(state.dead_ends),
            final_level_rng_state=state.level_rng.seed,
            config_weights=tuple(sorted(state.config_weights.items())),
            rng_trace=tuple(state.rng_trace), candidate_trace=tuple(state.candidate_trace),
        )
    state.rooms[boss_room].room_type = 5
    state.rooms[boss_room].variant = boss_config.variant
    state.rooms[boss_room].subtype = boss_config.subtype

    type8_seed = _trace_draw(
        state, "Level._generationRNG", state.level_rng, LEVEL_SHIFT_INDEX,
        0x00339A87, "seed RoomType 8 private selector",
    )
    type8_rng = IsaacRNG.game_constructor(type8_seed, TYPE8_SHIFT_INDEX)
    selected_type8: list[int] = []
    wanted = 2 if collectible_589_owned else 1
    for iteration in range(wanted):
        config_seed = _trace_draw(
            state, "post-topology RoomType8.local", type8_rng,
            TYPE8_SHIFT_INDEX, 0x00339B1E, f"RoomType 8 iteration {iteration}",
        )
        config = _select_config(
            state, config_seed, special_configs, room_type=8, subtype=-1
        )
        room_id = _consume_first_matching_endroom(
            state, config, "GetNewEndRoom(RoomType8)"
        )
        if room_id < 0:
            if iteration == 0:
                return BossThenType8Result(
                    completed=False, abort_operation="RoomType8",
                    boss=boss, boss_room=boss_room, type8_rooms=(),
                    rooms=tuple(replace(room, neighbors=set(room.neighbors)) for room in state.rooms),
                    room_map=tuple(state.room_map), dead_ends=tuple(state.dead_ends),
                    final_level_rng_state=state.level_rng.seed,
                    config_weights=tuple(sorted(state.config_weights.items())),
                    rng_trace=tuple(state.rng_trace), candidate_trace=tuple(state.candidate_trace),
                )
            break
        state.rooms[room_id].room_type = 8
        state.rooms[room_id].variant = config.variant
        state.rooms[room_id].subtype = config.subtype
        selected_type8.append(room_id)

    return BossThenType8Result(
        completed=True, abort_operation=None,
        boss=boss, boss_room=boss_room, type8_rooms=tuple(selected_type8),
        rooms=tuple(replace(room, neighbors=set(room.neighbors)) for room in state.rooms),
        room_map=tuple(state.room_map), dead_ends=tuple(state.dead_ends),
        final_level_rng_state=state.level_rng.seed,
        config_weights=tuple(sorted(state.config_weights.items())),
        rng_trace=tuple(state.rng_trace), candidate_trace=tuple(state.candidate_trace),
    )
