# Caves I blocked-predicate and XL-transaction binary evidence

Frozen executable: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

## Stage-3 blocked predicate

Question: does Caves I (LevelStage 3) have a Stage-3-specific Boss-neighbor
blocked behavior distinct from Basement I/II?

Answer: **No.** The boss-geometry placement uses a hardcoded
`distance_from_start > 1` filter, not a stage-dependent branch.

Evidence:

- `LevelGenerator::DetermineBossRoom` (RVA `0x005AED50`) takes the selected
  Boss RoomConfig's shape/door mask and scans the ordered dead-end list; it
  accepts a candidate only when `distance_from_start > 1`
  (`boss_distance_filter` in `special_rooms_reference.py`, `minimum_distance=1`
  in `special_rooms.py`). It receives no stage/stage-type argument.
- The XL multi-neighbor exception is in the topology generator, locked by the
  static slice `0x005B0768..0x005B07D7` and already `CONFIRMED_BINARY` in
  `caves1.md`; it is a topology draw, not a boss-geometry blocked rule.
- `LevelGenerator.blocked_positions` is a 169-entry vector cleared per attempt
  and populated only by topology/special placement, with no Stage-3-only
  write in the recovered slices.

The clean and reference implementations share this geometry leaf, and the
Caves-I differential exercises it identically. No Stage-3-specific branch was
found, so Basement I/II behavior is not polluted by Caves I.

## XL dual Boss / dual Treasure transaction

XL determination is `effective_curse & 0x02` (see `caves1.md`). Under XL the
ordinary post-topology pipeline selects and places two bosses and two
treasures. The through-Treasure reference
(`basement1_pipeline_reference.py`) gates the second boss on the same
`profile.level_stage == 3` Caves profile:

```text
boss       = select_canonical_caves_profile()   # pool 4
boss[1]    = select_canonical_caves_profile()   # pool 4 (XL second boss)
```

Both selections advance the persistent Caves pool (index 4) and are committed
only at the shared success boundary after Ultra and the late ordinary
RoomConfig pass. A Boss/Treasure geometry failure returns false and retries
the whole floor, retaining the seven persistent pre-rolls (see
`generation_retry_semantics.md`); neither the failed boss bit nor the second
treasure placement commits until the full attempt succeeds.

The dual-treasure path is part of the same through-Treasure leaf and is
covered end-to-end by the Caves-I differential corpus.

Algorithm confidence: `CONFIRMED_BINARY`.

External gameplay fixture status: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.
