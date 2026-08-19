"""Validate extracted STB files and emit a compact room-database index."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from isaacmap.resources import load_stb


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("rooms", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    files = sorted(args.rooms.rglob("*.stb"), key=lambda path: str(path).lower())
    totals = Counter()
    file_records = []
    for path in files:
        payload = path.read_bytes()
        rooms = load_stb(path)
        type_counts = Counter(room.room_type for room in rooms)
        shape_counts = Counter(room.shape for room in rooms)
        difficulty_counts = Counter(room.difficulty for room in rooms)
        totals.update(
            files=1,
            rooms=len(rooms),
            doors=sum(len(room.doors) for room in rooms),
            spawn_positions=sum(len(room.spawns) for room in rooms),
            entity_choices=sum(
                len(spawn.entities) for room in rooms for spawn in room.spawns
            ),
        )
        file_records.append(
            {
                "path": path.relative_to(args.rooms).as_posix(),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size": len(payload),
                "room_count": len(rooms),
                "room_types": dict(sorted(type_counts.items())),
                "room_shapes": dict(sorted(shape_counts.items())),
                "difficulties": dict(sorted(difficulty_counts.items())),
            }
        )

    report = {
        "format": "STB1",
        "totals": dict(totals),
        "files": file_records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["totals"], indent=2))
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
