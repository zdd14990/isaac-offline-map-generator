"""Readable BossPool implementation for the current executable profile.

The public exact floor generator remains fail-closed. These helpers cover the
freshly initialized Basement boss pool in the confirmed canonical Milestone 5
slice and are differential-tested against ``boss_pool_reference``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import struct

from .rng import IsaacRNG


POOL_COUNT = 37
MASTER_SHIFT_INDEX = 26  # (3,13,7)
POOL_SHIFT_INDEX = 17  # (2,21,9)
BASEMENT_POOL_INDEX = 1
CAVES_POOL_INDEX = 4
DEPTHS_POOL_INDEX = 7


def _f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


@dataclass(frozen=True)
class BossPoolEntry:
    boss_id: int
    weight: float
    initial_weight: float
    achievement: int = -1
    alternate_boss_id: int = 0


@dataclass(frozen=True)
class FreshBossSelection:
    boss_id: int
    pool_index: int
    shuffled_entry_ids: tuple[int, ...]
    initial_pool_state: int
    persistent_pool_state: int
    local_selector_final_state: int
    level_blacklist: frozenset[int]
    transitions: tuple[tuple[str, int, int], ...]


@dataclass(frozen=True)
class BossPoolRuntimeSelection:
    boss_id: int
    selected_entry_id: int
    pool_index: int
    persistent_pre_state: int
    persistent_post_state: int
    local_selector_final_state: int
    transitions: tuple[tuple[str, int, int], ...]
    repick_count: int = 0
    fallback_used: bool = False
    pool_reset_count: int = 0


@dataclass
class BossPoolRuntimeState:
    """The persistent state owned by ``Game+0x1AF70``.

    ``level_blacklist`` is transaction-local and cleared at every outer floor
    attempt. ``removed`` is only updated by the success commit at RVA
    0x00021B50. Pool RNG state is never part of that transaction.
    """

    game_start_seed: int
    pool_seeds: tuple[int, ...]
    pool_rngs: list[IsaacRNG]
    shuffled_entries: dict[int, tuple[BossPoolEntry, ...]]
    removed: set[int]
    level_blacklist: set[int]

    @classmethod
    def fresh_basement(
        cls, game_start_seed: int, basement_entries: tuple[BossPoolEntry, ...]
    ) -> "BossPoolRuntimeState":
        seeds = derive_pool_seeds(game_start_seed)
        return cls(
            game_start_seed=game_start_seed,
            pool_seeds=seeds,
            pool_rngs=[IsaacRNG.game_constructor(seed, POOL_SHIFT_INDEX) for seed in seeds],
            shuffled_entries={
                BASEMENT_POOL_INDEX: shuffle_entries(
                    basement_entries, seeds[BASEMENT_POOL_INDEX]
                )
            },
            removed=set(),
            level_blacklist=set(),
        )

    @classmethod
    def resume_canonical_basement(
        cls,
        game_start_seed: int,
        basement_entries: tuple[BossPoolEntry, ...],
        *,
        pool_state: int,
        removed: tuple[int, ...] | set[int],
    ) -> "BossPoolRuntimeState":
        """Restore the Basement pool from a generation-state snapshot."""

        result = cls.fresh_basement(game_start_seed, basement_entries)
        result.pool_rngs[BASEMENT_POOL_INDEX].seed = pool_state
        result.removed.update(removed)
        return result

    @classmethod
    def resume_canonical_caves(
        cls,
        game_start_seed: int,
        caves_entries: tuple[BossPoolEntry, ...],
        *,
        pool_state: int,
        removed: tuple[int, ...] | set[int],
    ) -> "BossPoolRuntimeState":
        """Restore pool 4 from a confirmed prior-floor generation snapshot."""

        seeds = derive_pool_seeds(game_start_seed)
        result = cls(
            game_start_seed=game_start_seed,
            pool_seeds=seeds,
            pool_rngs=[
                IsaacRNG.game_constructor(seed, POOL_SHIFT_INDEX) for seed in seeds
            ],
            shuffled_entries={
                CAVES_POOL_INDEX: shuffle_entries(
                    caves_entries, seeds[CAVES_POOL_INDEX]
                )
            },
            removed=set(removed),
            level_blacklist=set(),
        )
        result.pool_rngs[CAVES_POOL_INDEX].seed = pool_state
        return result

    def begin_attempt(self) -> None:
        # Level__attempt_reset RVA 0x003382C0.
        self.level_blacklist.clear()

    def commit_floor(self) -> None:
        # BossPool__commit_floor RVA 0x00021B50.
        self.removed.update(self.level_blacklist)
        self.level_blacklist.clear()

    def select_fresh_basement_profile(self) -> BossPoolRuntimeSelection:
        """Ordinary Basement path with all documented override branches false."""

        return self.select_canonical_basement_profile()

    @staticmethod
    def _pick_canonical_entry(
        entries: tuple[BossPoolEntry, ...],
        target: float,
        total: float,
        removed: set[int],
        level_blacklist: set[int],
    ) -> tuple[BossPoolEntry | None, int, bool]:
        """Port the remap/fallback loop at RVA ``0x00022620``."""

        repicks = 0
        for remaining in range(9, -1, -1):
            cumulative = _f32(0.0)
            hit_index = -1
            for index, entry in enumerate(entries):
                before = cumulative
                cumulative = _f32(cumulative + entry.weight)
                if not target < cumulative:
                    continue
                hit_index = index
                if (
                    entry.initial_weight > 0.0
                    and target < _f32(before + entry.initial_weight)
                    and entry.achievement < 0
                    and entry.boss_id not in removed
                    and entry.boss_id not in level_blacklist
                ):
                    return entry, repicks, False
                if remaining == 0:
                    for offset in range(1, len(entries)):
                        fallback = entries[(index + offset) % len(entries)]
                        if (
                            fallback.initial_weight > 0.0
                            and fallback.achievement < 0
                            and fallback.boss_id not in removed
                            and fallback.boss_id not in level_blacklist
                        ):
                            return fallback, repicks, True
                    return None, repicks, True
                target = _f32(
                    _f32(_f32(cumulative - target) / entry.weight) * total
                )
                repicks += 1
                break
            if hit_index < 0:
                continue
        return None, repicks, False

    def select_canonical_basement_profile(self) -> BossPoolRuntimeSelection:
        """Base-unlock ORIGINAL Basement pick, including removed-boss repicks."""

        return self._select_canonical_pool(BASEMENT_POOL_INDEX)

    def select_canonical_caves_profile(self) -> BossPoolRuntimeSelection:
        """Canonical ORIGINAL Caves pick from current RoomConfig stage 4."""

        return self._select_canonical_pool(CAVES_POOL_INDEX)

    def select_canonical_stage(self, room_config_stage: int) -> BossPoolRuntimeSelection:
        """Select from the BossPool indexed by the ORIGINAL room-config stage.

        Pool index equals room-config stage on the ORIGINAL route (1 Basement,
        4 Caves, 7 Depths, ...).
        """

        return self._select_canonical_pool(room_config_stage)

    def _select_canonical_pool(self, pool_index: int) -> BossPoolRuntimeSelection:
        entries = self.shuffled_entries[pool_index]
        persistent = self.pool_rngs[pool_index]
        pre_state = persistent.seed
        transitions: list[tuple[str, int, int]] = []
        for _ in range(7):
            pre = persistent.seed
            post = persistent.next()
            transitions.append((f"BossPools.pool[{pool_index}]._rng", pre, post))

        local = IsaacRNG.game_constructor(persistent.seed, POOL_SHIFT_INDEX)
        total = _f32(0.0)
        for entry in entries:
            total = _f32(total + entry.weight)
        selected: BossPoolEntry | None = None
        total_repicks = 0
        fallback_used = False
        pool_resets = 0
        for _ in range(10):
            local_pre = local.seed
            unit = local.random_float()
            transitions.append(
                (f"stack_copy(BossPools.pool[{pool_index}]._rng)", local_pre, local.seed)
            )
            selected, repicks, fallback = self._pick_canonical_entry(
                entries,
                _f32(unit * total),
                total,
                self.removed,
                self.level_blacklist,
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
            return BossPoolRuntimeSelection(
                1,
                1,
                pool_index,
                pre_state,
                persistent.seed,
                local.seed,
                tuple(transitions),
                total_repicks,
                fallback_used,
                pool_resets,
            )
        self.level_blacklist.add(selected.boss_id)
        boss_id = -selected.alternate_boss_id if selected.alternate_boss_id else selected.boss_id
        return BossPoolRuntimeSelection(
            boss_id=boss_id,
            selected_entry_id=selected.boss_id,
            pool_index=pool_index,
            persistent_pre_state=pre_state,
            persistent_post_state=persistent.seed,
            local_selector_final_state=local.seed,
            transitions=tuple(transitions),
            repick_count=total_repicks,
            fallback_used=fallback_used,
            pool_reset_count=pool_resets,
        )


_POOL_START = re.compile(r'<pool\s+name="([^"]+)"(?:\s+doubletrouble="([^"]+)")?\s*>')
_POOL_EMPTY = re.compile(r'<pool\s+name="([^"]+)"\s*/>')
_BOSS = re.compile(
    r'<boss\s+id="(\d+)"\s+weight="([0-9.]+)"'
    r'(?:\s+achievement="(-?\d+)")?'
    r'(?:\s+doubletrouble="(-?\d+)")?\s*/>'
)


def load_boss_pool_xml(path: Path | str) -> dict[str, tuple[BossPoolEntry, ...]]:
    """Parse the game's simple ordered boss-pool XML dialect.

    The installed file closes its outer ``<bosspools>`` with ``</pool>`` and
    is accepted by the game loader, so a strict general-purpose XML parser is
    intentionally not used here.
    """

    pools: dict[str, list[BossPoolEntry]] = {}
    current: list[BossPoolEntry] | None = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        empty = _POOL_EMPTY.search(line)
        if empty:
            pools[empty.group(1)] = []
            current = None
            continue
        start = _POOL_START.search(line)
        if start:
            current = []
            pools[start.group(1)] = current
            continue
        boss = _BOSS.search(line)
        if boss and current is not None:
            weight = _f32(float(boss.group(2)))
            current.append(
                BossPoolEntry(
                    boss_id=int(boss.group(1)),
                    weight=weight,
                    initial_weight=weight,
                    achievement=int(boss.group(3)) if boss.group(3) else -1,
                    alternate_boss_id=int(boss.group(4)) if boss.group(4) else 0,
                )
            )
    return {name: tuple(entries) for name, entries in pools.items()}


def derive_pool_seeds(game_start_seed: int) -> tuple[int, ...]:
    master = IsaacRNG.game_constructor(game_start_seed, MASTER_SHIFT_INDEX)
    return tuple(master.next() for _ in range(POOL_COUNT))


class _MT19937:
    def __init__(self, seed: int) -> None:
        self.state = [seed & 0xFFFFFFFF]
        for index in range(1, 624):
            previous = self.state[-1]
            self.state.append(
                (0x6C078965 * (previous ^ (previous >> 30)) + index)
                & 0xFFFFFFFF
            )
        self.position = 624

    def _twist(self) -> None:
        for index in range(624):
            combined = (
                (self.state[index] & 0x80000000)
                | (self.state[(index + 1) % 624] & 0x7FFFFFFF)
            )
            value = self.state[(index + 397) % 624] ^ (combined >> 1)
            if combined & 1:
                value ^= 0x9908B0DF
            self.state[index] = value & 0xFFFFFFFF
        self.position = 0

    def next(self) -> int:
        if self.position >= 624:
            self._twist()
        value = self.state[self.position]
        self.position += 1
        value ^= value >> 11
        value ^= (value << 7) & 0x9D2C5680
        value ^= (value << 15) & 0xEFC60000
        value ^= value >> 18
        return value & 0xFFFFFFFF


def shuffle_entries(entries: tuple[BossPoolEntry, ...], seed: int) -> tuple[BossPoolEntry, ...]:
    values = list(entries)
    mt = _MT19937(seed)
    for index in range(len(values) - 1, 0, -1):
        other = mt.next() % (index + 1)
        values[index], values[other] = values[other], values[index]
    return tuple(values)


def pick_fresh_basement_boss(
    game_start_seed: int, entries: tuple[BossPoolEntry, ...]
) -> FreshBossSelection:
    seeds = derive_pool_seeds(game_start_seed)
    initial = seeds[BASEMENT_POOL_INDEX]
    shuffled = shuffle_entries(entries, initial)
    if not shuffled:
        raise ValueError("the Basement boss pool must not be empty")

    persistent = IsaacRNG.game_constructor(initial, POOL_SHIFT_INDEX)
    transitions: list[tuple[str, int, int]] = []
    for _ in range(7):
        pre = persistent.seed
        post = persistent.next()
        transitions.append(("BossPools.pool[1]._rng", pre, post))

    selector = IsaacRNG.game_constructor(persistent.seed, POOL_SHIFT_INDEX)
    selector_pre = selector.seed
    unit = selector.random_float()
    transitions.append(("stack_copy(BossPools.pool[1]._rng)", selector_pre, selector.seed))
    total = _f32(0.0)
    for entry in shuffled:
        total = _f32(total + entry.weight)
    target = _f32(unit * total)
    cumulative = _f32(0.0)
    selected = shuffled[-1]
    for entry in shuffled:
        cumulative = _f32(cumulative + entry.weight)
        if target < cumulative:
            selected = entry
            break
    boss_id = -selected.alternate_boss_id if selected.alternate_boss_id else selected.boss_id
    return FreshBossSelection(
        boss_id=boss_id,
        pool_index=BASEMENT_POOL_INDEX,
        shuffled_entry_ids=tuple(entry.boss_id for entry in shuffled),
        initial_pool_state=initial,
        persistent_pool_state=persistent.seed,
        local_selector_final_state=selector.seed,
        level_blacklist=frozenset((selected.boss_id,)),
        transitions=tuple(transitions),
    )
