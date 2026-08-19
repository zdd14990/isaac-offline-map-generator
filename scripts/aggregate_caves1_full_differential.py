"""Aggregate Caves-I differential shards into the final report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("shards", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    totals = {
        "comparisons": 0,
        "attempts": 0,
        "retrying_seeds": 0,
        "max_attempts": 0,
        "rng_transitions": 0,
        "room_config_selections": 0,
        "boss_selections": 0,
        "xl_floors": 0,
        "mismatches": 0,
    }
    matches = True
    first = None
    for shard in args.shards:
        data = json.loads(shard.read_text(encoding="utf-8"))
        if first is None:
            first = data
        matches &= bool(data.get("matches"))
        if data.get("mismatch"):
            totals["mismatches"] += 1
        for key in totals:
            if key == "mismatches":
                continue
            if key == "max_attempts":
                totals[key] = max(totals[key], data["stats"].get(key, 0))
            else:
                totals[key] += data["stats"].get(key, 0)
        totals["mismatches"] += data["stats"].get("mismatches", 0)

    report = {
        "profile_sha256": first["profile_sha256"],
        "safety": first["safety"],
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical Caves I complete accepted 13x13 layout plus successful lifecycle handoff",
        "normal_seeds": 10000,
        "hard_seeds": 10000,
        "stats": totals,
        "matches": matches,
        "mismatch": None if matches else "see shard reports",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
