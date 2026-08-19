"""List direct and indirect x86 CALL sites from the hash-locked PE copy."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pefile
from capstone import CS_ARCH_X86, CS_MODE_32, Cs
from capstone.x86 import X86_OP_IMM


PROFILE_SHA256 = "3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b"


def _integer(value: str) -> int:
    return int(value, 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pe", type=Path, default=Path("research/input/isaac-ng.exe"))
    parser.add_argument("--start-va", type=_integer, required=True)
    parser.add_argument("--end-va", type=_integer, required=True)
    parser.add_argument("--target-va", type=_integer)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = args.pe.read_bytes()
    actual_hash = hashlib.sha256(data).hexdigest()
    if actual_hash != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual_hash}")
    pe = pefile.PE(data=data, fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    start_rva = args.start_va - image_base
    end_rva = args.end_va - image_base
    start_offset = pe.get_offset_from_rva(start_rva)
    code = data[start_offset : start_offset + end_rva - start_rva]

    disassembler = Cs(CS_ARCH_X86, CS_MODE_32)
    disassembler.detail = True
    rows = ["call_va\tcall_rva\ttarget_va\ttarget_rva\toperand"]
    for instruction in disassembler.disasm(code, args.start_va):
        if instruction.mnemonic != "call":
            continue
        target_va = "INDIRECT"
        target_rva = "INDIRECT"
        if instruction.operands and instruction.operands[0].type == X86_OP_IMM:
            target = instruction.operands[0].imm & 0xFFFFFFFF
            target_va = f"0x{target:08X}"
            target_rva = f"0x{target - image_base:08X}"
            if args.target_va is not None and target != args.target_va:
                continue
        elif args.target_va is not None:
            continue
        rows.append(
            "\t".join(
                (
                    f"0x{instruction.address:08X}",
                    f"0x{instruction.address - image_base:08X}",
                    target_va,
                    target_rva,
                    instruction.op_str,
                )
            )
        )
    output = "\n".join(rows) + "\n"
    if args.output is None:
        print(output, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
