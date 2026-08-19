"""Clean binary-derived Ultra Secret geometry for the frozen executable.

This is a research leaf, not a public complete-floor generator.  It ports
``LevelGenerator::PlaceUltraSecretRoom`` at RVA ``0x005AE640`` and the
red-door exclusion set prepared by its direct caller.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .rng import IsaacRNG
from .room_config import RoomConfigEntry
from .special_rooms import GeneratedRoom
from .topology_geometry import (
    DIRECTION_OFFSETS,
    GRID_HEIGHT,
    GRID_WIDTH,
    INVALID_POSITION,
    RoomShape,
    door_target_position,
)


GENERATOR_SHIFT_INDEX = 35
ULTRA_CONFIG_SHIFT_INDEX = 71
CANDIDATE_DRAW_RVA = 0x005AE755
SELECTION_DRAW_RVA = 0x005AEAE6

# Static vectors loaded at 0x005AE676..0x005AE6D6.  These are positions two
# steps away or diagonally adjacent to the empty Ultra candidate cell.
OUTER_OFFSETS: tuple[tuple[int, int], ...] = (
    (-2, 0),
    (-1, -1),
    (0, -2),
    (1, -1),
    (2, 0),
    (1, 1),
    (0, 2),
    (-1, 1),
)
FORCE_EXCLUDED_ROOM_TYPES = frozenset((5, 8, 7, 10))


@dataclass(frozen=True)
class UltraRNGTransition:
    binary_rva: int
    object_identity: str
    shift_index: int
    pre_state: int
    post_state: int
    reason: str
    result: int


@dataclass(frozen=True)
class UltraCandidateEvaluation:
    grid_index: int
    occupied: bool
    forbidden: bool
    blocked: bool
    base_score: int | None
    immediate_mask: int
    outer_neighbor_mask: int
    adjacency_count: int
    invalid_red_door_targets: tuple[int, ...]
    final_score: int | None
    best_action: str


@dataclass(frozen=True)
class UltraRedDoorWrite:
    room_id: int
    door_slot: int
    target_grid_index: int
    ultra_grid_index: int


@dataclass
class UltraGeometryState:
    rooms: list[GeneratedRoom]
    room_map: list[int]
    blocked_positions: list[bool]
    generator_rng: IsaacRNG
    red_door_writes: list[UltraRedDoorWrite] = field(default_factory=list)


@dataclass(frozen=True)
class UltraPlacementResult:
    room_id: int
    grid_index: int
    forbidden_indices: tuple[int, ...]
    best_candidates: tuple[int, ...]
    best_score: int
    evaluations: tuple[UltraCandidateEvaluation, ...]
    rng_transitions: tuple[UltraRNGTransition, ...]
    final_generator_rng_state: int
    connection_refresh_order: tuple[int, ...]
    red_door_writes: tuple[UltraRedDoorWrite, ...]


def _grid_index(position: tuple[int, int]) -> int:
    column, row = position
    if not (0 <= column < GRID_WIDTH and 0 <= row < GRID_HEIGHT):
        return -1
    return row * GRID_WIDTH + column


def build_ultra_forbidden_indices(
    rooms: list[GeneratedRoom] | tuple[GeneratedRoom, ...],
    descriptor_configs: dict[int, RoomConfigEntry],
) -> tuple[int, ...]:
    """Build the red-door exclusion set at RVA 0x0033C9EF..0x0033CAB6."""

    forbidden: set[int] = set()
    for room in rooms:
        config = descriptor_configs.get(room.generation_index)
        if config is None or _grid_index((room.column, room.line)) < 0:
            continue
        force = config.room_type in FORCE_EXCLUDED_ROOM_TYPES
        for slot in range(8):
            if not force and config.door_mask & (1 << slot):
                continue
            target = door_target_position(
                room.column,
                room.line,
                config.shape,
                slot,
                ignore_thin_restrictions=True,
            )
            index = _grid_index(target)
            if index >= 0:
                forbidden.add(index)
    return tuple(sorted(forbidden))


def _refresh_normal_connections(state: UltraGeometryState, room_id: int) -> None:
    room = state.rooms[room_id]
    room.doors = 0
    room.neighbors.clear()
    for slot in range(8):
        target = door_target_position(room.column, room.line, room.shape, slot)
        index = _grid_index(target)
        if index < 0:
            continue
        neighbor = state.room_map[index]
        if neighbor >= 0 and neighbor != room_id:
            room.doors |= 1 << slot
            room.neighbors.add(neighbor)


def _candidate_neighbor_is_compatible(
    room: GeneratedRoom,
    offset: tuple[int, int],
    forbidden: set[int],
) -> tuple[bool, tuple[int, ...]]:
    invalid: list[int] = []
    dx, dy = offset
    for direction, (direction_x, direction_y) in enumerate(DIRECTION_OFFSETS):
        if direction_x * dx + direction_y * dy <= 0:
            continue
        opposite_slot = (direction - 2) & 3
        target = door_target_position(
            room.column, room.line, room.shape, opposite_slot
        )
        index = _grid_index(target)
        if index < 0 or index in forbidden:
            invalid.append(index)
            return False, tuple(invalid)
    return True, ()


def _write_red_doors(
    state: UltraGeometryState, ultra_grid_index: int
) -> tuple[UltraRedDoorWrite, ...]:
    ultra_column = ultra_grid_index % GRID_WIDTH
    ultra_row = ultra_grid_index // GRID_WIDTH
    writes: list[UltraRedDoorWrite] = []
    for dx, dy in OUTER_OFFSETS:
        outer_index = _grid_index((ultra_column + dx, ultra_row + dy))
        if outer_index < 0:
            continue
        room_id = state.room_map[outer_index]
        if room_id < 0:
            continue
        room = state.rooms[room_id]
        for slot in range(8):
            target = door_target_position(room.column, room.line, room.shape, slot)
            target_index = _grid_index(target)
            if target_index < 0 or state.room_map[target_index] >= 0:
                continue
            target_column = target_index % GRID_WIDTH
            target_row = target_index // GRID_WIDTH
            if abs(target_column - ultra_column) + abs(target_row - ultra_row) != 1:
                continue
            room.doors |= 1 << slot
            write = UltraRedDoorWrite(
                room_id, slot, target_index, ultra_grid_index
            )
            writes.append(write)
            state.red_door_writes.append(write)
    return tuple(writes)


def place_ultra_secret_room(
    state: UltraGeometryState,
    forbidden_indices: tuple[int, ...],
) -> UltraPlacementResult:
    """Port ``LevelGenerator::PlaceUltraSecretRoom`` at RVA 0x005AE640."""

    forbidden = set(forbidden_indices)
    evaluations: list[UltraCandidateEvaluation] = []
    draws: list[UltraRNGTransition] = []
    best: list[int] = []
    best_score = 0

    for index in range(GRID_WIDTH * GRID_HEIGHT):
        occupied = state.room_map[index] >= 0
        blocked = state.blocked_positions[index]
        excluded = index in forbidden
        if occupied or blocked or excluded:
            evaluations.append(
                UltraCandidateEvaluation(
                    index,
                    occupied,
                    excluded,
                    blocked,
                    None,
                    0,
                    0,
                    0,
                    (),
                    None,
                    "ineligible",
                )
            )
            continue

        pre = state.generator_rng.seed
        post = state.generator_rng.next()
        base = post % 5 + 10
        draws.append(
            UltraRNGTransition(
                CANDIDATE_DRAW_RVA,
                "LevelGenerator._rng",
                GENERATOR_SHIFT_INDEX,
                pre,
                post,
                "eligible empty Ultra candidate score",
                base,
            )
        )
        column, row = index % GRID_WIDTH, index // GRID_WIDTH
        score = base
        immediate_mask = 0
        for direction, (dx, dy) in enumerate(DIRECTION_OFFSETS):
            immediate_index = _grid_index((column + dx, row + dy))
            if immediate_index < 0:
                continue
            if (
                state.room_map[immediate_index] >= 0
                or state.blocked_positions[immediate_index]
            ):
                immediate_mask |= 1 << direction
                score -= 100
                break

        outer_mask = 0
        count = 0
        invalid_targets: list[int] = []
        if score >= 0:
            for outer_position, offset in enumerate(OUTER_OFFSETS):
                if score < 0:
                    break
                dx, dy = offset
                outer_index = _grid_index((column + dx, row + dy))
                if outer_index < 0:
                    continue
                room_id = state.room_map[outer_index]
                if room_id < 0:
                    continue
                outer_mask |= 1 << outer_position
                compatible, invalid = _candidate_neighbor_is_compatible(
                    state.rooms[room_id], offset, forbidden
                )
                invalid_targets.extend(invalid)
                if not compatible:
                    score -= 100
                count += 1

        action = "discard"
        final_score: int | None = None
        if count and score >= 0:
            final_score = score if count >= 3 else score - (3 if count == 2 else 6)
            if final_score > best_score:
                best_score = final_score
                best[:] = (index,)
                action = "replace-best"
            elif final_score == best_score:
                best.append(index)
                action = "append-tie"
            else:
                action = "below-best"
        evaluations.append(
            UltraCandidateEvaluation(
                index,
                False,
                False,
                False,
                base,
                immediate_mask,
                outer_mask,
                count,
                tuple(invalid_targets),
                final_score,
                action,
            )
        )

    if not best:
        return UltraPlacementResult(
            -1,
            -1,
            forbidden_indices,
            (),
            best_score,
            tuple(evaluations),
            tuple(draws),
            state.generator_rng.seed,
            (),
            (),
        )

    pre = state.generator_rng.seed
    post = state.generator_rng.next()
    selected = best[post % len(best)]
    draws.append(
        UltraRNGTransition(
            SELECTION_DRAW_RVA,
            "LevelGenerator._rng",
            GENERATOR_SHIFT_INDEX,
            pre,
            post,
            "select among maximum-score Ultra candidates",
            selected,
        )
    )
    room_id = len(state.rooms)
    room = GeneratedRoom(
        generation_index=room_id,
        column=selected % GRID_WIDTH,
        line=selected // GRID_WIDTH,
        shape=RoomShape.ROOMSHAPE_1x1,
        origin_direction=-1,
        link_column=-1,
        link_line=-1,
        distance_from_start=0,
    )
    state.rooms.append(room)
    state.room_map[selected] = room_id
    _refresh_normal_connections(state, room_id)
    red_writes = _write_red_doors(state, selected)
    return UltraPlacementResult(
        room_id,
        selected,
        forbidden_indices,
        tuple(best),
        best_score,
        tuple(evaluations),
        tuple(draws),
        state.generator_rng.seed,
        (room_id,),
        red_writes,
    )
