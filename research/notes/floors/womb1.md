# Womb I (LevelStage 7, ORIGINAL) — implementation complete

Status: **IMPLEMENTED, PARTIAL_BINARY.** Generation open on MAIN route stage 7
(bot token `7`, `/map B911 99AC 0 7`). Evidence grade intentionally
`PARTIAL_BINARY` (100-sample corpus, not 20k-class). ALT route remains
FAIL CLOSED.

## Confirmed parameters

| Parameter | Value | Source |
|---|---|---|
| LevelStage | 7 | level-stages enum (repo) |
| StageType | 0 (ORIGINAL) | main route |
| Stage-seed slot | 7 | `stage_seed.py` (CONFIRMED_BINARY slot selection) |
| RoomConfig stage | **10 (CONFIRMED_BINARY)** | `get_room_config_stage(7, 0)` = 1+((7-1)>>1)*3 = 10; see `get_room_config_stage_stage7_8_alt.md` |
| BossPool index | **10 (CONFIRMED_BINARY)** | pool == ORIGINAL rcs (`boss_pool.py`); rcs = 10 confirmed; entries Scolex(7)/Mama Gurdy(49)/Lokii(31)/Mr. Fred(53)/Blastocyst(16) w=1 + The Matriarch(72) w=0.25 |
| Target room count | **20 NORMAL / 22-23 HARD (CONFIRMED_BINARY)** | `generate_dungeon.c`: `min(stage*10/3+5+bit, 20)`; stage 7 -> min(28+bit,20)=20; HARD `+2+bit` |
| Dead ends | **6 (CONFIRMED_BINARY)** | `generate_dungeon.c`: `(stage != 1) + 5` |
| XL target | **36 NORMAL / 38-39 HARD (CONFIRMED_BINARY)** | XL: `min(base*18//10, 45)` (confirmed Depths-I pattern); base 20 -> 36; HARD +2+bit. **Correction:** the `target*3/5` block in `generate_dungeon` is gated on curse bit 0x80, NOT Labyrinth (bit 2) — it is a different curse, not the XL target |
| Difficulty window | NORMAL 1..5 / HARD 5..10 (**PARTIAL_BINARY**) | validated through the full clean-vs-reference differential (100/100) |
| Planetarium chance | `1.2099999` (documentation only) | gate is False on canonical Womb (no collectible), so the chance is never consumed; value OPEN, recorded for documentation only |

## Stage-7 gate audit (BINARY-CONFIRMED)

- Type8/Shop/Treasure (`0x00339A87..0x0033A3FF`): disassembly shows only a
  `cmp [esi], 0xa` (level_stage==10) gate; **no stage-7/8-specific gate** —
  the ordinary blocks execute unconditionally on canonical Womb.
- Post-Treasure region `0x0033A410..0x0033A940`: embedded function data, no
  stage gates.
- Planetarium (`0x0033A8F7..0x0033AB45`): gate `stage<7 || (stage<9 && 0x6e)
  || stage==10`; canonical Womb (no collectible) skips select/geometry/chance
  but **consumes the unconditional 0x0033A961 selector-seed Level draw**.
- Post-layout tail: `-9` (rcs==13) skipped, `-10` (stage_type 4/5 AND
  level_stage 7/8) skipped → **28 persistent Level RNG draws, identical
  sequence to Depths II.**

## Differential evidence

- `research/binary/womb1_100_differential_report.json`: 100 ordered
  comparisons (50 NORMAL + 50 HARD), 0 mismatches, all milestones matched
  (M5 through-treasure incl. Boss/Type8/Shop/Treasure, M6 secret, M7 ultra,
  late defaults, post-layout tail 28-draw sequence).
- Targeted XL fixture: seeds 106/244/1381 (NORMAL) carry the Labyrinth curse
  (mask 2, target 36, dead ends 7); all matched clean-vs-reference; seed 106
  accepted 37 rooms with an additional boss (7, pool 10) at room 37.
- `scripts/differential_womb1_full.py` re-runs the corpus.

## Root-cause fix (round 4)

The reference Womb pipeline originally resumed pool 10 with `d2.final_boss`
(the Depths pool-7 state). Pool RNGs are independent per pool; pool 10 is
untouched until Womb, so its first-use state is its own game-start seed. Fixed
in `womb1_full_pipeline_reference.py` to use
`derive_pool_seeds_reference(start_seed)[WOMB_POOL_INDEX]`.

## Implementation

`floor_init(_reference).py` (`derive_womb1_topology_inputs`),
`generation_state.py` (`CanonicalWomb1Profile`),
`womb1_full_pipeline(_reference).py`, `womb1_lifecycle.py`,
`boss_pool(_reference).py` (`WOMB_POOL_INDEX=10`, `pools["womb"]`),
preview registry + `10.womb.stb` resource; tests
`tests/unit/test_womb_floor_init.py`, `tests/differential/test_womb_full_pipeline_differential.py`.
