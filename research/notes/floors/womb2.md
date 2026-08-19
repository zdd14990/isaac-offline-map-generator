# Womb II (LevelStage 8, ORIGINAL) — implementation complete

Status: **IMPLEMENTED, PARTIAL_BINARY.** Generation open on MAIN route stage 8
(bot token `8`, `/map B911 99AC 1 8`). Evidence grade intentionally
`PARTIAL_BINARY` (100-sample corpus, not 20k-class). ALT route remains
FAIL CLOSED.

## Confirmed parameters

| Parameter | Value | Source |
|---|---|---|
| LevelStage | 8 | level-stages enum (repo) |
| StageType | 0 (ORIGINAL) | main route |
| Stage-seed slot | 8 | `stage_seed.py` (CONFIRMED_BINARY slot selection) |
| RoomConfig stage | **10 (CONFIRMED_BINARY)** | `get_room_config_stage(8, 0)` = 1+((8-1)>>1)*3 = 10 (NOT Utero 11); see `get_room_config_stage_stage7_8_alt.md` |
| BossPool index | **10 (CONFIRMED_BINARY)** | pool == ORIGINAL rcs; rcs = 10 confirmed; pool 10 continues (advanced) from Womb I's selection |
| XL eligibility | **never (even stage)** | curse logic: Labyrinth only on odd stages below Stage 8; choice 0 consumes the selector and leaves the curse empty |
| Target room count | **20 NORMAL / 22-23 HARD (CONFIRMED_BINARY)** | `min(stage*10/3+5+bit, 20)`; stage 8 -> min(31+bit,20)=20; HARD `+2+bit` |
| Dead ends | **6 (CONFIRMED_BINARY)** | `(stage != 1) + 5` |
| Difficulty window | NORMAL 5..10 / HARD 10..15 (**PARTIAL_BINARY**) | validated through the full clean-vs-reference differential (100/100) |
| Planetarium chance | `1.4099999` (documentation only) | gate is False on canonical Womb (no collectible), so the chance is never consumed; value OPEN, recorded for documentation only |

## Stage-8 gate audit (BINARY-CONFIRMED)

Identical to Womb I: Type8/Shop/Treasure ordinary blocks execute
unconditionally (only a level_stage==10 gate exists in the region); the
Planetarium block consumes the unconditional 0x0033A961 draw and skips;
post-layout tail `-9`/`-10` both skipped → **28 persistent Level RNG draws,
same sequence as Depths II/Womb I**.

## Differential evidence

- `research/binary/womb2_100_differential_report.json`: 100 ordered
  comparisons (50 NORMAL + 50 HARD), 0 mismatches, all milestones matched
  (M5/M6/M7/late + post-layout tail).
- `scripts/differential_womb2_full.py` re-runs the corpus.

## Implementation

`floor_init(_reference).py` (`derive_womb2_topology_inputs`),
`generation_state.py` (`CanonicalWomb2Profile`),
`womb2_full_pipeline(_reference).py`, `womb2_lifecycle.py`
(next_level_stage=9 = Sheol, not implemented — lifecycle ends there),
preview registry; tests `tests/unit/test_womb_floor_init.py`,
`tests/differential/test_womb_full_pipeline_differential.py`.
