"""Verify static Stage-2 floor-entry constants and control transfers."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256


INIT_SLICE_RVA = 0x00344CF3
INIT_SLICE_SIZE = 0x34D
DUNGEON_SLICE_RVA = 0x00340E8E
DUNGEON_SLICE_SIZE = 0x3A5


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
        data = read(rva, 5)
        if data[0] != 0xE8:
            raise ValueError(f"RVA 0x{rva:08X} is not a near call")
        return (rva + 5 + struct.unpack("<i", data[1:])[0]) & 0xFFFFFFFF

    transfers = {
        "curse_gate_random_int": call_target(0x00344F09),
        "labyrinth_stage_predicate": call_target(0x00344F77),
        "lost_mode_predicate": call_target(0x00344F97),
        "maze_mode_predicate": call_target(0x00344FD0),
        "curse_normalizer": call_target(0x00345008),
        "level_generator_constructor": call_target(0x00341233),
    }
    expected_transfers = {
        "curse_gate_random_int": 0x003E9020,
        "labyrinth_stage_predicate": 0x003385C0,
        "lost_mode_predicate": 0x002F8120,
        "maze_mode_predicate": 0x002F8120,
        "curse_normalizer": 0x00464AE0,
        "level_generator_constructor": 0x005ADAF0,
    }
    transfer_checks = {
        key: value == expected_transfers[key] for key, value in transfers.items()
    }
    byte_checks = {
        "normal_curse_denominator_80": (0x00344CF3, "ba50000000"),
        "hard_curse_denominator_40": (0x00344D75, "b828000000"),
        "curse_modulo_six": (0x00344F4B, "b8abaaaaaa"),
        "labyrinth_bit": (0x00344F84, "834f0c02"),
        "lost_bit": (0x00344FA9, "834f0c04"),
        "darkness_bit": (0x00344FB4, "834f0c01"),
        "unknown_bit": (0x00344FBF, "834f0c08"),
        "maze_bit": (0x00344FD9, "834f0c20"),
        "blind_bit": (0x00344FF2, "834f0c40"),
        "target_formula_divide_three": (0x00340EC4, "b856555555"),
        "target_add_five": (0x00340ECF, "c1e81f83c005"),
        "target_cap_twenty": (0x00340ED9, "be14000000"),
        "lost_add_four": (0x00340F8D, "8385fcfbffff04"),
        "hard_add_two_plus_bit": (0x003410D3, "8b8dfcfbffff83c10203ce"),
        "required_dead_end_base": (0x00341132, "33c083bde8fbffff01"),
        "required_dead_end_add_five": (0x00341144, "8b770c83c005"),
    }
    instruction_checks = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    actual_hash = hashlib.sha256(payload).hexdigest()
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "control_transfers": all(transfer_checks.values()),
        "instruction_constants": all(instruction_checks.values()),
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE read as bytes only; no image loading or execution.",
        "level_init_slice_rva": f"0x{INIT_SLICE_RVA:08X}",
        "level_init_slice_size": INIT_SLICE_SIZE,
        "level_init_slice_sha256": hashlib.sha256(
            read(INIT_SLICE_RVA, INIT_SLICE_SIZE)
        ).hexdigest(),
        "generate_dungeon_slice_rva": f"0x{DUNGEON_SLICE_RVA:08X}",
        "generate_dungeon_slice_size": DUNGEON_SLICE_SIZE,
        "generate_dungeon_slice_sha256": hashlib.sha256(
            read(DUNGEON_SLICE_RVA, DUNGEON_SLICE_SIZE)
        ).hexdigest(),
        "control_transfers": {
            key: f"0x{value:08X}" for key, value in transfers.items()
        },
        "control_transfer_checks": transfer_checks,
        "instruction_checks": instruction_checks,
        "checks": checks,
        "matches": all(checks.values()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
