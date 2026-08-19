"""Run large clean/reference topology differential coverage offline."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from isaacmap.floor_init import derive_basement1_topology_inputs
from isaacmap.topology_differential import compare_clean_and_reference
from isaacmap.topology_reference import PROFILE_SHA256


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10_000)
    parser.add_argument(
        "--pe", type=Path, default=Path("research/input/isaac-ng.exe")
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("research/binary/topology_differential_report.json"),
    )
    args = parser.parse_args()
    if args.count <= 0:
        raise ValueError("count must be positive")
    actual_hash = hashlib.sha256(args.pe.read_bytes()).hexdigest()
    if actual_hash != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual_hash}")

    difficulties: dict[str, dict[str, object]] = {}
    all_shapes: set[int] = set()
    total_comparisons = 0
    total_rng_draws = 0
    for difficulty in ("NORMAL", "HARD"):
        aggregate: dict[str, object] = {
            "comparisons": 0,
            "rng_draws": 0,
            "max_rng_draws": 0,
            "boundary_skips": 0,
            "large_draws": 0,
            "large_random_failures": 0,
            "large_random_successes": 0,
            "large_candidates_appended": 0,
            "large_rooms_placed": 0,
            "forced_dead_end_attempts": 0,
            "forced_dead_end_successes": 0,
            "outer_retries": 0,
            "target_room_counts": set(),
            "shapes_placed": set(),
            "example_seeds": {},
        }
        examples: dict[str, int] = aggregate["example_seeds"]  # type: ignore[assignment]
        for start_seed in range(1, args.count + 1):
            inputs = derive_basement1_topology_inputs(start_seed, difficulty)
            reference, summary = compare_clean_and_reference(inputs)
            coverage = reference.coverage
            aggregate["comparisons"] = int(aggregate["comparisons"]) + 1
            aggregate["rng_draws"] = int(aggregate["rng_draws"]) + summary.rng_draw_count
            aggregate["max_rng_draws"] = max(
                int(aggregate["max_rng_draws"]), summary.rng_draw_count
            )
            for key in (
                "boundary_skips",
                "large_draws",
                "large_random_failures",
                "large_random_successes",
                "large_candidates_appended",
                "large_rooms_placed",
                "forced_dead_end_attempts",
                "forced_dead_end_successes",
            ):
                aggregate[key] = int(aggregate[key]) + int(getattr(coverage, key))
            aggregate["outer_retries"] = int(aggregate["outer_retries"]) + summary.retries
            target_counts: set[int] = aggregate["target_room_counts"]  # type: ignore[assignment]
            shape_set: set[int] = aggregate["shapes_placed"]  # type: ignore[assignment]
            target_counts.add(summary.target_room_count)
            shape_set.update(summary.shapes)
            all_shapes.update(summary.shapes)
            if coverage.boundary_skips and "boundary" not in examples:
                examples["boundary"] = start_seed
            if coverage.large_random_failures and "large_gate_failure" not in examples:
                examples["large_gate_failure"] = start_seed
            if coverage.large_rooms_placed and "large_room_placed" not in examples:
                examples["large_room_placed"] = start_seed
            if coverage.forced_dead_end_attempts and "forced_dead_end" not in examples:
                examples["forced_dead_end"] = start_seed
            if summary.retries and "outer_retry" not in examples:
                examples["outer_retry"] = start_seed
            for shape in range(9, 13):
                key = f"shape_{shape}"
                if shape in summary.shapes and key not in examples:
                    examples[key] = start_seed
        aggregate["target_room_counts"] = sorted(aggregate["target_room_counts"])  # type: ignore[arg-type]
        aggregate["shapes_placed"] = sorted(aggregate["shapes_placed"])  # type: ignore[arg-type]
        difficulties[difficulty] = aggregate
        total_comparisons += int(aggregate["comparisons"])
        total_rng_draws += int(aggregate["rng_draws"])

    combined_forced = sum(
        int(value["forced_dead_end_attempts"]) for value in difficulties.values()
    )
    combined_retries = sum(int(value["outer_retries"]) for value in difficulties.values())
    requirements = {
        "normal_covered": int(difficulties["NORMAL"]["comparisons"]) == args.count,
        "hard_covered": int(difficulties["HARD"]["comparisons"]) == args.count,
        "large_success_covered": any(
            int(value["large_rooms_placed"]) > 0 for value in difficulties.values()
        ),
        "large_failure_covered": any(
            int(value["large_random_failures"]) > 0 for value in difficulties.values()
        ),
        "forced_dead_end_covered": combined_forced > 0,
        "all_l_shapes_covered": set(range(9, 13)).issubset(all_shapes),
        "boundary_covered": any(
            int(value["boundary_skips"]) > 0 for value in difficulties.values()
        ),
        # Natural Basement I retries are recorded separately from a targeted
        # retry-schedule unit test; zero is a valid corpus observation.
        "natural_outer_retry_observed": combined_retries > 0,
    }
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "start_seed_range": [1, args.count],
        "total_comparisons": total_comparisons,
        "total_generator_rng_draws_compared": total_rng_draws,
        "difficulties": difficulties,
        "all_shapes_placed": sorted(all_shapes),
        "coverage_requirements": requirements,
        "differential_dimensions": [
            "target room count",
            "room anchors",
            "RoomShape",
            "occupied cells / complete room_map",
            "door masks and connection sets",
            "expansion order",
            "dead-end and non-dead-end order",
            "per-attempt retry/forced-dead-end counts",
            "every generator RNG pre-state and post-state",
            "final generator RNG state",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    required = {key: value for key, value in requirements.items() if key != "natural_outer_retry_observed"}
    return 0 if all(required.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

