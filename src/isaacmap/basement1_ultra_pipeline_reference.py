"""Mechanical reference continuation from the M6 boundary through Ultra."""

from __future__ import annotations

from dataclasses import dataclass, replace

from .basement1_secret_pipeline_reference import (
    ReferenceBasement1ThroughSecretResult,
    generate_basement1_through_secret_reference,
)
from .boss_pool_reference import BossPoolEntryReference
from .generation_state import CanonicalBasement1Profile, CanonicalCaves1Profile
from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config_reference import (
    RoomConfigEntryReference,
    RoomConfigKey,
    RoomConfigMutableStateReference,
    RoomConfigQueryReference,
    RoomConfigSelectionReference,
    entries_from_definitions_reference,
    select_room_with_stage_fallback_reference,
)
from .special_rooms import GeneratedRoom
from .ultra_secret_reference import (
    UltraReferenceResult,
    UltraReferenceState,
    build_ultra_forbidden_indices_reference,
    place_ultra_secret_room_reference,
)


ULTRA_SHIFTS = (13, 3, 17)


def _advance(state: int, shifts: tuple[int, int, int]) -> int:
    a, b, c = shifts
    value = state & 0xFFFFFFFF
    value ^= value >> a
    value ^= (value << b) & 0xFFFFFFFF
    value ^= value >> c
    return value & 0xFFFFFFFF


@dataclass(frozen=True)
class ReferencePostSecretThroughUltraResult:
    ultra_room: int
    ultra_config: RoomConfigKey
    rooms: tuple[GeneratedRoom, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    blocked_positions: tuple[bool, ...]
    descriptor_configs: tuple[tuple[int, RoomConfigKey], ...]
    config_rng: tuple[int, int, int]
    selections: tuple[RoomConfigSelectionReference, ...]
    geometry: UltraReferenceResult
    final_level: int
    final_generator: int
    weights: tuple[tuple[RoomConfigKey, float], ...]
    used_bits: tuple[int, ...]


@dataclass(frozen=True)
class ReferenceBasement1ThroughUltraResult:
    boundary_completed: bool
    through_secret: ReferenceBasement1ThroughSecretResult
    final: ReferencePostSecretThroughUltraResult | None


def _entries(
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
) -> tuple[RoomConfigEntryReference, ...]:
    return (
        entries_from_definitions_reference(special_definitions, stage=0)
        + entries_from_definitions_reference(basement_definitions, stage=1)
    )


def run_secret_to_ultra_reference(
    through_secret: ReferenceBasement1ThroughSecretResult,
    *,
    entries: tuple[RoomConfigEntryReference, ...],
    profile: CanonicalBasement1Profile | CanonicalCaves1Profile | None = None,
) -> ReferencePostSecretThroughUltraResult:
    if not through_secret.boundary_completed:
        raise ValueError("reference Ultra continuation requires M6 completion")
    attempt = through_secret.attempts[-1]
    m5 = attempt.through_treasure
    m6 = attempt.through_secret
    if m5 is None or m6 is None:
        raise ValueError("reference final M6 attempt is incomplete")
    if profile is None:
        profile = CanonicalBasement1Profile("NORMAL")
    profile.validate()

    entry_by_key = {entry.key: entry for entry in entries}
    descriptors = {
        room_id: entry_by_key[key] for room_id, key in m6.descriptor_configs
    }
    weights = RoomConfigMutableStateReference(dict(through_secret.weights))
    config_seed = _advance(m5.snapshot, ULTRA_SHIFTS)
    selections = select_room_with_stage_fallback_reference(
        entries,
        weights,
        RoomConfigQueryReference(
            config_seed, True, profile.room_config_stage, 29, subtype=-1
        ),
        profile.fallback_room_config_stage,
    )
    ultra_entry = selections[-1].selected
    if ultra_entry is None:
        raise AssertionError("reference frozen resources have no type-29 config")

    rooms = [replace(room, neighbors=set(room.neighbors)) for room in m6.rooms]
    forbidden = build_ultra_forbidden_indices_reference(rooms, descriptors)
    state = UltraReferenceState(
        rooms,
        list(m6.room_map),
        list(m6.blocked_positions),
        IsaacRNG.game_constructor(m6.final_generator_rng_state, 35),
    )
    geometry = place_ultra_secret_room_reference(state, forbidden)
    if geometry.room_id >= 0:
        room = state.rooms[geometry.room_id]
        room.room_type = ultra_entry.room_type
        room.variant = ultra_entry.variant
        room.subtype = ultra_entry.subtype
        descriptors[geometry.room_id] = ultra_entry

    return ReferencePostSecretThroughUltraResult(
        ultra_room=geometry.room_id,
        ultra_config=ultra_entry.key,
        rooms=tuple(replace(room, neighbors=set(room.neighbors)) for room in state.rooms),
        room_map=tuple(state.room_map),
        dead_ends=m6.dead_ends,
        blocked_positions=m6.blocked_positions,
        descriptor_configs=tuple(
            sorted((room_id, entry.key) for room_id, entry in descriptors.items())
        ),
        config_rng=(m5.snapshot, config_seed, 71),
        selections=selections,
        geometry=geometry,
        final_level=m6.final_level_rng_state,
        final_generator=geometry.final_rng,
        weights=tuple(sorted(weights.weights.items())),
        used_bits=m6.used_bits_after,
    )


def generate_basement1_through_ultra_reference(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntryReference, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> ReferenceBasement1ThroughUltraResult:
    m6 = generate_basement1_through_secret_reference(
        start_seed,
        difficulty,
        boss_entries=boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        max_attempts=max_attempts,
    )
    if not m6.boundary_completed:
        return ReferenceBasement1ThroughUltraResult(False, m6, None)
    return ReferenceBasement1ThroughUltraResult(
        True,
        m6,
        run_secret_to_ultra_reference(
            m6, entries=_entries(special_definitions, basement_definitions)
        ),
    )
