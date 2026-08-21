from __future__ import annotations

import pytest

from isaacmap.floor_init import can_apply_labyrinth, derive_alt_topology_inputs
from isaacmap.floor_init_reference import derive_alt_topology_inputs_reference
from isaacmap.seed import decode_seed


ALT_FLOORS = (
    (1, 4, 27, 2),
    (2, 5, 28, 3),
    (3, 4, 29, 4),
    (4, 5, 30, 5),
    (5, 4, 31, 6),
    (6, 5, 32, 7),
)


def _clean(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.seed_slot,
        value.level_rng_draws,
        value.copied_rng_draws,
        value.curse_rate_denominator,
        value.curse_gate_succeeded,
        value.curse_selector,
        value.effective_curse_mask,
        value.is_xl,
        value.generator_seed,
        value.target_room_count,
        value.required_dead_ends,
        value.allowed_shapes_mask,
        value.room_config_stage,
        value.room_config_min_difficulty,
        value.room_config_max_difficulty,
    )


def _reference(value) -> tuple[object, ...]:
    return (
        value.stage_seed,
        value.seed_slot,
        value.level_draws,
        value.copied_draws,
        value.curse_rate,
        value.curse_gate,
        value.curse_selector,
        value.curse_mask,
        value.is_xl,
        value.generator_seed,
        value.target,
        value.dead_ends,
        value.shapes,
        value.room_config_stage,
        value.minimum_difficulty,
        value.maximum_difficulty,
    )


@pytest.mark.parametrize("difficulty", ("NORMAL", "HARD"))
@pytest.mark.parametrize("level_stage,stage_type,rcs,slot", ALT_FLOORS)
def test_alt_initialization_matches_independent_reference(
    difficulty: str, level_stage: int, stage_type: int, rcs: int, slot: int
) -> None:
    masks: set[int] = set()
    for seed in range(1, 10_001):
        clean = derive_alt_topology_inputs(level_stage, stage_type, seed, difficulty)
        reference = derive_alt_topology_inputs_reference(
            level_stage, stage_type, seed, difficulty
        )
        assert _clean(clean) == _reference(reference)
        masks.add(clean.effective_curse_mask)
        assert clean.room_config_stage == rcs
        assert clean.seed_slot == slot
        if level_stage % 2 == 0:
            assert not clean.is_xl
    if level_stage % 2 == 1:
        assert masks == {0, 1, 2, 4, 8, 32, 64}
    else:
        assert masks == {0, 1, 4, 8, 32, 64}


    cases = {
        # (stage, type): (targetN range, dead_ends, diffN, diffH)
        (1, 4): ((8, 9), 5, (1, 5), (5, 10)),
        (2, 5): ((8, 9), 7, (5, 10), (10, 15)),
        (3, 4): ((15, 16), 6, (1, 5), (5, 10)),
        (4, 5): ((15, 16), 7, (5, 10), (10, 15)),
        (5, 4): ((20, 20), 6, (1, 5), (5, 10)),
        (6, 5): ((20, 20), 6, (5, 10), (10, 15)),
    }
    for (stage, stype), (tn, de, dn, dh) in cases.items():
        normal = derive_alt_topology_inputs(stage, stype, 1, "NORMAL")
        hard = derive_alt_topology_inputs(stage, stype, 1, "HARD")
        assert normal.target_room_count in tn, (stage, stype)
        assert normal.required_dead_ends == de, (stage, stype)
        assert (normal.room_config_min_difficulty, normal.room_config_max_difficulty) == dn
        assert (hard.room_config_min_difficulty, hard.room_config_max_difficulty) == dh
        # HARD adds 2 + (difficulty draw bit) after the NORMAL base.
        assert hard.target_room_count - normal.target_room_count in (2, 3)

def test_alt_xl_targets() -> None:
    """XL targets: 1+ -> 9/10, 3+ -> 21/23, 5+ -> 36 (NORMAL base)."""
    seen: dict[int, int] = {}
    for seed in range(1, 20_000):
        for stage, stype in ((1, 4), (3, 4), (5, 4)):
            inputs = derive_alt_topology_inputs(stage, stype, seed, "NORMAL")
            if inputs.is_xl:
                seen.setdefault(stage, inputs.target_room_count)
    assert seen.get(1) in (9, 10), seen
    assert seen.get(3) in (21, 22, 23), seen
    assert seen.get(5) == 36, seen


@pytest.mark.parametrize(
    "level_stage,expected",
    ((1, True), (2, False), (3, True), (4, False),
     (5, True), (6, False), (7, True), (8, False)),
)
def test_can_apply_labyrinth_binary_floor_matrix(
    level_stage: int, expected: bool
) -> None:
    assert can_apply_labyrinth(level_stage) is expected
    assert not can_apply_labyrinth(level_stage, game_mode=2)
    assert not can_apply_labyrinth(level_stage, game_mode=3)
    assert not can_apply_labyrinth(level_stage, stage_transition_id=0x2C)


def test_natural_xl_is_automatic_and_resets_on_even_alt_floors() -> None:
    downpour1 = derive_alt_topology_inputs(1, 4, 143, "NORMAL")
    dross = derive_alt_topology_inputs(2, 5, 143, "NORMAL")
    mines1 = derive_alt_topology_inputs(3, 4, 787, "NORMAL")
    ashpit = derive_alt_topology_inputs(4, 5, 787, "NORMAL")

    assert downpour1.effective_curse_mask == 0x02
    assert downpour1.is_xl
    assert downpour1.target_room_count == 9
    assert downpour1.required_dead_ends == 7
    assert not dross.is_xl
    assert not (dross.effective_curse_mask & 0x02)
    assert mines1.is_xl
    assert mines1.effective_curse_mask == 0x02
    assert not ashpit.is_xl
    assert not (ashpit.effective_curse_mask & 0x02)


def test_dkm89mnm_hard_downpour1_canonical_curse_trace() -> None:
    start_seed = decode_seed("DKM8 9MNM")
    clean = derive_alt_topology_inputs(1, 4, start_seed, "HARD")
    reference = derive_alt_topology_inputs_reference(1, 4, start_seed, "HARD")

    assert start_seed == 364_417_104
    assert clean.stage_seed == 362_265_690
    assert clean.seed_slot == 2
    assert clean.stage_type == 4
    assert clean.room_config_stage == 27
    assert clean.curse_rate_denominator == 40
    assert clean.copied_rng_draws[0] == 163_224_774
    assert clean.copied_rng_draws[0] % clean.curse_rate_denominator == 14
    assert not clean.curse_gate_succeeded
    assert clean.curse_selector is None
    assert clean.effective_curse_mask == 0
    assert not clean.is_xl
    assert clean.target_room_count == 10
    assert clean.required_dead_ends == 5
    assert _clean(clean) == _reference(reference)


@pytest.mark.parametrize(
    ("seed_text", "rate6_is_xl", "rate3_is_xl", "rate3_target"),
    [
        ("DKM8 9MNM", True, True, 12),
        ("BJPK 79MF", False, True, 13),
        ("BJPK 72ME", True, True, 11),
        ("BJPK 79FB", False, False, 11),
    ],
)
def test_progression_profile_probe_matrix_matches_clean_and_reference(
    seed_text: str,
    rate6_is_xl: bool,
    rate3_is_xl: bool,
    rate3_target: int,
) -> None:
    start_seed = decode_seed(seed_text)
    rate6 = derive_alt_topology_inputs(
        1, 4, start_seed, "HARD", generation_profile="RATE_10_6"
    )
    rate6_reference = derive_alt_topology_inputs_reference(
        1, 4, start_seed, "HARD", generation_profile="RATE_10_6"
    )
    rate3 = derive_alt_topology_inputs(
        1, 4, start_seed, "HARD", generation_profile="RATE_5_3"
    )
    rate3_reference = derive_alt_topology_inputs_reference(
        1, 4, start_seed, "HARD", generation_profile="RATE_5_3"
    )

    assert rate6.is_xl is rate6_is_xl
    assert rate3.is_xl is rate3_is_xl
    assert rate3.target_room_count == rate3_target
    assert _clean(rate6) == _reference(rate6_reference)
    assert _clean(rate3) == _reference(rate3_reference)


def test_alt_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="stage_type 4 or 5"):
        derive_alt_topology_inputs(1, 0, 1, "NORMAL")
    with pytest.raises(ValueError, match="level_stage 1..6"):
        derive_alt_topology_inputs(7, 4, 1, "NORMAL")
    with pytest.raises(ValueError, match="NORMAL or HARD"):
        derive_alt_topology_inputs(1, 4, 1, "GREED")
