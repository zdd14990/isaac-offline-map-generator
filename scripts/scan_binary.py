"""Static-only signature and constant scanner for the copied Isaac PE.

This script opens a PE as data. It never loads or executes the image.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import pefile


@dataclass(frozen=True)
class Match:
    name: str
    file_offset: int
    rva: int
    virtual_address: int


def parse_pattern(pattern: str) -> tuple[bytes, bytes]:
    compact = "".join(pattern.split())
    if len(compact) % 2:
        raise ValueError(f"odd-length signature: {pattern!r}")
    values = bytearray()
    masks = bytearray()
    for pos in range(0, len(compact), 2):
        pair = compact[pos : pos + 2]
        if pair in {"??", "**"}:
            values.append(0)
            masks.append(0)
        else:
            values.append(int(pair, 16))
            masks.append(0xFF)
    return bytes(values), bytes(masks)


def find_pattern(data: bytes, values: bytes, masks: bytes) -> list[int]:
    if not values:
        return []
    first_exact = next((i for i, mask in enumerate(masks) if mask), None)
    if first_exact is None:
        return list(range(len(data) - len(values) + 1))
    needle = bytes([values[first_exact]])
    hits: list[int] = []
    start = 0
    last = len(data) - len(values)
    while start + first_exact <= last + first_exact:
        found = data.find(needle, start + first_exact)
        if found < 0:
            break
        candidate = found - first_exact
        if candidate >= start and candidate <= last:
            if all(not mask or data[candidate + i] == values[i] for i, mask in enumerate(masks)):
                hits.append(candidate)
        start = candidate + 1
    return hits


SIGNATURES = {
    # Team REPENTOGON ZHL signatures; scanned independently against the copied PE.
    "Seeds::String2Seed": "55 8b ec 81 ec 0c 01 00 00 a1 ?? ?? ?? ?? 33 c5 89 45 ?? 56",
    "Seeds::constructor": "55 8b ec 51 f3 0f 7e 05 ?? ?? ?? ?? a1 ?? ?? ?? ?? 53",
    "Seeds::set_start_seed": "55 8b ec 53 56 8b f1 8b 4d ?? 57 89 4e",
    "Seeds::IsStringValidSeed": "55 8b ec ff 75 08 e8 ?? ?? ?? ?? 83 c4 04 85 c0 0f 95 c0 5d c3",
    "Seeds::Seed2String": (
        "55 8b ec 83 ec 0c a1 ?? ?? ?? ?? 33 c5 89 45 fc 53 8b 5d 0c "
        "32 d2 8b cb 56 8b 75 08 89 75 f8 85 db 74 12"
    ),
    "RNG::SetSeed": "55 8b ec 8b 45 ?? 33 d2 3b 55",
    "RNG::RandomInt": "55 8b ec 56 8b f1 8b 16",
    "RNG::RandomFloat": "55 8b ec 51 56 8b f1 8b 16 85 d2",
    "RNG::Next": (
        "56 8b f1 8b 16 85 d2 75 ?? 68 ?? ?? ?? ?? 6a ?? e8 ?? ?? ?? ?? "
        "8b 16 83 c4 08 85 d2 75 ?? cc 8b 4e ?? 8b c2 d3 e8 8b 4e ?? 33 c2 "
        "8b d0 d3 e2 8b 4e ?? 33 d0 8b c2 d3 e8 33 c2 89 06 5e c3"
    ),
    "RNG::game_constructor": "55 8b ec 8b 45 ?? 56 8b f1 57 8b 7d",
    "LevelGenerator::Generate": "55 8b ec 83 ec 08 8a 45",
    "LevelGenerator::place_room": "55 8b ec 83 e4 f8 83 ec 0c 53 8b 5d ?? b8 39 8e e3 38",
    "LevelGenerator::CreateRoom": (
        "55 8b ec 6a ff 68 ?? ?? ?? ?? 64 a1 ?? ?? ?? ?? 50 83 ec 50 "
        "a1 ?? ?? ?? ?? 33 c5 89 45 ?? 56 57 50 8d 45 ?? 64 a3 ?? ?? ?? ?? "
        "8b f9 8b 45"
    ),
    "LevelGenerator::GetNewEndRoom": "55 8b ec 83 e4 f8 51 53 56 57 8b f9 8b b7",
    "LevelGenerator::DetermineBossRoom": "55 8b ec 83 e4 f8 83 ec 24 53 56 57 8b f9 89",
    "LevelGenerator::mark_dead_ends": (
        "55 8b ec 51 53 56 57 8b f9 b8 39 8e e3 38 33 db 8b 8f 68 03 00 00 "
        "8b d1 8b b7 64 03 00 00"
    ),
    "LevelGenerator::get_neighbor_candidates": (
        "55 8b ec 6a ff 68 ?? ?? ?? ?? 64 a1 ?? ?? ?? ?? 50 81 ec 68 01 00 00 "
        "a1 ?? ?? ?? ?? 33 c5 89 45 ?? 53"
    ),
    "LevelGenerator::calc_required_doors": (
        "55 8b ec 83 e4 f8 83 ec 0c 53 56 57 8b f9 8b 87 70 03 00 00 "
        "8d 9f 70 03 00 00"
    ),
    "LevelGenerator::is_pos_free (generic signature candidate)": "55 8b ec 83 e4 f8 51 53 56 8b f1 57 8b 86",
    "LevelGenerator::is_placement_valid": (
        "55 8b ec 83 e4 f8 83 ec 24 53 56 8b 75 0c 33 db 57 8b 7d 08 89 4c 24 0c"
    ),
    "LevelGenerator::get_room_placement_offsets": "64 a1 ?? ?? ?? ?? 56 57 8b f9",
    "LevelGenerator::get_door_source_position": "55 8b ec 51 56 57 8b fa",
    "LevelGenerator::get_door_target_position": (
        "55 8b ec 83 e4 f8 81 ec 54 01 00 00 a1 ?? ?? ?? ?? 33 c4 "
        "89 84 24 ?? ?? ?? ?? 8b 45"
    ),
    "LevelGenerator::has_shape_slot": "55 8b ec 83 3c cd ?? ?? ?? ?? 01",
    "LevelGenerator_Room::constructor": "55 8b ec 51 8b 45 ?? 53 8b d9 56 57 8b 7d",
    "Level::Init (generic signature candidate)": (
        "53 8b dc 83 ec 08 83 e4 f8 83 c4 04 55 8b 6b ?? 89 6c 24 ?? 8b ec "
        "6a ff 68 ?? ?? ?? ?? 64 a1 ?? ?? ?? ?? 50 53 83 ec 68 a1 ?? ?? ?? ?? "
        "33 c5 89 45 ?? 56 57 50 8d 45 ?? 64 a3 ?? ?? ?? ?? 8b f9 89 7d"
    ),
    "Level::generate_dungeon": (
        "53 8b dc 83 ec 08 83 e4 f8 83 c4 04 55 8b 6b ?? 89 6c 24 ?? 8b ec "
        "6a ff 68 ?? ?? ?? ?? 64 a1 ?? ?? ?? ?? 50 53 81 ec 50 04 00 00"
    ),
}


CONSTANTS = {
    "seed_alphabet_ascii": b"ABCDEFGHJKLMNPQRSTWXYZ01234V6789",
    "seed_xor_0x0FEF7FFD_le": bytes.fromhex("fd7fef0f"),
}


def offset_to_rva(pe: pefile.PE, offset: int) -> int:
    return pe.get_rva_from_offset(offset)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    data = args.pe.read_bytes()
    pe = pefile.PE(data=data, fast_load=False)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    matches: list[Match] = []

    for name, pattern in SIGNATURES.items():
        values, masks = parse_pattern(pattern)
        for offset in find_pattern(data, values, masks):
            rva = offset_to_rva(pe, offset)
            matches.append(Match(name, offset, rva, image_base + rva))

    for name, constant in CONSTANTS.items():
        start = 0
        while True:
            offset = data.find(constant, start)
            if offset < 0:
                break
            rva = offset_to_rva(pe, offset)
            matches.append(Match(name, offset, rva, image_base + rva))
            start = offset + 1

    payload = {
        "pe": str(args.pe.resolve()),
        "image_base": image_base,
        "matches": [asdict(match) for match in sorted(matches, key=lambda item: (item.name, item.rva))],
    }
    rendered = json.dumps(payload, indent=2)
    print(rendered)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
