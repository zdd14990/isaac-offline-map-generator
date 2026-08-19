"""Offline Basement-II through-Treasure differential; never runs the game."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from isaacmap.basement1_pipeline_differential import compare_pipeline
from isaacmap.basement2_pipeline import generate_basement2_through_treasure
from isaacmap.basement2_pipeline_reference import (
    generate_basement2_through_treasure_reference,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import PROFILE_SHA256, BossPoolEntryReference
from isaacmap.floor_init import derive_basement2_topology_inputs
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
            entry.boss_id,
            entry.weight,
            entry.initial_weight,
            entry.achievement,
            entry.alternate_boss_id,
        )
        for entry in bosses
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
        "curse_masks": {},
        "target_counts": {},
        "abort_operations": {},
        "boss_ids": {},
        "boss_repick_operations": 0,
        "boss_repick_attempts": 0,
        "post_topology_rng_transitions": 0,
        "room_config_selector_calls": 0,
        "candidate_tests": 0,
        "accepted_room_counts": {},
        "pending_bosses": {},
        "retry_examples": [],
    }
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical Basement II replay through uncommitted Treasure boundary",
        "difficulty": args.difficulty,
        "seed_range": [args.start, args.start + args.count - 1],
        "stats": stats,
        "matches": False,
        "mismatch": None,
    }
    try:
        for seed in range(args.start, args.start + args.count):
            clean = generate_basement2_through_treasure(
                seed,
                args.difficulty,
                boss_entries=bosses,
                special_definitions=special,
                basement_definitions=basement,
                blue_womb_definitions=blue_womb,
            )
            reference = generate_basement2_through_treasure_reference(
                seed,
                args.difficulty,
                boss_entries=boss_refs,
                special_definitions=special,
                basement_definitions=basement,
                blue_womb_definitions=blue_womb,
            )
            compare_pipeline(clean, reference)
            if not clean.completed:
                raise AssertionError(f"boundary did not complete seed {seed}")
            if not clean.pending_boss_blacklist:
                raise AssertionError(f"current boss was committed early seed {seed}")

            inputs = derive_basement2_topology_inputs(seed, args.difficulty)
            b1_attempts = len(clean.replayed_basement1.layout.attempts)
            stats["comparisons"] += 1
            stats["basement1_attempts"] += b1_attempts
            stats["basement1_retrying_seeds"] += int(b1_attempts > 1)
            stats["basement2_attempts"] += len(clean.attempts)
            stats["basement2_retrying_seeds"] += int(len(clean.attempts) > 1)
            stats["basement2_max_attempts"] = max(
                stats["basement2_max_attempts"], len(clean.attempts)
            )
            _increment(stats["curse_masks"], inputs.effective_curse_mask)
            _increment(stats["target_counts"], inputs.target_room_count)
            _increment(stats["accepted_room_counts"], len(clean.rooms))
            _increment(stats["pending_bosses"], clean.pending_boss_blacklist[0])
            if len(clean.attempts) > 1 and len(stats["retry_examples"]) < 16:
                stats["retry_examples"].append(
                    {
                        "seed": seed,
                        "attempts": len(clean.attempts),
                        "aborts": [
                            attempt.post_topology.abort_operation
                            for attempt in clean.attempts
                            if attempt.post_topology is not None
                            and not attempt.post_topology.completed
                        ],
                    }
                )
            for attempt in clean.attempts:
                post = attempt.post_topology
                if post is None:
                    _increment(stats["abort_operations"], "Topology unusable")
                    continue
                if post.abort_operation is not None:
                    _increment(stats["abort_operations"], post.abort_operation)
                _increment(stats["boss_ids"], post.boss_selection.selected_entry_id)
                stats["boss_repick_operations"] += post.boss_selection.repick_count
                stats["boss_repick_attempts"] += int(
                    post.boss_selection.repick_count > 0
                )
                stats["post_topology_rng_transitions"] += len(post.rng_draws)
                stats["room_config_selector_calls"] += sum(
                    len(trace.selections) for trace in post.config_traces
                )
                stats["candidate_tests"] += len(post.candidate_traces)
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
