"""Verify static constants used by the first topology reconstruction step."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct

import pefile

from isaacmap.topology_geometry import DIRECTION_OFFSETS, SHAPE_DIMENSIONS


LEVEL_RNG_SHIFTS_RVA = 0x0071F66C
SHAPE_DIMENSIONS_RVA = 0x0085D378
DIRECTION_OFFSETS_RVA = 0x0085D3E0
START_ROOM_CONSTANTS_RVA = 0x007AAF30


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    payload = args.pe.read_bytes()
    pe = pefile.PE(data=payload, fast_load=True)

    def unpack(rva: int, formatter: str) -> tuple[int, ...]:
        return struct.unpack_from(formatter, payload, pe.get_offset_from_rva(rva))

    shifts = unpack(LEVEL_RNG_SHIFTS_RVA, "<3I")
    dimensions_flat = unpack(SHAPE_DIMENSIONS_RVA, "<26i")
    dimensions = tuple(
        tuple(dimensions_flat[index:index + 2])
        for index in range(0, len(dimensions_flat), 2)
    )
    directions_flat = unpack(DIRECTION_OFFSETS_RVA, "<8i")
    directions = tuple(
        tuple(directions_flat[index:index + 2])
        for index in range(0, len(directions_flat), 2)
    )
    start_column, start_line = unpack(START_ROOM_CONSTANTS_RVA, "<2I")

    checks = {
        "level_rng_shifts": shifts == (5, 9, 7),
        "shape_dimensions": dimensions == SHAPE_DIMENSIONS,
        "direction_offsets": directions == DIRECTION_OFFSETS,
        "start_position": (start_column, start_line) == (6, 6),
    }
    report = {
        "pe": str(args.pe.resolve()),
        "level_init_rva": "0x00344940",
        "level_generate_dungeon_rva": "0x00340e10",
        "level_generator_constructor_rva": "0x005adaf0",
        "level_generator_generate_rva": "0x005adbb0",
        "level_generator_generate_rooms_rva": "0x005b04d0",
        "level_generator_neighbors_rva": "0x005b0b00",
        "level_rng_shifts": shifts,
        "shape_dimensions": dimensions,
        "direction_offsets": directions,
        "start_position": [start_column, start_line],
        "start_grid_index": start_line * 13 + start_column,
        "checks": checks,
        "matches": all(checks.values()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
