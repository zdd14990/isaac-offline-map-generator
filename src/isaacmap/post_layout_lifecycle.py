"""Successful post-layout lifecycle tail for canonical ORIGINAL floors.

The accepted 13x13 map is already final when this leaf starts.  The binary
then initializes fixed negative-GridIndex descriptors and advances persistent
generation state needed by later floors.  No branch in this leaf can reject
or alter the accepted ordinary map.
"""

from __future__ import annotations

from dataclasses import dataclass

from .rng import IsaacRNG
from .room_config import (
    RoomConfigEntry,
    RoomConfigKey,
    RoomConfigMutableState,
    RoomConfigQuery,
    RoomConfigSelection,
    select_room,
)
from .room_config_reference import f32


LEVEL_SHIFT_INDEX = 35
DESCRIPTOR_DERIVED_SHIFT_INDEX = 66
SHOP_PRIVATE_SHIFT_INDEX = 19
ANGEL_PRIVATE_SHIFT_INDEX = 20

DOOR_CHANCE_FIRST_RVA = 0x0033D2B8
DOOR_CHANCE_SECOND_RVA = 0x0033D363
SHOP_PRIVATE_SEED_RVA = 0x0033D731
ANGEL_PRIVATE_SEED_RVA = 0x0033D7E9


@dataclass(frozen=True)
class LifecycleRNGTransition:
    binary_rva: int
    identity: str
    pre_state: int
    post_state: int
    reason: str


@dataclass(frozen=True)
class FixedDescriptorAssignment:
    grid_index: int
    room_type: int
    subtype: int
    descriptor_seeds: tuple[int, int, int, int]
    selector_seed: int
    config: RoomConfigKey | None
    selection: RoomConfigSelection


@dataclass(frozen=True)
class PostLayoutLifecycleResult:
    completed: bool
    assignments: tuple[FixedDescriptorAssignment, ...]
    rng_transitions: tuple[LifecycleRNGTransition, ...]
    persistent_level_draw_count: int
    final_level_rng_state: int
    final_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    final_special_room_used_bits: tuple[int, ...]
    cleared_special_counter: int
    skipped_optional_grid_indices: tuple[int, ...]


@dataclass(frozen=True)
class _FixedSpec:
    grid_index: int
    room_type: int
    stage: int
    subtype: int
    helper_rva: int
    selector_seed_rva: int


_CANONICAL_FIXED_SPECS = (
    _FixedSpec(-2, 3, 0, -1, 0x0033D3FB, 0x0033D40C),
    _FixedSpec(-6, 22, 0, -1, 0x0033D456, 0x0033D467),
    _FixedSpec(-4, 16, 0, -1, 0x0033D4B1, 0x0033D4C2),
    _FixedSpec(-5, 17, 0, -1, 0x0033D50C, 0x0033D554),
    _FixedSpec(-7, 5, 0, 55, 0x0033D59E, 0x0033D5AF),
    _FixedSpec(-8, 1, 13, 1, 0x0033D64F, 0x0033D660),
)


def _transition(
    rng: IsaacRNG,
    transitions: list[LifecycleRNGTransition],
    *,
    rva: int,
    identity: str,
    reason: str,
) -> int:
    pre = rng.seed
    post = rng.next()
    transitions.append(LifecycleRNGTransition(rva, identity, pre, post, reason))
    return post


def _descriptor_seeds(
    rng: IsaacRNG,
    transitions: list[LifecycleRNGTransition],
    *,
    rva: int,
    identity: str,
    grid_index: int,
) -> tuple[int, int, int, int]:
    values = tuple(
        _transition(
            rng,
            transitions,
            rva=rva,
            identity=identity,
            reason=f"GridIndex {grid_index} descriptor seed {index}",
        )
        for index in range(3)
    )
    derived = IsaacRNG.game_constructor(
        values[-1], DESCRIPTOR_DERIVED_SHIFT_INDEX
    ).next()
    return values[0], values[1], values[2], derived


def _query(
    seed: int, room_type: int, stage: int, subtype: int
) -> RoomConfigQuery:
    return RoomConfigQuery(
        seed,
        True,
        stage,
        room_type,
        shape=13,
        min_variant=0,
        max_variant=0xFFFFFFFF,
        min_difficulty=0 if stage == 13 else 1,
        max_difficulty=0 if stage == 13 else 10,
        required_doors=0,
        subtype=subtype,
        mode=0,
    )


def _assign(
    *,
    spec: _FixedSpec,
    rng: IsaacRNG,
    rng_identity: str,
    transitions: list[LifecycleRNGTransition],
    entries: tuple[RoomConfigEntry, ...],
    weights: RoomConfigMutableState,
) -> FixedDescriptorAssignment:
    seeds = _descriptor_seeds(
        rng,
        transitions,
        rva=spec.helper_rva,
        identity=rng_identity,
        grid_index=spec.grid_index,
    )
    selector_seed = _transition(
        rng,
        transitions,
        rva=spec.selector_seed_rva,
        identity=rng_identity,
        reason=f"GridIndex {spec.grid_index} RoomConfig selector seed",
    )
    selection = select_room(
        entries, weights, _query(selector_seed, spec.room_type, spec.stage, spec.subtype)
    )
    return FixedDescriptorAssignment(
        spec.grid_index,
        spec.room_type,
        spec.subtype,
        seeds,
        selector_seed,
        None if selection.entry is None else selection.entry.key,
        selection,
    )


def _door_chance(
    *,
    player_collectible_count: int,
    used_bits: set[int],
    special_counter: int,
) -> float:
    value = f32(1.05 if player_collectible_count >= 20 else 1.0)
    if 30 in used_bits:
        used_bits.remove(30)
        value = f32(value + f32(0.1))
    if 31 in used_bits:
        used_bits.remove(31)
        value = f32(value + f32(0.02))
    penalty = f32(f32(float(min(special_counter, 5))) * f32(0.05))
    return f32(f32(value - penalty) * f32(1.0 / 3.0))


def run_post_layout_lifecycle(
    *,
    level_rng_state: int,
    entries: tuple[RoomConfigEntry, ...],
    room_config_weights: tuple[tuple[RoomConfigKey, float], ...],
    special_room_used_bits: tuple[int, ...] = (),
    level_stage: int = 1,
    stage_type: int = 0,
    room_config_stage: int = 1,
    collectible_ids: frozenset[int] = frozenset(),
    player_collectible_count: int = 0,
    special_counter: int = 0,
) -> PostLayoutLifecycleResult:
    """Replay RVA ``0x0033D1D6..0x0033D925`` for the canonical profile."""

    expected_rcs = 1 + (level_stage - 1) // 2 * 3
    if (
        level_stage not in (1, 2, 3, 4, 5, 6, 7, 8)
        or stage_type != 0
        or room_config_stage != expected_rcs
        or collectible_ids
        or player_collectible_count != 0
        or special_counter != 0
    ):
        raise ValueError("state is outside the canonical ORIGINAL lifecycle profile")

    level_rng = IsaacRNG.game_constructor(level_rng_state, LEVEL_SHIFT_INDEX)
    weights = RoomConfigMutableState(dict(room_config_weights))
    transitions: list[LifecycleRNGTransition] = []
    assignments: list[FixedDescriptorAssignment] = []
    used_bits = set(special_room_used_bits)

    # The two chance gates always consume Level RNG.  Their descriptor-flag
    # writes require stages above Basement II and are therefore impossible here.
    chance = _door_chance(
        player_collectible_count=player_collectible_count,
        used_bits=used_bits,
        special_counter=special_counter,
    )
    for rva, label in (
        (DOOR_CHANCE_FIRST_RVA, "first post-layout door chance"),
        (DOOR_CHANCE_SECOND_RVA, "second post-layout door chance"),
    ):
        state = _transition(
            level_rng,
            transitions,
            rva=rva,
            identity="Level._generationRNG(index=35)",
            reason=label,
        )
        # Keep the binary32 comparison explicit even though the stage gate is
        # false, so the recovered probability arithmetic remains testable.
        _ = f32(
            f32(float(state)) * f32(2.3283061589829401e-10)
        ) < chance

    for spec in _CANONICAL_FIXED_SPECS:
        assignments.append(
            _assign(
                spec=spec,
                rng=level_rng,
                rng_identity="Level._generationRNG(index=35)",
                transitions=transitions,
                entries=entries,
                weights=weights,
            )
        )

    # GridIndex -13 (Shop) uses one persistent Level draw to seed a private
    # index-19 stream. Canonical option/profile bounds are both one, but the
    # two RandomInt calls still advance that private stream.
    shop_seed = _transition(
        level_rng,
        transitions,
        rva=SHOP_PRIVATE_SEED_RVA,
        identity="Level._generationRNG(index=35)",
        reason="GridIndex -13 private Shop stream seed",
    )
    shop_rng = IsaacRNG.game_constructor(shop_seed, SHOP_PRIVATE_SHIFT_INDEX)
    shop_subtype = shop_rng.random_int(1) + shop_rng.random_int(1)
    assignments.append(
        _assign(
            spec=_FixedSpec(-13, 2, 0, shop_subtype, 0x0033D78B, 0x0033D7A0),
            rng=shop_rng,
            rng_identity="GridIndex -13 private RNG(index=19)",
            transitions=transitions,
            entries=entries,
            weights=weights,
        )
    )

    # GridIndex -18 (Angel) similarly owns a private index-20 stream, without
    # the two subtype draws made by the Shop stream.
    angel_seed = _transition(
        level_rng,
        transitions,
        rva=ANGEL_PRIVATE_SEED_RVA,
        identity="Level._generationRNG(index=35)",
        reason="GridIndex -18 private Angel stream seed",
    )
    angel_rng = IsaacRNG.game_constructor(angel_seed, ANGEL_PRIVATE_SHIFT_INDEX)
    assignments.append(
        _assign(
            spec=_FixedSpec(-18, 15, 0, 1, 0x0033D823, 0x0033D838),
            rng=angel_rng,
            rng_identity="GridIndex -18 private RNG(index=20)",
            transitions=transitions,
            entries=entries,
            weights=weights,
        )
    )

    persistent_draws = sum(
        item.identity == "Level._generationRNG(index=35)" for item in transitions
    )
    if persistent_draws != 28:
        raise AssertionError("canonical post-layout tail must make 28 Level draws")
    return PostLayoutLifecycleResult(
        True,
        tuple(assignments),
        tuple(transitions),
        persistent_draws,
        level_rng.seed,
        tuple(sorted(weights.weights.items())),
        tuple(sorted(used_bits)),
        0,
        (-9, -10),
    )
