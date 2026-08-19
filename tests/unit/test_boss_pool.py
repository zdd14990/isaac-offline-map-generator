from __future__ import annotations

from pathlib import Path

from isaacmap.boss_pool import (
    BASEMENT_POOL_INDEX,
    POOL_COUNT,
    derive_pool_seeds,
    load_boss_pool_xml,
    pick_fresh_basement_boss,
)
from isaacmap.boss_pool_differential import compare_fresh_basement_boss


RESOURCE_ROOT = Path("research/input/extracted_resources/merged/resources")


def _basement_entries():
    return load_boss_pool_xml(RESOURCE_ROOT / "bosspools.xml")["basement"]


def test_current_resource_has_expected_ordered_basement_pool() -> None:
    pools = load_boss_pool_xml(RESOURCE_ROOT / "bosspools.xml")
    entries = pools["basement"]
    assert len(pools) == 25
    assert [entry.boss_id for entry in entries] == [
        1, 17, 2, 44, 64, 56, 65, 20, 13, 60, 84,
    ]
    assert [entry.weight for entry in entries] == [
        1.0, 1.0, 1.0, 1.0, 0.25, 1.0, 0.25, 0.25, 1.0, 1.0, 1.0,
    ]


def test_pool_seeds_are_one_chained_master_stream() -> None:
    seeds = derive_pool_seeds(0x12345678)
    assert len(seeds) == POOL_COUNT
    assert seeds[:4] == (
        0x4B73F4CE,
        0xF2B1C483,
        0x1343572B,
        0x767FD835,
    )


def test_fresh_basement_pick_preserves_separate_persistent_and_local_states() -> None:
    result = pick_fresh_basement_boss(0x12345678, _basement_entries())
    assert result.pool_index == BASEMENT_POOL_INDEX
    assert result.initial_pool_state == 0xF2B1C483
    assert result.shuffled_entry_ids == (20, 13, 84, 65, 56, 60, 64, 1, 17, 2, 44)
    assert result.boss_id == 13
    assert result.persistent_pool_state == 0x3B586A26
    assert result.local_selector_final_state == 0x207E4797
    assert len(result.transitions) == 8
    assert all(
        identity == "BossPools.pool[1]._rng"
        for identity, _, _ in result.transitions[:7]
    )
    assert result.transitions[-1][0] == "stack_copy(BossPools.pool[1]._rng)"


def test_first_hundred_fresh_boss_picks_match_mechanical_reference() -> None:
    entries = _basement_entries()
    for game_start_seed in range(1, 101):
        compare_fresh_basement_boss(game_start_seed, entries)
