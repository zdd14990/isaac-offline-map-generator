"""Mechanical Basement-II accepted-layout reference composition."""

from __future__ import annotations

from .basement1_full_pipeline_reference import (
    ReferenceBasement1FullAttempt,
    ReferenceBasement1FullResult,
    _mutations,
    generate_basement1_full_reference,
)
from .basement1_pipeline_reference import run_post_reference
from .basement1_secret_pipeline_reference import (
    ReferenceBasement1ThroughSecretResult,
    ReferenceSecretAttempt,
    _topology_signature,
    run_treasure_to_secret_reference,
)
from .basement1_ultra_pipeline_reference import run_secret_to_ultra_reference
from .boss_pool_reference import BossPoolEntryReference, BossPoolRuntimeReference
from .floor_init_reference import derive_basement2_topology_inputs_reference
from .generation_state import CanonicalBasement2Profile
from .late_room_config_reference import assign_late_default_room_configs_reference
from .post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from .resources import RoomDefinition
from .room_config_reference import (
    RoomConfigMutableStateReference,
    entries_from_definitions_reference,
)
from .topology_reference import LevelGeneratorReference, ReferenceRoom


def generate_basement2_full_reference(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntryReference, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> ReferenceBasement1FullResult:
    b1 = generate_basement1_full_reference(
        start_seed,
        difficulty,
        boss_entries=boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        max_attempts=max_attempts,
    )
    if not b1.completed:
        raise RuntimeError("reference Basement I layout did not complete")

    special = entries_from_definitions_reference(special_definitions, stage=0)
    basement = entries_from_definitions_reference(basement_definitions, stage=1)
    blue_womb = entries_from_definitions_reference(blue_womb_definitions, stage=13)
    entries = special + basement
    tail = run_post_layout_lifecycle_reference(
        level_rng_state=b1.final_level,
        entries=entries + blue_womb,
        room_config_weights=b1.weights,
        special_room_used_bits=b1.used_bits,
    )
    inputs = derive_basement2_topology_inputs_reference(start_seed, difficulty)
    profile = CanonicalBasement2Profile(
        difficulty,
        effective_curse_mask=inputs.curse_mask,
        special_room_used_bits=frozenset(tail.used_bits),
    )
    profile.validate()
    weights = RoomConfigMutableStateReference(dict(tail.weights))
    weights.reset_pool(basement)
    bosses = BossPoolRuntimeReference.resume_canonical_basement(
        start_seed,
        boss_entries,
        pool_state=b1.final_boss,
        removed=b1.removed,
    )
    generator = LevelGeneratorReference(inputs.generator_seed, [])
    level_state = inputs.generator_seed
    target = inputs.target
    used_bits = set(tail.used_bits)
    attempts: list[ReferenceBasement1FullAttempt] = []

    for number in range(1, max_attempts + 1):
        attempt_target = target
        bosses.begin_attempt()
        start_level = level_state
        start_generator = generator.rng.seed
        start_boss = bosses.pool_states[1]
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
                generator,
                level_state,
                bosses,
                weights,
                entries,
                profile,
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
                        bosses.pool_states[1],
                        used_before,
                        tuple(sorted(used_bits)),
                        _mutations(weights_before, weights.weights),
                        m5,
                        m6,
                    )
                    boundary = ReferenceBasement1ThroughSecretResult(
                        True,
                        (m6_attempt,),
                        level_state,
                        generator.rng.seed,
                        bosses.pool_states[1],
                        tuple(sorted(bosses.removed)),
                        tuple(sorted(bosses.level_blacklist)),
                        tuple(sorted(weights.weights.items())),
                        tuple(sorted(used_bits)),
                    )
                    m7 = run_secret_to_ultra_reference(boundary, entries=entries)
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
                bosses.pool_states[1],
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
                bosses.pool_states[1],
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
        bosses.pool_states[1],
        tuple(sorted(bosses.removed)),
        tuple(sorted(bosses.level_blacklist)),
        tuple(sorted(weights.weights.items())),
        tuple(sorted(used_bits)),
    )
