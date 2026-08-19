"""Offline full Basement I clean/reference differential; never runs the game."""

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
from isaacmap.resources import load_stb


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
        default=Path("research/binary/basement1_full_differential_report.json"),
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
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical fresh Basement I complete accepted layout",
        "seed_range": [args.start, args.start + args.count - 1],
        "difficulties": {},
        "total_comparisons": 0,
        "dimensions": [
            "all persistent outer-attempt states through M4/M5/M6/M7",
            "late collect order: non-dead ends then remaining dead ends",
            "fixed Start config and ordinary shape/door/difficulty queries",
            "Level RNG selector seeds and excluded-special advances",
            "RoomConfig candidate vectors, exact-door subset and weight decay",
            "late missing-config failure and whole-floor retry",
            "accepted descriptor/config completeness and BossPool commit boundary",
        ],
    }
    difficulties = tuple(args.difficulty) if args.difficulty else ("NORMAL", "HARD")
    try:
        for difficulty in difficulties:
            stats = {
                "comparisons": 0,
                "total_attempts": 0,
                "retrying_seeds": 0,
                "max_attempts": 0,
                "abort_operations": {},
                "late_attempts": 0,
                "late_failures": 0,
                "late_failure_examples": [],
                "ordinary_assignments": 0,
                "ordinary_shapes": {},
                "ordinary_variants": {},
                "minimum_difficulties": {},
                "required_door_masks": {},
                "selector_calls": 0,
                "selector_internal_draws": 0,
                "exact_door_selections": 0,
                "excluded_room_advances": 0,
                "accepted_room_counts": {},
                "ultra_missing": 0,
            }
            for seed in range(args.start, args.start + args.count):
                clean = generate_basement1_full(
                    seed,
                    difficulty,
                    boss_entries=bosses,
                    special_definitions=special,
                    basement_definitions=basement,
                )
                reference = generate_basement1_full_reference(
                    seed,
                    difficulty,
                    boss_entries=boss_refs,
                    special_definitions=special,
                    basement_definitions=basement,
                )
                compare_basement1_full(clean, reference)
                if not clean.completed:
                    raise AssertionError(f"full pipeline did not complete seed {seed}")
                stats["comparisons"] += 1
                stats["total_attempts"] += len(clean.attempts)
                stats["max_attempts"] = max(stats["max_attempts"], len(clean.attempts))
                if len(clean.attempts) > 1:
                    stats["retrying_seeds"] += 1
                for attempt in clean.attempts:
                    if attempt.abort_operation is not None:
                        _increment(stats["abort_operations"], attempt.abort_operation)
                    late = attempt.late_default
                    if late is None:
                        continue
                    stats["late_attempts"] += 1
                    if not late.completed:
                        stats["late_failures"] += 1
                        if len(stats["late_failure_examples"]) < 20:
                            stats["late_failure_examples"].append(
                                {
                                    "seed": seed,
                                    "attempt": attempt.attempt,
                                    "room_id": late.abort_room_id,
                                }
                            )
                    for assignment in late.assignments:
                        stats["ordinary_assignments"] += 1
                        room = late.rooms[assignment.room_id]
                        _increment(stats["ordinary_shapes"], int(room.shape))
                        _increment(stats["minimum_difficulties"], assignment.minimum_difficulty)
                        _increment(stats["required_door_masks"], assignment.required_doors)
                        if assignment.config is not None:
                            _increment(stats["ordinary_variants"], room.variant)
                        selection = assignment.selection
                        if selection is not None:
                            stats["selector_calls"] += 1
                            stats["selector_internal_draws"] += len(selection.draws)
                            stats["exact_door_selections"] += int(selection.used_exact_doors)
                    stats["excluded_room_advances"] += late.excluded_room_advance_count
                accepted = clean.attempts[-1]
                if accepted.through_ultra.ultra_room < 0:
                    stats["ultra_missing"] += 1
                _increment(stats["accepted_room_counts"], len(clean.rooms))
                if len(clean.rooms) != len(clean.descriptor_configs):
                    raise AssertionError("accepted map has unconfigured rooms")
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
