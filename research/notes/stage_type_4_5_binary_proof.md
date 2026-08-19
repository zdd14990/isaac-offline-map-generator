# StageType 4/5 (alternate route) semantics — current evidence

Status: **partially confirmed, partially open**. This file records exactly
what is binary-confirmed vs what still needs verification before the alternate
chapters can be generated.

## Frozen binary

`Binding of Isaac: Repentance+ v1.9.7.17.J460`, SHA256
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`.

## StageType enum (repo-confirmed)

`src/isaacmap/stage_seed.py`:

```python
STAGETYPE_REPENTANCE = 4
STAGETYPE_REPENTANCE_B = 5
```

`LEVEL_STAGE_MIN/MAX = 0..13`, `STAGE_SEED_COUNT = 14`.

## Chapter table (authoritative game data: stages.xml)

Resource stage ids (the `room_config_stage` used by RoomConfig selection):

| Chapter (I/II pair)     | resource stage id |
|-------------------------|-------------------|
| Basement (MAIN 1/2)     | 1                 |
| Caves (MAIN 3/4)        | 4                 |
| Depths (MAIN 5/6)       | 7                 |
| Womb (MAIN 7/8)         | 10                |
| Utero (alt womb II)     | 11                |
| Scarred Womb            | 12                |
| Blue Womb               | 13                |
| Downpour I              | 27                |
| Dross (Downpour II)     | 28                |
| Mines I                 | 29                |
| Ashpit (Mines II)       | 30                |
| Mausoleum I             | 31                |
| Gehenna (Mausoleum II)  | 32                |
| Corpse                  | 33                |
| Home                    | 35                |

The ORIGINAL-route mapping `room_config_stage = 1 + (level_stage-1)//2*3`
(Basement 1, Caves 4, Depths 7, Womb 10) is the repo's confirmed formula for
level_stage 1..6; its extension to level_stage 7/8 (=10) is a **prediction**
that must be verified against the binary `get_room_config_stage` before Womb
II generation is claimed (Utero/Scarred Womb exist as separate resource
stages, so 8 -> 10 is not guaranteed).

## Stage-seed slot (CONFIRMED_BINARY, repo)

`floor_stage_seed_slot(level_stage, stage_type)` in `stage_seed.py`:

```python
adjusted = level_stage + (stage_type in (STAGETYPE_REPENTANCE, STAGETYPE_REPENTANCE_B))
return min(adjusted, LEVEL_STAGE_MAX)   # 13 (Home slot)
```

So alternate floors use `level_stage + 1` seed slots: Downpour I -> slot 2,
Downpour II -> slot 3, Mines I -> slot 4, Mines II -> slot 5, Mausoleum I ->
slot 6, Mausoleum II -> slot 7, capped at Home (13). This is the "slot + 1"
rule the project already encodes; it is part of the confirmed stage-seed
reconstruction, not a guess.

## What the post-layout tail proves about stage_type 4/5

From `post_layout_descriptor_minus10.md` (binary): the only stage_type-
dependent branch in the tail `0x0033D1D6..0x0033D925` is the -10 descriptor
gate (`stage_type in (4,5) AND level_stage in (7,8)`), which is **skipped for
every alternate chapter at level_stage 1..6**. No other tail branch reads
stage_type. Consequently the tail's persistent Level RNG sequence for an
alternate floor at level_stage 1..6 is identical to the ORIGINAL floor at the
same level_stage (28 draws).

## Open items before generation can be implemented

1. `get_room_config_stage(level_stage, stage_type)` for:
   - (7, 0) / (8, 0): predict 10; must verify (Utero/Scarred Womb ambiguity).
   - (1..6, 4/5): Downpour/Mines/Mausoleum use their own resource stages
     27..32; verify how the function maps level_stage -> alt resource stage.
2. Floor-init (`Level::Init` / `generate_dungeon` prologue) for stage_type
   4/5: target room count, dead ends, XL/curse eligibility, shape mask,
   blocked-cell rules. Must NOT be assumed identical to ORIGINAL.
3. BossPool index for alternate chapters (pool == rcs holds on ORIGINAL; the
   alt pools in bosspools.xml need their own index/entry verification).
4. Special-room pipeline (through-Treasure, Secret/Ultra, post-Treasure
   blocks) stage_type 4/5 branches.
5. RunGenerationState route fields: what the game persists across alt-route
   transitions (Downpour I -> II -> Mines I -> ... -> Mausoleum II).
