"""Offline Basement-II accepted-layout differential; never runs the game."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement2_full_pipeline import generate_basement2_full
from isaacmap.basement2_full_pipeline_reference import generate_basement2_full_reference
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference, PROFILE_SHA256
from isaacmap.post_layout_lifecycle import run_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config import entries_from_definitions
from isaacmap.room_config_reference import entries_from_definitions_reference


DIMENSIONS = (
    "Basement-I lifecycle replay and inherited persistent generation state",
    "all Stage-2 persistent outer-attempt states through M5/M6/M7",
    "late collect order and current-stage ROOM_DEFAULT queries",
    "Level RNG selector seeds and excluded-special advances",
    "RoomConfig candidates, binary32 weights and exact-door selection",
    "accepted descriptor completeness and second BossPool commit boundary",
    "Stage-2 successful lifecycle fixed descriptors and 28-draw handoff",
)


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
    blue_womb = tuple(load_stb(args.resources / "rooms/13.blue womb.stb"))
    lifecycle_entries = (
        entries_from_definitions(special, stage=0)
        + entries_from_definitions(basement, stage=1)
        + entries_from_definitions(blue_womb, stage=13)
    )
    lifecycle_reference_entries = (
        entries_from_definitions_reference(special, stage=0)
        + entries_from_definitions_reference(basement, stage=1)
        + entries_from_definitions_reference(blue_womb, stage=13)
    )
    stats: dict[str, object] = {
        "comparisons": 0,
        "basement1_attempts": 0,
        "basement1_retrying_seeds": 0,
        "basement2_attempts": 0,
        "basement2_retrying_seeds": 0,
        "basement2_max_attempts": 0,
        "abort_operations": {},
        "late_attempts": 0,
        "late_failures": 0,
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
        "accepted_room_type_counts": {},
        "ultra_missing": 0,
        "lifecycle_persistent_level_draws": 0,
        "lifecycle_fixed_descriptor_assignments": 0,
        "lifecycle_private_rng_transitions": 0,
        "lifecycle_missing_configs": 0,
        "retry_examples": [],
    }
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical Basement II complete accepted 13x13 layout plus successful lifecycle handoff",
        "difficulty": args.difficulty,
        "seed_range": [args.start, args.start + args.count - 1],
        "dimensions": list(DIMENSIONS),
        "stats": stats,
        "matches": False,
        "mismatch": None,
    }
    try:
        for seed in range(args.start, args.start + args.count):
            clean = generate_basement2_full(
                seed,
                args.difficulty,
                boss_entries=bosses,
                special_definitions=special,
                basement_definitions=basement,
                blue_womb_definitions=blue_womb,
            )
            reference = generate_basement2_full_reference(
                seed,
                args.difficulty,
                boss_entries=boss_refs,
                special_definitions=special,
                basement_definitions=basement,
                blue_womb_definitions=blue_womb,
            )
            compare_basement1_full(clean, reference)
            if not clean.completed:
                raise AssertionError(f"accepted layout did not complete seed {seed}")
            if len(clean.permanent_removed_bosses) != 2 or clean.pending_boss_blacklist:
                raise AssertionError(f"BossPool commit boundary mismatch seed {seed}")
            if len(clean.rooms) != len(clean.descriptor_configs):
                raise AssertionError(f"accepted map has unconfigured rooms seed {seed}")

            tail = run_post_layout_lifecycle(
                level_rng_state=clean.final_level_rng_state,
                entries=lifecycle_entries,
                room_config_weights=clean.final_room_config_weights,
                special_room_used_bits=clean.final_special_room_used_bits,
                level_stage=2,
            )
            reference_tail = run_post_layout_lifecycle_reference(
                level_rng_state=reference.final_level,
                entries=lifecycle_reference_entries,
                room_config_weights=reference.weights,
                special_room_used_bits=reference.used_bits,
                level_stage=2,
            )
            compare_post_layout_lifecycle(tail, reference_tail)
            stats["lifecycle_persistent_level_draws"] += tail.persistent_level_draw_count
            stats["lifecycle_fixed_descriptor_assignments"] += len(tail.assignments)
            stats["lifecycle_private_rng_transitions"] += sum(
                item.identity != "Level._generationRNG(index=35)"
                for item in tail.rng_transitions
            )
            stats["lifecycle_missing_configs"] += sum(
                item.config is None for item in tail.assignments
            )

            b1_attempts = len(clean.replayed_basement1.layout.attempts)
            stats["comparisons"] += 1
            stats["basement1_attempts"] += b1_attempts
            stats["basement1_retrying_seeds"] += int(b1_attempts > 1)
            stats["basement2_attempts"] += len(clean.attempts)
            stats["basement2_retrying_seeds"] += int(len(clean.attempts) > 1)
            stats["basement2_max_attempts"] = max(
                stats["basement2_max_attempts"], len(clean.attempts)
            )
            for attempt in clean.attempts:
                if attempt.abort_operation is not None:
                    _increment(stats["abort_operations"], attempt.abort_operation)
                late = attempt.late_default
                if late is None:
                    continue
                stats["late_attempts"] += 1
                stats["late_failures"] += int(not late.completed)
                for assignment in late.assignments:
                    stats["ordinary_assignments"] += 1
                    room = late.rooms[assignment.room_id]
                    _increment(stats["ordinary_shapes"], int(room.shape))
                    _increment(stats["minimum_difficulties"], assignment.minimum_difficulty)
                    _increment(stats["required_door_masks"], assignment.required_doors)
                    if assignment.config is not None:
                        _increment(stats["ordinary_variants"], room.variant)
                    if assignment.selection is not None:
                        stats["selector_calls"] += 1
                        stats["selector_internal_draws"] += len(assignment.selection.draws)
                        stats["exact_door_selections"] += int(
                            assignment.selection.used_exact_doors
                        )
                stats["excluded_room_advances"] += late.excluded_room_advance_count
            accepted = clean.attempts[-1]
            stats["ultra_missing"] += int(accepted.through_ultra.ultra_room < 0)
            _increment(stats["accepted_room_counts"], len(clean.rooms))
            for room in clean.rooms:
                _increment(stats["accepted_room_type_counts"], room.room_type)
            if len(clean.attempts) > 1 and len(stats["retry_examples"]) < 16:
                stats["retry_examples"].append(
                    {
                        "seed": seed,
                        "attempts": len(clean.attempts),
                        "aborts": [attempt.abort_operation for attempt in clean.attempts[:-1]],
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
