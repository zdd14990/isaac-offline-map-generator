"""Deep clean/reference differential for the M6 pre-Ultra boundary."""

from __future__ import annotations

from .basement1_pipeline_differential import (
    _key,
    _post_clean,
    _post_reference,
    _room,
    _selection,
    _topology_clean,
)
from .basement1_secret_pipeline import Basement1ThroughSecretResult
from .basement1_secret_pipeline_reference import ReferenceBasement1ThroughSecretResult


def _draw(draw) -> tuple[object, ...]:
    identity = draw.object_identity if hasattr(draw, "object_identity") else draw.identity
    if identity.startswith("RoomConfig::select_room.local("):
        identity = "RoomConfig.local(" + identity.removeprefix("RoomConfig::select_room.local(")
    return (
        getattr(draw, "binary_rva", getattr(draw, "rva", None)),
        identity,
        draw.shift_index,
        getattr(draw, "pre_state", getattr(draw, "pre", None)),
        getattr(draw, "post_state", getattr(draw, "post", None)),
    )


def _condition(condition) -> tuple[object, ...]:
    return condition.binary_range, condition.condition, condition.value, condition.consequence


def _block(block) -> tuple[object, ...]:
    return (
        block.operation, block.binary_range, block.room_type, block.subtype,
        block.candidate_before, block.candidate_room, block.assigned,
        block.candidate_after,
        None if block.config is None else _key(block.config),
        block.predicate, block.persistent_bit_write,
    )


def _geometry(result) -> tuple[object, ...]:
    return (
        result.room_id, result.grid_index, result.forbidden_indices,
        result.best_candidates, result.best_score,
        tuple((
            item.grid_index, item.occupied, item.forbidden, item.blocked,
            item.base_score, item.neighbor_mask, item.adjacency_count,
            item.final_score, item.best_action,
        ) for item in result.evaluations),
        tuple((d.binary_rva, d.object_identity, d.shift_index, d.pre_state, d.post_state, d.reason, d.result) for d in result.rng_transitions),
        result.final_generator_rng_state, result.connection_refresh_order,
    )


def _m6(result) -> tuple[object, ...]:
    return (
        result.completed, result.abort_operation,
        tuple(_block(block) for block in result.blocks),
        result.secret_room,
        None if result.secret_config is None else _key(result.secret_config),
        tuple(_room(room) for room in result.rooms), result.room_map, result.dead_ends,
        tuple((room_id, _key(key)) for room_id, key in result.descriptor_configs),
        tuple(_draw(draw) for draw in result.rng_draws),
        tuple((trace.operation, tuple(_selection(selection) for selection in trace.selections)) for trace in result.config_traces),
        tuple((trace.operation, trace.candidate_order, trace.tested_room, trace.accepted, trace.dead_ends_after) for trace in result.candidate_traces),
        tuple(_condition(condition) for condition in result.conditions),
        tuple((item.iteration, item.binary_rva, item.pre_state, item.post_state, item.shift_index, item.reason) for item in result.secret_config_rng),
        _geometry(result.secret_geometry),
        (
            result.secret_descriptor.created, result.secret_descriptor.generator_room_id,
            result.secret_descriptor.list_index, result.secret_descriptor.grid_index,
            result.secret_descriptor.safe_grid_index, result.secret_descriptor.room_shape,
            result.secret_descriptor.room_type,
            result.secret_descriptor.descriptor_count_before,
            result.secret_descriptor.descriptor_count_after,
            result.secret_descriptor.dead_ends_before,
            result.secret_descriptor.dead_ends_after,
        ),
        result.final_level_rng_state,
        result.final_generator_rng_state, result.used_bits_after,
    )


def compare_secret_pipeline(
    clean: Basement1ThroughSecretResult,
    reference: ReferenceBasement1ThroughSecretResult,
) -> None:
    assert clean.boundary_completed == reference.boundary_completed, "boundary completion"
    assert len(clean.attempts) == len(reference.attempts), "attempt count"
    for ca, ra in zip(clean.attempts, reference.attempts):
        prefix = f"attempt {ca.attempt}: "
        assert ca.attempt == ra.attempt
        assert ca.target_room_count == ra.target_room_count, prefix + "target count"
        assert ca.topology_usable == ra.usable, prefix + "topology usable"
        assert _topology_clean(ca) == ra.topology_signature, prefix + "topology"
        assert (ca.start_level_rng_state, ca.end_level_rng_state) == (ra.start_level, ra.end_level), prefix + "Level RNG"
        assert (ca.start_generator_rng_state, ca.end_generator_rng_state) == (ra.start_generator, ra.end_generator), prefix + "generator RNG"
        assert (ca.start_boss_pool_state, ca.end_boss_pool_state) == (ra.start_boss, ra.end_boss), prefix + "BossPool RNG"
        assert (ca.used_bits_before, ca.used_bits_after) == (ra.used_before, ra.used_after), prefix + "persistent used bits"
        assert tuple((_key(k), old, new) for k, old, new in ca.room_config_mutations) == tuple((_key(k), old, new) for k, old, new in ra.weight_mutations), prefix + "RoomConfig weights"
        assert (ca.through_treasure is None) == (ra.through_treasure is None), prefix + "M5 presence"
        if ca.through_treasure is not None:
            assert _post_clean(ca.through_treasure) == _post_reference(ra.through_treasure), prefix + "M5"
        assert (ca.through_secret is None) == (ra.through_secret is None), prefix + "M6 presence"
        if ca.through_secret is not None:
            assert _m6(ca.through_secret) == _m6(ra.through_secret), prefix + "M6 deep state"
    assert clean.final_level_rng_state == reference.final_level, "final Level RNG"
    assert clean.final_generator_rng_state == reference.final_generator, "final generator RNG"
    assert clean.final_boss_pool_state == reference.final_boss, "final BossPool RNG"
    assert clean.permanent_removed_bosses == reference.removed, "permanent bosses at pre-Ultra boundary"
    assert clean.pending_boss_blacklist == reference.pending_blacklist, "uncommitted attempt boss blacklist"
    assert tuple((_key(k), value) for k, value in clean.final_room_config_weights) == tuple((_key(k), value) for k, value in reference.weights), "final RoomConfig weights"
    assert clean.final_special_room_used_bits == reference.used_bits, "final used bits"
