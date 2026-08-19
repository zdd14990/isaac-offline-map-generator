"""Aggregate non-overlapping offline M7 Ultra differential shards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCALAR_FIELDS = (
    "comparisons",
    "total_attempts",
    "retrying_seeds",
    "ultra_missing",
    "ultra_boundary",
    "ultra_diagonal_neighbor",
    "ultra_distance_two_neighbor",
    "ultra_secret_neighbor",
    "ultra_super_secret_neighbor",
    "ultra_large_neighbor",
    "ultra_l_shape_neighbor",
)
MAP_FIELDS = (
    "ultra_neighbor_counts",
    "ultra_tie_sizes",
    "ultra_red_door_write_counts",
    "ultra_config_variants",
    "eligible_candidate_counts",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("shards", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    inputs = [json.loads(path.read_text(encoding="utf-8")) for path in args.shards]
    first = inputs[0]
    for item in inputs:
        if (
            item["profile_sha256"] != first["profile_sha256"]
            or item["dimensions"] != first["dimensions"]
        ):
            raise ValueError("incompatible shard metadata")
    ranges = sorted(tuple(item["seed_range"]) for item in inputs)
    for left, right in zip(ranges, ranges[1:]):
        if left[1] + 1 != right[0]:
            raise ValueError(f"shard gap/overlap: {left}, {right}")
    report = {
        "profile_sha256": first["profile_sha256"],
        "safety": first["safety"],
        "external_validation": first["external_validation"],
        "scope": first["scope"],
        "seed_range": [ranges[0][0], ranges[-1][1]],
        "shards": [str(path) for path in args.shards],
        "difficulties": {},
        "total_comparisons": sum(item["total_comparisons"] for item in inputs),
        "dimensions": first["dimensions"],
    }
    for difficulty in ("NORMAL", "HARD"):
        target = {field: 0 for field in SCALAR_FIELDS}
        target.update({field: {} for field in MAP_FIELDS})
        for item in inputs:
            source = item["difficulties"][difficulty]
            for field in SCALAR_FIELDS:
                target[field] += source[field]
            for field in MAP_FIELDS:
                for key, value in source[field].items():
                    target[field][key] = target[field].get(key, 0) + value
        report["difficulties"][difficulty] = target
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

