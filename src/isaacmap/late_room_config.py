"""Clean late ordinary RoomConfig pass for the frozen Basement I profile.

This is the post-Ultra leaf at caller RVA ``0x0033CB5D..0x0033CF06``.
It deliberately does not own the outer retry transaction; a false result is
handed back to that caller so the complete pipeline can retry the whole floor.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from .rng import IsaacRNG
from .room_config import (
    RoomConfigEntry,
    RoomConfigKey,
    RoomConfigMutableState,
    RoomConfigQuery,
    RoomConfigSelection,
    select_room,
)
from .special_rooms import GeneratedRoom


LEVEL_SHIFT_INDEX = 35
LATE_SELECTOR_SEED_RVA = 0x0033CCA5
LATE_SELECTOR_CALL_RVA = 0x0033CCDE
LATE_ASSIGN_RVA = 0x0033CD07
LATE_EXCLUDED_ADVANCE_RVA = 0x0033CDD2
LATE_FAILURE_RVA = 0x0033CF06
START_GRID_INDEX = 84
START_VARIANT = 2


@dataclass(frozen=True)
class LateLevelRNGTransition:
    binary_rva: int
    pre_state: int
    post_state: int
    room_id: int
    reason: str


@dataclass(frozen=True)
class LateRoomAssignment:
    room_id: int
    grid_index: int
    required_doors: int
    minimum_difficulty: int
    maximum_difficulty: int
    config: RoomConfigKey | None
    fixed_start_config: bool
    selection: RoomConfigSelection | None


@dataclass(frozen=True)
class LateDefaultPassResult:
    completed: bool
    abort_room_id: int
    abort_rva: int | None
    collection_order: tuple[int, ...]
    assignments: tuple[LateRoomAssignment, ...]
    rooms: tuple[GeneratedRoom, ...]
    descriptor_configs: tuple[tuple[int, RoomConfigKey], ...]
    level_rng_transitions: tuple[LateLevelRNGTransition, ...]
    excluded_room_advance_count: int
    final_level_rng_state: int
    final_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]


def difficulty_window(difficulty: str) -> tuple[int, int]:
    value = str(difficulty).upper()
    if value == "NORMAL":
        return 1, 5
    if value == "HARD":
        return 5, 10
    raise ValueError("difficulty must be NORMAL or HARD")


def collect_late_default_rooms(
    non_dead_ends: tuple[int, ...], dead_ends: tuple[int, ...]
) -> tuple[int, ...]:
    """Port ``LevelGenerator::collect_rooms`` at RVA ``0x005AF0E0``."""

    order = tuple(non_dead_ends) + tuple(dead_ends)
    if len(set(order)) != len(order):
        raise ValueError("late ordinary collection contains duplicate room ids")
    return order


def _fixed_start_entry(entries: tuple[RoomConfigEntry, ...]) -> RoomConfigEntry:
    matches = tuple(
        entry
        for entry in entries
        if entry.key.stage == 0
        and entry.key.mode == 0
        and entry.room_type == 1
        and entry.variant == START_VARIANT
    )
    if len(matches) != 1:
        raise AssertionError("frozen special rooms must contain one start variant 2")
    return matches[0]


def _snapshot_rooms(rooms: list[GeneratedRoom]) -> tuple[GeneratedRoom, ...]:
    return tuple(replace(room, neighbors=set(room.neighbors)) for room in rooms)


def assign_late_default_room_configs(
    *,
    rooms: tuple[GeneratedRoom, ...],
    non_dead_ends: tuple[int, ...],
    dead_ends: tuple[int, ...],
    descriptor_configs: tuple[tuple[int, RoomConfigKey], ...],
    entries: tuple[RoomConfigEntry, ...],
    room_config_weights: tuple[tuple[RoomConfigKey, float], ...],
    level_rng_state: int,
    difficulty: str,
    room_config_stage: int = 1,
    level_stage: int = 1,
) -> LateDefaultPassResult:
    """Assign concrete configs to the final unconfigured ordinary rooms."""

    base_minimum, maximum = difficulty_window(difficulty)
    order = collect_late_default_rooms(non_dead_ends, dead_ends)
    if any(room_id < 0 or room_id >= len(rooms) for room_id in order):
        raise ValueError("late ordinary collection contains an invalid room id")

    mutable_rooms = [replace(room, neighbors=set(room.neighbors)) for room in rooms]
    weights = RoomConfigMutableState(dict(room_config_weights))
    descriptors = dict(descriptor_configs)
    level_rng = IsaacRNG.game_constructor(level_rng_state, LEVEL_SHIFT_INDEX)
    assignments: list[LateRoomAssignment] = []
    transitions: list[LateLevelRNGTransition] = []
    start_entry = _fixed_start_entry(entries)

    for room_id in order:
        room = mutable_rooms[room_id]
        grid_index = room.line * 13 + room.column
        required_doors = room.doors & 0xFF
        if grid_index == START_GRID_INDEX:
            room.room_type = start_entry.room_type
            room.variant = start_entry.variant
            room.subtype = start_entry.subtype
            descriptors[room_id] = start_entry.key
            assignments.append(
                LateRoomAssignment(
                    room_id,
                    grid_index,
                    required_doors,
                    base_minimum,
                    maximum,
                    start_entry.key,
                    True,
                    None,
                )
            )
            continue

        # The binary tests the current Level RNG state before advancing it.
        minimum = (
            1
            if base_minimum > 1 and level_rng.seed & 7 == 0
            else base_minimum
        )
        pre = level_rng.seed
        selector_seed = level_rng.next()
        transitions.append(
            LateLevelRNGTransition(
                LATE_SELECTOR_SEED_RVA,
                pre,
                selector_seed,
                room_id,
                "late ROOM_DEFAULT selector seed",
            )
        )
        selection = select_room(
            entries,
            weights,
            RoomConfigQuery(
                selector_seed,
                True,
                room_config_stage,
                1,
                shape=int(room.shape),
                min_variant=1 if level_stage == 11 else 0,
                max_variant=0xFFFFFFFF,
                min_difficulty=minimum,
                max_difficulty=maximum,
                required_doors=required_doors,
                subtype=0,
                mode=0,
            ),
        )
        entry = selection.entry
        assignments.append(
            LateRoomAssignment(
                room_id,
                grid_index,
                required_doors,
                minimum,
                maximum,
                None if entry is None else entry.key,
                False,
                selection,
            )
        )
        if entry is None:
            return LateDefaultPassResult(
                False,
                room_id,
                LATE_FAILURE_RVA,
                order,
                tuple(assignments),
                _snapshot_rooms(mutable_rooms),
                tuple(sorted(descriptors.items())),
                tuple(transitions),
                0,
                level_rng.seed,
                tuple(sorted(weights.weights.items())),
            )

        room.room_type = entry.room_type
        room.variant = entry.variant
        room.subtype = entry.subtype
        descriptors[room_id] = entry.key

    # The caller advances Level RNG once for every GeneratedRoom excluded from
    # collect_rooms (already configured special rooms, plus Secret/Ultra).
    excluded_count = len(mutable_rooms) - len(order)
    if excluded_count < 0:
        raise AssertionError("late collection cannot exceed generated room count")
    for _ in range(excluded_count):
        pre = level_rng.seed
        post = level_rng.next()
        transitions.append(
            LateLevelRNGTransition(
                LATE_EXCLUDED_ADVANCE_RVA,
                pre,
                post,
                -1,
                "advance for GeneratedRoom excluded from ordinary collection",
            )
        )

    return LateDefaultPassResult(
        True,
        -1,
        None,
        order,
        tuple(assignments),
        _snapshot_rooms(mutable_rooms),
        tuple(sorted(descriptors.items())),
        tuple(transitions),
        excluded_count,
        level_rng.seed,
        tuple(sorted(weights.weights.items())),
    )
