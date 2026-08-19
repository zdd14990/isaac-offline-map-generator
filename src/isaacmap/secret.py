"""Clean port of the frozen executable's ordinary Secret-room leaf.

This module is deliberately research-only.  It implements the two helpers at
RVA 0x00338D70 and 0x005AE170, but it does not expose a complete map API while
Ultra Secret and late default-room selection remain incomplete.
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
    SHAPE_DIMENSIONS,
    door_target_position,
)


GENERATOR_SHIFT_INDEX = 35
CANDIDATE_DRAW_RVA = 0x005AE2B4
SELECTION_DRAW_RVA = 0x005AE4A5


@dataclass(frozen=True)
class SecretRNGTransition:
    binary_rva: int
    object_identity: str
    shift_index: int
    pre_state: int
    post_state: int
    reason: str
    result: int


@dataclass(frozen=True)
class SecretCandidateEvaluation:
    grid_index: int
    occupied: bool
    forbidden: bool
    blocked: bool
    base_score: int | None
    neighbor_mask: int
    adjacency_count: int
    final_score: int | None
    best_action: str


@dataclass
class SecretGeometryState:
    rooms: list[GeneratedRoom]
    room_map: list[int]
    blocked_positions: list[bool]
    generator_rng: IsaacRNG


@dataclass(frozen=True)
class SecretPlacementResult:
    room_id: int
    grid_index: int
    forbidden_indices: tuple[int, ...]
    best_candidates: tuple[int, ...]
    best_score: int
    evaluations: tuple[SecretCandidateEvaluation, ...]
    rng_transitions: tuple[SecretRNGTransition, ...]
    final_generator_rng_state: int
    connection_refresh_order: tuple[int, ...]


def _descriptor_perimeter_targets(room: GeneratedRoom) -> tuple[int, ...]:
    """The eight rectangular target slots materialized by RVA 0x00338D70."""

    width, height = SHAPE_DIMENSIONS[int(room.shape)]
    x, y = room.column, room.line
    coordinates = (
        (x - 1, y), (x, y - 1), (x + width, y), (x, y + height),
        (x - 1, y + 1), (x + 1, y - 1),
        (x + width, y + 1), (x + 1, y + height),
    )
    return tuple(
        cy * GRID_WIDTH + cx if 0 <= cx < GRID_WIDTH and 0 <= cy < GRID_HEIGHT else -1
        for cx, cy in coordinates
    )


def build_secret_forbidden_indices(
    rooms: list[GeneratedRoom],
    descriptor_configs: dict[int, RoomConfigEntry],
    *,
    level_stage: int,
    start_grid_index: int = 84,
) -> tuple[int, ...]:
    """Port ``Level::build_secret_candidate_set`` (RVA 0x00338D70).

    Only rooms already assigned a concrete Level RoomDescriptor participate;
    ordinary generated rooms are configured later in the binary.
    """

    forbidden: set[int] = set()
    if level_stage == 11:
        x, y = start_grid_index % GRID_WIDTH, start_grid_index // GRID_WIDTH
        for dx, dy in DIRECTION_OFFSETS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                forbidden.add(ny * GRID_WIDTH + nx)

    for room in rooms:
        config = descriptor_configs.get(room.generation_index)
        if config is None:
            continue
        shape = int(config.shape)
        if shape == 1:
            slots = (0, 1, 2, 3)
        elif shape == 4:
            slots = (0, 1, 2, 3, 4, 6)
        elif shape == 6:
            slots = (0, 1, 2, 3, 5, 7)
        else:
            slots = tuple(range(8))
        targets = _descriptor_perimeter_targets(room)
        force_forbid = config.room_type in (5, 8, 7)
        for slot in slots:
            target = targets[slot]
            if target >= 0 and (force_forbid or not (config.door_mask & (1 << slot))):
                forbidden.add(target)
    return tuple(sorted(forbidden))


def _refresh_connections(state: SecretGeometryState, room_id: int) -> None:
    room = state.rooms[room_id]
    room.doors = 0
    room.neighbors.clear()
    for slot in range(8):
        target = door_target_position(room.column, room.line, room.shape, slot)
        if target == INVALID_POSITION:
            continue
        x, y = target
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            continue
        neighbor = state.room_map[y * GRID_WIDTH + x]
        if neighbor >= 0 and neighbor != room_id:
            room.doors |= 1 << slot
            room.neighbors.add(neighbor)


def place_secret_room(
    state: SecretGeometryState,
    forbidden_indices: tuple[int, ...],
) -> SecretPlacementResult:
    """Port ``LevelGenerator::PlaceSecretRoom`` at RVA 0x005AE170."""

    forbidden = set(forbidden_indices)
    evaluations: list[SecretCandidateEvaluation] = []
    draws: list[SecretRNGTransition] = []
    best: list[int] = []
    best_score = 0

    for index in range(GRID_WIDTH * GRID_HEIGHT):
        occupied = state.room_map[index] >= 0
        excluded = index in forbidden
        blocked = state.blocked_positions[index]
        if occupied or excluded or blocked:
            evaluations.append(SecretCandidateEvaluation(
                index, occupied, excluded, blocked, None, 0, 0, None, "ineligible"
            ))
            continue

        pre = state.generator_rng.seed
        post = state.generator_rng.next()
        base = post % 5 + 10
        draws.append(SecretRNGTransition(
            CANDIDATE_DRAW_RVA, "LevelGenerator._rng", GENERATOR_SHIFT_INDEX,
            pre, post, "eligible empty Secret candidate score", base,
        ))
        x, y = index % GRID_WIDTH, index // GRID_WIDTH
        score = base
        count = 0
        neighbor_mask = 0
        for direction, (dx, dy) in enumerate(DIRECTION_OFFSETS):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
                continue
            neighbor_id = state.room_map[ny * GRID_WIDTH + nx]
            if neighbor_id < 0:
                continue
            neighbor = state.rooms[neighbor_id]
            opposite_slot = (direction - 2) & 3
            target = door_target_position(
                neighbor.column, neighbor.line, neighbor.shape, opposite_slot
            )
            if target == INVALID_POSITION:
                score -= 100
            else:
                count += 1
                neighbor_mask |= 1 << direction

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
        evaluations.append(SecretCandidateEvaluation(
            index, False, False, False, base, neighbor_mask, count, final_score, action
        ))

    if not best:
        return SecretPlacementResult(
            -1, -1, forbidden_indices, (), best_score, tuple(evaluations),
            tuple(draws), state.generator_rng.seed, (),
        )

    pre = state.generator_rng.seed
    post = state.generator_rng.next()
    selected = best[post % len(best)]
    draws.append(SecretRNGTransition(
        SELECTION_DRAW_RVA, "LevelGenerator._rng", GENERATOR_SHIFT_INDEX,
        pre, post, "select among maximum-score Secret candidates", selected,
    ))
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

    refresh: list[int] = [room_id]
    _refresh_connections(state, room_id)
    for dx, dy in DIRECTION_OFFSETS:
        nx, ny = room.column + dx, room.line + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            neighbor = state.room_map[ny * GRID_WIDTH + nx]
            if neighbor >= 0:
                refresh.append(neighbor)
                _refresh_connections(state, neighbor)

    return SecretPlacementResult(
        room_id, selected, forbidden_indices, tuple(best), best_score,
        tuple(evaluations), tuple(draws), state.generator_rng.seed, tuple(refresh),
    )
