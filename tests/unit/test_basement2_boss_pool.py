from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline import generate_basement1_full
from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement1_full_pipeline_reference import generate_basement1_full_reference
from isaacmap.boss_pool import BossPoolRuntimeState, load_boss_pool_xml
from isaacmap.boss_pool_differential import compare_runtime_selection
from isaacmap.boss_pool_reference import (
    BossPoolEntryReference,
    BossPoolRuntimeReference,
)
from isaacmap.resources import load_stb


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))
BOSSES = load_boss_pool_xml(ROOT / "bosspools.xml")["basement"]
BOSS_REFS = tuple(
    BossPoolEntryReference(
        item.boss_id,
        item.weight,
        item.initial_weight,
        item.achievement,
        item.alternate_boss_id,
    )
    for item in BOSSES
)


def _replay_basement1(seed: int, difficulty: str):
    clean = generate_basement1_full(
        seed,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )
    reference = generate_basement1_full_reference(
        seed,
        difficulty,
        boss_entries=BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )
    compare_basement1_full(clean, reference)
    return clean, reference


def _resume_and_pick(seed: int, clean_b1, reference_b1):
    clean = BossPoolRuntimeState.resume_canonical_basement(
        seed,
        BOSSES,
        pool_state=clean_b1.final_boss_pool_state,
        removed=clean_b1.permanent_removed_bosses,
    )
    reference = BossPoolRuntimeReference.resume_canonical_basement(
        seed,
        BOSS_REFS,
        pool_state=reference_b1.final_boss,
        removed=reference_b1.removed,
    )
    clean.begin_attempt()
    reference.begin_attempt()
    clean_pick = clean.select_canonical_basement_profile()
    reference_pick = reference.select_canonical_basement_profile()
    compare_runtime_selection(clean_pick, reference_pick)
    assert clean.removed == reference.removed
    assert clean.level_blacklist == reference.level_blacklist
    return clean_pick


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_basement2_pick_restores_accepted_basement1_pool_state(difficulty: str) -> None:
    for seed in (1, 2, 7, 10):
        clean_b1, reference_b1 = _replay_basement1(seed, difficulty)
        pick = _resume_and_pick(seed, clean_b1, reference_b1)
        assert pick.selected_entry_id not in clean_b1.permanent_removed_bosses
        assert pick.persistent_pre_state == clean_b1.final_boss_pool_state
        assert len(pick.transitions) >= 8


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_natural_basement2_repick_is_found_from_corpus(difficulty: str) -> None:
    found = None
    for seed in range(1, 21):
        clean_b1, reference_b1 = _replay_basement1(seed, difficulty)
        pick = _resume_and_pick(seed, clean_b1, reference_b1)
        if pick.repick_count:
            found = (seed, clean_b1, pick)
            break
    assert found is not None
    seed, clean_b1, pick = found
    assert seed == 7  # Stable first fixture in the frozen 1..20 corpus.
    assert clean_b1.permanent_removed_bosses == (84,)
    assert pick.selected_entry_id == 56
    assert pick.repick_count == 1
    assert not pick.fallback_used


def test_all_removed_directed_fixture_exercises_pool_clear_and_retry() -> None:
    removed = {entry.boss_id for entry in BOSSES}
    clean = BossPoolRuntimeState.resume_canonical_basement(
        0x12345678,
        BOSSES,
        pool_state=0x3B586A26,
        removed=removed,
    )
    reference = BossPoolRuntimeReference.resume_canonical_basement(
        0x12345678,
        BOSS_REFS,
        pool_state=0x3B586A26,
        removed=removed,
    )
    clean.begin_attempt()
    reference.begin_attempt()
    clean_pick = clean.select_canonical_basement_profile()
    reference_pick = reference.select_canonical_basement_profile()
    compare_runtime_selection(clean_pick, reference_pick)
    assert clean_pick.pool_reset_count == 1
    assert clean_pick.fallback_used
    assert len(clean_pick.transitions) == 9
    assert clean.removed == reference.removed == set()
    assert clean.level_blacklist == reference.level_blacklist == {
        clean_pick.selected_entry_id
    }
