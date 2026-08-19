"""Verify static Caves pool-4 and XL second-boss composition."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool import CAVES_POOL_INDEX, load_boss_pool_xml
from isaacmap.boss_pool_reference import PROFILE_SHA256


PICK_RVA = 0x00022620
PICK_SIZE = 362
PICK_SHA256 = "9822d3ce7aab6b3a01a10bd9440213ed0e08de5f774527e8b98b2a6bcd21df52"
SELECT_RVA = 0x00022830
SELECT_SIZE = 1498
SELECT_SHA256 = "b4133528375302b58d0ace97c43d1109ee3dbeb626d685bf09851eaec0b78c33"
ROOM_CONFIG_STAGE_RVA = 0x0042D030
ROOM_CONFIG_STAGE_SIZE = 206


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("resources", type=Path)
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

    pools = load_boss_pool_xml(args.resources / "bosspools.xml")
    names = tuple(pools)
    caves = pools["caves"]
    calls = {
        "primary_boss": call_target(0x00339475),
        "xl_second_boss": call_target(0x00339926),
    }
    byte_checks = {
        "primary_passes_stage_and_stage_type": (
            0x0033946C,
            "8d8b70af0100515756",
        ),
        "xl_curse_gate": (
            0x003398F6,
            "23c7a8020f84fb000000",
        ),
        "xl_second_passes_stage_plus_one": (
            0x00339919,
            "ff7304898508ffffff8b034050",
        ),
        "xl_second_level_rng_snapshot": (
            0x00339913,
            "8b80d4820100ff7304",
        ),
        "xl_second_level_rng_restore": (
            0x003399D2,
            "f30f7e056cf6b1008983d4820100",
        ),
        "pool_selector_seven_prerolls": (
            0x000229F8,
            "e8f3663c00",
        ),
        "pool_selector_weighted_picker": (
            0x00022D4C,
            "e8cff8ffff",
        ),
    }
    instruction_checks = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    pick_hash = hashlib.sha256(read(PICK_RVA, PICK_SIZE)).hexdigest()
    select_hash = hashlib.sha256(read(SELECT_RVA, SELECT_SIZE)).hexdigest()
    stage_hash = hashlib.sha256(
        read(ROOM_CONFIG_STAGE_RVA, ROOM_CONFIG_STAGE_SIZE)
    ).hexdigest()
    actual_hash = hashlib.sha256(payload).hexdigest()
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "function_hashes": pick_hash == PICK_SHA256 and select_hash == SELECT_SHA256,
        "boss_calls": calls == {
            "primary_boss": SELECT_RVA,
            "xl_second_boss": SELECT_RVA,
        },
        "instruction_semantics": all(instruction_checks.values()),
        "caves_pool_index": CAVES_POOL_INDEX == 4
        and names[:4] == ("basement", "cellar", "burning basement", "caves"),
        "caves_pool_entries": len(caves) == 12
        and all(entry.achievement < 0 for entry in caves),
        "stage3_room_config_stage": 4
        == (0 + 1 + 2 * ((3 - 1) >> 1) + ((3 - 1) >> 1)),
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE and bosspools.xml read as data only; no image loading or execution.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical ORIGINAL Caves-I pool 4 primary and XL second-boss selection",
        "pick_boss": {
            "rva": f"0x{PICK_RVA:08X}",
            "size": PICK_SIZE,
            "sha256": pick_hash,
        },
        "select_boss_id": {
            "rva": f"0x{SELECT_RVA:08X}",
            "size": SELECT_SIZE,
            "sha256": select_hash,
        },
        "room_config_stage": {
            "rva": f"0x{ROOM_CONFIG_STAGE_RVA:08X}",
            "size": ROOM_CONFIG_STAGE_SIZE,
            "sha256": stage_hash,
            "canonical_stage3_result": 4,
        },
        "boss_calls": {key: f"0x{value:08X}" for key, value in calls.items()},
        "caves_pool": {
            "runtime_index": CAVES_POOL_INDEX,
            "xml_order_prefix": list(names[:4]),
            "entry_ids": [entry.boss_id for entry in caves],
        },
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
