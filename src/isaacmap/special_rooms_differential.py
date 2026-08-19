"""Differential comparison for the recovered Boss -> RoomType 8 slice."""

from __future__ import annotations

from .boss_pool import BossPoolEntry
from .boss_pool_reference import BossPoolEntryReference
from .resources import RoomDefinition
from .special_rooms import (
    room_configs_from_definitions,
    run_boss_then_type8,
)
from .special_rooms_reference import (
    configs_from_room_definitions_reference,
    run_boss_then_type8_reference,
)


def _room_key(room: object) -> tuple[object, ...]:
    return (
        int(room.generation_index), int(room.column), int(room.line), int(room.shape),
        int(room.doors), tuple(sorted(room.neighbors)), int(room.room_type),
        int(room.variant), int(room.subtype), int(room.distance_from_start),
    )


def compare_boss_then_type8(
    topology_clean: object,
    topology_reference: object,
    *,
    game_start_seed: int,
    level_rng_state: int,
    boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    collectible_589_owned: bool = False,
) -> None:
    clean = run_boss_then_type8(
        topology_clean,
        game_start_seed=game_start_seed,
        level_rng_state=level_rng_state,
        boss_entries=boss_entries,
        special_configs=room_configs_from_definitions(special_definitions),
        collectible_589_owned=collectible_589_owned,
    )
    reference = run_boss_then_type8_reference(
        topology_reference,
        game_start_seed=game_start_seed,
        level_rng_state=level_rng_state,
        boss_entries=tuple(
            BossPoolEntryReference(
                entry.boss_id, entry.weight, entry.initial_weight,
                entry.achievement, entry.alternate_boss_id,
            )
            for entry in boss_entries
        ),
        special_configs=configs_from_room_definitions_reference(special_definitions),
        collectible_589_owned=collectible_589_owned,
    )
    clean_key = (
        clean.completed, clean.abort_operation,
        clean.boss.boss_id, clean.boss_room, clean.type8_rooms,
        tuple(_room_key(room) for room in clean.rooms),
        clean.room_map, clean.dead_ends, clean.final_level_rng_state,
        clean.config_weights,
        tuple((draw.pre_state, draw.post_state, draw.shift_index, draw.binary_rva)
              for draw in clean.rng_trace),
        tuple((event.operation, event.candidate_order, event.tested_room,
               event.accepted, event.dead_ends_after)
              for event in clean.candidate_trace),
    )
    reference_key = (
        reference.completed, reference.abort_operation,
        reference.boss.boss_id, reference.boss_room, reference.type8_rooms,
        tuple(_room_key(room) for room in reference.rooms),
        reference.room_map, reference.dead_ends, reference.final_level_rng_state,
        reference.room_config_weights,
        tuple((draw.pre_state, draw.post_state, draw.shift_index, draw.binary_rva)
              for draw in reference.rng_ledger),
        tuple((event.operation, event.candidate_order, event.tested_room,
               event.accepted, event.dead_ends_after)
              for event in reference.candidate_events),
    )
    if clean_key != reference_key:
        raise AssertionError(
            "Boss/RoomType8 differential mismatch for start seed "
            f"0x{game_start_seed:08X}: clean={clean_key!r}, reference={reference_key!r}"
        )
