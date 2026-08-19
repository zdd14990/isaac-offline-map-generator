"""Offline resource discovery for XML and STB room databases."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import struct
from typing import Iterable

from .archive import ArchiveError, ArchiveReader


@dataclass(frozen=True)
class ResourceRecord:
    logical_path: str
    archive: str
    size: int
    output_path: Path


class ResourceFormatError(ValueError):
    """Raised when an extracted resource is structurally invalid."""


@dataclass(frozen=True)
class DoorDefinition:
    stored_x: int
    stored_y: int
    grid_x: int
    grid_y: int
    exists: bool


@dataclass(frozen=True)
class EntityDefinition:
    entity_type: int
    variant: int
    subtype: int
    weight: float


@dataclass(frozen=True)
class SpawnDefinition:
    stored_x: int
    stored_y: int
    grid_x: int
    grid_y: int
    entities: tuple[EntityDefinition, ...]


@dataclass(frozen=True)
class RoomDefinition:
    room_type: int
    variant: int
    subtype: int
    difficulty: int
    name: str
    weight: float
    stored_width: int
    stored_height: int
    grid_width: int
    grid_height: int
    shape: int
    doors: tuple[DoorDefinition, ...]
    spawns: tuple[SpawnDefinition, ...]
    source: Path | None = None


_STB_HEADER = struct.Struct("<4sI")
_STB_ROOM_PREFIX = struct.Struct("<IIIBH")
_STB_ROOM_SUFFIX = struct.Struct("<fBBBBH")
_STB_DOOR = struct.Struct("<hh?")
_STB_SPAWN = struct.Struct("<hhB")
_STB_ENTITY = struct.Struct("<HHHf")


def _unpack_at(formatter: struct.Struct, data: bytes, offset: int) -> tuple[tuple, int]:
    end = offset + formatter.size
    if end > len(data):
        raise ResourceFormatError(
            f"truncated STB record at offset 0x{offset:x}: "
            f"need {formatter.size} bytes, have {len(data) - offset}"
        )
    return formatter.unpack_from(data, offset), end


def parse_stb(data: bytes, *, source: Path | None = None) -> list[RoomDefinition]:
    """Parse the current game's little-endian ``STB1`` room format.

    The record layout is independently translated from the static format and
    cross-checked against Gibbed.Rebirth and Basement Renovator. Coordinates
    preserve both their stored values and their +1 bordered-grid values.
    """

    (header, room_count), offset = _unpack_at(_STB_HEADER, data, 0)
    if header != b"STB1":
        raise ResourceFormatError(f"expected STB1 header, got {header!r}")

    rooms: list[RoomDefinition] = []
    for room_number in range(room_count):
        try:
            (
                room_type,
                variant,
                subtype,
                difficulty,
                name_length,
            ), offset = _unpack_at(_STB_ROOM_PREFIX, data, offset)
            name_end = offset + name_length
            if name_end > len(data):
                raise ResourceFormatError(
                    f"truncated room name at offset 0x{offset:x}: "
                    f"need {name_length} bytes"
                )
            try:
                name = data[offset:name_end].decode("utf-8")
            except UnicodeDecodeError as error:
                raise ResourceFormatError(
                    f"room {room_number} name is not UTF-8"
                ) from error
            offset = name_end

            (
                weight,
                stored_width,
                stored_height,
                shape,
                door_count,
                spawn_count,
            ), offset = _unpack_at(_STB_ROOM_SUFFIX, data, offset)

            doors: list[DoorDefinition] = []
            for _ in range(door_count):
                (x, y, exists), offset = _unpack_at(_STB_DOOR, data, offset)
                doors.append(
                    DoorDefinition(
                        stored_x=x,
                        stored_y=y,
                        grid_x=x + 1,
                        grid_y=y + 1,
                        exists=exists,
                    )
                )

            spawns: list[SpawnDefinition] = []
            for _ in range(spawn_count):
                (x, y, entity_count), offset = _unpack_at(_STB_SPAWN, data, offset)
                entities: list[EntityDefinition] = []
                for _ in range(entity_count):
                    (
                        entity_type,
                        entity_variant,
                        entity_subtype,
                        entity_weight,
                    ), offset = _unpack_at(_STB_ENTITY, data, offset)
                    entities.append(
                        EntityDefinition(
                            entity_type=entity_type,
                            variant=entity_variant,
                            subtype=entity_subtype,
                            weight=entity_weight,
                        )
                    )
                spawns.append(
                    SpawnDefinition(
                        stored_x=x,
                        stored_y=y,
                        grid_x=x + 1,
                        grid_y=y + 1,
                        entities=tuple(entities),
                    )
                )
        except ResourceFormatError as error:
            location = f" in {source}" if source is not None else ""
            raise ResourceFormatError(f"room {room_number}{location}: {error}") from error

        rooms.append(
            RoomDefinition(
                room_type=room_type,
                variant=variant,
                subtype=subtype,
                difficulty=difficulty,
                name=name,
                weight=weight,
                stored_width=stored_width,
                stored_height=stored_height,
                grid_width=stored_width + 2,
                grid_height=stored_height + 2,
                shape=shape,
                doors=tuple(doors),
                spawns=tuple(spawns),
                source=source,
            )
        )

    if offset != len(data):
        location = f" in {source}" if source is not None else ""
        raise ResourceFormatError(
            f"{len(data) - offset} trailing bytes after {room_count} rooms{location}"
        )
    return rooms


def load_stb(path: Path | str) -> list[RoomDefinition]:
    source = Path(path)
    return parse_stb(source.read_bytes(), source=source)


@dataclass(frozen=True)
class RoomDatabase:
    rooms: tuple[RoomDefinition, ...]
    files: tuple[Path, ...]

    @classmethod
    def load(cls, paths: Iterable[Path | str]) -> "RoomDatabase":
        files = tuple(sorted((Path(path) for path in paths), key=lambda path: str(path).lower()))
        rooms = tuple(room for path in files for room in load_stb(path))
        return cls(rooms=rooms, files=files)

    @classmethod
    def from_directory(cls, root: Path | str) -> "RoomDatabase":
        directory = Path(root)
        return cls.load(directory.rglob("*.stb"))


def relevant_filelist_entries(filelist: Path | str) -> list[str]:
    """Return named base-resource XML/STB entries used by layout research."""

    lines = Path(filelist).read_text(encoding="utf-8").splitlines()
    return sorted(
        line
        for line in lines
        if line.startswith("resources/") and line.lower().endswith((".xml", ".stb"))
    )


def extract_resource_layers(
    archives: list[Path], logical_paths: list[str], output_root: Path
) -> list[ResourceRecord]:
    """Extract known paths into per-archive layers and a last-wins merged tree."""

    records: list[ResourceRecord] = []
    merged_root = output_root / "merged"
    for archive_path in archives:
        reader = ArchiveReader(archive_path)
        layer_root = output_root / "layers" / archive_path.name
        for logical_path in logical_paths:
            try:
                payload = reader.read(logical_path)
            except ArchiveError as error:
                raise ArchiveError(f"{archive_path.name}:{logical_path}: {error}") from error
            if payload is None:
                continue
            relative = Path(*logical_path.split("/"))
            layer_output = layer_root / relative
            merged_output = merged_root / relative
            layer_output.parent.mkdir(parents=True, exist_ok=True)
            merged_output.parent.mkdir(parents=True, exist_ok=True)
            layer_output.write_bytes(payload)
            merged_output.write_bytes(payload)
            records.append(
                ResourceRecord(
                    logical_path=logical_path,
                    archive=archive_path.name,
                    size=len(payload),
                    output_path=layer_output,
                )
            )
    return records
