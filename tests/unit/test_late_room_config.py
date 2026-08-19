from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.basement1_ultra_pipeline import generate_basement1_through_ultra
from isaacmap.basement1_ultra_pipeline_reference import (
    generate_basement1_through_ultra_reference,
)
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.late_room_config import (
    LATE_FAILURE_RVA,
    assign_late_default_room_configs,
    collect_late_default_rooms,
)
from isaacmap.late_room_config_differential import compare_late_default_pass
from isaacmap.late_room_config_reference import (
    assign_late_default_room_configs_reference,
)
from isaacmap.resources import load_stb
from isaacmap.room_config import entries_from_definitions
from isaacmap.room_config_reference import entries_from_definitions_reference


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
ENTRIES = entries_from_definitions(SPECIAL, stage=0) + entries_from_definitions(
    BASEMENT, stage=1
)
ENTRY_REFS = entries_from_definitions_reference(
    SPECIAL, stage=0
) + entries_from_definitions_reference(BASEMENT, stage=1)


def _run(seed: int, difficulty: str):
    clean_m7 = generate_basement1_through_ultra(
        seed,
        difficulty,
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )
    reference_m7 = generate_basement1_through_ultra_reference(
        seed,
        difficulty,
        boss_entries=BOSS_REFS,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )
    clean_attempt = clean_m7.through_secret.attempts[-1]
    reference_attempt = reference_m7.through_secret.attempts[-1]
    clean_final = clean_m7.final
    reference_final = reference_m7.final
    assert clean_final is not None and reference_final is not None
    clean = assign_late_default_room_configs(
        rooms=clean_final.rooms,
        non_dead_ends=clean_attempt.topology.non_dead_ends,
        dead_ends=clean_final.dead_ends,
        descriptor_configs=clean_final.descriptor_configs,
        entries=ENTRIES,
        room_config_weights=clean_final.final_room_config_weights,
        level_rng_state=clean_final.final_level_rng_state,
        difficulty=difficulty,
    )
    reference = assign_late_default_room_configs_reference(
        rooms=reference_final.rooms,
        non_dead_ends=reference_attempt.topology_signature[3],
        dead_ends=reference_final.dead_ends,
        descriptor_configs=reference_final.descriptor_configs,
        entries=ENTRY_REFS,
        room_config_weights=reference_final.weights,
        level_rng_state=reference_final.final_level,
        difficulty=difficulty,
    )
    compare_late_default_pass(clean, reference)
    return clean


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("seed", range(1, 11))
def test_late_pass_matches_independent_reference(seed: int, difficulty: str) -> None:
    result = _run(seed, difficulty)
    if result.completed:
        assert all(room.variant >= 0 for room in result.rooms)
        assert len(result.descriptor_configs) == len(result.rooms)


def test_collection_is_non_dead_then_remaining_dead_ends() -> None:
    assert collect_late_default_rooms((0, 2, 4), (7, 5)) == (0, 2, 4, 7, 5)
    with pytest.raises(ValueError):
        collect_late_default_rooms((0, 2), (2, 3))


def test_missing_compatible_config_fails_without_excluded_advances() -> None:
    m7 = generate_basement1_through_ultra(
        1,
        "NORMAL",
        boss_entries=BOSSES,
        special_definitions=SPECIAL,
        basement_definitions=BASEMENT,
    )
    final = m7.final
    attempt = m7.through_secret.attempts[-1]
    assert final is not None
    # Keep the fixed Start entry but remove every stage-1 ROOM_DEFAULT entry.
    insufficient = tuple(entry for entry in ENTRIES if entry.key.stage == 0)
    result = assign_late_default_room_configs(
        rooms=final.rooms,
        non_dead_ends=attempt.topology.non_dead_ends,
        dead_ends=final.dead_ends,
        descriptor_configs=final.descriptor_configs,
        entries=insufficient,
        room_config_weights=final.final_room_config_weights,
        level_rng_state=final.final_level_rng_state,
        difficulty="NORMAL",
    )
    assert not result.completed
    assert result.abort_rva == LATE_FAILURE_RVA
    assert result.abort_room_id == result.collection_order[1]
    assert result.excluded_room_advance_count == 0
    assert len(result.level_rng_transitions) == 1
