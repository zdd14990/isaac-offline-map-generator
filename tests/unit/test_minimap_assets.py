from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image

from isaacmap.ui import icons
from isaacmap.ui.minimap_assets import (
    ROOM_TYPE_ICON_ANIMATIONS,
    icon_animations_by_key,
    parse_minimap_anm2,
)


ANM2 = b"""<?xml version="1.0" encoding="UTF-8"?>
<AnimatedActor>
  <Content>
    <Spritesheets><Spritesheet Path="minimap_icons.png" Id="0"/></Spritesheets>
    <Layers><Layer Name="main" Id="0" SpritesheetId="0"/></Layers>
  </Content>
  <Animations>
    <Animation Name="IconShop" FrameNum="1" Loop="true">
      <LayerAnimations><LayerAnimation LayerId="0" Visible="true">
        <Frame XPosition="2" YPosition="3" XPivot="4" YPivot="5"
          XCrop="16" YCrop="32" Width="16" Height="16" Visible="true"/>
      </LayerAnimation></LayerAnimations>
    </Animation>
  </Animations>
</AnimatedActor>
"""


def test_anm2_index_exposes_sheet_layer_frame_crop_and_transform() -> None:
    index = parse_minimap_anm2(ANM2)
    frame = index.frame("IconShop")
    assert index.spritesheets == {0: "minimap_icons.png"}
    assert frame.layer_name == "main"
    assert frame.spritesheet_path == "minimap_icons.png"
    assert frame.crop_rectangle == (16, 32, 32, 48)
    assert (frame.x_position, frame.y_position) == (2, 3)
    assert (frame.x_pivot, frame.y_pivot) == (4, 5)
    assert frame.animation_frame == 0
    assert frame.visible


def test_room_type_bindings_reference_animation_names_not_crop_guesses() -> None:
    by_key = icon_animations_by_key()
    assert ROOM_TYPE_ICON_ANIMATIONS[7] == ("secret", "IconSecretRoom")
    assert ROOM_TYPE_ICON_ANIMATIONS[24] == ("planetarium", "IconPlanetarium")
    assert ROOM_TYPE_ICON_ANIMATIONS[29] == ("ultra_secret", "IconUltraSecretRoom")
    assert by_key["challenge"] == "IconAmbushRoom"


def test_official_cache_extractor_uses_parsed_anm2_crop(
    tmp_path: Path, monkeypatch
) -> None:
    game_root = tmp_path / "game"
    archive = game_root / "resources" / "packed" / icons.SOURCE_ARCHIVE
    archive.parent.mkdir(parents=True)
    archive.write_bytes(b"static archive placeholder")

    required = icon_animations_by_key()
    animation_xml = "".join(
        f'<Animation Name="{animation}" FrameNum="1" Loop="true">'
        '<LayerAnimations><LayerAnimation LayerId="0">'
        '<Frame XCrop="0" YCrop="0" Width="16" Height="16" Visible="true"/>'
        '</LayerAnimation></LayerAnimations></Animation>'
        for animation in sorted(set(required.values()))
    )
    anm2 = (
        '<AnimatedActor><Content><Spritesheets>'
        '<Spritesheet Path="minimap_icons.png" Id="0"/>'
        '</Spritesheets><Layers><Layer Name="main" Id="0" SpritesheetId="0"/>'
        f'</Layers></Content><Animations>{animation_xml}</Animations></AnimatedActor>'
    ).encode()
    sheet = Image.new("RGBA", (16, 16), (255, 255, 255, 255))
    stream = BytesIO()
    sheet.save(stream, format="PNG")

    class FakeArchiveReader:
        def __init__(self, _path: Path) -> None:
            pass

        def read(self, path: str) -> bytes | None:
            return {
                icons.SOURCE_ANM2: anm2,
                icons.SOURCE_PNG: stream.getvalue(),
            }.get(path)

    monkeypatch.setattr(icons, "ArchiveReader", FakeArchiveReader)
    result = icons.ensure_official_icon_cache(
        tmp_path / "cache", game_root=game_root
    )
    assert result.used_official_assets
    assert set(result.images) == set(required)
    assert all(source.crop_rectangle == (0, 0, 16, 16) for source in result.sources)

