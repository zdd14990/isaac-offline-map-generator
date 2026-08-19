"""Offline mass differential for the recovered Boss -> RoomType 8 slice."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_differential import compare_fresh_basement_boss
from isaacmap.floor_init import derive_basement1_topology_inputs
from isaacmap.resources import load_stb
from isaacmap.special_rooms import room_configs_from_definitions, run_boss_then_type8
from isaacmap.special_rooms_differential import compare_boss_then_type8
from isaacmap.topology import generate_basement1_topology_research
from isaacmap.topology_reference import PROFILE_SHA256, generate_basement1_topology_reference


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10_000)
    parser.add_argument("--pe", type=Path, default=Path("research/input/isaac-ng.exe"))
    parser.add_argument(
        "--resources",
        type=Path,
        default=Path("research/input/extracted_resources/merged/resources"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("research/binary/special_room_differential_report.json"),
    )
    args = parser.parse_args()
    if args.count <= 0:
        raise ValueError("count must be positive")
    actual_hash = hashlib.sha256(args.pe.read_bytes()).hexdigest()
    if actual_hash != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual_hash}")

    boss_entries = load_boss_pool_xml(args.resources / "bosspools.xml")["basement"]
    definitions = tuple(load_stb(args.resources / "rooms/00.special rooms.stb"))
    configs = room_configs_from_definitions(definitions)
    report: dict[str, object] = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "scope": "fresh vanilla Basement I Boss then RoomType 8 recovered slice",
        "start_seed_range": [1, args.count],
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "difficulties": {},
        "differential_dimensions": [
            "BossPool chained seeds and init-time shuffle",
            "BossPool persistent and local selector RNG states",
            "boss identity and room-config weight mutation",
            "ordered candidate scans and stable erases",
            "room anchors/shapes/type/variant/subtype mutations",
            "complete occupied room map and connections",
            "RoomType 8 selection and candidate-pool side effects",
            "every recovered RNG object transition and final Level RNG state",
        ],
    }
    total = 0
    total_rng_transitions = 0
    difficulties: dict[str, object] = report["difficulties"]  # type: ignore[assignment]

    try:
        for difficulty in ("NORMAL", "HARD"):
            aggregate = {
                "comparisons": 0,
                "boss_ids": set(),
                "boss_room_shapes_before_match": set(),
                "type8_counts": set(),
                "completed": 0,
                "boss_aborts": 0,
                "type8_aborts": 0,
                "candidate_tests": 0,
                "rng_transitions": 0,
                "final_level_rng_states": set(),
            }
            for game_start_seed in range(1, args.count + 1):
                inputs = derive_basement1_topology_inputs(game_start_seed, difficulty)
                clean_topology = generate_basement1_topology_research(inputs)
                reference_topology = generate_basement1_topology_reference(inputs)
                compare_fresh_basement_boss(game_start_seed, boss_entries)
                compare_boss_then_type8(
                    clean_topology,
                    reference_topology,
                    game_start_seed=game_start_seed,
                    level_rng_state=inputs.generator_seed,
                    boss_entries=boss_entries,
                    special_definitions=definitions,
                )
                result = run_boss_then_type8(
                    clean_topology,
                    game_start_seed=game_start_seed,
                    level_rng_state=inputs.generator_seed,
                    boss_entries=boss_entries,
                    special_configs=configs,
                )
                aggregate["comparisons"] += 1
                aggregate["boss_ids"].add(result.boss.boss_id)
                aggregate["type8_counts"].add(len(result.type8_rooms))
                if result.completed:
                    aggregate["completed"] += 1
                elif result.abort_operation == "Boss":
                    aggregate["boss_aborts"] += 1
                elif result.abort_operation == "RoomType8":
                    aggregate["type8_aborts"] += 1
                aggregate["candidate_tests"] += len(result.candidate_trace)
                aggregate["rng_transitions"] += len(result.rng_trace) + len(result.boss.transitions)
                aggregate["final_level_rng_states"].add(result.final_level_rng_state)
            total += aggregate["comparisons"]
            total_rng_transitions += aggregate["rng_transitions"]
            difficulties[difficulty] = {
                "comparisons": aggregate["comparisons"],
                "boss_ids": sorted(aggregate["boss_ids"]),
                "type8_counts": sorted(aggregate["type8_counts"]),
                "completed": aggregate["completed"],
                "boss_aborts": aggregate["boss_aborts"],
                "type8_aborts": aggregate["type8_aborts"],
                "candidate_tests": aggregate["candidate_tests"],
                "rng_transitions": aggregate["rng_transitions"],
                "distinct_final_level_rng_states": len(aggregate["final_level_rng_states"]),
            }
    except Exception as error:
        print(
            f"minimal differential reproduction: difficulty={difficulty} "
            f"start_seed=0x{game_start_seed:08X}",
            file=sys.stderr,
        )
        raise error

    report["total_comparisons"] = total
    report["total_rng_transitions_compared"] = total_rng_transitions
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
