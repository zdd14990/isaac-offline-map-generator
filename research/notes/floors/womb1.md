# Womb I (LevelStage 7, ORIGINAL) — parameter status

Status: **parameters partially established; generation NOT implemented.**

## Confirmed / derived so far

| Parameter | Value | Source |
|---|---|---|
| LevelStage | 7 | level-stages enum (repo) |
| StageType | 0 (ORIGINAL) | main route |
| Stage-seed slot | 7 | `stage_seed.py` (CONFIRMED_BINARY slot selection) |
| RoomConfig stage | **10 (CONFIRMED_BINARY)** | `get_room_config_stage(7, 0)` = 1+((7-1)>>1)*3 = 10; see `get_room_config_stage_stage7_8_alt.md` |
| BossPool index | **10 (CONFIRMED_BINARY)** | pool == ORIGINAL rcs (`boss_pool.py`); rcs = 10 confirmed |
| Target room count | **20 NORMAL / 22-23 HARD (CONFIRMED_BINARY)** | `generate_dungeon.c`: `min(stage*10/3+5+bit, 20)`; stage 7 -> min(28+bit,20)=20; HARD `+2+bit` |
| Dead ends | **6 (CONFIRMED_BINARY)** | `generate_dungeon.c`: `(stage != 1) + 5` |
| XL target | **12 NORMAL / 13 HARD (CONFIRMED_BINARY)** | XL: `max(4, target*3/5)` on 20/22-23 |
| Difficulty window | NORMAL 5..10 / HARD 10..15 (**predicted**) | pattern; RoomConfig selection not yet traced |
| Planetarium chance | `f32(f32(6*0.2)+0.01)` (**predicted**) | pattern (6 prior treasures) |

## Post-layout tail (BINARY-CONFIRMED this round)

- `-9` (rcs==13) skipped: Womb rcs 10 != 13.
- `-10` (stage_type 4/5 AND level_stage 7/8) skipped: stage_type 0.
- Door-chance flag writes: local-RNG only, no persistent draws.
- => **28 persistent Level RNG draws, identical sequence to Depths II.**
  See `post_layout_descriptor_minus9.md`, `post_layout_descriptor_minus10.md`.

## What still blocks implementation

1. Binary verify `get_room_config_stage(7, 0)` and `(8, 0)` (Womb II may use
   Utero rcs 11, which would change the expected tail `room_config_stage`
   argument and the entries passed to the lifecycle).
2. Through-Treasure pipeline for level_stage 7: the repo's leaf guards
   `level_stage in (1..6)`; every stage-dependent gate in
   `basement1_pipeline.py` (MiniBoss stage-1, Chest stage-2, perimeter-block
   stage-3, Challenge/Library stage gates, ...) must be verified against the
   binary for stage 7 rather than extrapolated.
3. **XL Womb I**: the existing XL machinery is gated to stages 3/5
   (`is_xl and level_stage in (3,5)`); stage-7 XL (Labyrinth) needs its own
   verification (dual boss/treasure, second-chapter room set).
4. Secret / Ultra / late RoomConfig assignment for stage 7.
5. `CanonicalWomb1Profile` + `derive_womb1_topology_inputs` + clean/reference
   pipelines + ~100 differentials + registry registration.

## Validation plan (when implemented)

50 NORMAL + 50 HARD ordered clean-vs-reference comparisons; evidence grade at
most `PARTIAL_BINARY` / `PREVIEW_SUPPORTED` (100 samples are not
20k-class). Never `CONFIRMED_BINARY` on 100 samples.
