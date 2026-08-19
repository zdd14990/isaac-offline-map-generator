"""True clean-vs-reference differential for the Ashpit (Downpour II) layout + tail."""

from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.boss_pool import ASHPIT_POOL_INDEX, load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.ashpit_full_pipeline_reference import generate_ashpit_full_reference
from isaacmap.ashpit_lifecycle import generate_ashpit_lifecycle
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config_reference import entries_from_definitions_reference


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
ASHPIT = tuple(load_stb(ROOT / "rooms/30.ashpit.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
_POOLS = load_boss_pool_xml(ROOT / "bosspools.xml")
ASHPIT_BOSSES = _POOLS["ashpit"]


def _refs(entries) -> tuple[BossPoolEntryReference, ...]:
    return tuple(
        BossPoolEntryReference(
            item.boss_id, item.weight, item.initial_weight, item.achievement, item.alternate_boss_id
        )
        for item in entries
    )


ASHPIT_BOSS_REFS = _refs(ASHPIT_BOSSES)
TAIL_REF_ENTRIES = (
    entries_from_definitions_reference(SPECIAL, stage=0)
    + entries_from_definitions_reference(BLUE_WOMB, stage=13)
)


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7, 11, 23, 47, 71))
def test_ashpit_clean_matches_reference(seed: int, difficulty: str) -> None:
    clean = generate_ashpit_lifecycle(
        seed,
        difficulty,
        ashpit_boss_entries=ASHPIT_BOSSES,
        special_definitions=SPECIAL,
        ashpit_definitions=ASHPIT,
        blue_womb_definitions=BLUE_WOMB,
    )

    reference = generate_ashpit_full_reference(
        seed,
        difficulty,
        ashpit_boss_entries=ASHPIT_BOSS_REFS,
        special_definitions=SPECIAL,
        ashpit_definitions=ASHPIT,
    )

    compare_basement1_full(clean.layout, reference)

    reference_tail = run_post_layout_lifecycle_reference(
        level_rng_state=reference.final_level,
        entries=TAIL_REF_ENTRIES,
        room_config_weights=reference.weights,
        special_room_used_bits=reference.used_bits,
        level_stage=4,
        stage_type=5,
        room_config_stage=30,
    )
    compare_post_layout_lifecycle(clean.post_layout, reference_tail)

    assert clean.next_run_state.completed_level_stage == 4
    assert clean.next_run_state.next_level_stage == 5
    assert clean.next_run_state.boss_pool_rng_states[ASHPIT_POOL_INDEX] == reference.final_boss


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_ashpit_mandatory_end_room_block_fires(difficulty: str) -> None:
    """Ashpit evaluates the alternate-path end room block (second-half,
    0x0033C4D1..0x0033C69E) but never places it: the second-half branch
    additionally requires collectible 626, which the canonical run lacks, so
    the block is present with config None (binary-accurate skip)."""
    clean = generate_ashpit_lifecycle(
        1,
        difficulty,
        ashpit_boss_entries=ASHPIT_BOSSES,
        special_definitions=SPECIAL,
        ashpit_definitions=ASHPIT,
        blue_womb_definitions=BLUE_WOMB,
    )
    attempt = clean.layout.attempts[clean.layout.accepted_attempt_index]
    assert attempt.through_secret is not None
    assert any(block.operation == "AltEndRoom" for block in attempt.through_secret.blocks)
    assert not any(
        block.operation == "AltEndRoom" and block.config is not None
        for block in attempt.through_secret.blocks
    )
