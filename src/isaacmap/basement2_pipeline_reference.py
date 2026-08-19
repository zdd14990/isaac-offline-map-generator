"""Mechanical Basement-II reference composition through Treasure."""

from __future__ import annotations

from .basement1_full_pipeline_reference import generate_basement1_full_reference
from .basement1_pipeline_reference import (
    ReferenceBasement1Result,
    ReferenceGenerationAttempt,
    _room_signature,
    run_post_reference,
)
from .boss_pool_reference import BossPoolEntryReference, BossPoolRuntimeReference
from .floor_init_reference import derive_basement2_topology_inputs_reference
from .generation_state import CanonicalBasement2Profile
from .post_layout_lifecycle_reference import run_post_layout_lifecycle_reference
from .resources import RoomDefinition
from .room_config_reference import (
    RoomConfigMutableStateReference,
    entries_from_definitions_reference,
)
from .topology_reference import LevelGeneratorReference, ReferenceRoom


def generate_basement2_through_treasure_reference(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntryReference, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    blue_womb_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> ReferenceBasement1Result:
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
    tail = run_post_layout_lifecycle_reference(
        level_rng_state=b1.final_level,
        entries=special + basement + blue_womb,
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
    attempts: list[ReferenceGenerationAttempt] = []

    for number in range(1, max_attempts + 1):
        attempt_target = target
        bosses.begin_attempt()
        start_level = level_state
        start_generator = generator.rng.seed
        start_boss = bosses.pool_states[1]
        before = dict(weights.weights)
        generator.blocked_positions[:] = [False] * 169
        generator.attempt = number
        generator.generate_once(
            target,
            inputs.dead_ends,
            inputs.shapes,
            ReferenceRoom(6, 6, 1),
        )
        usable = len(generator.dead_ends) >= inputs.dead_ends
        post = None
        if usable:
            post = run_post_reference(
                generator, level_state, bosses, weights, special + basement, profile
            )
            level_state = post.final_level_rng_state
        elif number >= 10 and number % 5 == 0 and target < 64:
            target += 1
        mutations = tuple(
            (key, before.get(key, value), value)
            for key, value in sorted(weights.weights.items())
            if before.get(key, value) != value
        )
        attempts.append(
            ReferenceGenerationAttempt(
                number,
                attempt_target,
                usable,
                _room_signature(generator),
                start_level,
                level_state,
                start_generator,
                generator.rng.seed,
                start_boss,
                bosses.pool_states[1],
                tuple(sorted(bosses.level_blacklist)),
                tuple(sorted(bosses.removed)),
                mutations,
                post,
            )
        )
        if post is not None and post.completed:
            return ReferenceBasement1Result(
                True,
                tuple(attempts),
                level_state,
                generator.rng.seed,
                bosses.pool_states[1],
                tuple(sorted(bosses.removed)),
                tuple(sorted(weights.weights.items())),
            )
    return ReferenceBasement1Result(
        False,
        tuple(attempts),
        level_state,
        generator.rng.seed,
        bosses.pool_states[1],
        tuple(sorted(bosses.removed)),
        tuple(sorted(weights.weights.items())),
    )
