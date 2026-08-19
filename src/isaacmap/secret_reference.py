"""Mechanical reference port of the Secret-room binary helpers."""

from __future__ import annotations

from dataclasses import dataclass

from .room_config_reference import RoomConfigEntryReference
from .secret import (
    CANDIDATE_DRAW_RVA,
    SELECTION_DRAW_RVA,
    SecretCandidateEvaluation,
    SecretPlacementResult,
    SecretRNGTransition,
)
from .special_rooms import GeneratedRoom
from .topology_geometry import GRID_HEIGHT, GRID_WIDTH, RoomShape, SHAPE_DIMENSIONS


UINT32_MASK = 0xFFFFFFFF
SHIFTS = (5, 9, 7)


def _advance(value: int) -> int:
    if value == 0:
        raise ValueError("zero LevelGenerator RNG state")
    value ^= value >> SHIFTS[0]
    value ^= (value << SHIFTS[1]) & UINT32_MASK
    value ^= value >> SHIFTS[2]
    return value & UINT32_MASK


@dataclass
class ReferenceSecretGeometryState:
    rooms: list[GeneratedRoom]
    room_map: list[int]
    blocked_positions: list[bool]
    generator_rng_state: int


def _perimeter(room: GeneratedRoom) -> tuple[int, ...]:
    width, height = SHAPE_DIMENSIONS[int(room.shape)]
    x = room.column
    y = room.line
    pairs = (
        (x - 1, y), (x, y - 1), (x + width, y), (x, y + height),
        (x - 1, y + 1), (x + 1, y - 1),
        (x + width, y + 1), (x + 1, y + height),
    )
    result: list[int] = []
    for cx, cy in pairs:
        result.append(cy * 13 + cx if 0 <= cx < 13 and 0 <= cy < 13 else -1)
    return tuple(result)


def build_secret_forbidden_indices_reference(
    rooms: list[GeneratedRoom],
    descriptor_configs: dict[int, RoomConfigEntryReference],
    *,
    level_stage: int,
    start_grid_index: int = 84,
) -> tuple[int, ...]:
    tree_values: set[int] = set()
    if level_stage == 11:
        sx, sy = start_grid_index % 13, start_grid_index // 13
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            cx, cy = sx + dx, sy + dy
            if 0 <= cx < 13 and 0 <= cy < 13:
                tree_values.add(cy * 13 + cx)

    for room in rooms:
        config = descriptor_configs.get(room.generation_index)
        if config is None:
            continue
        shape = config.shape
        scan_slots = list(range(8))
        if shape == 1:
            scan_slots = [0, 1, 2, 3]
        elif shape == 4:
            scan_slots = [0, 1, 2, 3, 4, 6]
        elif shape == 6:
            scan_slots = [0, 1, 2, 3, 5, 7]
        targets = _perimeter(room)
        for slot in scan_slots:
            if targets[slot] >= 0 and (
                config.room_type in (5, 8, 7)
                or (config.door_mask & (1 << slot)) == 0
            ):
                tree_values.add(targets[slot])
    return tuple(sorted(tree_values))


def _shape_target(room: GeneratedRoom, slot: int) -> tuple[int, int]:
    shape = int(room.shape)
    width, height = SHAPE_DIMENSIONS[shape]
    if height == 1 and slot in (4, 6):
        return -1, -1
    if width == 1 and slot in (5, 7):
        return -1, -1
    if shape in (3, 5) and slot in (0, 2, 4, 6):
        return -1, -1
    if shape in (2, 7) and slot in (1, 3, 5, 7):
        return -1, -1
    x, y = room.column, room.line
    default = (
        (x - 1, y), (x, y - 1), (x + width, y), (x, y + height),
        (x - 1, y + 1), (x + 1, y - 1),
        (x + width, y + 1), (x + 1, y + height),
    )
    if shape == 9:
        table = ((x,y),(x,y),(x+2,y),(x,y+2),(x-1,y+1),(x+1,y-1),(x+2,y+1),(x+1,y+2))
    elif shape == 10:
        table = ((x-1,y),(x,y-1),(x+1,y),(x,y+2),(x-1,y+1),(x+1,y),(x+2,y+1),(x+1,y+2))
    elif shape == 11:
        table = ((x-1,y),(x,y-1),(x+2,y),(x,y+1),(x,y+1),(x+1,y-1),(x+2,y+1),(x+1,y+2))
    elif shape == 12:
        table = ((x-1,y),(x,y-1),(x+2,y),(x,y+2),(x-1,y+1),(x+1,y-1),(x+1,y+1),(x+1,y+1))
    else:
        table = default
    return table[slot]


def _refresh(state: ReferenceSecretGeometryState, room_id: int) -> None:
    room = state.rooms[room_id]
    room.doors = 0
    room.neighbors.clear()
    for slot in range(8):
        x, y = _shape_target(room, slot)
        if 0 <= x < 13 and 0 <= y < 13:
            other = state.room_map[y * 13 + x]
            if other >= 0 and other != room_id:
                room.doors |= 1 << slot
                room.neighbors.add(other)


def place_secret_room_reference(
    state: ReferenceSecretGeometryState,
    forbidden_indices: tuple[int, ...],
) -> SecretPlacementResult:
    forbidden = set(forbidden_indices)
    evaluations: list[SecretCandidateEvaluation] = []
    transitions: list[SecretRNGTransition] = []
    vector: list[int] = []
    high_score = 0
    offsets = ((-1, 0), (0, -1), (1, 0), (0, 1))

    index = 0
    while index < 169:
        occupied = state.room_map[index] >= 0
        excluded = index in forbidden
        blocked = state.blocked_positions[index]
        if occupied or excluded or blocked:
            evaluations.append(SecretCandidateEvaluation(index, occupied, excluded, blocked, None, 0, 0, None, "ineligible"))
            index += 1
            continue
        before = state.generator_rng_state
        after = _advance(before)
        state.generator_rng_state = after
        base = after % 5 + 10
        transitions.append(SecretRNGTransition(CANDIDATE_DRAW_RVA, "LevelGenerator._rng", 35, before, after, "eligible empty Secret candidate score", base))
        x, y = index % 13, index // 13
        score = base
        links = 0
        mask = 0
        direction = 0
        while direction < 4:
            dx, dy = offsets[direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < 13 and 0 <= ny < 13:
                other_id = state.room_map[ny * 13 + nx]
                if other_id >= 0:
                    if _shape_target(state.rooms[other_id], (direction - 2) & 3) == (-1, -1):
                        score -= 100
                    else:
                        links += 1
                        mask |= 1 << direction
            direction += 1
        action = "discard"
        adjusted = None
        if links != 0 and score >= 0:
            adjusted = score
            if links <= 2:
                adjusted -= 3
                if links == 1:
                    adjusted -= 3
            if high_score < adjusted:
                vector = [index]
                high_score = adjusted
                action = "replace-best"
            elif adjusted == high_score:
                vector.append(index)
                action = "append-tie"
            else:
                action = "below-best"
        evaluations.append(SecretCandidateEvaluation(index, False, False, False, base, mask, links, adjusted, action))
        index += 1

    if not vector:
        return SecretPlacementResult(-1, -1, forbidden_indices, (), high_score, tuple(evaluations), tuple(transitions), state.generator_rng_state, ())

    before = state.generator_rng_state
    after = _advance(before)
    state.generator_rng_state = after
    grid = vector[after % len(vector)]
    transitions.append(SecretRNGTransition(SELECTION_DRAW_RVA, "LevelGenerator._rng", 35, before, after, "select among maximum-score Secret candidates", grid))
    room_id = len(state.rooms)
    room = GeneratedRoom(room_id, grid % 13, grid // 13, RoomShape.ROOMSHAPE_1x1, -1, -1, -1, 0)
    state.rooms.append(room)
    state.room_map[grid] = room_id
    refreshed = [room_id]
    _refresh(state, room_id)
    for dx, dy in offsets:
        nx, ny = room.column + dx, room.line + dy
        if 0 <= nx < 13 and 0 <= ny < 13:
            other = state.room_map[ny * 13 + nx]
            if other >= 0:
                refreshed.append(other)
                _refresh(state, other)
    return SecretPlacementResult(room_id, grid, forbidden_indices, tuple(vector), high_score, tuple(evaluations), tuple(transitions), state.generator_rng_state, tuple(refreshed))
