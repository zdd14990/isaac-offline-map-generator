"""Aggregate non-overlapping Basement-II accepted-layout shards."""

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
    "late_attempts",
    "late_failures",
    "ordinary_assignments",
    "selector_calls",
    "selector_internal_draws",
    "exact_door_selections",
    "excluded_room_advances",
    "ultra_missing",
    "lifecycle_persistent_level_draws",
    "lifecycle_fixed_descriptor_assignments",
    "lifecycle_private_rng_transitions",
    "lifecycle_missing_configs",
)
MAPS = (
    "abort_operations",
    "ordinary_shapes",
    "ordinary_variants",
    "minimum_difficulties",
    "required_door_masks",
    "accepted_room_counts",
    "accepted_room_type_counts",
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
    grouped = {"NORMAL": [], "HARD": []}
    for item in inputs:
        grouped[item["difficulty"]].append(item)
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
    for difficulty, items in grouped.items():
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
