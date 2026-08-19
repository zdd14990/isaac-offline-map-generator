"""Static verifier for canonical Stage-2 successful lifecycle tail."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256


TAIL_RVA = 0x0033D1D6
TAIL_SIZE = 0x77A
TAIL_SHA256 = "a21990350bea6c0557db4208de080246c67be678171774d8749362a5311c6d37"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    payload = args.pe.read_bytes()
    pe = pefile.PE(data=payload, fast_load=True)

    def read(rva: int, size: int) -> bytes:
        return pe.get_data(rva, size)

    byte_checks = {
        # Both chance draws occur, but descriptor-flag writes require Stage>4
        # and Stage>3 respectively.  Effective Stage 2 takes neither write.
        "first_door_flag_requires_stage_above_four": (0x0033D302, "833b047e5a"),
        "second_door_flag_requires_stage_above_three": (0x0033D3AC, "833b037e3c"),
        "first_flag_bit_write": (0x0033D354, "834c185810"),
        "second_flag_bit_write": (0x0033D3E8, "834c185810"),
        # The fixed -8 descriptor changes only when current RoomConfig stage
        # is 13; canonical Basement II has current stage 1.
        "blue_womb_current_stage_compare": (0x0033D5E8, "83bdd8feffff0d"),
        "canonical_negative_eight": (0x0033D645, "6af8"),
        # The optional -10 descriptor is restricted to StageType 4/5.
        "optional_stage_types_four_five": (0x0033D874, "8b470483f804740983f805"),
        "success_true": (0x0033D94C, "b001"),
    }
    instruction_checks = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    actual_hash = hashlib.sha256(payload).hexdigest()
    tail_hash = hashlib.sha256(read(TAIL_RVA, TAIL_SIZE)).hexdigest()
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "tail_hash": tail_hash == TAIL_SHA256,
        "stage_two_branch_bytes": all(instruction_checks.values()),
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE read as bytes only; no image loading or execution.",
        "scope": "canonical Basement II successful post-layout lifecycle tail",
        "tail_rva": f"0x{TAIL_RVA:08X}",
        "tail_size": TAIL_SIZE,
        "tail_sha256": tail_hash,
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
