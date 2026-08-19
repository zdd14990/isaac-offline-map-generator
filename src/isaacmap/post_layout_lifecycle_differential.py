"""Comparator for clean/reference Basement I post-layout lifecycle leaves."""

from __future__ import annotations

from .basement1_pipeline_differential import _key, _selection
from .post_layout_lifecycle import PostLayoutLifecycleResult
from .post_layout_lifecycle_reference import ReferencePostLayoutLifecycle


def compare_post_layout_lifecycle(
    clean: PostLayoutLifecycleResult, reference: ReferencePostLayoutLifecycle
) -> None:
    assert clean.completed
    assert clean.persistent_level_draw_count == reference.persistent_draws
    assert clean.final_level_rng_state == reference.final_level
    assert clean.final_special_room_used_bits == reference.used_bits
    assert clean.skipped_optional_grid_indices == reference.skipped
    assert tuple(
        (item.binary_rva, item.identity, item.pre_state, item.post_state, item.reason)
        for item in clean.rng_transitions
    ) == reference.transitions
    assert tuple((_key(key), value) for key, value in clean.final_room_config_weights) == tuple(
        (_key(key), value) for key, value in reference.weights
    )
    assert tuple(
        (
            item.grid_index,
            item.room_type,
            item.subtype,
            item.descriptor_seeds,
            item.selector_seed,
            _key(item.config),
            _selection(item.selection),
        )
        for item in clean.assignments
    ) == tuple(
        (
            item.grid_index,
            item.room_type,
            item.subtype,
            item.seeds,
            item.selector_seed,
            _key(item.config),
            _selection(item.selection),
        )
        for item in reference.assignments
    )
