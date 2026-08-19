from __future__ import annotations

import pytest

from isaacmap.floor_init import derive_alt_topology_inputs
from isaacmap.floor_init_reference import derive_alt_topology_inputs_reference


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


def test_alt_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="stage_type 4 or 5"):
        derive_alt_topology_inputs(1, 0, 1, "NORMAL")
    with pytest.raises(ValueError, match="level_stage 1..6"):
        derive_alt_topology_inputs(7, 4, 1, "NORMAL")
    with pytest.raises(ValueError, match="NORMAL or HARD"):
        derive_alt_topology_inputs(1, 4, 1, "GREED")
