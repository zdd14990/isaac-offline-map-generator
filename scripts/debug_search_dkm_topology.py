"""Search plausible DKM topology streams for the captured large-room signature."""

from __future__ import annotations

import sys

from isaacmap.floor_init import ALL_GENERATED_ROOM_SHAPES_MASK
from isaacmap.rng import IsaacRNG, RNG_SHIFT_TRIPLES
from isaacmap.seed import decode_seed
from isaacmap.stage_seed import derive_initial_seed_sequence
from isaacmap.topology import LevelGeneratorResearch, LevelGeneratorRoom
from isaacmap.topology_geometry import RoomShape, occupied_cells


DESIRED = {
    (4, 6, 7),
    (4, 8, 8),
    (2, 9, 9),
    (7, 9, 6),
}

DESIRED_FOOTPRINTS = (
    frozenset(((0, 0), (1, 0))),
    frozenset(((0, 2), (1, 2), (0, 3), (1, 3))),
    frozenset(((-1, 3), (-2, 4), (-1, 4))),
    frozenset(((3, 3), (4, 3))),
)

TRANSFORMS = (
    lambda x, y: (x, y),
    lambda x, y: (-x, y),
    lambda x, y: (x, -y),
    lambda x, y: (-x, -y),
    lambda x, y: (y, x),
    lambda x, y: (-y, x),
    lambda x, y: (y, -x),
    lambda x, y: (-y, -x),
)


def contains_captured_geometry(
    actual: set[tuple[int, int, int]], *, translated: bool = False
) -> bool:
    """Match only shape distinctions visible in the captured minimap.

    The minimap footprint cannot distinguish 2x1 (6) from IIH (7).  The
    missing top-left quadrant does identify the L room as LTL (9).
    """

    first_anchors = (
        (column, line)
        for column, line, shape in actual
        if shape in (6, 7)
    )
    for column, line in first_anchors:
        if not translated and (column, line) != (4, 6):
            continue
        if (
            (4, 8, 8) if not translated else (column, line + 2, 8)
        ) not in actual:
            continue
        if (
            (2, 9, 9) if not translated else (column - 2, line + 3, 9)
        ) not in actual:
            continue
        right_anchor = (7, 9) if not translated else (column + 3, line + 3)
        if any((*right_anchor, shape) in actual for shape in (6, 7)):
            return True
    return False


def signature(generator: LevelGeneratorResearch) -> set[tuple[int, int, int]]:
    return {
        (room.column, room.line, int(room.shape))
        for room in generator.rooms
        if int(room.shape) > 1
    }


def contains_captured_footprints(generator: LevelGeneratorResearch) -> bool:
    """Match the visible multi-cell rooms under translation and dihedral transforms."""

    actual = {
        frozenset(occupied_cells(room.column, room.line, room.shape))
        for room in generator.rooms
        if len(occupied_cells(room.column, room.line, room.shape)) > 1
    }
    if len(actual) != len(DESIRED_FOOTPRINTS):
        return False
    for transform in TRANSFORMS:
        wanted = tuple(
            frozenset(transform(column, line) for column, line in footprint)
            for footprint in DESIRED_FOOTPRINTS
        )
        first = wanted[0]
        for candidate in actual:
            if len(candidate) != len(first):
                continue
            for source_cell in first:
                for target_cell in candidate:
                    dx = target_cell[0] - source_cell[0]
                    dy = target_cell[1] - source_cell[1]
                    translated = tuple(
                        frozenset((x + dx, y + dy) for x, y in footprint)
                        for footprint in wanted
                    )
                    if translated[0] == candidate and all(
                        footprint in actual for footprint in translated[1:]
                    ):
                        return True
    return False


def contains_translation(actual: set[tuple[int, int, int]]) -> bool:
    for column, line, shape in actual:
        if shape != 7:
            continue
        if {
            (column, line, 7),
            (column, line + 2, 8),
            (column - 2, line + 3, 9),
            (column + 3, line + 3, 6),
        } <= actual:
            return True
    return False


def advance(seed: int) -> int:
    seed ^= seed >> 5
    seed ^= (seed << 9) & 0xFFFFFFFF
    seed ^= seed >> 7
    return seed & 0xFFFFFFFF


def advance_stage_slot(seed: int) -> int:
    """Port Seeds::advance_stage_slot's binary (5, 15, 17) xorshift."""

    seed ^= seed >> 5
    seed ^= (seed << 15) & 0xFFFFFFFF
    seed ^= seed >> 17
    return seed & 0xFFFFFFFF


def search_stage_slot_mutations(
    sequence,
) -> list[tuple[int, int, int, int, set[tuple[int, int, int]]]]:
    """Search binary-reachable slot-2 mutations that still roll Labyrinth."""

    mutated_stage_seed = sequence.stage_seeds[2]
    hits: list[tuple[int, int, int, int, set[tuple[int, int, int]]]] = []
    for mutations in range(1, 5001):
        mutated_stage_seed = advance_stage_slot(mutated_stage_seed)
        level_rng = IsaacRNG.game_constructor(mutated_stage_seed, 35)
        level_rng.next()
        copied_seed = level_rng.next()
        gate_draw = level_rng.next()
        generator_seed = level_rng.next()
        if gate_draw % 3 != 0 or generator_seed % 6 != 0:
            continue

        copied_rng = IsaacRNG.game_constructor(copied_seed, 35)
        copied_rng.next()  # gate
        copied_rng.next()  # selector
        difficulty_draw = copied_rng.next()
        base_target = min((1 * 10) // 3 + 5 + (gate_draw & 1), 20) - 3
        target = min((base_target * 18) // 10, 45) + 2 + (difficulty_draw & 1)

        candidate = LevelGeneratorResearch(generator_seed)
        candidate.is_xl = True
        candidate.generate_once(
            target,
            7,
            ALL_GENERATED_ROOM_SHAPES_MASK,
            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        actual = signature(candidate)
        if contains_captured_footprints(candidate):
            hits.append((mutations, mutated_stage_seed, generator_seed, target, actual))
            if len(hits) >= 20:
                break
    return hits


def search_retry_escalation() -> list[
    tuple[int, int, int, int, set[tuple[int, int, int]]]
]:
    """Search the binary outer-loop target escalation on forced retry."""

    hits: list[tuple[int, int, int, int, set[tuple[int, int, int]]]] = []
    for required_dead_ends in (7, 8):
        generator = LevelGeneratorResearch(3869886000)
        generator.is_xl = True
        target = 12
        for attempt in range(1, 1001):
            generator.generate_once(
                target,
                required_dead_ends,
                ALL_GENERATED_ROOM_SHAPES_MASK,
                LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
            )
            actual = signature(generator)
            if contains_captured_footprints(generator):
                hits.append(
                    (attempt, target, required_dead_ends, generator.rng.seed, actual)
                )
                if len(hits) >= 20:
                    return hits
            if attempt >= 10 and attempt % 5 == 0 and target < 64:
                target += 1
    return hits


def search_parameters() -> list[
    tuple[bool, int, int, int, set[tuple[int, int, int]]]
]:
    """Search target/dead-end inputs without assuming indistinguishable thin shapes."""

    hits: list[tuple[bool, int, int, int, set[tuple[int, int, int]]]] = []
    for is_xl in (False, True):
        for target in range(4, 31):
            for dead_ends in range(5, 13):
                candidate = LevelGeneratorResearch(3869886000)
                candidate.is_xl = is_xl
                candidate.generate_once(
                    target,
                    dead_ends,
                    ALL_GENERATED_ROOM_SHAPES_MASK,
                    LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
                )
                actual = signature(candidate)
                if contains_captured_footprints(candidate):
                    hits.append(
                        (is_xl, target, dead_ends, candidate.rng.seed, actual)
                    )
    return hits


def search_binary_reachable_footprints(
    sequence,
) -> list[tuple[int, int, int, int, bool, int, set[tuple[int, int, int]]]]:
    """Search compact binary-reachable seed and topology-input families."""

    hits: list[
        tuple[int, int, int, int, bool, int, set[tuple[int, int, int]]]
    ] = []
    for slot, stage_seed in enumerate(sequence.stage_seeds):
        level_rng = IsaacRNG.game_constructor(stage_seed, 35)
        for phase in range(1, 65):
            candidate_seed = level_rng.next()
            for target in range(7, 21):
                for dead_ends in range(5, 10):
                    for giant in (False, True):
                        candidate = LevelGeneratorResearch(candidate_seed)
                        candidate.is_xl = True
                        candidate.generate_once(
                            target,
                            dead_ends,
                            0x1FF0 if giant else ALL_GENERATED_ROOM_SHAPES_MASK,
                            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
                        )
                        if contains_captured_footprints(candidate):
                            hits.append(
                                (
                                    slot,
                                    phase,
                                    target,
                                    dead_ends,
                                    giant,
                                    candidate.rng.seed,
                                    signature(candidate),
                                )
                            )
                            if len(hits) >= 20:
                                return hits
    return hits


def main() -> None:
    generator = LevelGeneratorResearch(3869886000)
    generator.is_xl = True
    multiset_matches: list[tuple[int, set[tuple[int, int, int]]]] = []
    for attempt in range(1, 1001):
        generator.generate_once(
            12,
            7,
            ALL_GENERATED_ROOM_SHAPES_MASK,
            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        actual = signature(generator)
        if DESIRED <= actual:
            print("exact-subset", attempt, generator.rng.seed, sorted(actual))
        if contains_translation(actual):
            print("translated-attempt", attempt, generator.rng.seed, sorted(actual))
        if contains_captured_geometry(actual):
            print("captured-geometry-attempt", attempt, generator.rng.seed, sorted(actual))
        if contains_captured_geometry(actual, translated=True):
            print("translated-captured-attempt", attempt, generator.rng.seed, sorted(actual))
        if sorted(shape for _, _, shape in actual) == [6, 7, 8, 9]:
            multiset_matches.append((attempt, actual))
    print("matching-multisets", multiset_matches[:20])

    state = 362265690
    for phase in range(1, 5001):
        state = advance(state)
        candidate = LevelGeneratorResearch(state)
        candidate.is_xl = True
        candidate.generate_once(
            12,
            7,
            ALL_GENERATED_ROOM_SHAPES_MASK,
            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        actual = signature(candidate)
        if DESIRED <= actual:
            print("level-phase-subset", phase, state, sorted(actual))
        if contains_translation(actual):
            print("translated-phase", phase, state, sorted(actual))
        if contains_captured_geometry(actual):
            print("captured-geometry-phase", phase, state, sorted(actual))
        if contains_captured_geometry(actual, translated=True):
            print("translated-captured-phase", phase, state, sorted(actual))

    print("parameter-hits", search_parameters())

    # Audit only binary-reachable seed families.  ALT generation normally
    # selects slot 2; the neighboring slots and constructor shift table are
    # included to identify a wrong input contract without guessing a seed.
    start_seed = decode_seed("DKM8 9MNM")
    sequence = derive_initial_seed_sequence(start_seed)
    for slot, stage_seed in enumerate(sequence.stage_seeds):
        level_rng = IsaacRNG.game_constructor(stage_seed, 35)
        level_draws = [level_rng.next() for _ in range(12)]
        for phase, candidate_seed in enumerate(level_draws, start=1):
            candidate = LevelGeneratorResearch(candidate_seed)
            candidate.is_xl = True
            candidate.generate_once(
                12,
                7,
                ALL_GENERATED_ROOM_SHAPES_MASK,
                LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
            )
            actual = signature(candidate)
            if contains_captured_geometry(actual, translated=True):
                print("stage-slot-match", slot, phase, candidate_seed, sorted(actual))

    for shift_index in range(len(RNG_SHIFT_TRIPLES)):
        candidate = LevelGeneratorResearch(3869886000)
        candidate.rng = IsaacRNG.game_constructor(3869886000, shift_index)
        candidate.is_xl = True
        candidate.generate_once(
            12,
            7,
            ALL_GENERATED_ROOM_SHAPES_MASK,
            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        actual = signature(candidate)
        if contains_captured_geometry(actual, translated=True):
            print("generator-shift-match", shift_index, sorted(actual))

    for shape_mask in range(1 << 13):
        candidate = LevelGeneratorResearch(3869886000)
        candidate.is_xl = True
        candidate.generate_once(
            12,
            7,
            shape_mask,
            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        actual = signature(candidate)
        if contains_captured_geometry(actual, translated=True):
            print("shape-mask-match", hex(shape_mask), sorted(actual))

    # Cross-check only compact, binary-reachable input families.  This catches
    # a wrong stage slot, a nearby pre-topology RNG phase, the paired-ALT flag,
    # an extra dead-end requirement, or Giant's shape-mask/target branch without
    # treating arbitrary uint32 seeds as evidence.
    reachable_hits: list[
        tuple[int, int, int, int, bool, int, set[tuple[int, int, int]]]
    ] = []
    for slot, stage_seed in enumerate(sequence.stage_seeds):
        level_rng = IsaacRNG.game_constructor(stage_seed, 35)
        for phase in range(1, 65):
            candidate_seed = level_rng.next()
            for target in range(7, 21):
                for dead_ends in range(5, 10):
                    for giant in (False, True):
                        candidate = LevelGeneratorResearch(candidate_seed)
                        candidate.is_xl = True
                        candidate.generate_once(
                            target,
                            dead_ends,
                            0x1FF0 if giant else ALL_GENERATED_ROOM_SHAPES_MASK,
                            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
                        )
                        actual = signature(candidate)
                        if contains_captured_geometry(actual, translated=True):
                            reachable_hits.append(
                                (
                                    slot,
                                    phase,
                                    target,
                                    dead_ends,
                                    giant,
                                    candidate.rng.seed,
                                    actual,
                                )
                            )
                            if len(reachable_hits) >= 20:
                                print("binary-reachable-hits", reachable_hits)
                                return
    print("binary-reachable-hits", reachable_hits)

    # A continued/restarted floor can mutate its stored stage slot through
    # Seeds::advance_stage_slot.  This is a distinct (5,15,17) stream, not a
    # phase of the Level RNG's (5,9,7) stream searched above.
    print("stage-mutation-hits", search_stage_slot_mutations(sequence))


if __name__ == "__main__":
    if "--stage-mutations-only" in sys.argv:
        start_seed = decode_seed("DKM8 9MNM")
        print(
            "stage-mutation-hits",
            search_stage_slot_mutations(derive_initial_seed_sequence(start_seed)),
        )
    elif "--retry-escalation-only" in sys.argv:
        print("retry-escalation-hits", search_retry_escalation())
    elif "--parameter-only" in sys.argv:
        print("parameter-hits", search_parameters())
    elif "--reachable-only" in sys.argv:
        start_seed = decode_seed("DKM8 9MNM")
        print(
            "binary-reachable-hits",
            search_binary_reachable_footprints(
                derive_initial_seed_sequence(start_seed)
            ),
        )
    else:
        main()
