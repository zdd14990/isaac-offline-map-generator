# Depths I — ORIGINAL route reconstruction

Frozen executable: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

External gameplay validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

This note covers canonical LevelStage 5 entered from the confirmed Caves-II
generation snapshot. Depths I is the first floor where the target-count cap of
20 applies, and (being odd) it is the first floor after Caves I where Labyrinth
is possible again.

## Diff-first table

| Feature | Caves II (Stage 4) | Depths I (Stage 5) | Evidence |
|---|---|---|---|
| Stage seed slot | 4 | 5 | `get_initial_stage_seed(seed, 5)` |
| Topology target | `min(18 + bit, 20)` | `min(21 + bit, 20)` = 20 | `Level::generate_dungeon` `0x00340E10` |
| cap 20 | not binding | binding (21/22 → 20) | same `min(..., 0x14)` |
| Dead ends | 6 | 6 (7 XL) | `(stage != 1) + 5`, +1 XL |
| XL | impossible | possible (odd) | `Level::can_apply_labyrinth` `0x003385C0` |
| RoomConfig stage | 4 | 7 | `get_room_config_stage` = `1 + (stage-1)//2*3` |
| BossPool | 4 (advanced from Caves I) | 7 (run-start state) | `get_room_config_stage(5,0)=7` |
| Difficulty window | NORMAL (5,10) / HARD (10,15) | NORMAL (1,5) / HARD (5,10); XL (1,10)/(5,15) | odd-stage branch |
| Planetarium | `f32(3*0.2+0.01)` | `f32(4*0.2+0.01)` | `GetPlanetariumChance` |
| lifecycle tail | shared | shared | even/odd both skip -9/-10 at stage 5 |

## Floor entry

Level RNG uses initial stage-seed slot 5 with shift index 35. Curse gate
denominator 80 (NORMAL) / 40 (HARD). Odd Stage 5 satisfies the Labyrinth
predicate (`odd && stage < 8 && game_mode ∉ {2,3}`), so curse-selector choice
0 retains Labyrinth (bit 2) and makes the floor XL; choices 1..5 map to
Lost/Darkness/Unknown/Maze/Blind.

## Topology contract

```text
base = min(floor(5 * 10 / 3) + 5 + (Next & 1), 20)   # 21 or 22 -> capped 20
```

- non-XL: 20 (24 with Lost);
- XL: 20 * 1.8 = 36 (cap 45 not reached);
- HARD adds `2 + bit` after the XL/Lost modifier.

Required dead ends are six (seven XL). Difficulty windows:

| Profile | Non-XL | XL |
|---|---:|---:|
| NORMAL | 1..5 | 1..10 |
| HARD | 5..10 | 5..15 |

The `07.depths.stb` RoomConfig stage is 7; allowed shape mask `0x1FFE`.

## BossPool

`get_room_config_stage(5, ORIGINAL)` returns 7, so Depths I selects the
Depths BossPool (index 7) seeded from `bosspools.xml["depths"]`:

```text
id 5, 15, 19, 46, 48, 58, 68, 74
```

The pool's persistent RNG state is the run-start state (no earlier floor
selects pool 7), inherited through the Caves-II snapshot. It is committed to
permanent removal only after Ultra and the late ordinary pass succeed.

## Implementation

- `src/isaacmap/floor_init.py`: `derive_depths1_topology_inputs` (+ reference);
- `src/isaacmap/depths1_full_pipeline.py`: accepted-layout composition;
- `src/isaacmap/depths1_full_pipeline_reference.py`: mechanical reference;
- `src/isaacmap/depths1_lifecycle.py`: lifecycle handoff;
- `tests/differential/test_depths1_full_pipeline_differential.py`: differential.

Status: `CONFIRMED_BINARY` (20,000-seed reference/clean differential, zero
mismatch).
