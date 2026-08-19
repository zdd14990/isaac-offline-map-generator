"""Readable exact port of the profiled RoomConfig special-room selector."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Callable, Iterable

from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config_reference import (
    EXACT_DOOR_MULTIPLIER,
    MINIMUM_WEIGHT,
    ROOM_CONFIG_DRAW_RVA,
    ROOM_CONFIG_SHIFT_INDEX,
    WEIGHT_DECAY,
    f32,
    room_definition_door_mask,
)


@dataclass(frozen=True, order=True)
class RoomConfigKey:
    stage: int
    mode: int
    resource_index: int


@dataclass(frozen=True)
class RoomConfigEntry:
    key: RoomConfigKey
    room_type: int
    variant: int
    subtype: int
    difficulty: int
    shape: int
    initial_weight: float
    door_mask: int
    unlock_gated: bool = False


@dataclass(frozen=True)
class RoomConfigQuery:
    seed: int
    reduce_weight: bool
    stage: int
    room_type: int
    shape: int = 0x0D
    min_variant: int = 0
    max_variant: int = 0xFFFFFFFF
    min_difficulty: int = 1
    max_difficulty: int = 10
    required_doors: int = 0
    subtype: int = -1
    mode: int = 0


@dataclass(frozen=True)
class RoomConfigDraw:
    binary_rva: int
    pre_state: int
    post_state: int
    reason: str
    result_float: float


@dataclass(frozen=True)
class RoomConfigSelection:
    candidate_keys: tuple[RoomConfigKey, ...]
    exact_door_keys: tuple[RoomConfigKey, ...]
    used_exact_doors: bool
    entry: RoomConfigEntry | None
    old_weight: float | None
    new_weight: float | None
    draws: tuple[RoomConfigDraw, ...]


@dataclass
class RoomConfigMutableState:
    weights: dict[RoomConfigKey, float] = field(default_factory=dict)

    def reset(self, entries: Iterable[RoomConfigEntry]) -> None:
        for entry in entries:
            self.weights[entry.key] = f32(entry.initial_weight)

    def weight(self, entry: RoomConfigEntry) -> float:
        return self.weights.get(entry.key, f32(entry.initial_weight))


def entries_from_definitions(
    definitions: Iterable[RoomDefinition], *, stage: int, mode: int = 0
) -> tuple[RoomConfigEntry, ...]:
    return tuple(
        RoomConfigEntry(
            RoomConfigKey(stage, mode, index), room.room_type, room.variant,
            room.subtype, room.difficulty, room.shape, f32(room.weight),
            room_definition_door_mask(room),
        )
        for index, room in enumerate(definitions)
    )


def _sum_weights(entries: Iterable[RoomConfigEntry], state: RoomConfigMutableState) -> float:
    total = f32(0.0)
    for entry in entries:
        total = f32(total + state.weight(entry))
    return total


def select_room(
    entries: Iterable[RoomConfigEntry],
    state: RoomConfigMutableState,
    query: RoomConfigQuery,
    *,
    unlock_predicate: Callable[[RoomConfigEntry], bool] | None = None,
) -> RoomConfigSelection:
    if unlock_predicate is None:
        unlock_predicate = lambda entry: not entry.unlock_gated
    candidates = tuple(
        entry for entry in entries
        if entry.key.stage == query.stage
        and entry.key.mode == query.mode
        and entry.room_type == query.room_type
        and (query.shape == 0x0D or entry.shape == query.shape)
        and query.min_variant <= entry.variant <= query.max_variant
        and query.min_difficulty <= entry.difficulty <= query.max_difficulty
        and query.required_doors & entry.door_mask == query.required_doors
        and (query.subtype == -1 or entry.subtype == query.subtype)
        and unlock_predicate(entry)
    )
    exact = tuple(
        entry for entry in candidates if entry.door_mask == query.required_doors
    ) if query.required_doors else ()
    total = _sum_weights(candidates, state)
    if not candidates or not total > 0.0:
        return RoomConfigSelection(tuple(e.key for e in candidates), tuple(e.key for e in exact), False, None, None, None, ())

    rng = IsaacRNG.game_constructor(query.seed, ROOM_CONFIG_SHIFT_INDEX)
    pre = rng.seed
    first_unit = rng.random_float()
    draws = [RoomConfigDraw(ROOM_CONFIG_DRAW_RVA, pre, rng.seed, "weighted selection threshold", first_unit)]
    chosen = candidates
    chosen_total = total
    used_exact = False
    if exact:
        exact_total = _sum_weights(exact, state)
        gate = f32(f32(exact_total / total) * EXACT_DOOR_MULTIPLIER)
        pre = rng.seed
        second_unit = rng.random_float()
        draws.append(RoomConfigDraw(ROOM_CONFIG_DRAW_RVA, pre, rng.seed, "exact-door subset gate", second_unit))
        if second_unit < gate:
            chosen, chosen_total, used_exact = exact, exact_total, True

    threshold = f32(first_unit * chosen_total)
    cumulative = f32(0.0)
    selected = None
    for entry in chosen:
        cumulative = f32(cumulative + state.weight(entry))
        if threshold < cumulative:
            selected = entry
            break
    if selected is None:
        return RoomConfigSelection(tuple(e.key for e in candidates), tuple(e.key for e in exact), used_exact, None, None, None, tuple(draws))

    old = state.weight(selected)
    new = old
    if query.reduce_weight:
        new = max(f32(old * WEIGHT_DECAY), MINIMUM_WEIGHT)
        state.weights[selected.key] = new
    return RoomConfigSelection(tuple(e.key for e in candidates), tuple(e.key for e in exact), used_exact, selected, old, new, tuple(draws))


def select_room_with_stage_fallback(
    entries: Iterable[RoomConfigEntry],
    state: RoomConfigMutableState,
    query: RoomConfigQuery,
    fallback_stage: int,
    *,
    unlock_predicate: Callable[[RoomConfigEntry], bool] | None = None,
) -> tuple[RoomConfigSelection, ...]:
    first = select_room(entries, state, query, unlock_predicate=unlock_predicate)
    if first.entry is not None:
        return (first,)
    second = select_room(entries, state, replace(query, stage=fallback_stage), unlock_predicate=unlock_predicate)
    return first, second
