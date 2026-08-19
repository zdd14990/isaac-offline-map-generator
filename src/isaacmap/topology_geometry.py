"""Binary-derived 13x13 topology geometry for the profiled executable.

This module contains no approximate map generator.  It is the static geometry
layer used while reconstructing ``LevelGenerator`` and is deliberately not
exposed through a map CLI yet.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class RoomShape(IntEnum):
    NULL = 0
    ROOMSHAPE_1x1 = 1
    ROOMSHAPE_IH = 2
    ROOMSHAPE_IV = 3
    ROOMSHAPE_1x2 = 4
    ROOMSHAPE_IIV = 5
    ROOMSHAPE_2x1 = 6
    ROOMSHAPE_IIH = 7
    ROOMSHAPE_2x2 = 8
    ROOMSHAPE_LTL = 9
    ROOMSHAPE_LTR = 10
    ROOMSHAPE_LBL = 11
    ROOMSHAPE_LBR = 12


GRID_WIDTH = 13
GRID_HEIGHT = 13
INVALID_POSITION = (-1, -1)

# Width/height pairs at executable VA 0x00C5D378.
SHAPE_DIMENSIONS: tuple[tuple[int, int], ...] = (
    (0, 0),
    (1, 1),
    (1, 1),
    (1, 1),
    (1, 2),
    (1, 2),
    (2, 1),
    (2, 1),
    (2, 2),
    (2, 2),
    (2, 2),
    (2, 2),
    (2, 2),
)

# Occupancy lists returned by LevelGenerator::get_room_placement_offsets.
SHAPE_OFFSETS: tuple[tuple[tuple[int, int], ...], ...] = (
    (),
    ((0, 0),),
    ((0, 0),),
    ((0, 0),),
    ((0, 0), (0, 1)),
    ((0, 0), (0, 1)),
    ((0, 0), (1, 0)),
    ((0, 0), (1, 0)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
    ((1, 0), (0, 1), (1, 1)),
    ((0, 0), (0, 1), (1, 1)),
    ((0, 0), (1, 0), (1, 1)),
    ((0, 0), (1, 0), (0, 1)),
)

# Four direction deltas at executable VA 0x00C5D3E0.
DIRECTION_OFFSETS: tuple[tuple[int, int], ...] = (
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
)


def _shape_value(shape: int | RoomShape) -> int:
    value = int(shape)
    if not 1 <= value <= 12:
        raise ValueError("room shape must be in the range 1..12")
    return value


def _door_slot_value(door_slot: int) -> int:
    if isinstance(door_slot, bool) or not isinstance(door_slot, int):
        raise TypeError("door slot must be an integer")
    if not 0 <= door_slot <= 7:
        raise ValueError("door slot must be in the range 0..7")
    return door_slot


def occupied_cells(
    column: int, line: int, shape: int | RoomShape
) -> tuple[tuple[int, int], ...]:
    """Return the exact level-grid cells occupied by an anchored room."""

    value = _shape_value(shape)
    return tuple((column + dx, line + dy) for dx, dy in SHAPE_OFFSETS[value])


def has_shape_slot(
    shape: int | RoomShape, door_slot: int, *, ignore_thin_restrictions: bool = False
) -> bool:
    """Port RVA 0x005AF370 (``LevelGenerator::has_shape_slot``)."""

    value = _shape_value(shape)
    slot = _door_slot_value(door_slot)
    width, height = SHAPE_DIMENSIONS[value]
    if height == 1 and slot in (4, 6):
        return False
    if width == 1 and slot in (5, 7):
        return False
    if not ignore_thin_restrictions:
        if value in (RoomShape.ROOMSHAPE_IV, RoomShape.ROOMSHAPE_IIV):
            if slot in (0, 2, 4, 6):
                return False
        if value in (RoomShape.ROOMSHAPE_IH, RoomShape.ROOMSHAPE_IIH):
            if slot in (1, 3, 5, 7):
                return False
    return True


def door_source_position(
    column: int, line: int, shape: int | RoomShape, door_slot: int
) -> tuple[int, int]:
    """Port the valid-slot path of RVA 0x005AF3F0."""

    value = _shape_value(shape)
    slot = _door_slot_value(door_slot)
    if not has_shape_slot(value, slot):
        return INVALID_POSITION

    if value in (1, 2, 3):
        offset = (0, 0)
    elif value in (4, 5):
        offset = (0, 1) if slot in (3, 4, 6) else (0, 0)
    elif value in (6, 7):
        offset = (1, 0) if slot in (2, 5, 7) else (0, 0)
    elif value == 8:
        if slot in (2, 5):
            offset = (1, 0)
        elif slot in (3, 4):
            offset = (0, 1)
        elif slot in (6, 7):
            offset = (1, 1)
        else:
            offset = (0, 0)
    elif value == 9:
        if slot in (0, 2, 5):
            offset = (1, 0)
        elif slot in (1, 3, 4):
            offset = (0, 1)
        else:
            offset = (1, 1)
    elif value == 10:
        if slot in (0, 1, 2):
            offset = (0, 0)
        elif slot in (3, 4):
            offset = (0, 1)
        else:
            offset = (1, 1)
    elif value == 11:
        if slot in (0, 1, 3):
            offset = (0, 0)
        elif slot in (2, 5):
            offset = (1, 0)
        else:
            offset = (1, 1)
    else:  # ROOMSHAPE_LBR
        if slot in (0, 1):
            offset = (0, 0)
        elif slot in (2, 5, 7):
            offset = (1, 0)
        else:
            offset = (0, 1)
    return column + offset[0], line + offset[1]


def door_target_position(
    column: int,
    line: int,
    shape: int | RoomShape,
    door_slot: int,
    *,
    ignore_thin_restrictions: bool = False,
) -> tuple[int, int]:
    """Port RVA 0x005AF620, including the four L-shape tables."""

    value = _shape_value(shape)
    slot = _door_slot_value(door_slot)
    if not has_shape_slot(
        value, slot, ignore_thin_restrictions=ignore_thin_restrictions
    ):
        return INVALID_POSITION

    width, height = SHAPE_DIMENSIONS[value]
    default = (
        (column - 1, line),
        (column, line - 1),
        (column + width, line),
        (column, line + height),
        (column - 1, line + 1),
        (column + 1, line - 1),
        (column + width, line + 1),
        (column + 1, line + height),
    )
    if value == RoomShape.ROOMSHAPE_LTL:
        table = (
            (column, line),
            (column, line),
            (column + 2, line),
            (column, line + 2),
            (column - 1, line + 1),
            (column + 1, line - 1),
            (column + 2, line + 1),
            (column + 1, line + 2),
        )
    elif value == RoomShape.ROOMSHAPE_LTR:
        table = (
            (column - 1, line),
            (column, line - 1),
            (column + 1, line),
            (column, line + 2),
            (column - 1, line + 1),
            (column + 1, line),
            (column + 2, line + 1),
            (column + 1, line + 2),
        )
    elif value == RoomShape.ROOMSHAPE_LBL:
        table = (
            (column - 1, line),
            (column, line - 1),
            (column + 2, line),
            (column, line + 1),
            (column, line + 1),
            (column + 1, line - 1),
            (column + 2, line + 1),
            (column + 1, line + 2),
        )
    elif value == RoomShape.ROOMSHAPE_LBR:
        table = (
            (column - 1, line),
            (column, line - 1),
            (column + 2, line),
            (column, line + 2),
            (column - 1, line + 1),
            (column + 1, line - 1),
            (column + 1, line + 1),
            (column + 1, line + 1),
        )
    else:
        table = default
    return table[slot]


@dataclass(frozen=True)
class LargeRoomCandidateTemplate:
    anchor: tuple[int, int]
    shape: RoomShape
    divisor: int


_CANDIDATE_DIVISORS = (48, 24, 24, 24, 24, 72, 72, 36, 36, 36, 36, 24, 24)


def large_room_candidate_templates(
    target: tuple[int, int], direction: int
) -> tuple[LargeRoomCandidateTemplate, ...]:
    """Return the 13 ordered candidates built at RVA 0x005B0B00.

    ``direction`` is ``door_slot & 3``.  This helper only constructs the
    fixed anchor/shape/divisor table; the caller must still consume one RNG
    draw per entry and apply allowed-shape and collision filters in binary
    order.
    """

    if isinstance(direction, bool) or not isinstance(direction, int):
        raise TypeError("direction must be an integer")
    if not 0 <= direction <= 3:
        raise ValueError("direction must be in the range 0..3")

    tx, ty = target
    if direction in (0, 1):
        dx, dy = DIRECTION_OFFSETS[direction]
    else:
        dx, dy = (0, 0)
    base = (tx + dx, ty + dy)
    if direction in (0, 2):
        alternate = (base[0], base[1] - 1)
        third = (tx, ty - 1)
        first_shapes = (RoomShape.ROOMSHAPE_2x1, RoomShape.ROOMSHAPE_1x2)
        narrow = (RoomShape.ROOMSHAPE_IH, RoomShape.ROOMSHAPE_IIH)
    else:
        alternate = (base[0] - 1, base[1])
        third = (tx - 1, ty)
        first_shapes = (RoomShape.ROOMSHAPE_1x2, RoomShape.ROOMSHAPE_2x1)
        narrow = (RoomShape.ROOMSHAPE_IV, RoomShape.ROOMSHAPE_IIV)

    l_shapes = (
        (RoomShape.ROOMSHAPE_LBR, RoomShape.ROOMSHAPE_LTR, RoomShape.ROOMSHAPE_LBL, RoomShape.ROOMSHAPE_LTL),
        (RoomShape.ROOMSHAPE_LBR, RoomShape.ROOMSHAPE_LBL, RoomShape.ROOMSHAPE_LTR, RoomShape.ROOMSHAPE_LTL),
        (RoomShape.ROOMSHAPE_LBL, RoomShape.ROOMSHAPE_LTL, RoomShape.ROOMSHAPE_LTR, RoomShape.ROOMSHAPE_LBR),
        (RoomShape.ROOMSHAPE_LTR, RoomShape.ROOMSHAPE_LTL, RoomShape.ROOMSHAPE_LBL, RoomShape.ROOMSHAPE_LBR),
    )[direction]

    anchors = (
        base,
        target,
        third,
        base,
        alternate,
        base,
        alternate,
        base,
        alternate,
        base,
        alternate,
        target,
        base,
    )
    shapes = (
        first_shapes[0],
        first_shapes[1],
        first_shapes[1],
        RoomShape.ROOMSHAPE_2x2,
        RoomShape.ROOMSHAPE_2x2,
        l_shapes[0],
        l_shapes[1],
        l_shapes[2],
        l_shapes[2],
        l_shapes[3],
        l_shapes[3],
        narrow[0],
        narrow[1],
    )
    return tuple(
        LargeRoomCandidateTemplate(anchor, shape, divisor)
        for anchor, shape, divisor in zip(anchors, shapes, _CANDIDATE_DIVISORS)
    )
