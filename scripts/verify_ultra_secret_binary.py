"""Verify static constants/control transfers used by Ultra reconstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256
from isaacmap.ultra_secret import OUTER_OFFSETS


FUNCTION_RVA = 0x005AE640
FUNCTION_SIZE = 0x6F0
CARDINAL_VECTOR_RVAS = (0x007ACC40, 0x007AB0D0)
OUTER_VECTOR_RVAS = (0x007ACC90, 0x007ACC70, 0x007AB120, 0x007AB1C0)
ULTRA_SHIFT_RVA = 0x0071F81C


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    payload = args.pe.read_bytes()
    pe = pefile.PE(data=payload, fast_load=True)

    def read(rva: int, size: int) -> bytes:
        return pe.get_data(rva, size)

    def ints(rva: int, count: int) -> tuple[int, ...]:
        return struct.unpack(f"<{count}i", read(rva, count * 4))

    def call_target(rva: int) -> int:
        instruction = read(rva, 5)
        if instruction[0] != 0xE8:
            raise ValueError(f"RVA 0x{rva:08X} is not a near call")
        displacement = struct.unpack("<i", instruction[1:])[0]
        return (rva + 5 + displacement) & 0xFFFFFFFF

    cardinal = tuple(
        pair
        for rva in CARDINAL_VECTOR_RVAS
        for pair in zip(ints(rva, 4)[::2], ints(rva, 4)[1::2])
    )
    outer = tuple(
        pair
        for rva in OUTER_VECTOR_RVAS
        for pair in zip(ints(rva, 4)[::2], ints(rva, 4)[1::2])
    )
    shifts = ints(ULTRA_SHIFT_RVA, 3)
    byte_checks = {
        "scan_169": (0x005AEAC7, "81fea9000000"),
        "candidate_mod_5": (0x005AE78A, "b905000000"),
        "base_plus_10": (0x005AE79C, "8d720a"),
        "immediate_minus_100": (0x005AE81A, "83c69c"),
        "outer_invalid_minus_100": (0x005AE94C, "83ad18ffffff64"),
        "new_room_shape_1": (0x005AEB3E, "6a01"),
        "red_door_bit_or": (0x005AEC76, "09421c"),
    }
    byte_results = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    transfers = {
        "caller_to_ultra": call_target(0x0033CB05),
        "room_constructor": call_target(0x005AEB6B),
        "place_room": call_target(0x005AEB81),
        "update_new_connections": call_target(0x005AEB9F),
        "door_target_scoring": call_target(0x005AE8D1),
        "door_target_red_write": call_target(0x005AEC06),
    }
    transfer_expected = {
        "caller_to_ultra": 0x005AE640,
        "room_constructor": 0x003381B0,
        "place_room": 0x005B0330,
        "update_new_connections": 0x005AF980,
        "door_target_scoring": 0x005AF620,
        "door_target_red_write": 0x005AF620,
    }
    checks = {
        "profile_hash": hashlib.sha256(payload).hexdigest() == PROFILE_SHA256,
        "cardinal_offsets": cardinal == ((-1, 0), (0, -1), (1, 0), (0, 1)),
        "outer_offsets": outer == OUTER_OFFSETS,
        "index_71_shifts": shifts == (13, 3, 17),
        "control_transfers": transfers == transfer_expected,
        "instruction_constants": all(byte_results.values()),
    }
    function_bytes = read(FUNCTION_RVA, FUNCTION_SIZE)
    report = {
        "profile_sha256": hashlib.sha256(payload).hexdigest(),
        "safety": "PE read as bytes only; no image loading or execution.",
        "function_rva": f"0x{FUNCTION_RVA:08X}",
        "function_size": FUNCTION_SIZE,
        "function_sha256": hashlib.sha256(function_bytes).hexdigest(),
        "cardinal_offsets": cardinal,
        "outer_offsets": outer,
        "index_71_shifts": shifts,
        "control_transfers": {
            key: f"0x{value:08X}" for key, value in transfers.items()
        },
        "instruction_checks": byte_results,
        "checks": checks,
        "matches": all(checks.values()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

