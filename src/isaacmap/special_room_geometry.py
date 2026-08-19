"""Post-topology end-room reshape matcher for the frozen executable."""

from __future__ import annotations

from dataclasses import dataclass

from .topology_geometry import (
    GRID_HEIGHT,
    GRID_WIDTH,
    RoomShape,
    door_target_position,
    large_room_candidate_templates,
    occupied_cells,
)


ROOM_MATCHES_MASK_RVA = 0x005B1220


@dataclass(frozen=True)
class EndRoomGeometryCandidate:
    candidate_index: int
    anchor: tuple[int, int]
    shape: int
    connection_slot: int


@dataclass(frozen=True)
class EndRoomGeometryEvent:
    room_id: int
    candidate: EndRoomGeometryCandidate
    accepted: bool
    reason: str
    external_neighbor_count: int


def end_room_geometry_candidates(room: object) -> tuple[EndRoomGeometryCandidate, ...]:
    direction = int(room.origin_direction)
    opposite = (direction + 2) & 3
    # RVA 0x005B1220 builds one 1x1 candidate followed by the same thirteen
    # anchor/shape templates used by the topology large-room builder.
    values = [EndRoomGeometryCandidate(0, (int(room.link_column), int(room.link_line)), 1, opposite)]
    slots = (
        opposite, opposite + 4, opposite, opposite + 4,
        opposite, opposite + 4, opposite, opposite + 4,
        opposite, opposite + 4, opposite, opposite, opposite,
    )
    for index, (template, slot) in enumerate(
        zip(large_room_candidate_templates(values[0].anchor, direction), slots), start=1
    ):
        values.append(EndRoomGeometryCandidate(index, template.anchor, int(template.shape), slot))
    return tuple(values)


def _grid_index(column: int, line: int) -> int:
    return line * GRID_WIDTH + column if 0 <= column < GRID_WIDTH and 0 <= line < GRID_HEIGHT else -1


def _rebuild_connections(state: object) -> None:
    for room in state.rooms:
        room.doors = 0
        room.neighbors.clear()
        for slot in range(8):
            column, line = door_target_position(room.column, room.line, room.shape, slot)
            index = _grid_index(column, line)
            if index < 0:
                continue
            neighbor = state.room_map[index]
            if neighbor >= 0 and neighbor != room.generation_index:
                room.doors |= 1 << slot
                room.neighbors.add(neighbor)


def reshape_end_room(
    state: object,
    room_id: int,
    config_shape: int,
    required_doors: int,
    *,
    events: list[EndRoomGeometryEvent] | None = None,
) -> bool:
    """Port ``LevelGenerator::room_matches_mask`` for generated end rooms."""

    room = state.rooms[room_id]
    for candidate in end_room_geometry_candidates(room):
        if candidate.shape != config_shape:
            if events is not None:
                events.append(EndRoomGeometryEvent(room_id, candidate, False, "shape", 0))
            continue
        if required_doors & (1 << candidate.connection_slot) == 0:
            if events is not None:
                events.append(EndRoomGeometryEvent(room_id, candidate, False, "parent-door-mask", 0))
            continue

        valid = True
        for column, line in occupied_cells(candidate.anchor[0], candidate.anchor[1], candidate.shape):
            index = _grid_index(column, line)
            if index < 0 or state.room_map[index] not in (-1, room_id):
                valid = False
                break
        if not valid:
            if events is not None:
                events.append(EndRoomGeometryEvent(room_id, candidate, False, "occupied-or-boundary", 0))
            continue

        external = 0
        reason = "accepted"
        for slot in range(8):
            column, line = door_target_position(candidate.anchor[0], candidate.anchor[1], candidate.shape, slot)
            index = _grid_index(column, line)
            if index < 0:
                continue
            neighbor_id = state.room_map[index]
            if neighbor_id < 0 or neighbor_id == room_id:
                continue
            neighbor = state.rooms[neighbor_id]
            if not getattr(neighbor, "connection_count_exempt", False):
                external += 1
            if required_doors & (1 << slot) == 0:
                valid = False
                reason = "neighbor-door-mask"
                break
        if valid and external >= 2:
            valid = False
            reason = "two-or-more-external-neighbors"
        if not valid:
            if events is not None:
                events.append(EndRoomGeometryEvent(room_id, candidate, False, reason, external))
            continue

        for column, line in tuple(room.cells):
            index = _grid_index(column, line)
            if index >= 0 and state.room_map[index] == room_id:
                state.room_map[index] = -1
        room.column, room.line = candidate.anchor
        room.shape = RoomShape(candidate.shape)
        for column, line in occupied_cells(room.column, room.line, room.shape):
            state.room_map[_grid_index(column, line)] = room_id
        _rebuild_connections(state)
        if events is not None:
            events.append(EndRoomGeometryEvent(room_id, candidate, True, "accepted", external))
        return True
    return False
