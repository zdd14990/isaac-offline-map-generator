"""Pillow-based, Tk-independent Isaac minimap preview renderer."""

from __future__ import annotations

from dataclasses import dataclass
from math import floor
from typing import Mapping

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from isaacmap.topology_geometry import (
    GRID_HEIGHT,
    GRID_WIDTH,
    door_source_position,
    door_target_position,
)

from .models import PreviewMapModel, ROOM_TYPE_ICON_KEYS, RenderRoom


BACKGROUND = "#151311"
GRID_DOT = "#2a2723"
OUTLINE = "#0a0908"
CONNECTION_OUTLINE = "#0a0908"
CONNECTION_FILL = "#8b8174"
ROOM_COLORS = {
    1: "#82796d",
    2: "#9b7a36",
    3: "#6c6863",
    4: "#a59240",
    5: "#8e3f3d",
    6: "#9a514c",
    7: "#77716b",
    8: "#59677a",
    9: "#8b6a92",
    10: "#8f4545",
    11: "#9a5441",
    12: "#6b7d58",
    13: "#865d55",
    14: "#714243",
    15: "#b1a77f",
    17: "#9a514c",
    18: "#75628f",
    19: "#796b55",
    20: "#7e6648",
    21: "#66827d",
    24: "#4f668d",
    25: "#627f89",
    26: "#627f89",
    29: "#a06278",
}
ICON_BY_ROOM_TYPE = dict(ROOM_TYPE_ICON_KEYS)
FALLBACK_MARKS = {
    "start": "S",
    "shop": "$",
    "error": "ERR",
    "treasure": "T",
    "boss": "B",
    "miniboss": "MB",
    "secret": "?",
    "super_secret": "SS",
    "arcade": "A",
    "curse": "C",
    "challenge": "!",
    "library": "L",
    "sacrifice": "SA",
    "devil": "DV",
    "angel": "AN",
    "dungeon": "DNG",
    "boss_rush": "BR",
    "isaacs": "I",
    "barren": "BA",
    "chest": "CH",
    "dice": "D6",
    "black_market": "BM",
    "greed_exit": "GE",
    "planetarium": "P",
    "teleporter": "TP",
    "teleporter_exit": "TX",
    "secret_exit": "SE",
    "blue": "BL",
    "ultra_secret": "US",
    "deathmatch": "DM",
}


@dataclass(frozen=True)
class PixelRect:
    left: int
    top: int
    right: int
    bottom: int

    @property
    def center(self) -> tuple[float, float]:
        return ((self.left + self.right) / 2, (self.top + self.bottom) / 2)

    def contains(self, x: float, y: float) -> bool:
        return self.left <= x <= self.right and self.top <= y <= self.bottom


@dataclass(frozen=True)
class MapLayout:
    canvas_width: int
    canvas_height: int
    min_column: int
    max_column: int
    min_row: int
    max_row: int
    room_size: int
    gap: int
    origin_x: int
    origin_y: int

    @property
    def pitch(self) -> int:
        return self.room_size + self.gap

    @property
    def pixel_width(self) -> int:
        columns = self.max_column - self.min_column + 1
        return columns * self.room_size + (columns - 1) * self.gap

    @property
    def pixel_height(self) -> int:
        rows = self.max_row - self.min_row + 1
        return rows * self.room_size + (rows - 1) * self.gap

    def cell_rect(self, column: int, row: int) -> PixelRect:
        left = self.origin_x + (column - self.min_column) * self.pitch
        top = self.origin_y + (row - self.min_row) * self.pitch
        return PixelRect(left, top, left + self.room_size, top + self.room_size)


@dataclass(frozen=True)
class GridConnection:
    source_room: int
    target_room: int
    source_slot: int
    source_cell: tuple[int, int]
    target_cell: tuple[int, int]


def occupied_bounds(rooms: tuple[RenderRoom, ...]) -> tuple[int, int, int, int]:
    cells = tuple(cell for room in rooms for cell in room.cells)
    if not cells:
        raise ValueError("cannot lay out an empty map")
    columns = tuple(column for column, _ in cells)
    rows = tuple(row for _, row in cells)
    return min(columns), max(columns), min(rows), max(rows)


def compute_layout(
    rooms: tuple[RenderRoom, ...],
    canvas_width: int,
    canvas_height: int,
    *,
    padding: int = 34,
    maximum_room_size: int = 58,
) -> MapLayout:
    """Fit and center the occupied bounding box, not the empty 13x13 grid."""

    min_column, max_column, min_row, max_row = occupied_bounds(rooms)
    columns = max_column - min_column + 1
    rows = max_row - min_row + 1
    available_width = max(1, canvas_width - 2 * padding)
    available_height = max(1, canvas_height - 2 * padding)
    pitch = max(8, floor(min(available_width / columns, available_height / rows)))
    gap = max(4, min(10, floor(pitch * 0.16)))
    room_size = max(4, min(maximum_room_size, pitch - gap))
    pixel_width = columns * room_size + (columns - 1) * gap
    pixel_height = rows * room_size + (rows - 1) * gap
    return MapLayout(
        canvas_width=canvas_width,
        canvas_height=canvas_height,
        min_column=min_column,
        max_column=max_column,
        min_row=min_row,
        max_row=max_row,
        room_size=room_size,
        gap=gap,
        origin_x=(canvas_width - pixel_width) // 2,
        origin_y=(canvas_height - pixel_height) // 2,
    )


def room_icon_key(room: RenderRoom) -> str | None:
    if room.generation_index == 0:
        return "start"
    return ICON_BY_ROOM_TYPE.get(room.room_type)


def connection_segments(model: PreviewMapModel) -> tuple[GridConnection, ...]:
    """Read connection bits/DoorSlots; never infer links from adjacency alone."""

    found: list[GridConnection] = []
    seen: set[tuple[object, ...]] = set()
    for room in model.rooms:
        for slot in range(8):
            if room.doors & (1 << slot) == 0:
                continue
            source = door_source_position(room.column, room.line, room.shape, slot)
            target = door_target_position(room.column, room.line, room.shape, slot)
            column, row = target
            if not (0 <= column < GRID_WIDTH and 0 <= row < GRID_HEIGHT):
                continue
            target_room = model.room_map[row * GRID_WIDTH + column]
            if target_room < 0 or target_room == room.generation_index:
                continue
            endpoints = tuple(sorted((source, target)))
            key = (
                min(room.generation_index, target_room),
                max(room.generation_index, target_room),
                endpoints,
            )
            if key in seen:
                continue
            seen.add(key)
            found.append(
                GridConnection(
                    room.generation_index, target_room, slot, source, target
                )
            )
    return tuple(found)


def _draw_connection(
    draw: ImageDraw.ImageDraw, layout: MapLayout, connection: GridConnection
) -> None:
    source = layout.cell_rect(*connection.source_cell).center
    target = layout.cell_rect(*connection.target_cell).center
    outer = max(5, layout.room_size // 7)
    inner = max(2, outer - 4)
    draw.line((source, target), fill=CONNECTION_OUTLINE, width=outer)
    draw.line((source, target), fill=CONNECTION_FILL, width=inner)


def room_render_mask(room: RenderRoom, layout: MapLayout) -> Image.Image:
    mask = Image.new("L", (layout.canvas_width, layout.canvas_height), 0)
    draw = ImageDraw.Draw(mask)
    cells = set(room.cells)
    for column, row in cells:
        rect = layout.cell_rect(column, row)
        draw.rectangle((rect.left, rect.top, rect.right, rect.bottom), fill=255)
        if (column + 1, row) in cells:
            neighbor = layout.cell_rect(column + 1, row)
            draw.rectangle((rect.right, rect.top, neighbor.left, rect.bottom), fill=255)
        if (column, row + 1) in cells:
            neighbor = layout.cell_rect(column, row + 1)
            draw.rectangle((rect.left, rect.bottom, rect.right, neighbor.top), fill=255)

    # Fill the center junction for 2x2 and three-cell L polyominoes while
    # preserving the L shape's genuinely missing occupied cell.
    for column in range(min(c[0] for c in cells), max(c[0] for c in cells)):
        for row in range(min(c[1] for c in cells), max(c[1] for c in cells)):
            block = {
                (column, row),
                (column + 1, row),
                (column, row + 1),
                (column + 1, row + 1),
            }
            if len(block & cells) >= 3:
                top_left = layout.cell_rect(column, row)
                bottom_right = layout.cell_rect(column + 1, row + 1)
                draw.rectangle(
                    (top_left.right, top_left.bottom, bottom_right.left, bottom_right.top),
                    fill=255,
                )
    return mask


def _mask_centroid(mask: Image.Image) -> tuple[float, float]:
    """Return the alpha-weighted center of an actual rendered geometry mask."""

    bounds = mask.getbbox()
    if bounds is None:
        raise ValueError("cannot calculate the center of an empty mask")
    cropped = mask.crop(bounds).convert("L")
    width, height = cropped.size
    pixels = tuple(cropped.tobytes())
    total = sum(pixels)
    if total == 0:
        raise ValueError("cannot calculate the center of a transparent mask")
    x_moment = sum((index % width) * value for index, value in enumerate(pixels))
    y_moment = sum((index // width) * value for index, value in enumerate(pixels))
    return (
        bounds[0] + x_moment / total,
        bounds[1] + y_moment / total,
    )


def room_render_center(room: RenderRoom, layout: MapLayout) -> tuple[float, float]:
    """Center icons on the union geometry of all occupied RoomShape cells."""

    return _mask_centroid(room_render_mask(room, layout))


def icon_render_size(layout: MapLayout) -> int:
    """Scale with map zoom only; large RoomShapes never enlarge the icon."""

    return max(16, min(28, layout.room_size * 3 // 5))


def icon_paste_position(
    icon: Image.Image, center: tuple[float, float]
) -> tuple[int, int]:
    """Align visible sprite pixels, not the asymmetric transparent 16x16 frame."""

    alpha = icon.convert("RGBA").getchannel("A")
    try:
        visible_center = _mask_centroid(alpha)
    except ValueError:
        visible_center = ((icon.width - 1) / 2, (icon.height - 1) / 2)
    return (
        round(center[0] - visible_center[0]),
        round(center[1] - visible_center[1]),
    )


def _draw_icon_or_mark(
    image: Image.Image,
    draw: ImageDraw.ImageDraw,
    room: RenderRoom,
    layout: MapLayout,
    icons: Mapping[str, Image.Image],
) -> None:
    key = room_icon_key(room)
    if key is None:
        return
    center = room_render_center(room, layout)
    icon = icons.get(key)
    if icon is not None:
        size = icon_render_size(layout)
        resized = icon.convert("RGBA").resize((size, size), Image.Resampling.NEAREST)
        image.alpha_composite(resized, icon_paste_position(resized, center))
        return

    mark = FALLBACK_MARKS[key]
    font = ImageFont.load_default(size=max(10, min(18, layout.room_size // 3)))
    box = draw.textbbox((0, 0), mark, font=font, stroke_width=1)
    width, height = box[2] - box[0], box[3] - box[1]
    draw.text(
        (center[0] - (box[0] + box[2]) / 2, center[1] - (box[1] + box[3]) / 2),
        mark,
        font=font,
        fill="#f4eadb",
        stroke_width=1,
        stroke_fill="#17130f",
    )


def render_map(
    model: PreviewMapModel,
    canvas_width: int,
    canvas_height: int,
    *,
    icons: Mapping[str, Image.Image] | None = None,
) -> tuple[Image.Image, MapLayout]:
    """Render a readable partial map and return its hit-test layout."""

    width, height = max(320, canvas_width), max(240, canvas_height)
    layout = compute_layout(model.rooms, width, height)
    image = Image.new("RGBA", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(image)

    for column in range(layout.min_column, layout.max_column + 1):
        for row in range(layout.min_row, layout.max_row + 1):
            center = layout.cell_rect(column, row).center
            draw.point(center, fill=GRID_DOT)

    for connection in connection_segments(model):
        _draw_connection(draw, layout, connection)

    icon_images = icons or {}
    for room in model.rooms:
        mask = room_render_mask(room, layout)
        border = mask.filter(ImageFilter.MaxFilter(5))
        image.paste(OUTLINE, (0, 0), border)
        image.paste(ROOM_COLORS.get(room.room_type, ROOM_COLORS[1]), (0, 0), mask)

    draw = ImageDraw.Draw(image)
    for room in model.rooms:
        _draw_icon_or_mark(image, draw, room, layout, icon_images)
    return image, layout


def hit_test_room(
    model: PreviewMapModel, layout: MapLayout, x: float, y: float
) -> RenderRoom | None:
    for room in reversed(model.rooms):
        if any(layout.cell_rect(*cell).contains(x, y) for cell in room.cells):
            return room
    return None
