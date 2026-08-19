"""Aggregate non-overlapping Basement-II through-Secret shards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCALARS = (
    "comparisons",
    "basement1_attempts",
    "basement1_retrying_seeds",
    "basement2_attempts",
    "basement2_retrying_seeds",
    "secret_missing",
    "secret_boundary",
    "secret_large_neighbor",
    "secret_l_shape_neighbor",
)
MAPS = (
    "secret_neighbor_counts",
    "secret_tie_sizes",
    "blocks_seen",
    "blocks_assigned",
    "accepted_room_type_counts",
    "accepted_room_counts",
    "final_used_bit_sets",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("shards", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inputs = [json.loads(path.read_text(encoding="utf-8")) for path in args.shards]
    first = inputs[0]
    for item in inputs:
        if (
            item["profile_sha256"] != first["profile_sha256"]
            or item["dimensions"] != first["dimensions"]
            or item["scope"] != first["scope"]
            or not item["matches"]
        ):
            raise ValueError("incompatible or failed shard")

    by_difficulty: dict[str, list[dict[str, object]]] = {"NORMAL": [], "HARD": []}
    for item in inputs:
        by_difficulty[item["difficulty"]].append(item)
    report = {
        "profile_sha256": first["profile_sha256"],
        "safety": first["safety"],
        "external_validation": first["external_validation"],
        "scope": first["scope"],
        "dimensions": first["dimensions"],
        "shards": [str(path) for path in args.shards],
        "difficulties": {},
        "total_comparisons": 0,
        "matches": True,
    }
    for difficulty, items in by_difficulty.items():
        if not items:
            raise ValueError(f"missing {difficulty} shards")
        items.sort(key=lambda item: item["seed_range"][0])
        for left, right in zip(items, items[1:]):
            if left["seed_range"][1] + 1 != right["seed_range"][0]:
                raise ValueError(f"{difficulty} shard gap/overlap")
        target: dict[str, object] = {field: 0 for field in SCALARS}
        target.update({field: {} for field in MAPS})
        target["basement2_max_attempts"] = 0
        target["retry_examples"] = []
        for item in items:
            source = item["stats"]
            for field in SCALARS:
                target[field] += source[field]
            target["basement2_max_attempts"] = max(
                target["basement2_max_attempts"], source["basement2_max_attempts"]
            )
            for field in MAPS:
                for key, value in source[field].items():
                    target[field][key] = target[field].get(key, 0) + value
            remaining = 16 - len(target["retry_examples"])
            if remaining > 0:
                target["retry_examples"].extend(source["retry_examples"][:remaining])
        target["seed_range"] = [items[0]["seed_range"][0], items[-1]["seed_range"][1]]
        report["difficulties"][difficulty] = target
        report["total_comparisons"] += target["comparisons"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
