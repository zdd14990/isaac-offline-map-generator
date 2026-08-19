"""Aggregate non-overlapping Caves-I topology differential shards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SCALARS = (
    "comparisons",
    "generator_rng_draws",
    "outer_retries",
    "retrying_seeds",
    "curse_gate_successes",
    "xl_floors",
    "xl_exception_draws",
    "boundary_skips",
    "large_rooms_placed",
    "forced_dead_end_attempts",
)
MAPS = (
    "curse_masks",
    "curse_selector_modulo_six",
    "difficulty_windows",
    "target_room_counts",
    "accepted_room_counts",
    "shapes",
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
        "scope": first["scope"],
        "external_validation": first["external_validation"],
        "shards": [str(path) for path in args.shards],
        "difficulties": {},
        "total_comparisons": 0,
        "total_generator_rng_draws": 0,
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
        target["max_retries"] = 0
        for item in items:
            source = item["stats"]
            for field in SCALARS:
                target[field] += source[field]
            target["max_retries"] = max(target["max_retries"], source["max_retries"])
            for field in MAPS:
                for key, value in source[field].items():
                    target[field][key] = target[field].get(key, 0) + value
        target["seed_range"] = [items[0]["seed_range"][0], items[-1]["seed_range"][1]]
        report["difficulties"][difficulty] = target
        report["total_comparisons"] += target["comparisons"]
        report["total_generator_rng_draws"] += target["generator_rng_draws"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
