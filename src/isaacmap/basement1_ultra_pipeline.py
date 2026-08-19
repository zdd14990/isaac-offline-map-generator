"""Clean canonical Basement I continuation through Ultra Secret.

The returned boundary is still not a complete accepted floor.  The late
ordinary ROOM_DEFAULT configuration pass follows and may reject the attempt.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .basement1_secret_pipeline import (
    Basement1ThroughSecretResult,
    PostTreasureThroughSecretResult,
    generate_basement1_through_secret,
)
from .boss_pool import BossPoolEntry
from .generation_state import (
    CanonicalBasement1Profile,
    CanonicalBasement2Profile,
    CanonicalCaves1Profile,
)
from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config import (
    RoomConfigEntry,
    RoomConfigKey,
    RoomConfigMutableState,
    RoomConfigQuery,
    RoomConfigSelection,
    entries_from_definitions,
    select_room_with_stage_fallback,
)
from .special_rooms import GeneratedRoom
from .ultra_secret import (
    GENERATOR_SHIFT_INDEX,
    ULTRA_CONFIG_SHIFT_INDEX,
    UltraGeometryState,
    UltraPlacementResult,
    build_ultra_forbidden_indices,
    place_ultra_secret_room,
)


@dataclass(frozen=True)
class UltraConfigRNGTransition:
    binary_rva: int
    object_identity: str
    shift_index: int
    pre_state: int
    post_state: int
    reason: str


@dataclass(frozen=True)
class UltraDescriptorMutation:
    created: bool
    generator_room_id: int
    list_index: int
    grid_index: int
    safe_grid_index: int
    room_shape: int
    room_type: int
    descriptor_count_before: int
    descriptor_count_after: int
    dead_ends_before: tuple[int, ...]
    dead_ends_after: tuple[int, ...]
    level_descriptor_tail_field: int | None


@dataclass(frozen=True)
class PostSecretThroughUltraResult:
    completed: bool
    ultra_room: int
    ultra_config: RoomConfigKey | None
    rooms: tuple[GeneratedRoom, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    blocked_positions: tuple[bool, ...]
    descriptor_configs: tuple[tuple[int, RoomConfigKey], ...]
    ultra_config_rng: UltraConfigRNGTransition
    ultra_config_selections: tuple[RoomConfigSelection, ...]
    ultra_geometry: UltraPlacementResult
    ultra_descriptor: UltraDescriptorMutation
    final_level_rng_state: int
    final_generator_rng_state: int
    final_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    special_room_used_bits: tuple[int, ...]


@dataclass(frozen=True)
class Basement1ThroughUltraResult:
    boundary_completed: bool
    start_seed: int
    difficulty: str
    stage_seed: int
    through_secret: Basement1ThroughSecretResult
    final: PostSecretThroughUltraResult | None


def _entries(
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
) -> tuple[RoomConfigEntry, ...]:
    return (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(basement_definitions, stage=1)
    )


def run_secret_to_ultra(
    through_secret: Basement1ThroughSecretResult,
    *,
    entries: tuple[RoomConfigEntry, ...],
    profile: CanonicalBasement1Profile | CanonicalBasement2Profile | CanonicalCaves1Profile | None = None,
) -> PostSecretThroughUltraResult:
    """Continue the final M6 boundary without reimplementing earlier stages."""

    if not through_secret.boundary_completed or not through_secret.attempts:
        raise ValueError("Ultra continuation requires a completed Secret boundary")
    attempt = through_secret.attempts[-1]
    m5 = attempt.through_treasure
    m6 = attempt.through_secret
    if m5 is None or m6 is None or not m6.completed:
        raise ValueError("Ultra continuation requires final attempt M5/M6 state")
    if profile is None:
        profile = CanonicalBasement1Profile(through_secret.difficulty)
    if profile.difficulty != through_secret.difficulty:
        raise ValueError("Ultra profile difficulty does not match the boundary")
    profile.validate()

    entry_by_key = {entry.key: entry for entry in entries}
    descriptors = {
        room_id: entry_by_key[key] for room_id, key in m6.descriptor_configs
    }
    weights = RoomConfigMutableState(dict(through_secret.final_room_config_weights))

    # The saved post-Type8 snapshot seeds a separate index-71 object.  Binary
    # advances it exactly once and passes that state to the type-29 selector.
    config_rng = IsaacRNG.game_constructor(
        m5.post_type8_seed_snapshot, ULTRA_CONFIG_SHIFT_INDEX
    )
    config_pre = config_rng.seed
    config_seed = config_rng.next()
    config_transition = UltraConfigRNGTransition(
        0x0033C977,
        "Ultra.config.private",
        ULTRA_CONFIG_SHIFT_INDEX,
        config_pre,
        config_seed,
        "derive RoomType 29 selector/assignment seed from post-Type8 snapshot",
    )
    selections = select_room_with_stage_fallback(
        entries,
        weights,
        RoomConfigQuery(
            config_seed,
            True,
            profile.room_config_stage,
            29,
            subtype=-1,
        ),
        profile.fallback_room_config_stage,
    )
    ultra_entry = selections[-1].entry
    if ultra_entry is None:
        raise AssertionError("frozen resources have no Ultra Secret RoomConfig")

    rooms = [replace(room, neighbors=set(room.neighbors)) for room in m6.rooms]
    room_map = list(m6.room_map)
    blocked = list(m6.blocked_positions)
    forbidden = build_ultra_forbidden_indices(rooms, descriptors)

    # Geometry does not consume the index-71 object.  PlaceUltraSecretRoom is
    # a LevelGenerator method and continues its persistent index-35 RNG.
    geometry_state = UltraGeometryState(
        rooms,
        room_map,
        blocked,
        IsaacRNG.game_constructor(
            m6.final_generator_rng_state, GENERATOR_SHIFT_INDEX
        ),
    )
    descriptor_count_before = len(descriptors)
    geometry = place_ultra_secret_room(geometry_state, forbidden)
    if geometry.room_id >= 0:
        room = geometry_state.rooms[geometry.room_id]
        room.room_type = ultra_entry.room_type
        room.variant = ultra_entry.variant
        room.subtype = ultra_entry.subtype
        descriptors[geometry.room_id] = ultra_entry

    mutation = UltraDescriptorMutation(
        created=geometry.room_id >= 0,
        generator_room_id=geometry.room_id,
        list_index=descriptor_count_before if geometry.room_id >= 0 else -1,
        grid_index=geometry.grid_index,
        safe_grid_index=geometry.grid_index,
        room_shape=1 if geometry.room_id >= 0 else 0,
        room_type=29 if geometry.room_id >= 0 else 0,
        descriptor_count_before=descriptor_count_before,
        descriptor_count_after=len(descriptors),
        dead_ends_before=m6.dead_ends,
        dead_ends_after=m6.dead_ends,
        # The direct caller writes 99 to the assigned Level RoomDescriptor's
        # trailing field after a successful assignment (RVA 0x0033CB24).
        level_descriptor_tail_field=99 if geometry.room_id >= 0 else None,
    )
    return PostSecretThroughUltraResult(
        completed=True,
        ultra_room=geometry.room_id,
        ultra_config=ultra_entry.key,
        rooms=tuple(
            replace(room, neighbors=set(room.neighbors))
            for room in geometry_state.rooms
        ),
        room_map=tuple(geometry_state.room_map),
        dead_ends=m6.dead_ends,
        blocked_positions=m6.blocked_positions,
        descriptor_configs=tuple(
            sorted((room_id, entry.key) for room_id, entry in descriptors.items())
        ),
        ultra_config_rng=config_transition,
        ultra_config_selections=selections,
        ultra_geometry=geometry,
        ultra_descriptor=mutation,
        final_level_rng_state=m6.final_level_rng_state,
        final_generator_rng_state=geometry.final_generator_rng_state,
        final_room_config_weights=tuple(sorted(weights.weights.items())),
        special_room_used_bits=m6.used_bits_after,
    )


def generate_basement1_through_ultra(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Basement1ThroughUltraResult:
    m6 = generate_basement1_through_secret(
        start_seed,
        difficulty,
        boss_entries=boss_entries,
        special_definitions=special_definitions,
        basement_definitions=basement_definitions,
        max_attempts=max_attempts,
    )
    if not m6.boundary_completed:
        return Basement1ThroughUltraResult(
            False, start_seed, difficulty, m6.stage_seed, m6, None
        )
    final = run_secret_to_ultra(
        m6, entries=_entries(special_definitions, basement_definitions)
    )
    return Basement1ThroughUltraResult(
        True, start_seed, difficulty, m6.stage_seed, m6, final
    )
