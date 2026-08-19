"""Verify that both Basement I difficulty windows expose every room shape."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from isaacmap.resources import load_stb


WINDOWS = {"NORMAL": (1, 5), "HARD": (5, 10)}
EXPECTED_SHAPES = tuple(range(1, 13))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stb", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rooms = load_stb(args.stb)
    windows = {}
    matches = True
    for name, (minimum, maximum) in WINDOWS.items():
        eligible = [
            room
            for room in rooms
            if room.room_type == 1
            and room.weight > 0
            and minimum <= room.difficulty <= maximum
        ]
        counts = Counter(room.shape for room in eligible)
        shapes = tuple(sorted(counts))
        window_matches = shapes == EXPECTED_SHAPES
        matches &= window_matches
        windows[name] = {
            "minimum_difficulty": minimum,
            "maximum_difficulty": maximum,
            "positive_weight_default_rooms": len(eligible),
            "shape_counts": dict(sorted(counts.items())),
            "shapes": shapes,
            "all_shapes_1_through_12": window_matches,
        }

    report = {
        "stb": str(args.stb.resolve()),
        "windows": windows,
        "allowed_shapes_mask": "0x00001ffe",
        "matches": matches,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
