"""Static verifier for shared Stage-2 Ultra and late-default layout tail."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256


POST_RVA = 0x00339370
POST_SIZE = 17370
POST_SHA256 = "7ae850e43abce93f33e12ef5881bf9d09043ea866ad7773d643965659ad16996"
ULTRA_RVA = 0x005AE640
ULTRA_SIZE = 0x6F0
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
        data = read(rva, 5)
        if data[0] != 0xE8:
            raise ValueError(f"RVA 0x{rva:08X} is not a near call")
        return (rva + 5 + struct.unpack("<i", data[1:])[0]) & 0xFFFFFFFF

    calls = {
        "derive_current_room_config_stage": (0x003393DF, 0x0042D030),
        "type29_select_with_current_stage": (0x0033C9CD, 0x0042CDD0),
        "place_ultra": (0x0033CB05, ULTRA_RVA),
        "collect_late_rooms": (0x0033CB97, COLLECT_RVA),
        "late_default_select": (0x0033CCDE, 0x0042C7D0),
        "late_assign": (0x0033CD07, 0x00338AB0),
    }
    actual_calls = {name: call_target(rva) for name, (rva, _) in calls.items()}
    call_checks = {
        name: actual_calls[name] == expected for name, (_, expected) in calls.items()
    }
    byte_checks = {
        "room_config_stage_saved_once": (0x003393DF, "e84c3c0f0083c4048985d8feffff"),
        # Both type-29 and late ROOM_DEFAULT selectors push that saved stage
        # from [ebp-0x128].  No Basement-I literal is embedded in either call.
        "type29_current_stage_argument": (0x0033C9C0, "6a1d6a00ffb5d8feffff6a0152"),
        "late_default_current_stage_argument": (0x0033CCD3, "6a01ffb5d8feffff6a0150"),
        "type29_null_continues_to_late": (0x0033C9DA, "85f60f847b010000"),
        "ultra_null_allowed": (0x0033CB0A, "85c07428"),
        "ultra_descriptor_tail_99": (0x0033CB24, "6983cc820100b8000000c744181063000000"),
        "late_collect_unconditional_entry": (0x0033CB5D, "33dbc785fcfeffff00000000"),
        "late_null_returns_false": (0x0033CCE9, "85c00f84ac010000"),
        "false_return": (0x0033CF06, "32c0"),
        "collect_non_dead_first": (0x005AF12F, "8bb37c030000"),
        "collect_dead_second": (0x005AF17C, "8bb370030000"),
    }
    instruction_checks = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    hashes = {
        "post_topology": hashlib.sha256(read(POST_RVA, POST_SIZE)).hexdigest(),
        "place_ultra": hashlib.sha256(read(ULTRA_RVA, ULTRA_SIZE)).hexdigest(),
        "collect_late_rooms": hashlib.sha256(read(COLLECT_RVA, COLLECT_SIZE)).hexdigest(),
    }
    actual_hash = hashlib.sha256(payload).hexdigest()
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "post_topology_hash": hashes["post_topology"] == POST_SHA256,
        "control_transfers": all(call_checks.values()),
        "shared_tail_instruction_bytes": all(instruction_checks.values()),
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE read as bytes only; no image loading or execution.",
        "scope": "canonical Basement II shared Ultra/late-default accepted-layout tail",
        "function_hashes": hashes,
        "control_transfers": {
            name: f"0x{target:08X}" for name, target in actual_calls.items()
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
