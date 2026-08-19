from __future__ import annotations

import pytest
from PIL import Image

from isaacmap.topology_geometry import GRID_HEIGHT, GRID_WIDTH, RoomShape
from isaacmap.ui.minimap_assets import ROOM_TYPE_ICON_ANIMATIONS
from isaacmap.ui.models import (
    ROOM_TYPE_ICON_KEYS,
    ROOM_TYPE_NAMES,
    PreviewMapModel,
    RenderRoom,
    legend_labels,
)
from isaacmap.ui.renderer import (
    FALLBACK_MARKS,
    compute_layout,
    connection_segments,
    hit_test_room,
    icon_paste_position,
    icon_render_size,
    render_map,
    room_render_center,
    room_render_mask,
    room_icon_key,
)


def _room(
    generation_index: int,
    column: int,
    row: int,
    shape: RoomShape,
    *,
    room_type: int = 1,
    doors: int = 0,
) -> RenderRoom:
    return RenderRoom(
        generation_index=generation_index,
        column=column,
        line=row,
        shape=shape,
        room_type=room_type,
        doors=doors,
    )


def _model(*rooms: RenderRoom) -> PreviewMapModel:
    room_map = [-1] * (GRID_WIDTH * GRID_HEIGHT)
    for room in rooms:
        for column, row in room.cells:
            room_map[row * GRID_WIDTH + column] = room.generation_index
    return PreviewMapModel(tuple(rooms), tuple(room_map))


def test_1x1_room_uses_one_real_grid_cell() -> None:
    assert _room(0, 6, 6, RoomShape.ROOMSHAPE_1x1).cells == ((6, 6),)


@pytest.mark.parametrize("shape", [RoomShape.ROOMSHAPE_2x1, RoomShape.ROOMSHAPE_IIH])
def test_horizontal_large_room_uses_existing_shape_helper(shape: RoomShape) -> None:
    assert _room(0, 5, 6, shape).cells == ((5, 6), (6, 6))


@pytest.mark.parametrize("shape", [RoomShape.ROOMSHAPE_1x2, RoomShape.ROOMSHAPE_IIV])
def test_vertical_large_room_uses_existing_shape_helper(shape: RoomShape) -> None:
    assert _room(0, 6, 5, shape).cells == ((6, 5), (6, 6))


def test_2x2_room_occupies_all_four_cells() -> None:
    assert set(_room(0, 5, 5, RoomShape.ROOMSHAPE_2x2).cells) == {
        (5, 5),
        (6, 5),
        (5, 6),
        (6, 6),
    }


@pytest.mark.parametrize(
    ("shape", "missing"),
    [
        (RoomShape.ROOMSHAPE_LTL, (5, 5)),
        (RoomShape.ROOMSHAPE_LTR, (6, 5)),
        (RoomShape.ROOMSHAPE_LBL, (5, 6)),
        (RoomShape.ROOMSHAPE_LBR, (6, 6)),
    ],
)
def test_all_four_l_shapes_preserve_the_missing_cell(
    shape: RoomShape, missing: tuple[int, int]
) -> None:
    cells = set(_room(0, 5, 5, shape).cells)
    assert len(cells) == 3
    assert missing not in cells
    assert cells | {missing} == {(5, 5), (6, 5), (5, 6), (6, 6)}


def test_connections_read_door_slots_instead_of_guessing_adjacent_cells() -> None:
    left = _room(0, 6, 6, RoomShape.ROOMSHAPE_1x1, doors=1 << 2)
    right = _room(1, 7, 6, RoomShape.ROOMSHAPE_1x1, doors=1 << 0)
    segments = connection_segments(_model(left, right))
    assert len(segments) == 1
    assert segments[0].source_cell == (6, 6)
    assert segments[0].target_cell == (7, 6)

    # Adjacency alone is deliberately insufficient.
    assert connection_segments(_model(
        _room(0, 6, 6, RoomShape.ROOMSHAPE_1x1),
        _room(1, 7, 6, RoomShape.ROOMSHAPE_1x1),
    )) == ()


def test_occupied_bounding_box_is_centered_in_canvas() -> None:
    rooms = (
        _room(0, 4, 5, RoomShape.ROOMSHAPE_1x1),
        _room(1, 7, 7, RoomShape.ROOMSHAPE_2x1),
    )
    layout = compute_layout(rooms, 900, 500)
    left_margin = layout.origin_x
    right_margin = layout.canvas_width - (layout.origin_x + layout.pixel_width)
    top_margin = layout.origin_y
    bottom_margin = layout.canvas_height - (layout.origin_y + layout.pixel_height)
    assert abs(left_margin - right_margin) <= 1
    assert abs(top_margin - bottom_margin) <= 1
    assert (layout.min_column, layout.max_column, layout.min_row, layout.max_row) == (
        4,
        8,
        5,
        7,
    )


@pytest.mark.parametrize(
    ("room", "expected"),
    [
        (_room(0, 6, 6, RoomShape.ROOMSHAPE_1x1), "start"),
        (_room(1, 6, 6, RoomShape.ROOMSHAPE_1x1, room_type=1), None),
        (_room(1, 6, 6, RoomShape.ROOMSHAPE_1x1, room_type=2), "shop"),
        (_room(1, 6, 6, RoomShape.ROOMSHAPE_1x1, room_type=4), "treasure"),
        (_room(1, 6, 6, RoomShape.ROOMSHAPE_1x1, room_type=5), "boss"),
        (_room(1, 6, 6, RoomShape.ROOMSHAPE_1x1, room_type=7), "secret"),
        (_room(1, 6, 6, RoomShape.ROOMSHAPE_1x1, room_type=8), "super_secret"),
    ],
)
def test_room_type_icon_mapping(room: RenderRoom, expected: str | None) -> None:
    assert room_icon_key(room) == expected


def test_every_known_special_room_type_has_icon_or_text_mapping() -> None:
    for room_type in ROOM_TYPE_NAMES:
        if room_type in (0, 1):
            continue
        room = _room(1, 6, 6, RoomShape.ROOMSHAPE_1x1, room_type=room_type)
        key = room_icon_key(room)
        assert key == ROOM_TYPE_ICON_KEYS[room_type]
        assert key in FALLBACK_MARKS


def test_all_m6_assignable_special_types_use_official_minimap_animations() -> None:
    # Canonical M6 may actually assign these types to accepted descriptors.
    m6_types = {2, 4, 5, 6, 7, 8, 10, 12, 13, 18, 21, 24}
    assert m6_types <= set(ROOM_TYPE_ICON_ANIMATIONS)


def test_legend_uses_only_special_types_present_in_current_map() -> None:
    model = _model(
        _room(0, 6, 6, RoomShape.ROOMSHAPE_1x1),
        _room(1, 7, 6, RoomShape.ROOMSHAPE_1x1, room_type=5),
        _room(2, 8, 6, RoomShape.ROOMSHAPE_1x1, room_type=10),
        _room(3, 9, 6, RoomShape.ROOMSHAPE_1x1, room_type=5),
    )
    assert legend_labels(model) == ("Start", "Normal", "Boss", "Curse")


@pytest.mark.parametrize("shape", list(RoomShape)[1:])
def test_icon_center_uses_complete_rendered_geometry(shape: RoomShape) -> None:
    room = _room(1, 5, 5, shape, room_type=5)
    model = _model(room)
    layout = compute_layout(model.rooms, 600, 500)
    center = room_render_center(room, layout)

    # The center must land in the rendered union, including bridges between
    # occupied cells and all four genuinely non-rectangular L variants.
    mask = room_render_mask(room, layout)
    assert mask.getpixel((round(center[0]), round(center[1]))) > 0

    cells = tuple(layout.cell_rect(*cell).center for cell in room.cells)
    equal_area_center = (
        sum(x for x, _ in cells) / len(cells),
        sum(y for _, y in cells) / len(cells),
    )
    assert center[0] == pytest.approx(equal_area_center[0], abs=layout.gap / 2 + 1)
    assert center[1] == pytest.approx(equal_area_center[1], abs=layout.gap / 2 + 1)

    if len(room.cells) > 1:
        anchor_center = layout.cell_rect(room.column, room.line).center
        assert center != anchor_center


def test_visible_sprite_alpha_is_centered_instead_of_transparent_frame() -> None:
    icon = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    icon.putpixel((3, 2), (255, 255, 255, 255))
    assert icon_paste_position(icon, (100, 80)) == (97, 78)


def test_icon_size_depends_on_zoom_not_room_shape() -> None:
    one = _room(1, 4, 4, RoomShape.ROOMSHAPE_1x1, room_type=5)
    large = _room(2, 6, 4, RoomShape.ROOMSHAPE_2x2, room_type=5)
    one_layout = compute_layout((one,), 700, 500)
    large_layout = compute_layout((large,), 700, 500)
    assert icon_render_size(one_layout) == icon_render_size(large_layout)


@pytest.mark.parametrize("shape", list(RoomShape)[1:])
def test_renderer_draws_every_room_shape_and_hit_tests_real_cells(shape: RoomShape) -> None:
    room = _room(0, 5, 5, shape)
    model = _model(room)
    image, layout = render_map(model, 500, 400)
    assert image.size == (500, 400)
    for cell in room.cells:
        center = layout.cell_rect(*cell).center
        assert hit_test_room(model, layout, *center) == room
