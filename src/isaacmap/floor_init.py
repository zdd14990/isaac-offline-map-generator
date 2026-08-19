"""Proven floor-initialization inputs for the first exact topology target."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .rng import IsaacRNG
from .stage_seed import get_initial_stage_seed


class Difficulty(str, Enum):
    NORMAL = "NORMAL"
    HARD = "HARD"


LEVEL_RNG_SHIFT_INDEX = 35  # (5, 9, 7), VA 0x00B1F66C.
ALL_GENERATED_ROOM_SHAPES_MASK = sum(1 << shape for shape in range(1, 13))


@dataclass(frozen=True)
class Basement1TopologyInputs:
    """Inputs handed to ``LevelGenerator`` on the supported research path.

    This is not a completed floor.  The scope is a fresh, ordinary, vanilla
    run on ``STAGE1_1`` + ``STAGETYPE_ORIGINAL``, with no challenge, effective
    curse, seed effect, ascent/daily state, Voodoo Head owner, blocked cell, or
    stage-seed mutation before ``Level::Init``.
    """

    stage_seed: int
    level_rng_draws: tuple[int, int, int, int]
    generator_seed: int
    target_room_count: int
    required_dead_ends: int
    allowed_shapes_mask: int
    starting_grid_index: int = 84
    starting_shape: int = 1


@dataclass(frozen=True)
class Basement2TopologyInputs:
    """Binary-derived Stage 2 entry values for the canonical base profile.

    Unlike Basement I, Stage 2 performs the ordinary curse gate.  The copied
    stack RNG owns that gate, its optional curse-selector draw, and the HARD
    room-count bonus.  The persistent Level RNG independently supplies the
    base count bit and the LevelGenerator seed.
    """

    stage_seed: int
    level_rng_draws: tuple[int, int, int, int]
    copied_rng_draws: tuple[int, ...]
    curse_rate_denominator: int
    curse_gate_succeeded: bool
    curse_selector: int | None
    effective_curse_mask: int
    generator_seed: int
    target_room_count: int
    required_dead_ends: int
    allowed_shapes_mask: int
    room_config_min_difficulty: int
    room_config_max_difficulty: int
    starting_grid_index: int = 84
    starting_shape: int = 1


@dataclass(frozen=True)
class Caves1TopologyInputs:
    """Binary-derived Stage 3 ORIGINAL inputs after Basement-II replay.

    Stage 3 is the first supported entry on which the ordinary curse selector
    may retain Labyrinth.  ``is_xl`` therefore changes both topology target
    size and the generator's candidate-link rule; it is not presentation
    metadata.
    """

    stage_seed: int
    level_rng_draws: tuple[int, int, int, int]
    copied_rng_draws: tuple[int, ...]
    curse_rate_denominator: int
    curse_gate_succeeded: bool
    curse_selector: int | None
    effective_curse_mask: int
    is_xl: bool
    generator_seed: int
    target_room_count: int
    required_dead_ends: int
    allowed_shapes_mask: int
    room_config_stage: int
    room_config_min_difficulty: int
    room_config_max_difficulty: int
    starting_grid_index: int = 84
    starting_shape: int = 1


def derive_basement1_topology_inputs(
    start_seed: int, difficulty: Difficulty | str
) -> Basement1TopologyInputs:
    """Derive the confirmed pre-``Generate`` values for Basement I.

    The third main-stream draw and the first draw from the copied stack RNG
    are identical on this no-curse path.  HARD therefore adds ``2 + bit`` to
    a base count which already contains the same low bit.
    """

    try:
        difficulty_value = Difficulty(difficulty)
    except ValueError as error:
        raise ValueError("difficulty must be NORMAL or HARD") from error

    stage_seed = get_initial_stage_seed(start_seed, 1)
    level_rng = IsaacRNG.game_constructor(stage_seed, LEVEL_RNG_SHIFT_INDEX)
    first = level_rng.next()
    second = level_rng.next()

    # Level::Init copies the stack RNG at this point. Basement I suppresses
    # the ordinary curse roll, so its next state equals the third main draw.
    copied_rng = IsaacRNG(second, level_rng.shift1, level_rng.shift2, level_rng.shift3)
    third = level_rng.next()
    hard_bonus_draw = copied_rng.next()
    if hard_bonus_draw != third:  # pragma: no cover - structural invariant
        raise AssertionError("the no-curse copied RNG must remain phase-aligned")

    target_room_count = 8 + (third & 1)
    if difficulty_value is Difficulty.HARD:
        target_room_count += 2 + (hard_bonus_draw & 1)

    fourth = level_rng.next()
    return Basement1TopologyInputs(
        stage_seed=stage_seed,
        level_rng_draws=(first, second, third, fourth),
        generator_seed=fourth,
        target_room_count=target_room_count,
        required_dead_ends=5,
        allowed_shapes_mask=ALL_GENERATED_ROOM_SHAPES_MASK,
    )


def derive_basement2_topology_inputs(
    start_seed: int, difficulty: Difficulty | str
) -> Basement2TopologyInputs:
    """Derive canonical ORIGINAL Basement II topology inputs.

    The fixed profile is the base fresh-save generation tier documented in
    ``research/notes/canonical_run_profile.md``: no challenge/daily/ascent,
    no seed-effect curse masks, no collectible 260/599 owner, no optional
    progression curse-rate flags and no mod callback mutation.
    """

    try:
        difficulty_value = Difficulty(difficulty)
    except ValueError as error:
        raise ValueError("difficulty must be NORMAL or HARD") from error

    stage_seed = get_initial_stage_seed(start_seed, 2)
    level_rng = IsaacRNG.game_constructor(stage_seed, LEVEL_RNG_SHIFT_INDEX)
    first = level_rng.next()
    second = level_rng.next()

    copied_rng = IsaacRNG(
        second, level_rng.shift1, level_rng.shift2, level_rng.shift3
    )
    copied_draws: list[int] = []
    curse_rate = 40 if difficulty_value is Difficulty.HARD else 80
    curse_gate = copied_rng.next()
    copied_draws.append(curse_gate)
    curse_succeeded = curse_gate % curse_rate == 0
    curse_selector: int | None = None
    curse_mask = 0
    if curse_succeeded:
        curse_selector = copied_rng.next()
        copied_draws.append(curse_selector)
        choice = curse_selector % 6
        # Labyrinth is only valid on odd stages below Stage 8. Basement II is
        # even, so choice 0 consumes the selector but leaves the curse empty.
        if choice == 1:
            curse_mask = 0x04  # Lost
        elif choice == 2:
            curse_mask = 0x01  # Darkness
        elif choice == 3:
            curse_mask = 0x08  # Unknown
        elif choice == 4:
            curse_mask = 0x20  # Maze
        elif choice == 5:
            curse_mask = 0x40  # Blind

    third = level_rng.next()
    target_room_count = (2 * 10) // 3 + 5 + (third & 1)
    if curse_mask & 0x04:
        target_room_count += 4
    if difficulty_value is Difficulty.HARD:
        hard_bonus = copied_rng.next()
        copied_draws.append(hard_bonus)
        target_room_count += 2 + (hard_bonus & 1)

    fourth = level_rng.next()
    minimum, maximum = (
        (10, 15) if difficulty_value is Difficulty.HARD else (5, 10)
    )
    return Basement2TopologyInputs(
        stage_seed=stage_seed,
        level_rng_draws=(first, second, third, fourth),
        copied_rng_draws=tuple(copied_draws),
        curse_rate_denominator=curse_rate,
        curse_gate_succeeded=curse_succeeded,
        curse_selector=curse_selector,
        effective_curse_mask=curse_mask,
        generator_seed=fourth,
        target_room_count=target_room_count,
        required_dead_ends=6,
        allowed_shapes_mask=ALL_GENERATED_ROOM_SHAPES_MASK,
        room_config_min_difficulty=minimum,
        room_config_max_difficulty=maximum,
    )


def derive_caves1_topology_inputs(
    start_seed: int, difficulty: Difficulty | str
) -> Caves1TopologyInputs:
    """Derive canonical ORIGINAL Caves-I topology inputs from the run seed.

    The canonical generation profile still has no gameplay-supplied curse
    modifiers, collectible 599 owner, Giant curse, challenge/daily/ascent or
    alternate route.  A naturally selected Labyrinth curse is retained on odd
    Stage 3 and is modeled exactly rather than suppressed.
    """

    try:
        difficulty_value = Difficulty(difficulty)
    except ValueError as error:
        raise ValueError("difficulty must be NORMAL or HARD") from error

    stage_seed = get_initial_stage_seed(start_seed, 3)
    level_rng = IsaacRNG.game_constructor(stage_seed, LEVEL_RNG_SHIFT_INDEX)
    first = level_rng.next()
    second = level_rng.next()
    copied_rng = IsaacRNG(
        second, level_rng.shift1, level_rng.shift2, level_rng.shift3
    )
    copied_draws: list[int] = []
    curse_rate = 40 if difficulty_value is Difficulty.HARD else 80
    curse_gate = copied_rng.next()
    copied_draws.append(curse_gate)
    curse_succeeded = curse_gate % curse_rate == 0
    curse_selector: int | None = None
    curse_mask = 0
    if curse_succeeded:
        curse_selector = copied_rng.next()
        copied_draws.append(curse_selector)
        choice = curse_selector % 6
        if choice == 0:
            # Level::can_have_labyrinth accepts odd Stage 3 below Stage 8 in
            # the canonical ordinary game mode.
            curse_mask = 0x02
        elif choice == 1:
            curse_mask = 0x04
        elif choice == 2:
            curse_mask = 0x01
        elif choice == 3:
            curse_mask = 0x08
        elif choice == 4:
            curse_mask = 0x20
        else:
            curse_mask = 0x40

    third = level_rng.next()
    base_target = min((3 * 10) // 3 + 5 + (third & 1), 20)
    is_xl = bool(curse_mask & 0x02)
    if is_xl:
        # RVA 0x00340F4A uses the frozen binary64 constant 1.8 followed by
        # cvttsd2si and a cap of 45.
        target_room_count = min((base_target * 18) // 10, 45)
    else:
        target_room_count = base_target
        if curse_mask & 0x04:
            target_room_count += 4

    # The copied stack RNG always advances here.  NORMAL discards the low bit;
    # HARD uses it for the 2 + bit room-count bonus.
    difficulty_draw = copied_rng.next()
    copied_draws.append(difficulty_draw)
    if difficulty_value is Difficulty.HARD:
        target_room_count += 2 + (difficulty_draw & 1)

    fourth = level_rng.next()
    if is_xl:
        minimum, maximum = (
            (5, 15) if difficulty_value is Difficulty.HARD else (1, 10)
        )
    else:
        minimum, maximum = (
            (5, 10) if difficulty_value is Difficulty.HARD else (1, 5)
        )
    return Caves1TopologyInputs(
        stage_seed=stage_seed,
        level_rng_draws=(first, second, third, fourth),
        copied_rng_draws=tuple(copied_draws),
        curse_rate_denominator=curse_rate,
        curse_gate_succeeded=curse_succeeded,
        curse_selector=curse_selector,
        effective_curse_mask=curse_mask,
        is_xl=is_xl,
        generator_seed=fourth,
        target_room_count=target_room_count,
        required_dead_ends=7 if is_xl else 6,
        allowed_shapes_mask=ALL_GENERATED_ROOM_SHAPES_MASK,
        room_config_stage=4,
        room_config_min_difficulty=minimum,
        room_config_max_difficulty=maximum,
    )


@dataclass(frozen=True)
class Caves2TopologyInputs:
    """Binary-derived Stage 4 ORIGINAL inputs after Caves-I replay.

    Even Stage 4 can never satisfy the Labyrinth predicate, so ``is_xl`` is
    always false.  It shares the Caves RoomConfig stage (4) and the Caves
    BossPool (index 4) with Caves I.
    """

    stage_seed: int
    level_rng_draws: tuple[int, int, int, int]
    copied_rng_draws: tuple[int, ...]
    curse_rate_denominator: int
    curse_gate_succeeded: bool
    curse_selector: int | None
    effective_curse_mask: int
    is_xl: bool
    generator_seed: int
    target_room_count: int
    required_dead_ends: int
    allowed_shapes_mask: int
    room_config_stage: int
    room_config_min_difficulty: int
    room_config_max_difficulty: int
    starting_grid_index: int = 84
    starting_shape: int = 1


def derive_caves2_topology_inputs(
    start_seed: int, difficulty: Difficulty | str
) -> Caves2TopologyInputs:
    """Derive canonical ORIGINAL Caves-II topology inputs from the run seed."""

    try:
        difficulty_value = Difficulty(difficulty)
    except ValueError as error:
        raise ValueError("difficulty must be NORMAL or HARD") from error

    stage_seed = get_initial_stage_seed(start_seed, 4)
    level_rng = IsaacRNG.game_constructor(stage_seed, LEVEL_RNG_SHIFT_INDEX)
    first = level_rng.next()
    second = level_rng.next()
    copied_rng = IsaacRNG(
        second, level_rng.shift1, level_rng.shift2, level_rng.shift3
    )
    copied_draws: list[int] = []
    curse_rate = 40 if difficulty_value is Difficulty.HARD else 80
    curse_gate = copied_rng.next()
    copied_draws.append(curse_gate)
    curse_succeeded = curse_gate % curse_rate == 0
    curse_selector: int | None = None
    curse_mask = 0
    if curse_succeeded:
        curse_selector = copied_rng.next()
        copied_draws.append(curse_selector)
        choice = curse_selector % 6
        # Labyrinth (choice 0) is only valid on odd stages below Stage 8.
        # Caves II is even, so choice 0 consumes the selector but is empty.
        if choice == 1:
            curse_mask = 0x04  # Lost
        elif choice == 2:
            curse_mask = 0x01  # Darkness
        elif choice == 3:
            curse_mask = 0x08  # Unknown
        elif choice == 4:
            curse_mask = 0x20  # Maze
        elif choice == 5:
            curse_mask = 0x40  # Blind

    third = level_rng.next()
    target_room_count = min((4 * 10) // 3 + 5 + (third & 1), 20)
    if curse_mask & 0x04:
        target_room_count += 4

    # The copied stack RNG always advances here.  NORMAL discards the low bit;
    # HARD uses it for the 2 + bit room-count bonus.
    difficulty_draw = copied_rng.next()
    copied_draws.append(difficulty_draw)
    if difficulty_value is Difficulty.HARD:
        target_room_count += 2 + (difficulty_draw & 1)

    fourth = level_rng.next()
    minimum, maximum = (
        (10, 15) if difficulty_value is Difficulty.HARD else (5, 10)
    )
    return Caves2TopologyInputs(
        stage_seed=stage_seed,
        level_rng_draws=(first, second, third, fourth),
        copied_rng_draws=tuple(copied_draws),
        curse_rate_denominator=curse_rate,
        curse_gate_succeeded=curse_succeeded,
        curse_selector=curse_selector,
        effective_curse_mask=curse_mask,
        is_xl=False,
        generator_seed=fourth,
        target_room_count=target_room_count,
        required_dead_ends=6,
        allowed_shapes_mask=ALL_GENERATED_ROOM_SHAPES_MASK,
        room_config_stage=4,
        room_config_min_difficulty=minimum,
        room_config_max_difficulty=maximum,
    )


@dataclass(frozen=True)
class Depths1TopologyInputs:
    """Binary-derived Stage 5 ORIGINAL inputs after Caves-II replay.

    Odd Stage 5 can satisfy the Labyrinth predicate again, so ``is_xl`` is
    possible.  ``target_room_count`` is capped at 20 before the XL/Lost
    modifiers.
    """

    stage_seed: int
    level_rng_draws: tuple[int, int, int, int]
    copied_rng_draws: tuple[int, ...]
    curse_rate_denominator: int
    curse_gate_succeeded: bool
    curse_selector: int | None
    effective_curse_mask: int
    is_xl: bool
    generator_seed: int
    target_room_count: int
    required_dead_ends: int
    allowed_shapes_mask: int
    room_config_stage: int
    room_config_min_difficulty: int
    room_config_max_difficulty: int
    starting_grid_index: int = 84
    starting_shape: int = 1


def derive_depths1_topology_inputs(
    start_seed: int, difficulty: Difficulty | str
) -> Depths1TopologyInputs:
    """Derive canonical ORIGINAL Depths-I topology inputs from the run seed."""

    try:
        difficulty_value = Difficulty(difficulty)
    except ValueError as error:
        raise ValueError("difficulty must be NORMAL or HARD") from error

    stage_seed = get_initial_stage_seed(start_seed, 5)
    level_rng = IsaacRNG.game_constructor(stage_seed, LEVEL_RNG_SHIFT_INDEX)
    first = level_rng.next()
    second = level_rng.next()
    copied_rng = IsaacRNG(
        second, level_rng.shift1, level_rng.shift2, level_rng.shift3
    )
    copied_draws: list[int] = []
    curse_rate = 40 if difficulty_value is Difficulty.HARD else 80
    curse_gate = copied_rng.next()
    copied_draws.append(curse_gate)
    curse_succeeded = curse_gate % curse_rate == 0
    curse_selector: int | None = None
    curse_mask = 0
    if curse_succeeded:
        curse_selector = copied_rng.next()
        copied_draws.append(curse_selector)
        choice = curse_selector % 6
        if choice == 0:
            # Odd Stage 5 below Stage 8 accepts Labyrinth.
            curse_mask = 0x02
        elif choice == 1:
            curse_mask = 0x04  # Lost
        elif choice == 2:
            curse_mask = 0x01  # Darkness
        elif choice == 3:
            curse_mask = 0x08  # Unknown
        elif choice == 4:
            curse_mask = 0x20  # Maze
        elif choice == 5:
            curse_mask = 0x40  # Blind

    third = level_rng.next()
    # floor(5 * 10 / 3) + 5 = 21, capped at 20 for both bit values.
    base_target = min((5 * 10) // 3 + 5 + (third & 1), 20)
    is_xl = bool(curse_mask & 0x02)
    if is_xl:
        target_room_count = min((base_target * 18) // 10, 45)
    else:
        target_room_count = base_target
        if curse_mask & 0x04:
            target_room_count += 4

    difficulty_draw = copied_rng.next()
    copied_draws.append(difficulty_draw)
    if difficulty_value is Difficulty.HARD:
        target_room_count += 2 + (difficulty_draw & 1)

    fourth = level_rng.next()
    if is_xl:
        minimum, maximum = (
            (5, 15) if difficulty_value is Difficulty.HARD else (1, 10)
        )
    else:
        minimum, maximum = (
            (5, 10) if difficulty_value is Difficulty.HARD else (1, 5)
        )
    return Depths1TopologyInputs(
        stage_seed=stage_seed,
        level_rng_draws=(first, second, third, fourth),
        copied_rng_draws=tuple(copied_draws),
        curse_rate_denominator=curse_rate,
        curse_gate_succeeded=curse_succeeded,
        curse_selector=curse_selector,
        effective_curse_mask=curse_mask,
        is_xl=is_xl,
        generator_seed=fourth,
        target_room_count=target_room_count,
        required_dead_ends=7 if is_xl else 6,
        allowed_shapes_mask=ALL_GENERATED_ROOM_SHAPES_MASK,
        room_config_stage=7,
        room_config_min_difficulty=minimum,
        room_config_max_difficulty=maximum,
    )


@dataclass(frozen=True)
class Depths2TopologyInputs:
    """Binary-derived Stage 6 ORIGINAL inputs after Depths-I replay.

    Even Stage 6 never satisfies the Labyrinth predicate, so ``is_xl`` is
    always false.  ``target_room_count`` is capped at 20 before the Lost/HARD
    modifiers.
    """

    stage_seed: int
    level_rng_draws: tuple[int, int, int, int]
    copied_rng_draws: tuple[int, ...]
    curse_rate_denominator: int
    curse_gate_succeeded: bool
    curse_selector: int | None
    effective_curse_mask: int
    is_xl: bool
    generator_seed: int
    target_room_count: int
    required_dead_ends: int
    allowed_shapes_mask: int
    room_config_stage: int
    room_config_min_difficulty: int
    room_config_max_difficulty: int
    starting_grid_index: int = 84
    starting_shape: int = 1


def derive_depths2_topology_inputs(
    start_seed: int, difficulty: Difficulty | str
) -> Depths2TopologyInputs:
    """Derive canonical ORIGINAL Depths-II topology inputs from the run seed."""

    try:
        difficulty_value = Difficulty(difficulty)
    except ValueError as error:
        raise ValueError("difficulty must be NORMAL or HARD") from error

    stage_seed = get_initial_stage_seed(start_seed, 6)
    level_rng = IsaacRNG.game_constructor(stage_seed, LEVEL_RNG_SHIFT_INDEX)
    first = level_rng.next()
    second = level_rng.next()
    copied_rng = IsaacRNG(
        second, level_rng.shift1, level_rng.shift2, level_rng.shift3
    )
    copied_draws: list[int] = []
    curse_rate = 40 if difficulty_value is Difficulty.HARD else 80
    curse_gate = copied_rng.next()
    copied_draws.append(curse_gate)
    curse_succeeded = curse_gate % curse_rate == 0
    curse_selector: int | None = None
    curse_mask = 0
    if curse_succeeded:
        curse_selector = copied_rng.next()
        copied_draws.append(curse_selector)
        choice = curse_selector % 6
        # Labyrinth (choice 0) is only valid on odd stages below Stage 8.
        if choice == 1:
            curse_mask = 0x04  # Lost
        elif choice == 2:
            curse_mask = 0x01  # Darkness
        elif choice == 3:
            curse_mask = 0x08  # Unknown
        elif choice == 4:
            curse_mask = 0x20  # Maze
        elif choice == 5:
            curse_mask = 0x40  # Blind

    third = level_rng.next()
    # floor(6 * 10 / 3) + 5 = 25, capped at 20 for both bit values.
    base_target = min((6 * 10) // 3 + 5 + (third & 1), 20)
    target_room_count = base_target
    if curse_mask & 0x04:
        target_room_count += 4

    difficulty_draw = copied_rng.next()
    copied_draws.append(difficulty_draw)
    if difficulty_value is Difficulty.HARD:
        target_room_count += 2 + (difficulty_draw & 1)

    fourth = level_rng.next()
    minimum, maximum = (
        (10, 15) if difficulty_value is Difficulty.HARD else (5, 10)
    )
    return Depths2TopologyInputs(
        stage_seed=stage_seed,
        level_rng_draws=(first, second, third, fourth),
        copied_rng_draws=tuple(copied_draws),
        curse_rate_denominator=curse_rate,
        curse_gate_succeeded=curse_succeeded,
        curse_selector=curse_selector,
        effective_curse_mask=curse_mask,
        is_xl=False,
        generator_seed=fourth,
        target_room_count=target_room_count,
        required_dead_ends=6,
        allowed_shapes_mask=ALL_GENERATED_ROOM_SHAPES_MASK,
        room_config_stage=7,
        room_config_min_difficulty=minimum,
        room_config_max_difficulty=maximum,
    )


@dataclass(frozen=True)
class Womb1TopologyInputs:
    """Binary-derived Stage 7 ORIGINAL inputs after Depths-II replay.

    Odd Stage 7 can satisfy the Labyrinth predicate (XL), so ``is_xl`` is
    possible.  ``target_room_count`` is capped at 20 before the XL/Lost
    modifiers, exactly like the confirmed Stage-5 pattern.
    """

    stage_seed: int
    level_rng_draws: tuple[int, int, int, int]
    copied_rng_draws: tuple[int, ...]
    curse_rate_denominator: int
    curse_gate_succeeded: bool
    curse_selector: int | None
    effective_curse_mask: int
    is_xl: bool
    generator_seed: int
    target_room_count: int
    required_dead_ends: int
    allowed_shapes_mask: int
    room_config_stage: int
    room_config_min_difficulty: int
    room_config_max_difficulty: int
    starting_grid_index: int = 84
    starting_shape: int = 1


def derive_womb1_topology_inputs(
    start_seed: int, difficulty: Difficulty | str
) -> Womb1TopologyInputs:
    """Derive canonical ORIGINAL Womb-I topology inputs from the run seed."""

    try:
        difficulty_value = Difficulty(difficulty)
    except ValueError as error:
        raise ValueError("difficulty must be NORMAL or HARD") from error

    stage_seed = get_initial_stage_seed(start_seed, 7)
    level_rng = IsaacRNG.game_constructor(stage_seed, LEVEL_RNG_SHIFT_INDEX)
    first = level_rng.next()
    second = level_rng.next()
    copied_rng = IsaacRNG(
        second, level_rng.shift1, level_rng.shift2, level_rng.shift3
    )
    copied_draws: list[int] = []
    curse_rate = 40 if difficulty_value is Difficulty.HARD else 80
    curse_gate = copied_rng.next()
    copied_draws.append(curse_gate)
    curse_succeeded = curse_gate % curse_rate == 0
    curse_selector: int | None = None
    curse_mask = 0
    if curse_succeeded:
        curse_selector = copied_rng.next()
        copied_draws.append(curse_selector)
        choice = curse_selector % 6
        if choice == 0:
            # Odd Stage 7 below Stage 8 accepts Labyrinth.
            curse_mask = 0x02
        elif choice == 1:
            curse_mask = 0x04  # Lost
        elif choice == 2:
            curse_mask = 0x01  # Darkness
        elif choice == 3:
            curse_mask = 0x08  # Unknown
        elif choice == 4:
            curse_mask = 0x20  # Maze
        elif choice == 5:
            curse_mask = 0x40  # Blind

    third = level_rng.next()
    # floor(7 * 10 / 3) + 5 = 28, capped at 20 for both bit values.
    base_target = min((7 * 10) // 3 + 5 + (third & 1), 20)
    is_xl = bool(curse_mask & 0x02)
    if is_xl:
        target_room_count = min((base_target * 18) // 10, 45)
    else:
        target_room_count = base_target
        if curse_mask & 0x04:
            target_room_count += 4

    difficulty_draw = copied_rng.next()
    copied_draws.append(difficulty_draw)
    if difficulty_value is Difficulty.HARD:
        target_room_count += 2 + (difficulty_draw & 1)

    fourth = level_rng.next()
    if is_xl:
        minimum, maximum = (
            (5, 15) if difficulty_value is Difficulty.HARD else (1, 10)
        )
    else:
        minimum, maximum = (
            (5, 10) if difficulty_value is Difficulty.HARD else (1, 5)
        )
    return Womb1TopologyInputs(
        stage_seed=stage_seed,
        level_rng_draws=(first, second, third, fourth),
        copied_rng_draws=tuple(copied_draws),
        curse_rate_denominator=curse_rate,
        curse_gate_succeeded=curse_succeeded,
        curse_selector=curse_selector,
        effective_curse_mask=curse_mask,
        is_xl=is_xl,
        generator_seed=fourth,
        target_room_count=target_room_count,
        required_dead_ends=7 if is_xl else 6,
        allowed_shapes_mask=ALL_GENERATED_ROOM_SHAPES_MASK,
        room_config_stage=10,
        room_config_min_difficulty=minimum,
        room_config_max_difficulty=maximum,
    )


@dataclass(frozen=True)
class Womb2TopologyInputs:
    """Binary-derived Stage 8 ORIGINAL inputs after Womb-I replay.

    Even Stage 8 never satisfies the Labyrinth predicate, so ``is_xl`` is
    always false.
    """

    stage_seed: int
    level_rng_draws: tuple[int, int, int, int]
    copied_rng_draws: tuple[int, ...]
    curse_rate_denominator: int
    curse_gate_succeeded: bool
    curse_selector: int | None
    effective_curse_mask: int
    is_xl: bool
    generator_seed: int
    target_room_count: int
    required_dead_ends: int
    allowed_shapes_mask: int
    room_config_stage: int
    room_config_min_difficulty: int
    room_config_max_difficulty: int
    starting_grid_index: int = 84
    starting_shape: int = 1


def derive_womb2_topology_inputs(
    start_seed: int, difficulty: Difficulty | str
) -> Womb2TopologyInputs:
    """Derive canonical ORIGINAL Womb-II topology inputs from the run seed."""

    try:
        difficulty_value = Difficulty(difficulty)
    except ValueError as error:
        raise ValueError("difficulty must be NORMAL or HARD") from error

    stage_seed = get_initial_stage_seed(start_seed, 8)
    level_rng = IsaacRNG.game_constructor(stage_seed, LEVEL_RNG_SHIFT_INDEX)
    first = level_rng.next()
    second = level_rng.next()
    copied_rng = IsaacRNG(
        second, level_rng.shift1, level_rng.shift2, level_rng.shift3
    )
    copied_draws: list[int] = []
    curse_rate = 40 if difficulty_value is Difficulty.HARD else 80
    curse_gate = copied_rng.next()
    copied_draws.append(curse_gate)
    curse_succeeded = curse_gate % curse_rate == 0
    curse_selector: int | None = None
    curse_mask = 0
    if curse_succeeded:
        curse_selector = copied_rng.next()
        copied_draws.append(curse_selector)
        choice = curse_selector % 6
        # Labyrinth (choice 0) is only valid on odd stages below Stage 8.
        # Womb II is even, so choice 0 consumes the selector and leaves the
        # curse empty.
        if choice == 1:
            curse_mask = 0x04  # Lost
        elif choice == 2:
            curse_mask = 0x01  # Darkness
        elif choice == 3:
            curse_mask = 0x08  # Unknown
        elif choice == 4:
            curse_mask = 0x20  # Maze
        elif choice == 5:
            curse_mask = 0x40  # Blind

    third = level_rng.next()
    # floor(8 * 10 / 3) + 5 = 31, capped at 20 for both bit values.
    base_target = min((8 * 10) // 3 + 5 + (third & 1), 20)
    target_room_count = base_target
    if curse_mask & 0x04:
        target_room_count += 4

    difficulty_draw = copied_rng.next()
    copied_draws.append(difficulty_draw)
    if difficulty_value is Difficulty.HARD:
        target_room_count += 2 + (difficulty_draw & 1)

    fourth = level_rng.next()
    minimum, maximum = (
        (10, 15) if difficulty_value is Difficulty.HARD else (5, 10)
    )
    return Womb2TopologyInputs(
        stage_seed=stage_seed,
        level_rng_draws=(first, second, third, fourth),
        copied_rng_draws=tuple(copied_draws),
        curse_rate_denominator=curse_rate,
        curse_gate_succeeded=curse_succeeded,
        curse_selector=curse_selector,
        effective_curse_mask=curse_mask,
        is_xl=False,
        generator_seed=fourth,
        target_room_count=target_room_count,
        required_dead_ends=6,
        allowed_shapes_mask=ALL_GENERATED_ROOM_SHAPES_MASK,
        room_config_stage=10,
        room_config_min_difficulty=minimum,
        room_config_max_difficulty=maximum,
    )
