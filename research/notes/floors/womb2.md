# Womb II (LevelStage 8, ORIGINAL) — parameter status

Status: **parameters partially established; generation NOT implemented.**

## Confirmed / derived so far

| Parameter | Value | Source |
|---|---|---|
| LevelStage | 8 | level-stages enum (repo) |
| StageType | 0 (ORIGINAL) | main route |
| Stage-seed slot | 8 | `stage_seed.py` (CONFIRMED_BINARY slot selection) |
| RoomConfig stage | **10 (CONFIRMED_BINARY)** | `get_room_config_stage(8, 0)` = 1+((8-1)>>1)*3 = 10 (NOT Utero 11); see `get_room_config_stage_stage7_8_alt.md` |
| BossPool index | **10 (CONFIRMED_BINARY)** | pool == ORIGINAL rcs; rcs = 10 confirmed |
| XL eligibility | **never (even stage)** | curse logic: Labyrinth only on odd stages |
| Target room count | **20 NORMAL / 22-23 HARD (CONFIRMED_BINARY)** | `min(stage*10/3+5+bit, 20)`; stage 8 -> min(31+bit,20)=20; HARD `+2+bit` |
| Dead ends | **6 (CONFIRMED_BINARY)** | `(stage != 1) + 5` |
| Difficulty window | NORMAL 5..10 / HARD 10..15 (**predicted**) | pattern |
| Planetarium chance | `f32(f32(7*0.2)+0.01)` (**predicted**) | pattern (7 prior treasures) |

## Post-layout tail (BINARY-CONFIRMED this round)

Identical to Womb I: `-9` and `-10` both skipped (rcs != 13; stage_type 0),
so **28 persistent Level RNG draws, same sequence as Depths II/Womb I**. The
only open tail question is the `room_config_stage` argument value (10 vs 11)
that the lifecycle passes in and that the guard must accept.

## What still blocks implementation

1. Binary verify `get_room_config_stage(8, 0)` (Utero rcs 11 vs formula 10).
   This changes: lifecycle `room_config_stage`, `entries_from_definitions`
   stage, BossPool index, and the tail guard's expected rcs.
2. Through-Treasure pipeline for level_stage 8 (same as Womb I: every
   stage-dependent gate must be verified, not extrapolated).
3. Secret / Ultra / late RoomConfig assignment for stage 8.
4. `CanonicalWomb2Profile` + `derive_womb2_topology_inputs` + clean/reference
   pipelines + ~100 differentials + registry registration.

## Validation plan (when implemented)

50 NORMAL + 50 HARD ordered clean-vs-reference comparisons; evidence grade at
most `PARTIAL_BINARY` / `PREVIEW_SUPPORTED`.
