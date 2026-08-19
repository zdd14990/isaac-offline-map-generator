from __future__ import annotations

import pytest

from isaacmap.rng import IsaacRNG, RNG_SHIFT_TRIPLES


def test_shift_table_shape_and_endpoints() -> None:
    assert len(RNG_SHIFT_TRIPLES) == 81
    assert RNG_SHIFT_TRIPLES[0] == (1, 3, 10)
    assert RNG_SHIFT_TRIPLES[27] == (3, 23, 25)
    assert RNG_SHIFT_TRIPLES[80] == (17, 15, 26)


@pytest.mark.parametrize(
    ("shift_index", "expected"),
    [
        (0, [0x00000009, 0x00000065, 0x000002EF, 0x00001F5F]),
        (27, [0x00800001, 0x00100001, 0x00920001, 0x00004001]),
        (80, [0x00008001, 0x40000011, 0x5008A005, 0x14080804]),
    ],
)
def test_next_fixed_vectors(shift_index: int, expected: list[int]) -> None:
    rng = IsaacRNG.from_seed(1, shift_index)
    assert [rng.next() for _ in expected] == expected


def test_random_int_advances_even_for_zero_maximum() -> None:
    direct = IsaacRNG.from_seed(0x12345678, 27)
    expected_state = direct.next()
    rng = IsaacRNG.from_seed(0x12345678, 27)
    assert rng.random_int(0) == 0
    assert rng.seed == expected_state


def test_random_int_is_unsigned_remainder() -> None:
    direct = IsaacRNG.from_seed(0xFFFFFFFF, 27)
    expected_state = direct.next()
    rng = IsaacRNG.from_seed(0xFFFFFFFF, 27)
    assert rng.random_int(1000) == expected_state % 1000


def test_random_float_binary32_path() -> None:
    rng = IsaacRNG.from_seed(1, 27)
    assert rng.random_float() == pytest.approx(0.001953125, rel=0, abs=0)


def test_set_seed_clamps_shift_index_to_80() -> None:
    rng = IsaacRNG.from_seed(1, 0xFFFFFFFF)
    assert (rng.shift1, rng.shift2, rng.shift3) == RNG_SHIFT_TRIPLES[80]


def test_constructor_rejects_out_of_range_shift_index() -> None:
    with pytest.raises(ValueError):
        IsaacRNG.game_constructor(1, 81)


@pytest.mark.parametrize("method", ["next", "random_int", "random_float"])
def test_zero_seed_draw_is_rejected(method: str) -> None:
    rng = IsaacRNG.from_seed(0, 0)
    with pytest.raises(ValueError):
        if method == "random_int":
            rng.random_int(10)
        else:
            getattr(rng, method)()
