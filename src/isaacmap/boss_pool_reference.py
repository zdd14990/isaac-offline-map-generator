"""Mechanical BossPool reference for the frozen executable profile.

This module intentionally mirrors the x86 loops recovered at RVAs
0x000218E0 and 0x00022830.  It is a research component, not a complete public
floor generator.  In particular, ``pick_fresh_basement_boss_reference`` is
scoped to a fresh vanilla Basement pool with no achievement-gated special
boss override and no pre-existing removed/level-blacklist bits.
"""

from __future__ import annotations

from dataclasses import dataclass
import struct
from typing import Iterable

from .boss_pool import fixed_boss_for_level


PROFILE_SHA256 = "3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b"
UINT32_MASK = 0xFFFFFFFF
POOL_COUNT = 37
MASTER_SHIFT_INDEX = 26
MASTER_SHIFTS = (3, 13, 7)
POOL_SHIFT_INDEX = 17
POOL_SHIFTS = (2, 21, 9)
BASEMENT_POOL_INDEX = 1
CAVES_POOL_INDEX = 4
DEPTHS_POOL_INDEX = 7
WOMB_POOL_INDEX = 10
DOWNPOUR_POOL_INDEX = 27
DROSS_POOL_INDEX = 28
MINES_POOL_INDEX = 29
ASHPIT_POOL_INDEX = 30
MAUSOLEUM_POOL_INDEX = 31
GEHENNA_POOL_INDEX = 32


def _f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


_RANDOM_FLOAT_SCALE = struct.unpack("<f", struct.pack("<I", 0x2F7FFFFE))[0]


def _advance(state: int, shifts: tuple[int, int, int]) -> int:
    if state == 0:
        raise ValueError("the profiled binary asserts before drawing a zero RNG state")
    state ^= state >> shifts[0]
    state ^= (state << shifts[1]) & UINT32_MASK
    state ^= state >> shifts[2]
    return state & UINT32_MASK


def _random_float_from_state(state: int) -> float:
    unsigned_as_float = _f32(float(state & UINT32_MASK))
    return _f32(unsigned_as_float * _RANDOM_FLOAT_SCALE)


@dataclass(frozen=True)
class BossPoolEntryReference:
    boss_id: int
    weight: float
    initial_weight: float
    achievement: int = -1
    alternate_boss_id: int = 0


@dataclass(frozen=True)
class BossPoolDrawReference:
    sequence: int
    binary_rva: int
    object_identity: str
    shift_index: int
    shifts: tuple[int, int, int]
    pre_state: int
    post_state: int
    reason: str
    usage: str


@dataclass(frozen=True)
class FreshBossSelectionReference:
    boss_id: int
    pool_index: int
    shuffled_entry_ids: tuple[int, ...]
    initial_pool_state: int
    persistent_pool_state: int
    local_selector_final_state: int
    level_blacklist: frozenset[int]
    ledger: tuple[BossPoolDrawReference, ...]


@dataclass(frozen=True)
class BossPoolRuntimeSelectionReference:
    boss_id: int
    selected_entry_id: int
    pool_index: int
    persistent_pre_state: int
    persistent_post_state: int
    local_selector_final_state: int
    ledger: tuple[BossPoolDrawReference, ...]
    repick_count: int = 0
    fallback_used: bool = False
    pool_reset_count: int = 0


@dataclass
class BossPoolRuntimeReference:
    game_start_seed: int
    pool_seeds: tuple[int, ...]
    pool_states: list[int]
    shuffled_entries: dict[int, tuple[BossPoolEntryReference, ...]]
    removed: set[int]
    level_blacklist: set[int]

    @classmethod
    def fresh_basement(
        cls, game_start_seed: int,
        basement_entries: tuple[BossPoolEntryReference, ...],
    ) -> "BossPoolRuntimeReference":
        seeds = derive_pool_seeds_reference(game_start_seed)
        return cls(
            game_start_seed, seeds, list(seeds),
            {BASEMENT_POOL_INDEX: shuffle_entries_reference(
                basement_entries, seeds[BASEMENT_POOL_INDEX]
            )},
            set(), set(),
        )

    @classmethod
    def resume_canonical_basement(
        cls,
        game_start_seed: int,
        basement_entries: tuple[BossPoolEntryReference, ...],
        *,
        pool_state: int,
        removed: tuple[int, ...] | set[int],
    ) -> "BossPoolRuntimeReference":
        result = cls.fresh_basement(game_start_seed, basement_entries)
        result.pool_states[BASEMENT_POOL_INDEX] = pool_state
        result.removed.update(removed)
        return result

    @classmethod
    def resume_canonical_caves(
        cls,
        game_start_seed: int,
        caves_entries: tuple[BossPoolEntryReference, ...],
        *,
        pool_state: int,
        removed: tuple[int, ...] | set[int],
    ) -> "BossPoolRuntimeReference":
        seeds = derive_pool_seeds_reference(game_start_seed)
        result = cls(
            game_start_seed,
            seeds,
            list(seeds),
            {
                CAVES_POOL_INDEX: shuffle_entries_reference(
                    caves_entries, seeds[CAVES_POOL_INDEX]
                )
            },
            set(removed),
            set(),
        )
        result.pool_states[CAVES_POOL_INDEX] = pool_state
        return result

    @classmethod
    def resume_canonical_depths(
        cls,
        game_start_seed: int,
        depths_entries: tuple[BossPoolEntryReference, ...],
        *,
        pool_state: int,
        removed: tuple[int, ...] | set[int],
    ) -> "BossPoolRuntimeReference":
        seeds = derive_pool_seeds_reference(game_start_seed)
        result = cls(
            game_start_seed,
            seeds,
            list(seeds),
            {
                DEPTHS_POOL_INDEX: shuffle_entries_reference(
                    depths_entries, seeds[DEPTHS_POOL_INDEX]
                )
            },
            set(removed),
            set(),
        )
        result.pool_states[DEPTHS_POOL_INDEX] = pool_state
        return result

    @classmethod
    def resume_canonical_womb(
        cls,
        game_start_seed: int,
        womb_entries: tuple[BossPoolEntryReference, ...],
        *,
        pool_state: int,
        removed: tuple[int, ...] | set[int],
    ) -> "BossPoolRuntimeReference":
        seeds = derive_pool_seeds_reference(game_start_seed)
        result = cls(
            game_start_seed,
            seeds,
            list(seeds),
            {
                WOMB_POOL_INDEX: shuffle_entries_reference(
                    womb_entries, seeds[WOMB_POOL_INDEX]
                )
            },
            set(removed),
            set(),
        )
        result.pool_states[WOMB_POOL_INDEX] = pool_state
        return result

    def begin_attempt(self) -> None:
        self.level_blacklist.clear()

    def commit_floor(self) -> None:
        self.removed |= self.level_blacklist
        self.level_blacklist.clear()

    def select_fresh_basement_profile(self) -> BossPoolRuntimeSelectionReference:
        return self.select_canonical_basement_profile()

    @staticmethod
    def _pick_canonical_entry(
        entries: tuple[BossPoolEntryReference, ...],
        target: float,
        total: float,
        removed: set[int],
        level_blacklist: set[int],
    ) -> tuple[BossPoolEntryReference | None, int, bool]:
        remapped = 0
        countdown = 9
        while countdown >= 0:
            cumulative = _f32(0.0)
            hit_index = -1
            for index, entry in enumerate(entries):
                before = cumulative
                cumulative = _f32(cumulative + _f32(entry.weight))
                if not target < cumulative:
                    continue
                hit_index = index
                if (
                    _f32(entry.initial_weight) > 0.0
                    and target < _f32(_f32(entry.initial_weight) + before)
                    and entry.achievement < 0
                    and entry.boss_id not in removed
                    and entry.boss_id not in level_blacklist
                ):
                    return entry, remapped, False
                if countdown == 0:
                    cursor = (index + 1) % len(entries)
                    while cursor != index:
                        candidate = entries[cursor]
                        if (
                            _f32(candidate.initial_weight) > 0.0
                            and candidate.achievement < 0
                            and candidate.boss_id not in removed
                            and candidate.boss_id not in level_blacklist
                        ):
                            return candidate, remapped, True
                        cursor = (cursor + 1) % len(entries)
                    return None, remapped, True
                numerator = _f32(cumulative - target)
                ratio = _f32(numerator / _f32(entry.weight))
                target = _f32(ratio * total)
                remapped += 1
                break
            countdown -= 1
            if hit_index < 0:
                continue
        return None, remapped, False

    def select_canonical_basement_profile(self) -> BossPoolRuntimeSelectionReference:
        return self._select_canonical_pool(BASEMENT_POOL_INDEX)

    def select_canonical_caves_profile(self) -> BossPoolRuntimeSelectionReference:
        return self._select_canonical_pool(CAVES_POOL_INDEX)

    def select_canonical_stage(self, room_config_stage: int) -> BossPoolRuntimeSelectionReference:
        return self._select_canonical_pool(room_config_stage)

    def select_floor_boss(
        self,
        level_stage: int,
        stage_type: int,
        room_config_stage: int,
    ) -> BossPoolRuntimeSelectionReference:
        """Mirror ``Level::select_boss_id``: fixed switch first, pool otherwise."""

        fixed = fixed_boss_for_level(level_stage, stage_type)
        if fixed is None:
            return self._select_canonical_pool(room_config_stage)
        state = self.pool_states[room_config_stage]
        return BossPoolRuntimeSelectionReference(
            boss_id=fixed,
            selected_entry_id=fixed,
            pool_index=room_config_stage,
            persistent_pre_state=state,
            persistent_post_state=state,
            local_selector_final_state=state,
            ledger=(),
            repick_count=0,
            fallback_used=False,
            pool_reset_count=0,
        )

    def _select_canonical_pool(
        self, pool_index: int
    ) -> BossPoolRuntimeSelectionReference:
        entries = self.shuffled_entries[pool_index]
        state = self.pool_states[pool_index]
        initial = state
        ledger: list[BossPoolDrawReference] = []
        for index in range(7):
            post = _advance(state, POOL_SHIFTS)
            ledger.append(BossPoolDrawReference(
                index, 0x00022830, f"BossPools.pool[{pool_index}]._rng",
                POOL_SHIFT_INDEX, POOL_SHIFTS, state, post,
                "ordinary Level::select_boss_id pre-roll", f"pre-roll {index + 1}/7",
            ))
            state = post
        self.pool_states[pool_index] = state
        total = _f32(0.0)
        for entry in entries:
            total = _f32(total + entry.weight)
        selected = None
        local_state = state
        total_repicks = 0
        fallback_used = False
        pool_resets = 0
        for outer in range(10):
            local_post = _advance(local_state, POOL_SHIFTS)
            ledger.append(BossPoolDrawReference(
                7 + outer, 0x00022D04,
                f"stack_copy(BossPools.pool[{pool_index}]._rng)",
                POOL_SHIFT_INDEX, POOL_SHIFTS, local_state, local_post,
                "ordinary weighted BossPool::PickBoss", "binary32 threshold",
            ))
            local_state = local_post
            target = _f32(_random_float_from_state(local_post) * total)
            selected, repicks, fallback = self._pick_canonical_entry(
                entries, target, total, self.removed, self.level_blacklist
            )
            total_repicks += repicks
            fallback_used |= fallback
            if selected is not None:
                break
            for entry in entries:
                self.removed.discard(entry.boss_id)
                self.level_blacklist.discard(entry.boss_id)
            pool_resets += 1
        if selected is None:
            return BossPoolRuntimeSelectionReference(
                1, 1, pool_index, initial, state, local_state, tuple(ledger),
                total_repicks, fallback_used, pool_resets,
            )
        self.level_blacklist.add(selected.boss_id)
        boss_id = -selected.alternate_boss_id if selected.alternate_boss_id else selected.boss_id
        return BossPoolRuntimeSelectionReference(
            boss_id, selected.boss_id, pool_index, initial, state, local_state,
            tuple(ledger), total_repicks, fallback_used, pool_resets,
        )


class _MT19937Reference:
    """Literal port of RVAs 0x004FD3C0 and 0x004FD410."""

    def __init__(self, seed: int) -> None:
        self.words = [0] * 624
        self.words[0] = seed & UINT32_MASK
        index = 1
        while index < 624:
            previous = self.words[index - 1]
            self.words[index] = (
                ((previous >> 30) ^ previous) * 0x6C078965 + index
            ) & UINT32_MASK
            index += 1
        self.index = 624

    def next(self) -> int:
        if self.index >= 624:
            index = 0
            while index < 227:
                mixed = (
                    ((self.words[index + 1] ^ self.words[index]) & 0x7FFFFFFF)
                    ^ self.words[index]
                )
                self.words[index] = (
                    self.words[index + 397]
                    ^ (mixed >> 1)
                    ^ (0x9908B0DF if mixed & 1 else 0)
                ) & UINT32_MASK
                index += 1
            while index < 623:
                mixed = (
                    ((self.words[index + 1] ^ self.words[index]) & 0x7FFFFFFF)
                    ^ self.words[index]
                )
                self.words[index] = (
                    self.words[index - 227]
                    ^ (mixed >> 1)
                    ^ (0x9908B0DF if mixed & 1 else 0)
                ) & UINT32_MASK
                index += 1
            mixed = (
                ((self.words[0] ^ self.words[623]) & 0x7FFFFFFF)
                ^ self.words[623]
            )
            self.words[623] = (
                self.words[396]
                ^ (mixed >> 1)
                ^ (0x9908B0DF if mixed & 1 else 0)
            ) & UINT32_MASK
            self.index = 0

        value = self.words[self.index]
        self.index += 1
        value ^= value >> 11
        value ^= (value & 0xFF3A58AD) << 7
        value &= UINT32_MASK
        value ^= (value & 0xFFFFDF8C) << 15
        value &= UINT32_MASK
        return (value ^ (value >> 18)) & UINT32_MASK


def derive_pool_seeds_reference(game_start_seed: int) -> tuple[int, ...]:
    """Derive pool 0..36 by one chained master advance per pool."""

    state = game_start_seed & UINT32_MASK
    result: list[int] = []
    remaining = 0x25
    while remaining != 0:
        state = _advance(state, MASTER_SHIFTS)
        result.append(state)
        remaining -= 1
    return tuple(result)


def shuffle_entries_reference(
    entries: Iterable[BossPoolEntryReference], seed: int
) -> tuple[BossPoolEntryReference, ...]:
    """Init-time MT19937 Fisher-Yates used independently for one pool."""

    values = list(entries)
    if not values:
        return ()
    mt = _MT19937Reference(seed)
    current_count = len(values)
    current_index = current_count - 1
    while current_index > 0:
        other_index = mt.next() % current_count
        if current_index != other_index:
            values[current_index], values[other_index] = (
                values[other_index],
                values[current_index],
            )
        current_index -= 1
        current_count -= 1
    return tuple(values)


def pick_fresh_basement_boss_reference(
    game_start_seed: int,
    entries: Iterable[BossPoolEntryReference],
) -> FreshBossSelectionReference:
    """Fresh Basement baseline through the ordinary weighted-pick path.

    The seven persistent draws occur even when all optional special-boss
    branches are disabled.  The subsequent weighted-pick draw advances a
    stack copy and therefore is deliberately absent from the persistent pool
    state.
    """

    pool_seeds = derive_pool_seeds_reference(game_start_seed)
    initial_state = pool_seeds[BASEMENT_POOL_INDEX]
    shuffled = shuffle_entries_reference(entries, initial_state)
    if not shuffled:
        raise ValueError("the Basement boss pool must not be empty")

    draw_rvas = (0x000229F8, 0x00022A02, 0x00022A0D, 0x00022A18,
                 0x00022A23, 0x00022A2E, 0x00022A36)
    state = initial_state
    ledger: list[BossPoolDrawReference] = []
    for sequence, rva in enumerate(draw_rvas):
        pre = state
        state = _advance(state, POOL_SHIFTS)
        ledger.append(
            BossPoolDrawReference(
                sequence=sequence,
                binary_rva=rva,
                object_identity="BossPools.pool[1]._rng",
                shift_index=POOL_SHIFT_INDEX,
                shifts=POOL_SHIFTS,
                pre_state=pre,
                post_state=state,
                reason="Level::select_boss_id optional-special pre-roll",
                usage=(
                    "special boss predicate input"
                    if sequence < 5
                    else "unconditionally consumed/discarded pre-roll"
                ),
            )
        )

    persistent_state = state
    local_pre = state
    state = _advance(state, POOL_SHIFTS)
    total_weight = _f32(0.0)
    for entry in shuffled:
        total_weight = _f32(total_weight + _f32(entry.weight))
    target = _f32(_random_float_from_state(state) * total_weight)
    ledger.append(
        BossPoolDrawReference(
            sequence=len(ledger),
            binary_rva=0x00022D04,
            object_identity="Level::select_boss_id.stack_copy(pool[1]._rng)",
            shift_index=POOL_SHIFT_INDEX,
            shifts=POOL_SHIFTS,
            pre_state=local_pre,
            post_state=state,
            reason="ordinary weighted BossPool::PickBoss",
            usage="binary32 unit float multiplied by pool total weight",
        )
    )

    cumulative = _f32(0.0)
    selected: BossPoolEntryReference | None = None
    for entry in shuffled:
        cumulative = _f32(cumulative + _f32(entry.weight))
        if target < cumulative:
            selected = entry
            break
    if selected is None:
        raise AssertionError("positive boss weights must select an entry")
    boss_id = (
        -selected.alternate_boss_id
        if selected.alternate_boss_id
        else selected.boss_id
    )
    return FreshBossSelectionReference(
        boss_id=boss_id,
        pool_index=BASEMENT_POOL_INDEX,
        shuffled_entry_ids=tuple(entry.boss_id for entry in shuffled),
        initial_pool_state=initial_state,
        persistent_pool_state=persistent_state,
        local_selector_final_state=state,
        level_blacklist=frozenset((selected.boss_id,)),
        ledger=tuple(ledger),
    )
