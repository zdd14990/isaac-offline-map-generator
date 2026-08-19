"""Mechanical reference for the frozen late ordinary RoomConfig pass."""

from __future__ import annotations

from dataclasses import dataclass, replace

from .rng import IsaacRNG
from .room_config_reference import (
    RoomConfigEntryReference,
    RoomConfigKey,
    RoomConfigMutableStateReference,
    RoomConfigQueryReference,
    RoomConfigSelectionReference,
    select_room_reference,
)
from .special_rooms import GeneratedRoom


@dataclass(frozen=True)
class ReferenceLateAssignment:
    room_id: int
    grid_index: int
    required_doors: int
    minimum_difficulty: int
    maximum_difficulty: int
    config: RoomConfigKey | None
    fixed: bool
    selection: RoomConfigSelectionReference | None


@dataclass(frozen=True)
class ReferenceLateDefaultResult:
    completed: bool
    abort_room_id: int
    order: tuple[int, ...]
    assignments: tuple[ReferenceLateAssignment, ...]
    rooms: tuple[GeneratedRoom, ...]
    descriptors: tuple[tuple[int, RoomConfigKey], ...]
    transitions: tuple[tuple[int, int, int, str], ...]
    excluded_count: int
    final_level: int
    weights: tuple[tuple[RoomConfigKey, float], ...]


def _advance_level(rng: IsaacRNG) -> tuple[int, int]:
    before = rng.seed
    rng.next()
    return before, rng.seed


def assign_late_default_room_configs_reference(
    *,
    rooms: tuple[GeneratedRoom, ...],
    non_dead_ends: tuple[int, ...],
    dead_ends: tuple[int, ...],
    descriptor_configs: tuple[tuple[int, RoomConfigKey], ...],
    entries: tuple[RoomConfigEntryReference, ...],
    room_config_weights: tuple[tuple[RoomConfigKey, float], ...],
    level_rng_state: int,
    difficulty: str,
    room_config_stage: int = 1,
    level_stage: int = 1,
) -> ReferenceLateDefaultResult:
    if difficulty == "NORMAL":
        base_minimum, maximum = 1, 5
    elif difficulty == "HARD":
        base_minimum, maximum = 5, 10
    else:
        raise ValueError("difficulty must be NORMAL or HARD")

    order_list: list[int] = []
    for room_id in non_dead_ends:
        order_list.append(room_id)
    for room_id in dead_ends:
        order_list.append(room_id)
    order = tuple(order_list)
    if len(set(order)) != len(order):
        raise ValueError("reference late collection contains duplicates")

    mutable_rooms = [replace(room, neighbors=set(room.neighbors)) for room in rooms]
    descriptors = dict(descriptor_configs)
    weights = RoomConfigMutableStateReference(dict(room_config_weights))
    rng = IsaacRNG.game_constructor(level_rng_state, 35)
    transitions: list[tuple[int, int, int, str]] = []
    assignments: list[ReferenceLateAssignment] = []
    fixed = [
        entry
        for entry in entries
        if entry.key.stage == 0
        and entry.key.mode == 0
        and entry.room_type == 1
        and entry.variant == 2
    ]
    if len(fixed) != 1:
        raise AssertionError("reference start config lookup failed")

    for room_id in order:
        room = mutable_rooms[room_id]
        grid_index = room.line * 13 + room.column
        doors = room.doors & 0xFF
        if grid_index == 84:
            entry = fixed[0]
            room.room_type, room.variant, room.subtype = (
                entry.room_type,
                entry.variant,
                entry.subtype,
            )
            descriptors[room_id] = entry.key
            assignments.append(
                ReferenceLateAssignment(
                    room_id, grid_index, doors, base_minimum, maximum,
                    entry.key, True, None,
                )
            )
            continue

        minimum = 1 if base_minimum > 1 and rng.seed % 8 == 0 else base_minimum
        before, selector_seed = _advance_level(rng)
        transitions.append((before, selector_seed, room_id, "selector"))
        selection = select_room_reference(
            entries,
            weights,
            RoomConfigQueryReference(
                selector_seed,
                True,
                room_config_stage,
                1,
                shape=int(room.shape),
                min_variant=1 if level_stage == 11 else 0,
                max_variant=0xFFFFFFFF,
                min_difficulty=minimum,
                max_difficulty=maximum,
                required_doors=doors,
                subtype=0,
                mode=0,
            ),
        )
        entry = selection.selected
        assignments.append(
            ReferenceLateAssignment(
                room_id, grid_index, doors, minimum, maximum,
                None if entry is None else entry.key, False, selection,
            )
        )
        if entry is None:
            return ReferenceLateDefaultResult(
                False, room_id, order, tuple(assignments),
                tuple(replace(item, neighbors=set(item.neighbors)) for item in mutable_rooms),
                tuple(sorted(descriptors.items())), tuple(transitions), 0,
                rng.seed, tuple(sorted(weights.weights.items())),
            )
        room.room_type, room.variant, room.subtype = (
            entry.room_type,
            entry.variant,
            entry.subtype,
        )
        descriptors[room_id] = entry.key

    excluded = len(mutable_rooms) - len(order)
    for _ in range(excluded):
        before, after = _advance_level(rng)
        transitions.append((before, after, -1, "excluded"))
    return ReferenceLateDefaultResult(
        True, -1, order, tuple(assignments),
        tuple(replace(item, neighbors=set(item.neighbors)) for item in mutable_rooms),
        tuple(sorted(descriptors.items())), tuple(transitions), excluded,
        rng.seed, tuple(sorted(weights.weights.items())),
    )
