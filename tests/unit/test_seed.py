from __future__ import annotations

import pytest

from isaacmap.seed import (
    InvalidSeedError,
    SEED_ALPHABET,
    decode_seed,
    encode_seed,
    is_valid_seed,
    seed_checksum,
)


@pytest.mark.parametrize(
    ("start_seed", "display_seed"),
    [
        (0x00000001, "B911 99AC"),
        (0x12345678, "D1PW XBN9"),
        (0xFFFFFFFF, "8AJJ AAYH"),
    ],
)
def test_binary_derived_golden_vectors(start_seed: int, display_seed: str) -> None:
    assert encode_seed(start_seed) == display_seed
    assert decode_seed(display_seed) == start_seed


@pytest.mark.parametrize(
    "start_seed",
    [1, 2, 31, 32, 0x1234, 0x0FEF7FFD, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF],
)
def test_round_trip(start_seed: int) -> None:
    display_seed = encode_seed(start_seed)
    assert len(display_seed) == 9
    assert display_seed[4] == " "
    assert set(display_seed.replace(" ", "")) <= set(SEED_ALPHABET)
    assert decode_seed(display_seed) == start_seed


def test_checksum_rotates_after_every_five_bit_step() -> None:
    assert seed_checksum(1) == 2
    assert seed_checksum(0xFFFFFFFF) == 0x87


@pytest.mark.parametrize(
    "display_seed",
    [
        "ABCD EFGH",  # Structurally valid but checksum-invalid.
        "abcd efgh",
        "ABCD-EFGH",
        "ABCDEFGHI",
        "ABCD EFG",
        "ABCD EFGHI",
        "ABCI EFGH",  # I is deliberately absent from the alphabet.
        "ABCO EFGH",  # O is deliberately absent from the alphabet.
    ],
)
def test_invalid_seed_is_rejected(display_seed: str) -> None:
    with pytest.raises(InvalidSeedError):
        decode_seed(display_seed)
    assert not is_valid_seed(display_seed)


@pytest.mark.parametrize("start_seed", [0, -1, 0x1_0000_0000])
def test_non_run_seed_integer_is_rejected(start_seed: int) -> None:
    with pytest.raises(ValueError):
        encode_seed(start_seed)


@pytest.mark.parametrize("value", [None, 1, b"B911 A82D"])
def test_non_string_seed_is_rejected(value: object) -> None:
    with pytest.raises(TypeError):
        decode_seed(value)  # type: ignore[arg-type]
    assert not is_valid_seed(value)
