"""Aggregate disjoint Basement-II through-Treasure shards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


MAP_KEYS = (
    "curse_masks",
    "target_counts",
    "abort_operations",
    "boss_ids",
    "accepted_room_counts",
    "pending_bosses",
)
COUNT_KEYS = (
    "comparisons",
    "basement1_attempts",
    "basement1_retrying_seeds",
    "basement2_attempts",
    "basement2_retrying_seeds",
    "boss_repick_operations",
    "boss_repick_attempts",
    "post_topology_rng_transitions",
    "room_config_selector_calls",
    "candidate_tests",
)


def _merge(target: dict[str, int], source: dict[str, int]) -> None:
    for key, value in source.items():
        target[key] = target.get(key, 0) + value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    shards = [json.loads(path.read_text(encoding="utf-8")) for path in args.inputs]
    difficulties: dict[str, dict[str, object]] = {}
    for shard in shards:
        aggregate = difficulties.setdefault(
            shard["difficulty"],
            {
                **{key: 0 for key in COUNT_KEYS},
                **{key: {} for key in MAP_KEYS},
                "basement2_max_attempts": 0,
                "retry_examples": [],
                "seed_ranges": [],
            },
        )
        stats = shard["stats"]
        for key in COUNT_KEYS:
            aggregate[key] += stats[key]
        for key in MAP_KEYS:
            _merge(aggregate[key], stats[key])
        aggregate["basement2_max_attempts"] = max(
            aggregate["basement2_max_attempts"], stats["basement2_max_attempts"]
        )
        aggregate["retry_examples"].extend(stats["retry_examples"])
        aggregate["retry_examples"] = aggregate["retry_examples"][:24]
        aggregate["seed_ranges"].append(shard["seed_range"])
    report = {
        "profile_sha256": shards[0]["profile_sha256"],
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical Basement II replay through uncommitted Treasure boundary",
        "total_comparisons": sum(
            item["comparisons"] for item in difficulties.values()
        ),
        "difficulties": difficulties,
        "source_shards": [str(path) for path in args.inputs],
        "matches": all(shard["matches"] for shard in shards),
        "mismatch": next(
            (shard["mismatch"] for shard in shards if shard["mismatch"]), None
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
