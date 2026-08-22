from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline import (
    EXTERNAL_VALIDATION,
    FULL_LAYOUT_STATUS,
    generate_basement1_full,
)
from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.basement1_full_pipeline_reference import (
    generate_basement1_full_reference,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.resources import load_stb
from isaacmap.seed import decode_seed


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


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", range(1, 11))
def test_full_pipeline_matches_reference(seed: int, difficulty: str) -> None:
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
    assert clean.completed
    assert clean.generation_status == FULL_LAYOUT_STATUS
    assert clean.external_validation == EXTERNAL_VALIDATION
    assert clean.pending_boss_blacklist == ()
    assert len(clean.rooms) == len(clean.descriptor_configs)
    assert all(room.variant >= 0 and room.subtype >= 0 for room in clean.rooms)


def test_boss_blacklist_commits_only_after_late_success() -> None:
    result = generate_basement1_full(
        1,
        "NORMAL",
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )
    assert len(result.attempts) == 2
    assert result.attempts[0].abort_operation == "Treasure geometry"
    assert result.attempts[1].late_default is not None
    assert result.attempts[1].late_default.completed
    assert result.pending_boss_blacklist == ()
    accepted_boss = result.attempts[-1].through_treasure.boss_selection.selected_entry_id
    assert result.permanent_removed_bosses == (accepted_boss,)


def test_qqtt_fqpg_hard_full_pipeline_matches_independent_reference() -> None:
    start_seed = decode_seed("QQTT FQPG")
    clean = generate_basement1_full(
        start_seed,
        "HARD",
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )
    reference = generate_basement1_full_reference(
        start_seed,
        "HARD",
        boss_entries=BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )

    compare_basement1_full(clean, reference)
    assert clean.completed
