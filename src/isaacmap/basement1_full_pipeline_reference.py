"""Mechanical accepted-layout reference for canonical frozen Basement I."""

from __future__ import annotations

from dataclasses import dataclass

from .basement1_pipeline_reference import ReferencePostResult, run_post_reference
from .basement1_secret_pipeline import PostTreasureThroughSecretResult
from .basement1_secret_pipeline_reference import (
    ReferenceBasement1ThroughSecretResult,
    ReferenceSecretAttempt,
    _topology_signature,
    run_treasure_to_secret_reference,
)
from .basement1_ultra_pipeline_reference import (
    ReferencePostSecretThroughUltraResult,
    run_secret_to_ultra_reference,
)
from .boss_pool_reference import (
    BossPoolEntryReference,
    BossPoolRuntimeReference,
)
from .floor_init import derive_basement1_topology_inputs
from .generation_state import CanonicalBasement1Profile
from .late_room_config_reference import (
    ReferenceLateDefaultResult,
    assign_late_default_room_configs_reference,
)
from .resources import RoomDefinition
from .room_config_reference import (
    RoomConfigEntryReference,
    RoomConfigKey,
    RoomConfigMutableStateReference,
    entries_from_definitions_reference,
)
from .special_rooms import GeneratedRoom
from .topology_reference import LevelGeneratorReference, ReferenceRoom


@dataclass(frozen=True)
class ReferenceBasement1FullAttempt:
    attempt: int
    target: int
    usable: bool
    topology_signature: tuple[object, ...]
    start_level: int
    end_level: int
    start_generator: int
    end_generator: int
    start_boss: int
    end_boss: int
    used_before: tuple[int, ...]
    used_after: tuple[int, ...]
    weight_mutations: tuple[tuple[RoomConfigKey, float, float], ...]
    through_treasure: ReferencePostResult | None
    through_secret: PostTreasureThroughSecretResult | None
    through_ultra: ReferencePostSecretThroughUltraResult | None
    late_default: ReferenceLateDefaultResult | None
    abort: str | None


@dataclass(frozen=True)
class ReferenceBasement1FullResult:
    completed: bool
    attempts: tuple[ReferenceBasement1FullAttempt, ...]
    accepted_attempt_index: int
    rooms: tuple[GeneratedRoom, ...]
    room_map: tuple[int, ...]
    descriptors: tuple[tuple[int, RoomConfigKey], ...]
    final_level: int
    final_generator: int
    final_boss: int
    removed: tuple[int, ...]
    pending_blacklist: tuple[int, ...]
    weights: tuple[tuple[RoomConfigKey, float], ...]
    used_bits: tuple[int, ...]


def _entries(
    special: tuple[RoomDefinition, ...], basement: tuple[RoomDefinition, ...]
) -> tuple[RoomConfigEntryReference, ...]:
    return (
        entries_from_definitions_reference(special, stage=0)
        + entries_from_definitions_reference(basement, stage=1)
    )


def _mutations(before, after):
    return tuple(
        (key, before.get(key, value), value)
        for key, value in sorted(after.items())
        if before.get(key, value) != value
    )


def generate_basement1_full_reference(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntryReference, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> ReferenceBasement1FullResult:
    profile = CanonicalBasement1Profile(difficulty)
    profile.validate()
    inputs = derive_basement1_topology_inputs(start_seed, difficulty)
    entries = _entries(special_definitions, basement_definitions)
    weights = RoomConfigMutableStateReference()
    weights.reset_pool(entries)
    bosses = BossPoolRuntimeReference.fresh_basement(start_seed, boss_entries)
    generator = LevelGeneratorReference(inputs.generator_seed, [])
    level_state = inputs.generator_seed
    target = inputs.target_room_count
    used_bits: set[int] = set(profile.special_room_used_bits)
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
            inputs.required_dead_ends,
            inputs.allowed_shapes_mask,
            ReferenceRoom(6, 6, 1),
        )
        topology = _topology_signature(generator)
        usable = len(generator.dead_ends) >= inputs.required_dead_ends
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
                        bosses.pool_states[1],
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
                        bosses.pool_states[1],
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
