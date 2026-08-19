"""Verify Stage-2 entry through the shared Treasure boundary statically."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256


FUNCTION_RVA = 0x00339370
FUNCTION_SIZE = 17370
FUNCTION_SHA256 = "7ae850e43abce93f33e12ef5881bf9d09043ea866ad7773d643965659ad16996"


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

    calls = {
        "boss_identity": (0x00339475, 0x00022830),
        "boss_config": (0x003394C3, 0x00339080),
        "boss_geometry": (0x003394F2, 0x005AEF10),
        "type8_config": (0x00339B64, 0x0042C7D0),
        "type8_geometry": (0x00339B78, 0x005AE0E0),
        "shop_config": (0x0033A205, 0x0042C7D0),
        "shop_geometry": (0x0033A219, 0x005AE0E0),
        "treasure_stage_wrapper": (0x0033A7AD, 0x0042CDD0),
        "treasure_geometry": (0x0033A7C1, 0x005AE0E0),
    }
    actual_calls = {name: call_target(rva) for name, (rva, _) in calls.items()}
    call_checks = {
        name: actual_calls[name] == expected for name, (_, expected) in calls.items()
    }
    byte_checks = {
        "additional_boss_only_stage_twelve": (
            0x00339533,
            "833e0c0f8595030000",
        ),
        "xl_uses_curse_bit_two": (0x003398F8, "a802"),
        "shop_accepts_stage_below_seven": (0x00339C0A, "8b0683f8077c76"),
        "treasure_accepts_stage_below_seven": (0x0033A2C3, "8b0683f8077c6e"),
        "treasure_passes_current_config_stage": (
            0x0033A79E,
            "6a0d6a046a00ffb5d8feffff6a0150",
        ),
        "treasure_geometry_failure_rejects_attempt": (
            0x0033A7C6,
            "85c00f8438270000",
        ),
    }
    instruction_checks = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    actual_hash = hashlib.sha256(payload).hexdigest()
    function_hash = hashlib.sha256(read(FUNCTION_RVA, FUNCTION_SIZE)).hexdigest()
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "function_hash": function_hash == FUNCTION_SHA256,
        "control_transfers": all(call_checks.values()),
        "stage_predicates": all(instruction_checks.values()),
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE read as bytes only; no image loading or execution.",
        "scope": "canonical Basement II shared Boss/Type8/Shop/Treasure boundary",
        "function_rva": f"0x{FUNCTION_RVA:08X}",
        "function_size": FUNCTION_SIZE,
        "function_sha256": function_hash,
        "control_transfers": {
            key: f"0x{value:08X}" for key, value in actual_calls.items()
        },
        "control_transfer_checks": call_checks,
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
