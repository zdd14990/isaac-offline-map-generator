"""Offline Basement-II through-Secret differential; never runs the game."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from isaacmap.basement1_secret_pipeline_differential import compare_secret_pipeline
from isaacmap.basement2_secret_pipeline import generate_basement2_through_secret
from isaacmap.basement2_secret_pipeline_reference import (
    generate_basement2_through_secret_reference,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference, PROFILE_SHA256
from isaacmap.resources import load_stb


DIMENSIONS = (
    "Basement-I lifecycle replay and inherited persistent generation state",
    "full Stage-2 topology/Boss/Type8/Shop/Treasure attempt state",
    "ordered Stage-2 Treasure-to-Secret block/config/candidate traces",
    "Stage-2 Planetarium binary32 threshold and special-room predicates",
    "Secret forbidden set and all 169 candidate evaluations",
    "Secret descriptor/map/connection mutation and final RNG states",
    "pre-Ultra pending BossPool blacklist remains uncommitted",
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
    actual = hashlib.sha256(args.pe.read_bytes()).hexdigest()
    if actual != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual}")

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
    stats: dict[str, object] = {
        "comparisons": 0,
        "basement1_attempts": 0,
        "basement1_retrying_seeds": 0,
        "basement2_attempts": 0,
        "basement2_retrying_seeds": 0,
        "basement2_max_attempts": 0,
        "secret_missing": 0,
        "secret_boundary": 0,
        "secret_large_neighbor": 0,
        "secret_l_shape_neighbor": 0,
        "secret_neighbor_counts": {},
        "secret_tie_sizes": {},
        "blocks_seen": {},
        "blocks_assigned": {},
        "accepted_room_type_counts": {},
        "accepted_room_counts": {},
        "final_used_bit_sets": {},
        "retry_examples": [],
    }
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical Basement II replay through uncommitted Secret boundary; Ultra and late default variants excluded",
        "difficulty": args.difficulty,
        "seed_range": [args.start, args.start + args.count - 1],
        "dimensions": list(DIMENSIONS),
        "stats": stats,
        "matches": False,
        "mismatch": None,
    }
    try:
        for seed in range(args.start, args.start + args.count):
            clean = generate_basement2_through_secret(
                seed,
                args.difficulty,
                boss_entries=bosses,
                special_definitions=special,
                basement_definitions=basement,
                blue_womb_definitions=blue_womb,
            )
            reference = generate_basement2_through_secret_reference(
                seed,
                args.difficulty,
                boss_entries=boss_refs,
                special_definitions=special,
                basement_definitions=basement,
                blue_womb_definitions=blue_womb,
            )
            compare_secret_pipeline(clean, reference)
            if not clean.boundary_completed:
                raise AssertionError(f"boundary did not complete seed {seed}")
            if not clean.pending_boss_blacklist:
                raise AssertionError(f"current boss was committed early seed {seed}")
            accepted = clean.attempts[-1].through_secret
            if accepted is None or clean.rooms != accepted.rooms:
                raise AssertionError(f"accepted attempt snapshot mismatch seed {seed}")

            b1_attempts = len(clean.replayed_basement1.layout.attempts)
            stats["comparisons"] += 1
            stats["basement1_attempts"] += b1_attempts
            stats["basement1_retrying_seeds"] += int(b1_attempts > 1)
            stats["basement2_attempts"] += len(clean.attempts)
            stats["basement2_retrying_seeds"] += int(len(clean.attempts) > 1)
            stats["basement2_max_attempts"] = max(
                stats["basement2_max_attempts"], len(clean.attempts)
            )
            _increment(stats["accepted_room_counts"], len(clean.rooms))
            for room in clean.rooms:
                _increment(stats["accepted_room_type_counts"], room.room_type)
            for block in accepted.blocks:
                _increment(stats["blocks_seen"], block.operation)
                if block.assigned:
                    _increment(stats["blocks_assigned"], block.operation)
            geometry = accepted.secret_geometry
            if geometry.room_id < 0:
                stats["secret_missing"] += 1
            else:
                evaluation = geometry.evaluations[geometry.grid_index]
                _increment(stats["secret_neighbor_counts"], evaluation.adjacency_count)
                _increment(stats["secret_tie_sizes"], len(geometry.best_candidates))
                x, y = geometry.grid_index % 13, geometry.grid_index // 13
                stats["secret_boundary"] += int(x in (0, 12) or y in (0, 12))
                neighbor_ids = accepted.rooms[geometry.room_id].neighbors
                stats["secret_large_neighbor"] += int(
                    any(int(accepted.rooms[index].shape) in (4, 6, 8) for index in neighbor_ids)
                )
                stats["secret_l_shape_neighbor"] += int(
                    any(int(accepted.rooms[index].shape) in (9, 10, 11, 12) for index in neighbor_ids)
                )
            used = ",".join(map(str, accepted.used_bits_after)) or "none"
            _increment(stats["final_used_bit_sets"], used)
            if len(clean.attempts) > 1 and len(stats["retry_examples"]) < 16:
                stats["retry_examples"].append(
                    {
                        "seed": seed,
                        "attempts": len(clean.attempts),
                        "aborts": [
                            attempt.through_treasure.abort_operation
                            for attempt in clean.attempts
                            if attempt.through_treasure is not None
                            and not attempt.through_treasure.completed
                        ],
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
