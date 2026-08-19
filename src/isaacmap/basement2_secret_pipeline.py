"""Canonical Basement-II composition through the Secret-room boundary.

This module only composes already recovered clean leaves.  It replays the
successful Basement-I lifecycle, restores its persistent generation state,
and exposes the accepted Stage-2 attempt after Secret placement.  Ultra
Secret and the late default-room pass remain outside this boundary.
"""

from __future__ import annotations

from dataclasses import dataclass

from .basement1_lifecycle import Basement1LifecycleResult, generate_basement1_lifecycle
from .basement1_pipeline import _topology_snapshot, run_post_topology_through_treasure
from .basement1_secret_pipeline import (
    SecretGenerationAttemptResult,
    run_treasure_to_secret,
)
from .boss_pool import BossPoolEntry, BossPoolRuntimeState
from .floor_init import derive_basement2_topology_inputs
from .generation_state import CanonicalBasement2Profile, FloorGenerationState, RunGenerationState
from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config import RoomConfigKey, RoomConfigMutableState, entries_from_definitions
from .special_rooms import GeneratedRoom
from .topology import LevelGeneratorResearch, LevelGeneratorRoom
from .topology_geometry import RoomShape


BASEMENT2_SECRET_STATUS = "BASEMENT2_THROUGH_SECRET_RESEARCH_BOUNDARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"
LEVEL_SHIFT_INDEX = 35


@dataclass(frozen=True)
class Basement2ThroughSecretResult:
    boundary_completed: bool
    generation_status: str
    external_validation: str
    start_seed: int
    difficulty: str
    stage_seed: int
    replayed_basement1: Basement1LifecycleResult
    entry_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    attempts: tuple[SecretGenerationAttemptResult, ...]
    final_level_rng_state: int
    final_generator_rng_state: int
    final_boss_pool_state: int
    permanent_removed_bosses: tuple[int, ...]
    pending_boss_blacklist: tuple[int, ...]
    final_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    final_special_room_used_bits: tuple[int, ...]
    rooms: tuple[GeneratedRoom, ...]


def generate_basement2_through_secret(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Basement2ThroughSecretResult:
    """Replay to the accepted Stage-2 pre-Ultra boundary.

    The current Stage-2 boss remains in the attempt-local blacklist because a
    later Ultra/default-room failure could still reject this same attempt.
    """

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
    attempts: list[SecretGenerationAttemptResult] = []

    for attempt_number in range(1, max_attempts + 1):
        floor_state.retry_count = attempt_number - 1
        run_state.boss_pools.begin_attempt()
        start_level = level_rng.seed
        start_generator = generator.rng.seed
        start_boss = run_state.boss_pools.pool_rngs[1].seed
        used_before = tuple(sorted(run_state.special_room_used_bits))
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
        through_treasure = None
        through_secret = None
        if usable:
            through_treasure = run_post_topology_through_treasure(
                generator,
                run_state=run_state,
                floor_state=floor_state,
                entries=entries,
                profile=profile,
            )
            if through_treasure.completed:
                through_secret = run_treasure_to_secret(
                    through_treasure,
                    generator=generator,
                    run_state=run_state,
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
            SecretGenerationAttemptResult(
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
                used_before,
                tuple(sorted(run_state.special_room_used_bits)),
                mutations,
                through_treasure,
                through_secret,
            )
        )
        if through_secret is not None and through_secret.completed:
            return Basement2ThroughSecretResult(
                True,
                BASEMENT2_SECRET_STATUS,
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
                through_secret.rooms,
            )

    return Basement2ThroughSecretResult(
        False,
        BASEMENT2_SECRET_STATUS,
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
        (),
    )
