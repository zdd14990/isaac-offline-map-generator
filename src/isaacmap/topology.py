"""Readable port of the binary-confirmed ordinary topology loop.

Exactness depends on a separately proved floor-entry contract. It remains separate from
the mechanical reference port, and it is not exposed as a complete exact-map
API because special-room placement is outside Milestone 4.  External gameplay
fixture validation is tracked independently from the static-binary proof.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field, replace
from typing import Protocol

from .floor_init import Basement1TopologyInputs
from .rng import IsaacRNG
from .topology_geometry import (
    DIRECTION_OFFSETS,
    GRID_HEIGHT,
    GRID_WIDTH,
    INVALID_POSITION,
    RoomShape,
    door_source_position,
    door_target_position,
    large_room_candidate_templates,
    occupied_cells,
)


class TopologyInputs(Protocol):
    generator_seed: int
    target_room_count: int
    required_dead_ends: int
    allowed_shapes_mask: int


@dataclass
class LevelGeneratorRoom:
    column: int
    line: int
    shape: RoomShape
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
    def link_position(self) -> tuple[int, int]:
        return self.link_column, self.link_line

    @property
    def grid_index(self) -> int:
        return self.line * GRID_WIDTH + self.column

    @property
    def cells(self) -> tuple[tuple[int, int], ...]:
        return occupied_cells(self.column, self.line, self.shape)


@dataclass(frozen=True)
class TopologyResearchResult:
    rooms: tuple[LevelGeneratorRoom, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    non_dead_ends: tuple[int, ...]
    target_room_count: int
    retries: int
    final_rng_seed: int
    expansion_order: tuple[int, ...]
    forced_dead_end_attempts: int


class LevelGeneratorResearch:
    """Typed port of the recovered x86 ``LevelGenerator`` structure."""

    def __init__(self, seed: int) -> None:
        self.rng = IsaacRNG.game_constructor(seed, 35)  # (5,9,7)
        self.allowed_shapes = 0
        self.room_map = [-1] * (GRID_WIDTH * GRID_HEIGHT)
        self.blocked_positions = [False] * (GRID_WIDTH * GRID_HEIGHT)
        self.rooms: list[LevelGeneratorRoom] = []
        self.dead_ends: list[int] = []
        self.non_dead_ends: list[int] = []
        self.is_xl = False
        self.is_chapter6 = False
        self.is_stage_void = False
        self.next_boss_room_index = -1
        self.num_boss_rooms = 0
        self.expansion_order: list[int] = []
        self.forced_dead_end_attempts = 0

    @staticmethod
    def _in_bounds(position: tuple[int, int]) -> bool:
        column, line = position
        return 0 <= column < GRID_WIDTH and 0 <= line < GRID_HEIGHT

    @staticmethod
    def _grid_index(position: tuple[int, int]) -> int:
        column, line = position
        if not LevelGeneratorResearch._in_bounds(position):
            return -1
        return line * GRID_WIDTH + column

    def _shape_allowed(self, shape: int | RoomShape) -> bool:
        return bool(self.allowed_shapes & (1 << int(shape)))

    def is_pos_free(
        self, position: tuple[int, int], shape: int | RoomShape
    ) -> bool:
        chapter6_forbidden = -1
        if self.rooms:
            start = self.rooms[0]
            chapter6_forbidden = self._grid_index((start.column, start.line - 1))
        for cell in occupied_cells(position[0], position[1], shape):
            index = self._grid_index(cell)
            if index < 0:
                return False
            if self.is_chapter6 and index == chapter6_forbidden:
                return False
            if self.room_map[index] >= 0 or self.blocked_positions[index]:
                return False
        return True

    def count_neighbor_links(self, position: tuple[int, int]) -> int:
        """Port RVA 0x005B0440."""

        center_index = self._grid_index(position)
        center_room = self.room_map[center_index] if center_index >= 0 else -1
        count = 0
        for dx, dy in DIRECTION_OFFSETS:
            neighbor_index = self._grid_index((position[0] + dx, position[1] + dy))
            if neighbor_index < 0:
                continue
            neighbor_room = self.room_map[neighbor_index]
            if neighbor_room >= 0 and neighbor_room != center_room:
                count += 1
        return count

    def is_placement_valid(self, room: LevelGeneratorRoom) -> bool:
        """Port RVA 0x005B0240's eight-slot compatibility pass."""

        for slot in range(8):
            source = door_source_position(room.column, room.line, room.shape, slot)
            target = door_target_position(
                room.column,
                room.line,
                room.shape,
                slot,
                ignore_thin_restrictions=True,
            )
            target_index = self._grid_index(target)
            if target_index < 0:
                continue
            neighbor_id = self.room_map[target_index]
            if neighbor_id < 0:
                continue
            if source == INVALID_POSITION:
                return False
            neighbor = self.rooms[neighbor_id]
            if not any(
                door_target_position(
                    neighbor.column, neighbor.line, neighbor.shape, return_slot
                )
                == source
                for return_slot in range(8)
            ):
                return False
        return True

    def place_room(self, room: LevelGeneratorRoom) -> LevelGeneratorRoom:
        placed = replace(
            room,
            generation_index=len(self.rooms),
            neighbors=set(room.neighbors),
        )
        self.rooms.append(placed)
        for cell in placed.cells:
            index = self._grid_index(cell)
            if index < 0:
                raise AssertionError("binary placement preconditions require an in-bounds cell")
            self.room_map[index] = placed.generation_index
        return placed

    def _candidate(
        self,
        column: int,
        line: int,
        shape: int | RoomShape,
        source: LevelGeneratorRoom,
        door_slot: int,
        target: tuple[int, int],
    ) -> LevelGeneratorRoom:
        return LevelGeneratorRoom(
            column=column,
            line=line,
            shape=RoomShape(shape),
            origin_neighbor_connect_dir=door_slot & 3,
            origin_neighbor_door_slot=door_slot,
            link_column=target[0],
            link_line=target[1],
            distance_from_start=source.distance_from_start + 1,
        )

    def get_neighbor_candidates(
        self, generation_index: int, *, force_all_large: bool = False
    ) -> list[LevelGeneratorRoom]:
        source = self.rooms[generation_index]
        candidates: list[LevelGeneratorRoom] = []
        shape1_allowed = self._shape_allowed(RoomShape.ROOMSHAPE_1x1)
        for door_slot in range(8):
            target = door_target_position(
                source.column, source.line, source.shape, door_slot
            )
            if not self._in_bounds(target):
                continue
            if not self.is_pos_free(target, RoomShape.ROOMSHAPE_1x1):
                continue

            if shape1_allowed:
                candidates.append(
                    self._candidate(
                        target[0],
                        target[1],
                        RoomShape.ROOMSHAPE_1x1,
                        source,
                        door_slot,
                        target,
                    )
                )

            templates = large_room_candidate_templates(target, door_slot & 3)
            for template in templates:
                draw = self.rng.next()
                random_gate = (
                    draw % template.divisor == 0
                    or not shape1_allowed
                    or force_all_large
                )
                if not random_gate or not self._shape_allowed(template.shape):
                    continue
                if not self.is_pos_free(template.anchor, template.shape):
                    continue
                candidates.append(
                    self._candidate(
                        template.anchor[0],
                        template.anchor[1],
                        template.shape,
                        source,
                        door_slot,
                        target,
                    )
                )
        return candidates

    def shuffle_candidates(self, candidates: list[LevelGeneratorRoom]) -> None:
        for current_size in range(len(candidates), 1, -1):
            other = self.rng.next() % current_size
            current = current_size - 1
            candidates[current], candidates[other] = candidates[other], candidates[current]

    def generate_rooms(self, target_count: int, start_room: LevelGeneratorRoom) -> None:
        start = self.place_room(start_room)
        queue: deque[int] = deque((start.generation_index,))
        placed_count = 0

        while queue and placed_count < target_count:
            source_index = queue.popleft()
            self.expansion_order.append(source_index)
            candidates = self.get_neighbor_candidates(source_index)
            self.shuffle_candidates(candidates)

            if source_index == start.generation_index:
                if target_count < 16:
                    wanted = 2 + (self.rng.next() & 1)
                else:
                    wanted = len(candidates)
            else:
                wanted = min(
                    len(candidates),
                    sum(self.rng.next() & 1 for _ in range(4)),
                )

            placed_from_source = 0
            for candidate in candidates:
                if not self.is_pos_free(
                    (candidate.column, candidate.line), candidate.shape
                ):
                    continue
                links = self.count_neighbor_links(candidate.link_position)
                if links >= 2:
                    if not (self.is_xl or self.is_stage_void):
                        continue
                    if self.rng.next() % 10 != 0:
                        continue
                if not self.is_placement_valid(candidate):
                    continue

                placed = self.place_room(candidate)
                if self.rng.next() % 3 == 0:
                    queue.append(placed.generation_index)
                else:
                    queue.appendleft(placed.generation_index)
                placed_count += 1
                placed_from_source += 1
                if placed_from_source >= wanted or placed_count >= target_count:
                    break

    def update_room_connections(self, room: LevelGeneratorRoom) -> None:
        room.doors = 0
        room.neighbors.clear()
        for slot in range(8):
            target = door_target_position(room.column, room.line, room.shape, slot)
            index = self._grid_index(target)
            if index < 0:
                continue
            neighbor = self.room_map[index]
            if neighbor < 0:
                continue
            room.doors |= 1 << slot
            room.neighbors.add(neighbor)

    def mark_dead_ends(self) -> None:
        for room in self.rooms[1:]:
            if self.count_neighbor_links(room.link_position) < 2:
                room.dead_end = True

        for room in self.rooms[1:]:
            if room.link_position == INVALID_POSITION:
                continue
            opposite = (room.origin_neighbor_connect_dir + 2) & 3
            dx, dy = DIRECTION_OFFSETS[opposite]
            parent_position = (room.link_column + dx, room.link_line + dy)
            parent_index = self._grid_index(parent_position)
            parent_id = self.room_map[parent_index] if parent_index >= 0 else -1
            if parent_id < 0:
                raise AssertionError("binary invariant: candidate must retain a parent link")
            self.rooms[parent_id].dead_end = False

    def classify_dead_ends(self) -> None:
        self.dead_ends.clear()
        self.non_dead_ends.clear()
        self.mark_dead_ends()
        for room in self.rooms:
            self.update_room_connections(room)
            destination = self.dead_ends if room.dead_end else self.non_dead_ends
            destination.append(room.generation_index)

    def force_new_dead_end(self) -> bool:
        room_index = 0
        while room_index < len(self.rooms):
            candidates = self.get_neighbor_candidates(
                self.rooms[room_index].generation_index,
                force_all_large=True,
            )
            for candidate in candidates:
                if not self.is_pos_free(
                    (candidate.column, candidate.line), candidate.shape
                ):
                    continue
                if self.count_neighbor_links(candidate.link_position) >= 2:
                    continue
                self.place_room(candidate)
                return True
            room_index += 1
        return False

    def generate_once(
        self,
        target_count: int,
        required_dead_ends: int,
        allowed_shapes: int,
        start_room: LevelGeneratorRoom,
    ) -> None:
        self.allowed_shapes = allowed_shapes
        self.room_map[:] = [-1] * len(self.room_map)
        self.rooms.clear()
        self.dead_ends.clear()
        self.non_dead_ends.clear()
        self.expansion_order.clear()
        self.forced_dead_end_attempts = 0
        self.next_boss_room_index = -1
        self.num_boss_rooms = 0
        self.generate_rooms(target_count, start_room)
        self.classify_dead_ends()

        remaining_attempts = 5
        while len(self.dead_ends) < required_dead_ends and remaining_attempts > 0:
            self.forced_dead_end_attempts += 1
            self.force_new_dead_end()
            self.classify_dead_ends()
            remaining_attempts -= 1

        # RVA 0x005ADCA9..0x005ADD20 uses an in-place selection sort.  A
        # stable high-level sort changes equal-distance order after earlier
        # swaps, which later room selection observes.
        position = 0
        while position < len(self.dead_ends):
            best = position
            for scan in range(position + 1, len(self.dead_ends)):
                if (
                    self.rooms[self.dead_ends[best]].distance_from_start
                    < self.rooms[self.dead_ends[scan]].distance_from_start
                ):
                    best = scan
            self.dead_ends[position], self.dead_ends[best] = (
                self.dead_ends[best],
                self.dead_ends[position],
            )
            position += 1


def generate_topology_research(
    inputs: TopologyInputs,
) -> TopologyResearchResult:
    """Run the topology leaf under a separately verified floor contract."""

    generator = LevelGeneratorResearch(inputs.generator_seed)
    generator.is_xl = bool(getattr(inputs, "is_xl", False))
    target_count = inputs.target_room_count
    retries = 0
    attempt = 0
    while True:
        attempt += 1
        generator.blocked_positions[:] = [False] * len(generator.blocked_positions)
        generator.generate_once(
            target_count=target_count,
            required_dead_ends=inputs.required_dead_ends,
            allowed_shapes=inputs.allowed_shapes_mask,
            start_room=LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        if len(generator.dead_ends) >= inputs.required_dead_ends:
            break
        retries += 1
        if attempt >= 10 and attempt % 5 == 0 and target_count < 64:
            target_count += 1

    rooms = tuple(replace(room, neighbors=set(room.neighbors)) for room in generator.rooms)
    return TopologyResearchResult(
        rooms=rooms,
        room_map=tuple(generator.room_map),
        dead_ends=tuple(generator.dead_ends),
        non_dead_ends=tuple(generator.non_dead_ends),
        target_room_count=target_count,
        retries=retries,
        final_rng_seed=generator.rng.seed,
        expansion_order=tuple(generator.expansion_order),
        forced_dead_end_attempts=generator.forced_dead_end_attempts,
    )


def generate_basement1_topology_research(
    inputs: Basement1TopologyInputs,
) -> TopologyResearchResult:
    """Compatibility wrapper for the frozen Basement I input contract."""

    return generate_topology_research(inputs)
