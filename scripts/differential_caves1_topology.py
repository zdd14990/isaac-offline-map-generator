"""Shardable clean/reference differential for canonical Caves-I topology."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from isaacmap.boss_pool_reference import PROFILE_SHA256
from isaacmap.floor_init import derive_caves1_topology_inputs
from isaacmap.floor_init_reference import derive_caves1_topology_inputs_reference
from isaacmap.topology_differential import compare_topology_results
from isaacmap.topology_reference import generate_topology_reference


def _increment(target: dict[str, int], value: object) -> None:
    key = str(value)
    target[key] = target.get(key, 0) + 1


def _entry_signature(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.level_rng_draws,
        value.copied_rng_draws,
        value.curse_rate_denominator,
        value.curse_gate_succeeded,
        value.curse_selector,
        value.effective_curse_mask,
        value.is_xl,
        value.generator_seed,
        value.target_room_count,
        value.required_dead_ends,
        value.allowed_shapes_mask,
        value.room_config_stage,
        value.room_config_min_difficulty,
        value.room_config_max_difficulty,
    )


def _reference_signature(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.level_draws,
        value.copied_draws,
        value.curse_rate,
        value.curse_gate,
        value.curse_selector,
        value.curse_mask,
        value.is_xl,
        value.generator_seed,
        value.target,
        value.dead_ends,
        value.shapes,
        value.room_config_stage,
        value.minimum_difficulty,
        value.maximum_difficulty,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--count", type=int, default=2_500)
    parser.add_argument("--difficulty", choices=("NORMAL", "HARD"), required=True)
    parser.add_argument("--pe", type=Path, default=Path("research/input/isaac-ng.exe"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    actual_hash = hashlib.sha256(args.pe.read_bytes()).hexdigest()
    if actual_hash != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual_hash}")
    end = args.start + args.count - 1
    stats = {
        "comparisons": 0,
        "generator_rng_draws": 0,
        "outer_retries": 0,
        "retrying_seeds": 0,
        "max_retries": 0,
        "curse_gate_successes": 0,
        "xl_floors": 0,
        "xl_exception_draws": 0,
        "curse_masks": {},
        "curse_selector_modulo_six": {},
        "difficulty_windows": {},
        "target_room_counts": {},
        "accepted_room_counts": {},
        "shapes": {},
        "boundary_skips": 0,
        "large_rooms_placed": 0,
        "forced_dead_end_attempts": 0,
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "scope": "canonical base-profile ORIGINAL Caves I topology including natural XL",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "difficulty": args.difficulty,
        "seed_range": [args.start, end],
        "stats": stats,
        "matches": True,
        "mismatch": None,
    }
    try:
        for seed in range(args.start, end + 1):
            inputs = derive_caves1_topology_inputs(seed, args.difficulty)
            reference_inputs = derive_caves1_topology_inputs_reference(
                seed, args.difficulty
            )
            assert _entry_signature(inputs) == _reference_signature(reference_inputs)
            reference = generate_topology_reference(inputs)
            reference, summary = compare_topology_results(inputs, reference)
            coverage = reference.coverage
            stats["comparisons"] += 1
            stats["generator_rng_draws"] += summary.rng_draw_count
            stats["outer_retries"] += summary.retries
            stats["retrying_seeds"] += int(summary.retries > 0)
            stats["max_retries"] = max(stats["max_retries"], summary.retries)
            stats["curse_gate_successes"] += int(inputs.curse_gate_succeeded)
            stats["xl_floors"] += int(inputs.is_xl)
            stats["xl_exception_draws"] += sum(
                draw.control_flow_reason == "XL/Void multi-neighbor exception"
                for draw in reference.generator_rng_ledger
            )
            _increment(stats["curse_masks"], inputs.effective_curse_mask)
            if inputs.curse_selector is not None:
                _increment(
                    stats["curse_selector_modulo_six"],
                    inputs.curse_selector % 6,
                )
            _increment(
                stats["difficulty_windows"],
                f"{inputs.room_config_min_difficulty}..{inputs.room_config_max_difficulty}",
            )
            _increment(stats["target_room_counts"], summary.target_room_count)
            _increment(stats["accepted_room_counts"], summary.room_count)
            for shape in summary.shapes:
                _increment(stats["shapes"], shape)
            stats["boundary_skips"] += coverage.boundary_skips
            stats["large_rooms_placed"] += coverage.large_rooms_placed
            stats["forced_dead_end_attempts"] += coverage.forced_dead_end_attempts
    except AssertionError as error:
        report["matches"] = False
        report["mismatch"] = f"seed {seed}: {error}"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
