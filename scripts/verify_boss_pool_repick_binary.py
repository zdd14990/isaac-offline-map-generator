"""Verify the inherited Basement BossPool repick/fallback instructions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256


PICK_RVA = 0x00022620
PICK_SIZE = 362
PICK_SHA256 = "9822d3ce7aab6b3a01a10bd9440213ed0e08de5f774527e8b98b2a6bcd21df52"
SELECT_RVA = 0x00022830
SELECT_SIZE = 1498
SELECT_SHA256 = "b4133528375302b58d0ace97c43d1109ee3dbeb626d685bf09851eaec0b78c33"


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

    next_calls = (
        0x000229F8,
        0x00022A02,
        0x00022A0D,
        0x00022A18,
        0x00022A23,
        0x00022A2E,
        0x00022A36,
    )
    transfers = {
        "seven_persistent_prerolls": [call_target(rva) for rva in next_calls],
        "weighted_picker": call_target(0x00022D4C),
    }
    transfer_checks = {
        "seven_persistent_prerolls": len(next_calls) == 7
        and set(transfers["seven_persistent_prerolls"]) == {0x003E90F0},
        "weighted_picker": transfers["weighted_picker"] == PICK_RVA,
    }
    byte_checks = {
        "repick_countdown_nine": (0x00022651, "c744241409000000"),
        "binary32_cumulative_add": (0x00022683, "f30f584604"),
        "binary32_target_remap": (
            0x0002271B,
            "f30f5cc3f30f5e4604f30f594124",
        ),
        "circular_fallback_next_entry": (0x00022765, "8b55088d5e14"),
        "circular_fallback_wrap": (0x0002276E, "3b5a1c75038b5a18"),
        "local_binary32_pool_threshold": (
            0x00022D3B,
            "660f5ad0f30f5915f09fba00f30f595624",
        ),
        "clear_permanent_removed_bit": (0x00022D64, "8b93ac080000"),
        "clear_attempt_blacklist_bit": (0x00022D7D, "8b93bc080000"),
        "clear_each_entry_stride": (0x00022D89, "83c014"),
        "outer_null_retry_limit_ten": (0x00022DD8, "83f80a"),
        "exhaustion_monstro_id_one": (0x00022DED, "b901000000"),
    }
    instruction_checks = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    pick_hash = hashlib.sha256(read(PICK_RVA, PICK_SIZE)).hexdigest()
    select_hash = hashlib.sha256(read(SELECT_RVA, SELECT_SIZE)).hexdigest()
    actual_hash = hashlib.sha256(payload).hexdigest()
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "function_hashes": pick_hash == PICK_SHA256 and select_hash == SELECT_SHA256,
        "control_transfers": all(transfer_checks.values()),
        "instruction_semantics": all(instruction_checks.values()),
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE read as bytes only; no image loading or execution.",
        "scope": "inherited canonical Basement BossPool repick/fallback/reset path",
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
        "control_transfers": {
            "seven_persistent_prerolls": [
                f"0x{value:08X}"
                for value in transfers["seven_persistent_prerolls"]
            ],
            "weighted_picker": f"0x{transfers['weighted_picker']:08X}",
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
