"""Canonical Basement I layout plus successful post-layout state handoff."""

from __future__ import annotations

from dataclasses import dataclass

from .basement1_full_pipeline import (
    EXTERNAL_VALIDATION,
    Basement1FullResult,
    generate_basement1_full,
)
from .boss_pool import BossPoolEntry, derive_pool_seeds
from .generation_state import CanonicalRunGenerationSnapshot
from .post_layout_lifecycle import (
    PostLayoutLifecycleResult,
    run_post_layout_lifecycle,
)
from .resources import RoomDefinition
from .room_config import entries_from_definitions


BASEMENT1_LIFECYCLE_STATUS = "BASEMENT1_CANONICAL_LIFECYCLE_CONFIRMED_BINARY"


@dataclass(frozen=True)
class Basement1LifecycleResult:
    completed: bool
    generation_status: str
    external_validation: str
    layout: Basement1FullResult
    post_layout: PostLayoutLifecycleResult
    next_run_state: CanonicalRunGenerationSnapshot


def generate_basement1_lifecycle(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Basement1LifecycleResult:
    layout = generate_basement1_full(
        start_seed,
        difficulty,
        boss_entries=boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        max_attempts=max_attempts,
    )
    if not layout.completed:
        raise RuntimeError("Basement I layout did not complete within max_attempts")
    entries = (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(basement_definitions, stage=1)
        + entries_from_definitions(blue_womb_definitions, stage=13)
    )
    tail = run_post_layout_lifecycle(
        level_rng_state=layout.final_level_rng_state,
        entries=entries,
        room_config_weights=layout.final_room_config_weights,
        special_room_used_bits=layout.final_special_room_used_bits,
    )
    pool_states = list(derive_pool_seeds(start_seed))
    pool_states[1] = layout.final_boss_pool_state
    next_state = CanonicalRunGenerationSnapshot(
        game_start_seed=start_seed,
        completed_level_stage=1,
        next_level_stage=2,
        boss_pool_rng_states=tuple(pool_states),
        permanent_removed_bosses=layout.permanent_removed_bosses,
        room_config_weights=tail.final_room_config_weights,
        special_room_used_bits=tail.final_special_room_used_bits,
        last_floor_level_rng_state=tail.final_level_rng_state,
        lifecycle="basement1-success-tail-complete",
    )
    return Basement1LifecycleResult(
        True,
        BASEMENT1_LIFECYCLE_STATUS,
        EXTERNAL_VALIDATION,
        layout,
        tail,
        next_state,
    )
