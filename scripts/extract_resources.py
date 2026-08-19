"""Extract named XML/STB resources with the static Python archive reader."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from isaacmap.resources import extract_resource_layers, relevant_filelist_entries


# This order matches the observed official ResourceExtractor enumeration for
# these selected archives. Later archives overwrite earlier logical paths.
ARCHIVE_ORDER = ("repentance.a", "config.a", "rooms.a", "afterbirth.a", "afterbirthp.a")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("game", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    filelist = args.game / "tools" / "ResourceExtractor" / "filelist.txt"
    packed = args.game / "resources" / "packed"
    logical_paths = relevant_filelist_entries(filelist)
    archives = [packed / name for name in ARCHIVE_ORDER]
    records = extract_resource_layers(archives, logical_paths, args.output)

    index_path = args.output / "resource_index.csv"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=("logical_path", "archive", "size", "output_path")
        )
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "logical_path": record.logical_path,
                    "archive": record.archive,
                    "size": record.size,
                    "output_path": str(record.output_path.resolve()),
                }
            )

    merged_files = sum(1 for path in (args.output / "merged").rglob("*") if path.is_file())
    print(f"Named XML/STB paths: {len(logical_paths)}")
    print(f"Extracted archive-layer records: {len(records)}")
    print(f"Merged files: {merged_files}")
    print(f"Index: {index_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

