"""Verify static instructions used by the canonical late default pass."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256


LATE_RVA = 0x0033CB5D
LATE_SIZE = 0x3C6
COLLECT_RVA = 0x005AF0E0
COLLECT_SIZE = 0xFE


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    payload = args.pe.read_bytes()
    pe = pefile.PE(data=payload, fast_load=True)

    def read(rva: int, size: int) -> bytes:
        return pe.get_data(rva, size)

    def call_target(rva: int) -> int:
        instruction = read(rva, 5)
        if instruction[0] != 0xE8:
            raise ValueError(f"RVA 0x{rva:08X} is not a near call")
        displacement = struct.unpack("<i", instruction[1:])[0]
        return (rva + 5 + displacement) & 0xFFFFFFFF

    transfers = {
        "collect_rooms": call_target(0x0033CB97),
        "start_get_room": call_target(0x0033CC84),
        "level_rng_selector_seed": call_target(0x0033CCA5),
        "direct_select_room": call_target(0x0033CCDE),
        "assign_room_config": call_target(0x0033CD07),
        "excluded_room_rng_advance": call_target(0x0033CDD2),
    }
    expected_transfers = {
        "collect_rooms": 0x005AF0E0,
        "start_get_room": 0x0042C720,
        "level_rng_selector_seed": 0x003E90F0,
        "direct_select_room": 0x0042C7D0,
        "assign_room_config": 0x00338AB0,
        "excluded_room_rng_advance": 0x003E90F0,
    }
    byte_checks = {
        # collect_rooms reads non-dead ends (+0x37c) first, then remaining
        # dead ends (+0x370).
        "collect_non_dead_first": (0x005AF12F, "8bb37c030000"),
        "collect_dead_second": (0x005AF17C, "8bb370030000"),
        "hard_minimum_pre_draw_gate": (0x0033CC0D, "f60707"),
        "shape_from_generated_room": (0x0033CC9A, "8b4018"),
        "required_doors_address": (0x0033CC97, "8d781c"),
        "room_type_default": (0x0033CCD3, "6a01"),
        "reduce_weight_true": (0x0033CCDB, "6a01"),
        "null_selector_branch": (0x0033CCE9, "85c00f84ac010000"),
        "false_return": (0x0033CF06, "32c0"),
        "start_variant_two": (0x0033CC71, "33c0b902000000"),
    }
    byte_results = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    actual_hash = hashlib.sha256(payload).hexdigest()
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "control_transfers": transfers == expected_transfers,
        "instruction_constants": all(byte_results.values()),
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE read as bytes only; no image loading or execution.",
        "late_slice_rva": f"0x{LATE_RVA:08X}",
        "late_slice_size": LATE_SIZE,
        "late_slice_sha256": hashlib.sha256(read(LATE_RVA, LATE_SIZE)).hexdigest(),
        "collect_rooms_rva": f"0x{COLLECT_RVA:08X}",
        "collect_rooms_size": COLLECT_SIZE,
        "collect_rooms_sha256": hashlib.sha256(read(COLLECT_RVA, COLLECT_SIZE)).hexdigest(),
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
