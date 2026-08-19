"""Statically compare RNG constants in a copied PE with the Python profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import struct

import pefile

from isaacmap.rng import RNG_SHIFT_TRIPLES


IMAGE_BASE_EXPECTED = 0x00400000
SHIFT_TABLE_RVA = 0x0071F4C8
RANDOM_FLOAT_CORRECTION_RVA = 0x007ACB00
RANDOM_FLOAT_SCALE_RVA = 0x007A9FF0
RANDOM_FLOAT_SCALE_BITS = 0x2F7FFFFE


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    payload = args.pe.read_bytes()
    pe = pefile.PE(data=payload, fast_load=True)
    if pe.OPTIONAL_HEADER.ImageBase != IMAGE_BASE_EXPECTED:
        raise SystemExit(f"unexpected image base: 0x{pe.OPTIONAL_HEADER.ImageBase:x}")

    table_offset = pe.get_offset_from_rva(SHIFT_TABLE_RVA)
    flat = struct.unpack_from("<243I", payload, table_offset)
    binary_table = tuple(tuple(flat[index:index + 3]) for index in range(0, 243, 3))
    table_matches = binary_table == RNG_SHIFT_TRIPLES

    correction_offset = pe.get_offset_from_rva(RANDOM_FLOAT_CORRECTION_RVA)
    corrections = struct.unpack_from("<2d", payload, correction_offset)
    scale_offset = pe.get_offset_from_rva(RANDOM_FLOAT_SCALE_RVA)
    (scale_bits,) = struct.unpack_from("<I", payload, scale_offset)
    (scale,) = struct.unpack("<f", struct.pack("<I", scale_bits))

    report = {
        "pe": str(args.pe.resolve()),
        "image_base": pe.OPTIONAL_HEADER.ImageBase,
        "shift_table_rva": SHIFT_TABLE_RVA,
        "shift_triples": len(binary_table),
        "shift_table_matches_python": table_matches,
        "random_float_correction_rva": RANDOM_FLOAT_CORRECTION_RVA,
        "random_float_corrections": corrections,
        "random_float_scale_rva": RANDOM_FLOAT_SCALE_RVA,
        "random_float_scale_bits": f"0x{scale_bits:08x}",
        "random_float_scale": scale,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if (
        table_matches
        and corrections == (0.0, 4294967296.0)
        and scale_bits == RANDOM_FLOAT_SCALE_BITS
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
