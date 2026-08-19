"""Independent clean/reference differential for the pre-late M7 boundary."""

from __future__ import annotations

from .basement1_pipeline_differential import _key, _room, _selection
from .basement1_secret_pipeline_differential import compare_secret_pipeline
from .basement1_ultra_pipeline import Basement1ThroughUltraResult
from .basement1_ultra_pipeline_reference import (
    ReferenceBasement1ThroughUltraResult,
)


def _clean_geometry(result) -> tuple[object, ...]:
    return (
        result.room_id,
        result.grid_index,
        result.forbidden_indices,
        result.best_candidates,
        result.best_score,
        tuple(
            (
                item.grid_index,
                item.occupied,
                item.forbidden,
                item.blocked,
                item.base_score,
                item.immediate_mask,
                item.outer_neighbor_mask,
                item.adjacency_count,
                item.invalid_red_door_targets,
                item.final_score,
                item.best_action,
            )
            for item in result.evaluations
        ),
        tuple(
            (
                draw.pre_state,
                draw.post_state,
                "selection" if "select among" in draw.reason else "candidate",
                draw.result,
            )
            for draw in result.rng_transitions
        ),
        result.final_generator_rng_state,
        tuple(
            (
                item.room_id,
                item.door_slot,
                item.target_grid_index,
                item.ultra_grid_index,
            )
            for item in result.red_door_writes
        ),
    )


def _reference_geometry(result) -> tuple[object, ...]:
    return (
        result.room_id,
        result.grid_index,
        result.forbidden,
        result.best,
        result.best_score,
        tuple(
            (
                item.index,
                item.occupied,
                item.forbidden,
                item.blocked,
                item.base,
                item.immediate_mask,
                item.ring_mask,
                item.count,
                item.invalid_targets,
                item.score,
                item.action,
            )
            for item in result.evaluations
        ),
        result.transitions,
        result.final_rng,
        result.red_writes,
    )


def compare_ultra_pipeline(
    clean: Basement1ThroughUltraResult,
    reference: ReferenceBasement1ThroughUltraResult,
) -> None:
    compare_secret_pipeline(clean.through_secret, reference.through_secret)
    assert clean.boundary_completed == reference.boundary_completed, "M7 boundary"
    assert (clean.final is None) == (reference.final is None), "M7 result presence"
    if clean.final is None or reference.final is None:
        return
    final = clean.final
    expected = reference.final
    assert final.ultra_room == expected.ultra_room, "Ultra room id"
    assert _key(final.ultra_config) == _key(expected.ultra_config), "Ultra config"
    assert tuple(_room(room) for room in final.rooms) == tuple(
        _room(room) for room in expected.rooms
    ), "post-Ultra rooms"
    assert final.room_map == expected.room_map, "post-Ultra room map"
    assert final.dead_ends == expected.dead_ends, "post-Ultra dead ends"
    assert final.blocked_positions == expected.blocked_positions, "blocked positions"
    assert tuple((room_id, _key(key)) for room_id, key in final.descriptor_configs) == tuple(
        (room_id, _key(key)) for room_id, key in expected.descriptor_configs
    ), "descriptor configs"
    assert (
        final.ultra_config_rng.pre_state,
        final.ultra_config_rng.post_state,
        final.ultra_config_rng.shift_index,
    ) == expected.config_rng, "index-71 config RNG"
    assert tuple(_selection(item) for item in final.ultra_config_selections) == tuple(
        _selection(item) for item in expected.selections
    ), "Ultra RoomConfig selection"
    assert _clean_geometry(final.ultra_geometry) == _reference_geometry(
        expected.geometry
    ), "Ultra geometry"
    assert final.final_level_rng_state == expected.final_level, "final Level RNG"
    assert final.final_generator_rng_state == expected.final_generator, "final generator RNG"
    assert tuple((_key(key), value) for key, value in final.final_room_config_weights) == tuple(
        (_key(key), value) for key, value in expected.weights
    ), "final weights"
    assert final.special_room_used_bits == expected.used_bits, "used bits"

    before_count = len(clean.through_secret.attempts[-1].through_secret.descriptor_configs)
    created = expected.ultra_room >= 0
    mutation = final.ultra_descriptor
    assert (
        mutation.created,
        mutation.generator_room_id,
        mutation.list_index,
        mutation.grid_index,
        mutation.safe_grid_index,
        mutation.room_shape,
        mutation.room_type,
        mutation.descriptor_count_before,
        mutation.descriptor_count_after,
        mutation.dead_ends_before,
        mutation.dead_ends_after,
        mutation.level_descriptor_tail_field,
    ) == (
        created,
        expected.ultra_room,
        before_count if created else -1,
        expected.geometry.grid_index,
        expected.geometry.grid_index,
        1 if created else 0,
        29 if created else 0,
        before_count,
        before_count + (1 if created else 0),
        expected.dead_ends,
        expected.dead_ends,
        99 if created else None,
    ), "Ultra descriptor mutation"

