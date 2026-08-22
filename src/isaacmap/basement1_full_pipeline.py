"""Complete accepted-layout pipeline for canonical frozen Basement I.

All generation leaves are imported from their existing clean modules.  This
module owns only the outer transaction: Ultra and late ordinary RoomConfig
must finish before the attempt-local BossPool blacklist is committed.
"""

from __future__ import annotations

from dataclasses import dataclass

from .basement1_pipeline import (
    PostTopologyAttemptResult,
    _topology_snapshot,
    run_post_topology_through_treasure,
)
from .basement1_secret_pipeline import (
    Basement1ThroughSecretResult,
    PostTreasureThroughSecretResult,
    SecretGenerationAttemptResult,
    run_treasure_to_secret,
)
from .basement1_ultra_pipeline import (
    PostSecretThroughUltraResult,
    run_secret_to_ultra,
)
from .boss_pool import BossPoolEntry, BossPoolRuntimeState
from .floor_init import derive_basement1_topology_inputs
from .generation_state import (
    CanonicalBasement1Profile,
    FloorGenerationState,
    RunGenerationState,
)
from .late_room_config import LateDefaultPassResult, assign_late_default_room_configs
from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config import (
    RoomConfigEntry,
    RoomConfigKey,
    RoomConfigMutableState,
    entries_from_definitions,
)
from .special_rooms import GeneratedRoom
from .topology import LevelGeneratorResearch, LevelGeneratorRoom, TopologyResearchResult
from .topology_geometry import RoomShape


FULL_LAYOUT_STATUS = "FULL_LAYOUT_PIPELINE_CONFIRMED_BINARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"
LEVEL_SHIFT_INDEX = 35


@dataclass(frozen=True)
class Basement1FullAttemptResult:
    attempt: int
    target_room_count: int
    topology_usable: bool
    topology: TopologyResearchResult
    start_level_rng_state: int
    end_level_rng_state: int
    start_generator_rng_state: int
    end_generator_rng_state: int
    start_boss_pool_state: int
    end_boss_pool_state: int
    used_bits_before: tuple[int, ...]
    used_bits_after: tuple[int, ...]
    room_config_mutations: tuple[tuple[RoomConfigKey, float, float], ...]
    through_treasure: PostTopologyAttemptResult | None
    through_secret: PostTreasureThroughSecretResult | None
    through_ultra: PostSecretThroughUltraResult | None
    late_default: LateDefaultPassResult | None
    abort_operation: str | None


@dataclass(frozen=True)
class Basement1FullResult:
    completed: bool
    generation_status: str
    external_validation: str
    start_seed: int
    difficulty: str
    stage_seed: int
    attempts: tuple[Basement1FullAttemptResult, ...]
    accepted_attempt_index: int
    rooms: tuple[GeneratedRoom, ...]
    room_map: tuple[int, ...]
    descriptor_configs: tuple[tuple[int, RoomConfigKey], ...]
    final_level_rng_state: int
    final_generator_rng_state: int
    final_boss_pool_state: int
    permanent_removed_bosses: tuple[int, ...]
    pending_boss_blacklist: tuple[int, ...]
    final_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    final_special_room_used_bits: tuple[int, ...]


def _entries(
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
) -> tuple[RoomConfigEntry, ...]:
    return (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(basement_definitions, stage=1)
    )


def _weight_mutations(
    before: dict[RoomConfigKey, float], after: dict[RoomConfigKey, float]
) -> tuple[tuple[RoomConfigKey, float, float], ...]:
    return tuple(
        (key, before.get(key, value), value)
        for key, value in sorted(after.items())
        if before.get(key, value) != value
    )


def _m6_boundary(
    *,
    start_seed: int,
    difficulty: str,
    stage_seed: int,
    attempt: SecretGenerationAttemptResult,
    run_state: RunGenerationState,
    level_rng: IsaacRNG,
    generator: LevelGeneratorResearch,
    boss_pool_index: int = 1,
) -> Basement1ThroughSecretResult:
    assert attempt.through_secret is not None
    return Basement1ThroughSecretResult(
        True,
        start_seed,
        difficulty,
        stage_seed,
        (attempt,),
        level_rng.seed,
        generator.rng.seed,
        run_state.boss_pools.pool_rngs[boss_pool_index].seed,
        tuple(sorted(run_state.boss_pools.removed)),
        tuple(sorted(run_state.boss_pools.level_blacklist)),
        tuple(sorted(run_state.room_config.weights.items())),
        tuple(sorted(run_state.special_room_used_bits)),
        attempt.through_secret.rooms,
    )


def generate_basement1_full(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Basement1FullResult:
    inputs = derive_basement1_topology_inputs(start_seed, difficulty)
    profile = CanonicalBasement1Profile(
        difficulty=difficulty,
        effective_curse_mask=inputs.effective_curse_mask,
        is_xl=inputs.is_xl,
    )
    profile.validate()
    entries = _entries(special_definitions, basement_definitions)
    run_state = RunGenerationState(
        start_seed,
        BossPoolRuntimeState.fresh_basement(start_seed, boss_entries),
        RoomConfigMutableState(),
        special_room_used_bits=set(profile.special_room_used_bits),
    )
    run_state.room_config.reset(entries)
    generator = LevelGeneratorResearch(inputs.generator_seed)
    generator.is_xl = profile.is_xl
    level_rng = IsaacRNG.game_constructor(inputs.generator_seed, LEVEL_SHIFT_INDEX)
    generator._m6_level_rng = level_rng
    floor_state = FloorGenerationState(
        inputs.stage_seed,
        target_room_count=inputs.target_room_count,
        level_rng=level_rng,
        level_generator=generator,
    )
    attempts: list[Basement1FullAttemptResult] = []

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
        m5: PostTopologyAttemptResult | None = None
        m6: PostTreasureThroughSecretResult | None = None
        m7: PostSecretThroughUltraResult | None = None
        late: LateDefaultPassResult | None = None
        abort: str | None = None

        if usable:
            m5 = run_post_topology_through_treasure(
                generator,
                run_state=run_state,
                floor_state=floor_state,
                entries=entries,
                profile=profile,
            )
            if not m5.completed:
                abort = m5.abort_operation
            else:
                m6 = run_treasure_to_secret(
                    m5,
                    generator=generator,
                    run_state=run_state,
                    entries=entries,
                    profile=profile,
                )
                if not m6.completed:
                    abort = m6.abort_operation
                else:
                    weights_after_m6 = dict(run_state.room_config.weights)
                    m6_attempt = SecretGenerationAttemptResult(
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
                        _weight_mutations(weights_before, weights_after_m6),
                        m5,
                        m6,
                    )
                    m7 = run_secret_to_ultra(
                        _m6_boundary(
                            start_seed=start_seed,
                            difficulty=difficulty,
                            stage_seed=inputs.stage_seed,
                            attempt=m6_attempt,
                            run_state=run_state,
                            level_rng=level_rng,
                            generator=generator,
                        ),
                        entries=entries,
                        profile=profile,
                    )
                    run_state.room_config.weights = dict(
                        m7.final_room_config_weights
                    )
                    generator.rng.seed = m7.final_generator_rng_state
                    late = assign_late_default_room_configs(
                        rooms=m7.rooms,
                        non_dead_ends=topology.non_dead_ends,
                        dead_ends=m7.dead_ends,
                        descriptor_configs=m7.descriptor_configs,
                        entries=entries,
                        room_config_weights=m7.final_room_config_weights,
                        level_rng_state=m7.final_level_rng_state,
                        difficulty=difficulty,
                    )
                    level_rng.seed = late.final_level_rng_state
                    run_state.room_config.weights = dict(
                        late.final_room_config_weights
                    )
                    if not late.completed:
                        abort = "Late ROOM_DEFAULT RoomConfig"
        else:
            abort = "Topology dead-end requirement"
            if (
                attempt_number >= 10
                and attempt_number % 5 == 0
                and floor_state.target_room_count < 64
            ):
                floor_state.target_room_count += 1

        attempts.append(
            Basement1FullAttemptResult(
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
                _weight_mutations(weights_before, run_state.room_config.weights),
                m5,
                m6,
                m7,
                late,
                abort,
            )
        )
        if late is not None and late.completed:
            run_state.boss_pools.commit_floor()
            run_state.current_stage_lifecycle = "basement1-full-layout-accepted"
            return Basement1FullResult(
                True,
                FULL_LAYOUT_STATUS,
                EXTERNAL_VALIDATION,
                start_seed,
                difficulty,
                inputs.stage_seed,
                tuple(attempts),
                attempt_number - 1,
                late.rooms,
                m7.room_map,
                late.descriptor_configs,
                level_rng.seed,
                generator.rng.seed,
                run_state.boss_pools.pool_rngs[1].seed,
                tuple(sorted(run_state.boss_pools.removed)),
                tuple(sorted(run_state.boss_pools.level_blacklist)),
                tuple(sorted(run_state.room_config.weights.items())),
                tuple(sorted(run_state.special_room_used_bits)),
            )

    return Basement1FullResult(
        False,
        "UNSUPPORTED — FAIL CLOSED",
        EXTERNAL_VALIDATION,
        start_seed,
        difficulty,
        inputs.stage_seed,
        tuple(attempts),
        -1,
        (),
        (),
        (),
        level_rng.seed,
        generator.rng.seed,
        run_state.boss_pools.pool_rngs[1].seed,
        tuple(sorted(run_state.boss_pools.removed)),
        tuple(sorted(run_state.boss_pools.level_blacklist)),
        tuple(sorted(run_state.room_config.weights.items())),
        tuple(sorted(run_state.special_room_used_bits)),
    )
