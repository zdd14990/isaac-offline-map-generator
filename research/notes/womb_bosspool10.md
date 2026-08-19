# Womb BossPool 10

Status: **CONFIRMED_BINARY** (pool index convention + local `bosspools.xml`).

## Index mapping

The game's BossPool array index is the XML pool position + 1 (special/greed
pools are not part of the ORIGINAL chapter indexing):

| index | XML pool | rcs (ORIGINAL) |
|---|---|---|
| 1  | basement      | 1 |
| 4  | caves         | 4 |
| 7  | depths        | 7 |
| **10** | **womb**  | **10** |
| 11 | utero         | — |
| 12 | scarred womb  | — |
| 19 | downpour      | alt I |
| 20 | dross         | alt II |
| 21 | mines         | alt I |
| 23 | mausoleum     | alt I |

This matches the repo constants `BASEMENT_POOL_INDEX=1`, `CAVES_POOL_INDEX=4`,
`DEPTHS_POOL_INDEX=7` and the confirmed rule "pool index == ORIGINAL
room-config stage". `WOMB_POOL_INDEX = 10`.

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

## Womb I -> Womb II inheritance

Same pattern as Caves I->II and Depths I->II (repo lifecycle functions):

- both floors use rcs 10 / pool index 10;
- Womb I selection mutates the persistent pool-10 RNG and commits permanent
  removals on success;
- Womb II resumes from the Womb-I snapshot (`pool_states[10]` =
  `womb1.final_boss_pool_state`, removals carried) — never a fresh pool.

The `CanonicalRunGenerationSnapshot` already carries all 37 pool RNG states
and the permanent-removal set, so no new snapshot fields are required for
pool 10.
