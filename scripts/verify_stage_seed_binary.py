"""Verify constants used by Seeds::set_start_seed in a copied executable."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct

import pefile


SEQUENCE_SHIFTS_RVA = 0x0071F60C
EXPECTED_SEQUENCE_SHIFTS = (3, 23, 25)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    payload = args.pe.read_bytes()
    pe = pefile.PE(data=payload, fast_load=True)
    offset = pe.get_offset_from_rva(SEQUENCE_SHIFTS_RVA)
    shifts = struct.unpack_from("<3I", payload, offset)
    report = {
        "pe": str(args.pe.resolve()),
        "set_start_seed_rva": "0x005eb880",
        "sequence_shifts_rva": f"0x{SEQUENCE_SHIFTS_RVA:08x}",
        "sequence_shifts": shifts,
        "expected": EXPECTED_SEQUENCE_SHIFTS,
        "matches": shifts == EXPECTED_SEQUENCE_SHIFTS,
        "stage_seed_count_from_loop_immediate": 14,
        "player_init_draws_after_stage_loop": 1,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
