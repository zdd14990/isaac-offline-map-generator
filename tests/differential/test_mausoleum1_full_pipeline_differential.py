"""True clean-vs-reference differential for the Mausoleum1 (Downpour II) layout + tail."""

from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.boss_pool import MAUSOLEUM_POOL_INDEX, load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.mausoleum1_full_pipeline_reference import generate_mausoleum1_full_reference
from isaacmap.mausoleum1_lifecycle import generate_mausoleum1_lifecycle
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config_reference import entries_from_definitions_reference


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
MAUSOLEUM1 = tuple(load_stb(ROOT / "rooms/31.mausoleum.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
_POOLS = load_boss_pool_xml(ROOT / "bosspools.xml")
MAUSOLEUM1_BOSSES = _POOLS["mausoleum"]


def _refs(entries) -> tuple[BossPoolEntryReference, ...]:
    return tuple(
        BossPoolEntryReference(
            item.boss_id, item.weight, item.initial_weight, item.achievement, item.alternate_boss_id
        )
        for item in entries
    )


MAUSOLEUM1_BOSS_REFS = _refs(MAUSOLEUM1_BOSSES)
TAIL_REF_ENTRIES = (
    entries_from_definitions_reference(SPECIAL, stage=0)
    + entries_from_definitions_reference(BLUE_WOMB, stage=13)
)


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7, 11, 23, 47, 71))
def test_mausoleum1_clean_matches_reference(seed: int, difficulty: str) -> None:
    clean = generate_mausoleum1_lifecycle(
        seed,
        difficulty,
        mausoleum1_boss_entries=MAUSOLEUM1_BOSSES,
        special_definitions=SPECIAL,
        mausoleum1_definitions=MAUSOLEUM1,
        blue_womb_definitions=BLUE_WOMB,
    )

    reference = generate_mausoleum1_full_reference(
        seed,
        difficulty,
        mausoleum1_boss_entries=MAUSOLEUM1_BOSS_REFS,
        special_definitions=SPECIAL,
        mausoleum1_definitions=MAUSOLEUM1,
    )

    compare_basement1_full(clean.layout, reference)

    reference_tail = run_post_layout_lifecycle_reference(
        level_rng_state=reference.final_level,
        entries=TAIL_REF_ENTRIES,
        room_config_weights=reference.weights,
        special_room_used_bits=reference.used_bits,
        level_stage=5,
        stage_type=4,
        room_config_stage=31,
    )
    compare_post_layout_lifecycle(clean.post_layout, reference_tail)

    assert clean.next_run_state.completed_level_stage == 5
    assert clean.next_run_state.next_level_stage == 6
    assert clean.next_run_state.boss_pool_rng_states[MAUSOLEUM_POOL_INDEX] == reference.final_boss


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_mausoleum1_mandatory_end_room_block_fires(difficulty: str) -> None:
    """Mausoleum I is outside both first/second-half stage sets (1..4), so
    the alternate-path end room predicates never fire; the M6 leaf still
    records the branch evaluation as an AltEndRoom block with config None."""
    clean = generate_mausoleum1_lifecycle(
        1,
        difficulty,
        mausoleum1_boss_entries=MAUSOLEUM1_BOSSES,
        special_definitions=SPECIAL,
        mausoleum1_definitions=MAUSOLEUM1,
        blue_womb_definitions=BLUE_WOMB,
    )
    attempt = clean.layout.attempts[clean.layout.accepted_attempt_index]
    assert attempt.through_secret is not None
    assert any(block.operation == "AltEndRoom" for block in attempt.through_secret.blocks)
    assert not any(
        block.operation == "AltEndRoom" and block.config is not None
        for block in attempt.through_secret.blocks
    )
