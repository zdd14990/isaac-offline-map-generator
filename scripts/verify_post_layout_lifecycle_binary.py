"""Verify static instructions used by the canonical post-layout tail."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256


TAIL_RVA = 0x0033D1D6
TAIL_SIZE = 0x77A
HELPER_RVA = 0x00028940
HELPER_SIZE = 235


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

    helper_calls = (
        0x0033D3FB, 0x0033D456, 0x0033D4B1, 0x0033D50C,
        0x0033D59E, 0x0033D64F, 0x0033D78B, 0x0033D823,
    )
    selector_calls = (
        0x0033D433, 0x0033D48E, 0x0033D4E9, 0x0033D57B,
        0x0033D5D6, 0x0033D687, 0x0033D7C6, 0x0033D85F,
    )
    level_next_calls = (
        0x0033D2B8, 0x0033D363, 0x0033D40C, 0x0033D467,
        0x0033D4C2, 0x0033D554, 0x0033D5AF, 0x0033D660,
        0x0033D731, 0x0033D7E9,
    )
    transfers = {
        "descriptor_seed_helpers": [call_target(rva) for rva in helper_calls],
        "room_config_selectors": [call_target(rva) for rva in selector_calls],
        "level_next_calls": [call_target(rva) for rva in level_next_calls],
    }
    transfer_matches = (
        set(transfers["descriptor_seed_helpers"]) == {0x00028940}
        and set(transfers["room_config_selectors"]) == {0x0042C7D0}
        and set(transfers["level_next_calls"]) == {0x003E90F0}
    )

    byte_checks = {
        "fixed_grid_indices_order": (
            0x0033D3ED,
            "6aff6afe",
        ),
        "error_room_type": (0x0033D42A, "6a0d6a03"),
        "black_market_room_type": (0x0033D485, "6a0d6a16"),
        "dungeon_room_type": (0x0033D4DA, "6a0d"),
        "bossrush_collectible_550": (0x0033D520, "6826020000"),
        "boss_subtype_55": (0x0033D5B4, "6aff6a37"),
        "blue_womb_stage_13": (0x0033D62F, "6a006a0d"),
        "canonical_negative_eight": (0x0033D645, "6af8"),
        "shop_negative_thirteen": (0x0033D779, "6aff6af3"),
        "angel_negative_eighteen": (0x0033D805, "6aee"),
        "optional_stage_types_four_five": (0x0033D874, "8b470483f804740983f805"),
        "optional_negative_ten": (0x0033D8C6, "6aff6af6"),
        "success_true": (0x0033D94C, "b001"),
    }
    byte_results = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    actual_hash = hashlib.sha256(payload).hexdigest()
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "control_transfers": transfer_matches,
        "instruction_constants": all(byte_results.values()),
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE read as bytes only; no image loading or execution.",
        "tail_rva": f"0x{TAIL_RVA:08X}",
        "tail_size": TAIL_SIZE,
        "tail_sha256": hashlib.sha256(read(TAIL_RVA, TAIL_SIZE)).hexdigest(),
        "descriptor_seed_helper_rva": f"0x{HELPER_RVA:08X}",
        "descriptor_seed_helper_size": HELPER_SIZE,
        "descriptor_seed_helper_sha256": hashlib.sha256(
            read(HELPER_RVA, HELPER_SIZE)
        ).hexdigest(),
        "control_transfers": {
            key: [f"0x{value:08X}" for value in values]
            for key, values in transfers.items()
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
