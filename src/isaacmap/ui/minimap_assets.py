"""ANM2 metadata and verified RoomType-to-minimap-icon bindings.

The semantic RoomType values come from the frozen installation's
``resources/scripts/enums.lua``.  Pixel rectangles are never duplicated in
code: they are parsed from the selected animation/layer/frame in ANM2.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Mapping
from xml.etree import ElementTree


@dataclass(frozen=True)
class MinimapFrame:
    animation: str
    animation_frame: int
    layer_id: int
    layer_name: str
    spritesheet_id: int
    spritesheet_path: str
    x_crop: int
    y_crop: int
    width: int
    height: int
    x_position: int
    y_position: int
    x_pivot: int
    y_pivot: int
    visible: bool

    @property
    def crop_rectangle(self) -> tuple[int, int, int, int]:
        return (
            self.x_crop,
            self.y_crop,
            self.x_crop + self.width,
            self.y_crop + self.height,
        )


@dataclass(frozen=True)
class MinimapAnm2Index:
    animations: Mapping[str, tuple[MinimapFrame, ...]]
    spritesheets: Mapping[int, str]

    def frame(self, animation: str, frame: int = 0) -> MinimapFrame:
        try:
            frames = self.animations[animation]
        except KeyError as error:
            raise ValueError(f"ANM2 animation not found: {animation}") from error
        if not 0 <= frame < len(frames):
            raise ValueError(
                f"ANM2 animation {animation!r} has no frame {frame}; "
                f"available frames: 0..{len(frames) - 1}"
            )
        return frames[frame]


# Bindings are semantic, not guessed crop coordinates.  When two RoomTypes use
# the same official animation (teleporter entrance/exit), each keeps its own UI
# key while the ANM2 parser resolves the shared frame.
ROOM_TYPE_ICON_ANIMATIONS: dict[int, tuple[str, str]] = {
    2: ("shop", "IconShop"),
    4: ("treasure", "IconTreasureRoom"),
    5: ("boss", "IconBoss"),
    6: ("miniboss", "IconMiniboss"),
    7: ("secret", "IconSecretRoom"),
    8: ("super_secret", "IconSuperSecretRoom"),
    9: ("arcade", "IconArcade"),
    10: ("curse", "IconCurseRoom"),
    11: ("challenge", "IconAmbushRoom"),
    12: ("library", "IconLibrary"),
    13: ("sacrifice", "IconSacrificeRoom"),
    14: ("devil", "IconDevilRoom"),
    15: ("angel", "IconAngelRoom"),
    17: ("boss_rush", "IconBossAmbushRoom"),
    18: ("isaacs", "IconIsaacsRoom"),
    19: ("barren", "IconBarrenRoom"),
    20: ("chest", "IconChestRoom"),
    21: ("dice", "IconDiceRoom"),
    24: ("planetarium", "IconPlanetarium"),
    25: ("teleporter", "IconTeleporterRoom"),
    26: ("teleporter_exit", "IconTeleporterRoom"),
    29: ("ultra_secret", "IconUltraSecretRoom"),
}


def icon_animations_by_key() -> dict[str, str]:
    return {key: animation for key, animation in ROOM_TYPE_ICON_ANIMATIONS.values()}


def _integer(attributes: Mapping[str, str], name: str, default: int = 0) -> int:
    try:
        return int(attributes.get(name, str(default)))
    except ValueError as error:
        raise ValueError(f"invalid integer ANM2 attribute {name!r}") from error


def parse_minimap_anm2(data: bytes | str) -> MinimapAnm2Index:
    """Index every visible layer frame and its declared spritesheet.

    The parser intentionally retains animation, layer, frame, crop, pivot and
    sheet metadata so cache extraction remains data-driven if the frozen asset
    is inspected again or a later version is introduced explicitly.
    """

    root = ElementTree.fromstring(data)
    spritesheets = {
        int(node.attrib["Id"]): PurePosixPath(node.attrib["Path"]).as_posix()
        for node in root.findall("./Content/Spritesheets/Spritesheet")
    }
    layers: dict[int, tuple[str, int]] = {}
    for node in root.findall("./Content/Layers/Layer"):
        layer_id = int(node.attrib["Id"])
        sheet_id = int(node.attrib["SpritesheetId"])
        if sheet_id not in spritesheets:
            raise ValueError(
                f"ANM2 layer {layer_id} references missing spritesheet {sheet_id}"
            )
        layers[layer_id] = (node.attrib.get("Name", str(layer_id)), sheet_id)

    animations: dict[str, tuple[MinimapFrame, ...]] = {}
    for animation in root.findall("./Animations/Animation"):
        animation_name = animation.attrib["Name"]
        frames: list[MinimapFrame] = []
        for layer_animation in animation.findall("./LayerAnimations/LayerAnimation"):
            layer_id = int(layer_animation.attrib.get("LayerId", "0"))
            if layer_id not in layers:
                raise ValueError(
                    f"ANM2 animation {animation_name!r} references missing layer {layer_id}"
                )
            layer_name, sheet_id = layers[layer_id]
            for frame_index, frame in enumerate(layer_animation.findall("./Frame")):
                frames.append(
                    MinimapFrame(
                        animation=animation_name,
                        animation_frame=frame_index,
                        layer_id=layer_id,
                        layer_name=layer_name,
                        spritesheet_id=sheet_id,
                        spritesheet_path=spritesheets[sheet_id],
                        x_crop=_integer(frame.attrib, "XCrop"),
                        y_crop=_integer(frame.attrib, "YCrop"),
                        width=_integer(frame.attrib, "Width"),
                        height=_integer(frame.attrib, "Height"),
                        x_position=_integer(frame.attrib, "XPosition"),
                        y_position=_integer(frame.attrib, "YPosition"),
                        x_pivot=_integer(frame.attrib, "XPivot"),
                        y_pivot=_integer(frame.attrib, "YPivot"),
                        visible=frame.attrib.get("Visible", "true").lower() == "true",
                    )
                )
        animations[animation_name] = tuple(frames)
    return MinimapAnm2Index(animations=animations, spritesheets=spritesheets)

