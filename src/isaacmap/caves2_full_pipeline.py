"""Canonical Caves-II accepted-layout research composition.

All geometry and selection work is delegated to existing clean leaves.  This
module owns only the Stage-4 replay/attempt transaction and does not perform
the successful post-layout lifecycle handoff to later floors.
"""

from __future__ import annotations

from dataclasses import dataclass

from .basement1_full_pipeline import (
    Basement1FullAttemptResult,
    _m6_boundary,
    _weight_mutations,
)
from .basement1_pipeline import _topology_snapshot, run_post_topology_through_treasure
from .basement1_secret_pipeline import SecretGenerationAttemptResult, run_treasure_to_secret
from .basement1_ultra_pipeline import run_secret_to_ultra
from .boss_pool import (
    BossPoolEntry,
    BossPoolRuntimeState,
    BASEMENT_POOL_INDEX,
    CAVES_POOL_INDEX,
    POOL_SHIFT_INDEX,
    derive_pool_seeds,
    shuffle_entries,
)
from .caves1_full_pipeline import Caves1FullResult
from .floor_init import derive_caves2_topology_inputs
from .generation_state import CanonicalCaves2Profile, FloorGenerationState, RunGenerationState
from .late_room_config import assign_late_default_room_configs
from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config import RoomConfigKey, RoomConfigMutableState, entries_from_definitions
from .special_rooms import GeneratedRoom
from .topology import LevelGeneratorResearch, LevelGeneratorRoom
from .topology_geometry import RoomShape


CAVES2_LAYOUT_STATUS = "CAVES2_FULL_LAYOUT_PIPELINE_CONFIRMED_BINARY"
EXTERNAL_VALIDATION = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"
LEVEL_SHIFT_INDEX = 35


@dataclass(frozen=True)
class Caves2FullResult:
    completed: bool
    generation_status: str
    external_validation: str
    start_seed: int
    difficulty: str
    stage_seed: int
    replayed_caves1: Caves1FullResult
    entry_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
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


def generate_caves2_full(
    caves1_result: Caves1FullResult,
    entry_state_snapshot: "CanonicalRunGenerationSnapshot",
    *,
    basement_boss_entries: tuple[BossPoolEntry, ...],
    caves_boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    caves_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Caves2FullResult:
    """Generate Caves II from a successful Caves I result and explicit entry state.

    The entry state must be a CanonicalRunGenerationSnapshot with next_level_stage=4
    and completed_level_stage=3, typically from Caves1LifecycleResult.next_run_state.
    The Caves BossPool (index 4) RNG state is inherited (advanced) from Caves I.
    """
    from .generation_state import CanonicalRunGenerationSnapshot

    snapshot = entry_state_snapshot
    if snapshot.next_level_stage != 4 or snapshot.completed_level_stage != 3:
        raise ValueError(
            f"Caves II entry requires snapshot with "
            f"next_level_stage=4, completed_level_stage=3; "
            f"got next={snapshot.next_level_stage}, completed={snapshot.completed_level_stage}"
        )

    start_seed = snapshot.game_start_seed

    inputs = derive_caves2_topology_inputs(start_seed, caves1_result.difficulty)
    profile = CanonicalCaves2Profile(
        caves1_result.difficulty,
        effective_curse_mask=inputs.effective_curse_mask,
        is_xl=inputs.is_xl,
        special_room_used_bits=frozenset(snapshot.special_room_used_bits),
    )
    profile.validate()

    # Load all room entries: stage 0 (special), 1 (basement), 4 (caves), 13 (blue_womb)
    special_entries = entries_from_definitions(special_definitions, stage=0)
    basement_entries = entries_from_definitions(basement_definitions, stage=1)
    caves_entries = entries_from_definitions(caves_definitions, stage=4)
    blue_womb_entries = entries_from_definitions(blue_womb_definitions, stage=13)
    entries = special_entries + basement_entries + caves_entries + blue_womb_entries

    # Initialize room config: preserve previous stages, reset only stage 4
    room_config = RoomConfigMutableState(dict(snapshot.room_config_weights))
    room_config.reset(caves_entries)
    entry_weights = tuple(sorted(room_config.weights.items()))

    # Resume BossPool for Caves II: the Caves pool (4) continues from Caves I.
    seeds = derive_pool_seeds(start_seed)
    pool_rngs = [IsaacRNG.game_constructor(seed, POOL_SHIFT_INDEX) for seed in seeds]
    pool_rngs[BASEMENT_POOL_INDEX].seed = snapshot.boss_pool_rng_states[BASEMENT_POOL_INDEX]
    pool_rngs[CAVES_POOL_INDEX].seed = snapshot.boss_pool_rng_states[CAVES_POOL_INDEX]

    bosses = BossPoolRuntimeState(
        game_start_seed=start_seed,
        pool_seeds=seeds,
        pool_rngs=pool_rngs,
        shuffled_entries={
            BASEMENT_POOL_INDEX: shuffle_entries(basement_boss_entries, seeds[BASEMENT_POOL_INDEX]),
            CAVES_POOL_INDEX: shuffle_entries(caves_boss_entries, seeds[CAVES_POOL_INDEX]),
        },
        removed=set(snapshot.permanent_removed_bosses),
        level_blacklist=set(),
    )

    run_state = RunGenerationState(
        start_seed,
        bosses,
        room_config,
        "caves1-success-tail-complete/caves2-entered",
        set(snapshot.special_room_used_bits),
    )

    # Initialize LevelGenerator and Level RNG for Stage 4
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
        start_boss = run_state.boss_pools.pool_rngs[CAVES_POOL_INDEX].seed
        used_before = tuple(sorted(run_state.special_room_used_bits))
        weights_before = dict(run_state.room_config.weights)

        # Clear blocked positions and generate topology
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
                        run_state.boss_pools.pool_rngs[CAVES_POOL_INDEX].seed,
                        used_before,
                        tuple(sorted(run_state.special_room_used_bits)),
                        _weight_mutations(weights_before, run_state.room_config.weights),
                        m5,
                        m6,
                    )
                    m7 = run_secret_to_ultra(
                        _m6_boundary(
                            start_seed=start_seed,
                            difficulty=caves1_result.difficulty,
                            stage_seed=inputs.stage_seed,
                            attempt=m6_attempt,
                            run_state=run_state,
                            level_rng=level_rng,
                            generator=generator,
                        ),
                        entries=entries,
                        profile=profile,
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
                        difficulty=caves1_result.difficulty,
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
                run_state.boss_pools.pool_rngs[CAVES_POOL_INDEX].seed,
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
            run_state.current_stage_lifecycle = "caves2-full-layout-accepted"
            return Caves2FullResult(
                True,
                CAVES2_LAYOUT_STATUS,
                EXTERNAL_VALIDATION,
                start_seed,
                caves1_result.difficulty,
                inputs.stage_seed,
                caves1_result,
                entry_weights,
                tuple(attempts),
                attempt_number - 1,
                late.rooms,
                m7.room_map,
                late.descriptor_configs,
                level_rng.seed,
                generator.rng.seed,
                run_state.boss_pools.pool_rngs[CAVES_POOL_INDEX].seed,
                tuple(sorted(run_state.boss_pools.removed)),
                tuple(sorted(run_state.boss_pools.level_blacklist)),
                tuple(sorted(run_state.room_config.weights.items())),
                tuple(sorted(run_state.special_room_used_bits)),
            )

    return Caves2FullResult(
        False,
        "UNSUPPORTED — FAIL CLOSED",
        EXTERNAL_VALIDATION,
        start_seed,
        caves1_result.difficulty,
        inputs.stage_seed,
        caves1_result,
        entry_weights,
        tuple(attempts),
        -1,
        (),
        (),
        (),
        level_rng.seed,
        generator.rng.seed,
        run_state.boss_pools.pool_rngs[CAVES_POOL_INDEX].seed,
        tuple(sorted(run_state.boss_pools.removed)),
        tuple(sorted(run_state.boss_pools.level_blacklist)),
        tuple(sorted(run_state.room_config.weights.items())),
        tuple(sorted(run_state.special_room_used_bits)),
    )
