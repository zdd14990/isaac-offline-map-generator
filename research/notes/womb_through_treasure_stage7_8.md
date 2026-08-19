# Womb I/II through-Treasure gates (stage 7/8)

Status: **partially confirmed**. Boss and XL paths verified from
`Level__place_post_topology_rooms.c` (decompiled, hash-locked PE). Type8 /
Shop / Treasure sections not yet read line-by-line; their clean-model
stage-independence is stated with the evidence level noted per row.

## Function

`Level::place_post_topology_rooms` (`0x739370`, decompiled to
`research/decomp/ghidra/Level__place_post_topology_rooms.c`, 2735 lines)
contains the full post-topology generation: Boss -> Type8 -> Shop -> Treasure
-> post-Treasure specials -> Secret -> Ultra -> post-layout tail. Level fields:
`*param = level_stage`, `param[1] = stage_type`, `local_12c = rcs`.

## Verified rows (stage 7/8 = ORIGINAL, rcs 10)

| operation | stage7 | stage8 | predicate / RVA | RNG effect |
|---|---|---|---|---|
| Boss | executes | executes | `Level__select_boss_id(level_stage, stage_type, pool)`; pool derived from rcs(10) = pool 10; geometry via `post_topology_dispatch` + `assign_room_config` | 1 config seed draw + geometry draws (shared leaf) |
| XL second boss (stage 7) | executes when Labyrinth | n/a (even stage) | `select_boss_id(level_stage + 1, stage_type)` — same pool 10 since rcs(8,0)=10; RNG state saved before and **restored** after (`local_d8[0x60b5] = local_fc` + re-init shifts from `DAT_00b1f66c`) | 0 net persistent draws (rewound) |
| "additional multi-boss Stage 12 block" | skip | skip | `*local_d8 == 0xc` gate (Void only) | none |
| Labyrinth/XL gate | bit 2 of curse | n/a | `(~remove & (add|curse|used) & 2) == 0` — bit 0x02 = Labyrinth | branches to XL path |

## Not yet read line-by-line (clean-model stage-independence, unverified)

| operation | clean model | binary verification |
|---|---|---|
| Type8 / Super Secret | unconditional for canonical 1..6 | NOT YET read at 0x00339A87 region |
| Shop | unconditional (condition trace always True) | NOT YET read at 0x00339DB4 region |
| Treasure | unconditional | NOT YET read at 0x0033A76B region |
| Planetarium | stage-parameterized chance | NOT YET read |
| Dice/Sacrifice, Library, Curse, MiniBoss, Challenge, Chest/Arcade, Isaac/Barren | stage-gated, all false/true as modelled | NOT YET read |
| Secret | shared helper | NOT YET re-verified for 7/8 |
| Ultra Secret | shared helper | NOT YET re-verified for 7/8 |

The clean `basement1_pipeline.py` gates that are stage-specific (MiniBoss
`stage==1`, Chest `stage==2`, perimeter `stage==3`, multi-boss `stage==12`)
all evaluate false for 7/8 in the clean model; the gates that are
`stage >= 2` / `stage >= 3` evaluate true. Whether the BINARY has any
additional 7/8-specific gate inside Type8/Shop/Treasure remains to be read.
Until that is done, the Womb floors stay FAIL CLOSED.

## Required before implementation

1. Read 0x00339A87..0x0033A3FF (Type8/Shop/Treasure) and the post-Treasure
   section for any `level_stage` / `stage_type` gate at 7/8.
2. Confirm the `is_xl and level_stage in (3,5)` guard extension to 7 in the
   clean leaf is justified by the binary XL path (verified above: XL boss
   uses `stage+1`, pool 10, RNG rewind — stage-independent shape).
3. Confirm BossPool 10 resume in `CanonicalRunGenerationSnapshot`
   (`pool_states[10]` carried Depths II -> Womb I -> Womb II).
