"""Aggregate disjoint Basement I lifecycle differential shards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DICT_FIELDS = (
    "fixed_grid_indices",
    "fixed_room_types",
    "selected_resource_indices",
    "selected_variants",
    "final_used_bit_sets",
)
SUM_FIELDS = (
    "comparisons",
    "total_layout_attempts",
    "retrying_seeds",
    "persistent_level_draws",
    "fixed_descriptor_assignments",
    "missing_configs",
    "private_rng_transitions",
)


def _sort_key(item: tuple[str, int]) -> tuple[int, object]:
    key = item[0]
    return (0, int(key)) if key.lstrip("-").isdigit() else (1, key)


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
        combined["max_layout_attempts"] = 0
        for field in DICT_FIELDS:
            combined[field] = {}
        for shard in shards:
            stats = shard["difficulties"][difficulty]
            for field in SUM_FIELDS:
                combined[field] += stats[field]
            combined["max_layout_attempts"] = max(
                combined["max_layout_attempts"], stats["max_layout_attempts"]
            )
            for field in DICT_FIELDS:
                for key, value in stats[field].items():
                    combined[field][key] = combined[field].get(key, 0) + value
        for field in DICT_FIELDS:
            combined[field] = dict(sorted(combined[field].items(), key=_sort_key))
        report["difficulties"][difficulty] = combined
        report["total_comparisons"] += combined["comparisons"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
