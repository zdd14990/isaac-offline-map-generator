"""Explicit run/floor generation state for the frozen Basement I profile."""

from __future__ import annotations

from dataclasses import dataclass, field

from .boss_pool import BossPoolRuntimeState
from .room_config import RoomConfigMutableState
from .room_config import RoomConfigKey


# Game::GetPlanetariumChance performs float32 multiply/add operations.  The
# Stage-2 canonical expression f32(f32(1 * 0.2f) + 0.01f) is one ULP above a
# direct float32 conversion of the decimal literal 0.21.
BASEMENT2_PLANETARIUM_CHANCE_F32 = 0.21000000834465027
# Canonical Caves-I entry still assumes that no Treasure Room has been
# visited.  Game::GetPlanetariumChance therefore evaluates, in binary32
# order, f32(f32(2 * 0.2f) + 0.01f).
CAVES1_PLANETARIUM_CHANCE_F32 = 0.4099999964237213
# Caves II (Stage 4) entry: three prior Treasure Rooms.  In binary32 order,
# f32(f32(3 * 0.2f) + 0.01f).
CAVES2_PLANETARIUM_CHANCE_F32 = 0.6100000143051147
# Depths I (Stage 5) entry: four prior Treasure Rooms.  In binary32 order,
# f32(f32(4 * 0.2f) + 0.01f).
DEPTHS1_PLANETARIUM_CHANCE_F32 = 0.8100000023841858
# Depths II (Stage 6) entry: five prior Treasure Rooms.  In binary32 order,
# f32(f32(5 * 0.2f) + 0.01f).
DEPTHS2_PLANETARIUM_CHANCE_F32 = 1.0099999904632568


@dataclass(frozen=True)
class CanonicalBasement1Profile:
    """State contract for the currently proven ordinary fresh-run branch."""

    difficulty: str
    level_stage: int = 1
    stage_type: int = 0
    room_config_stage: int = 1
    fallback_room_config_stage: int = 0
    challenge_id: int = 0
    game_mode: int = 0
    character_id: int = 0
    effective_curse_mask: int = 0
    is_xl: bool = False
    is_ascent: bool = False
    is_daily: bool = False
    collectible_ids: frozenset[int] = frozenset()
    visited_room_types: frozenset[int] = frozenset()
    shop_state_flags: tuple[bool, bool, bool, bool] = (False, False, False, False)
    shop_generation_count: int = 0
    unlock_all_room_entries: bool = True
    # M6 extends the canonical profile with the player/persistent predicates
    # read between Treasure and Secret.  These are explicit because they are
    # not derivable from a stage seed in the general case.
    player0_max_hearts: int = 6
    player0_coins: int = 0
    player0_full_health: bool = True
    planetarium_unlocked: bool = True
    planetarium_chance: float = 0.01
    library_subtype_max: int = 4
    special_room_used_bits: frozenset[int] = frozenset()

    def validate(self) -> None:
        if self.difficulty not in ("NORMAL", "HARD"):
            raise ValueError("difficulty must be NORMAL or HARD")
        expected = (
            self.level_stage == 1 and self.stage_type == 0
            and self.room_config_stage == 1 and self.fallback_room_config_stage == 0
            and self.challenge_id == 0 and self.game_mode == 0
            and self.character_id == 0 and self.effective_curse_mask == 0
            and not self.is_xl and not self.is_ascent and not self.is_daily
            and not self.collectible_ids and not self.visited_room_types
            and self.shop_state_flags == (False, False, False, False)
            and self.shop_generation_count == 0
            and self.player0_max_hearts == 6 and self.player0_coins == 0
            and self.player0_full_health and self.planetarium_unlocked
            and self.planetarium_chance == 0.01
            and self.library_subtype_max == 4
            and not self.special_room_used_bits
        )
        if not expected:
            raise ValueError(
                "state is outside the binary-confirmed canonical fresh Basement I profile"
            )


@dataclass(frozen=True)
class CanonicalBasement2Profile(CanonicalBasement1Profile):
    """Stage-2 entry contract after canonical Basement-I generation replay."""

    level_stage: int = 2
    planetarium_chance: float = BASEMENT2_PLANETARIUM_CHANCE_F32

    def validate(self) -> None:
        if self.difficulty not in ("NORMAL", "HARD"):
            raise ValueError("difficulty must be NORMAL or HARD")
        expected = (
            self.level_stage == 2
            and self.stage_type == 0
            and self.room_config_stage == 1
            and self.fallback_room_config_stage == 0
            and self.challenge_id == 0
            and self.game_mode == 0
            and self.character_id == 0
            and self.effective_curse_mask in (0, 1, 4, 8, 32, 64)
            and not self.is_xl
            and not self.is_ascent
            and not self.is_daily
            and not self.collectible_ids
            and not self.visited_room_types
            and self.shop_state_flags == (False, False, False, False)
            and self.shop_generation_count == 0
            and self.player0_max_hearts == 6
            and self.player0_coins == 0
            and self.player0_full_health
            and self.planetarium_unlocked
            and self.planetarium_chance == BASEMENT2_PLANETARIUM_CHANCE_F32
            and self.library_subtype_max == 4
            and self.special_room_used_bits <= frozenset(range(9, 15))
        )
        if not expected:
            raise ValueError(
                "state is outside the binary-confirmed canonical Basement II entry profile"
            )


@dataclass(frozen=True)
class CanonicalCaves1Profile(CanonicalBasement1Profile):
    """Stage-3 ORIGINAL entry after canonical Basement-II replay.

    ``planetarium_chance`` is an explicit gameplay-profile input: it is only
    seed-replayable while the canonical run has not visited either earlier
    Treasure Room.  Natural Labyrinth is retained and represented by both
    curse bit 2 and ``is_xl``.
    """

    level_stage: int = 3
    room_config_stage: int = 4
    planetarium_chance: float = CAVES1_PLANETARIUM_CHANCE_F32

    def validate(self) -> None:
        if self.difficulty not in ("NORMAL", "HARD"):
            raise ValueError("difficulty must be NORMAL or HARD")
        expected = (
            self.level_stage == 3
            and self.stage_type == 0
            and self.room_config_stage == 4
            and self.fallback_room_config_stage == 0
            and self.challenge_id == 0
            and self.game_mode == 0
            and self.character_id == 0
            and self.effective_curse_mask in (0, 1, 2, 4, 8, 32, 64)
            and self.is_xl == bool(self.effective_curse_mask & 0x02)
            and not self.is_ascent
            and not self.is_daily
            and not self.collectible_ids
            and not self.visited_room_types
            and self.shop_state_flags == (False, False, False, False)
            and self.shop_generation_count == 0
            and self.player0_max_hearts == 6
            and self.player0_coins == 0
            and self.player0_full_health
            and self.planetarium_unlocked
            and self.planetarium_chance == CAVES1_PLANETARIUM_CHANCE_F32
            and self.library_subtype_max == 4
            and self.special_room_used_bits <= frozenset(range(9, 15))
        )
        if not expected:
            raise ValueError(
                "state is outside the binary-confirmed canonical Caves I entry profile"
            )


@dataclass(frozen=True)
class CanonicalCaves2Profile(CanonicalBasement1Profile):
    """Stage-4 ORIGINAL entry after canonical Caves-I replay.

    Even Stage 4 never satisfies the Labyrinth predicate, so ``is_xl`` is
    always false and the curse mask can never contain bit 2.
    """

    level_stage: int = 4
    room_config_stage: int = 4
    planetarium_chance: float = CAVES2_PLANETARIUM_CHANCE_F32

    def validate(self) -> None:
        if self.difficulty not in ("NORMAL", "HARD"):
            raise ValueError("difficulty must be NORMAL or HARD")
        expected = (
            self.level_stage == 4
            and self.stage_type == 0
            and self.room_config_stage == 4
            and self.fallback_room_config_stage == 0
            and self.challenge_id == 0
            and self.game_mode == 0
            and self.character_id == 0
            and self.effective_curse_mask in (0, 1, 4, 8, 32, 64)
            and not self.is_xl
            and not self.is_ascent
            and not self.is_daily
            and not self.collectible_ids
            and not self.visited_room_types
            and self.shop_state_flags == (False, False, False, False)
            and self.shop_generation_count == 0
            and self.player0_max_hearts == 6
            and self.player0_coins == 0
            and self.player0_full_health
            and self.planetarium_unlocked
            and self.planetarium_chance == CAVES2_PLANETARIUM_CHANCE_F32
            and self.library_subtype_max == 4
            and self.special_room_used_bits <= frozenset(range(9, 15))
        )
        if not expected:
            raise ValueError(
                "state is outside the binary-confirmed canonical Caves II entry profile"
            )


@dataclass(frozen=True)
class CanonicalDepths1Profile(CanonicalBasement1Profile):
    """Stage-5 ORIGINAL entry after canonical Caves-II replay.

    Odd Stage 5 satisfies the Labyrinth predicate again, so ``is_xl`` is
    possible and represented by curse bit 2.
    """

    level_stage: int = 5
    room_config_stage: int = 7
    planetarium_chance: float = DEPTHS1_PLANETARIUM_CHANCE_F32

    def validate(self) -> None:
        if self.difficulty not in ("NORMAL", "HARD"):
            raise ValueError("difficulty must be NORMAL or HARD")
        expected = (
            self.level_stage == 5
            and self.stage_type == 0
            and self.room_config_stage == 7
            and self.fallback_room_config_stage == 0
            and self.challenge_id == 0
            and self.game_mode == 0
            and self.character_id == 0
            and self.effective_curse_mask in (0, 1, 2, 4, 8, 32, 64)
            and self.is_xl == bool(self.effective_curse_mask & 0x02)
            and not self.is_ascent
            and not self.is_daily
            and not self.collectible_ids
            and not self.visited_room_types
            and self.shop_state_flags == (False, False, False, False)
            and self.shop_generation_count == 0
            and self.player0_max_hearts == 6
            and self.player0_coins == 0
            and self.player0_full_health
            and self.planetarium_unlocked
            and self.planetarium_chance == DEPTHS1_PLANETARIUM_CHANCE_F32
            and self.library_subtype_max == 4
            and self.special_room_used_bits <= frozenset(range(9, 15))
        )
        if not expected:
            raise ValueError(
                "state is outside the binary-confirmed canonical Depths I entry profile"
            )


@dataclass(frozen=True)
class CanonicalDepths2Profile(CanonicalBasement1Profile):
    """Stage-6 ORIGINAL entry after canonical Depths-I replay.

    Even Stage 6 never satisfies the Labyrinth predicate, so ``is_xl`` is
    always false and the curse mask can never contain bit 2.
    """

    level_stage: int = 6
    room_config_stage: int = 7
    planetarium_chance: float = DEPTHS2_PLANETARIUM_CHANCE_F32

    def validate(self) -> None:
        if self.difficulty not in ("NORMAL", "HARD"):
            raise ValueError("difficulty must be NORMAL or HARD")
        expected = (
            self.level_stage == 6
            and self.stage_type == 0
            and self.room_config_stage == 7
            and self.fallback_room_config_stage == 0
            and self.challenge_id == 0
            and self.game_mode == 0
            and self.character_id == 0
            and self.effective_curse_mask in (0, 1, 4, 8, 32, 64)
            and not self.is_xl
            and not self.is_ascent
            and not self.is_daily
            and not self.collectible_ids
            and not self.visited_room_types
            and self.shop_state_flags == (False, False, False, False)
            and self.shop_generation_count == 0
            and self.player0_max_hearts == 6
            and self.player0_coins == 0
            and self.player0_full_health
            and self.planetarium_unlocked
            and self.planetarium_chance == DEPTHS2_PLANETARIUM_CHANCE_F32
            and self.library_subtype_max == 4
            and self.special_room_used_bits <= frozenset(range(9, 15))
        )
        if not expected:
            raise ValueError(
                "state is outside the binary-confirmed canonical Depths II entry profile"
            )


@dataclass(frozen=True)
class CanonicalWomb1Profile(CanonicalBasement1Profile):
    """Stage-7 ORIGINAL entry after canonical Depths-II replay.

    Odd Stage 7 may satisfy the Labyrinth predicate (XL), so ``is_xl`` and
    curse bit 2 are allowed.  Planetarium is gated to stage < 7 in the binary
    (canonical Womb never places it), so ``planetarium_chance`` is recorded
    for documentation only.
    """

    level_stage: int = 7
    room_config_stage: int = 10
    planetarium_chance: float = 1.2099999

    def validate(self) -> None:
        if self.difficulty not in ("NORMAL", "HARD"):
            raise ValueError("difficulty must be NORMAL or HARD")
        expected = (
            self.level_stage == 7
            and self.stage_type == 0
            and self.room_config_stage == 10
            and self.fallback_room_config_stage == 0
            and self.challenge_id == 0
            and self.game_mode == 0
            and self.character_id == 0
            and self.effective_curse_mask in (0, 1, 2, 4, 8, 32, 64)
            and not self.is_ascent
            and not self.is_daily
            and not self.collectible_ids
            and not self.visited_room_types
            and self.shop_state_flags == (False, False, False, False)
            and self.shop_generation_count == 0
            and self.player0_max_hearts == 6
            and self.player0_coins == 0
            and self.player0_full_health
            and self.planetarium_unlocked
            and self.library_subtype_max == 4
            and self.special_room_used_bits <= frozenset(range(9, 15))
        )
        if not expected:
            raise ValueError(
                "state is outside the binary-confirmed canonical Womb I entry profile"
            )


@dataclass(frozen=True)
class CanonicalWomb2Profile(CanonicalBasement1Profile):
    """Stage-8 ORIGINAL entry after canonical Womb-I replay.

    Even Stage 8 never satisfies the Labyrinth predicate, so ``is_xl`` is
    always false and the curse mask can never contain bit 2.
    """

    level_stage: int = 8
    room_config_stage: int = 10
    planetarium_chance: float = 1.4099999

    def validate(self) -> None:
        if self.difficulty not in ("NORMAL", "HARD"):
            raise ValueError("difficulty must be NORMAL or HARD")
        expected = (
            self.level_stage == 8
            and self.stage_type == 0
            and self.room_config_stage == 10
            and self.fallback_room_config_stage == 0
            and self.challenge_id == 0
            and self.game_mode == 0
            and self.character_id == 0
            and self.effective_curse_mask in (0, 1, 4, 8, 32, 64)
            and not self.is_xl
            and not self.is_ascent
            and not self.is_daily
            and not self.collectible_ids
            and not self.visited_room_types
            and self.shop_state_flags == (False, False, False, False)
            and self.shop_generation_count == 0
            and self.player0_max_hearts == 6
            and self.player0_coins == 0
            and self.player0_full_health
            and self.planetarium_unlocked
            and self.library_subtype_max == 4
            and self.special_room_used_bits <= frozenset(range(9, 15))
        )
        if not expected:
            raise ValueError(
                "state is outside the binary-confirmed canonical Womb II entry profile"
            )


@dataclass
class RunGenerationState:
    game_start_seed: int
    boss_pools: BossPoolRuntimeState
    room_config: RoomConfigMutableState = field(default_factory=RoomConfigMutableState)
    current_stage_lifecycle: str = "fresh-run-before-basement1"
    # Game+0x26548 bitset.  MiniBoss assignment mutates it immediately and
    # Level::attempt_reset does not roll it back.
    special_room_used_bits: set[int] = field(default_factory=set)


@dataclass
class FloorGenerationState:
    stage_seed: int
    retry_count: int = 0
    target_room_count: int = 0
    current_descriptors: list[object] = field(default_factory=list)
    dead_end_candidates: list[int] = field(default_factory=list)
    # ``level_rng`` and ``level_generator`` are deliberately typed as object:
    # their identities, not a common superclass, are the important contract.
    level_rng: object | None = None
    level_generator: object | None = None


@dataclass(frozen=True)
class CanonicalRunGenerationSnapshot:
    """Generation-only state handed from one canonical floor to the next."""

    game_start_seed: int
    completed_level_stage: int
    next_level_stage: int
    boss_pool_rng_states: tuple[int, ...]
    permanent_removed_bosses: tuple[int, ...]
    room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    special_room_used_bits: tuple[int, ...]
    last_floor_level_rng_state: int
    lifecycle: str
