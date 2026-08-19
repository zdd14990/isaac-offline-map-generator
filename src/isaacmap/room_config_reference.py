"""Mechanical RoomConfig selector for the frozen executable.

This module follows the control flow at RVA ``0x0042C7D0``.  It deliberately
keeps the two candidate vectors, their resource order, binary32 additions and
the optional second RNG draw visible.  It is research infrastructure and does
not make the public floor generator supported.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import struct
from typing import Callable, Iterable

from .resources import RoomDefinition


UINT32_MASK = 0xFFFFFFFF
ROOM_CONFIG_SHIFT_INDEX = 7
ROOM_CONFIG_SHIFTS = (1, 21, 20)
ROOM_CONFIG_SELECT_RVA = 0x0042C7D0
ROOM_CONFIG_DRAW_RVA = 0x0042CBDE
ROOM_CONFIG_WEIGHT_WRITE_RVA = 0x0042CD95


def f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


FLOAT_SCALE = struct.unpack("<f", struct.pack("<I", 0x2F7FFFFE))[0]
EXACT_DOOR_MULTIPLIER = f32(9.99)
WEIGHT_DECAY = f32(0.1)
MINIMUM_WEIGHT = f32(1.0e-7)


def _advance(state: int) -> int:
    if state == 0:
        raise ValueError("RoomConfig selector seed must be nonzero")
    state ^= state >> ROOM_CONFIG_SHIFTS[0]
    state ^= (state << ROOM_CONFIG_SHIFTS[1]) & UINT32_MASK
    state ^= state >> ROOM_CONFIG_SHIFTS[2]
    return state & UINT32_MASK


def _unit(state: int) -> float:
    return f32(f32(float(state & UINT32_MASK)) * FLOAT_SCALE)


def _door_coordinate_map(shape: int) -> dict[tuple[int, int], int]:
    # RoomConfig door coordinates are 13x7 room-interior coordinates.  L-room
    # internal edges therefore use 12/13 and 6/7 rather than the outer bounds.
    maps: dict[int, tuple[tuple[int, int], ...]] = {
        1: ((-1, 3), (6, -1), (13, 3), (6, 7)),
        2: ((-1, 3), (13, 3)),
        3: ((6, -1), (6, 7)),
        4: ((-1, 3), (6, -1), (13, 3), (6, 14), (-1, 10), (13, 10)),
        5: ((-1, 3), (6, -1), (13, 3), (6, 14), (-1, 10), (13, 10)),
        6: ((-1, 3), (6, -1), (26, 3), (6, 7), (19, -1), (19, 7)),
        7: ((-1, 3), (26, 3)),
        8: ((-1, 3), (6, -1), (26, 3), (6, 14), (-1, 10), (19, -1), (26, 10), (19, 14)),
        9: ((12, 3), (6, 6), (26, 3), (6, 14), (-1, 10), (19, -1), (26, 10), (19, 14)),
        10: ((-1, 3), (6, -1), (13, 3), (6, 14), (-1, 10), (19, 6), (26, 10), (19, 14)),
        11: ((-1, 3), (6, -1), (26, 3), (6, 7), (12, 10), (19, -1), (26, 10), (19, 14)),
        12: ((-1, 3), (6, -1), (26, 3), (6, 14), (-1, 10), (19, -1), (13, 10), (19, 7)),
    }
    slots = {
        1: (0, 1, 2, 3), 2: (0, 2), 3: (1, 3),
        4: (0, 1, 2, 3, 4, 6), 5: (0, 1, 2, 3, 4, 6),
        6: (0, 1, 2, 3, 5, 7), 7: (0, 2),
        8: tuple(range(8)), 9: tuple(range(8)), 10: tuple(range(8)),
        11: tuple(range(8)), 12: tuple(range(8)),
    }
    try:
        return dict(zip(maps[shape], slots[shape]))
    except KeyError as error:
        raise ValueError(f"unsupported RoomShape {shape}") from error


def room_definition_door_mask(room: RoomDefinition) -> int:
    coordinate_map = _door_coordinate_map(room.shape)
    mask = 0
    for door in room.doors:
        try:
            slot = coordinate_map[(door.stored_x, door.stored_y)]
        except KeyError as error:
            raise ValueError(
                f"unrecognized shape {room.shape} door coordinate "
                f"{(door.stored_x, door.stored_y)} in {room.name!r}"
            ) from error
        if door.exists:
            mask |= 1 << slot
    return mask


@dataclass(frozen=True, order=True)
class RoomConfigKey:
    stage: int
    mode: int
    resource_index: int


@dataclass(frozen=True)
class RoomConfigEntryReference:
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
class RoomConfigQueryReference:
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
class RoomConfigDrawReference:
    draw_index: int
    binary_rva: int
    object_identity: str
    pre_state: int
    post_state: int
    reason: str
    result_float: float


@dataclass(frozen=True)
class RoomConfigSelectionReference:
    query: RoomConfigQueryReference
    all_candidates: tuple[RoomConfigKey, ...]
    exact_door_candidates: tuple[RoomConfigKey, ...]
    selected_from_exact_doors: bool
    selected: RoomConfigEntryReference | None
    selected_old_weight: float | None
    selected_new_weight: float | None
    draws: tuple[RoomConfigDrawReference, ...]


@dataclass
class RoomConfigMutableStateReference:
    weights: dict[RoomConfigKey, float] = field(default_factory=dict)

    def reset_pool(self, entries: Iterable[RoomConfigEntryReference]) -> None:
        for entry in entries:
            self.weights[entry.key] = f32(entry.initial_weight)

    def get(self, entry: RoomConfigEntryReference) -> float:
        return self.weights.get(entry.key, f32(entry.initial_weight))


def entries_from_definitions_reference(
    definitions: Iterable[RoomDefinition], *, stage: int, mode: int = 0
) -> tuple[RoomConfigEntryReference, ...]:
    return tuple(
        RoomConfigEntryReference(
            key=RoomConfigKey(stage, mode, index),
            room_type=room.room_type,
            variant=room.variant,
            subtype=room.subtype,
            difficulty=room.difficulty,
            shape=room.shape,
            initial_weight=f32(room.weight),
            door_mask=room_definition_door_mask(room),
        )
        for index, room in enumerate(definitions)
    )


def select_room_reference(
    entries: Iterable[RoomConfigEntryReference],
    mutable: RoomConfigMutableStateReference,
    query: RoomConfigQueryReference,
    *,
    unlock_predicate: Callable[[RoomConfigEntryReference], bool] | None = None,
) -> RoomConfigSelectionReference:
    """Port the ordinary path of RVA 0x0042C7D0.

    Seed-effect rerouting at the function prologue is intentionally outside
    this leaf selector and must be rejected by the generation profile before
    entering it.
    """

    if not 0 <= query.seed <= UINT32_MASK or query.seed == 0:
        raise ValueError("seed must be a nonzero uint32")
    if unlock_predicate is None:
        unlock_predicate = lambda entry: not entry.unlock_gated

    candidates: list[RoomConfigEntryReference] = []
    for entry in entries:
        if entry.key.stage != query.stage or entry.key.mode != query.mode:
            continue
        if entry.room_type != query.room_type:
            continue
        if query.shape != 0x0D and entry.shape != query.shape:
            continue
        if not query.min_variant <= entry.variant <= query.max_variant:
            continue
        if not query.min_difficulty <= entry.difficulty <= query.max_difficulty:
            continue
        if query.required_doors & entry.door_mask != query.required_doors:
            continue
        if query.subtype != -1 and entry.subtype != query.subtype:
            continue
        if not unlock_predicate(entry):
            continue
        candidates.append(entry)

    exact = (
        [entry for entry in candidates if entry.door_mask == query.required_doors]
        if query.required_doors != 0 else []
    )
    if not candidates:
        return RoomConfigSelectionReference(
            query, (), (), False, None, None, None, ()
        )

    total = f32(0.0)
    for entry in candidates:
        total = f32(total + mutable.get(entry))
    if not total > 0.0:
        return RoomConfigSelectionReference(
            query, tuple(e.key for e in candidates), tuple(e.key for e in exact),
            False, None, None, None, (),
        )

    draws: list[RoomConfigDrawReference] = []
    first_state = _advance(query.seed)
    first_unit = _unit(first_state)
    draws.append(RoomConfigDrawReference(
        0, ROOM_CONFIG_DRAW_RVA,
        f"RoomConfig::select_room.local(seed=0x{query.seed:08X})",
        query.seed, first_state, "weighted selection threshold", first_unit,
    ))

    chosen = candidates
    chosen_total = total
    from_exact = False
    if exact:
        exact_total = f32(0.0)
        for entry in exact:
            exact_total = f32(exact_total + mutable.get(entry))
        exact_probability = f32(f32(exact_total / total) * EXACT_DOOR_MULTIPLIER)
        second_state = _advance(first_state)
        second_unit = _unit(second_state)
        draws.append(RoomConfigDrawReference(
            1, ROOM_CONFIG_DRAW_RVA,
            f"RoomConfig::select_room.local(seed=0x{query.seed:08X})",
            first_state, second_state, "exact-door subset gate", second_unit,
        ))
        if second_unit < exact_probability:
            chosen = exact
            chosen_total = exact_total
            from_exact = True

    threshold = f32(first_unit * chosen_total)
    cumulative = f32(0.0)
    selected: RoomConfigEntryReference | None = None
    for entry in chosen:
        cumulative = f32(cumulative + mutable.get(entry))
        if threshold < cumulative:
            selected = entry
            break
    if selected is None:
        return RoomConfigSelectionReference(
            query, tuple(e.key for e in candidates), tuple(e.key for e in exact),
            from_exact, None, None, None, tuple(draws),
        )

    old = mutable.get(selected)
    new = old
    if query.reduce_weight:
        new = max(f32(old * WEIGHT_DECAY), MINIMUM_WEIGHT)
        mutable.weights[selected.key] = new
    return RoomConfigSelectionReference(
        query, tuple(e.key for e in candidates), tuple(e.key for e in exact),
        from_exact, selected, old, new, tuple(draws),
    )


def select_room_with_stage_fallback_reference(
    entries: Iterable[RoomConfigEntryReference],
    mutable: RoomConfigMutableStateReference,
    query: RoomConfigQueryReference,
    fallback_stage: int,
    *,
    unlock_predicate: Callable[[RoomConfigEntryReference], bool] | None = None,
) -> tuple[RoomConfigSelectionReference, ...]:
    first = select_room_reference(entries, mutable, query, unlock_predicate=unlock_predicate)
    if first.selected is not None:
        return (first,)
    fallback = RoomConfigQueryReference(**{
        **query.__dict__, "stage": fallback_stage,
    })
    return (
        first,
        select_room_reference(entries, mutable, fallback, unlock_predicate=unlock_predicate),
    )
