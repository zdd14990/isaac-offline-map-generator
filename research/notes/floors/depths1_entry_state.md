# Depths I entry state

Frozen executable: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Depths I (LevelStage 5) is entered from `Caves2LifecycleResult.next_run_state`
with `completed_level_stage=4` and `next_level_stage=5`. The following
generation state is inherited and must NOT be re-initialized:

## Inherited from the Caves-II snapshot

- **37 BossPool persistent RNG states**: pool 1 (Basement) and pool 4 (Caves)
  carry their committed post-floor states; pool 7 (Depths) is still the
  run-start state because no earlier floor selects it.
- **permanent removed bosses**: the four bosses committed by Basement I,
  Basement II, Caves I and Caves II (five under Caves-I XL).
- **RoomConfig mutable weights**: every stage's current weight, including the
  stage-4 (Caves) decay; `Level::Init` resets only the stage-7 (Depths) pool.
- **special-room used bits**: `Game+0x26548` bits cleared by the Caves-II tail.
- **last floor Level RNG state**: recorded for proof; Depths I re-derives its
  own Level RNG from its stage-seed slot 5.
- **stage seed slots**: `_stageSeeds[0..13]` are fixed at run start; slot 5 is
  read for Depths I.
- **canonical profile**: difficulty, StageType ORIGINAL, no challenge/daily/
  ascent, no collectibles, canonical player generation inputs, fresh-save
  unlock/achievement profile.

## Not inherited (recomputed per floor)

- Level RNG (from stage-seed slot 5).
- LevelGenerator (from the Stage-5 generator seed).
- topology temporaries (cleared per attempt).

The entry contract is enforced by `generate_depths1_full`, which rejects a
snapshot that is not `next_level_stage=5, completed_level_stage=4`.
