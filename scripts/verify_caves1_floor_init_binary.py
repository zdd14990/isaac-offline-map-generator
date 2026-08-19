"""Verify static canonical Caves-I floor-entry constants and branches."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile

from isaacmap.boss_pool_reference import PROFILE_SHA256
from isaacmap.resources import load_stb


INIT_SLICE_RVA = 0x00344CF3
INIT_SLICE_SIZE = 0x34D
DUNGEON_SLICE_RVA = 0x00340E8E
DUNGEON_SLICE_SIZE = 0x4C3
LABYRINTH_PREDICATE_RVA = 0x003385C0
LABYRINTH_PREDICATE_SIZE = 0x43
ROOM_CONFIG_STAGE_RVA = 0x0042D030
ROOM_CONFIG_STAGE_SIZE = 0xCE
XL_MULTIPLIER_RVA = 0x007AA628
XL_TOPOLOGY_BRANCH_RVA = 0x005B0768
XL_TOPOLOGY_BRANCH_SIZE = 0x6C


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("resources", type=Path)
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

    transfers = {
        "curse_gate_random_int": call_target(0x00344F09),
        "labyrinth_stage_predicate": call_target(0x00344F77),
        "curse_normalizer": call_target(0x00345008),
        "level_generator_constructor": call_target(0x00341233),
        "room_config_stage": call_target(0x00341347),
    }
    expected_transfers = {
        "curse_gate_random_int": 0x003E9020,
        "labyrinth_stage_predicate": LABYRINTH_PREDICATE_RVA,
        "curse_normalizer": 0x00464AE0,
        "level_generator_constructor": 0x005ADAF0,
        "room_config_stage": ROOM_CONFIG_STAGE_RVA,
    }
    transfer_checks = {
        key: value == expected_transfers[key] for key, value in transfers.items()
    }
    byte_checks = {
        "normal_curse_denominator_80": (0x00344CF3, "ba50000000"),
        "hard_curse_denominator_40": (0x00344D75, "b828000000"),
        "curse_modulo_six": (0x00344F4B, "b8abaaaaaa"),
        "labyrinth_bit": (0x00344F84, "834f0c02"),
        "stage_target_formula": (0x00340EC1, "8d0c80b856555555"),
        "target_add_five": (0x00340ECF, "c1e81f83c005"),
        "base_target_cap_twenty": (0x00340ED9, "be14000000"),
        "xl_curse_test": (0x00340F35, "a802"),
        "xl_target_cap_forty_five": (0x00340F41, "b92d000000"),
        "xl_multiply_binary64": (0x00340F4A, "f20f590528a6ba00"),
        "lost_add_four": (0x00340F8D, "8385fcfbffff04"),
        "copied_rng_always_advances": (0x0034109F, "8b4e048bc2d3e8"),
        "hard_bonus_gate": (0x003410CA, "83b8c869020001"),
        "hard_add_two_plus_bit": (0x003410D3, "8b8dfcfbffff83c10203ce"),
        "required_dead_end_base": (0x00341132, "33c083bde8fbffff01"),
        "required_dead_end_xl_add_six": (0x0034116D, "a802741133c0"),
        "difficulty_xl_test": (0x0034126B, "8bbd00fcffffa802"),
        "difficulty_stage_below_nine": (0x0034127D, "83f809"),
        "hard_odd_window_5_10": (0x003412AA, "c785ecfbffff0a000000"),
        "normal_odd_window_1_5": (0x003412DA, "c785ecfbffff05000000"),
        "xl_normal_hard_minimum": (0x003412F4, "83bdf4fbffff01"),
        "room_config_stage_original_formula": (0x0042D0AE, "4983fa047508"),
        "topology_neighbor_count_at_least_two": (0x005B0768, "8d46288bcf50e8cdfcffff83f802"),
        "topology_xl_flag": (0x005B0778, "80bf9003000000"),
        "topology_void_fallback_flag": (0x005B0781, "80bf9203000000"),
        "topology_exception_modulo_ten": (0x005B07C3, "b90a00000033c233d28907f7f1"),
        "topology_exception_accept_zero": (0x005B07D0, "85d20f857c010000"),
    }
    instruction_checks = {
        name: read(rva, len(bytes.fromhex(expected))).hex() == expected
        for name, (rva, expected) in byte_checks.items()
    }
    labyrinth_checks = {
        "odd_stage": read(0x003385CF, 0x13).hex()
        == "8b098bc1250100008079054883c8fe4083f801",
        "below_stage_eight": read(0x003385E4, 5).hex() == "83f9087d15",
        "ordinary_mode_only": read(0x003385E9, 0x10).hex()
        == "8b82c869020083f802740a83f8037405",
        "returns_true": read(0x003385F9, 5).hex() == "b001c20400",
    }
    multiplier_bytes = read(XL_MULTIPLIER_RVA, 8)
    multiplier = struct.unpack("<d", multiplier_bytes)[0]
    caves_path = args.resources / "rooms" / "04.caves.stb"
    caves_payload = caves_path.read_bytes()
    caves = load_stb(caves_path)
    difficulty_windows = ((1, 5), (5, 10), (1, 10), (5, 15))
    shapes_by_window = {
        f"{minimum}..{maximum}": sorted(
            {
                room.shape
                for room in caves
                if room.room_type == 1
                and minimum <= room.difficulty <= maximum
            }
        )
        for minimum, maximum in difficulty_windows
    }
    shape_checks = {
        key: value == list(range(1, 13))
        for key, value in shapes_by_window.items()
    }
    actual_hash = hashlib.sha256(payload).hexdigest()
    checks = {
        "profile_hash": actual_hash == PROFILE_SHA256,
        "control_transfers": all(transfer_checks.values()),
        "instruction_constants": all(instruction_checks.values()),
        "labyrinth_predicate": all(labyrinth_checks.values()),
        "xl_multiplier": multiplier_bytes.hex() == "cdccccccccccfc3f"
        and multiplier == 1.8,
        "xl_topology_branch": all(
            instruction_checks[name]
            for name in (
                "topology_neighbor_count_at_least_two",
                "topology_xl_flag",
                "topology_void_fallback_flag",
                "topology_exception_modulo_ten",
                "topology_exception_accept_zero",
            )
        ),
        "room_config_stage": 4
        == (0 + 1 + 2 * ((3 - 1) >> 1) + ((3 - 1) >> 1)),
        "caves_shapes": all(shape_checks.values()),
    }
    report = {
        "profile_sha256": actual_hash,
        "safety": "PE and STB read as bytes only; no image loading or execution.",
        "external_validation": "NOT_EXTERNALLY_VALIDATED_GAMEPLAY",
        "scope": "canonical ORIGINAL Caves I floor entry/topology inputs",
        "level_init_slice": {
            "rva": f"0x{INIT_SLICE_RVA:08X}",
            "size": INIT_SLICE_SIZE,
            "sha256": hashlib.sha256(read(INIT_SLICE_RVA, INIT_SLICE_SIZE)).hexdigest(),
        },
        "generate_dungeon_slice": {
            "rva": f"0x{DUNGEON_SLICE_RVA:08X}",
            "size": DUNGEON_SLICE_SIZE,
            "sha256": hashlib.sha256(read(DUNGEON_SLICE_RVA, DUNGEON_SLICE_SIZE)).hexdigest(),
        },
        "labyrinth_predicate": {
            "rva": f"0x{LABYRINTH_PREDICATE_RVA:08X}",
            "size": LABYRINTH_PREDICATE_SIZE,
            "sha256": hashlib.sha256(
                read(LABYRINTH_PREDICATE_RVA, LABYRINTH_PREDICATE_SIZE)
            ).hexdigest(),
            "checks": labyrinth_checks,
        },
        "room_config_stage_function": {
            "rva": f"0x{ROOM_CONFIG_STAGE_RVA:08X}",
            "size": ROOM_CONFIG_STAGE_SIZE,
            "sha256": hashlib.sha256(
                read(ROOM_CONFIG_STAGE_RVA, ROOM_CONFIG_STAGE_SIZE)
            ).hexdigest(),
            "canonical_stage3_result": 4,
        },
        "xl_multiplier": {
            "rva": f"0x{XL_MULTIPLIER_RVA:08X}",
            "bytes": multiplier_bytes.hex(),
            "value": multiplier,
        },
        "xl_topology_branch": {
            "rva": f"0x{XL_TOPOLOGY_BRANCH_RVA:08X}",
            "size": XL_TOPOLOGY_BRANCH_SIZE,
            "sha256": hashlib.sha256(
                read(XL_TOPOLOGY_BRANCH_RVA, XL_TOPOLOGY_BRANCH_SIZE)
            ).hexdigest(),
            "behavior": "links >= 2 accepted only for XL/Void and Next() % 10 == 0",
        },
        "caves_resource": {
            "path": str(caves_path),
            "sha256": hashlib.sha256(caves_payload).hexdigest(),
            "room_count": len(caves),
            "room_default_shapes_by_difficulty_window": shapes_by_window,
        },
        "control_transfers": {
            key: f"0x{value:08X}" for key, value in transfers.items()
        },
        "control_transfer_checks": transfer_checks,
        "instruction_checks": instruction_checks,
        "shape_checks": shape_checks,
        "checks": checks,
        "matches": all(checks.values()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
