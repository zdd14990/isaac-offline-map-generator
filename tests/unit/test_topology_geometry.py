from __future__ import annotations

import pytest

from isaacmap.topology_geometry import (
    INVALID_POSITION,
    RoomShape,
    door_source_position,
    door_target_position,
    has_shape_slot,
    large_room_candidate_templates,
    occupied_cells,
)


def test_binary_room_shape_occupancy() -> None:
    assert occupied_cells(6, 6, RoomShape.ROOMSHAPE_1x1) == ((6, 6),)
    assert occupied_cells(3, 4, RoomShape.ROOMSHAPE_2x2) == (
        (3, 4),
        (4, 4),
        (3, 5),
        (4, 5),
    )
    assert occupied_cells(3, 4, RoomShape.ROOMSHAPE_LTL) == (
        (4, 4),
        (3, 5),
        (4, 5),
    )
    assert occupied_cells(3, 4, RoomShape.ROOMSHAPE_LBR) == (
        (3, 4),
        (4, 4),
        (3, 5),
    )


def test_thin_room_door_restrictions_match_binary() -> None:
    assert [slot for slot in range(8) if has_shape_slot(2, slot)] == [0, 2]
    assert [slot for slot in range(8) if has_shape_slot(3, slot)] == [1, 3]
    assert [slot for slot in range(8) if has_shape_slot(5, slot)] == [1, 3]
    assert [slot for slot in range(8) if has_shape_slot(7, slot)] == [0, 2]
    assert [slot for slot in range(8) if has_shape_slot(8, slot)] == list(range(8))


def test_one_by_one_door_targets() -> None:
    expected = ((5, 6), (6, 5), (7, 6), (6, 7))
    assert tuple(door_target_position(6, 6, 1, slot) for slot in range(4)) == expected
    assert door_target_position(6, 6, 1, 4) == INVALID_POSITION


def test_large_room_door_sources() -> None:
    assert door_source_position(4, 4, 8, 0) == (4, 4)
    assert door_source_position(4, 4, 8, 2) == (5, 4)
    assert door_source_position(4, 4, 8, 4) == (4, 5)
    assert door_source_position(4, 4, 8, 7) == (5, 5)


def test_l_shape_inner_target_tables() -> None:
    assert door_target_position(4, 4, 9, 0) == (4, 4)
    assert door_target_position(4, 4, 9, 1) == (4, 4)
    assert door_target_position(4, 4, 10, 2) == (5, 4)
    assert door_target_position(4, 4, 11, 3) == (4, 5)
    assert door_target_position(4, 4, 12, 6) == (5, 5)
    assert door_target_position(4, 4, 12, 7) == (5, 5)


def test_every_valid_door_target_is_adjacent_to_its_source() -> None:
    for shape in range(1, 13):
        cells = set(occupied_cells(4, 4, shape))
        for slot in range(8):
            if not has_shape_slot(shape, slot):
                continue
            source = door_source_position(4, 4, shape, slot)
            target = door_target_position(4, 4, shape, slot)
            assert abs(source[0] - target[0]) + abs(source[1] - target[1]) == 1
            assert source in cells
            assert target not in cells


def test_candidate_template_order_for_left_door() -> None:
    candidates = large_room_candidate_templates((5, 6), 0)
    assert len(candidates) == 13
    assert [candidate.divisor for candidate in candidates] == [
        48, 24, 24, 24, 24, 72, 72, 36, 36, 36, 36, 24, 24
    ]
    assert (candidates[0].anchor, candidates[0].shape) == (
        (4, 6), RoomShape.ROOMSHAPE_2x1
    )
    assert (candidates[1].anchor, candidates[1].shape) == (
        (5, 6), RoomShape.ROOMSHAPE_1x2
    )
    assert (candidates[2].anchor, candidates[2].shape) == (
        (5, 5), RoomShape.ROOMSHAPE_1x2
    )
    assert [candidate.shape for candidate in candidates[5:11]] == [
        RoomShape.ROOMSHAPE_LBR,
        RoomShape.ROOMSHAPE_LTR,
        RoomShape.ROOMSHAPE_LBL,
        RoomShape.ROOMSHAPE_LBL,
        RoomShape.ROOMSHAPE_LTL,
        RoomShape.ROOMSHAPE_LTL,
    ]


@pytest.mark.parametrize("bad", [0, 13])
def test_invalid_shape_is_rejected(bad: int) -> None:
    with pytest.raises(ValueError):
        occupied_cells(0, 0, bad)
