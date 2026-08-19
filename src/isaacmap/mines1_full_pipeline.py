"""Canonical Mines1 (2+) accepted-layout research composition.

Stage-3 ALT entry: StageType 4, rcs 29, slot 4, pool 29.  The first-half
mandatory end room (0x0033C416..0x0033C4D1) fires on every Mines1 floor.

Evidence grade: PARTIAL_BINARY.
"""

from __future__ import annotations

from dataclasses import dataclass

from .basement1_full_pipeline import (
    Basement1FullAttemptResult,
    Basement1FullResult,
    _m6_boundary,
    _weight_mutations,
)
from .basement1_pipeline import _topology_snapshot, run_post_topology_through_treasure
from .basement1_secret_pipeline import SecretGenerationAttemptResult, run_treasure_to_secret
from .basement1_ultra_pipeline import run_secret_to_ultra
from .boss_pool import MINES_POOL_INDEX, BossPoolEntry, BossPoolRuntimeState
from .floor_init import derive_alt_topology_inputs
from .generation_state import (
    CanonicalMines1Profile,
    FloorGenerationState,
    RunGenerationState,
)
from .late_room_config import assign_late_default_room_configs
from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config import RoomConfigMutableState, entries_from_definitions
from .special_rooms import GeneratedRoom
from .topology import LevelGeneratorResearch, LevelGeneratorRoom
from .topology_geometry import RoomShape


MINES1_LAYOUT_STATUS = "MINES1_FULL_LAYOUT_PIPELINE_PARTIAL_BINARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"
LEVEL_SHIFT_INDEX = 35


def generate_mines1_full(
    start_seed: int,
    difficulty: str,
    *,
    mines1_boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    mines1_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Basement1FullResult:
    """Generate Mines1 (ALT stage 2, rcs 28) from the run seed."""
    inputs = derive_alt_topology_inputs(3, 4, start_seed, difficulty)
    profile = CanonicalMines1Profile(
        difficulty,
        effective_curse_mask=inputs.effective_curse_mask,
        is_xl=inputs.is_xl,
    )
    profile.validate()
    entries = (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(mines1_definitions, stage=29)
    )
    run_state = RunGenerationState(
        start_seed,
        BossPoolRuntimeState.fresh_alt(start_seed, MINES_POOL_INDEX, mines1_boss_entries),
        RoomConfigMutableState(),
        special_room_used_bits=set(profile.special_room_used_bits),
    )
    run_state.room_config.reset(entries)
    generator = LevelGeneratorResearch(inputs.generator_seed)
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
        start_boss = run_state.boss_pools.pool_rngs[MINES_POOL_INDEX].seed
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
        m5 = None
        m6 = None
        m7 = None
        late = None
        abort = None

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
                        run_state.boss_pools.pool_rngs[MINES_POOL_INDEX].seed,
                        used_before,
                        tuple(sorted(run_state.special_room_used_bits)),
                        _weight_mutations(weights_before, run_state.room_config.weights),
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
                            boss_pool_index=MINES_POOL_INDEX,
                        ),
                        entries=entries,
                    )
                    run_state.room_config.weights = dict(m7.final_room_config_weights)
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
                        room_config_stage=profile.room_config_stage,
                        level_stage=profile.level_stage,
                    )
                    level_rng.seed = late.final_level_rng_state
                    run_state.room_config.weights = dict(late.final_room_config_weights)
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
                run_state.boss_pools.pool_rngs[MINES_POOL_INDEX].seed,
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
            run_state.current_stage_lifecycle = "mines1-full-layout-accepted"
            return Basement1FullResult(
                True,
                MINES1_LAYOUT_STATUS,
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
                run_state.boss_pools.pool_rngs[MINES_POOL_INDEX].seed,
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
        run_state.boss_pools.pool_rngs[MINES_POOL_INDEX].seed,
        tuple(sorted(run_state.boss_pools.removed)),
        tuple(sorted(run_state.boss_pools.level_blacklist)),
        tuple(sorted(run_state.room_config.weights.items())),
        tuple(sorted(run_state.special_room_used_bits)),
    )
