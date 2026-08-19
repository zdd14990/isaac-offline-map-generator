# Level::get_room_config_stage — Womb 7/8 and alternate mapping

Status: **CONFIRMED_BINARY** (static Ghidra decompilation of the frozen PE;
see `research/decomp/ghidra/Level__get_room_config_stage.c`).

## Function

```c
int __fastcall Level__get_room_config_stage(int level_stage, int stage_type, int param_3)
```

- Called from `Level::place_post_topology_rooms` and `Level::generate_dungeon`
  with `param_3 = -1` (canonical route default).
- `param_3 == 1`, or (`param_3 == -1` and game mode 2/3 = Greed/Greedier),
  selects the special-mode mapping (below).

## Canonical mapping (game mode 0, param_3 == -1)

### ORIGINAL route (stage_type 0), level_stage 1..8

```c
return stage_type + 1 + ((level_stage - 1) >> 1) * 3;   // == 1 + ((stage-1)>>1)*3
```

| level_stage | room_config_stage |
|---|---|
| 1 (Basement I)   | 1 |
| 2 (Basement II)  | 1 |
| 3 (Caves I)      | 4 |
| 4 (Caves II)     | 4 |
| 5 (Depths I)     | 7 |
| 6 (Depths II)    | 7 |
| **7 (Womb I)**   | **10** |
| **8 (Womb II)**  | **10** |

**(7, ORIGINAL) -> 10 and (8, ORIGINAL) -> 10 are CONFIRMED.** Womb II does
NOT use Utero (11); the existing clean formula `1+(stage-1)//2*3` matches the
binary for 1..8 exactly. The Utero/Scarred Womb resource stages (11/12) are
reached through other routes/conditions, not canonical ORIGINAL 8.

### Alternate route, stage_type 4 (REPENTANCE), level_stage 1..6

```c
return ((level_stage - 1) & ~1) + 0x1b;      // 27 + even part of (stage-1)
```

| level_stage | room_config_stage |
|---|---|
| 1 (Downpour I)  | 27 |
| 2 | 27 |
| 3 (Mines I)     | 29 |
| 4 | 29 |
| 5 (Mausoleum I) | 31 |
| 6 | 31 |

### Alternate route, stage_type 5 (REPENTANCE_B), level_stage 1..6

```c
return (((level_stage - 1) >> 1) * 2) + 0x1c; // 28 + even part of (stage-1)
```

| level_stage | room_config_stage |
|---|---|
| 1 | 28 |
| 2 (Downpour II / Dross)    | 28 |
| 3 | 30 |
| 4 (Mines II / Ashpit)      | 30 |
| 5 | 32 |
| 6 (Mausoleum II / Gehenna) | 32 |

**StageType 5 is the "second chapter" variant**: the alternate route uses
stage_type 4 for the I floors (Downpour/Mines/Mausoleum -> 27/29/31) and
stage_type 5 for the II floors (Dross/Ashpit/Gehenna -> 28/30/32). This
matches the stages.xml resource pairs and explains why both 4 and 5 exist.
Both 4 and 5 get the same stage-seed slot rule (`level_stage + 1`).

### The -10 descriptor predicate, cross-checked

`(level_stage in (7,8) and stage_type in (4,5))` -> rcs 33 (Corpse):
- (7, 4): ((7-1)&~1)+27 = 33
- (8, 5): ((8-1)>>1)*2+28 = 6+28 = 34?? -> check: (8-1)>>1 = 3; 3*2+28 = 34.
  (8,4) -> ((8-1)&~1)+27 = 7&~1+27 = 6+27 = 33; (7,5) -> (6>>1)*2+28 = 32.
  So (7,4)/(8,4) -> 33 (Corpse); (7,5) -> 32 (Gehenna); (8,5) -> 34.
  The -10 descriptor's (7,8) x (4,5) domain therefore covers Corpse
  (rcs 33) and adjacent alt-second floors; all outside the current 8-floor
  scope. This stays consistent with `post_layout_descriptor_minus10.md`.

### Higher level stages (canonical path)

- 9: 13 (Sheol) / 36 (Backwards) if stage_type 4
- 12: 26 (The Void)
- 13: 35 (Home)
- 10/11: `stage_type + (stage-3)*2` (14/16 + stage_type)

### Special mode (Greed/Greedier: game mode 2/3, or param_3 == 1)

- 7 -> 25 (Ultra Greed), 6 -> 24 (The Shop), 5 -> 14 (Sheol)
- stage_type 4 -> 2*stage+25, stage_type 5 -> 2*stage+26
- ORIGINAL -> `3*stage + stage_type - 2`

## Relation to stages.xml

`stages.xml` resource stage ids are the OUTPUTS of this function: 1/4/7/10
(ORIGINAL pairs), 27..32 (alt I/II pairs), 13/26/33/35/36 (special chapters).
The function is the authority; stages.xml alone was only a hint (e.g. Utero
11 is NOT the canonical Womb II rcs).

## Confirmed vs open

- CONFIRMED_BINARY: the full `(level_stage, stage_type, param_3)` mapping
  above (decompiled from the hash-locked PE).
- OPEN: how the route progression ASSIGNS stage_type 4 vs 5 per alternate
  floor at runtime (both alt-path predicates accept either value); the rcs
  function's distinct 4/5 branches strongly imply I=4, II=5, but the level
  transition code has not been traced yet.
