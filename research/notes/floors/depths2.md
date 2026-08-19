# Depths II — ORIGINAL route reconstruction

Frozen executable: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

External gameplay validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

This note covers canonical LevelStage 6 entered from the confirmed Depths-I
generation snapshot. Depths II shares the Depths RoomConfig stage (7) and the
Depths BossPool (index 7) with Depths I; the pool-7 RNG state is inherited
(advanced) from Depths I.

## Diff-first table

| Feature | Depths I (Stage 5) | Depths II (Stage 6) | Evidence |
|---|---|---|---|
| Stage seed slot | 5 | 6 | `get_initial_stage_seed(seed, 6)` |
| Topology target | `min(21+bit, 20)` | `min(25+bit, 20)` | `0x00340E10` |
| cap 20 | binding | binding | same `min(..., 0x14)` |
| Dead ends | 6 (7 XL) | 6 | `(stage != 1) + 5` |
| XL | possible (odd) | impossible (even) | `can_apply_labyrinth` `0x003385C0` odd-only |
| RoomConfig stage | 7 | 7 | `1 + (stage-1)//2*3` |
| BossPool | 7 (run-start) | 7 (advanced from Depths I) | shared Chapter-3 pool |
| Difficulty window | NORMAL (1,5)/(1,10) XL; HARD (5,10)/(5,15) XL | NORMAL (5,10); HARD (10,15) | even-stage branch |
| Planetarium | `f32(4*0.2+0.01)` | `f32(5*0.2+0.01)` | `GetPlanetariumChance` |

## Floor entry

Level RNG uses initial stage-seed slot 6 with shift index 35. Curse gate
denominator 80 (NORMAL) / 40 (HARD). Even Stage 6 never satisfies the
Labyrinth predicate, so curse-selector choice 0 leaves the curse empty;
choices 1..5 map to Lost/Darkness/Unknown/Maze/Blind.

## Topology contract

```text
base = min(floor(6 * 10 / 3) + 5 + (Next & 1), 20)   # 25 or 26 -> capped 20
```

- non-XL: 20 (24 with Lost);
- HARD adds `2 + bit`.

Required dead ends are six. Difficulty windows: NORMAL (5..10), HARD (10..15).
The `07.depths.stb` RoomConfig stage is 7; allowed shape mask `0x1FFE`.

## BossPool continuity

`get_room_config_stage(6, ORIGINAL)` returns 7 (same as Stage 5), so Depths II
shares the Depths BossPool (index 7). The pool's persistent RNG state is
inherited (advanced) from the Depths-I snapshot — the Depths-II boss selection
continues the same pool rather than starting from the run-start state.

## Condition matrix

The post-Treasure condition blocks are the same shared predicates as every
prior floor (see `basement1_secret_pipeline`). On the canonical Depths II
profile:

| Block | Behavior |
|---|---|
| Planetarium | ALWAYS_EXECUTED |
| Dice/Sacrifice | ALWAYS_EXECUTED |
| Library | ALWAYS_EXECUTED |
| Curse | ALWAYS_EXECUTED |
| MiniBoss | ALWAYS_EXECUTED |
| Challenge | ALWAYS_EXECUTED |
| Chest/Arcade | ALWAYS_EXECUTED |
| Isaac/Barren | ALWAYS_SKIPPED |
| route blocks (3) | ALWAYS_SKIPPED |

## Implementation

- `src/isaacmap/floor_init.py`: `derive_depths2_topology_inputs` (+ reference);
- `src/isaacmap/depths2_full_pipeline.py`: accepted-layout composition;
- `src/isaacmap/depths2_full_pipeline_reference.py`: mechanical reference;
- `src/isaacmap/depths2_lifecycle.py`: lifecycle handoff;
- `tests/differential/test_depths2_full_pipeline_differential.py`: differential.

Status: `CONFIRMED_BINARY` (20,000-seed reference/clean differential, zero
mismatch).
