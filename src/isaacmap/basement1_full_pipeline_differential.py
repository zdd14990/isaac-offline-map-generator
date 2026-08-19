"""Deep clean/reference differential for the accepted Basement I layout."""

from __future__ import annotations

from .basement1_full_pipeline import Basement1FullResult
from .basement1_full_pipeline_reference import ReferenceBasement1FullResult
from .basement1_pipeline_differential import (
    _key,
    _post_clean,
    _post_reference,
    _room,
    _selection,
    _topology_clean,
)
from .basement1_secret_pipeline_differential import _m6
from .basement1_ultra_pipeline_differential import (
    _clean_geometry,
    _reference_geometry,
)
from .late_room_config_differential import compare_late_default_pass


def _ultra_clean(value) -> tuple[object, ...]:
    return (
        value.ultra_room,
        _key(value.ultra_config),
        tuple(_room(room) for room in value.rooms),
        value.room_map,
        value.dead_ends,
        value.blocked_positions,
        tuple((room_id, _key(key)) for room_id, key in value.descriptor_configs),
        (
            value.ultra_config_rng.pre_state,
            value.ultra_config_rng.post_state,
            value.ultra_config_rng.shift_index,
        ),
        tuple(_selection(item) for item in value.ultra_config_selections),
        _clean_geometry(value.ultra_geometry),
        value.final_level_rng_state,
        value.final_generator_rng_state,
        tuple((_key(key), weight) for key, weight in value.final_room_config_weights),
        value.special_room_used_bits,
    )


def _ultra_reference(value) -> tuple[object, ...]:
    return (
        value.ultra_room,
        _key(value.ultra_config),
        tuple(_room(room) for room in value.rooms),
        value.room_map,
        value.dead_ends,
        value.blocked_positions,
        tuple((room_id, _key(key)) for room_id, key in value.descriptor_configs),
        value.config_rng,
        tuple(_selection(item) for item in value.selections),
        _reference_geometry(value.geometry),
        value.final_level,
        value.final_generator,
        tuple((_key(key), weight) for key, weight in value.weights),
        value.used_bits,
    )


def compare_basement1_full(
    clean: Basement1FullResult, reference: ReferenceBasement1FullResult
) -> None:
    assert clean.completed == reference.completed, "full completion"
    assert len(clean.attempts) == len(reference.attempts), "full attempt count"
    for actual, expected in zip(clean.attempts, reference.attempts):
        prefix = f"attempt {actual.attempt}: "
        assert actual.attempt == expected.attempt
        assert actual.target_room_count == expected.target, prefix + "target"
        assert actual.topology_usable == expected.usable, prefix + "usable"
        assert _topology_clean(actual) == expected.topology_signature, prefix + "topology"
        assert (
            actual.start_level_rng_state,
            actual.end_level_rng_state,
        ) == (expected.start_level, expected.end_level), prefix + "Level RNG"
        assert (
            actual.start_generator_rng_state,
            actual.end_generator_rng_state,
        ) == (expected.start_generator, expected.end_generator), prefix + "generator RNG"
        assert (
            actual.start_boss_pool_state,
            actual.end_boss_pool_state,
        ) == (expected.start_boss, expected.end_boss), prefix + "BossPool RNG"
        assert (actual.used_bits_before, actual.used_bits_after) == (
            expected.used_before,
            expected.used_after,
        ), prefix + "used bits"
        assert tuple(
            (_key(key), old, new)
            for key, old, new in actual.room_config_mutations
        ) == tuple(
            (_key(key), old, new)
            for key, old, new in expected.weight_mutations
        ), prefix + "weights"
        assert actual.abort_operation == expected.abort, prefix + "abort"
        assert (actual.through_treasure is None) == (
            expected.through_treasure is None
        ), prefix + "M5 presence"
        if actual.through_treasure is not None:
            assert _post_clean(actual.through_treasure) == _post_reference(
                expected.through_treasure
            ), prefix + "M5"
        assert (actual.through_secret is None) == (
            expected.through_secret is None
        ), prefix + "M6 presence"
        if actual.through_secret is not None:
            assert _m6(actual.through_secret) == _m6(
                expected.through_secret
            ), prefix + "M6"
        assert (actual.through_ultra is None) == (
            expected.through_ultra is None
        ), prefix + "M7 presence"
        if actual.through_ultra is not None:
            assert _ultra_clean(actual.through_ultra) == _ultra_reference(
                expected.through_ultra
            ), prefix + "M7"
        assert (actual.late_default is None) == (
            expected.late_default is None
        ), prefix + "late presence"
        if actual.late_default is not None:
            compare_late_default_pass(actual.late_default, expected.late_default)

    assert clean.accepted_attempt_index == reference.accepted_attempt_index
    assert tuple(_room(room) for room in clean.rooms) == tuple(
        _room(room) for room in reference.rooms
    ), "accepted rooms"
    assert clean.room_map == reference.room_map, "accepted room map"
    assert tuple((room_id, _key(key)) for room_id, key in clean.descriptor_configs) == tuple(
        (room_id, _key(key)) for room_id, key in reference.descriptors
    ), "accepted descriptors"
    assert clean.final_level_rng_state == reference.final_level
    assert clean.final_generator_rng_state == reference.final_generator
    assert clean.final_boss_pool_state == reference.final_boss
    assert clean.permanent_removed_bosses == reference.removed
    assert clean.pending_boss_blacklist == reference.pending_blacklist
    assert tuple((_key(key), weight) for key, weight in clean.final_room_config_weights) == tuple(
        (_key(key), weight) for key, weight in reference.weights
    )
    assert clean.final_special_room_used_bits == reference.used_bits
