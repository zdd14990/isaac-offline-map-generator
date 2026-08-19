"""Read-only presentation models for the research preview."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from isaacmap.preview import PreviewGeneration
from isaacmap.topology_geometry import GRID_WIDTH, RoomShape, occupied_cells

from .minimap_assets import ROOM_TYPE_ICON_ANIMATIONS


ROOM_TYPE_NAMES = {
    0: "ROOM_NULL",
    1: "ROOM_DEFAULT",
    2: "ROOM_SHOP",
    3: "ROOM_ERROR",
    4: "ROOM_TREASURE",
    5: "ROOM_BOSS",
    6: "ROOM_MINIBOSS",
    7: "ROOM_SECRET",
    8: "ROOM_SUPER_SECRET",
    9: "ROOM_ARCADE",
    10: "ROOM_CURSE",
    11: "ROOM_CHALLENGE",
    12: "ROOM_LIBRARY",
    13: "ROOM_SACRIFICE",
    14: "ROOM_DEVIL",
    15: "ROOM_ANGEL",
    16: "ROOM_DUNGEON",
    17: "ROOM_BOSSRUSH",
    18: "ROOM_ISAACS",
    19: "ROOM_BARREN",
    20: "ROOM_CHEST",
    21: "ROOM_DICE",
    22: "ROOM_BLACK_MARKET",
    23: "ROOM_GREED_EXIT",
    24: "ROOM_PLANETARIUM",
    25: "ROOM_TELEPORTER",
    26: "ROOM_TELEPORTER_EXIT",
    27: "ROOM_SECRET_EXIT",
    28: "ROOM_BLUE",
    29: "ROOM_ULTRASECRET",
    30: "ROOM_DEATHMATCH",
}

ROOM_TYPE_DISPLAY_NAMES = {
    room_type: name.removeprefix("ROOM_").replace("_", " ").title()
    for room_type, name in ROOM_TYPE_NAMES.items()
}
ROOM_TYPE_DISPLAY_NAMES.update(
    {
        1: "Normal",
        6: "MiniBoss",
        8: "Super Secret",
        17: "Boss Rush",
        18: "Isaac's",
        22: "Black Market",
        23: "Greed Exit",
        24: "Planetarium",
        25: "Teleporter",
        26: "Teleporter Exit",
        27: "Secret Exit",
        28: "Blue",
        29: "Ultra Secret",
    }
)

# Every known non-default RoomType receives either an official icon key or a
# text fallback.  Actual art availability is kept separate in minimap_assets.
ROOM_TYPE_ICON_KEYS = {
    room_type: ROOM_TYPE_NAMES[room_type].removeprefix("ROOM_").lower()
    for room_type in ROOM_TYPE_NAMES
    if room_type not in (0, 1)
}
ROOM_TYPE_ICON_KEYS.update(
    {
        room_type: key
        for room_type, (key, _animation) in ROOM_TYPE_ICON_ANIMATIONS.items()
    }
)


@dataclass(frozen=True)
class RenderRoom:
    generation_index: int
    column: int
    line: int
    shape: RoomShape
    room_type: int = 1
    variant: int = -1
    subtype: int = -1
    distance_from_start: int = 0
    doors: int = 0
    neighbors: tuple[int, ...] = ()
    config_stage: int | None = None
    config_mode: int | None = None
    config_resource_index: int | None = None

    @property
    def grid_index(self) -> int:
        return self.line * GRID_WIDTH + self.column

    @property
    def cells(self) -> tuple[tuple[int, int], ...]:
        return occupied_cells(self.column, self.line, self.shape)

    @property
    def room_type_name(self) -> str:
        return ROOM_TYPE_NAMES.get(self.room_type, f"ROOM_TYPE_{self.room_type}")

    @classmethod
    def from_generated(cls, room: object, config: object | None = None) -> "RenderRoom":
        return cls(
            generation_index=int(room.generation_index),
            column=int(room.column),
            line=int(room.line),
            shape=RoomShape(int(room.shape)),
            room_type=int(room.room_type),
            variant=int(room.variant),
            subtype=int(room.subtype),
            distance_from_start=int(room.distance_from_start),
            doors=int(room.doors),
            neighbors=tuple(sorted(int(value) for value in room.neighbors)),
            config_stage=None if config is None else int(config.stage),
            config_mode=None if config is None else int(config.mode),
            config_resource_index=(
                None if config is None else int(config.resource_index)
            ),
        )


@dataclass(frozen=True)
class PreviewMapModel:
    rooms: tuple[RenderRoom, ...]
    room_map: tuple[int, ...]

    @classmethod
    def from_preview(cls, preview: PreviewGeneration) -> "PreviewMapModel":
        configs = dict(preview.descriptor_configs)
        return cls(
            rooms=tuple(
                RenderRoom.from_generated(room, configs.get(room.generation_index))
                for room in preview.rooms
            ),
            room_map=preview.room_map,
        )


def _config_dict(key: object | None) -> dict[str, int] | None:
    if key is None:
        return None
    return {
        "stage": int(key.stage),
        "mode": int(key.mode),
        "resource_index": int(key.resource_index),
    }


def preview_to_dict(preview: PreviewGeneration) -> dict[str, Any]:
    """Return a JSON-safe accepted-layout snapshot of the clean result."""

    post = preview.final_post_topology
    final = preview.final_late_default
    configs: dict[int, object] = dict(preview.descriptor_configs)

    rooms = []
    for room in preview.rooms:
        rendered = RenderRoom.from_generated(room, configs.get(room.generation_index))
        rooms.append(
            {
                "generation_index": rendered.generation_index,
                "grid_index": rendered.grid_index,
                "column": rendered.column,
                "row": rendered.line,
                "room_type": rendered.room_type,
                "room_type_name": rendered.room_type_name,
                "shape": int(rendered.shape),
                "shape_name": rendered.shape.name,
                "occupied_grid_indices": [
                    row * GRID_WIDTH + column for column, row in rendered.cells
                ],
                "doors": rendered.doors,
                "connections": list(rendered.neighbors),
                "variant": None if rendered.variant < 0 else rendered.variant,
                "subtype": None if rendered.subtype < 0 else rendered.subtype,
                "distance_from_start": rendered.distance_from_start,
                "config": _config_dict(configs.get(rendered.generation_index)),
            }
        )

    attempt_trace = []
    for index, attempt in enumerate(preview.attempts):
        through_treasure = attempt.through_treasure
        outcome = attempt.abort_operation or "accepted"
        attempt_trace.append(
            {
                "attempt": index,
                "outcome": outcome,
                "topology_usable": attempt.topology_usable,
                "target_room_count": attempt.target_room_count,
                "level_rng_start": attempt.start_level_rng_state,
                "level_rng_end": attempt.end_level_rng_state,
                "level_generator_rng_start": attempt.start_generator_rng_state,
                "level_generator_rng_end": attempt.end_generator_rng_state,
            }
        )

    pipeline = preview.pipeline_result
    return {
        "seed": preview.seed,
        "start_seed_uint32": preview.start_seed,
        "difficulty": preview.difficulty,
        "floor": preview.floor,
        "status": preview.generation_status,
        "partial": preview.partial,
        "algorithm_evidence": preview.algorithm_evidence,
        "gameplay_fixture": preview.gameplay_fixture,
        "stage_seed": pipeline.stage_seed,
        "attempts": preview.attempt_count,
        "final_attempt": preview.final_attempt_index,
        "attempt_trace": attempt_trace,
        "final_level_rng_state": pipeline.final_level_rng_state,
        "final_level_generator_rng_state": pipeline.final_generator_rng_state,
        "final_boss_pool_state": pipeline.final_boss_pool_state,
        "boss_id": post.boss_selection.boss_id,
        "boss_pool_index": post.boss_selection.pool_index,
        "boss_pool_persistent_state": post.boss_selection.persistent_post_state,
        "boss_room_config": _config_dict(post.boss_config),
        "super_secret_grid_indices": [
            post.rooms[room_id].line * GRID_WIDTH + post.rooms[room_id].column
            for room_id in post.type8_rooms
        ],
        "shop_grid_index": post.rooms[post.shop_room].line * GRID_WIDTH
        + post.rooms[post.shop_room].column,
        "treasure_grid_index": post.rooms[post.treasure_room].line * GRID_WIDTH
        + post.rooms[post.treasure_room].column,
        "secret_generation_supported": True,
        "secret_generated": preview.secret_grid_index is not None,
        "secret_grid_index": preview.secret_grid_index,
        "ultra_secret_generation_supported": True,
        "ultra_secret_generated": preview.ultra_secret_grid_index is not None,
        "ultra_secret_grid_index": preview.ultra_secret_grid_index,
        "normal_room_configs_supported": True,
        "not_yet_generated": [],
        "rooms": rooms,
    }


def room_tooltip(room: RenderRoom) -> str:
    lines = [
        f"GridIndex: {room.grid_index}",
        f"RoomType: {room.room_type_name}",
        f"Shape: {room.shape.name}",
    ]
    if room.variant >= 0:
        lines.append(f"Variant: {room.variant}")
    if room.subtype >= 0:
        lines.append(f"Subtype: {room.subtype}")
    if room.config_resource_index is not None:
        lines.append(
            "Config: "
            f"stage={room.config_stage} mode={room.config_mode} "
            f"resource={room.config_resource_index}"
        )
    lines.extend(
        (
            f"Generation order: {room.generation_index}",
            f"Distance from start: {room.distance_from_start}",
        )
    )
    return "\n".join(lines)


def legend_labels(model: PreviewMapModel | None) -> tuple[str, ...]:
    """Build the legend from RoomTypes that actually occur in the map."""

    labels = ["Start", "Normal"]
    if model is None:
        return tuple(labels)
    seen: set[int] = set()
    for room in model.rooms:
        if room.generation_index == 0 or room.room_type in (0, 1):
            continue
        if room.room_type in seen:
            continue
        seen.add(room.room_type)
        labels.append(
            ROOM_TYPE_DISPLAY_NAMES.get(room.room_type, f"RoomType {room.room_type}")
        )
    return tuple(labels)
