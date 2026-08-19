"""Mechanical reference for canonical ORIGINAL later-floor initialization."""

from __future__ import annotations

from dataclasses import dataclass

from .stage_seed import get_initial_stage_seed


MASK = 0xFFFFFFFF
LEVEL_SHIFTS = (5, 9, 7)


def _advance(value: int) -> int:
    if value == 0:
        raise ValueError("reference RNG cannot advance zero")
    value ^= value >> LEVEL_SHIFTS[0]
    value ^= (value << LEVEL_SHIFTS[1]) & MASK
    value ^= value >> LEVEL_SHIFTS[2]
    return value & MASK


@dataclass(frozen=True)
class ReferenceBasement2TopologyInputs:
    stage_seed: int
    level_draws: tuple[int, int, int, int]
    copied_draws: tuple[int, ...]
    curse_rate: int
    curse_gate: bool
    curse_selector: int | None
    curse_mask: int
    generator_seed: int
    target: int
    dead_ends: int
    shapes: int
    minimum_difficulty: int
    maximum_difficulty: int


@dataclass(frozen=True)
class ReferenceCaves1TopologyInputs:
    stage_seed: int
    level_draws: tuple[int, int, int, int]
    copied_draws: tuple[int, ...]
    curse_rate: int
    curse_gate: bool
    curse_selector: int | None
    curse_mask: int
    is_xl: bool
    generator_seed: int
    target: int
    dead_ends: int
    shapes: int
    room_config_stage: int
    minimum_difficulty: int
    maximum_difficulty: int


def derive_basement2_topology_inputs_reference(
    start_seed: int, difficulty: str
) -> ReferenceBasement2TopologyInputs:
    if difficulty not in ("NORMAL", "HARD"):
        raise ValueError("difficulty must be NORMAL or HARD")
    stage_seed = get_initial_stage_seed(start_seed, 2)
    first = _advance(stage_seed)
    second = _advance(first)
    copied = second
    copied_values: list[int] = []
    copied = _advance(copied)
    copied_values.append(copied)
    rate = 40 if difficulty == "HARD" else 80
    gate = copied % rate == 0
    selector = None
    curse = 0
    if gate:
        copied = _advance(copied)
        copied_values.append(copied)
        selector = copied
        choice = copied % 6
        if choice == 1:
            curse = 4
        elif choice == 2:
            curse = 1
        elif choice == 3:
            curse = 8
        elif choice == 4:
            curse = 0x20
        elif choice == 5:
            curse = 0x40
    third = _advance(second)
    target = 11 + (third & 1)
    if curse & 4:
        target += 4
    if difficulty == "HARD":
        copied = _advance(copied)
        copied_values.append(copied)
        target += 2 + (copied & 1)
    fourth = _advance(third)
    minimum, maximum = (10, 15) if difficulty == "HARD" else (5, 10)
    return ReferenceBasement2TopologyInputs(
        stage_seed,
        (first, second, third, fourth),
        tuple(copied_values),
        rate,
        gate,
        selector,
        curse,
        fourth,
        target,
        6,
        0x1FFE,
        minimum,
        maximum,
    )


def derive_caves1_topology_inputs_reference(
    start_seed: int, difficulty: str
) -> ReferenceCaves1TopologyInputs:
    if difficulty not in ("NORMAL", "HARD"):
        raise ValueError("difficulty must be NORMAL or HARD")
    stage_seed = get_initial_stage_seed(start_seed, 3)
    first = _advance(stage_seed)
    second = _advance(first)
    copied = _advance(second)
    copied_values = [copied]
    rate = 40 if difficulty == "HARD" else 80
    gate = copied % rate == 0
    selector = None
    curse = 0
    if gate:
        copied = _advance(copied)
        copied_values.append(copied)
        selector = copied
        curse = (2, 4, 1, 8, 0x20, 0x40)[copied % 6]
    third = _advance(second)
    target = 15 + (third & 1)
    xl = bool(curse & 2)
    if xl:
        target = min(int(float(target) * 1.8), 45)
    elif curse & 4:
        target += 4
    copied = _advance(copied)
    copied_values.append(copied)
    if difficulty == "HARD":
        target += 2 + (copied & 1)
    fourth = _advance(third)
    if xl:
        minimum, maximum = (5, 15) if difficulty == "HARD" else (1, 10)
    else:
        minimum, maximum = (5, 10) if difficulty == "HARD" else (1, 5)
    return ReferenceCaves1TopologyInputs(
        stage_seed,
        (first, second, third, fourth),
        tuple(copied_values),
        rate,
        gate,
        selector,
        curse,
        xl,
        fourth,
        target,
        7 if xl else 6,
        0x1FFE,
        4,
        minimum,
        maximum,
    )


@dataclass(frozen=True)
class ReferenceCaves2TopologyInputs:
    stage_seed: int
    level_draws: tuple[int, int, int, int]
    copied_draws: tuple[int, ...]
    curse_rate: int
    curse_gate: bool
    curse_selector: int | None
    curse_mask: int
    is_xl: bool
    generator_seed: int
    target: int
    dead_ends: int
    shapes: int
    room_config_stage: int
    minimum_difficulty: int
    maximum_difficulty: int


def derive_caves2_topology_inputs_reference(
    start_seed: int, difficulty: str
) -> ReferenceCaves2TopologyInputs:
    if difficulty not in ("NORMAL", "HARD"):
        raise ValueError("difficulty must be NORMAL or HARD")
    stage_seed = get_initial_stage_seed(start_seed, 4)
    first = _advance(stage_seed)
    second = _advance(first)
    copied = second
    copied_values: list[int] = []
    copied = _advance(copied)
    copied_values.append(copied)
    rate = 40 if difficulty == "HARD" else 80
    gate = copied % rate == 0
    selector = None
    curse = 0
    if gate:
        copied = _advance(copied)
        copied_values.append(copied)
        selector = copied
        choice = copied % 6
        # Even Stage 4: Labyrinth (choice 0) is not valid and leaves curse 0.
        if choice == 1:
            curse = 4
        elif choice == 2:
            curse = 1
        elif choice == 3:
            curse = 8
        elif choice == 4:
            curse = 0x20
        elif choice == 5:
            curse = 0x40
    third = _advance(second)
    target = 18 + (third & 1)
    if curse & 4:
        target += 4
    copied = _advance(copied)
    copied_values.append(copied)
    if difficulty == "HARD":
        target += 2 + (copied & 1)
    fourth = _advance(third)
    minimum, maximum = (10, 15) if difficulty == "HARD" else (5, 10)
    return ReferenceCaves2TopologyInputs(
        stage_seed,
        (first, second, third, fourth),
        tuple(copied_values),
        rate,
        gate,
        selector,
        curse,
        False,
        fourth,
        target,
        6,
        0x1FFE,
        4,
        minimum,
        maximum,
    )


@dataclass(frozen=True)
class ReferenceDepths1TopologyInputs:
    stage_seed: int
    level_draws: tuple[int, int, int, int]
    copied_draws: tuple[int, ...]
    curse_rate: int
    curse_gate: bool
    curse_selector: int | None
    curse_mask: int
    is_xl: bool
    generator_seed: int
    target: int
    dead_ends: int
    shapes: int
    room_config_stage: int
    minimum_difficulty: int
    maximum_difficulty: int


def derive_depths1_topology_inputs_reference(
    start_seed: int, difficulty: str
) -> ReferenceDepths1TopologyInputs:
    if difficulty not in ("NORMAL", "HARD"):
        raise ValueError("difficulty must be NORMAL or HARD")
    stage_seed = get_initial_stage_seed(start_seed, 5)
    first = _advance(stage_seed)
    second = _advance(first)
    copied = _advance(second)
    copied_values = [copied]
    rate = 40 if difficulty == "HARD" else 80
    gate = copied % rate == 0
    selector = None
    curse = 0
    if gate:
        copied = _advance(copied)
        copied_values.append(copied)
        selector = copied
        curse = (2, 4, 1, 8, 0x20, 0x40)[copied % 6]
    third = _advance(second)
    target = min(21 + (third & 1), 20)
    xl = bool(curse & 2)
    if xl:
        target = min(int(float(target) * 1.8), 45)
    elif curse & 4:
        target += 4
    copied = _advance(copied)
    copied_values.append(copied)
    if difficulty == "HARD":
        target += 2 + (copied & 1)
    fourth = _advance(third)
    if xl:
        minimum, maximum = (5, 15) if difficulty == "HARD" else (1, 10)
    else:
        minimum, maximum = (5, 10) if difficulty == "HARD" else (1, 5)
    return ReferenceDepths1TopologyInputs(
        stage_seed,
        (first, second, third, fourth),
        tuple(copied_values),
        rate,
        gate,
        selector,
        curse,
        xl,
        fourth,
        target,
        7 if xl else 6,
        0x1FFE,
        7,
        minimum,
        maximum,
    )


@dataclass(frozen=True)
class ReferenceDepths2TopologyInputs:
    stage_seed: int
    level_draws: tuple[int, int, int, int]
    copied_draws: tuple[int, ...]
    curse_rate: int
    curse_gate: bool
    curse_selector: int | None
    curse_mask: int
    is_xl: bool
    generator_seed: int
    target: int
    dead_ends: int
    shapes: int
    room_config_stage: int
    minimum_difficulty: int
    maximum_difficulty: int


def derive_depths2_topology_inputs_reference(
    start_seed: int, difficulty: str
) -> ReferenceDepths2TopologyInputs:
    if difficulty not in ("NORMAL", "HARD"):
        raise ValueError("difficulty must be NORMAL or HARD")
    stage_seed = get_initial_stage_seed(start_seed, 6)
    first = _advance(stage_seed)
    second = _advance(first)
    copied = second
    copied_values: list[int] = []
    copied = _advance(copied)
    copied_values.append(copied)
    rate = 40 if difficulty == "HARD" else 80
    gate = copied % rate == 0
    selector = None
    curse = 0
    if gate:
        copied = _advance(copied)
        copied_values.append(copied)
        selector = copied
        choice = copied % 6
        if choice == 1:
            curse = 4
        elif choice == 2:
            curse = 1
        elif choice == 3:
            curse = 8
        elif choice == 4:
            curse = 0x20
        elif choice == 5:
            curse = 0x40
    third = _advance(second)
    target = min(25 + (third & 1), 20)
    if curse & 4:
        target += 4
    copied = _advance(copied)
    copied_values.append(copied)
    if difficulty == "HARD":
        target += 2 + (copied & 1)
    fourth = _advance(third)
    minimum, maximum = (10, 15) if difficulty == "HARD" else (5, 10)
    return ReferenceDepths2TopologyInputs(
        stage_seed,
        (first, second, third, fourth),
        tuple(copied_values),
        rate,
        gate,
        selector,
        curse,
        False,
        fourth,
        target,
        6,
        0x1FFE,
        7,
        minimum,
        maximum,
    )


@dataclass(frozen=True)
class ReferenceWomb1TopologyInputs:
    stage_seed: int
    level_draws: tuple[int, int, int, int]
    copied_draws: tuple[int, ...]
    curse_rate: int
    curse_gate: bool
    curse_selector: int | None
    curse_mask: int
    is_xl: bool
    generator_seed: int
    target: int
    dead_ends: int
    shapes: int
    room_config_stage: int
    minimum_difficulty: int
    maximum_difficulty: int


def derive_womb1_topology_inputs_reference(
    start_seed: int, difficulty: str
) -> ReferenceWomb1TopologyInputs:
    if difficulty not in ("NORMAL", "HARD"):
        raise ValueError("difficulty must be NORMAL or HARD")
    stage_seed = get_initial_stage_seed(start_seed, 7)
    first = _advance(stage_seed)
    second = _advance(first)
    copied = second
    copied_values: list[int] = []
    copied = _advance(copied)
    copied_values.append(copied)
    rate = 40 if difficulty == "HARD" else 80
    gate = copied % rate == 0
    selector = None
    curse = 0
    if gate:
        copied = _advance(copied)
        copied_values.append(copied)
        selector = copied
        choice = copied % 6
        if choice == 0:
            # Odd Stage 7 below Stage 8 accepts Labyrinth.
            curse = 2
        elif choice == 1:
            curse = 4
        elif choice == 2:
            curse = 1
        elif choice == 3:
            curse = 8
        elif choice == 4:
            curse = 0x20
        elif choice == 5:
            curse = 0x40
    third = _advance(second)
    base = min(28 + (third & 1), 20)
    is_xl = bool(curse & 2)
    if is_xl:
        target = min(base * 18 // 10, 45)
    else:
        target = base
        if curse & 4:
            target += 4
    copied = _advance(copied)
    copied_values.append(copied)
    if difficulty == "HARD":
        target += 2 + (copied & 1)
    fourth = _advance(third)
    if is_xl:
        minimum, maximum = (5, 15) if difficulty == "HARD" else (1, 10)
    else:
        minimum, maximum = (5, 10) if difficulty == "HARD" else (1, 5)
    return ReferenceWomb1TopologyInputs(
        stage_seed,
        (first, second, third, fourth),
        tuple(copied_values),
        rate,
        gate,
        selector,
        curse,
        is_xl,
        fourth,
        target,
        7 if is_xl else 6,
        0x1FFE,
        10,
        minimum,
        maximum,
    )


@dataclass(frozen=True)
class ReferenceWomb2TopologyInputs:
    stage_seed: int
    level_draws: tuple[int, int, int, int]
    copied_draws: tuple[int, ...]
    curse_rate: int
    curse_gate: bool
    curse_selector: int | None
    curse_mask: int
    is_xl: bool
    generator_seed: int
    target: int
    dead_ends: int
    shapes: int
    room_config_stage: int
    minimum_difficulty: int
    maximum_difficulty: int


def derive_womb2_topology_inputs_reference(
    start_seed: int, difficulty: str
) -> ReferenceWomb2TopologyInputs:
    if difficulty not in ("NORMAL", "HARD"):
        raise ValueError("difficulty must be NORMAL or HARD")
    stage_seed = get_initial_stage_seed(start_seed, 8)
    first = _advance(stage_seed)
    second = _advance(first)
    copied = second
    copied_values: list[int] = []
    copied = _advance(copied)
    copied_values.append(copied)
    rate = 40 if difficulty == "HARD" else 80
    gate = copied % rate == 0
    selector = None
    curse = 0
    if gate:
        copied = _advance(copied)
        copied_values.append(copied)
        selector = copied
        choice = copied % 6
        # Labyrinth (choice 0) is only valid on odd stages below Stage 8.
        # Womb II is even, so choice 0 consumes the selector and is empty.
        if choice == 1:
            curse = 4
        elif choice == 2:
            curse = 1
        elif choice == 3:
            curse = 8
        elif choice == 4:
            curse = 0x20
        elif choice == 5:
            curse = 0x40
    third = _advance(second)
    base = min(31 + (third & 1), 20)
    target = base
    if curse & 4:
        target += 4
    copied = _advance(copied)
    copied_values.append(copied)
    if difficulty == "HARD":
        target += 2 + (copied & 1)
    fourth = _advance(third)
    minimum, maximum = (10, 15) if difficulty == "HARD" else (5, 10)
    return ReferenceWomb2TopologyInputs(
        stage_seed,
        (first, second, third, fourth),
        tuple(copied_values),
        rate,
        gate,
        selector,
        curse,
        False,
        fourth,
        target,
        6,
        0x1FFE,
        10,
        minimum,
        maximum,
    )
