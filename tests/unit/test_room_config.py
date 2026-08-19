from __future__ import annotations

from pathlib import Path

from isaacmap.resources import load_stb
from isaacmap.room_config import (
    RoomConfigMutableState,
    RoomConfigQuery,
    entries_from_definitions,
    select_room,
    select_room_with_stage_fallback,
)
from isaacmap.room_config_reference import (
    RoomConfigMutableStateReference,
    RoomConfigQueryReference,
    entries_from_definitions_reference,
    room_definition_door_mask,
    select_room_reference,
    select_room_with_stage_fallback_reference,
)


ROOM_ROOT = Path("research/input/extracted_resources/merged/resources/rooms")
SPECIAL = tuple(load_stb(ROOM_ROOT / "00.special rooms.stb"))
BASEMENT = tuple(load_stb(ROOM_ROOT / "01.basement.stb"))


def _selection_signature(selection):
    entry = selection.entry if hasattr(selection, "entry") else selection.selected
    keys = selection.candidate_keys if hasattr(selection, "candidate_keys") else selection.all_candidates
    exact = selection.exact_door_keys if hasattr(selection, "exact_door_keys") else selection.exact_door_candidates
    used = selection.used_exact_doors if hasattr(selection, "used_exact_doors") else selection.selected_from_exact_doors
    draws = selection.draws
    return (
        tuple((k.stage, k.mode, k.resource_index) for k in keys),
        tuple((k.stage, k.mode, k.resource_index) for k in exact),
        used,
        None if entry is None else (
            entry.key.stage, entry.key.mode, entry.key.resource_index,
            entry.room_type, entry.variant, entry.subtype, entry.shape,
        ),
        selection.old_weight if hasattr(selection, "old_weight") else selection.selected_old_weight,
        selection.new_weight if hasattr(selection, "new_weight") else selection.selected_new_weight,
        tuple((d.binary_rva, d.pre_state, d.post_state, d.reason, d.result_float) for d in draws),
    )


def test_every_installed_room_door_coordinate_has_a_binary_slot() -> None:
    for path in ROOM_ROOT.glob("*.stb"):
        for room in load_stb(path):
            room_definition_door_mask(room)


def test_room_config_selector_clean_matches_mechanical_reference() -> None:
    clean_entries = entries_from_definitions(SPECIAL, stage=0)
    reference_entries = entries_from_definitions_reference(SPECIAL, stage=0)
    for seed in range(1, 1001):
        clean_state = RoomConfigMutableState()
        reference_state = RoomConfigMutableStateReference()
        clean_state.reset(clean_entries)
        reference_state.reset_pool(reference_entries)
        clean_query = RoomConfigQuery(seed, True, 0, 8, subtype=-1)
        reference_query = RoomConfigQueryReference(seed, True, 0, 8, subtype=-1)
        clean = select_room(clean_entries, clean_state, clean_query)
        reference = select_room_reference(reference_entries, reference_state, reference_query)
        assert _selection_signature(clean) == _selection_signature(reference), f"seed={seed}"
        assert tuple(sorted((k.stage, k.mode, k.resource_index, v) for k, v in clean_state.weights.items())) == tuple(
            sorted((k.stage, k.mode, k.resource_index, v) for k, v in reference_state.weights.items())
        )


def test_stage_fallback_reuses_numeric_seed_and_only_decays_selected_pool() -> None:
    clean_entries = entries_from_definitions(SPECIAL, stage=0) + entries_from_definitions(BASEMENT, stage=1)
    reference_entries = entries_from_definitions_reference(SPECIAL, stage=0) + entries_from_definitions_reference(BASEMENT, stage=1)
    clean_state = RoomConfigMutableState()
    reference_state = RoomConfigMutableStateReference()
    clean_state.reset(clean_entries)
    reference_state.reset_pool(reference_entries)
    clean_query = RoomConfigQuery(0x12345678, True, 1, 4, subtype=0)
    reference_query = RoomConfigQueryReference(0x12345678, True, 1, 4, subtype=0)
    clean = select_room_with_stage_fallback(clean_entries, clean_state, clean_query, 0)
    reference = select_room_with_stage_fallback_reference(reference_entries, reference_state, reference_query, 0)
    assert len(clean) == len(reference) == 2
    assert clean[0].entry is None and reference[0].selected is None
    assert clean[1].draws[0].pre_state == reference[1].draws[0].pre_state == 0x12345678
    assert _selection_signature(clean[1]) == _selection_signature(reference[1])


def test_required_doors_uses_second_draw_and_exact_subset_gate() -> None:
    clean_entries = entries_from_definitions(SPECIAL, stage=0)
    reference_entries = entries_from_definitions_reference(SPECIAL, stage=0)
    clean_state = RoomConfigMutableState()
    reference_state = RoomConfigMutableStateReference()
    clean_state.reset(clean_entries)
    reference_state.reset_pool(reference_entries)
    clean = select_room(clean_entries, clean_state, RoomConfigQuery(0x87654321, True, 0, 4, required_doors=1))
    reference = select_room_reference(reference_entries, reference_state, RoomConfigQueryReference(0x87654321, True, 0, 4, required_doors=1))
    assert len(clean.draws) == len(reference.draws) == 2
    assert _selection_signature(clean) == _selection_signature(reference)


def test_weight_decay_persists_across_attempts_until_level_init_reset() -> None:
    entries = entries_from_definitions(SPECIAL, stage=0)
    state = RoomConfigMutableState()
    state.reset(entries)
    query = RoomConfigQuery(0x11223344, True, 0, 8)
    first = select_room(entries, state, query)
    assert first.entry is not None
    decayed = state.weight(first.entry)
    assert decayed == first.new_weight and decayed < first.old_weight
    # A generation-attempt abort does not call ResetRoomWeights.
    assert state.weight(first.entry) == decayed
    # Level::Init before a new floor does.
    state.reset(entries)
    assert state.weight(first.entry) == first.entry.initial_weight
