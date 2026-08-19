"""20k-seed offline differential through Treasure (no Isaac execution)."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from isaacmap.basement1_pipeline import generate_basement1_through_treasure
from isaacmap.basement1_pipeline_differential import compare_pipeline
from isaacmap.basement1_pipeline_reference import generate_basement1_through_treasure_reference
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference, PROFILE_SHA256
from isaacmap.resources import load_stb


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--count",type=int,default=10_000)
    parser.add_argument("--pe",type=Path,default=Path("research/input/isaac-ng.exe"))
    parser.add_argument("--resources",type=Path,default=Path("research/input/extracted_resources/merged/resources"))
    parser.add_argument("--output",type=Path,default=Path("research/binary/basement1_pipeline_differential_report.json")); args=parser.parse_args()
    actual=hashlib.sha256(args.pe.read_bytes()).hexdigest()
    if actual != PROFILE_SHA256: raise RuntimeError(f"refusing non-profiled PE: {actual}")
    bosses=load_boss_pool_xml(args.resources/"bosspools.xml")["basement"]
    boss_refs=tuple(BossPoolEntryReference(x.boss_id,x.weight,x.initial_weight,x.achievement,x.alternate_boss_id) for x in bosses)
    special=tuple(load_stb(args.resources/"rooms/00.special rooms.stb")); basement=tuple(load_stb(args.resources/"rooms/01.basement.stb"))
    report={"profile_sha256":PROFILE_SHA256,"safety":"Copied PE read as data only; isaac-ng.exe was not executed or loaded.","external_validation":"NOT_EXTERNALLY_VALIDATED_GAMEPLAY","scope":"canonical fresh Basement I through Treasure; Secret and Ultra excluded","difficulties":{},"total_comparisons":0,"differential_dimensions":["attempt count and target-room count","full M4 topology state and final generator RNG state","BossPool persistent/local state, blacklist, permanent removal","RoomConfig ordered candidates, exact-door subset, binary32 weights and draws","ordered end-room candidate scans, geometry decisions, stable erase","room anchors, RoomShape, occupied map, connections and RoomType mutation","all post-topology RNG object transitions and final states","binary condition traces through Treasure"]}
    try:
        for difficulty in ("NORMAL","HARD"):
            stats={"comparisons":0,"total_attempts":0,"retrying_seeds":0,"abort_operations":{},"max_attempts":0,"topology_shapes":set(),"selected_config_shapes":{"Boss":set(),"RoomType8":set(),"Shop":set(),"Treasure":set()},"geometry_candidate_shapes":set(),"post_topology_rng_transitions":0,"room_config_selector_calls":0,"candidate_tests":0,"condition_traces":0}
            for seed in range(1,args.count+1):
                clean=generate_basement1_through_treasure(seed,difficulty,boss_entries=bosses,special_definitions=special,basement_definitions=basement)
                reference=generate_basement1_through_treasure_reference(seed,difficulty,boss_entries=boss_refs,special_definitions=special,basement_definitions=basement)
                compare_pipeline(clean,reference)
                stats["comparisons"]+=1; stats["total_attempts"]+=len(clean.attempts); stats["max_attempts"]=max(stats["max_attempts"],len(clean.attempts))
                if len(clean.attempts)>1: stats["retrying_seeds"]+=1
                for attempt in clean.attempts:
                    stats["topology_shapes"].update(int(room.shape) for room in attempt.topology.rooms)
                    if attempt.post_topology and attempt.post_topology.abort_operation:
                        op=attempt.post_topology.abort_operation; stats["abort_operations"][op]=stats["abort_operations"].get(op,0)+1
                    if attempt.post_topology:
                        post=attempt.post_topology
                        stats["post_topology_rng_transitions"]+=len(post.rng_draws)
                        stats["candidate_tests"]+=len(post.candidate_traces)
                        stats["condition_traces"]+=len(post.conditions)
                        stats["geometry_candidate_shapes"].update(int(event.candidate.shape) for event in post.geometry_traces)
                        for trace in post.config_traces:
                            stats["room_config_selector_calls"]+=len(trace.selections)
                            for selection in trace.selections:
                                if selection.entry is not None:
                                    stats["selected_config_shapes"][trace.operation].add(int(selection.entry.shape))
            stats["topology_shapes"]=sorted(stats["topology_shapes"])
            stats["geometry_candidate_shapes"]=sorted(stats["geometry_candidate_shapes"])
            stats["selected_config_shapes"]={key:sorted(value) for key,value in stats["selected_config_shapes"].items()}
            report["difficulties"][difficulty]=stats; report["total_comparisons"]+=stats["comparisons"]
    except Exception:
        print(f"minimal differential reproduction: difficulty={difficulty} start_seed=0x{seed:08X}",file=sys.stderr); raise
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2)); return 0


if __name__=="__main__": raise SystemExit(main())
