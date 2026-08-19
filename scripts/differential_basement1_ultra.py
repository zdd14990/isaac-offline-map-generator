"""20k-seed offline M7 Ultra differential; the game is never executed."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from isaacmap.basement1_ultra_pipeline import generate_basement1_through_ultra
from isaacmap.basement1_ultra_pipeline_differential import compare_ultra_pipeline
from isaacmap.basement1_ultra_pipeline_reference import (
    generate_basement1_through_ultra_reference,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference, PROFILE_SHA256
from isaacmap.resources import load_stb


def _increment(target: dict[str, int], key: object) -> None:
    text = str(key)
    target[text] = target.get(text, 0) + 1


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
        default=Path("research/binary/basement1_ultra_differential_report.json"),
    )
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
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical fresh Basement I through Ultra; late default variants excluded",
        "seed_range": [args.start, args.start + args.count - 1],
        "difficulties": {},
        "total_comparisons": 0,
        "dimensions": [
            "full M4/M5/M6 attempt state and persistent owners",
            "index-71 Ultra RoomConfig seed derivation and index-7 selector draws",
            "red-door exclusion set from every configured descriptor and door slot",
            "all 169 Ultra candidate evaluations in stable scan order",
            "immediate-cell rejection, ordered outer-ring neighbors and door compatibility",
            "persistent index-35 candidate/tie RNG transitions",
            "type-29 1x1 descriptor/map mutation and red-door bit writes",
            "Ultra null result continues without floor retry",
            "pre-late pending BossPool blacklist remains uncommitted",
        ],
    }

    selected_difficulties = tuple(args.difficulty) if args.difficulty else ("NORMAL", "HARD")
    try:
        for difficulty in selected_difficulties:
            stats = {
                "comparisons": 0,
                "total_attempts": 0,
                "retrying_seeds": 0,
                "ultra_missing": 0,
                "ultra_boundary": 0,
                "ultra_diagonal_neighbor": 0,
                "ultra_distance_two_neighbor": 0,
                "ultra_secret_neighbor": 0,
                "ultra_super_secret_neighbor": 0,
                "ultra_large_neighbor": 0,
                "ultra_l_shape_neighbor": 0,
                "ultra_neighbor_counts": {},
                "ultra_tie_sizes": {},
                "ultra_red_door_write_counts": {},
                "ultra_config_variants": {},
                "eligible_candidate_counts": {},
            }
            for seed in range(args.start, args.start + args.count):
                clean = generate_basement1_through_ultra(
                    seed,
                    difficulty,
                    boss_entries=bosses,
                    special_definitions=special,
                    basement_definitions=basement,
                )
                reference = generate_basement1_through_ultra_reference(
                    seed,
                    difficulty,
                    boss_entries=boss_refs,
                    special_definitions=special,
                    basement_definitions=basement,
                )
                compare_ultra_pipeline(clean, reference)
                stats["comparisons"] += 1
                attempts = clean.through_secret.attempts
                stats["total_attempts"] += len(attempts)
                if len(attempts) > 1:
                    stats["retrying_seeds"] += 1
                final = clean.final
                if final is None:
                    continue
                geometry = final.ultra_geometry
                _increment(stats["eligible_candidate_counts"], len(geometry.rng_transitions) - (1 if geometry.best_candidates else 0))
                _increment(stats["ultra_tie_sizes"], len(geometry.best_candidates))
                _increment(stats["ultra_red_door_write_counts"], len(geometry.red_door_writes))
                if final.ultra_room >= 0:
                    _increment(stats["ultra_config_variants"], final.rooms[final.ultra_room].variant)
                if geometry.room_id < 0:
                    stats["ultra_missing"] += 1
                    continue

                evaluation = geometry.evaluations[geometry.grid_index]
                _increment(stats["ultra_neighbor_counts"], evaluation.adjacency_count)
                x, y = geometry.grid_index % 13, geometry.grid_index // 13
                if x in (0, 12) or y in (0, 12):
                    stats["ultra_boundary"] += 1
                pre = attempts[-1].through_secret
                if pre is None:
                    continue
                neighbor_ids: list[int] = []
                for position, (dx, dy) in enumerate((
                    (-2, 0), (-1, -1), (0, -2), (1, -1),
                    (2, 0), (1, 1), (0, 2), (-1, 1),
                )):
                    if evaluation.outer_neighbor_mask & (1 << position) == 0:
                        continue
                    index = (y + dy) * 13 + x + dx
                    neighbor_ids.append(pre.room_map[index])
                    if abs(dx) == 1 and abs(dy) == 1:
                        stats["ultra_diagonal_neighbor"] += 1
                    else:
                        stats["ultra_distance_two_neighbor"] += 1
                neighbor_rooms = [pre.rooms[room_id] for room_id in neighbor_ids]
                if any(room.room_type == 7 for room in neighbor_rooms):
                    stats["ultra_secret_neighbor"] += 1
                if any(room.room_type == 8 for room in neighbor_rooms):
                    stats["ultra_super_secret_neighbor"] += 1
                if any(int(room.shape) in (4, 5, 6, 7, 8) for room in neighbor_rooms):
                    stats["ultra_large_neighbor"] += 1
                if any(int(room.shape) in (9, 10, 11, 12) for room in neighbor_rooms):
                    stats["ultra_l_shape_neighbor"] += 1
            report["difficulties"][difficulty] = stats
            report["total_comparisons"] += stats["comparisons"]
    except Exception:
        print(
            f"minimal differential reproduction: difficulty={difficulty} start_seed=0x{seed:08X}",
            file=sys.stderr,
        )
        raise

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

