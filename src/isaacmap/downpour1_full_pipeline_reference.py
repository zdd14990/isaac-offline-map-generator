"""Mechanical Downpour-I accepted-layout reference composition.

Independent orchestration reference for the Stage-1 ALT entry (stage_type 4,
rcs 27, slot 2).  It never calls a clean high-level pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass

from .basement1_full_pipeline_reference import (
    ReferenceBasement1FullAttempt,
    ReferenceBasement1FullResult,
    _mutations,
)
from .basement1_pipeline_reference import run_post_reference
from .basement1_secret_pipeline import PostTreasureThroughSecretResult
from .basement1_secret_pipeline_reference import (
    ReferenceBasement1ThroughSecretResult,
    ReferenceSecretAttempt,
    _topology_signature,
    run_treasure_to_secret_reference,
)
from .basement1_ultra_pipeline_reference import run_secret_to_ultra_reference
from .boss_pool_reference import (
    DOWNPOUR_POOL_INDEX,
    BossPoolEntryReference,
    BossPoolRuntimeReference,
)
from .floor_init_reference import derive_alt_topology_inputs_reference
from .generation_state import CanonicalDownpour1Profile
from .late_room_config_reference import assign_late_default_room_configs_reference
from .resources import RoomDefinition
from .room_config_reference import (
    RoomConfigMutableStateReference,
    entries_from_definitions_reference,
)
from .topology_reference import LevelGeneratorReference, ReferenceRoom


def generate_downpour1_full_reference(
    start_seed: int,
    difficulty: str,
    *,
    downpour_boss_entries: tuple[BossPoolEntryReference, ...],
    special_definitions: tuple[RoomDefinition, ...],
    downpour_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> ReferenceBasement1FullResult:
    inputs = derive_alt_topology_inputs_reference(1, 4, start_seed, difficulty)
    profile = CanonicalDownpour1Profile(
        difficulty,
        effective_curse_mask=inputs.curse_mask,
        is_xl=inputs.is_xl,
    )
    profile.validate()
    entries = (
        entries_from_definitions_reference(special_definitions, stage=0)
        + entries_from_definitions_reference(downpour_definitions, stage=27)
    )
    weights = RoomConfigMutableStateReference()
    weights.reset_pool(entries)
    bosses = BossPoolRuntimeReference.fresh_alt(
        start_seed, DOWNPOUR_POOL_INDEX, downpour_boss_entries
    )
    generator = LevelGeneratorReference(inputs.generator_seed, [])
    level_state = inputs.generator_seed
    target = inputs.target
    used_bits: set[int] = set(profile.special_room_used_bits)
    attempts: list[ReferenceBasement1FullAttempt] = []

    for number in range(1, max_attempts + 1):
        attempt_target = target
        bosses.begin_attempt()
        start_level = level_state
        start_generator = generator.rng.seed
        start_boss = bosses.pool_states[DOWNPOUR_POOL_INDEX]
        used_before = tuple(sorted(used_bits))
        weights_before = dict(weights.weights)
        generator.blocked_positions[:] = [False] * 169
        generator.attempt = number
        generator.generate_once(
            target,
            inputs.dead_ends,
            inputs.shapes,
            ReferenceRoom(6, 6, 1),
        )
        topology = _topology_signature(generator)
        usable = len(generator.dead_ends) >= inputs.dead_ends
        m5 = None
        m6 = None
        m7 = None
        late = None
        abort = None

        if usable:
            m5 = run_post_reference(
                generator, level_state, bosses, weights, entries, profile
            )
            level_state = m5.final_level_rng_state
            if not m5.completed:
                abort = m5.abort
            else:
                m6 = run_treasure_to_secret_reference(
                    m5,
                    generator=generator,
                    weights=weights,
                    entries=entries,
                    profile=profile,
                    used_bits=used_bits,
                )
                level_state = m6.final_level_rng_state
                if not m6.completed:
                    abort = m6.abort_operation
                else:
                    weights_after_m6 = dict(weights.weights)
                    m6_attempt = ReferenceSecretAttempt(
                        number,
                        attempt_target,
                        usable,
                        topology,
                        start_level,
                        level_state,
                        start_generator,
                        generator.rng.seed,
                        start_boss,
                        bosses.pool_states[DOWNPOUR_POOL_INDEX],
                        used_before,
                        tuple(sorted(used_bits)),
                        _mutations(weights_before, weights_after_m6),
                        m5,
                        m6,
                    )
                    boundary = ReferenceBasement1ThroughSecretResult(
                        True,
                        (m6_attempt,),
                        level_state,
                        generator.rng.seed,
                        bosses.pool_states[DOWNPOUR_POOL_INDEX],
                        tuple(sorted(bosses.removed)),
                        tuple(sorted(bosses.level_blacklist)),
                        tuple(sorted(weights.weights.items())),
                        tuple(sorted(used_bits)),
                    )
                    m7 = run_secret_to_ultra_reference(
                        boundary, entries=entries
                    )
                    generator.rng.seed = m7.final_generator
                    weights.weights = dict(m7.weights)
                    late = assign_late_default_room_configs_reference(
                        rooms=m7.rooms,
                        non_dead_ends=topology[3],
                        dead_ends=m7.dead_ends,
                        descriptor_configs=m7.descriptor_configs,
                        entries=entries,
                        room_config_weights=m7.weights,
                        level_rng_state=m7.final_level,
                        difficulty=difficulty,
                        room_config_stage=profile.room_config_stage,
                        level_stage=profile.level_stage,
                    )
                    level_state = late.final_level
                    weights.weights = dict(late.weights)
                    if not late.completed:
                        abort = "Late ROOM_DEFAULT RoomConfig"
        else:
            abort = "Topology dead-end requirement"
            if number >= 10 and number % 5 == 0 and target < 64:
                target += 1

        attempts.append(
            ReferenceBasement1FullAttempt(
                number,
                attempt_target,
                usable,
                topology,
                start_level,
                level_state,
                start_generator,
                generator.rng.seed,
                start_boss,
                bosses.pool_states[DOWNPOUR_POOL_INDEX],
                used_before,
                tuple(sorted(used_bits)),
                _mutations(weights_before, weights.weights),
                m5,
                m6,
                m7,
                late,
                abort,
            )
        )
        if late is not None and late.completed:
            bosses.commit_floor()
            return ReferenceBasement1FullResult(
                True,
                tuple(attempts),
                number - 1,
                late.rooms,
                m7.room_map,
                late.descriptors,
                level_state,
                generator.rng.seed,
                bosses.pool_states[DOWNPOUR_POOL_INDEX],
                tuple(sorted(bosses.removed)),
                tuple(sorted(bosses.level_blacklist)),
                tuple(sorted(weights.weights.items())),
                tuple(sorted(used_bits)),
            )

    return ReferenceBasement1FullResult(
        False,
        tuple(attempts),
        -1,
        (),
        (),
        (),
        level_state,
        generator.rng.seed,
        bosses.pool_states[DOWNPOUR_POOL_INDEX],
        tuple(sorted(bosses.removed)),
        tuple(sorted(bosses.level_blacklist)),
        tuple(sorted(weights.weights.items())),
        tuple(sorted(used_bits)),
    )
