"""Isaac display-seed encoding for the version-locked executable profile.

The implementation is a direct translation of ``Seed2String`` and
``String2Seed`` in the copied executable with SHA-256
``3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b``.
It does not load or execute game code.
"""

from __future__ import annotations

SEED_ALPHABET = "ABCDEFGHJKLMNPQRSTWXYZ01234V6789"
SEED_XOR_MASK = 0x0FEF7FFD
UINT32_MAX = 0xFFFFFFFF

_DECODE_TABLE = {character: index for index, character in enumerate(SEED_ALPHABET)}


class InvalidSeedError(ValueError):
    """Raised when text is not a valid ordinary Isaac run seed."""


def _require_start_seed(seed: int) -> int:
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("start seed must be an integer")
    if not 1 <= seed <= UINT32_MAX:
        raise ValueError("ordinary start seed must be in the range 1..0xffffffff")
    return seed


def seed_checksum(seed: int) -> int:
    """Return the exact eight-bit checksum used by the current executable."""

    _require_start_seed(seed)
    working = seed
    checksum = 0
    while working:
        checksum = (checksum + (working & 0xFF)) & 0xFF
        working >>= 5
        checksum = ((checksum << 1) + (checksum >> 7)) & 0xFF
    return checksum


def encode_seed(start_seed: int) -> str:
    """Encode a nonzero uint32 run seed as canonical ``XXXX XXXX`` text."""

    seed = _require_start_seed(start_seed)
    encoded_bits = ((seed ^ SEED_XOR_MASK) << 8) | seed_checksum(seed)
    characters = "".join(
        SEED_ALPHABET[(encoded_bits >> shift) & 0x1F]
        for shift in range(35, -1, -5)
    )
    return f"{characters[:4]} {characters[4:]}"


def decode_seed(display_seed: str) -> int:
    """Decode and validate a canonical ordinary Isaac run seed.

    This deliberately mirrors the binary's strict format: exactly nine ASCII
    characters, a literal space in position four, and uppercase alphabet
    members. The binary uses zero as its invalid sentinel, so the reserved
    internal seed zero is not accepted by this public run-seed API.
    """

    if not isinstance(display_seed, str):
        raise TypeError("display seed must be a string")
    if len(display_seed) != 9 or display_seed[4] != " ":
        raise InvalidSeedError("seed must use the exact form 'XXXX XXXX'")

    encoded_bits = 0
    for position, character in enumerate(display_seed):
        if position == 4:
            continue
        try:
            value = _DECODE_TABLE[character]
        except KeyError as error:
            raise InvalidSeedError(
                f"invalid seed character {character!r} at position {position}"
            ) from error
        encoded_bits = (encoded_bits << 5) | value

    expected_checksum = encoded_bits & 0xFF
    start_seed = ((encoded_bits >> 8) ^ SEED_XOR_MASK) & UINT32_MAX
    if start_seed == 0:
        raise InvalidSeedError("zero is reserved as the binary's invalid-seed sentinel")
    actual_checksum = seed_checksum(start_seed)
    if actual_checksum != expected_checksum:
        raise InvalidSeedError(
            f"seed checksum mismatch: encoded=0x{expected_checksum:02x}, "
            f"computed=0x{actual_checksum:02x}"
        )
    return start_seed


def is_valid_seed(display_seed: object) -> bool:
    """Return whether *display_seed* is a valid ordinary run seed."""

    if not isinstance(display_seed, str):
        return False
    try:
        decode_seed(display_seed)
    except (InvalidSeedError, TypeError):
        return False
    return True
