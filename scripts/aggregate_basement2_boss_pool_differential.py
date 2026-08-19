"""Aggregate disjoint Basement-II BossPool differential shards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


MAP_KEYS = (
    "basement1_removed_bosses",
    "basement2_selected_bosses",
    "repick_count_distribution",
)
COUNT_KEYS = (
    "comparisons",
    "basement1_total_attempts",
    "basement1_retrying_seeds",
    "persistent_rng_draws",
    "local_rng_draws",
    "repick_operations",
    "repicking_seeds",
    "fallback_seeds",
    "pool_reset_seeds",
)


def _merge_counts(target: dict[str, int], source: dict[str, int]) -> None:
    for key, value in source.items():
        target[key] = target.get(key, 0) + value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    shards = [json.loads(path.read_text(encoding="utf-8")) for path in args.inputs]
    by_difficulty: dict[str, dict[str, object]] = {}
    for shard in shards:
        difficulty = shard["difficulty"]
        aggregate = by_difficulty.setdefault(
            difficulty,
            {
                **{key: 0 for key in COUNT_KEYS},
                **{key: {} for key in MAP_KEYS},
                "fixture_examples": [],
                "seed_ranges": [],
            },
        )
        aggregate["seed_ranges"].append(shard["seed_range"])
        stats = shard["stats"]
        for key in COUNT_KEYS:
            aggregate[key] += stats[key]
        for key in MAP_KEYS:
            _merge_counts(aggregate[key], stats[key])
        aggregate["fixture_examples"].extend(stats["fixture_examples"])
        aggregate["fixture_examples"] = aggregate["fixture_examples"][:20]

    report = {
        "profile_sha256": shards[0]["profile_sha256"],
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical Basement II inherited Basement BossPool selection",
        "total_comparisons": sum(
            data["comparisons"] for data in by_difficulty.values()
        ),
        "difficulties": by_difficulty,
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
