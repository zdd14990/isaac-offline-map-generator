"""Integration tests for the Caves I layout pipeline.

Caves I is `PARTIAL_BINARY` (see ``research/notes/floors/caves1_handoff_audit.md``):

- the accepted-layout composition ``generate_caves1_full`` is exercised as a
  smoke test of the reused Basement leaves, but has no full differential corpus;
- the post-layout lifecycle ``generate_caves1_lifecycle`` fails closed.
"""

from pathlib import Path

import pytest

from isaacmap.basement2_lifecycle import generate_basement2_lifecycle
from isaacmap.caves1_full_pipeline import generate_caves1_full
from isaacmap.caves1_lifecycle import generate_caves1_lifecycle
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.resources import load_stb


ROOT = Path("research/input/extracted_resources/merged/resources")
SPECIAL = tuple(load_stb(ROOT / "rooms/00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOT / "rooms/01.basement.stb"))
CAVES = tuple(load_stb(ROOT / "rooms/04.caves.stb"))
BLUE_WOMB = tuple(load_stb(ROOT / "rooms/13.blue womb.stb"))
BOSSES = load_boss_pool_xml(ROOT / "bosspools.xml")["basement"]
CAVES_BOSSES = load_boss_pool_xml(ROOT / "bosspools.xml")["caves"]


def test_basement_and_caves_boss_lists_differ() -> None:
    """The Caves BossPool must not be seeded from the basement boss list."""
    basement_ids = sorted(entry.boss_id for entry in BOSSES)
    caves_ids = sorted(entry.boss_id for entry in CAVES_BOSSES)
    assert basement_ids != caves_ids
    assert set(caves_ids) == {3, 4, 14, 18, 21, 28, 45, 47, 57, 67, 69, 94}


def _basement2_lifecycle(seed: int, difficulty: str):
    return generate_basement2_lifecycle(
        seed,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        blue_womb_definitions=BLUE_WOMB,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", (1, 2, 5, 7))
def test_caves1_full_layout_composes_from_basement2_snapshot(
    seed: int, difficulty: str
) -> None:
    """The accepted-layout composition completes from a Basement II snapshot."""
    basement2 = _basement2_lifecycle(seed, difficulty)

    caves1 = generate_caves1_full(
        basement2.layout,
        basement2.next_run_state,
        basement_boss_entries=BOSSES,
        caves_boss_entries=CAVES_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        blue_womb_definitions=BLUE_WOMB,
        max_attempts=100,
    )

    assert caves1.completed
    assert caves1.start_seed == seed
    assert caves1.difficulty == difficulty
    assert caves1.attempts
    assert 0 <= caves1.accepted_attempt_index < len(caves1.attempts)
    assert caves1.rooms
    assert len(caves1.room_map) > 0
    assert len(caves1.descriptor_configs) == len(caves1.rooms)


def test_caves1_entry_state_validation() -> None:
    """Caves I rejects an entry snapshot that is not the Stage-3 boundary."""
    basement2 = _basement2_lifecycle(1, "NORMAL")

    # A Basement II snapshot that has not advanced to Stage 3 must be rejected.
    wrong_stage = basement2.next_run_state
    assert wrong_stage.next_level_stage == 3  # correct boundary for Caves I

    # Mismatched completed stage must raise.
    from isaacmap.generation_state import CanonicalRunGenerationSnapshot

    stale = CanonicalRunGenerationSnapshot(
        game_start_seed=wrong_stage.game_start_seed,
        completed_level_stage=1,
        next_level_stage=3,
        boss_pool_rng_states=wrong_stage.boss_pool_rng_states,
        permanent_removed_bosses=wrong_stage.permanent_removed_bosses,
        room_config_weights=wrong_stage.room_config_weights,
        special_room_used_bits=wrong_stage.special_room_used_bits,
        last_floor_level_rng_state=wrong_stage.last_floor_level_rng_state,
        lifecycle="wrong",
    )
    with pytest.raises(ValueError, match="completed_level_stage=2"):
        generate_caves1_full(
            basement2.layout,
            stale,
            basement_boss_entries=BOSSES,
            caves_boss_entries=CAVES_BOSSES,
            special_definitions=SPECIAL,
            basement_definitions=BASEMENT,
            caves_definitions=CAVES,
            blue_womb_definitions=BLUE_WOMB,
        )


def test_caves1_lifecycle_completes_shared_tail() -> None:
    """The shared Stage-3 post-layout tail completes the lifecycle."""
    basement2 = _basement2_lifecycle(1, "NORMAL")
    caves1 = generate_caves1_lifecycle(
        basement2,
        basement_boss_entries=BOSSES,
        caves_boss_entries=CAVES_BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
        caves_definitions=CAVES,
        blue_womb_definitions=BLUE_WOMB,
    )
    assert caves1.completed
    assert caves1.next_run_state.completed_level_stage == 3
    assert caves1.next_run_state.next_level_stage == 4
    # The shared tail advances exactly 28 persistent Level draws and assigns
    # the eight fixed descriptors, matching Basement I/II.
    assert caves1.post_layout.persistent_level_draw_count == 28
    assert len(caves1.post_layout.assignments) == 8
