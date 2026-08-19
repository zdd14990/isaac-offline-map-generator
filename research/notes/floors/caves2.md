# Caves II — ORIGINAL route reconstruction

Frozen executable: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

External gameplay validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

This note covers canonical LevelStage 4 entered from the confirmed Caves-I
generation snapshot. Caves II shares the Caves RoomConfig stage (4) and the
Caves BossPool (index 4) with Caves I; the BossPool RNG state is inherited
(advanced) from Caves I rather than re-initialized.

## Diff-first table

| Feature | Caves I (Stage 3) | Caves II (Stage 4) | Evidence |
|---|---|---|---|
| Stage seed slot | 3 | 4 | `get_initial_stage_seed(seed, 4)` |
| Topology target | `min(15 + bit, 20)` | `min(18 + bit, 20)` | `Level::generate_dungeon` `0x00340E10` line 126 |
| Dead ends | 6 (7 XL) | 6 | `(stage != 1) + 5`; even stage never XL |
| XL | possible (Labyrinth, odd stage) | impossible (even stage) | `Level::can_apply_labyrinth` `0x003385C0` (odd-only) |
| BossPool | pool 4, initial state | pool 4, inherited (advanced) | `get_room_config_stage` returns 4 for stages 3 and 4 |
| RoomConfig stage | 4 | 4 | `get_room_config_stage` formula |
| Difficulty window | NORMAL (1,5)/(1,10) XL; HARD (5,10)/(5,15) XL | NORMAL (5,10); HARD (10,15) | even-stage branch |
| Shop | subtype 11 | subtype 11 | shared through-Treasure leaf |
| Treasure | stage-4 fallback | stage-4 fallback | shared through-Treasure leaf |
| Planetarium | `f32(2*0.2 + 0.01)` | `f32(3*0.2 + 0.01)` | `GetPlanetariumChance` |
| Dice/Sacrifice | canonical skip | canonical skip | shared predicates |
| Library | subtype ≤ 4 | subtype ≤ 4 | shared predicates |
| Curse | can retain Labyrinth | never Labyrinth | odd-only Labyrinth |
| MiniBoss | present | present | shared predicates |
| Challenge | present | present | shared predicates |
| Chest/Arcade | present | present | shared predicates |
| Secret | `CONFIRMED_BINARY` | shared | shared leaf |
| Ultra | `CONFIRMED_BINARY` | shared | shared leaf |
| late variants | stage-4 ROOM_DEFAULT | stage-4 ROOM_DEFAULT | shared late leaf |
| lifecycle tail | shared `0x0033D1D6..0x0033D94B` | shared | even stage skips -9/-10 |

## Floor entry

Level RNG uses initial stage-seed slot 4 with shift index 35. The ordinary
curse gate denominator is 80 (NORMAL) / 40 (HARD). Even Stage 4 never
satisfies the Labyrinth predicate (`odd && stage < 8 && game_mode ∉ {2,3}`),
so curse-selector choice 0 leaves the curse empty; choices 1..5 map to
Lost/Darkness/Unknown/Maze/Blind exactly as Basement II.

## Topology contract

```text
target = min(floor(4 * 10 / 3) + 5 + (Next & 1), 20)   # 18 or 19
```

Lost curse adds four; HARD adds `2 + bit`. Required dead ends are six. The
ordinary Caves RoomConfig stage is 4; difficulty windows are NORMAL (5..10)
and HARD (10..15). The allowed-shape mask is `0x1FFE` (Shapes 1..12).

## BossPool continuity

`get_room_config_stage(4, ORIGINAL)` returns 4 (same as stage 3), so Caves II
selects from the Caves BossPool (index 4). The pool's persistent RNG state is
inherited from the Caves-I lifecycle snapshot, so the Caves-II boss selection
continues the same pool rather than starting from the run-start seed.

## Implementation

- `src/isaacmap/floor_init.py`: `derive_caves2_topology_inputs` (+ reference);
- `src/isaacmap/caves2_full_pipeline.py`: accepted-layout composition;
- `src/isaacmap/caves2_full_pipeline_reference.py`: mechanical reference;
- `src/isaacmap/caves2_lifecycle.py`: lifecycle handoff;
- `tests/differential/test_caves2_full_pipeline_differential.py`: differential.

Status: `CONFIRMED_BINARY` (20,000-seed reference/clean differential, zero
mismatch).
