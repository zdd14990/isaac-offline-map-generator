"""Canonical Basement-II composition through the Treasure boundary.

This is an internal research boundary, not a complete supported floor.  It
replays the confirmed Basement-I lifecycle, restores persistent generation
state, resets only the current stage-1 RoomConfig pool, and composes the
existing topology/post-topology leaves through Treasure.
"""

from __future__ import annotations

from dataclasses import dataclass

from .basement1_lifecycle import Basement1LifecycleResult, generate_basement1_lifecycle
from .basement1_pipeline import (
    GenerationAttemptResult,
    _topology_snapshot,
    run_post_topology_through_treasure,
)
from .boss_pool import BossPoolEntry, BossPoolRuntimeState
from .floor_init import derive_basement2_topology_inputs
from .generation_state import (
    CanonicalBasement2Profile,
    FloorGenerationState,
    RunGenerationState,
)
from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config import RoomConfigKey, RoomConfigMutableState, entries_from_definitions
from .special_rooms import GeneratedRoom
from .topology import LevelGeneratorResearch, LevelGeneratorRoom
from .topology_geometry import RoomShape


BASEMENT2_TREASURE_STATUS = "BASEMENT2_THROUGH_TREASURE_RESEARCH_BOUNDARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"
LEVEL_SHIFT_INDEX = 35


@dataclass(frozen=True)
class Basement2ThroughTreasureResult:
    completed: bool
    generation_status: str
    external_validation: str
    start_seed: int
    difficulty: str
    stage_seed: int
    replayed_basement1: Basement1LifecycleResult
    entry_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    attempts: tuple[GenerationAttemptResult, ...]
    final_level_rng_state: int
    final_generator_rng_state: int
    final_boss_pool_state: int
    permanent_removed_bosses: tuple[int, ...]
    pending_boss_blacklist: tuple[int, ...]
    final_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    final_special_room_used_bits: tuple[int, ...]
    rooms: tuple[GeneratedRoom, ...]


def generate_basement2_through_treasure(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Basement2ThroughTreasureResult:
    replay = generate_basement1_lifecycle(
        start_seed,
        difficulty,
        boss_entries=boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        blue_womb_definitions=blue_womb_definitions,
        max_attempts=max_attempts,
    )
    snapshot = replay.next_run_state
    if (
        snapshot.game_start_seed != start_seed
        or snapshot.completed_level_stage != 1
        or snapshot.next_level_stage != 2
    ):
        raise ValueError("Basement-II entry requires a successful Basement-I snapshot")

    inputs = derive_basement2_topology_inputs(start_seed, difficulty)
    profile = CanonicalBasement2Profile(
        difficulty,
        effective_curse_mask=inputs.effective_curse_mask,
        special_room_used_bits=frozenset(snapshot.special_room_used_bits),
    )
    profile.validate()
    special_entries = entries_from_definitions(special_definitions, stage=0)
    basement_entries = entries_from_definitions(basement_definitions, stage=1)
    entries = special_entries + basement_entries
    room_config = RoomConfigMutableState(dict(snapshot.room_config_weights))
    # Level::Init resets the current RoomConfig stage, not the inherited
    # special-stage weights or unrelated stage-13 fixed-descriptor pool.
    room_config.reset(basement_entries)
    entry_weights = tuple(sorted(room_config.weights.items()))
    bosses = BossPoolRuntimeState.resume_canonical_basement(
        start_seed,
        boss_entries,
        pool_state=snapshot.boss_pool_rng_states[1],
        removed=snapshot.permanent_removed_bosses,
    )
    run_state = RunGenerationState(
        start_seed,
        bosses,
        room_config,
        "basement1-success-tail-complete/basement2-entered",
        set(snapshot.special_room_used_bits),
    )
    generator = LevelGeneratorResearch(inputs.generator_seed)
    level_rng = IsaacRNG.game_constructor(inputs.generator_seed, LEVEL_SHIFT_INDEX)
    generator._m6_level_rng = level_rng
    floor_state = FloorGenerationState(
        inputs.stage_seed,
        target_room_count=inputs.target_room_count,
        level_rng=level_rng,
        level_generator=generator,
    )
    attempts: list[GenerationAttemptResult] = []
    final_rooms: tuple[GeneratedRoom, ...] = ()

    for attempt_number in range(1, max_attempts + 1):
        floor_state.retry_count = attempt_number - 1
        run_state.boss_pools.begin_attempt()
        start_level = level_rng.seed
        start_generator = generator.rng.seed
        start_boss = run_state.boss_pools.pool_rngs[1].seed
        weights_before = dict(run_state.room_config.weights)
        generator.blocked_positions[:] = [False] * len(generator.blocked_positions)
        generator.generate_once(
            floor_state.target_room_count,
            inputs.required_dead_ends,
            inputs.allowed_shapes_mask,
            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        topology = _topology_snapshot(generator, floor_state.target_room_count)
        usable = len(generator.dead_ends) >= inputs.required_dead_ends
        post = None
        if usable:
            post = run_post_topology_through_treasure(
                generator,
                run_state=run_state,
                floor_state=floor_state,
                entries=entries,
                profile=profile,
            )
        elif (
            attempt_number >= 10
            and attempt_number % 5 == 0
            and floor_state.target_room_count < 64
        ):
            floor_state.target_room_count += 1
        mutations = tuple(
            (key, weights_before.get(key, value), value)
            for key, value in sorted(run_state.room_config.weights.items())
            if weights_before.get(key, value) != value
        )
        attempts.append(
            GenerationAttemptResult(
                attempt_number,
                topology.target_room_count,
                usable,
                topology,
                start_level,
                level_rng.seed,
                start_generator,
                generator.rng.seed,
                start_boss,
                run_state.boss_pools.pool_rngs[1].seed,
                tuple(sorted(run_state.boss_pools.level_blacklist)),
                tuple(sorted(run_state.boss_pools.removed)),
                mutations,
                post,
            )
        )
        if post is not None and post.completed:
            final_rooms = post.rooms
            # This boundary deliberately does not commit the current boss: a
            # later Stage-2 placement failure must still reject this attempt.
            return Basement2ThroughTreasureResult(
                True,
                BASEMENT2_TREASURE_STATUS,
                EXTERNAL_VALIDATION,
                start_seed,
                difficulty,
                inputs.stage_seed,
                replay,
                entry_weights,
                tuple(attempts),
                level_rng.seed,
                generator.rng.seed,
                run_state.boss_pools.pool_rngs[1].seed,
                tuple(sorted(run_state.boss_pools.removed)),
                tuple(sorted(run_state.boss_pools.level_blacklist)),
                tuple(sorted(run_state.room_config.weights.items())),
                tuple(sorted(run_state.special_room_used_bits)),
                final_rooms,
            )

    return Basement2ThroughTreasureResult(
        False,
        BASEMENT2_TREASURE_STATUS,
        EXTERNAL_VALIDATION,
        start_seed,
        difficulty,
        inputs.stage_seed,
        replay,
        entry_weights,
        tuple(attempts),
        level_rng.seed,
        generator.rng.seed,
        run_state.boss_pools.pool_rngs[1].seed,
        tuple(sorted(run_state.boss_pools.removed)),
        tuple(sorted(run_state.boss_pools.level_blacklist)),
        tuple(sorted(run_state.room_config.weights.items())),
        tuple(sorted(run_state.special_room_used_bits)),
        final_rooms,
    )
