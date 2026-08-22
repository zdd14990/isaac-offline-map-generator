"""Probe alternate interpretations of the topology loop's STL operations.

This is a research diagnostic only.  A geometry hit is not sufficient to
change the formal generator; the corresponding copied-PE instructions still
have to confirm the interpretation.
"""

from __future__ import annotations

from collections import deque

from isaacmap.floor_init import ALL_GENERATED_ROOM_SHAPES_MASK
from isaacmap.topology import LevelGeneratorResearch, LevelGeneratorRoom
from isaacmap.topology_geometry import RoomShape


def _signature(generator: LevelGeneratorResearch) -> set[tuple[int, int, int]]:
    return {
        (room.column, room.line, int(room.shape))
        for room in generator.rooms
        if int(room.shape) > 1
    }


def _matches_captured_geometry(actual: set[tuple[int, int, int]]) -> bool:
    for column, line, shape in actual:
        if shape not in (6, 7):
            continue
        if (column, line + 2, 8) not in actual:
            continue
        if (column - 2, line + 3, 9) not in actual:
            continue
        if any((column + 3, line + 3, other) in actual for other in (6, 7)):
            return True
    return False


class VariantGenerator(LevelGeneratorResearch):
    def __init__(
        self,
        seed: int,
        *,
        pop_back: bool,
        zero_to_front: bool,
        forward_shuffle: bool,
    ) -> None:
        super().__init__(seed)
        self.pop_back = pop_back
        self.zero_to_front = zero_to_front
        self.forward_shuffle = forward_shuffle

    def shuffle_candidates(self, candidates: list[LevelGeneratorRoom]) -> None:
        if not self.forward_shuffle:
            return super().shuffle_candidates(candidates)
        for current in range(len(candidates) - 1):
            other = current + self.rng.next() % (len(candidates) - current)
            candidates[current], candidates[other] = candidates[other], candidates[current]

    def generate_rooms(self, target_count: int, start_room: LevelGeneratorRoom) -> None:
        start = self.place_room(start_room)
        queue: deque[int] = deque((start.generation_index,))
        placed_count = 0

        while queue and placed_count < target_count:
            source_index = queue.pop() if self.pop_back else queue.popleft()
            self.expansion_order.append(source_index)
            candidates = self.get_neighbor_candidates(source_index)
            self.shuffle_candidates(candidates)

            if source_index == start.generation_index:
                wanted = 2 + (self.rng.next() & 1) if target_count < 16 else len(candidates)
            else:
                wanted = min(
                    len(candidates),
                    sum(self.rng.next() & 1 for _ in range(4)),
                )

            placed_from_source = 0
            for candidate in candidates:
                if not self.is_pos_free((candidate.column, candidate.line), candidate.shape):
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
                zero = self.rng.next() % 3 == 0
                put_front = zero if self.zero_to_front else not zero
                if put_front:
                    queue.appendleft(placed.generation_index)
                else:
                    queue.append(placed.generation_index)
                placed_count += 1
                placed_from_source += 1
                if placed_from_source >= wanted or placed_count >= target_count:
                    break


def main() -> None:
    for pop_back in (False, True):
        for zero_to_front in (False, True):
            for forward_shuffle in (False, True):
                generator = VariantGenerator(
                    3_869_886_000,
                    pop_back=pop_back,
                    zero_to_front=zero_to_front,
                    forward_shuffle=forward_shuffle,
                )
                generator.is_xl = True
                generator.generate_once(
                    12,
                    7,
                    ALL_GENERATED_ROOM_SHAPES_MASK,
                    LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
                )
                actual = _signature(generator)
                print(
                    {
                        "pop_back": pop_back,
                        "zero_to_front": zero_to_front,
                        "forward_shuffle": forward_shuffle,
                        "match": _matches_captured_geometry(actual),
                        "rooms": len(generator.rooms),
                        "dead_ends": len(generator.dead_ends),
                        "rng": generator.rng.seed,
                        "large": sorted(actual),
                    }
                )


if __name__ == "__main__":
    main()
