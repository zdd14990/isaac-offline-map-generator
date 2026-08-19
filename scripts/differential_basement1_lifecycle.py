"""Offline Basement I layout/lifecycle differential; never runs the game."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from isaacmap.basement1_full_pipeline import generate_basement1_full
from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement1_full_pipeline_reference import (
    generate_basement1_full_reference,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference, PROFILE_SHA256
from isaacmap.post_layout_lifecycle import run_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_differential import (
    compare_post_layout_lifecycle,
)
from isaacmap.post_layout_lifecycle_reference import (
    run_post_layout_lifecycle_reference,
)
from isaacmap.resources import load_stb
from isaacmap.room_config import entries_from_definitions
from isaacmap.room_config_reference import entries_from_definitions_reference


def _increment(target: dict[str, int], value: object) -> None:
    key = str(value)
    target[key] = target.get(key, 0) + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--count", type=int, default=10_000)
    parser.add_argument("--difficulty", action="append", choices=("NORMAL", "HARD"))
    parser.add_argument("--pe", type=Path, default=Path("research/input/isaac-ng.exe"))
    parser.add_argument(
        "--resources",
        type=Path,
        default=Path("research/input/extracted_resources/merged/resources"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("research/binary/basement1_lifecycle_differential_report.json"),
    )
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
    blue_womb = tuple(load_stb(args.resources / "rooms/13.blue womb.stb"))
    clean_entries = (
        entries_from_definitions(special, stage=0)
        + entries_from_definitions(basement, stage=1)
        + entries_from_definitions(blue_womb, stage=13)
    )
    reference_entries = (
        entries_from_definitions_reference(special, stage=0)
        + entries_from_definitions_reference(basement, stage=1)
        + entries_from_definitions_reference(blue_womb, stage=13)
    )
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical fresh Basement I accepted layout plus post-layout lifecycle handoff",
        "seed_range": [args.start, args.start + args.count - 1],
        "difficulties": {},
        "total_comparisons": 0,
        "dimensions": [
            "complete accepted Basement I layout clean/reference equality",
            "two persistent Level RNG probability draws and binary32 arithmetic",
            "six fixed negative descriptors on the persistent Level RNG",
            "private Shop index-19 and Angel index-20 RNG streams",
            "descriptor seed helper and derived index-66 seed",
            "eight RoomConfig selections and persistent weight mutations",
            "28-draw persistent Level RNG handoff to the next floor",
            "special-room used-bit clearing and optional-descriptor skips",
        ],
    }
    difficulties = tuple(args.difficulty) if args.difficulty else ("NORMAL", "HARD")
    try:
        for difficulty in difficulties:
            stats = {
                "comparisons": 0,
                "total_layout_attempts": 0,
                "retrying_seeds": 0,
                "max_layout_attempts": 0,
                "persistent_level_draws": 0,
                "fixed_descriptor_assignments": 0,
                "fixed_grid_indices": {},
                "fixed_room_types": {},
                "selected_resource_indices": {},
                "selected_variants": {},
                "final_used_bit_sets": {},
                "missing_configs": 0,
                "private_rng_transitions": 0,
            }
            for seed in range(args.start, args.start + args.count):
                clean_layout = generate_basement1_full(
                    seed,
                    difficulty,
                    boss_entries=bosses,
                    special_definitions=special,
                    basement_definitions=basement,
                )
                reference_layout = generate_basement1_full_reference(
                    seed,
                    difficulty,
                    boss_entries=boss_refs,
                    special_definitions=special,
                    basement_definitions=basement,
                )
                compare_basement1_full(clean_layout, reference_layout)
                if not clean_layout.completed:
                    raise AssertionError(f"full pipeline did not complete seed {seed}")

                clean = run_post_layout_lifecycle(
                    level_rng_state=clean_layout.final_level_rng_state,
                    entries=clean_entries,
                    room_config_weights=clean_layout.final_room_config_weights,
                    special_room_used_bits=clean_layout.final_special_room_used_bits,
                )
                reference = run_post_layout_lifecycle_reference(
                    level_rng_state=reference_layout.final_level,
                    entries=reference_entries,
                    room_config_weights=reference_layout.weights,
                    special_room_used_bits=reference_layout.used_bits,
                )
                compare_post_layout_lifecycle(clean, reference)

                stats["comparisons"] += 1
                stats["total_layout_attempts"] += len(clean_layout.attempts)
                stats["max_layout_attempts"] = max(
                    stats["max_layout_attempts"], len(clean_layout.attempts)
                )
                stats["retrying_seeds"] += int(len(clean_layout.attempts) > 1)
                stats["persistent_level_draws"] += clean.persistent_level_draw_count
                stats["fixed_descriptor_assignments"] += len(clean.assignments)
                stats["private_rng_transitions"] += sum(
                    item.identity != "Level._generationRNG(index=35)"
                    for item in clean.rng_transitions
                )
                _increment(
                    stats["final_used_bit_sets"], clean.final_special_room_used_bits
                )
                for assignment in clean.assignments:
                    _increment(stats["fixed_grid_indices"], assignment.grid_index)
                    _increment(stats["fixed_room_types"], assignment.room_type)
                    if assignment.config is None:
                        stats["missing_configs"] += 1
                        continue
                    _increment(
                        stats["selected_resource_indices"],
                        assignment.config.resource_index,
                    )
                    selected = assignment.selection.entry
                    if selected is None:
                        raise AssertionError("assignment config has no selected entry")
                    _increment(stats["selected_variants"], selected.variant)
            report["difficulties"][difficulty] = stats
            report["total_comparisons"] += stats["comparisons"]
    except AssertionError as error:
        report["mismatch"] = str(error)
        report["matches"] = False
    else:
        report["mismatch"] = None
        report["matches"] = True
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
