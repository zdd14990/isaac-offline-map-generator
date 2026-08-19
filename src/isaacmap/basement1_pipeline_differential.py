"""Deep clean/reference comparator for retry + Boss/Type8/Shop/Treasure."""

from __future__ import annotations

from .basement1_pipeline import Basement1ThroughTreasureResult
from .basement1_pipeline_reference import ReferenceBasement1Result


def _key(key) -> tuple[int, int, int]:
    return key.stage, key.mode, key.resource_index


def _room(room) -> tuple[object, ...]:
    return (
        room.generation_index, room.column, room.line, int(room.shape),
        room.origin_direction, room.link_column, room.link_line,
        room.distance_from_start, room.doors, tuple(sorted(room.neighbors)),
        room.room_type, room.variant, room.subtype,
    )


def _topology_clean(attempt) -> tuple[object, ...]:
    topology=attempt.topology
    return (
        tuple((r.generation_index,r.column,r.line,int(r.shape),tuple(sorted(r.neighbors)),r.doors,r.distance_from_start) for r in topology.rooms),
        topology.room_map,topology.dead_ends,topology.non_dead_ends,topology.expansion_order,
    )


def _selection(selection) -> tuple[object, ...]:
    entry=getattr(selection,"entry",getattr(selection,"selected",None))
    candidates=getattr(selection,"candidate_keys",getattr(selection,"all_candidates",()))
    exact=getattr(selection,"exact_door_keys",getattr(selection,"exact_door_candidates",()))
    used=getattr(selection,"used_exact_doors",getattr(selection,"selected_from_exact_doors",False))
    old=getattr(selection,"old_weight",getattr(selection,"selected_old_weight",None))
    new=getattr(selection,"new_weight",getattr(selection,"selected_new_weight",None))
    return (
        tuple(_key(k) for k in candidates),tuple(_key(k) for k in exact),used,
        None if entry is None else (_key(entry.key),entry.room_type,entry.variant,entry.subtype,entry.difficulty,entry.shape,entry.initial_weight,entry.door_mask),
        old,new,tuple((d.binary_rva,d.pre_state,d.post_state,d.reason,d.result_float) for d in selection.draws),
    )


def _boss_selection(selection) -> tuple[object, ...]:
    return (
        selection.boss_id,
        selection.selected_entry_id,
        selection.persistent_pre_state,
        selection.persistent_post_state,
        selection.local_selector_final_state,
        selection.repick_count,
        selection.fallback_used,
        selection.pool_reset_count,
    )


def _post_clean(post) -> tuple[object, ...]:
    return (
        post.completed,post.abort_operation,post.boss_selection.boss_id,
        post.boss_selection.selected_entry_id,post.boss_selection.persistent_pre_state,
        post.boss_selection.persistent_post_state,post.boss_selection.local_selector_final_state,
        post.boss_selection.repick_count,post.boss_selection.fallback_used,
        post.boss_selection.pool_reset_count,
        post.boss_room,None if post.boss_config is None else _key(post.boss_config),
        post.type8_rooms,post.shop_room,None if post.shop_config is None else _key(post.shop_config),
        post.treasure_room,None if post.treasure_config is None else _key(post.treasure_config),
        post.post_type8_seed_snapshot,tuple(_room(r) for r in post.rooms),post.room_map,post.dead_ends,
        tuple((d.binary_rva,d.shift_index,d.pre_state,d.post_state) for d in post.rng_draws),
        tuple((t.operation,tuple(_selection(s) for s in t.selections)) for t in post.config_traces),
        tuple((t.operation,t.candidate_order,t.tested_room,t.accepted,t.dead_ends_after) for t in post.candidate_traces),
        tuple((g.room_id,g.candidate.candidate_index,g.candidate.anchor,g.candidate.shape,g.candidate.connection_slot,g.accepted,g.reason,g.external_neighbor_count) for g in post.geometry_traces),
        tuple((c.binary_range,c.condition,c.value,c.consequence) for c in post.conditions),
        tuple(_boss_selection(value) for value in post.additional_boss_selections),
        post.additional_boss_rooms,
        tuple(_key(key) for key in post.additional_boss_configs),
        post.treasure_rooms,
        tuple(_key(key) for key in post.treasure_configs),
    )


def _post_reference(post) -> tuple[object, ...]:
    return (
        post.completed,post.abort,post.boss.boss_id,post.boss.selected_entry_id,
        post.boss.persistent_pre_state,post.boss.persistent_post_state,
        post.boss.local_selector_final_state,post.boss.repick_count,
        post.boss.fallback_used,post.boss.pool_reset_count,post.boss_room,
        None if post.boss_config is None else _key(post.boss_config),post.type8_rooms,
        post.shop_room,None if post.shop_config is None else _key(post.shop_config),
        post.treasure_room,None if post.treasure_config is None else _key(post.treasure_config),
        post.snapshot,tuple(_room(r) for r in post.rooms),post.room_map,post.dead_ends,
        tuple((d.rva,d.shift_index,d.pre,d.post) for d in post.draws),
        tuple((t.operation,tuple(_selection(s) for s in t.selections)) for t in post.configs),
        tuple((t.operation,t.candidate_order,t.tested_room,t.accepted,t.dead_ends_after) for t in post.candidates),
        tuple((g.room_id,g.candidate.candidate_index,g.candidate.anchor,g.candidate.shape,g.candidate.connection_slot,g.accepted,g.reason,g.external_neighbor_count) for g in post.geometry),
        tuple((c.binary_range,c.condition,c.value,c.consequence) for c in post.conditions),
        tuple(_boss_selection(value) for value in post.additional_bosses),
        post.additional_boss_rooms,
        tuple(_key(key) for key in post.additional_boss_configs),
        post.treasure_rooms,
        tuple(_key(key) for key in post.treasure_configs),
    )


def compare_pipeline(clean: Basement1ThroughTreasureResult, reference: ReferenceBasement1Result) -> None:
    assert clean.completed == reference.completed, "completed"
    assert len(clean.attempts) == len(reference.attempts), "attempt count"
    for ca,ra in zip(clean.attempts,reference.attempts):
        prefix=f"attempt {ca.attempt}: "
        assert ca.attempt == ra.attempt
        assert ca.target_room_count == ra.target_room_count,prefix+"target count"
        assert ca.topology_usable == ra.usable,prefix+"topology usability"
        assert _topology_clean(ca) == ra.topology_signature,prefix+"topology state"
        assert (ca.start_level_rng_state,ca.end_level_rng_state)==(ra.start_level,ra.end_level),prefix+"Level RNG"
        assert (ca.start_generator_rng_state,ca.end_generator_rng_state)==(ra.start_generator,ra.end_generator),prefix+"generator RNG"
        assert (ca.start_boss_pool_state,ca.end_boss_pool_state)==(ra.start_boss,ra.end_boss),prefix+"BossPool RNG"
        assert ca.level_blacklist_after == ra.blacklist,prefix+"level blacklist"
        assert ca.permanent_removed_after == ra.removed,prefix+"permanent removed"
        assert tuple((_key(k),a,b) for k,a,b in ca.room_config_mutations)==tuple((_key(k),a,b) for k,a,b in ra.weight_mutations),prefix+"RoomConfig mutations"
        assert (ca.post_topology is None)==(ra.post is None),prefix+"post presence"
        if ca.post_topology is not None:
            assert _post_clean(ca.post_topology)==_post_reference(ra.post),prefix+"post-topology deep state"
    assert clean.final_level_rng_state==reference.final_level,"final Level RNG"
    assert clean.final_generator_rng_state==reference.final_generator,"final generator RNG"
    assert clean.final_boss_pool_state==reference.final_boss,"final BossPool RNG"
    assert clean.permanent_removed_bosses==reference.removed,"committed bosses"
    assert tuple((_key(k),v) for k,v in clean.final_room_config_weights)==tuple((_key(k),v) for k,v in reference.weights),"final weights"
