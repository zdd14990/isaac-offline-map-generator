"""Mechanical reference port of the profiled x86 ``LevelGenerator``.

This module deliberately mirrors the recovered branch and draw order.  It is
kept separate from :mod:`isaacmap.topology`, whose implementation is intended
to remain readable.  All RVAs refer to executable SHA-256
``3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .floor_init import Basement1TopologyInputs, Difficulty, derive_basement1_topology_inputs
from .topology import TopologyInputs


PROFILE_SHA256 = "3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b"
GRID_WIDTH = 13
GRID_HEIGHT = 13
INVALID_POSITION = (-1, -1)
GENERATOR_SHIFT_INDEX = 35
GENERATOR_SHIFTS = (5, 9, 7)
UINT32_MASK = 0xFFFFFFFF

# These copies are intentional.  The reference implementation must not share
# clean geometry helpers with topology.py, otherwise differential testing
# could not detect a common table/branch error.
_SHAPE_DIMENSIONS = (
    (0, 0),
    (1, 1), (1, 1), (1, 1),
    (1, 2), (1, 2),
    (2, 1), (2, 1),
    (2, 2), (2, 2), (2, 2), (2, 2), (2, 2),
)
_SHAPE_OFFSETS = (
    (),
    ((0, 0),),
    ((0, 0),),
    ((0, 0),),
    ((0, 0), (0, 1)),
    ((0, 0), (0, 1)),
    ((0, 0), (1, 0)),
    ((0, 0), (1, 0)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
    ((1, 0), (0, 1), (1, 1)),
    ((0, 0), (0, 1), (1, 1)),
    ((0, 0), (1, 0), (1, 1)),
    ((0, 0), (1, 0), (0, 1)),
)
_DIRECTIONS = ((-1, 0), (0, -1), (1, 0), (0, 1))
_LARGE_DIVISORS = (48, 24, 24, 24, 24, 72, 72, 36, 36, 36, 36, 24, 24)


@dataclass(frozen=True)
class RNGDraw:
    sequence: int
    binary_rva: int
    binary_range: str
    rng_object: str
    shift_index: int
    shifts: tuple[int, int, int]
    pre_state: int
    post_state: int
    control_flow_reason: str
    result_usage: str
    attempt: int = 0
    source_room: int = -1
    door_slot: int = -1
    candidate_index: int = -1


@dataclass(frozen=True)
class ReferenceEvent:
    kind: str
    rng_state: int
    attempt: int
    values: tuple[int, ...] = ()


@dataclass
class ReferenceRoom:
    column: int
    line: int
    shape: int
    generation_index: int = -1
    doors: int = 0
    origin_neighbor_connect_dir: int = -1
    origin_neighbor_door_slot: int = -1
    link_column: int = -1
    link_line: int = -1
    neighbors: set[int] = field(default_factory=set)
    dead_end: bool = False
    distance_from_start: int = 0

    @property
    def grid_index(self) -> int:
        return self.line * GRID_WIDTH + self.column

    @property
    def link_position(self) -> tuple[int, int]:
        return self.link_column, self.link_line

    @property
    def occupied_cells(self) -> tuple[tuple[int, int], ...]:
        return tuple(
            (self.column + dx, self.line + dy)
            for dx, dy in _SHAPE_OFFSETS[self.shape]
        )


@dataclass(frozen=True)
class ReferenceAttempt:
    attempt: int
    target_room_count: int
    expansion_order: tuple[int, ...]
    dead_end_order: tuple[int, ...]
    forced_dead_end_attempts: int
    final_rng_state: int


@dataclass(frozen=True)
class ReferenceCoverage:
    boundary_skips: int
    large_draws: int
    large_random_failures: int
    large_random_successes: int
    large_candidates_appended: int
    large_rooms_placed: int
    forced_dead_end_attempts: int
    forced_dead_end_successes: int
    retry_count: int


@dataclass(frozen=True)
class TopologyReferenceResult:
    rooms: tuple[ReferenceRoom, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    non_dead_ends: tuple[int, ...]
    target_room_count: int
    retries: int
    expansion_order: tuple[int, ...]
    final_rng_state: int
    entry_rng_ledger: tuple[RNGDraw, ...]
    generator_rng_ledger: tuple[RNGDraw, ...]
    events: tuple[ReferenceEvent, ...]
    attempts: tuple[ReferenceAttempt, ...]
    coverage: ReferenceCoverage


class _LedgerRNG:
    def __init__(
        self,
        seed: int,
        *,
        object_name: str,
        shared_ledger: list[RNGDraw],
        shift_index: int = GENERATOR_SHIFT_INDEX,
        shifts: tuple[int, int, int] = GENERATOR_SHIFTS,
    ) -> None:
        self.seed = seed & UINT32_MASK
        self.object_name = object_name
        self.ledger = shared_ledger
        self.shift_index = shift_index
        self.shifts = shifts

    def copy(self, object_name: str) -> _LedgerRNG:
        return _LedgerRNG(
            self.seed,
            object_name=object_name,
            shared_ledger=self.ledger,
            shift_index=self.shift_index,
            shifts=self.shifts,
        )

    def draw(
        self,
        *,
        binary_rva: int,
        binary_range: str,
        reason: str,
        usage: str,
        attempt: int = 0,
        source_room: int = -1,
        door_slot: int = -1,
        candidate_index: int = -1,
    ) -> int:
        if self.seed == 0:
            raise ValueError("the profiled binary asserts before drawing a zero RNG state")
        pre = self.seed
        value = pre
        value ^= value >> self.shifts[0]
        value ^= (value << self.shifts[1]) & UINT32_MASK
        value ^= value >> self.shifts[2]
        self.seed = value & UINT32_MASK
        self.ledger.append(
            RNGDraw(
                sequence=len(self.ledger),
                binary_rva=binary_rva,
                binary_range=binary_range,
                rng_object=self.object_name,
                shift_index=self.shift_index,
                shifts=self.shifts,
                pre_state=pre,
                post_state=self.seed,
                control_flow_reason=reason,
                result_usage=usage,
                attempt=attempt,
                source_room=source_room,
                door_slot=door_slot,
                candidate_index=candidate_index,
            )
        )
        return self.seed


def _in_bounds(position: tuple[int, int]) -> bool:
    return 0 <= position[0] < GRID_WIDTH and 0 <= position[1] < GRID_HEIGHT


def _grid_index(position: tuple[int, int]) -> int:
    return position[1] * GRID_WIDTH + position[0] if _in_bounds(position) else -1


def _has_shape_slot(shape: int, slot: int, ignore_thin: bool = False) -> bool:
    width, height = _SHAPE_DIMENSIONS[shape]
    if height == 1 and slot in (4, 6):
        return False
    if width == 1 and slot in (5, 7):
        return False
    if not ignore_thin:
        if shape in (3, 5) and slot in (0, 2, 4, 6):
            return False
        if shape in (2, 7) and slot in (1, 3, 5, 7):
            return False
    return True


def _door_source(column: int, line: int, shape: int, slot: int) -> tuple[int, int]:
    if not _has_shape_slot(shape, slot):
        return INVALID_POSITION
    if shape in (1, 2, 3):
        offset = (0, 0)
    elif shape in (4, 5):
        offset = (0, 1) if slot in (3, 4, 6) else (0, 0)
    elif shape in (6, 7):
        offset = (1, 0) if slot in (2, 5, 7) else (0, 0)
    elif shape == 8:
        if slot in (2, 5):
            offset = (1, 0)
        elif slot in (3, 4):
            offset = (0, 1)
        elif slot in (6, 7):
            offset = (1, 1)
        else:
            offset = (0, 0)
    elif shape == 9:
        if slot in (0, 2, 5):
            offset = (1, 0)
        elif slot in (1, 3, 4):
            offset = (0, 1)
        else:
            offset = (1, 1)
    elif shape == 10:
        if slot in (0, 1, 2):
            offset = (0, 0)
        elif slot in (3, 4):
            offset = (0, 1)
        else:
            offset = (1, 1)
    elif shape == 11:
        if slot in (0, 1, 3):
            offset = (0, 0)
        elif slot in (2, 5):
            offset = (1, 0)
        else:
            offset = (1, 1)
    else:
        if slot in (0, 1):
            offset = (0, 0)
        elif slot in (2, 5, 7):
            offset = (1, 0)
        else:
            offset = (0, 1)
    return column + offset[0], line + offset[1]


def _door_target(
    column: int,
    line: int,
    shape: int,
    slot: int,
    ignore_thin: bool = False,
) -> tuple[int, int]:
    if not _has_shape_slot(shape, slot, ignore_thin):
        return INVALID_POSITION
    width, height = _SHAPE_DIMENSIONS[shape]
    table = (
        (column - 1, line),
        (column, line - 1),
        (column + width, line),
        (column, line + height),
        (column - 1, line + 1),
        (column + 1, line - 1),
        (column + width, line + 1),
        (column + 1, line + height),
    )
    if shape == 9:
        table = (
            (column, line), (column, line), (column + 2, line),
            (column, line + 2), (column - 1, line + 1),
            (column + 1, line - 1), (column + 2, line + 1),
            (column + 1, line + 2),
        )
    elif shape == 10:
        table = (
            (column - 1, line), (column, line - 1), (column + 1, line),
            (column, line + 2), (column - 1, line + 1),
            (column + 1, line), (column + 2, line + 1),
            (column + 1, line + 2),
        )
    elif shape == 11:
        table = (
            (column - 1, line), (column, line - 1), (column + 2, line),
            (column, line + 1), (column, line + 1),
            (column + 1, line - 1), (column + 2, line + 1),
            (column + 1, line + 2),
        )
    elif shape == 12:
        table = (
            (column - 1, line), (column, line - 1), (column + 2, line),
            (column, line + 2), (column - 1, line + 1),
            (column + 1, line - 1), (column + 1, line + 1),
            (column + 1, line + 1),
        )
    return table[slot]


def _large_templates(
    target: tuple[int, int], direction: int
) -> tuple[tuple[int, int, int, int], ...]:
    tx, ty = target
    if direction in (0, 1):
        dx, dy = _DIRECTIONS[direction]
    else:
        dx, dy = 0, 0
    base = (tx + dx, ty + dy)
    if direction in (0, 2):
        alternate = (base[0], base[1] - 1)
        third = (tx, ty - 1)
        first_shapes = (6, 4)
        narrow = (2, 7)
    else:
        alternate = (base[0] - 1, base[1])
        third = (tx - 1, ty)
        first_shapes = (4, 6)
        narrow = (3, 5)
    l_shapes = (
        (12, 10, 11, 9),
        (12, 11, 10, 9),
        (11, 9, 10, 12),
        (10, 9, 11, 12),
    )[direction]
    anchors = (
        base, target, third, base, alternate, base, alternate,
        base, alternate, base, alternate, target, base,
    )
    shapes = (
        first_shapes[0], first_shapes[1], first_shapes[1], 8, 8,
        l_shapes[0], l_shapes[1], l_shapes[2], l_shapes[2],
        l_shapes[3], l_shapes[3], narrow[0], narrow[1],
    )
    return tuple(
        (anchor[0], anchor[1], shape, divisor)
        for anchor, shape, divisor in zip(anchors, shapes, _LARGE_DIVISORS)
    )


class LevelGeneratorReference:
    """Control-flow-shaped port of RVAs 0x005ADBB0 and 0x005B04D0."""

    def __init__(self, seed: int, ledger: list[RNGDraw]) -> None:
        self.rng = _LedgerRNG(
            seed,
            object_name="LevelGenerator._rng",
            shared_ledger=ledger,
        )
        self.allowed_shapes = 0
        self.room_map = [-1] * 169
        self.blocked_positions = [False] * 169
        self.rooms: list[ReferenceRoom] = []
        self.dead_ends: list[int] = []
        self.non_dead_ends: list[int] = []
        self.is_xl = False
        self.is_chapter6 = False
        self.is_stage_void = False
        self.next_boss_room_index = -1
        self.num_boss_rooms = 0
        self.attempt = 0
        self.expansion_order: list[int] = []
        self.events: list[ReferenceEvent] = []
        self.boundary_skips = 0
        self.large_draws = 0
        self.large_random_failures = 0
        self.large_random_successes = 0
        self.large_candidates_appended = 0
        self.large_rooms_placed = 0
        self.forced_dead_end_attempts = 0
        self.forced_dead_end_successes = 0

    def _event(self, kind: str, *values: int) -> None:
        self.events.append(ReferenceEvent(kind, self.rng.seed, self.attempt, tuple(values)))

    def _shape_allowed(self, shape: int) -> bool:
        return bool(self.allowed_shapes & (1 << shape))

    def is_pos_free(self, position: tuple[int, int], shape: int) -> bool:
        forbidden = -1
        if self.rooms:
            forbidden = _grid_index((self.rooms[0].column, self.rooms[0].line - 1))
        for dx, dy in _SHAPE_OFFSETS[shape]:
            index = _grid_index((position[0] + dx, position[1] + dy))
            if index < 0:
                return False
            if self.is_chapter6 and index == forbidden:
                return False
            if self.room_map[index] >= 0:
                return False
            if self.blocked_positions[index]:
                return False
        return True

    def count_neighbor_links(self, position: tuple[int, int]) -> int:
        center_index = _grid_index(position)
        center_room = self.room_map[center_index] if center_index >= 0 else -1
        result = 0
        for dx, dy in _DIRECTIONS:
            neighbor_index = _grid_index((position[0] + dx, position[1] + dy))
            if neighbor_index < 0:
                continue
            neighbor_room = self.room_map[neighbor_index]
            if neighbor_room >= 0 and neighbor_room != center_room:
                result += 1
        return result

    def is_placement_valid(self, room: ReferenceRoom) -> bool:
        slot = 0
        while slot < 8:
            source = _door_source(room.column, room.line, room.shape, slot)
            target = _door_target(room.column, room.line, room.shape, slot, True)
            target_index = _grid_index(target)
            if target_index >= 0:
                neighbor_id = self.room_map[target_index]
                if neighbor_id >= 0:
                    if source == INVALID_POSITION:
                        return False
                    neighbor = self.rooms[neighbor_id]
                    return_slot = 0
                    while return_slot < 8:
                        if _door_target(
                            neighbor.column, neighbor.line, neighbor.shape, return_slot
                        ) == source:
                            break
                        return_slot += 1
                    if return_slot > 7:
                        return False
            slot += 1
        return True

    def place_room(self, room: ReferenceRoom) -> ReferenceRoom:
        placed = ReferenceRoom(
            column=room.column,
            line=room.line,
            shape=room.shape,
            generation_index=len(self.rooms),
            doors=room.doors,
            origin_neighbor_connect_dir=room.origin_neighbor_connect_dir,
            origin_neighbor_door_slot=room.origin_neighbor_door_slot,
            link_column=room.link_column,
            link_line=room.link_line,
            neighbors=set(room.neighbors),
            dead_end=room.dead_end,
            distance_from_start=room.distance_from_start,
        )
        self.rooms.append(placed)
        for cell in placed.occupied_cells:
            index = _grid_index(cell)
            if index < 0:
                raise AssertionError("binary place_room precondition violated")
            self.room_map[index] = placed.generation_index
        if placed.shape != 1:
            self.large_rooms_placed += 1
        self._event("room_placed", placed.generation_index, placed.grid_index, placed.shape)
        return placed

    @staticmethod
    def _candidate(
        column: int,
        line: int,
        shape: int,
        source: ReferenceRoom,
        slot: int,
        target: tuple[int, int],
    ) -> ReferenceRoom:
        return ReferenceRoom(
            column=column,
            line=line,
            shape=shape,
            origin_neighbor_connect_dir=slot & 3,
            origin_neighbor_door_slot=slot,
            link_column=target[0],
            link_line=target[1],
            distance_from_start=source.distance_from_start + 1,
        )

    def get_neighbor_candidates(
        self, generation_index: int, force_all_large: bool
    ) -> list[ReferenceRoom]:
        source = self.rooms[generation_index]
        result: list[ReferenceRoom] = []
        shape1_allowed = self._shape_allowed(1)
        slot = 0
        while slot < 8:
            target = _door_target(source.column, source.line, source.shape, slot)
            if not _in_bounds(target):
                self.boundary_skips += 1
                slot += 1
                continue
            if not self.is_pos_free(target, 1):
                slot += 1
                continue
            if shape1_allowed:
                result.append(
                    self._candidate(target[0], target[1], 1, source, slot, target)
                )
            template_index = 0
            templates = _large_templates(target, slot & 3)
            while template_index < 13:
                column, line, shape, divisor = templates[template_index]
                draw = self.rng.draw(
                    binary_rva=0x005B1030,
                    binary_range="0x005B1030..0x005B104B",
                    reason=(
                        "forced-dead-end candidate gate (draw retained despite override)"
                        if force_all_large
                        else "ordinary large-room candidate gate"
                    ),
                    usage=f"candidate[{template_index}] modulo {divisor}",
                    attempt=self.attempt,
                    source_room=generation_index,
                    door_slot=slot,
                    candidate_index=template_index,
                )
                self.large_draws += 1
                random_success = draw % divisor == 0
                if random_success:
                    self.large_random_successes += 1
                else:
                    self.large_random_failures += 1
                gate = random_success or not shape1_allowed or force_all_large
                if gate and self._shape_allowed(shape) and self.is_pos_free((column, line), shape):
                    result.append(
                        self._candidate(column, line, shape, source, slot, target)
                    )
                    self.large_candidates_appended += 1
                template_index += 1
            slot += 1
        self._event("candidate_list", generation_index, len(result), int(force_all_large))
        return result

    def shuffle_candidates(self, candidates: list[ReferenceRoom], source_index: int) -> None:
        current_size = len(candidates)
        while 1 < current_size:
            draw = self.rng.draw(
                binary_rva=0x005B1B8F,
                binary_range="0x005B1B8F..0x005B1BAA",
                reason="Fisher-Yates candidate shuffle",
                usage=f"swap index {current_size - 1} with Next() % {current_size}",
                attempt=self.attempt,
                source_room=source_index,
            )
            other = draw % current_size
            current = current_size - 1
            candidates[current], candidates[other] = candidates[other], candidates[current]
            current_size -= 1

    def generate_rooms(self, target_count: int, start_room: ReferenceRoom) -> None:
        start = self.place_room(start_room)
        queue = [start.generation_index]
        placed_count = 0
        while queue and placed_count < target_count:
            source_index = queue.pop(0)
            self.expansion_order.append(source_index)
            self._event("source_pop", source_index, len(queue), placed_count)
            candidates = self.get_neighbor_candidates(source_index, False)
            self.shuffle_candidates(candidates, source_index)
            if source_index == start.generation_index:
                if target_count < 16:
                    draw = self.rng.draw(
                        binary_rva=0x005B05F0,
                        binary_range="0x005B05F0..0x005B060E",
                        reason="starting-room fanout",
                        usage="wanted = 2 + (Next() & 1)",
                        attempt=self.attempt,
                        source_room=source_index,
                    )
                    wanted = 2 + (draw & 1)
                else:
                    wanted = len(candidates)
            else:
                draw0 = self.rng.draw(
                    binary_rva=0x005B063A,
                    binary_range="0x005B063A..0x005B0657",
                    reason="non-start room fanout draw 1/4",
                    usage="low bit contributes to wanted child count",
                    attempt=self.attempt,
                    source_room=source_index,
                )
                draw1 = self.rng.draw(
                    binary_rva=0x005B0679,
                    binary_range="0x005B0679..0x005B0696",
                    reason="non-start room fanout draw 2/4",
                    usage="low bit contributes to wanted child count",
                    attempt=self.attempt,
                    source_room=source_index,
                )
                draw2 = self.rng.draw(
                    binary_rva=0x005B06B8,
                    binary_range="0x005B06B8..0x005B06D5",
                    reason="non-start room fanout draw 3/4",
                    usage="low bit contributes to wanted child count",
                    attempt=self.attempt,
                    source_room=source_index,
                )
                draw3 = self.rng.draw(
                    binary_rva=0x005B06F4,
                    binary_range="0x005B06F4..0x005B0715",
                    reason="non-start room fanout draw 4/4",
                    usage="low bit contributes to wanted child count",
                    attempt=self.attempt,
                    source_room=source_index,
                )
                wanted = min(
                    len(candidates),
                    (draw0 & 1) + (draw1 & 1) + (draw2 & 1) + (draw3 & 1),
                )
            self._event("wanted_children", source_index, wanted, len(candidates))
            placed_from_source = 0
            candidate_index = 0
            while candidate_index < len(candidates):
                candidate = candidates[candidate_index]
                if self.is_pos_free((candidate.column, candidate.line), candidate.shape):
                    links = self.count_neighbor_links(candidate.link_position)
                    accept_links = links < 2
                    if not accept_links and (self.is_xl or self.is_stage_void):
                        draw = self.rng.draw(
                            binary_rva=0x005B07AA,
                            binary_range="0x005B07AA..0x005B07CC",
                            reason="XL/Void multi-neighbor exception",
                            usage="candidate accepted only when Next() % 10 == 0",
                            attempt=self.attempt,
                            source_room=source_index,
                            candidate_index=candidate_index,
                        )
                        accept_links = draw % 10 == 0
                    if accept_links and self.is_placement_valid(candidate):
                        placed = self.place_room(candidate)
                        draw = self.rng.draw(
                            binary_rva=0x005B0815,
                            binary_range="0x005B0815..0x005B0837",
                            reason="new expansion queue insertion side",
                            usage="push_back when Next() % 3 == 0, otherwise push_front",
                            attempt=self.attempt,
                            source_room=source_index,
                            candidate_index=candidate_index,
                        )
                        if draw % 3 == 0:
                            queue.append(placed.generation_index)
                        else:
                            queue.insert(0, placed.generation_index)
                        placed_count += 1
                        placed_from_source += 1
                        if placed_from_source >= wanted or placed_count >= target_count:
                            break
                candidate_index += 1

    def update_room_connections(self, room: ReferenceRoom) -> None:
        room.doors = 0
        room.neighbors.clear()
        slot = 0
        while slot < 8:
            target = _door_target(room.column, room.line, room.shape, slot)
            index = _grid_index(target)
            if index >= 0:
                neighbor = self.room_map[index]
                if neighbor >= 0:
                    room.doors |= 1 << slot
                    room.neighbors.add(neighbor)
            slot += 1

    def mark_dead_ends(self) -> None:
        room_index = 1
        while room_index < len(self.rooms):
            room = self.rooms[room_index]
            if self.count_neighbor_links(room.link_position) < 2:
                room.dead_end = True
            room_index += 1
        room_index = 1
        while room_index < len(self.rooms):
            room = self.rooms[room_index]
            if room.link_position != INVALID_POSITION:
                direction = (room.origin_neighbor_connect_dir + 2) & 3
                dx, dy = _DIRECTIONS[direction]
                parent_position = (room.link_column + dx, room.link_line + dy)
                parent_index = _grid_index(parent_position)
                parent_id = self.room_map[parent_index] if parent_index >= 0 else -1
                if parent_id < 0:
                    raise AssertionError("binary invalid-connecting-neighbor path reached")
                self.rooms[parent_id].dead_end = False
            room_index += 1

    def classify_dead_ends(self) -> None:
        self.dead_ends.clear()
        self.non_dead_ends.clear()
        self.mark_dead_ends()
        room_index = 0
        while room_index < len(self.rooms):
            room = self.rooms[room_index]
            self.update_room_connections(room)
            if room.dead_end:
                self.dead_ends.append(room_index)
            else:
                self.non_dead_ends.append(room_index)
            room_index += 1
        self._event("classify", *self.dead_ends)

    def force_new_dead_end(self) -> bool:
        self.forced_dead_end_attempts += 1
        room_index = 0
        while room_index < len(self.rooms):
            candidates = self.get_neighbor_candidates(room_index, True)
            candidate_index = 0
            while candidate_index < len(candidates):
                candidate = candidates[candidate_index]
                if self.is_pos_free((candidate.column, candidate.line), candidate.shape):
                    if self.count_neighbor_links(candidate.link_position) < 2:
                        self.place_room(candidate)
                        self.forced_dead_end_successes += 1
                        self._event("force_success", room_index, candidate_index)
                        return True
                candidate_index += 1
            room_index += 1
        self._event("force_failure")
        return False

    def generate_once(
        self,
        target_count: int,
        required_dead_ends: int,
        allowed_shapes: int,
        start_room: ReferenceRoom,
    ) -> int:
        self.allowed_shapes = allowed_shapes
        self.room_map[:] = [-1] * 169
        self.rooms.clear()
        self.dead_ends.clear()
        self.non_dead_ends.clear()
        self.expansion_order.clear()
        self.next_boss_room_index = -1
        self.num_boss_rooms = 0
        forced_before = self.forced_dead_end_attempts
        self.generate_rooms(target_count, start_room)
        self.classify_dead_ends()
        remaining = 5
        while len(self.dead_ends) < required_dead_ends and remaining > 0:
            self.force_new_dead_end()
            self.classify_dead_ends()
            remaining -= 1
        # RVA 0x005ADCA9..0x005ADD20 selection-sorts descending distance.
        position = 0
        while position < len(self.dead_ends):
            best_position = position
            scan = position + 1
            while scan < len(self.dead_ends):
                if (
                    self.rooms[self.dead_ends[best_position]].distance_from_start
                    < self.rooms[self.dead_ends[scan]].distance_from_start
                ):
                    best_position = scan
                scan += 1
            self.dead_ends[position], self.dead_ends[best_position] = (
                self.dead_ends[best_position],
                self.dead_ends[position],
            )
            position += 1
        return self.forced_dead_end_attempts - forced_before


def _build_basement1_entry_ledger(
    inputs: Basement1TopologyInputs,
) -> tuple[list[RNGDraw], int]:
    ledger: list[RNGDraw] = []
    level_rng = _LedgerRNG(
        inputs.stage_seed,
        object_name="Level._generationRNG",
        shared_ledger=ledger,
    )
    level_rng.draw(
        binary_rva=0x00344C1E,
        binary_range="0x00344C1E..0x00344C42",
        reason="Level::Init first generation-RNG advance",
        usage="early Level::Init state progression",
    )
    level_rng.draw(
        binary_rva=0x00344CAA,
        binary_range="0x00344CAA..0x00344CCE",
        reason="Level::Init second generation-RNG advance",
        usage="state copied into the stack RNG after this draw",
    )
    copied_rng = level_rng.copy("Level::generate_dungeon.stack_rng_copy")
    level_rng.draw(
        binary_rva=0x00340E8E,
        binary_range="0x00340E8E..0x00340EB8",
        reason="ordinary dungeon base room-count draw",
        usage="target base low bit",
    )
    copied_rng.draw(
        binary_rva=0x0034109F,
        binary_range="0x0034109F..0x003410C0",
        reason="difficulty bonus draw from copied stack RNG",
        usage="HARD adds 2 + (Next() & 1); NORMAL discards value",
    )
    generator_seed = level_rng.draw(
        binary_rva=0x00341202,
        binary_range="0x00341202..0x0034122D",
        reason="LevelGenerator constructor seed draw",
        usage="seed passed to LevelGenerator constructor with shift index 35",
    )
    if generator_seed != inputs.generator_seed:
        raise AssertionError("confirmed floor-init and reference entry streams disagree")
    return ledger, generator_seed


def generate_topology_reference(
    inputs: TopologyInputs,
    *,
    entry_rng_ledger: tuple[RNGDraw, ...] = (),
) -> TopologyReferenceResult:
    """Run the mechanical topology reference for a verified floor entry."""

    generator_seed = inputs.generator_seed
    generator_ledger: list[RNGDraw] = []
    generator = LevelGeneratorReference(generator_seed, generator_ledger)
    generator.is_xl = bool(getattr(inputs, "is_xl", False))
    target_count = inputs.target_room_count
    retries = 0
    attempts: list[ReferenceAttempt] = []
    while True:
        generator.attempt += 1
        generator.blocked_positions[:] = [False] * 169
        forced = generator.generate_once(
            target_count,
            inputs.required_dead_ends,
            inputs.allowed_shapes_mask,
            ReferenceRoom(6, 6, 1),
        )
        attempts.append(
            ReferenceAttempt(
                attempt=generator.attempt,
                target_room_count=target_count,
                expansion_order=tuple(generator.expansion_order),
                dead_end_order=tuple(generator.dead_ends),
                forced_dead_end_attempts=forced,
                final_rng_state=generator.rng.seed,
            )
        )
        if len(generator.dead_ends) >= inputs.required_dead_ends:
            break
        retries += 1
        if generator.attempt >= 10 and generator.attempt % 5 == 0 and target_count < 64:
            target_count += 1

    rooms = tuple(
        ReferenceRoom(
            column=room.column,
            line=room.line,
            shape=room.shape,
            generation_index=room.generation_index,
            doors=room.doors,
            origin_neighbor_connect_dir=room.origin_neighbor_connect_dir,
            origin_neighbor_door_slot=room.origin_neighbor_door_slot,
            link_column=room.link_column,
            link_line=room.link_line,
            neighbors=set(room.neighbors),
            dead_end=room.dead_end,
            distance_from_start=room.distance_from_start,
        )
        for room in generator.rooms
    )
    return TopologyReferenceResult(
        rooms=rooms,
        room_map=tuple(generator.room_map),
        dead_ends=tuple(generator.dead_ends),
        non_dead_ends=tuple(generator.non_dead_ends),
        target_room_count=target_count,
        retries=retries,
        expansion_order=tuple(generator.expansion_order),
        final_rng_state=generator.rng.seed,
        entry_rng_ledger=entry_rng_ledger,
        generator_rng_ledger=tuple(generator_ledger),
        events=tuple(generator.events),
        attempts=tuple(attempts),
        coverage=ReferenceCoverage(
            boundary_skips=generator.boundary_skips,
            large_draws=generator.large_draws,
            large_random_failures=generator.large_random_failures,
            large_random_successes=generator.large_random_successes,
            large_candidates_appended=generator.large_candidates_appended,
            large_rooms_placed=generator.large_rooms_placed,
            forced_dead_end_attempts=generator.forced_dead_end_attempts,
            forced_dead_end_successes=generator.forced_dead_end_successes,
            retry_count=retries,
        ),
    )


def generate_basement1_topology_reference(
    inputs: Basement1TopologyInputs,
) -> TopologyReferenceResult:
    """Compatibility wrapper for the frozen ordinary Basement I scope."""

    entry_ledger, generator_seed = _build_basement1_entry_ledger(inputs)
    if generator_seed != inputs.generator_seed:
        raise AssertionError("Basement I entry ledger disagrees with generator seed")
    return generate_topology_reference(inputs, entry_rng_ledger=tuple(entry_ledger))


def derive_and_generate_basement1_topology_reference(
    start_seed: int,
    difficulty: Difficulty | str,
) -> TopologyReferenceResult:
    return generate_basement1_topology_reference(
        derive_basement1_topology_inputs(start_seed, difficulty)
    )
