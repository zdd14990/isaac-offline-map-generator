"""Offline inherited Basement-II BossPool differential; never runs the game."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from isaacmap.basement1_full_pipeline import generate_basement1_full
from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement1_full_pipeline_reference import generate_basement1_full_reference
from isaacmap.boss_pool import BossPoolRuntimeState, load_boss_pool_xml
from isaacmap.boss_pool_differential import compare_runtime_selection
from isaacmap.boss_pool_reference import (
    PROFILE_SHA256,
    BossPoolEntryReference,
    BossPoolRuntimeReference,
)
from isaacmap.resources import load_stb


def _increment(target: dict[str, int], value: object) -> None:
    key = str(value)
    target[key] = target.get(key, 0) + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--difficulty", choices=("NORMAL", "HARD"), required=True)
    parser.add_argument("--pe", type=Path, default=Path("research/input/isaac-ng.exe"))
    parser.add_argument(
        "--resources",
        type=Path,
        default=Path("research/input/extracted_resources/merged/resources"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    actual_hash = hashlib.sha256(args.pe.read_bytes()).hexdigest()
    if actual_hash != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual_hash}")

    bosses = load_boss_pool_xml(args.resources / "bosspools.xml")["basement"]
    boss_refs = tuple(
        BossPoolEntryReference(
            item.boss_id,
            item.weight,
            item.initial_weight,
            item.achievement,
            item.alternate_boss_id,
        )
        for item in bosses
    )
    special = tuple(load_stb(args.resources / "rooms/00.special rooms.stb"))
    basement = tuple(load_stb(args.resources / "rooms/01.basement.stb"))
    stats: dict[str, object] = {
        "comparisons": 0,
        "basement1_total_attempts": 0,
        "basement1_retrying_seeds": 0,
        "basement1_removed_bosses": {},
        "basement2_selected_bosses": {},
        "persistent_rng_draws": 0,
        "local_rng_draws": 0,
        "repick_operations": 0,
        "repicking_seeds": 0,
        "repick_count_distribution": {},
        "fallback_seeds": 0,
        "pool_reset_seeds": 0,
        "fixture_examples": [],
    }
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical Basement II inherited Basement BossPool selection",
        "difficulty": args.difficulty,
        "seed_range": [args.start, args.start + args.count - 1],
        "stats": stats,
        "matches": False,
        "mismatch": None,
    }
    try:
        for seed in range(args.start, args.start + args.count):
            clean_b1 = generate_basement1_full(
                seed,
                args.difficulty,
                boss_entries=bosses,
                special_definitions=special,
                basement_definitions=basement,
            )
            reference_b1 = generate_basement1_full_reference(
                seed,
                args.difficulty,
                boss_entries=boss_refs,
                special_definitions=special,
                basement_definitions=basement,
            )
            compare_basement1_full(clean_b1, reference_b1)
            clean = BossPoolRuntimeState.resume_canonical_basement(
                seed,
                bosses,
                pool_state=clean_b1.final_boss_pool_state,
                removed=clean_b1.permanent_removed_bosses,
            )
            reference = BossPoolRuntimeReference.resume_canonical_basement(
                seed,
                boss_refs,
                pool_state=reference_b1.final_boss,
                removed=reference_b1.removed,
            )
            clean.begin_attempt()
            reference.begin_attempt()
            clean_pick = clean.select_canonical_basement_profile()
            reference_pick = reference.select_canonical_basement_profile()
            compare_runtime_selection(clean_pick, reference_pick)
            if clean.removed != reference.removed:
                raise AssertionError(f"removed set mismatch for seed {seed}")
            if clean.level_blacklist != reference.level_blacklist:
                raise AssertionError(f"blacklist mismatch for seed {seed}")
            if clean_pick.selected_entry_id in clean_b1.permanent_removed_bosses:
                raise AssertionError(f"removed boss reselected for seed {seed}")

            stats["comparisons"] += 1
            stats["basement1_total_attempts"] += len(clean_b1.attempts)
            stats["basement1_retrying_seeds"] += int(len(clean_b1.attempts) > 1)
            _increment(stats["basement1_removed_bosses"], clean_b1.permanent_removed_bosses[0])
            _increment(stats["basement2_selected_bosses"], clean_pick.selected_entry_id)
            stats["persistent_rng_draws"] += 7
            stats["local_rng_draws"] += len(clean_pick.transitions) - 7
            stats["repick_operations"] += clean_pick.repick_count
            stats["repicking_seeds"] += int(clean_pick.repick_count > 0)
            _increment(stats["repick_count_distribution"], clean_pick.repick_count)
            stats["fallback_seeds"] += int(clean_pick.fallback_used)
            stats["pool_reset_seeds"] += int(clean_pick.pool_reset_count > 0)
            if clean_pick.repick_count and len(stats["fixture_examples"]) < 12:
                stats["fixture_examples"].append(
                    {
                        "seed": seed,
                        "basement1_removed": list(clean_b1.permanent_removed_bosses),
                        "basement2_selected": clean_pick.selected_entry_id,
                        "repick_count": clean_pick.repick_count,
                    }
                )
    except AssertionError as error:
        report["mismatch"] = str(error)
    else:
        report["matches"] = True
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
