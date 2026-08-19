"""Mechanical Caves-I lifecycle reference (layout + shared tail + snapshot)."""

from __future__ import annotations

from dataclasses import dataclass

from .basement1_full_pipeline_reference import ReferenceBasement1FullResult
from .basement2_full_pipeline_reference import generate_basement2_full_reference
from .boss_pool_reference import (
    BASEMENT_POOL_INDEX,
    CAVES_POOL_INDEX,
    BossPoolEntryReference,
    derive_pool_seeds_reference,
)
from .caves1_full_pipeline_reference import generate_caves1_full_reference
from .generation_state import CanonicalRunGenerationSnapshot
from .post_layout_lifecycle_reference import (
    ReferencePostLayoutLifecycle,
    run_post_layout_lifecycle_reference,
)
from .resources import RoomDefinition
from .room_config_reference import entries_from_definitions_reference


@dataclass(frozen=True)
class ReferenceCaves1LifecycleResult:
    completed: bool
    layout: ReferenceBasement1FullResult
    post_layout: ReferencePostLayoutLifecycle
    next_run_state: CanonicalRunGenerationSnapshot


def generate_caves1_lifecycle_reference(
    start_seed: int,
    difficulty: str,
    *,
    basement_boss_entries: tuple[BossPoolEntryReference, ...],
    caves_boss_entries: tuple[BossPoolEntryReference, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    caves_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> ReferenceCaves1LifecycleResult:
    # Basement II reference result (also produced internally by the Caves-I
    # layout reference; recomputed here for the full 37-pool snapshot).
    b2 = generate_basement2_full_reference(
        start_seed,
        difficulty,
        boss_entries=basement_boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        blue_womb_definitions=blue_womb_definitions,
        max_attempts=max_attempts,
    )

    layout = generate_caves1_full_reference(
        start_seed,
        difficulty,
        basement_boss_entries=basement_boss_entries,
        caves_boss_entries=caves_boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        caves_definitions=caves_definitions,
        blue_womb_definitions=blue_womb_definitions,
        max_attempts=max_attempts,
    )
    if not layout.completed:
        raise RuntimeError("reference Caves I layout did not complete")

    special = entries_from_definitions_reference(special_definitions, stage=0)
    caves = entries_from_definitions_reference(caves_definitions, stage=4)
    blue_womb = entries_from_definitions_reference(blue_womb_definitions, stage=13)
    tail = run_post_layout_lifecycle_reference(
        level_rng_state=layout.final_level,
        entries=special + caves + blue_womb,
        room_config_weights=layout.weights,
        special_room_used_bits=layout.used_bits,
        level_stage=3,
        room_config_stage=4,
    )

    pool_states = list(derive_pool_seeds_reference(start_seed))
    pool_states[BASEMENT_POOL_INDEX] = b2.final_boss
    pool_states[CAVES_POOL_INDEX] = layout.final_boss
    next_state = CanonicalRunGenerationSnapshot(
        game_start_seed=start_seed,
        completed_level_stage=3,
        next_level_stage=4,
        boss_pool_rng_states=tuple(pool_states),
        permanent_removed_bosses=layout.removed,
        room_config_weights=tail.weights,
        special_room_used_bits=tail.used_bits,
        last_floor_level_rng_state=tail.final_level,
        lifecycle="caves1-success-tail-complete",
    )
    return ReferenceCaves1LifecycleResult(True, layout, tail, next_state)
