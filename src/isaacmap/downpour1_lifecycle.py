"""Canonical Downpour-I accepted layout plus successful lifecycle handoff.

The Stage-1 ALT post-layout tail reuses the shared ``place_post_topology_rooms``
tail (RVA ``0x0033D1D6..0x0033D94B``): 28 persistent Level RNG draws (the
``-9``/``-10`` branches are skipped for stage_type 4/5 at level 1..6).
"""

from __future__ import annotations
from .boss_pool import DOWNPOUR_POOL_INDEX, BossPoolEntry, derive_pool_seeds
from dataclasses import dataclass

from .boss_pool import DOWNPOUR_POOL_INDEX, BossPoolEntry
from .downpour1_full_pipeline import Basement1FullResult, generate_downpour1_full
from .generation_state import CanonicalRunGenerationSnapshot
from .post_layout_lifecycle import PostLayoutLifecycleResult, run_post_layout_lifecycle
from .resources import RoomDefinition
from .room_config import entries_from_definitions


DOWNPOUR1_LIFECYCLE_STATUS = "DOWNPOUR1_CANONICAL_LIFECYCLE_PARTIAL_BINARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"


@dataclass(frozen=True)
class Downpour1LifecycleResult:
    completed: bool
    generation_status: str
    external_validation: str
    layout: Basement1FullResult
    post_layout: PostLayoutLifecycleResult
    next_run_state: CanonicalRunGenerationSnapshot


def generate_downpour1_lifecycle(
    start_seed: int,
    difficulty: str,
    *,
    downpour_boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    downpour_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Downpour1LifecycleResult:
    layout = generate_downpour1_full(
        start_seed,
        difficulty,
        downpour_boss_entries=downpour_boss_entries,
        special_definitions=special_definitions,
        downpour_definitions=downpour_definitions,
        max_attempts=max_attempts,
    )
    if not layout.completed:
        raise RuntimeError("Downpour I layout did not complete within max_attempts")
    entries = (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(blue_womb_definitions, stage=13)
    )
    tail = run_post_layout_lifecycle(
        level_rng_state=layout.final_level_rng_state,
        entries=entries,
        room_config_weights=layout.final_room_config_weights,
        special_room_used_bits=layout.final_special_room_used_bits,
        level_stage=1,
        stage_type=4,
        room_config_stage=27,
    )
    pool_states = list(derive_pool_seeds(layout.start_seed))
    pool_states[DOWNPOUR_POOL_INDEX] = layout.final_boss_pool_state

    next_state = CanonicalRunGenerationSnapshot(
        game_start_seed=layout.start_seed,
        completed_level_stage=1,
        next_level_stage=2,
        boss_pool_rng_states=tuple(pool_states),
        permanent_removed_bosses=layout.permanent_removed_bosses,
        room_config_weights=tail.final_room_config_weights,
        special_room_used_bits=tail.final_special_room_used_bits,
        last_floor_level_rng_state=tail.final_level_rng_state,
        lifecycle="downpour1-success-tail-complete",
    )
    return Downpour1LifecycleResult(
        True,
        DOWNPOUR1_LIFECYCLE_STATUS,
        EXTERNAL_VALIDATION,
        layout,
        tail,
        next_state,
    )
