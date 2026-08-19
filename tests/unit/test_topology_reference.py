from __future__ import annotations

from dataclasses import replace

import pytest

from isaacmap.floor_init import derive_basement1_topology_inputs
from isaacmap.topology_differential import compare_clean_and_reference
from isaacmap.topology_reference import (
    derive_and_generate_basement1_topology_reference,
)


def test_entry_rng_ledger_names_exact_objects_and_binary_sites() -> None:
    result = derive_and_generate_basement1_topology_reference(1, "NORMAL")
    assert [draw.binary_rva for draw in result.entry_rng_ledger] == [
        0x00344C1E,
        0x00344CAA,
        0x00340E8E,
        0x0034109F,
        0x00341202,
    ]
    assert [draw.rng_object for draw in result.entry_rng_ledger] == [
        "Level._generationRNG",
        "Level._generationRNG",
        "Level._generationRNG",
        "Level::generate_dungeon.stack_rng_copy",
        "Level._generationRNG",
    ]
    assert [(draw.pre_state, draw.post_state) for draw in result.entry_rng_ledger] == [
        (0x00100001, 0x2152A305),
        (0x2152A305, 0x91146405),
        (0x91146405, 0xAD4AA83F),
        (0x91146405, 0xAD4AA83F),
        (0xAD4AA83F, 0xE809B57C),
    ]
    assert all(draw.shift_index == 35 for draw in result.entry_rng_ledger)
    assert all(draw.shifts == (5, 9, 7) for draw in result.entry_rng_ledger)


@pytest.mark.parametrize("difficulty", ["NORMAL", "HARD"])
def test_first_hundred_seeds_match_every_differential_dimension(difficulty: str) -> None:
    for start_seed in range(1, 101):
        compare_clean_and_reference(
            derive_basement1_topology_inputs(start_seed, difficulty)
        )


def test_coverage_examples_include_forcing_boundaries_and_all_l_shapes() -> None:
    shapes: set[int] = set()
    forced = 0
    boundaries = 0
    random_failures = 0
    large_rooms = 0
    for start_seed in range(1, 14):
        reference, _ = compare_clean_and_reference(
            derive_basement1_topology_inputs(start_seed, "NORMAL")
        )
        shapes.update(room.shape for room in reference.rooms)
        forced += reference.coverage.forced_dead_end_attempts
        boundaries += reference.coverage.boundary_skips
        random_failures += reference.coverage.large_random_failures
        large_rooms += reference.coverage.large_rooms_placed
    assert set(range(9, 13)).issubset(shapes)
    assert forced > 0
    assert boundaries > 0
    assert random_failures > 0
    assert large_rooms > 0


def test_targeted_retry_path_matches_reference_and_clean() -> None:
    # required_dead_ends=6 is a branch fixture, not a claim about the standard
    # Basement I parameter (which is 5).  Seed 290 makes the first attempt
    # fail after all five forced-dead-end tries and the second attempt succeed.
    inputs = replace(
        derive_basement1_topology_inputs(290, "NORMAL"),
        required_dead_ends=6,
    )
    reference, summary = compare_clean_and_reference(inputs)
    assert summary.retries == 1
    assert len(reference.attempts) == 2
    assert reference.attempts[0].forced_dead_end_attempts == 5


def test_binary_selection_sort_tie_order_is_not_stable_sort_order() -> None:
    reference, _ = compare_clean_and_reference(
        derive_basement1_topology_inputs(1, "NORMAL")
    )
    assert reference.dead_ends == (9, 8, 4, 3, 2)
    assert reference.rooms[4].distance_from_start == 2
    assert reference.rooms[3].distance_from_start == 2


def test_generator_ledger_is_one_contiguous_state_chain() -> None:
    reference, _ = compare_clean_and_reference(
        derive_basement1_topology_inputs(4, "HARD")
    )
    assert reference.generator_rng_ledger
    assert all(
        left.post_state == right.pre_state
        for left, right in zip(
            reference.generator_rng_ledger,
            reference.generator_rng_ledger[1:],
        )
    )
    assert reference.generator_rng_ledger[-1].post_state == reference.final_rng_state
    assert all(draw.shift_index == 35 for draw in reference.generator_rng_ledger)
    assert all(draw.shifts == (5, 9, 7) for draw in reference.generator_rng_ledger)

