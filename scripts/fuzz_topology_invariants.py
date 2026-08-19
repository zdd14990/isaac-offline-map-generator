"""Exercise the research topology port without treating it as a game oracle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from isaacmap.floor_init import derive_basement1_topology_inputs
from isaacmap.topology import generate_basement1_topology_research
from isaacmap.topology_geometry import occupied_cells


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=1000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.seeds < 1:
        raise SystemExit("--seeds must be positive")

    max_rooms = 0
    max_retries = 0
    large_rooms = 0
    for start_seed in range(1, args.seeds + 1):
        for difficulty in ("NORMAL", "HARD"):
            inputs = derive_basement1_topology_inputs(start_seed, difficulty)
            result = generate_basement1_topology_research(inputs)
            if result.rooms[0].grid_index != 84 or len(result.dead_ends) < 5:
                raise AssertionError("start-room/dead-end invariant failed")
            seen: set[tuple[int, int]] = set()
            for room in result.rooms:
                for cell in occupied_cells(room.column, room.line, room.shape):
                    if not (0 <= cell[0] < 13 and 0 <= cell[1] < 13):
                        raise AssertionError("out-of-bounds occupied cell")
                    if cell in seen:
                        raise AssertionError("overlapping occupied cell")
                    seen.add(cell)
            max_rooms = max(max_rooms, len(result.rooms))
            max_retries = max(max_retries, result.retries)
            large_rooms += sum(room.shape > 3 for room in result.rooms)

    report = {
        "status": "INVARIANTS_ONLY_NOT_AN_ORACLE",
        "seed_range": [1, args.seeds],
        "difficulties": ["NORMAL", "HARD"],
        "runs": args.seeds * 2,
        "max_rooms": max_rooms,
        "max_retries": max_retries,
        "large_rooms": large_rooms,
        "checks": [
            "start_grid_index_84",
            "at_least_five_dead_ends",
            "occupied_cells_in_13x13",
            "no_occupied_cell_overlap",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
