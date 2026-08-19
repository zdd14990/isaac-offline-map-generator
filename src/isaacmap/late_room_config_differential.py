"""Clean/reference comparator for the late ordinary RoomConfig leaf."""

from __future__ import annotations

from .basement1_pipeline_differential import _key, _room, _selection
from .late_room_config import LateDefaultPassResult
from .late_room_config_reference import ReferenceLateDefaultResult


def compare_late_default_pass(
    clean: LateDefaultPassResult, reference: ReferenceLateDefaultResult
) -> None:
    assert clean.completed == reference.completed, "late completion"
    assert clean.abort_room_id == reference.abort_room_id, "late abort room"
    assert clean.collection_order == reference.order, "late collection order"
    assert clean.excluded_room_advance_count == reference.excluded_count, "excluded count"
    assert clean.final_level_rng_state == reference.final_level, "late Level RNG"
    assert tuple(_room(room) for room in clean.rooms) == tuple(
        _room(room) for room in reference.rooms
    ), "late rooms"
    assert tuple((room_id, _key(key)) for room_id, key in clean.descriptor_configs) == tuple(
        (room_id, _key(key)) for room_id, key in reference.descriptors
    ), "late descriptors"
    assert tuple((_key(key), weight) for key, weight in clean.final_room_config_weights) == tuple(
        (_key(key), weight) for key, weight in reference.weights
    ), "late weights"
    assert tuple(
        (
            item.pre_state,
            item.post_state,
            item.room_id,
            "selector" if item.room_id >= 0 else "excluded",
        )
        for item in clean.level_rng_transitions
    ) == reference.transitions, "late Level RNG transitions"
    assert tuple(
        (
            item.room_id,
            item.grid_index,
            item.required_doors,
            item.minimum_difficulty,
            item.maximum_difficulty,
            _key(item.config),
            item.fixed_start_config,
            None if item.selection is None else _selection(item.selection),
        )
        for item in clean.assignments
    ) == tuple(
        (
            item.room_id,
            item.grid_index,
            item.required_doors,
            item.minimum_difficulty,
            item.maximum_difficulty,
            _key(item.config),
            item.fixed,
            None if item.selection is None else _selection(item.selection),
        )
        for item in reference.assignments
    ), "late assignments"
