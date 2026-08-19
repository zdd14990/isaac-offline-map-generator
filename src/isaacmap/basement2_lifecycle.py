"""Canonical Basement-II accepted layout plus successful lifecycle handoff."""

from __future__ import annotations

from dataclasses import dataclass

from .basement2_full_pipeline import Basement2FullResult, generate_basement2_full
from .boss_pool import BossPoolEntry
from .generation_state import CanonicalRunGenerationSnapshot
from .post_layout_lifecycle import PostLayoutLifecycleResult, run_post_layout_lifecycle
from .resources import RoomDefinition
from .room_config import entries_from_definitions


BASEMENT2_LIFECYCLE_STATUS = "BASEMENT2_CANONICAL_LIFECYCLE_CONFIRMED_BINARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"


@dataclass(frozen=True)
class Basement2LifecycleResult:
    completed: bool
    generation_status: str
    external_validation: str
    layout: Basement2FullResult
    post_layout: PostLayoutLifecycleResult
    next_run_state: CanonicalRunGenerationSnapshot


def generate_basement2_lifecycle(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Basement2LifecycleResult:
    layout = generate_basement2_full(
        start_seed,
        difficulty,
        boss_entries=boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        blue_womb_definitions=blue_womb_definitions,
        max_attempts=max_attempts,
    )
    if not layout.completed:
        raise RuntimeError("Basement II layout did not complete within max_attempts")
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
        level_stage=2,
        stage_type=0,
        room_config_stage=1,
    )
    pool_states = list(layout.replayed_basement1.next_run_state.boss_pool_rng_states)
    pool_states[1] = layout.final_boss_pool_state
    next_state = CanonicalRunGenerationSnapshot(
        game_start_seed=start_seed,
        completed_level_stage=2,
        next_level_stage=3,
        boss_pool_rng_states=tuple(pool_states),
        permanent_removed_bosses=layout.permanent_removed_bosses,
        room_config_weights=tail.final_room_config_weights,
        special_room_used_bits=tail.final_special_room_used_bits,
        last_floor_level_rng_state=tail.final_level_rng_state,
        lifecycle="basement2-success-tail-complete",
    )
    return Basement2LifecycleResult(
        True,
        BASEMENT2_LIFECYCLE_STATUS,
        EXTERNAL_VALIDATION,
        layout,
        tail,
        next_state,
    )
