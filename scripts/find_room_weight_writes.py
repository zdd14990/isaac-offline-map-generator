"""Find static x86 writes to RoomConfig_Room.Weight (+0x34) in the frozen PE.

The executable is opened only as bytes and is never loaded or executed.
"""

from __future__ import annotations

import hashlib
import argparse
from pathlib import Path

import pefile
from capstone import CS_AC_WRITE, CS_ARCH_X86, CS_MODE_32, Cs
from capstone.x86 import X86_OP_MEM


PROFILE_SHA256 = "3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-va", type=lambda value: int(value, 0), default=0)
    parser.add_argument("--end-va", type=lambda value: int(value, 0), default=0xFFFFFFFF)
    args = parser.parse_args()
    path = Path("research/input/isaac-ng.exe")
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual}")

    pe = pefile.PE(data=data, fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    text = next(section for section in pe.sections if section.Name.rstrip(b"\0") == b".text")
    code = text.get_data()
    start = image_base + text.VirtualAddress

    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    decoder.detail = True
    decoder.skipdata = True
    instructions = list(decoder.disasm(code, start))
    for index, instruction in enumerate(instructions):
        is_weight_write = False
        for operand_index, operand in enumerate(instruction.operands):
            if operand.type != X86_OP_MEM or operand.mem.disp != 0x34:
                continue
            # Capstone 5's Python wheel does not always populate operand.access
            # for legacy x86 SSE stores, so retain the explicit destination test.
            if (operand.access & CS_AC_WRITE) or (
                operand_index == 0 and instruction.mnemonic.startswith("mov")
            ):
                is_weight_write = True
        if not is_weight_write:
            continue
        if not args.start_va <= instruction.address < args.end_va:
            continue
        print(f"\nWRITE VA 0x{instruction.address:08X} RVA 0x{instruction.address-image_base:08X}")
        for nearby in instructions[max(0, index - 8) : index + 9]:
            marker = ">" if nearby.address == instruction.address else " "
            print(f"{marker} 0x{nearby.address:08X}  {nearby.mnemonic:<8} {nearby.op_str}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
