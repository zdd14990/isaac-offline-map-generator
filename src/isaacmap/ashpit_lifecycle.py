"""Canonical Ashpit (4+) accepted layout plus successful lifecycle handoff."""

from __future__ import annotations

from dataclasses import dataclass

from .boss_pool import ASHPIT_POOL_INDEX, BossPoolEntry, derive_pool_seeds
from .ashpit_full_pipeline import Basement1FullResult, generate_ashpit_full
from .generation_state import CanonicalRunGenerationSnapshot
from .post_layout_lifecycle import PostLayoutLifecycleResult, run_post_layout_lifecycle
from .resources import RoomDefinition
from .room_config import entries_from_definitions


ASHPIT_LIFECYCLE_STATUS = "ASHPIT_CANONICAL_LIFECYCLE_PARTIAL_BINARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"


@dataclass(frozen=True)
class AshpitLifecycleResult:
    completed: bool
    generation_status: str
    external_validation: str
    layout: Basement1FullResult
    post_layout: PostLayoutLifecycleResult
    next_run_state: CanonicalRunGenerationSnapshot


def generate_ashpit_lifecycle(
    start_seed: int,
    difficulty: str,
    *,
    ashpit_boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    ashpit_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> AshpitLifecycleResult:
    layout = generate_ashpit_full(
        start_seed,
        difficulty,
        ashpit_boss_entries=ashpit_boss_entries,
        special_definitions=special_definitions,
        ashpit_definitions=ashpit_definitions,
        max_attempts=max_attempts,
    )
    if not layout.completed:
        raise RuntimeError("Ashpit layout did not complete within max_attempts")

    entries = (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(blue_womb_definitions, stage=13)
    )
    tail = run_post_layout_lifecycle(
        level_rng_state=layout.final_level_rng_state,
        entries=entries,
        room_config_weights=layout.final_room_config_weights,
        special_room_used_bits=layout.final_special_room_used_bits,
        level_stage=4,
        stage_type=5,
        room_config_stage=30,
    )

    pool_states = list(derive_pool_seeds(layout.start_seed))
    pool_states[ASHPIT_POOL_INDEX] = layout.final_boss_pool_state
    next_state = CanonicalRunGenerationSnapshot(
        game_start_seed=layout.start_seed,
        completed_level_stage=4,
        next_level_stage=5,
        boss_pool_rng_states=tuple(pool_states),
        permanent_removed_bosses=layout.permanent_removed_bosses,
        room_config_weights=tail.final_room_config_weights,
        special_room_used_bits=tail.final_special_room_used_bits,
        last_floor_level_rng_state=tail.final_level_rng_state,
        lifecycle="ashpit-success-tail-complete",
    )
    return AshpitLifecycleResult(
        True,
        ASHPIT_LIFECYCLE_STATUS,
        EXTERNAL_VALIDATION,
        layout,
        tail,
        next_state,
    )
