"""Export a complete per-draw Basement I topology RNG ledger offline."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from isaacmap.floor_init import derive_basement1_topology_inputs
from isaacmap.topology_reference import (
    PROFILE_SHA256,
    generate_basement1_topology_reference,
)


def _parse_uint32(value: str) -> int:
    result = int(value, 0)
    if not 0 < result <= 0xFFFFFFFF:
        raise argparse.ArgumentTypeError("start seed must be in 1..0xffffffff")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-seed", type=_parse_uint32, required=True)
    parser.add_argument("--difficulty", choices=("NORMAL", "HARD"), required=True)
    parser.add_argument(
        "--pe", type=Path, default=Path("research/input/isaac-ng.exe")
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    actual_hash = hashlib.sha256(args.pe.read_bytes()).hexdigest()
    if actual_hash != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual_hash}")

    inputs = derive_basement1_topology_inputs(args.start_seed, args.difficulty)
    result = generate_basement1_topology_reference(inputs)
    payload = {
        "profile_sha256": PROFILE_SHA256,
        "start_seed": args.start_seed,
        "difficulty": args.difficulty,
        "inputs": asdict(inputs),
        "entry_rng_ledger": [asdict(draw) for draw in result.entry_rng_ledger],
        "generator_rng_ledger": [
            asdict(draw) for draw in result.generator_rng_ledger
        ],
        "attempts": [asdict(attempt) for attempt in result.attempts],
        "target_room_count": result.target_room_count,
        "retry_count": result.retries,
        "final_generator_rng_state": result.final_rng_state,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
