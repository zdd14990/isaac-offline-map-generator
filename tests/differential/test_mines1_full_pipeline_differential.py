"""True clean-vs-reference differential for the Mines I layout + tail."""

from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_full_pipeline_differential import compare_basement1_full
from isaacmap.boss_pool import MINES_POOL_INDEX, load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.floor_init import derive_alt_topology_inputs
from isaacmap.mines1_full_pipeline_reference import generate_mines1_full_reference
from isaacmap.mines1_lifecycle import generate_mines1_lifecycle
from isaacmap.post_layout_lifecycle_differential import compare_post_layout_lifecycle
from isaacmap.post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from isaacmap.resources import load_stb
from isaacmap.room_config_reference import entries_from_definitions_reference


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
MINES1 = tuple(load_stb(ROOT / "rooms/29.mines.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
_POOLS = load_boss_pool_xml(ROOT / "bosspools.xml")
MINES1_BOSSES = _POOLS["mines"]


def _refs(entries) -> tuple[BossPoolEntryReference, ...]:
    return tuple(
        BossPoolEntryReference(
            item.boss_id, item.weight, item.initial_weight, item.achievement, item.alternate_boss_id
        )
        for item in entries
    )


MINES1_BOSS_REFS = _refs(MINES1_BOSSES)
TAIL_REF_ENTRIES = (
    entries_from_definitions_reference(SPECIAL, stage=0)
    + entries_from_definitions_reference(BLUE_WOMB, stage=13)
)


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7, 11, 23, 47, 71))
def test_mines1_clean_matches_reference(seed: int, difficulty: str) -> None:
    clean = generate_mines1_lifecycle(
        seed,
        difficulty,
        mines1_boss_entries=MINES1_BOSSES,
        special_definitions=SPECIAL,
        mines1_definitions=MINES1,
        blue_womb_definitions=BLUE_WOMB,
    )

    reference = generate_mines1_full_reference(
        seed,
        difficulty,
        mines1_boss_entries=MINES1_BOSS_REFS,
        special_definitions=SPECIAL,
        mines1_definitions=MINES1,
    )

    compare_basement1_full(clean.layout, reference)

    reference_tail = run_post_layout_lifecycle_reference(
        level_rng_state=reference.final_level,
        entries=TAIL_REF_ENTRIES,
        room_config_weights=reference.weights,
        special_room_used_bits=reference.used_bits,
        level_stage=3,
        stage_type=4,
        room_config_stage=29,
    )
    compare_post_layout_lifecycle(clean.post_layout, reference_tail)

    assert clean.next_run_state.completed_level_stage == 3
    assert clean.next_run_state.next_level_stage == 4
    assert clean.next_run_state.boss_pool_rng_states[MINES_POOL_INDEX] == reference.final_boss


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
def test_mines1_mandatory_end_room_block_fires(difficulty: str) -> None:
    """Mines I evaluates the alternate-path end room block (second-half,
    0x0033C4D1..0x0033C69E) but never places it: the second-half branch
    additionally requires collectible 626, which the canonical run lacks, so
    the block is present with config None (binary-accurate skip).  Even on XL
    floors (Labyrinth-eligible odd stage) the 626 gate keeps it a no-op."""
    clean = generate_mines1_lifecycle(
        1,
        difficulty,
        mines1_boss_entries=MINES1_BOSSES,
        special_definitions=SPECIAL,
        mines1_definitions=MINES1,
        blue_womb_definitions=BLUE_WOMB,
    )
    attempt = clean.layout.attempts[clean.layout.accepted_attempt_index]
    assert attempt.through_secret is not None
    assert any(block.operation == "AltEndRoom" for block in attempt.through_secret.blocks)
    assert not any(
        block.operation == "AltEndRoom" and block.config is not None
        for block in attempt.through_secret.blocks
    )


@pytest.mark.parametrize("difficulty,seed", (("NORMAL", 787), ("HARD", 229)))
def test_mines1_natural_xl_matches_reference(difficulty: str, seed: int) -> None:
    inputs = derive_alt_topology_inputs(3, 4, seed, difficulty)
    assert inputs.is_xl
    clean = generate_mines1_lifecycle(
        seed,
        difficulty,
        mines1_boss_entries=MINES1_BOSSES,
        special_definitions=SPECIAL,
        mines1_definitions=MINES1,
        blue_womb_definitions=BLUE_WOMB,
    )
    reference = generate_mines1_full_reference(
        seed,
        difficulty,
        mines1_boss_entries=MINES1_BOSS_REFS,
        special_definitions=SPECIAL,
        mines1_definitions=MINES1,
    )
    compare_basement1_full(clean.layout, reference)
    assert clean.layout.attempts[clean.layout.accepted_attempt_index].target_room_count == (
        inputs.target_room_count
    )
