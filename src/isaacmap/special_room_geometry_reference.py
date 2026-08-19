"""Mechanical counterpart of the end-room geometry matcher."""

from __future__ import annotations

from .special_room_geometry import EndRoomGeometryCandidate, EndRoomGeometryEvent


_OFFSETS = (
    (), ((0, 0),), ((0, 0),), ((0, 0),),
    ((0, 0), (0, 1)), ((0, 0), (0, 1)),
    ((0, 0), (1, 0)), ((0, 0), (1, 0)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
    ((1, 0), (0, 1), (1, 1)),
    ((0, 0), (0, 1), (1, 1)),
    ((0, 0), (1, 0), (1, 1)),
    ((0, 0), (1, 0), (0, 1)),
)
_DIMS = ((0, 0), (1, 1), (1, 1), (1, 1), (1, 2), (1, 2), (2, 1), (2, 1), (2, 2), (2, 2), (2, 2), (2, 2), (2, 2))
_DIR = ((-1, 0), (0, -1), (1, 0), (0, 1))


def _templates(room: object) -> tuple[EndRoomGeometryCandidate, ...]:
    direction = int(room.origin_direction)
    tx, ty = int(room.link_column), int(room.link_line)
    opposite = (direction + 2) & 3
    if direction in (0, 1):
        base = (tx + _DIR[direction][0], ty + _DIR[direction][1])
    else:
        base = (tx, ty)
    if direction in (0, 2):
        alternate, third = (base[0], base[1] - 1), (tx, ty - 1)
        first, second, narrow = 6, 4, (2, 7)
    else:
        alternate, third = (base[0] - 1, base[1]), (tx - 1, ty)
        first, second, narrow = 4, 6, (3, 5)
    l = (
        (12, 10, 11, 9), (12, 11, 10, 9),
        (11, 9, 10, 12), (10, 9, 11, 12),
    )[direction]
    anchors = ((tx, ty), base, (tx, ty), third, base, alternate, base, alternate, base, alternate, base, alternate, (tx, ty), base)
    shapes = (1, first, second, second, 8, 8, l[0], l[1], l[2], l[2], l[3], l[3], narrow[0], narrow[1])
    slots = (opposite, opposite, opposite + 4, opposite, opposite + 4, opposite, opposite + 4, opposite, opposite + 4, opposite, opposite + 4, opposite, opposite, opposite)
    return tuple(EndRoomGeometryCandidate(i, anchor, shape, slot) for i, (anchor, shape, slot) in enumerate(zip(anchors, shapes, slots)))


def _idx(x: int, y: int) -> int:
    return y * 13 + x if 0 <= x < 13 and 0 <= y < 13 else -1


def _has_slot(shape: int, slot: int) -> bool:
    width, height = _DIMS[shape]
    if height == 1 and slot in (4, 6): return False
    if width == 1 and slot in (5, 7): return False
    if shape in (3, 5) and slot in (0, 2, 4, 6): return False
    if shape in (2, 7) and slot in (1, 3, 5, 7): return False
    return True


def _target(x: int, y: int, shape: int, slot: int) -> tuple[int, int]:
    if not _has_slot(shape, slot): return (-1, -1)
    w, h = _DIMS[shape]
    table = ((x-1,y),(x,y-1),(x+w,y),(x,y+h),(x-1,y+1),(x+1,y-1),(x+w,y+1),(x+1,y+h))
    if shape == 9: table=((x,y),(x,y),(x+2,y),(x,y+2),(x-1,y+1),(x+1,y-1),(x+2,y+1),(x+1,y+2))
    elif shape == 10: table=((x-1,y),(x,y-1),(x+1,y),(x,y+2),(x-1,y+1),(x+1,y),(x+2,y+1),(x+1,y+2))
    elif shape == 11: table=((x-1,y),(x,y-1),(x+2,y),(x,y+1),(x,y+1),(x+1,y-1),(x+2,y+1),(x+1,y+2))
    elif shape == 12: table=((x-1,y),(x,y-1),(x+2,y),(x,y+2),(x-1,y+1),(x+1,y-1),(x+1,y+1),(x+1,y+1))
    return table[slot]


def _rebuild(state: object) -> None:
    for room in state.rooms:
        room.doors = 0; room.neighbors.clear()
        for slot in range(8):
            x,y=_target(room.column,room.line,int(room.shape),slot); index=_idx(x,y)
            if index >= 0:
                other=state.room_map[index]
                if other >= 0 and other != room.generation_index:
                    room.doors |= 1 << slot; room.neighbors.add(other)


def reshape_end_room_reference(state: object, room_id: int, config_shape: int, required_doors: int, *, events: list[EndRoomGeometryEvent] | None = None) -> bool:
    room=state.rooms[room_id]
    for candidate in _templates(room):
        reason="shape"; external=0
        if candidate.shape != config_shape:
            if events is not None: events.append(EndRoomGeometryEvent(room_id,candidate,False,reason,external))
            continue
        if required_doors & (1 << candidate.connection_slot) == 0:
            if events is not None: events.append(EndRoomGeometryEvent(room_id,candidate,False,"parent-door-mask",external))
            continue
        valid=True
        for dx,dy in _OFFSETS[candidate.shape]:
            index=_idx(candidate.anchor[0]+dx,candidate.anchor[1]+dy)
            if index < 0 or state.room_map[index] not in (-1,room_id): valid=False; break
        if not valid:
            if events is not None: events.append(EndRoomGeometryEvent(room_id,candidate,False,"occupied-or-boundary",external))
            continue
        for slot in range(8):
            x,y=_target(candidate.anchor[0],candidate.anchor[1],candidate.shape,slot); index=_idx(x,y)
            if index < 0: continue
            other=state.room_map[index]
            if other < 0 or other == room_id: continue
            if not getattr(state.rooms[other],"connection_count_exempt",False): external += 1
            if required_doors & (1 << slot) == 0: valid=False; reason="neighbor-door-mask"; break
        if valid and external >= 2: valid=False; reason="two-or-more-external-neighbors"
        if not valid:
            if events is not None: events.append(EndRoomGeometryEvent(room_id,candidate,False,reason,external))
            continue
        for dx,dy in _OFFSETS[int(room.shape)]:
            index=_idx(room.column+dx,room.line+dy)
            if index >= 0 and state.room_map[index] == room_id: state.room_map[index]=-1
        room.column,room.line=candidate.anchor; room.shape=candidate.shape
        for dx,dy in _OFFSETS[candidate.shape]: state.room_map[_idx(room.column+dx,room.line+dy)]=room_id
        _rebuild(state)
        if events is not None: events.append(EndRoomGeometryEvent(room_id,candidate,True,"accepted",external))
        return True
    return False
