"""The 32-bit RNG used by the version-locked Isaac executable profile."""

from __future__ import annotations

from dataclasses import dataclass
import struct

UINT32_MASK = 0xFFFFFFFF

# 81 triples at executable VA 0x00B1F4C8 (RVA 0x0071F4C8). The values were
# statically extracted from the copied executable and cross-checked with the
# open-source eden-seed-finder table. Index 60 differs: the current executable
# has (9, 5, 14), while that older public table has (9, 5, 1).
RNG_SHIFT_TRIPLES: tuple[tuple[int, int, int], ...] = (
    (1, 3, 10), (1, 5, 16), (1, 5, 19), (1, 9, 29), (1, 11, 6),
    (1, 11, 16), (1, 19, 3), (1, 21, 20), (1, 27, 27), (2, 5, 15),
    (2, 5, 21), (2, 7, 7), (2, 7, 9), (2, 7, 25), (2, 9, 15),
    (2, 15, 17), (2, 15, 25), (2, 21, 9), (3, 1, 14), (3, 3, 26),
    (3, 3, 28), (3, 3, 29), (3, 5, 20), (3, 5, 22), (3, 5, 25),
    (3, 7, 29), (3, 13, 7), (3, 23, 25), (3, 25, 24), (3, 27, 11),
    (4, 3, 17), (4, 3, 27), (4, 5, 15), (5, 3, 21), (5, 7, 22),
    (5, 9, 7), (5, 9, 28), (5, 9, 31), (5, 13, 6), (5, 15, 17),
    (5, 17, 13), (5, 21, 12), (5, 27, 8), (5, 27, 21), (5, 27, 25),
    (5, 27, 28), (6, 1, 11), (6, 3, 17), (6, 17, 9), (6, 21, 7),
    (6, 21, 13), (7, 1, 9), (7, 1, 18), (7, 1, 25), (7, 13, 25),
    (7, 17, 21), (7, 25, 12), (7, 25, 20), (8, 7, 23), (8, 9, 23),
    (9, 5, 14), (9, 5, 25), (9, 11, 19), (9, 21, 16), (10, 9, 21),
    (10, 9, 25), (11, 7, 12), (11, 7, 16), (11, 17, 13), (11, 21, 13),
    (12, 9, 23), (13, 3, 17), (13, 3, 27), (13, 5, 19), (13, 17, 15),
    (14, 1, 15), (14, 13, 15), (15, 1, 29), (17, 15, 20), (17, 15, 23),
    (17, 15, 26),
)

if len(RNG_SHIFT_TRIPLES) != 81:  # pragma: no cover - import-time invariant
    raise AssertionError("the Isaac RNG shift table must contain 81 triples")


def _uint32(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if not 0 <= value <= UINT32_MASK:
        raise ValueError(f"{name} must be in the range 0..0xffffffff")
    return value


def _float32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


_RANDOM_FLOAT_SCALE = struct.unpack("<f", struct.pack("<I", 0x2F7FFFFE))[0]


@dataclass
class IsaacRNG:
    """Mutable 16-byte RNG state, matching ``RNG::SetSeed`` semantics.

    ``SetSeed`` clamps an unsigned shift index above 80 to 80. A zero seed can
    be stored by the binary, but every draw hits its assertion path, so draw
    methods reject it here without trying to emulate the binary's crash.
    """

    seed: int
    shift1: int
    shift2: int
    shift3: int

    @classmethod
    def from_seed(cls, seed: int, shift_index: int) -> "IsaacRNG":
        seed = _uint32(seed, "seed")
        shift_index = _uint32(shift_index, "shift index")
        shift1, shift2, shift3 = RNG_SHIFT_TRIPLES[min(shift_index, 80)]
        return cls(seed, shift1, shift2, shift3)

    @classmethod
    def game_constructor(cls, seed: int, shift_index: int) -> "IsaacRNG":
        """Match the constructor, which asserts instead of clamping the index."""

        seed = _uint32(seed, "seed")
        shift_index = _uint32(shift_index, "shift index")
        if shift_index >= len(RNG_SHIFT_TRIPLES):
            raise ValueError("game constructor requires a shift index below 81")
        shift1, shift2, shift3 = RNG_SHIFT_TRIPLES[shift_index]
        return cls(seed, shift1, shift2, shift3)

    def set_seed(self, seed: int, shift_index: int) -> None:
        replacement = self.from_seed(seed, shift_index)
        self.seed = replacement.seed
        self.shift1 = replacement.shift1
        self.shift2 = replacement.shift2
        self.shift3 = replacement.shift3

    def next(self) -> int:
        if self.seed == 0:
            raise ValueError("the game RNG cannot advance a zero state")
        value = self.seed
        value ^= value >> self.shift1
        value ^= (value << self.shift2) & UINT32_MASK
        value ^= value >> self.shift3
        self.seed = value & UINT32_MASK
        return self.seed

    def random_int(self, maximum: int) -> int:
        maximum = _uint32(maximum, "maximum")
        value = self.next()
        return value % maximum if maximum else 0

    def random_float(self) -> float:
        # Current x86 SSE sequence: uint32 -> double, correct signed values by
        # 2^32, round to binary32, multiply by the binary32 constant stored as
        # 0x2F7FFFFE in this executable, and round again.
        value = self.next()
        as_binary32 = _float32(float(value))
        return _float32(as_binary32 * _RANDOM_FLOAT_SCALE)
