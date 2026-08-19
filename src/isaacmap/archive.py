"""Read Isaac ``ARCH000`` resource archives without executing game code.

The archive structures, filename hashes, LZW decoder, and MiniZ block handling
are clean Python ports of Gibbed.Rebirth (zlib license), cross-checked against
the local archives. Only extraction is implemented; archives are never edited.
"""

from __future__ import annotations

import struct
import zlib
from dataclasses import dataclass
from pathlib import Path


UINT32_MASK = 0xFFFFFFFF


class ArchiveError(RuntimeError):
    """Base error for malformed or unsupported Isaac archives."""


class UnsupportedArchiveBlockError(ArchiveError):
    """Raised for an archive compression mode that is not implemented."""


def compute_name_hash(path: str) -> tuple[int, int]:
    """Return Isaac's two 32-bit lowercase path hashes."""

    normalized = path.lower().replace("\\", "/")
    hash_a = 5381
    hash_b = 0x5BB2220E
    for value in normalized.encode("utf-8"):
        hash_a = (hash_a * 33 + value) & UINT32_MASK
        hash_b = ((hash_b ^ value) * 0x1000193) & UINT32_MASK
    return hash_a, hash_b


@dataclass(frozen=True)
class ArchiveEntry:
    name_hash_a: int
    name_hash_b: int
    offset: int
    length: int
    checksum: int

    @property
    def combined_name_hash(self) -> int:
        return self.name_hash_a | (self.name_hash_b << 32)


class _BitReader:
    def __init__(self, buffer: bytes):
        self.buffer = buffer
        self.position = 0
        self.remaining_bits = 0
        self.value = 0

    def read(self, bits: int) -> int:
        if not 0 < bits <= 32:
            raise ValueError("bits must be in [1, 32]")
        while self.remaining_bits < bits:
            if self.position >= len(self.buffer):
                raise ArchiveError("unexpected end of LZW bitstream")
            self.value = ((self.value << 8) | self.buffer[self.position]) & UINT32_MASK
            self.position += 1
            self.remaining_bits += 8
        self.remaining_bits -= bits
        mask = (1 << bits) - 1
        return (self.value >> self.remaining_bits) & mask


class _CodeDictionary:
    CAPACITY = 4096

    def __init__(self):
        self.items: list[tuple[int, int]] = []
        self.code_length = 8
        self.reset()

    def reset(self) -> None:
        self.items = [(-1, value) for value in range(256)]
        self.code_length = 8

    def add(self, last_value: int, previous_index: int) -> None:
        if len(self.items) >= self.CAPACITY:
            raise ArchiveError("LZW dictionary overflow")
        if not 0 <= previous_index < len(self.items):
            raise ArchiveError("invalid LZW previous index")
        self.items.append((previous_index, last_value))

    def update_code_length(self) -> None:
        while len(self.items) >= 1 << self.code_length:
            self.code_length += 1

    def decode(self, index: int) -> tuple[bytes, int]:
        if not 0 <= index < len(self.items):
            raise ArchiveError(f"invalid LZW dictionary index {index}")
        values = bytearray()
        while index != -1:
            previous, value = self.items[index]
            values.append(value)
            index = previous
            if len(values) > self.CAPACITY:
                raise ArchiveError("cyclic LZW dictionary entry")
        values.reverse()
        return bytes(values), values[0]


def _decompress_lzw(data: bytes, offset: int, expected_length: int) -> bytes:
    dictionary = _CodeDictionary()
    output = bytearray()
    cursor = offset

    while len(output) < expected_length:
        if cursor + 4 > len(data):
            raise ArchiveError("truncated LZW block header")
        block_length = struct.unpack_from("<I", data, cursor)[0]
        cursor += 4
        block = data[cursor : cursor + block_length]
        cursor += block_length
        if len(block) != block_length:
            raise ArchiveError("truncated LZW block")

        reader = _BitReader(block)
        previous_index = reader.read(dictionary.code_length)
        line, last_value = dictionary.decode(previous_index)
        output.extend(line)

        while reader.position < len(block):
            if len(dictionary.items) + 1 >= dictionary.CAPACITY:
                dictionary.reset()
                previous_index = reader.read(dictionary.code_length)
                line, last_value = dictionary.decode(previous_index)
                output.extend(line)
                continue

            dictionary.update_code_length()
            index = reader.read(dictionary.code_length)
            if index == len(dictionary.items):
                if previous_index != -1:
                    dictionary.add(last_value, previous_index)
                line, last_value = dictionary.decode(index)
                output.extend(line)
            else:
                if index > len(dictionary.items):
                    raise ArchiveError("invalid future LZW dictionary index")
                line, last_value = dictionary.decode(index)
                output.extend(line)
                if previous_index != -1:
                    dictionary.add(last_value, previous_index)
            previous_index = index

    if len(output) != expected_length:
        raise ArchiveError(
            f"LZW length mismatch: expected {expected_length}, got {len(output)}"
        )
    return bytes(output)


class _IsaacCipher:
    """ISAAC stream used by encrypted raw MiniZ blocks.

    This is a clean Python translation of the zlib-licensed Gibbed.Rebirth
    archive reader already used as the format reference for this module.
    """

    SIZE = 256
    MASK = (SIZE - 1) << 2

    def __init__(self, name_hash_b: int):
        seed = name_hash_b & 0xFFFFFFFF
        low = (
            seed
            ^ (((seed ^ ((seed << 15) & 0xFFFFFFFFFFFFFFFF)) << 8) & 0xFFFFFFFFFFFFFFFF)
            ^ (seed >> 9)
        ) & 0xFFFFFFFF
        seed64 = ((seed << 32) | low) & 0xFFFFFFFFFFFFFFFF
        results: list[int] = []
        for _ in range(self.SIZE):
            part = ((seed64 >> 27) ^ (seed64 >> 45)) & 0xFFFFFFFF
            shift = seed64 >> 59
            results.append(
                ((part >> shift) | (part << ((-shift) & 31))) & 0xFFFFFFFF
            )
            seed64 = (
                seed64 * 6364136223846793005 + 127
            ) & 0xFFFFFFFFFFFFFFFF

        self.results = results
        self.state = [0] * self.SIZE
        self.index = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self._initialize()

    @staticmethod
    def _mix(values: tuple[int, ...]) -> tuple[int, ...]:
        a, b, c, d, e, f, g, h = values
        mask = 0xFFFFFFFF
        a = (a ^ (b << 11)) & mask; d = (d + a) & mask; b = (b + c) & mask
        b = (b ^ (c >> 2)) & mask; e = (e + b) & mask; c = (c + d) & mask
        c = (c ^ (d << 8)) & mask; f = (f + c) & mask; d = (d + e) & mask
        d = (d ^ (e >> 16)) & mask; g = (g + d) & mask; e = (e + f) & mask
        e = (e ^ (f << 10)) & mask; h = (h + e) & mask; f = (f + g) & mask
        f = (f ^ (g >> 4)) & mask; a = (a + f) & mask; g = (g + h) & mask
        g = (g ^ (h << 8)) & mask; b = (b + g) & mask; h = (h + a) & mask
        h = (h ^ (a >> 9)) & mask; c = (c + h) & mask; a = (a + b) & mask
        return a, b, c, d, e, f, g, h

    def _initialize(self) -> None:
        values = (0x9E3779B9,) * 8
        for _ in range(4):
            values = self._mix(values)
        for index in range(0, self.SIZE, 8):
            values = tuple(
                (value + self.results[index + offset]) & 0xFFFFFFFF
                for offset, value in enumerate(values)
            )
            values = self._mix(values)
            self.state[index : index + 8] = values
        for index in range(0, self.SIZE, 8):
            values = tuple(
                (value + self.state[index + offset]) & 0xFFFFFFFF
                for offset, value in enumerate(values)
            )
            values = self._mix(values)
            self.state[index : index + 8] = values
        self._generate()

    def _step(self, index: int, other: int, shift: int, *, left: bool) -> int:
        x = self.state[index]
        if left:
            self.a = (self.a ^ (self.a << shift)) & 0xFFFFFFFF
        else:
            self.a = (self.a ^ (self.a >> shift)) & 0xFFFFFFFF
        self.a = (self.a + self.state[other]) & 0xFFFFFFFF
        y = (
            self.state[((x & self.MASK) >> 2)] + self.a + self.b
        ) & 0xFFFFFFFF
        self.state[index] = y
        self.b = (
            self.state[(((y >> 8) & self.MASK) >> 2)] + x
        ) & 0xFFFFFFFF
        self.results[index] = self.b
        return other + 1

    def _generate(self) -> None:
        self.c = (self.c + 1) & 0xFFFFFFFF
        self.b = (self.b + self.c) & 0xFFFFFFFF
        index, other = 0, self.SIZE // 2
        while index < self.SIZE // 2:
            other = self._step(index, other, 13, left=True); index += 1
            other = self._step(index, other, 6, left=False); index += 1
            other = self._step(index, other, 2, left=True); index += 1
            other = self._step(index, other, 16, left=False); index += 1
        other = 0
        while index < self.SIZE:
            other = self._step(index, other, 13, left=True); index += 1
            other = self._step(index, other, 6, left=False); index += 1
            other = self._step(index, other, 2, left=True); index += 1
            other = self._step(index, other, 16, left=False); index += 1

    def value(self) -> int:
        result = self.results[self.index]
        self.index += 1
        if self.index >= self.SIZE:
            self._generate()
            self.index = 0
        return result


def _decompress_miniz(
    data: bytes,
    offset: int,
    expected_length: int,
    *,
    name_hash_b: int,
) -> bytes:
    output = bytearray()
    cursor = offset
    compressed = True
    cipher: _IsaacCipher | None = None

    while True:
        if cursor + 4 > len(data):
            raise ArchiveError("truncated MiniZ block header")
        flags = struct.unpack_from("<I", data, cursor)[0]
        cursor += 4
        block_length = flags & 0x7FFFFFFF
        last_block = bool(flags & 0x80000000)
        block = data[cursor : cursor + block_length]
        cursor += block_length
        if len(block) != block_length:
            raise ArchiveError("truncated MiniZ block")

        if not compressed or (not last_block and block_length == 1024):
            compressed = False
            if cipher is None:
                cipher = _IsaacCipher(name_hash_b)
            decrypted = bytearray(block)
            for position in range(0, len(decrypted), 4):
                key = cipher.value()
                for offset_in_word in range(min(4, len(decrypted) - position)):
                    decrypted[position + offset_in_word] ^= (
                        key >> (offset_in_word * 8)
                    ) & 0xFF
            output.extend(decrypted)
        else:
            try:
                # Isaac stores independent raw-DEFLATE chunks that may omit the
                # conventional end-of-stream marker. ``decompressobj`` preserves
                # the successfully decoded bytes in that case; the declared entry
                # length and archive checksum provide the strict validation.
                inflater = zlib.decompressobj(wbits=-15)
                output.extend(inflater.decompress(block))
                output.extend(inflater.flush())
            except zlib.error as error:
                raise ArchiveError(f"raw DEFLATE failed: {error}") from error

        if len(output) > expected_length:
            raise ArchiveError("MiniZ output exceeds declared entry length")
        if last_block:
            break

    if len(output) != expected_length:
        raise ArchiveError(
            f"MiniZ length mismatch: expected {expected_length}, got {len(output)}"
        )
    return bytes(output)


def compute_checksum(data: bytes, seed: int = 0xABABEB98) -> int:
    """Reproduce the archive checksum, including its historical block bleed."""

    checksum = seed
    block = bytearray(512)
    offset = 0
    while offset < len(data):
        block_length = min(512, len(data) - offset)
        block[:block_length] = data[offset : offset + block_length]
        for position in range(0, ((block_length + 3) // 4) * 4, 4):
            value = struct.unpack_from("<I", block, position)[0]
            checksum = (
                (checksum >> 1) + value + ((checksum << 31) & UINT32_MASK)
            ) & UINT32_MASK
        offset += block_length
    return checksum


class ArchiveReader:
    """Read-only parser for one local Isaac resource archive."""

    MAGIC = b"ARCH000"

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self._data = self.path.read_bytes()
        if len(self._data) < 14 or self._data[:7] != self.MAGIC:
            raise ArchiveError(f"not an ARCH000 archive: {self.path}")
        self.compression_mode = self._data[7]
        table_offset, entry_count = struct.unpack_from("<IH", self._data, 8)
        table_end = table_offset + entry_count * 20
        if table_end > len(self._data):
            raise ArchiveError("archive index extends past end of file")
        self.entries = tuple(
            ArchiveEntry(*struct.unpack_from("<IIIII", self._data, table_offset + i * 20))
            for i in range(entry_count)
        )
        self._by_hash = {
            (entry.name_hash_a, entry.name_hash_b): entry for entry in self.entries
        }

    def find(self, path: str) -> ArchiveEntry | None:
        return self._by_hash.get(compute_name_hash(path))

    def read(self, path: str, *, verify_checksum: bool = True) -> bytes | None:
        entry = self.find(path)
        if entry is None:
            return None
        if self.compression_mode == 1:
            result = _decompress_lzw(self._data, entry.offset, entry.length)
        elif self.compression_mode == 2:
            result = _decompress_miniz(
                self._data,
                entry.offset,
                entry.length,
                name_hash_b=entry.name_hash_b,
            )
        else:
            raise UnsupportedArchiveBlockError(
                f"archive compression mode {self.compression_mode} is not supported"
            )
        if verify_checksum:
            actual = compute_checksum(result)
            if actual != entry.checksum:
                raise ArchiveError(
                    f"checksum mismatch for {path}: expected 0x{entry.checksum:08X}, "
                    f"got 0x{actual:08X}"
                )
        return result
