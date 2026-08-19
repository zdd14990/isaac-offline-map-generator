from __future__ import annotations

import struct

import pytest

from isaacmap.resources import ResourceFormatError, parse_stb


def _sample_stb() -> bytes:
    return b"".join(
        [
            struct.pack("<4sI", b"STB1", 1),
            struct.pack("<IIIBH", 1, 123, 4, 7, 4),
            b"Test",
            struct.pack("<fBBBBH", 2.5, 13, 7, 1, 1, 1),
            struct.pack("<hh?", -1, 3, True),
            struct.pack("<hhB", 2, 5, 1),
            struct.pack("<HHHf", 10, 20, 30, 0.75),
        ]
    )


def test_parse_stb1_room_metadata_and_entities() -> None:
    [room] = parse_stb(_sample_stb())
    assert (room.room_type, room.variant, room.subtype) == (1, 123, 4)
    assert (room.difficulty, room.name, room.weight, room.shape) == (7, "Test", 2.5, 1)
    assert (room.stored_width, room.stored_height) == (13, 7)
    assert (room.grid_width, room.grid_height) == (15, 9)
    assert (room.doors[0].stored_x, room.doors[0].grid_x) == (-1, 0)
    assert room.doors[0].exists is True
    assert (room.spawns[0].stored_x, room.spawns[0].grid_x) == (2, 3)
    assert room.spawns[0].entities[0].subtype == 30


@pytest.mark.parametrize(
    "payload",
    [b"", b"STB0" + b"\x00" * 4, _sample_stb()[:-1], _sample_stb() + b"x"],
)
def test_invalid_stb_is_rejected(payload: bytes) -> None:
    with pytest.raises(ResourceFormatError):
        parse_stb(payload)
