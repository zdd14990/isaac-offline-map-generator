"""Offline Mines1 (2+) clean/reference differential; never runs the game."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference, PROFILE_SHA256
from isaacmap.mines1_full_pipeline_reference import generate_mines1_full_reference
from isaacmap.mines1_lifecycle import generate_mines1_lifecycle
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config_reference import entries_from_definitions_reference


def _refs(entries) -> tuple[BossPoolEntryReference, ...]:
    return tuple(
        BossPoolEntryReference(
            item.boss_id, item.weight, item.initial_weight, item.achievement, item.alternate_boss_id
        )
        for item in entries
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--count", type=int, default=50)
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

    pools = load_boss_pool_xml(args.resources / "bosspools.xml")
    mines1_bosses = pools["mines"]
    mines1_refs = _refs(mines1_bosses)

    special = tuple(load_stb(args.resources / "rooms/00.special rooms.stb"))
    mines1 = tuple(load_stb(args.resources / "rooms/29.mines.stb"))
    blue_womb = tuple(load_stb(args.resources / "rooms/13.blue womb.stb"))

    tail_ref_entries = (
        entries_from_definitions_reference(special, stage=0)
        + entries_from_definitions_reference(blue_womb, stage=13)
    )

    stats = {
        "comparisons": 0,
        "attempts": 0,
        "retrying_seeds": 0,
        "max_attempts": 0,
        "rng_transitions": 0,
        "room_config_selections": 0,
        "boss_selections": 0,
        "xl_floors": 0,
        "secret_placements": 0,
        "ultra_placements": 0,
        "mismatches": 0,
    }
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "evidence_grade": "PARTIAL_BINARY",
        "validation_corpus": "50 NORMAL + 50 HARD comparisons (intentionally limited)",
        "difficulty": args.difficulty,
        "seed_range": [args.start, args.start + args.count - 1],
        "stats": stats,
        "matches": False,
        "mismatch": None,
    }

    try:
        for seed in range(args.start, args.start + args.count):
            clean = generate_mines1_lifecycle(
                seed,
                args.difficulty,
                mines1_boss_entries=mines1_bosses,
                special_definitions=special,
                mines1_definitions=mines1,
                blue_womb_definitions=blue_womb,
            )

            reference = generate_mines1_full_reference(
                seed,
                args.difficulty,
                mines1_boss_entries=mines1_refs,
                special_definitions=special,
                mines1_definitions=mines1,
            )
            compare_basement1_full(clean.layout, reference)

            reference_tail = run_post_layout_lifecycle_reference(
                level_rng_state=reference.final_level,
                entries=tail_ref_entries,
                room_config_weights=reference.weights,
                special_room_used_bits=reference.used_bits,
                level_stage=3,
                stage_type=4,
                room_config_stage=29,
            )
            compare_post_layout_lifecycle(clean.post_layout, reference_tail)

            stats["comparisons"] += 1
            attempts = len(clean.layout.attempts)
            stats["attempts"] += attempts
            stats["retrying_seeds"] += int(attempts > 1)
            stats["max_attempts"] = max(stats["max_attempts"], attempts)
            stats["rng_transitions"] += len(clean.post_layout.rng_transitions)
            stats["room_config_selections"] += len(clean.post_layout.assignments)
            stats["boss_selections"] += 1
            stats["secret_placements"] += 1
            stats["ultra_placements"] += 1
    except AssertionError as error:
        report["mismatch"] = str(error)
        stats["mismatches"] += 1
    else:
        report["matches"] = True

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
