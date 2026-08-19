"""Canonical Dross (2+) accepted layout plus successful lifecycle handoff."""

from __future__ import annotations

from dataclasses import dataclass

from .boss_pool import DROSS_POOL_INDEX, BossPoolEntry, derive_pool_seeds
from .dross_full_pipeline import Basement1FullResult, generate_dross_full
from .generation_state import CanonicalRunGenerationSnapshot
from .post_layout_lifecycle import PostLayoutLifecycleResult, run_post_layout_lifecycle
from .resources import RoomDefinition
from .room_config import entries_from_definitions


DROSS_LIFECYCLE_STATUS = "DROSS_CANONICAL_LIFECYCLE_PARTIAL_BINARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"


@dataclass(frozen=True)
class DrossLifecycleResult:
    completed: bool
    generation_status: str
    external_validation: str
    layout: Basement1FullResult
    post_layout: PostLayoutLifecycleResult
    next_run_state: CanonicalRunGenerationSnapshot


def generate_dross_lifecycle(
    start_seed: int,
    difficulty: str,
    *,
    dross_boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    dross_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> DrossLifecycleResult:
    layout = generate_dross_full(
        start_seed,
        difficulty,
        dross_boss_entries=dross_boss_entries,
        special_definitions=special_definitions,
        dross_definitions=dross_definitions,
        max_attempts=max_attempts,
    )
    if not layout.completed:
        raise RuntimeError("Dross layout did not complete within max_attempts")

    entries = (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(blue_womb_definitions, stage=13)
    )
    tail = run_post_layout_lifecycle(
        level_rng_state=layout.final_level_rng_state,
        entries=entries,
        room_config_weights=layout.final_room_config_weights,
        special_room_used_bits=layout.final_special_room_used_bits,
        level_stage=2,
        stage_type=5,
        room_config_stage=28,
    )

    pool_states = list(derive_pool_seeds(layout.start_seed))
    pool_states[DROSS_POOL_INDEX] = layout.final_boss_pool_state
    next_state = CanonicalRunGenerationSnapshot(
        game_start_seed=layout.start_seed,
        completed_level_stage=2,
        next_level_stage=3,
        boss_pool_rng_states=tuple(pool_states),
        permanent_removed_bosses=layout.permanent_removed_bosses,
        room_config_weights=tail.final_room_config_weights,
        special_room_used_bits=tail.final_special_room_used_bits,
        last_floor_level_rng_state=tail.final_level_rng_state,
        lifecycle="dross-success-tail-complete",
    )
    return DrossLifecycleResult(
        True,
        DROSS_LIFECYCLE_STATUS,
        EXTERNAL_VALIDATION,
        layout,
        tail,
        next_state,
    )
