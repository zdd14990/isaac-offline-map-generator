"""Static verifier for canonical Stage-2 Treasure-to-Secret branches.

The frozen PE is read only as bytes.  It is never loaded as an image or
executed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256


POST_RVA = 0x00339370
POST_SIZE = 17370
POST_SHA256 = "7ae850e43abce93f33e12ef5881bf9d09043ea866ad7773d643965659ad16996"
PLANETARIUM_RVA = 0x0034DBD0
PLANETARIUM_SIZE = 597
PLANETARIUM_SHA256 = "ab284be888cb4e4848aa6537dda6921c4e7c4b85b0323f5a006daf2f8e67700f"
PLAYER_CONDITION_RVA = 0x005BEB30
PLAYER_CONDITION_SIZE = 110
PLAYER_CONDITION_SHA256 = "b3083f83cd1b7109c8c35e15a2a59f8fcb772f6e47574c1b31ff7d1508a66630"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    payload = args.pe.read_bytes()
    pe = pefile.PE(data=payload, fast_load=True)

    def read(rva: int, size: int) -> bytes:
        return pe.get_data(rva, size)

    def call_target(rva: int) -> int:
        data = read(rva, 5)
        if data[0] != 0xE8:
            raise ValueError(f"RVA 0x{rva:08X} is not a near call")
        return (rva + 5 + struct.unpack("<i", data[1:])[0]) & 0xFFFFFFFF

    calls = {
        "planetarium_chance": (0x0033A8F7, PLANETARIUM_RVA),
        "challenge_player_condition": (0x0033BD21, PLAYER_CONDITION_RVA),
    }
    actual_calls = {name: call_target(rva) for name, (rva, _) in calls.items()}
    call_checks = {
        name: actual_calls[name] == expected for name, (_, expected) in calls.items()
    }
    byte_checks = {
        # The second MiniBoss RNG draw and modulo-three calculation occur for
        # Stage 2, but the following effective-stage compare only accepts 1.
        "miniboss_secondary_draw_and_stage_one_gate": (
            0x0033BA1A,
            "b8abaaaaaad3ee33f2f7e68bce8937d1ea8d04522bc875248b0d7816c7008b410483f804740983f80574048b01eb08a17816c7008b004083f80174",
        ),
        # Odd draws reject effective Stage <=2, then the player predicate is
        # called with zero and assignment requires effective Stage >=2.
        "challenge_parity_player_and_stage_gates": (
            0x0033BCF5,
            "891f83e001741d8b460483f804740983f80574048b06eb038b064083f8020f8e67ffffff8d8ea8ba01006a00e80a2e280084c00f8452ffffff8b460483f804740983f80574048b06eb038b064083f8010f8e",
        ),
        # RoomType 20 requires max-hearts >1 and effective Stage 2 is in the
        # explicit even-stage assignment list.
        "chest_max_hearts_and_even_stage_assignment": (
            0x0033C05B,
            "837b081475578b0d7816c7006a00e802b8cdff83b85c130000017e418a853bffffff83fe02741883fe04741383fe06740e83fe08740984c0742383fe0a7f1e8b8530ffffff85c074466a0051ff378b8d2cffffff5350e8fac9ffffeb328b8530",
        ),
        "planetarium_base_load": (0x0034DBD6, "f30f10056ca0ba00"),
        "planetarium_last_treasure_stage_load": (0x0034DCE4, "8b9658650200"),
        "planetarium_skipped_treasure_increment": (0x0034DD09, "f30f590598a1ba00"),
        "planetarium_add_base": (0x0034DD11, "f30f58056ca0ba00"),
        "planetarium_clamp_floor": (0x0034DDFD, "f30f5f056ca0ba00"),
        "planetarium_clamp_ceiling": (0x0034DE05, "f30f5d0554a4ba00"),
        # Param 0 makes the helper aggregate whether any eligible player
        # satisfies its full-health-style health predicate.
        "player_condition_health_fields": (
            0x005BEB55,
            "8b814c1300000381441300003b81401300007d09e842cbe1ff84c07402b001",
        ),
    }
    instruction_checks = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    constants = {
        "base_0_01": (0x007AA06C, 0.01),
        "skipped_treasure_0_20": (0x007AA198, 0.2),
        "cap_1_0": (0x007AA454, 1.0),
    }
    actual_constants = {
        name: struct.unpack("<f", read(rva, 4))[0]
        for name, (rva, _) in constants.items()
    }
    constant_checks = {
        name: read(rva, 4) == struct.pack("<f", expected)
        for name, (rva, expected) in constants.items()
    }
    stage_two_chance = struct.unpack(
        "<f",
        struct.pack(
            "<f",
            struct.unpack(
                "<f",
                struct.pack("<f", actual_constants["skipped_treasure_0_20"]),
            )[0]
            + actual_constants["base_0_01"],
        ),
    )[0]
    actual_hash = hashlib.sha256(payload).hexdigest()
    function_hashes = {
        "post_topology": hashlib.sha256(read(POST_RVA, POST_SIZE)).hexdigest(),
        "planetarium_chance": hashlib.sha256(
            read(PLANETARIUM_RVA, PLANETARIUM_SIZE)
        ).hexdigest(),
        "challenge_player_condition": hashlib.sha256(
            read(PLAYER_CONDITION_RVA, PLAYER_CONDITION_SIZE)
        ).hexdigest(),
    }
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "post_topology_hash": function_hashes["post_topology"] == POST_SHA256,
        "planetarium_function_hash": function_hashes["planetarium_chance"] == PLANETARIUM_SHA256,
        "player_condition_function_hash": function_hashes["challenge_player_condition"] == PLAYER_CONDITION_SHA256,
        "control_transfers": all(call_checks.values()),
        "stage_two_branch_bytes": all(instruction_checks.values()),
        "planetarium_constants": all(constant_checks.values()),
        "canonical_stage_two_planetarium_chance_bits": struct.pack(
            "<f", stage_two_chance
        ).hex() == "3e0a573e",
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE read as bytes only; no image loading or execution.",
        "scope": "canonical Basement II Treasure-to-Secret stage predicates",
        "function_hashes": function_hashes,
        "control_transfers": {
            key: f"0x{value:08X}" for key, value in actual_calls.items()
        },
        "control_transfer_checks": call_checks,
        "instruction_checks": instruction_checks,
        "constants": actual_constants,
        "canonical_stage_two_planetarium_chance": stage_two_chance,
        "canonical_stage_two_planetarium_chance_f32_bits": struct.pack(
            "<f", stage_two_chance
        ).hex(),
        "constant_checks": constant_checks,
        "checks": checks,
        "matches": all(checks.values()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
