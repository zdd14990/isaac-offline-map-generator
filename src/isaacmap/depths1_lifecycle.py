"""Canonical Depths-I accepted layout plus successful lifecycle handoff.

The Stage-5 post-layout tail reuses the shared ``place_post_topology_rooms``
tail (RVA ``0x0033D1D6..0x0033D94B``).  Stage 5 (room-config stage 7) skips
the ``-9`` (room-config-stage 13) and ``-10`` (stage-type 4/5 plus level-stage
7/8) branches, so the tail is identical to earlier floors.
"""

from __future__ import annotations

from dataclasses import dataclass

from .boss_pool import DEPTHS_POOL_INDEX, BossPoolEntry
from .caves2_lifecycle import Caves2LifecycleResult
from .depths1_full_pipeline import Depths1FullResult, generate_depths1_full
from .generation_state import CanonicalRunGenerationSnapshot
from .post_layout_lifecycle import PostLayoutLifecycleResult, run_post_layout_lifecycle
from .resources import RoomDefinition
from .room_config import entries_from_definitions


DEPTHS1_LIFECYCLE_STATUS = "DEPTHS1_CANONICAL_LIFECYCLE_CONFIRMED_BINARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"


@dataclass(frozen=True)
class Depths1LifecycleResult:
    completed: bool
    generation_status: str
    external_validation: str
    layout: Depths1FullResult
    post_layout: PostLayoutLifecycleResult
    next_run_state: CanonicalRunGenerationSnapshot


def generate_depths1_lifecycle(
    caves2_result: Caves2LifecycleResult,
    *,
    depths_boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    caves_definitions: tuple[RoomDefinition, ...],
    depths_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Depths1LifecycleResult:
    layout = generate_depths1_full(
        caves2_result.layout,
        caves2_result.next_run_state,
        depths_boss_entries=depths_boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        caves_definitions=caves_definitions,
        depths_definitions=depths_definitions,
        blue_womb_definitions=blue_womb_definitions,
        max_attempts=max_attempts,
    )
    if not layout.completed:
        raise RuntimeError("Depths I layout did not complete within max_attempts")

    entries = (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(depths_definitions, stage=7)
        + entries_from_definitions(blue_womb_definitions, stage=13)
    )
    tail = run_post_layout_lifecycle(
        level_rng_state=layout.final_level_rng_state,
        entries=entries,
        room_config_weights=layout.final_room_config_weights,
        special_room_used_bits=layout.final_special_room_used_bits,
        level_stage=5,
        stage_type=0,
        room_config_stage=7,
    )

    pool_states = list(caves2_result.next_run_state.boss_pool_rng_states)
    pool_states[DEPTHS_POOL_INDEX] = layout.final_boss_pool_state
    next_state = CanonicalRunGenerationSnapshot(
        game_start_seed=layout.start_seed,
        completed_level_stage=5,
        next_level_stage=6,
        boss_pool_rng_states=tuple(pool_states),
        permanent_removed_bosses=layout.permanent_removed_bosses,
        room_config_weights=tail.final_room_config_weights,
        special_room_used_bits=tail.final_special_room_used_bits,
        last_floor_level_rng_state=tail.final_level_rng_state,
        lifecycle="depths1-success-tail-complete",
    )
    return Depths1LifecycleResult(
        True,
        DEPTHS1_LIFECYCLE_STATUS,
        EXTERNAL_VALIDATION,
        layout,
        tail,
        next_state,
    )
