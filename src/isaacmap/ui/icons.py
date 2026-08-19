"""Read-only extraction and caching of official Isaac minimap icon frames."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from io import BytesIO
import json
import os
from pathlib import Path
from typing import Mapping
from PIL import Image

from isaacmap.archive import ArchiveReader

from .minimap_assets import icon_animations_by_key, parse_minimap_anm2


DEFAULT_GAME_ROOT = Path(
    os.environ.get("ISAAC_GAME_ROOT")
    or r"C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth"
)
SOURCE_ARCHIVE = "afterbirthp.a"
SOURCE_ANM2 = "resources/gfx/ui/minimap_icons.anm2"
SOURCE_PNG = "resources/gfx/ui/minimap_icons.png"
ICON_ANIMATIONS = icon_animations_by_key()


@dataclass(frozen=True)
class IconFrameSource:
    key: str
    animation: str
    source_asset: str
    source_archive: str
    source_anm2: str
    source_png: str
    frame: int
    crop_rectangle: tuple[int, int, int, int]


@dataclass(frozen=True)
class IconCacheResult:
    images: Mapping[str, Image.Image]
    sources: tuple[IconFrameSource, ...]
    used_official_assets: bool
    message: str


def _manifest_path(cache_dir: Path) -> Path:
    return cache_dir / "icon_manifest.json"


def _load_cached(cache_dir: Path) -> IconCacheResult | None:
    manifest_path = _manifest_path(cache_dir)
    if not manifest_path.is_file():
        return None
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        sources = tuple(
            IconFrameSource(
                key=item["key"],
                animation=item["animation"],
                source_asset=item["source_asset"],
                source_archive=item["source_archive"],
                source_anm2=item["source_anm2"],
                source_png=item["source_png"],
                frame=int(item["frame"]),
                crop_rectangle=tuple(int(value) for value in item["crop_rectangle"]),
            )
            for item in payload["icons"]
        )
        if {source.key for source in sources} != set(ICON_ANIMATIONS):
            return None
        images = {
            source.key: Image.open(cache_dir / f"{source.key}.png").convert("RGBA")
            for source in sources
        }
    except (KeyError, OSError, ValueError, TypeError, json.JSONDecodeError):
        return None
    return IconCacheResult(images, sources, True, "official minimap icon cache loaded")


def ensure_official_icon_cache(
    cache_dir: Path | str,
    *,
    game_root: Path | str = DEFAULT_GAME_ROOT,
) -> IconCacheResult:
    """Extract verified RoomType frames without modifying game resources."""

    target = Path(cache_dir)
    cached = _load_cached(target)
    if cached is not None:
        return cached

    archive_path = Path(game_root) / "resources" / "packed" / SOURCE_ARCHIVE
    if not archive_path.is_file():
        return IconCacheResult({}, (), False, "official archive unavailable; using text markers")
    try:
        reader = ArchiveReader(archive_path)
        anm2_data = reader.read(SOURCE_ANM2)
        png_data = reader.read(SOURCE_PNG)
        if anm2_data is None or png_data is None:
            raise ValueError("verified minimap icon assets are absent from the archive")
        index = parse_minimap_anm2(anm2_data)
        sprite = Image.open(BytesIO(png_data)).convert("RGBA")
        target.mkdir(parents=True, exist_ok=True)
        images: dict[str, Image.Image] = {}
        sources: list[IconFrameSource] = []
        for key, animation in ICON_ANIMATIONS.items():
            frame = index.frame(animation)
            if frame.spritesheet_path.casefold() != Path(SOURCE_PNG).name.casefold():
                raise ValueError(
                    f"animation {animation!r} references unexpected sheet "
                    f"{frame.spritesheet_path!r}"
                )
            crop = frame.crop_rectangle
            image = sprite.crop(crop)
            image.save(target / f"{key}.png")
            images[key] = image
            sources.append(
                IconFrameSource(
                    key=key,
                    animation=animation,
                    source_asset=f"{SOURCE_ANM2} → {SOURCE_PNG}",
                    source_archive=str(archive_path),
                    source_anm2=SOURCE_ANM2,
                    source_png=SOURCE_PNG,
                    frame=frame.animation_frame,
                    crop_rectangle=crop,
                )
            )
        manifest = {
            "read_only_source": True,
            "resize_filter": "Image.Resampling.NEAREST",
            "icons": [asdict(source) for source in sources],
        }
        _manifest_path(target).write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )
        return IconCacheResult(
            images, tuple(sources), True, "official minimap icons extracted to project cache"
        )
    except Exception as error:  # UI fallback must remain available without guessing art.
        return IconCacheResult({}, (), False, f"official icon extraction unavailable: {error}")
