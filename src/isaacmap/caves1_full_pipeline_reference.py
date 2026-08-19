"""Mechanical Caves-I accepted-layout reference composition.

Independent orchestration reference.  It composes the already binary-confirmed
reference leaves (topology, Boss/Treasure, Secret, Ultra, late RoomConfig,
post-layout tail) through the Stage-3 attempt transaction, using the Caves
BossPool (index 4) seeded from ``bosspools.xml["caves"]``.  It does not call
the clean high-level pipeline.
"""

from __future__ import annotations

from .basement1_full_pipeline_reference import (
    ReferenceBasement1FullAttempt,
    ReferenceBasement1FullResult,
    _mutations,
)
from .basement1_pipeline_reference import run_post_reference
from .basement1_secret_pipeline_reference import (
    ReferenceBasement1ThroughSecretResult,
    ReferenceSecretAttempt,
    _topology_signature,
    run_treasure_to_secret_reference,
)
from .basement1_ultra_pipeline_reference import run_secret_to_ultra_reference
from .basement2_full_pipeline_reference import generate_basement2_full_reference
from .boss_pool_reference import (
    CAVES_POOL_INDEX,
    BossPoolEntryReference,
    BossPoolRuntimeReference,
    derive_pool_seeds_reference,
)
from .floor_init_reference import derive_caves1_topology_inputs_reference
from .generation_state import CanonicalCaves1Profile
from .late_room_config_reference import assign_late_default_room_configs_reference
from .post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from .resources import RoomDefinition
from .room_config_reference import (
    RoomConfigMutableStateReference,
    entries_from_definitions_reference,
)
from .topology_reference import LevelGeneratorReference, ReferenceRoom


def generate_caves1_full_reference(
    start_seed: int,
    difficulty: str,
    *,
    basement_boss_entries: tuple[BossPoolEntryReference, ...],
    caves_boss_entries: tuple[BossPoolEntryReference, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    caves_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> ReferenceBasement1FullResult:
    b2 = generate_basement2_full_reference(
        start_seed,
        difficulty,
        boss_entries=basement_boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        blue_womb_definitions=blue_womb_definitions,
        max_attempts=max_attempts,
    )
    if not b2.completed:
        raise RuntimeError("reference Basement II layout did not complete")

    special = entries_from_definitions_reference(special_definitions, stage=0)
    basement = entries_from_definitions_reference(basement_definitions, stage=1)
    caves = entries_from_definitions_reference(caves_definitions, stage=4)
    blue_womb = entries_from_definitions_reference(blue_womb_definitions, stage=13)

    # Basement II successful tail -> Caves I entry state (weights/used-bits).
    b2_tail = run_post_layout_lifecycle_reference(
        level_rng_state=b2.final_level,
        entries=special + basement + blue_womb,
        room_config_weights=b2.weights,
        special_room_used_bits=b2.used_bits,
        level_stage=2,
    )

    inputs = derive_caves1_topology_inputs_reference(start_seed, difficulty)
    profile = CanonicalCaves1Profile(
        difficulty,
        effective_curse_mask=inputs.curse_mask,
        is_xl=inputs.is_xl,
        special_room_used_bits=frozenset(b2_tail.used_bits),
    )
    profile.validate()

    entries = special + basement + caves + blue_womb
    weights = RoomConfigMutableStateReference(dict(b2_tail.weights))
    weights.reset_pool(caves)

    seeds = derive_pool_seeds_reference(start_seed)
    bosses = BossPoolRuntimeReference.resume_canonical_caves(
        start_seed,
        caves_boss_entries,
        pool_state=seeds[CAVES_POOL_INDEX],
        removed=b2.removed,
    )

    generator = LevelGeneratorReference(inputs.generator_seed, [])
    level_state = inputs.generator_seed
    target = inputs.target
    used_bits = set(b2_tail.used_bits)
    attempts: list[ReferenceBasement1FullAttempt] = []

    for number in range(1, max_attempts + 1):
        attempt_target = target
        bosses.begin_attempt()
        start_level = level_state
        start_generator = generator.rng.seed
        start_boss = bosses.pool_states[CAVES_POOL_INDEX]
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
                        bosses.pool_states[CAVES_POOL_INDEX],
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
                        bosses.pool_states[CAVES_POOL_INDEX],
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
                bosses.pool_states[CAVES_POOL_INDEX],
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
                bosses.pool_states[CAVES_POOL_INDEX],
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
        bosses.pool_states[CAVES_POOL_INDEX],
        tuple(sorted(bosses.removed)),
        tuple(sorted(bosses.level_blacklist)),
        tuple(sorted(weights.weights.items())),
        tuple(sorted(used_bits)),
    )
