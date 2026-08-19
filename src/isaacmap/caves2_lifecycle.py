"""Canonical Caves-II accepted layout plus successful lifecycle handoff.

The Stage-4 post-layout tail reuses the shared ``place_post_topology_rooms``
tail (RVA ``0x0033D1D6..0x0033D94B``).  Even Stage 4 never takes the ``-9``
(room-config-stage 13) or ``-10`` (stage-type 4/5 plus level-stage 7/8)
branches, so the tail is identical to Basement I/II and Caves I.
"""

from __future__ import annotations

from dataclasses import dataclass

from .boss_pool import CAVES_POOL_INDEX, BossPoolEntry
from .caves1_lifecycle import Caves1LifecycleResult
from .caves2_full_pipeline import Caves2FullResult, generate_caves2_full
from .generation_state import CanonicalRunGenerationSnapshot
from .post_layout_lifecycle import PostLayoutLifecycleResult, run_post_layout_lifecycle
from .resources import RoomDefinition
from .room_config import entries_from_definitions


CAVES2_LIFECYCLE_STATUS = "CAVES2_CANONICAL_LIFECYCLE_CONFIRMED_BINARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"


@dataclass(frozen=True)
class Caves2LifecycleResult:
    completed: bool
    generation_status: str
    external_validation: str
    layout: Caves2FullResult
    post_layout: PostLayoutLifecycleResult
    next_run_state: CanonicalRunGenerationSnapshot


def generate_caves2_lifecycle(
    caves1_result: Caves1LifecycleResult,
    *,
    basement_boss_entries: tuple[BossPoolEntry, ...],
    caves_boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    caves_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Caves2LifecycleResult:
    layout = generate_caves2_full(
        caves1_result.layout,
        caves1_result.next_run_state,
        basement_boss_entries=basement_boss_entries,
        caves_boss_entries=caves_boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        caves_definitions=caves_definitions,
        blue_womb_definitions=blue_womb_definitions,
        max_attempts=max_attempts,
    )
    if not layout.completed:
        raise RuntimeError("Caves II layout did not complete within max_attempts")

    entries = (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(caves_definitions, stage=4)
        + entries_from_definitions(blue_womb_definitions, stage=13)
    )
    tail = run_post_layout_lifecycle(
        level_rng_state=layout.final_level_rng_state,
        entries=entries,
        room_config_weights=layout.final_room_config_weights,
        special_room_used_bits=layout.final_special_room_used_bits,
        level_stage=4,
        stage_type=0,
        room_config_stage=4,
    )

    pool_states = list(caves1_result.next_run_state.boss_pool_rng_states)
    pool_states[CAVES_POOL_INDEX] = layout.final_boss_pool_state
    next_state = CanonicalRunGenerationSnapshot(
        game_start_seed=layout.start_seed,
        completed_level_stage=4,
        next_level_stage=5,
        boss_pool_rng_states=tuple(pool_states),
        permanent_removed_bosses=layout.permanent_removed_bosses,
        room_config_weights=tail.final_room_config_weights,
        special_room_used_bits=tail.final_special_room_used_bits,
        last_floor_level_rng_state=tail.final_level_rng_state,
        lifecycle="caves2-success-tail-complete",
    )
    return Caves2LifecycleResult(
        True,
        CAVES2_LIFECYCLE_STATUS,
        EXTERNAL_VALIDATION,
        layout,
        tail,
        next_state,
    )
