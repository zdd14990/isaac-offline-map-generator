from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement2_full_pipeline_reference import generate_basement2_full_reference
from isaacmap.basement2_lifecycle import generate_basement2_lifecycle
from isaacmap.boss_pool import (
    CAVES_POOL_INDEX,
    BossPoolRuntimeState,
    load_boss_pool_xml,
)
from isaacmap.boss_pool_differential import compare_runtime_selection
from isaacmap.boss_pool_reference import (
    BossPoolEntryReference,
    BossPoolRuntimeReference,
    derive_pool_seeds_reference,
)
from isaacmap.floor_init import derive_caves1_topology_inputs
from isaacmap.resources import load_stb


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
POOLS = load_boss_pool_xml(ROOT / "bosspools.xml")
BASEMENT_BOSSES = POOLS["basement"]
CAVES_BOSSES = POOLS["caves"]
BASEMENT_REFS = tuple(
    BossPoolEntryReference(
        item.boss_id,
        item.weight,
        item.initial_weight,
        item.achievement,
        item.alternate_boss_id,
    )
    for item in BASEMENT_BOSSES
)
CAVES_REFS = tuple(
    BossPoolEntryReference(
        item.boss_id,
        item.weight,
        item.initial_weight,
        item.achievement,
        item.alternate_boss_id,
    )
    for item in CAVES_BOSSES
)


@lru_cache(maxsize=16)
def _entry(seed: int, difficulty: str):
    clean = generate_basement2_lifecycle(
        seed,
        difficulty,
        boss_entries=BASEMENT_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    reference = generate_basement2_full_reference(
        seed,
        difficulty,
        boss_entries=BASEMENT_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )
    compare_basement1_full(clean.layout, reference)
    return clean.next_run_state, reference


def _resume(seed: int, clean_snapshot, reference_b2):
    clean = BossPoolRuntimeState.resume_canonical_caves(
        seed,
        CAVES_BOSSES,
        pool_state=clean_snapshot.boss_pool_rng_states[CAVES_POOL_INDEX],
        removed=clean_snapshot.permanent_removed_bosses,
    )
    reference = BossPoolRuntimeReference.resume_canonical_caves(
        seed,
        CAVES_REFS,
        pool_state=derive_pool_seeds_reference(seed)[CAVES_POOL_INDEX],
        removed=reference_b2.removed,
    )
    return clean, reference


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 7, 23))
def test_caves1_primary_boss_restores_stage3_pool_state(
    seed: int, difficulty: str
) -> None:
    snapshot, reference_b2 = _entry(seed, difficulty)
    clean, reference = _resume(seed, snapshot, reference_b2)
    clean.begin_attempt()
    reference.begin_attempt()
    clean_pick = clean.select_canonical_caves_profile()
    reference_pick = reference.select_canonical_caves_profile()
    compare_runtime_selection(clean_pick, reference_pick)
    assert clean_pick.pool_index == CAVES_POOL_INDEX == 4
    assert clean_pick.persistent_pre_state == snapshot.boss_pool_rng_states[4]
    assert clean.removed == reference.removed
    assert clean.level_blacklist == reference.level_blacklist


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_caves1_xl_selects_two_distinct_attempt_local_bosses(difficulty: str) -> None:
    seed = next(
        seed
        for seed in range(1, 10_001)
        if derive_caves1_topology_inputs(seed, difficulty).is_xl
    )
    snapshot, reference_b2 = _entry(seed, difficulty)
    clean, reference = _resume(seed, snapshot, reference_b2)
    clean.begin_attempt()
    reference.begin_attempt()
    first = clean.select_canonical_caves_profile()
    first_reference = reference.select_canonical_caves_profile()
    compare_runtime_selection(first, first_reference)
    second = clean.select_canonical_caves_profile()
    second_reference = reference.select_canonical_caves_profile()
    compare_runtime_selection(second, second_reference)
    assert first.selected_entry_id != second.selected_entry_id
    assert second.persistent_pre_state == first.persistent_post_state
    assert len(clean.level_blacklist) == 2
    assert clean.level_blacklist == reference.level_blacklist


def test_caves_pool_all_removed_directed_reset_path() -> None:
    removed = {entry.boss_id for entry in CAVES_BOSSES}
    clean = BossPoolRuntimeState.resume_canonical_caves(
        0x12345678,
        CAVES_BOSSES,
        pool_state=0x3B586A26,
        removed=removed,
    )
    reference = BossPoolRuntimeReference.resume_canonical_caves(
        0x12345678,
        CAVES_REFS,
        pool_state=0x3B586A26,
        removed=removed,
    )
    clean.begin_attempt()
    reference.begin_attempt()
    clean_pick = clean.select_canonical_caves_profile()
    reference_pick = reference.select_canonical_caves_profile()
    compare_runtime_selection(clean_pick, reference_pick)
    assert clean_pick.pool_reset_count == 1
    assert clean_pick.fallback_used
    assert clean.removed == reference.removed == set()
    assert clean.level_blacklist == reference.level_blacklist
