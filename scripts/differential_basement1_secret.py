"""20k-seed offline M6 differential (the Isaac executable is never run)."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from isaacmap.basement1_secret_pipeline import generate_basement1_through_secret
from isaacmap.basement1_secret_pipeline_differential import compare_secret_pipeline
from isaacmap.basement1_secret_pipeline_reference import generate_basement1_through_secret_reference
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference, PROFILE_SHA256
from isaacmap.resources import load_stb


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--count", type=int, default=10_000)
    parser.add_argument("--difficulty", action="append", choices=("NORMAL", "HARD"))
    parser.add_argument("--pe", type=Path, default=Path("research/input/isaac-ng.exe"))
    parser.add_argument("--resources", type=Path, default=Path("research/input/extracted_resources/merged/resources"))
    parser.add_argument("--output", type=Path, default=Path("research/binary/basement1_secret_differential_report.json"))
    args = parser.parse_args()
    actual = hashlib.sha256(args.pe.read_bytes()).hexdigest()
    if actual != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual}")
    bosses = load_boss_pool_xml(args.resources / "bosspools.xml")["basement"]
    boss_refs = tuple(BossPoolEntryReference(x.boss_id, x.weight, x.initial_weight, x.achievement, x.alternate_boss_id) for x in bosses)
    special = tuple(load_stb(args.resources / "rooms/00.special rooms.stb"))
    basement = tuple(load_stb(args.resources / "rooms/01.basement.stb"))
    report = {
        "profile_sha256": PROFILE_SHA256,
        "safety": "Copied PE read as data only; isaac-ng.exe was not executed or loaded.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical fresh Basement I through Secret; Ultra and late default variants excluded",
        "seed_range": [args.start, args.start + args.count - 1],
        "difficulties": {},
        "total_comparisons": 0,
        "dimensions": [
            "full M4/M5 attempt state and persistent owners",
            "ordered Treasure-to-Secret block/config/candidate traces",
            "stable dead-end erase and tail reappend",
            "RoomConfig candidates, binary32 weights, selector draws",
            "Secret forbidden set and all 169 candidate evaluations",
            "Secret neighbor masks, scores, ties and LevelGenerator RNG transitions",
            "Secret descriptor/map/connection mutation and final RNG states",
            "pre-Ultra pending BossPool blacklist remains uncommitted",
        ],
    }
    try:
        for difficulty in (tuple(args.difficulty) if args.difficulty else ("NORMAL", "HARD")):
            stats = {
                "comparisons": 0, "total_attempts": 0, "retrying_seeds": 0,
                "secret_missing": 0, "secret_neighbor_counts": {},
                "secret_tie_sizes": {}, "secret_boundary": 0,
                "secret_large_neighbor": 0, "secret_l_shape_neighbor": 0,
                "blocks_assigned": {}, "blocks_seen": {},
                "final_used_bit_sets": {},
            }
            for seed in range(args.start, args.start + args.count):
                clean = generate_basement1_through_secret(seed, difficulty, boss_entries=bosses, special_definitions=special, basement_definitions=basement)
                reference = generate_basement1_through_secret_reference(seed, difficulty, boss_entries=boss_refs, special_definitions=special, basement_definitions=basement)
                compare_secret_pipeline(clean, reference)
                stats["comparisons"] += 1
                stats["total_attempts"] += len(clean.attempts)
                if len(clean.attempts) > 1: stats["retrying_seeds"] += 1
                m6 = clean.attempts[-1].through_secret
                if m6 is None: continue
                for block in m6.blocks:
                    stats["blocks_seen"][block.operation] = stats["blocks_seen"].get(block.operation, 0) + 1
                    if block.assigned: stats["blocks_assigned"][block.operation] = stats["blocks_assigned"].get(block.operation, 0) + 1
                geometry = m6.secret_geometry
                if geometry.room_id < 0:
                    stats["secret_missing"] += 1
                else:
                    evaluation = geometry.evaluations[geometry.grid_index]
                    count = str(evaluation.adjacency_count)
                    stats["secret_neighbor_counts"][count] = stats["secret_neighbor_counts"].get(count, 0) + 1
                    ties = str(len(geometry.best_candidates))
                    stats["secret_tie_sizes"][ties] = stats["secret_tie_sizes"].get(ties, 0) + 1
                    x, y = geometry.grid_index % 13, geometry.grid_index // 13
                    if x in (0, 12) or y in (0, 12): stats["secret_boundary"] += 1
                    neighbor_ids = m6.rooms[geometry.room_id].neighbors
                    if any(int(m6.rooms[r].shape) in (4, 6, 8) for r in neighbor_ids): stats["secret_large_neighbor"] += 1
                    if any(int(m6.rooms[r].shape) in (9, 10, 11, 12) for r in neighbor_ids): stats["secret_l_shape_neighbor"] += 1
                used = ",".join(map(str, m6.used_bits_after)) or "none"
                stats["final_used_bit_sets"][used] = stats["final_used_bit_sets"].get(used, 0) + 1
            report["difficulties"][difficulty] = stats
            report["total_comparisons"] += stats["comparisons"]
    except Exception:
        print(f"minimal differential reproduction: difficulty={difficulty} start_seed=0x{seed:08X}", file=sys.stderr)
        raise
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
