"""Find instructions containing an immediate/displacement in the locked PE."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pefile
from capstone import CS_ARCH_X86, CS_MODE_32, Cs


PROFILE_SHA256 = "3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b"


def _integer(value: str) -> int:
    return int(value, 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("value", type=_integer)
    parser.add_argument("--pe", type=Path, default=Path("research/input/isaac-ng.exe"))
    args = parser.parse_args()

    data = args.pe.read_bytes()
    actual_hash = hashlib.sha256(data).hexdigest()
    if actual_hash != PROFILE_SHA256:
        raise RuntimeError(f"refusing non-profiled PE: {actual_hash}")
    pe = pefile.PE(data=data, fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    disassembler = Cs(CS_ARCH_X86, CS_MODE_32)
    disassembler.skipdata = True
    needle = f"0x{args.value:x}"

    print("va\trva\tbytes\tinstruction")
    for section in pe.sections:
        if not section.IMAGE_SCN_MEM_EXECUTE:
            continue
        start = section.PointerToRawData
        code = data[start : start + section.SizeOfRawData]
        base = image_base + section.VirtualAddress
        for instruction in disassembler.disasm(code, base):
            if needle not in instruction.op_str.lower():
                continue
            print(
                f"0x{instruction.address:08X}\t"
                f"0x{instruction.address - image_base:08X}\t"
                f"{instruction.bytes.hex(' ')}\t"
                f"{instruction.mnemonic} {instruction.op_str}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
