"""Emulate isolated copied-PE topology leaf functions with Unicorn.

The Windows loader is never invoked.  No process is created for the target,
and no import, entry point, or game loop is executed.  Only exact function and
constant bytes are copied into Unicorn-owned memory after a profile hash check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

import pefile
from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_MODE_32, Uc
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EDX, UC_X86_REG_ESP

from isaacmap.topology_geometry import has_shape_slot
from isaacmap.topology_reference import PROFILE_SHA256


IMAGE_BASE = 0x00400000
CANONICAL_RVA = 0x005AFD70
CANONICAL_VA = IMAGE_BASE + CANONICAL_RVA
CANONICAL_SIZE = 0x19
HAS_SHAPE_SLOT_RVA = 0x005AF370
HAS_SHAPE_SLOT_VA = IMAGE_BASE + HAS_SHAPE_SLOT_RVA
HAS_SHAPE_SLOT_SIZE = 0x79
DIMENSIONS_RVA = 0x0085D378
DIMENSIONS_VA = IMAGE_BASE + DIMENSIONS_RVA
DIMENSIONS_SIZE = 13 * 8
STACK_BASE = 0x01000000
STACK_SIZE = 0x10000
DATA_BASE = 0x02000000
STOP_ADDRESS = 0x00F00000


def _extract(payload: bytes, pe: pefile.PE, rva: int, size: int) -> bytes:
    offset = pe.get_offset_from_rva(rva)
    return payload[offset : offset + size]


def _emulator(
    canonical: bytes, has_shape_slot_bytes: bytes, dimensions: bytes
) -> Uc:
    emulator = Uc(UC_ARCH_X86, UC_MODE_32)
    emulator.mem_map(0x009AF000, 0x2000)
    emulator.mem_write(CANONICAL_VA, canonical)
    emulator.mem_write(HAS_SHAPE_SLOT_VA, has_shape_slot_bytes)
    emulator.mem_map(0x00C5D000, 0x1000)
    emulator.mem_write(DIMENSIONS_VA, dimensions)
    emulator.mem_map(STACK_BASE, STACK_SIZE)
    emulator.mem_map(DATA_BASE, 0x1000)
    emulator.mem_map(STOP_ADDRESS, 0x1000)

    def stop_at_sentinel(uc: Uc, address: int, _size: int, _data: object) -> None:
        if address == STOP_ADDRESS:
            uc.emu_stop()

    emulator.hook_add(UC_HOOK_CODE, stop_at_sentinel)
    return emulator


def _prepare_call(emulator: Uc, stack_arguments: tuple[int, ...]) -> None:
    stack = STACK_BASE + STACK_SIZE - 0x100
    emulator.mem_write(
        stack,
        struct.pack("<" + "I" * (1 + len(stack_arguments)), STOP_ADDRESS, *stack_arguments),
    )
    emulator.reg_write(UC_X86_REG_ESP, stack)


def _run_canonical(
    canonical: bytes,
    has_shape_slot_bytes: bytes,
    dimensions: bytes,
    column: int,
    line: int,
) -> int:
    emulator = _emulator(canonical, has_shape_slot_bytes, dimensions)
    emulator.mem_write(DATA_BASE, struct.pack("<ii", column, line))
    _prepare_call(emulator, ())
    emulator.reg_write(UC_X86_REG_ECX, DATA_BASE)
    emulator.emu_start(CANONICAL_VA, STOP_ADDRESS, count=100)
    value = emulator.reg_read(UC_X86_REG_EAX) & 0xFFFFFFFF
    return value - 0x100000000 if value & 0x80000000 else value


def _run_has_shape_slot(
    canonical: bytes,
    has_shape_slot_bytes: bytes,
    dimensions: bytes,
    shape: int,
    slot: int,
    ignore_thin: bool,
) -> bool:
    emulator = _emulator(canonical, has_shape_slot_bytes, dimensions)
    _prepare_call(emulator, (int(ignore_thin),))
    emulator.reg_write(UC_X86_REG_ECX, shape)
    emulator.reg_write(UC_X86_REG_EDX, slot)
    emulator.emu_start(HAS_SHAPE_SLOT_VA, STOP_ADDRESS, count=200)
    return bool(emulator.reg_read(UC_X86_REG_EAX) & 0xFF)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    payload = args.pe.read_bytes()
    actual_hash = hashlib.sha256(payload).hexdigest()
    if actual_hash != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual_hash}")
    pe = pefile.PE(data=payload, fast_load=True)
    canonical = _extract(payload, pe, CANONICAL_RVA, CANONICAL_SIZE)
    has_shape_slot_bytes = _extract(
        payload, pe, HAS_SHAPE_SLOT_RVA, HAS_SHAPE_SLOT_SIZE
    )
    dimensions = _extract(payload, pe, DIMENSIONS_RVA, DIMENSIONS_SIZE)

    canonical_cases = 0
    for column in range(-2, 15):
        for line in range(-2, 15):
            expected = line * 13 + column if 0 <= column < 13 and 0 <= line < 13 else -1
            actual = _run_canonical(
                canonical, has_shape_slot_bytes, dimensions, column, line
            )
            if actual != expected:
                raise AssertionError(("canonical_grid_index", column, line, expected, actual))
            canonical_cases += 1

    slot_cases = 0
    for shape in range(1, 13):
        for slot in range(8):
            for ignore_thin in (False, True):
                expected = has_shape_slot(
                    shape,
                    slot,
                    ignore_thin_restrictions=ignore_thin,
                )
                actual = _run_has_shape_slot(
                    canonical,
                    has_shape_slot_bytes,
                    dimensions,
                    shape,
                    slot,
                    ignore_thin,
                )
                if actual != expected:
                    raise AssertionError(
                        ("has_shape_slot", shape, slot, ignore_thin, expected, actual)
                    )
                slot_cases += 1

    report = {
        "profile_sha256": PROFILE_SHA256,
        "engine": "Unicorn 2.1.4 x86-32",
        "safety": {
            "target_process_created": False,
            "windows_loader_used": False,
            "pe_entry_point_executed": False,
            "imports_executed": False,
            "game_loop_executed": False,
            "method": "Exact leaf-function/data bytes copied into Unicorn-owned memory",
        },
        "emulated_functions": [
            {
                "name": "LevelGenerator::canonical_grid_index",
                "rva": "0x005afd70",
                "byte_sha256": hashlib.sha256(canonical).hexdigest(),
                "cases": canonical_cases,
                "matches_python": True,
            },
            {
                "name": "LevelGenerator::has_shape_slot",
                "rva": "0x005af370",
                "byte_sha256": hashlib.sha256(has_shape_slot_bytes).hexdigest(),
                "cases": slot_cases,
                "matches_python": True,
            },
        ],
        "full_level_generator_assessment": {
            "feasible_in_principle": True,
            "implemented": False,
            "status": "HIGH_ISOLATION_COST_NOT_BLOCKING_STATIC_PROOF",
            "reason": (
                "Generate/get_neighbor_candidates use MSVC vector/deque/set code, heap allocation, "
                "SEH/TLS, security cookies, logging, and global data. Full emulation needs a PE "
                "memory mapper plus deterministic allocator/container/logger/TLS stubs; leaf "
                "emulation proves the safe method but is not yet an independent whole-generator oracle."
            ),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

