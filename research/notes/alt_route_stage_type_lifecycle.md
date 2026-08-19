# ALT route StageType lifecycle (1+..6+) — BINARY-CONFIRMED

Frozen binary: `Binding of Isaac: Repentance+ v1.9.7.17.J460`, SHA256
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`.
All addresses below are VAs; RVA = VA - 0x400000.

## The canonical ALT StageType sequence

```text
1+  Downpour I    level_stage 1   StageType 4   rcs 27   pool 27   slot 2
2+  Dross         level_stage 2   StageType 5   rcs 28   pool 28   slot 3
3+  Mines I       level_stage 3   StageType 4   rcs 29   pool 29   slot 4
4+  Ashpit        level_stage 4   StageType 5   rcs 30   pool 30   slot 5
5+  Mausoleum I   level_stage 5   StageType 4   rcs 31   pool 31   slot 6
6+  Gehenna       level_stage 6   StageType 5   rcs 32   pool 32   slot 7
```

The `4, 5, 4, 5, 4, 5` alternation is **forced**, not assumed:

1. `Level__get_room_config_stage` (decompiled, `get_room_config_stage_stage7_8_alt.md`):
   - StageType 4: `((stage-1)&~1)+27` -> 27 (st.1/2), 29 (st.3/4), 31 (st.5/6)
   - StageType 5: `((stage-1)>>1)*2+28` -> 28 (st.2), 30 (st.4), 32 (st.6)
2. `stages.xml` resource ids: Downpour 27, Dross 28, Mines 29, Ashpit 30,
   Mausoleum 31, Gehenna 32, Corpse 33.
3. Therefore Dross MUST be (2, StageType 5) to get rcs 28, Ashpit (4, 5) -> 30,
   Gehenna (6, 5) -> 32; the I floors take StageType 4 for 27/29/31.

## Transition machinery (RVAs)

| RVA | Function | Role |
|---|---|---|
| 0x744940 | `Level::Init` | reads `[Level+0]`=stage, `[Level+4]`=stage_type; **slot = stage + 1 iff stage_type in (4,5)**, capped at 13 (Home); log `"Level::Init m_Stage %d, m_StageType %d Seed %u"` |
| 0x7466d0 | stage/type setter | clamps stage to 0..13, stage_type to 0..5; writes `[Level]` and `[Level+4]`; sets `Game+0x26500` = 0xafc8 when (stage < 7 AND stage_type 4/5) else 0x8ca0 |
| 0x7467c0 | pre-Init alt fixup | alt-flag (`Game+0x2654c` bit 0x10000) set and Game stage 1..6: per-stage table `Game + 0x6746c + stage*0x320`; `+0x318` = chapter stage_type (4/5 alt), `+0x31c` = pairing flag; alt chapters call 0x7466d0 with stage-1/type-4 or stage/type-4 |
| 0x740e10 | `generate_dungeon` | reads `[Level+4]` for the alt modifiers (see floor-init matrix) |
| 0x7451ea | rcs call in generate_dungeon | `get_room_config_stage(stage, stage_type, -1)` |

The per-stage chapter-type table values (stages 1..6 -> 4/5) are also forced
by the rcs function + stages.xml (row 1-2 above); the table itself is built at
runtime (its region sits in `.reloc`), so its initial file bytes are not the
source of truth.

## BossPool index == rcs (27..32) — hardcoded name table

`BossPool__bosspools_xml_consumer` (0x4218e0) parses `bosspools.xml`; the
parser at 0x421bf0 contains a hardcoded name -> pool-index table (string
pointers in `.rdata` at 0xb1a620+):

```text
basement->1   cellar->2   burning basement->3   caves->4   catacombs->5
flooded caves->6   depths->7   necropolis->8   dank depths->9   womb->10
utero->11   scarred womb->12   blue womb->13   sheol->14   cathedral->15
dark room->16   chest->17   void->26   downpour->27   mines->29
mausoleum->31   corpse->33   dross->28   ashpit->30   gehenna->32
```

`select_boss_id` (0x422830) indexes the pool array by `rcs*0x3c` inside the
BossPools manager (`Game+0x1af70`), so pool index == rcs holds for ALT too
(downpour 27, dross 28, mines 29, ashpit 30, mausoleum 31, gehenna 32,
corpse 33). **The earlier "XML position + 1" guess in
`womb_bosspool10.md` was only coincidentally correct for the ORIGINAL pools
(1/4/7/10); it is WRONG for alt pools (position 19..24).** Corrected here.

Pool entries (bosspools.xml): downpour = Beelzeblub(75)/Wormwood(76)/
Rainmaker(77)/Min Min(91) w=1; dross = 75/76/Clog(92)/Colostomia(95)/
Turdlet(97); mines = Reap Creep(74)/Tuff Twins(80)/Hornfel(82)/Great
Gideon(83); ashpit = The Pile(73)/The Shell(96)/Singe(93)/Great Gideon(83)/
Clutch(102); mausoleum = The Siren(79)/The Heretic(81); gehenna = The
Visage(78)/Horny Boys(101).

## Fixed bosses by level (select_boss_id switch) — NEW FINDING

`select_boss_id(this=Game+0x1af70, arg1=level_stage, arg2=stage_type,
arg3=manager)`; after the Home (level 13) special, it switches on
**level_stage** 6..12 (`lea ecx,[edi-6]; cmp ecx,6; jmp table`):

- stage_type NOT 4/5 (incl. ORIGINAL 0):
  - level 6 -> **Mom (6)**; level 8 -> **Mom's Heart (8)** (or It Lives! 25
    when a flag/mode condition holds); level 10 -> Satan (24) / Isaac (39,
    stage_type 1); level 11 -> The Lamb (54) / ??? (40); level 12 ->
    Delirium (70).
- stage_type 4/5 (ALT):
  - level 6 -> **Mom-Mausoleum (89)**; level 8 -> **Mother (88)**; level
    10/11 -> ??? (40); level 12 -> Delirium (70). Levels 1..5 (and 7) fall
    through to the weighted pool pick (pools 27..31 / 33).

Boss rooms: all fixed ids exist in `00.special rooms.stb` (type 5, subtype =
boss id); additionally `31.mausoleum.stb` carries the 89 room and
`33.corpse.stb` the 88 room.

**Impact on the ORIGINAL route (must be fixed alongside ALT):** Depths II
(level 6) and Womb II (level 8) bosses are FIXED (Mom / Mom's Heart), not
pool picks. The current repo implementation (rounds 1-4) selects from pools
7/10 for those floors — a latent binary-truth violation invisible to the
clean-vs-reference differentials (both sides shared the omission). The pool
RNG for pools 7/10 is therefore NOT advanced on Depths II / Womb II, and the
XL second boss at level_stage+1=8 (Womb I XL, Depths I XL) is also fixed.

## Transition conditions summary

- ALT entry: `Game+0x2654c` bit 0x10000 (Repentance alt-path flag), game
  mode not 2/3.
- First/second-half predicates (used by generate_dungeon for the -3 target
  and +1 dead-ends modifiers):
  - `alt_path_first_half_predicate` (0x74ef70): stage_type in (4,5) AND
    (stage == 2 OR (stage == 1 AND Labyrinth curse bit 2)).
  - `alt_path_second_half_predicate` (0x74efd0): stage_type in (4,5) AND
    (stage == 4 OR (stage == 3 AND Labyrinth bit 2)).
  - I.e. chapters 1/2 of the ALT route (Downpour/Dross, Mines/Ashpit) get the
    modifiers; Mausoleum/Gehenna (stages 5/6) do NOT.
- Stage-seed slot: `stage + 1` for stage_type 4/5 (Level::Init), capped 13.
