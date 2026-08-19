"""Create a reproducible static fingerprint for a copied Isaac PE."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import pefile


VERSION_MARKERS = (
    b"v1.9.7.17",
    b"Binding of Isaac: Repentance+ v1.9.7.17.J460",
    b"1.9.7.16",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    payload = args.pe.read_bytes()
    pe = pefile.PE(data=payload, fast_load=False)
    timestamp = pe.FILE_HEADER.TimeDateStamp
    markers = {}
    for marker in VERSION_MARKERS:
        offsets = []
        start = 0
        while True:
            offset = payload.find(marker, start)
            if offset < 0:
                break
            offsets.append(offset)
            start = offset + 1
        markers[marker.decode("ascii")] = [f"0x{offset:x}" for offset in offsets]

    report = {
        "path": str(args.pe.resolve()),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size": len(payload),
        "machine": f"0x{pe.FILE_HEADER.Machine:04x}",
        "architecture": "x86" if pe.FILE_HEADER.Machine == 0x14C else "unknown",
        "optional_header_magic": f"0x{pe.OPTIONAL_HEADER.Magic:04x}",
        "image_base": f"0x{pe.OPTIONAL_HEADER.ImageBase:08x}",
        "section_count": pe.FILE_HEADER.NumberOfSections,
        "characteristics": f"0x{pe.FILE_HEADER.Characteristics:04x}",
        "pe_timestamp_raw": f"0x{timestamp:08x}",
        "pe_timestamp_utc": datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
        "windows_file_version": None,
        "windows_product_version": None,
        "ascii_version_markers": markers,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
