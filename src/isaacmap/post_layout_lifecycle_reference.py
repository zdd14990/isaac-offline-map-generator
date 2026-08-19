"""Mechanical reference for the successful Basement I/II post-layout tail."""

from __future__ import annotations

from dataclasses import dataclass

from .room_config_reference import (
    RoomConfigEntryReference,
    RoomConfigKey,
    RoomConfigMutableStateReference,
    RoomConfigQueryReference,
    RoomConfigSelectionReference,
    f32,
    select_room_reference,
)


MASK = 0xFFFFFFFF
LEVEL_SHIFTS = (5, 9, 7)
DERIVED_SHIFTS = (11, 7, 12)
SHOP_SHIFTS = (3, 3, 26)
ANGEL_SHIFTS = (3, 3, 28)


@dataclass
class _ReferenceRNG:
    state: int
    shifts: tuple[int, int, int]

    def advance(self) -> int:
        value = self.state
        if value == 0:
            raise ValueError("reference RNG cannot advance zero")
        value ^= value >> self.shifts[0]
        value ^= (value << self.shifts[1]) & MASK
        value ^= value >> self.shifts[2]
        self.state = value & MASK
        return self.state

    def random_int(self, maximum: int) -> int:
        value = self.advance()
        return value % maximum if maximum else 0


@dataclass(frozen=True)
class ReferenceFixedDescriptor:
    grid_index: int
    room_type: int
    subtype: int
    seeds: tuple[int, int, int, int]
    selector_seed: int
    config: RoomConfigKey | None
    selection: RoomConfigSelectionReference


@dataclass(frozen=True)
class ReferencePostLayoutLifecycle:
    assignments: tuple[ReferenceFixedDescriptor, ...]
    transitions: tuple[tuple[int, str, int, int, str], ...]
    persistent_draws: int
    final_level: int
    weights: tuple[tuple[RoomConfigKey, float], ...]
    used_bits: tuple[int, ...]
    skipped: tuple[int, ...]


def _draw(
    rng: _ReferenceRNG,
    transitions: list[tuple[int, str, int, int, str]],
    rva: int,
    identity: str,
    reason: str,
) -> int:
    old = rng.state
    new = rng.advance()
    transitions.append((rva, identity, old, new, reason))
    return new


def _descriptor_seeds(
    rng: _ReferenceRNG,
    transitions: list[tuple[int, str, int, int, str]],
    rva: int,
    identity: str,
    grid_index: int,
) -> tuple[int, int, int, int]:
    generated: list[int] = []
    for index in range(3):
        generated.append(
            _draw(
                rng,
                transitions,
                rva,
                identity,
                f"GridIndex {grid_index} descriptor seed {index}",
            )
        )
    fourth_rng = _ReferenceRNG(generated[-1], DERIVED_SHIFTS)
    return generated[0], generated[1], generated[2], fourth_rng.advance()


def _select(
    *,
    grid_index: int,
    room_type: int,
    stage: int,
    subtype: int,
    helper_rva: int,
    selector_rva: int,
    rng: _ReferenceRNG,
    identity: str,
    transitions: list[tuple[int, str, int, int, str]],
    entries: tuple[RoomConfigEntryReference, ...],
    weights: RoomConfigMutableStateReference,
) -> ReferenceFixedDescriptor:
    seeds = _descriptor_seeds(
        rng, transitions, helper_rva, identity, grid_index
    )
    selector_seed = _draw(
        rng,
        transitions,
        selector_rva,
        identity,
        f"GridIndex {grid_index} RoomConfig selector seed",
    )
    selection = select_room_reference(
        entries,
        weights,
        RoomConfigQueryReference(
            selector_seed,
            True,
            stage,
            room_type,
            shape=13,
            min_variant=0,
            max_variant=MASK,
            min_difficulty=0 if stage == 13 else 1,
            max_difficulty=0 if stage == 13 else 10,
            required_doors=0,
            subtype=subtype,
            mode=0,
        ),
    )
    return ReferenceFixedDescriptor(
        grid_index,
        room_type,
        subtype,
        seeds,
        selector_seed,
        None if selection.selected is None else selection.selected.key,
        selection,
    )


def run_post_layout_lifecycle_reference(
    *,
    level_rng_state: int,
    entries: tuple[RoomConfigEntryReference, ...],
    room_config_weights: tuple[tuple[RoomConfigKey, float], ...],
    special_room_used_bits: tuple[int, ...] = (),
    level_stage: int = 1,
    stage_type: int = 0,
    room_config_stage: int = 1,
) -> ReferencePostLayoutLifecycle:
    if stage_type in (4, 5) and level_stage in (1, 2, 3, 4, 5, 6):
        expected_rcs = (
            ((level_stage - 1) & ~1) + 27
            if stage_type == 4
            else ((level_stage - 1) >> 1) * 2 + 28
        )
    else:
        expected_rcs = 1 + (level_stage - 1) // 2 * 3
    if level_stage not in (1, 2, 3, 4, 5, 6, 7, 8) or stage_type not in (0, 4, 5) or room_config_stage != expected_rcs:
        raise ValueError("reference state is outside the canonical ORIGINAL lifecycle profile")
    level = _ReferenceRNG(level_rng_state, LEVEL_SHIFTS)
    weights = RoomConfigMutableStateReference(dict(room_config_weights))
    transitions: list[tuple[int, str, int, int, str]] = []
    assignments: list[ReferenceFixedDescriptor] = []
    used_bits = set(special_room_used_bits)

    # Reproduce the two used-bit bonuses and their one-shot clearing before
    # calculating the canonical 1/3 door chance. Both stage predicates are
    # false on LevelStage 1/2, but the probability arithmetic and Level draws
    # still happen in the binary.
    chance_base = f32(1.0)
    if 30 in used_bits:
        used_bits.remove(30)
        chance_base = f32(chance_base + f32(0.1))
    if 31 in used_bits:
        used_bits.remove(31)
        chance_base = f32(chance_base + f32(0.02))
    chance = f32(f32(chance_base - f32(0.0)) * f32(1.0 / 3.0))
    for rva, reason in (
        (0x0033D2B8, "first post-layout door chance"),
        (0x0033D363, "second post-layout door chance"),
    ):
        value = _draw(
            level, transitions, rva, "Level._generationRNG(index=35)", reason
        )
        _ = f32(f32(float(value)) * f32(2.3283061589829401e-10)) < chance
    specs = (
        (-2, 3, 0, -1, 0x0033D3FB, 0x0033D40C),
        (-6, 22, 0, -1, 0x0033D456, 0x0033D467),
        (-4, 16, 0, -1, 0x0033D4B1, 0x0033D4C2),
        (-5, 17, 0, -1, 0x0033D50C, 0x0033D554),
        (-7, 5, 0, 55, 0x0033D59E, 0x0033D5AF),
        (-8, 1, 13, 1, 0x0033D64F, 0x0033D660),
    )
    for grid, room_type, stage, subtype, helper, selector in specs:
        assignments.append(
            _select(
                grid_index=grid,
                room_type=room_type,
                stage=stage,
                subtype=subtype,
                helper_rva=helper,
                selector_rva=selector,
                rng=level,
                identity="Level._generationRNG(index=35)",
                transitions=transitions,
                entries=entries,
                weights=weights,
            )
        )

    shop_seed = _draw(
        level,
        transitions,
        0x0033D731,
        "Level._generationRNG(index=35)",
        "GridIndex -13 private Shop stream seed",
    )
    shop = _ReferenceRNG(shop_seed, SHOP_SHIFTS)
    subtype = shop.random_int(1) + shop.random_int(1)
    assignments.append(
        _select(
            grid_index=-13,
            room_type=2,
            stage=0,
            subtype=subtype,
            helper_rva=0x0033D78B,
            selector_rva=0x0033D7A0,
            rng=shop,
            identity="GridIndex -13 private RNG(index=19)",
            transitions=transitions,
            entries=entries,
            weights=weights,
        )
    )

    angel_seed = _draw(
        level,
        transitions,
        0x0033D7E9,
        "Level._generationRNG(index=35)",
        "GridIndex -18 private Angel stream seed",
    )
    angel = _ReferenceRNG(angel_seed, ANGEL_SHIFTS)
    assignments.append(
        _select(
            grid_index=-18,
            room_type=15,
            stage=0,
            subtype=1,
            helper_rva=0x0033D823,
            selector_rva=0x0033D838,
            rng=angel,
            identity="GridIndex -18 private RNG(index=20)",
            transitions=transitions,
            entries=entries,
            weights=weights,
        )
    )

    persistent = sum(item[1] == "Level._generationRNG(index=35)" for item in transitions)
    return ReferencePostLayoutLifecycle(
        tuple(assignments),
        tuple(transitions),
        persistent,
        level.state,
        tuple(sorted(weights.weights.items())),
        tuple(sorted(used_bits)),
        (-9, -10),
    )
