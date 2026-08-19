"""Reference/clean differential checks for the Basement BossPool."""

from __future__ import annotations

from .boss_pool import (
    BossPoolEntry,
    BossPoolRuntimeSelection,
    pick_fresh_basement_boss,
)
from .boss_pool_reference import (
    BossPoolEntryReference,
    BossPoolRuntimeSelectionReference,
    pick_fresh_basement_boss_reference,
)


def compare_runtime_selection(
    clean: BossPoolRuntimeSelection,
    reference: BossPoolRuntimeSelectionReference,
) -> None:
    """Compare persistent/local RNG state and the inherited-pool repick path."""

    clean_key = (
        clean.boss_id,
        clean.selected_entry_id,
        clean.pool_index,
        clean.persistent_pre_state,
        clean.persistent_post_state,
        clean.local_selector_final_state,
        clean.repick_count,
        clean.fallback_used,
        clean.pool_reset_count,
        tuple((pre, post) for _, pre, post in clean.transitions),
    )
    reference_key = (
        reference.boss_id,
        reference.selected_entry_id,
        reference.pool_index,
        reference.persistent_pre_state,
        reference.persistent_post_state,
        reference.local_selector_final_state,
        reference.repick_count,
        reference.fallback_used,
        reference.pool_reset_count,
        tuple((draw.pre_state, draw.post_state) for draw in reference.ledger),
    )
    if clean_key != reference_key:
        raise AssertionError(
            "BossPool runtime differential mismatch: "
            f"clean={clean_key!r}, reference={reference_key!r}"
        )


def compare_fresh_basement_boss(game_start_seed: int, entries: tuple[BossPoolEntry, ...]) -> None:
    clean = pick_fresh_basement_boss(game_start_seed, entries)
    reference = pick_fresh_basement_boss_reference(
        game_start_seed,
        tuple(
            BossPoolEntryReference(
                boss_id=entry.boss_id,
                weight=entry.weight,
                initial_weight=entry.initial_weight,
                achievement=entry.achievement,
                alternate_boss_id=entry.alternate_boss_id,
            )
            for entry in entries
        ),
    )
    clean_key = (
        clean.boss_id,
        clean.pool_index,
        clean.shuffled_entry_ids,
        clean.initial_pool_state,
        clean.persistent_pool_state,
        clean.local_selector_final_state,
        clean.level_blacklist,
        tuple((pre, post) for _, pre, post in clean.transitions),
    )
    reference_key = (
        reference.boss_id,
        reference.pool_index,
        reference.shuffled_entry_ids,
        reference.initial_pool_state,
        reference.persistent_pool_state,
        reference.local_selector_final_state,
        reference.level_blacklist,
        tuple((draw.pre_state, draw.post_state) for draw in reference.ledger),
    )
    if clean_key != reference_key:
        raise AssertionError(
            f"BossPool differential mismatch for start seed 0x{game_start_seed:08X}: "
            f"clean={clean_key!r}, reference={reference_key!r}"
        )
