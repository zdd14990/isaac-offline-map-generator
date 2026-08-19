"""Aggregate disjoint full-pipeline differential shards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DICT_FIELDS = (
    "abort_operations",
    "ordinary_shapes",
    "ordinary_variants",
    "minimum_difficulties",
    "required_door_masks",
    "accepted_room_counts",
)
SUM_FIELDS = (
    "comparisons",
    "total_attempts",
    "retrying_seeds",
    "late_attempts",
    "late_failures",
    "ordinary_assignments",
    "selector_calls",
    "selector_internal_draws",
    "exact_door_selections",
    "excluded_room_advances",
    "ultra_missing",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    shards = [json.loads(path.read_text(encoding="utf-8")) for path in args.inputs]
    if not shards or any(not item.get("matches") for item in shards):
        raise RuntimeError("all shards must be present and matching")
    first = shards[0]
    report = {
        "profile_sha256": first["profile_sha256"],
        "safety": first["safety"],
        "external_validation": first["external_validation"],
        "scope": first["scope"],
        "shards": len(shards),
        "seed_ranges": [item["seed_range"] for item in shards],
        "dimensions": first["dimensions"],
        "difficulties": {},
        "total_comparisons": 0,
        "mismatch": None,
        "matches": True,
    }
    for difficulty in ("NORMAL", "HARD"):
        combined = {field: 0 for field in SUM_FIELDS}
        combined["max_attempts"] = 0
        combined["late_failure_examples"] = []
        for field in DICT_FIELDS:
            combined[field] = {}
        for shard in shards:
            stats = shard["difficulties"][difficulty]
            for field in SUM_FIELDS:
                combined[field] += stats[field]
            combined["max_attempts"] = max(combined["max_attempts"], stats["max_attempts"])
            combined["late_failure_examples"].extend(stats["late_failure_examples"])
            for field in DICT_FIELDS:
                for key, value in stats[field].items():
                    combined[field][key] = combined[field].get(key, 0) + value
        combined["late_failure_examples"] = combined["late_failure_examples"][:20]
        for field in DICT_FIELDS:
            combined[field] = dict(sorted(combined[field].items(), key=lambda item: int(item[0]) if item[0].lstrip("-").isdigit() else item[0]))
        report["difficulties"][difficulty] = combined
        report["total_comparisons"] += combined["comparisons"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
