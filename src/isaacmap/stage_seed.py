"""Initial stage-seed sequence derived by ``Seeds::set_start_seed``."""

from __future__ import annotations

from dataclasses import dataclass

from .rng import IsaacRNG, UINT32_MASK

LEVEL_STAGE_MIN = 0
LEVEL_STAGE_MAX = 13
STAGE_SEED_COUNT = 14
START_SEQUENCE_SHIFT_INDEX = 27  # Current table entry (3, 23, 25).
STAGETYPE_REPENTANCE = 4
STAGETYPE_REPENTANCE_B = 5


def _validate_start_seed(start_seed: int) -> int:
    if isinstance(start_seed, bool) or not isinstance(start_seed, int):
        raise TypeError("start seed must be an integer")
    if not 1 <= start_seed <= UINT32_MASK:
        raise ValueError("ordinary start seed must be in the range 1..0xffffffff")
    return start_seed


@dataclass(frozen=True)
class InitialSeedSequence:
    start_seed: int
    stage_seeds: tuple[int, ...]
    player_init_seed: int

    def stage_seed(self, level_stage: int) -> int:
        if isinstance(level_stage, bool) or not isinstance(level_stage, int):
            raise TypeError("level stage must be an integer")
        if not LEVEL_STAGE_MIN <= level_stage <= LEVEL_STAGE_MAX:
            raise ValueError("level stage must be in the range 0..13")
        return self.stage_seeds[level_stage]


def derive_initial_seed_sequence(start_seed: int) -> InitialSeedSequence:
    """Precompute the exact 14 stage slots and player-init seed.

    The zero-input fallback in the game calls its nondeterministic global
    ``Random`` function. It is outside the ordinary display-seed domain and is
    deliberately rejected here.
    """

    start_seed = _validate_start_seed(start_seed)
    rng = IsaacRNG.game_constructor(start_seed, START_SEQUENCE_SHIFT_INDEX)
    stage_seeds = tuple(rng.next() for _ in range(STAGE_SEED_COUNT))
    player_init_seed = rng.next()
    return InitialSeedSequence(start_seed, stage_seeds, player_init_seed)


def get_initial_stage_seed(start_seed: int, level_stage: int) -> int:
    """Return the initially precomputed seed for a LevelStage index 0..13."""

    return derive_initial_seed_sequence(start_seed).stage_seed(level_stage)


def floor_stage_seed_slot(level_stage: int, stage_type: int) -> int:
    """Return the stage-seed slot selected by ``Level::Init``.

    Repentance alternate-path stage types use the next slot, with the result
    capped at the Home slot. Other stage types use ``LevelStage`` directly.
    """

    if isinstance(level_stage, bool) or not isinstance(level_stage, int):
        raise TypeError("level stage must be an integer")
    if not LEVEL_STAGE_MIN <= level_stage <= LEVEL_STAGE_MAX:
        raise ValueError("level stage must be in the range 0..13")
    if isinstance(stage_type, bool) or not isinstance(stage_type, int):
        raise TypeError("stage type must be an integer")
    if not 0 <= stage_type <= STAGETYPE_REPENTANCE_B:
        raise ValueError("stage type must be in the range 0..5")
    adjusted = level_stage + (
        stage_type in (STAGETYPE_REPENTANCE, STAGETYPE_REPENTANCE_B)
    )
    return min(adjusted, LEVEL_STAGE_MAX)


def get_initial_floor_stage_seed(
    start_seed: int, level_stage: int, stage_type: int
) -> int:
    """Select the initially precomputed slot exactly as ``Level::Init`` does."""

    slot = floor_stage_seed_slot(level_stage, stage_type)
    return get_initial_stage_seed(start_seed, slot)
