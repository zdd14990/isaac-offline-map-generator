# Womb BossPool 10

Status: **CONFIRMED_BINARY** (pool index convention + local `bosspools.xml`).

## Index mapping

The ORIGINAL-route pools coincide with both the XML file order + 1 and the
room-config stage.  The ALT pools are indexed by the hardcoded name->index
table inside the `bosspools.xml` parser (RVA 0x421bf0) and equal the
room-config stage (27..32) — **not** the XML file position + 1 (19..24).
See `alt_route_stage_type_lifecycle.md` for the extracted table.

| index | pool | rcs |
|---|---|---|
| 1  | basement      | 1 |
| 4  | caves         | 4 |
| 7  | depths        | 7 |
| **10** | **womb**  | **10** |
| 11 | utero         | — |
| 12 | scarred womb  | — |
| 27 | downpour      | 27 (alt I) |
| 28 | dross         | 28 (alt II) |
| 29 | mines         | 29 (alt I) |
| 30 | ashpit        | 30 (alt II) |
| 31 | mausoleum     | 31 (alt I) |
| 32 | gehenna       | 32 (alt II) |
| 33 | corpse        | 33 |

This matches the repo constants `BASEMENT_POOL_INDEX=1`, `CAVES_POOL_INDEX=4`,
`DEPTHS_POOL_INDEX=7` and the confirmed rule "pool index == room-config
stage". `WOMB_POOL_INDEX = 10`.

## Pool 10 entries (`bosspools.xml`, pool name "womb")

```xml
<pool name="womb" doubletrouble="3800">
    <boss id="7"  weight="1"    />  <!-- Scolex -->
    <boss id="49" weight="1"    />  <!-- Mama Gurdy -->
    <boss id="31" weight="1"    />  <!-- Lokii -->
    <boss id="53" weight="1"    />  <!-- Mr. Fred -->
    <boss id="16" weight="1"    />  <!-- Blastocyst -->
    <boss id="72" weight="0.25" />  <!-- The Matriarch -->
</pool>
```

Order is the XML order; shuffle uses pool seed slot 10 (`derive_pool_seeds`)
with the confirmed Fisher-Yates pass.

## Womb II boss is FIXED (not pool 10) — NEW FINDING (round 5)

`Level__select_boss_id` (0x422830) switches on **level_stage** 6..12 before
any pool selection: ORIGINAL level 8 -> Mom's Heart (8) (or It Lives! 25
under a flag condition), level 6 -> Mom (6); ALT level 8 -> Mother (88),
level 6 -> Mom-Mausoleum (89). Therefore:

- Womb II (level 8, ORIGINAL) boss = **Mom's Heart (8)** — the pool-10 RNG is
  NOT advanced and nothing is committed to the removal set on Womb II;
- Womb I XL second boss (select_boss_id(level_stage+1=8, type 0)) = fixed
  Mom's Heart (8), not a pool-10 pick;
- Depths II (level 6) boss = **Mom (6)** — same latent fix on the ORIGINAL
  route (the earlier pool-7 pick for level 6 was a clean-vs-reference
  invisible bug, now corrected).

See `alt_route_stage_type_lifecycle.md` for the full switch table.

## Womb I -> Womb II inheritance (revised)

- Womb I (level 7) uses rcs 10 / pool index 10 (weighted pick), mutating the
  persistent pool-10 RNG and committing removals on success;
- Womb II (level 8) uses the FIXED boss (Mom's Heart 8) — pool 10 resumes
  from the Womb-I snapshot unchanged (`pool_states[10]` =
  `womb1.final_boss_pool_state`, which is now the post-Womb-I state with no
  Womb-II advance).

The `CanonicalRunGenerationSnapshot` already carries all 37 pool RNG states
and the permanent-removal set, so no new snapshot fields are required.
