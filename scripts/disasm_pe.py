"""Disassemble bytes from a copied x86 PE without loading or executing it."""

from __future__ import annotations

import argparse
from pathlib import Path

import pefile
from capstone import CS_ARCH_X86, CS_MODE_32, Cs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pe", type=Path)
    parser.add_argument("--rva", required=True, type=lambda value: int(value, 0))
    parser.add_argument("--size", default=512, type=lambda value: int(value, 0))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = args.pe.read_bytes()
    pe = pefile.PE(data=data, fast_load=False)
    offset = pe.get_offset_from_rva(args.rva)
    code = data[offset : offset + args.size]
    base = pe.OPTIONAL_HEADER.ImageBase + args.rva

    disassembler = Cs(CS_ARCH_X86, CS_MODE_32)
    disassembler.detail = False
    lines: list[str] = []
    for insn in disassembler.disasm(code, base):
        raw = insn.bytes.hex(" ")
        lines.append(f"{insn.address:08x}  {raw:<30}  {insn.mnemonic:<8} {insn.op_str}")
    rendered = "\n".join(lines) + "\n"
    print(rendered, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
