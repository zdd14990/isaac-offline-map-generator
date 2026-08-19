"""Mass clean/reference differential for canonical Basement II topology."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from isaacmap.boss_pool_reference import PROFILE_SHA256
from isaacmap.floor_init import derive_basement2_topology_inputs
from isaacmap.floor_init_reference import derive_basement2_topology_inputs_reference
from isaacmap.topology_differential import compare_topology_results
from isaacmap.topology_reference import generate_topology_reference


def _increment(target: dict[str, int], value: object) -> None:
    key = str(value)
    target[key] = target.get(key, 0) + 1


def _compare_entry(clean, reference) -> None:
    assert (
        clean.stage_seed,
        clean.level_rng_draws,
        clean.copied_rng_draws,
        clean.curse_rate_denominator,
        clean.curse_gate_succeeded,
        clean.curse_selector,
        clean.effective_curse_mask,
        clean.generator_seed,
        clean.target_room_count,
        clean.required_dead_ends,
        clean.allowed_shapes_mask,
        clean.room_config_min_difficulty,
        clean.room_config_max_difficulty,
    ) == (
        reference.stage_seed,
        reference.level_draws,
        reference.copied_draws,
        reference.curse_rate,
        reference.curse_gate,
        reference.curse_selector,
        reference.curse_mask,
        reference.generator_seed,
        reference.target,
        reference.dead_ends,
        reference.shapes,
        reference.minimum_difficulty,
        reference.maximum_difficulty,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10_000)
    parser.add_argument("--pe", type=Path, default=Path("research/input/isaac-ng.exe"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("research/binary/basement2_topology_differential_report.json"),
    )
    args = parser.parse_args()
    actual_hash = hashlib.sha256(args.pe.read_bytes()).hexdigest()
    if actual_hash != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual_hash}")

    report = {
        "profile_sha256": actual_hash,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "scope": "canonical base-profile ORIGINAL Basement II topology",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "seed_range": [1, args.count],
        "difficulties": {},
        "total_comparisons": 0,
        "total_generator_rng_draws": 0,
        "matches": True,
        "mismatch": None,
    }
    try:
        for difficulty in ("NORMAL", "HARD"):
            stats = {
                "comparisons": 0,
                "generator_rng_draws": 0,
                "outer_retries": 0,
                "retrying_seeds": 0,
                "max_retries": 0,
                "curse_gate_successes": 0,
                "curse_masks": {},
                "curse_selector_modulo_six": {},
                "target_room_counts": {},
                "accepted_room_counts": {},
                "shapes": {},
                "boundary_skips": 0,
                "large_rooms_placed": 0,
                "forced_dead_end_attempts": 0,
            }
            for seed in range(1, args.count + 1):
                inputs = derive_basement2_topology_inputs(seed, difficulty)
                reference_inputs = derive_basement2_topology_inputs_reference(
                    seed, difficulty
                )
                _compare_entry(inputs, reference_inputs)
                reference = generate_topology_reference(inputs)
                reference, summary = compare_topology_results(inputs, reference)
                coverage = reference.coverage
                stats["comparisons"] += 1
                stats["generator_rng_draws"] += summary.rng_draw_count
                stats["outer_retries"] += summary.retries
                stats["retrying_seeds"] += int(summary.retries > 0)
                stats["max_retries"] = max(stats["max_retries"], summary.retries)
                stats["curse_gate_successes"] += int(inputs.curse_gate_succeeded)
                _increment(stats["curse_masks"], inputs.effective_curse_mask)
                if inputs.curse_selector is not None:
                    _increment(
                        stats["curse_selector_modulo_six"],
                        inputs.curse_selector % 6,
                    )
                _increment(stats["target_room_counts"], summary.target_room_count)
                _increment(stats["accepted_room_counts"], summary.room_count)
                for shape in summary.shapes:
                    _increment(stats["shapes"], shape)
                stats["boundary_skips"] += coverage.boundary_skips
                stats["large_rooms_placed"] += coverage.large_rooms_placed
                stats["forced_dead_end_attempts"] += coverage.forced_dead_end_attempts
            report["difficulties"][difficulty] = stats
            report["total_comparisons"] += stats["comparisons"]
            report["total_generator_rng_draws"] += stats["generator_rng_draws"]
    except AssertionError as error:
        report["matches"] = False
        report["mismatch"] = str(error)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
