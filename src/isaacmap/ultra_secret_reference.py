"""Mechanical reference transcription of Ultra Secret placement.

The control flow follows RVA 0x005AE640 directly and intentionally differs in
structure from the readable clean implementation in ``ultra_secret.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .rng import IsaacRNG
from .room_config import RoomConfigEntry
from .special_rooms import GeneratedRoom
from .topology_geometry import (
    GRID_HEIGHT,
    GRID_WIDTH,
    RoomShape,
    door_target_position,
)


CARDINAL = ((-1, 0), (0, -1), (1, 0), (0, 1))
RING = (
    (-2, 0),
    (-1, -1),
    (0, -2),
    (1, -1),
    (2, 0),
    (1, 1),
    (0, 2),
    (-1, 1),
)


@dataclass
class UltraReferenceState:
    rooms: list[GeneratedRoom]
    room_map: list[int]
    blocked: list[bool]
    rng: IsaacRNG


@dataclass(frozen=True)
class UltraReferenceEvaluation:
    index: int
    occupied: bool
    forbidden: bool
    blocked: bool
    base: int | None
    immediate_mask: int
    ring_mask: int
    count: int
    invalid_targets: tuple[int, ...]
    score: int | None
    action: str


@dataclass(frozen=True)
class UltraReferenceResult:
    room_id: int
    grid_index: int
    forbidden: tuple[int, ...]
    best: tuple[int, ...]
    best_score: int
    evaluations: tuple[UltraReferenceEvaluation, ...]
    transitions: tuple[tuple[int, int, str, int], ...]
    final_rng: int
    red_writes: tuple[tuple[int, int, int, int], ...]
    rooms: tuple[GeneratedRoom, ...]
    room_map: tuple[int, ...]


def _index(x: int, y: int) -> int:
    return y * 13 + x if 0 <= x < 13 and 0 <= y < 13 else -1


def build_ultra_forbidden_indices_reference(
    rooms: list[GeneratedRoom] | tuple[GeneratedRoom, ...],
    configs: dict[int, RoomConfigEntry],
) -> tuple[int, ...]:
    values: set[int] = set()
    for descriptor in rooms:
        data = configs.get(descriptor.generation_index)
        if data is None or _index(descriptor.column, descriptor.line) < 0:
            continue
        for slot in range(8):
            if not (data.door_mask & (1 << slot)) or data.room_type in (5, 8, 7, 10):
                x, y = door_target_position(
                    descriptor.column,
                    descriptor.line,
                    data.shape,
                    slot,
                    ignore_thin_restrictions=True,
                )
                candidate = _index(x, y)
                if candidate >= 0:
                    values.add(candidate)
    return tuple(sorted(values))


def place_ultra_secret_room_reference(
    state: UltraReferenceState, forbidden_values: tuple[int, ...]
) -> UltraReferenceResult:
    forbidden = set(forbidden_values)
    maximum = 0
    vector: list[int] = []
    trace: list[UltraReferenceEvaluation] = []
    rng_trace: list[tuple[int, int, str, int]] = []

    for candidate in range(169):
        occupied = state.room_map[candidate] >= 0
        blocked = state.blocked[candidate]
        excluded = candidate in forbidden
        if occupied or blocked or excluded:
            trace.append(
                UltraReferenceEvaluation(
                    candidate,
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
        before = state.rng.seed
        after = state.rng.next()
        score = after % 5 + 10
        base = score
        rng_trace.append((before, after, "candidate", base))
        cy, cx = divmod(candidate, 13)
        immediate = 0
        for direction in range(4):
            px = cx + CARDINAL[direction][0]
            py = cy + CARDINAL[direction][1]
            position = _index(px, py)
            if position >= 0 and (
                state.room_map[position] >= 0 or state.blocked[position]
            ):
                immediate |= 1 << direction
                score -= 100
                break

        neighbor_count = 0
        ring_mask = 0
        invalid: list[int] = []
        ring_position = 0
        while ring_position < 8 and score >= 0:
            ox, oy = RING[ring_position]
            position = _index(cx + ox, cy + oy)
            if position >= 0 and state.room_map[position] >= 0:
                ring_mask |= 1 << ring_position
                descriptor = state.rooms[state.room_map[position]]
                direction = 0
                while direction < 4:
                    if CARDINAL[direction][0] * ox + CARDINAL[direction][1] * oy > 0:
                        target = door_target_position(
                            descriptor.column,
                            descriptor.line,
                            descriptor.shape,
                            (direction - 2) & 3,
                        )
                        target_index = _index(*target)
                        if target_index < 0 or target_index in forbidden:
                            score -= 100
                            invalid.append(target_index)
                            break
                    direction += 1
                neighbor_count += 1
            ring_position += 1

        action = "discard"
        final = None
        if neighbor_count and score >= 0:
            final = score
            if neighbor_count < 3:
                final -= 3
            if neighbor_count < 2:
                final -= 3
            if final > maximum:
                maximum = final
                vector = [candidate]
                action = "replace-best"
            elif final == maximum:
                vector.append(candidate)
                action = "append-tie"
            else:
                action = "below-best"
        trace.append(
            UltraReferenceEvaluation(
                candidate,
                False,
                False,
                False,
                base,
                immediate,
                ring_mask,
                neighbor_count,
                tuple(invalid),
                final,
                action,
            )
        )

    room_id = -1
    selected = -1
    red_writes: list[tuple[int, int, int, int]] = []
    if vector:
        before = state.rng.seed
        after = state.rng.next()
        selected = vector[after % len(vector)]
        rng_trace.append((before, after, "selection", selected))
        room_id = len(state.rooms)
        state.rooms.append(
            GeneratedRoom(
                generation_index=room_id,
                column=selected % 13,
                line=selected // 13,
                shape=RoomShape.ROOMSHAPE_1x1,
                origin_direction=-1,
                link_column=-1,
                link_line=-1,
                distance_from_start=0,
            )
        )
        state.room_map[selected] = room_id
        room = state.rooms[room_id]
        room.doors = 0
        room.neighbors.clear()

        uy, ux = divmod(selected, 13)
        for ox, oy in RING:
            position = _index(ux + ox, uy + oy)
            if position < 0 or state.room_map[position] < 0:
                continue
            neighbor_id = state.room_map[position]
            neighbor = state.rooms[neighbor_id]
            for slot in range(8):
                tx, ty = door_target_position(
                    neighbor.column, neighbor.line, neighbor.shape, slot
                )
                target = _index(tx, ty)
                if target >= 0 and state.room_map[target] < 0:
                    if abs(tx - ux) + abs(ty - uy) == 1:
                        neighbor.doors |= 1 << slot
                        red_writes.append((neighbor_id, slot, target, selected))

    return UltraReferenceResult(
        room_id,
        selected,
        forbidden_values,
        tuple(vector),
        maximum,
        tuple(trace),
        tuple(rng_trace),
        state.rng.seed,
        tuple(red_writes),
        tuple(replace(room, neighbors=set(room.neighbors)) for room in state.rooms),
        tuple(state.room_map),
    )
