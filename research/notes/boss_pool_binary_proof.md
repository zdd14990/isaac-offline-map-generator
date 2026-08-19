# BossPool binary proof

Profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Algorithm evidence:

- initialization, 37-seed derivation, entry layout and init-time shuffle:
  `CONFIRMED_BINARY`;
- fresh ordinary Basement weighted selection core and persistent/local state
  boundary: `CONFIRMED_BINARY`;
- fresh ordinary Basement I attempt/commit lifecycle, including geometry-failure
  retry: `CONFIRMED_BINARY`;
- inherited canonical Basement-pool remap/fallback/reset behavior used by
  Basement II: `CONFIRMED_BINARY` at the isolated BossPool leaf;
- optional character/unlock/game-mode overrides and arbitrary continue state:
  outside the canonical profile and rejected by the current entry point.

External validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Functions and callers

| Function | RVA | Evidence |
|---|---:|---|
| BossPools XML/init consumer | `0x000218E0` | 37-slot seed loop, XML load and per-pool shuffle |
| BossPool entry availability | `0x000217A0` | achievement/removal predicates |
| BossPool entry removed | `0x00021720` | persistent and per-level bitsets |
| BossPool weighted pick | `0x00022620` | ordered binary32 cumulative scan, repick/fallback |
| Level boss identity selector | `0x00022830` | pool selection, seven pre-rolls, override branches, local weighted selector |
| Game initialization caller | `0x002F8140` | owns call site `0x002F8579` |
| BossPool init call | `0x002F8579` | pushes `Game+0x1BB88`, sets `ECX=Game+0x1AF70`, calls `0x000218E0` |
| BossPool state/continue loader | `0x0028CDC0` | reinitialization and restored-state lifecycle |
| MT19937 seed | `0x004FD3C0` | standard 624-word initialization |
| MT19937 next | `0x004FD410` | twist and temper used by init shuffle |

## Structure

BossPools contains 37 fixed slots of stride `0x3C`.  Per slot:

```text
+0x18  entry vector begin
+0x1C  entry vector end
+0x20  entry vector capacity end
+0x24  total current weight (binary32)
+0x28  persistent xorshift seed
+0x2C  shift 1
+0x30  shift 2
+0x34  shift 3
+0x38  double/alternate-boss field
```

Entry stride is `0x14`:

```text
+0x00  boss id
+0x04  current weight
+0x08  initial weight
+0x0C  achievement/condition id
+0x10  alternate/double-trouble boss id
```

The current merged `bosspools.xml` exposes 25 named resource pools, while the
runtime table still has 37 fixed config-stage slots.  The custom game parser
accepts the installed file's non-strict outer closing tag, so the offline
loader intentionally does not use a strict general XML parser.

## Exact 37-pool seed derivation

At call RVA `0x002F8579` the caller passes `_gameStartSeed`, not the stage
seed.  RVA `0x000218E0` performs exactly 37 chained advances with index 26:

```text
state[0] = gameStartSeed
for n = 0..36:
    state[n+1] = xorshift32(state[n], 3, 13, 7)
    pool[n].rng.seed = state[n+1]
    pool[n].rng.shifts = (2, 21, 9)  // index 17
```

Thus `pool0=f(start)` and `pool1=f(pool0)`.  Original Basement maps to config
stage/pool index 1, not slot 0.

For `gameStartSeed=0x12345678`, the first four fixed-slot seeds are:

```text
4B73F4CE F2B1C483 1343572B 767FD835
```

## Deterministic initialization shuffle

After parsing the XML and optional overlay, the initializer loops through all
37 pools.  For each non-empty pool:

1. initialize MT19937 with that pool's xorshift seed;
2. for `i = count-1` down to `1`, draw `j = mt.next() % (i+1)`;
3. swap the entire `0x14`-byte entries at `i` and `j`.

This is an initialization-time Fisher-Yates shuffle.  It does not advance the
pool's persistent index-17 xorshift object.  The MT state is not the later Boss
selection RNG.  Reload/continue paths can invoke initialization again and then
restore persistent state; this lifecycle is why a complete offline state
contract must distinguish a fresh run from a continue.

## Basement source pool

Ordered source entries before shuffle are:

```text
id 1  weight 1.00
id 17 weight 1.00
id 2  weight 1.00
id 44 weight 1.00
id 64 weight 0.25
id 56 weight 1.00
id 65 weight 0.25
id 20 weight 0.25
id 13 weight 1.00
id 60 weight 1.00
id 84 weight 1.00
```

## Selection and persistence

`Level::select_boss_id` derives the pool index from
`Level::get_room_config_stage(stage, stageType)`.  Difficulty is not the direct
pool-index input.  On the ordinary path it advances the chosen persistent
pool RNG seven times, checks character/game mode/unlock/special-boss branches,
then copies the resulting RNG fields to a local weighted selector.

The local selector advances for `BossPool::PickBoss`; its result is converted
through the current x86 binary32 `RandomFloat` path and scanned against the
shuffled entry vector in order.  Availability considers current vs initial
weight, achievement condition, removed bitsets and a stage-specific exclusion.
The pick helper has repick and circular fallback behavior; the outer selector
retries and finally returns Monstro id 1 after ten failed attempts.

The exact inherited-pool path is locked by
`research/binary/boss_pool_repick_binary_verification.json`. A rejected entry
remaps the current target as binary32
`((cumulative_after - target) / entry.weight) * total`; it does not consume a
second local draw. The tenth scan enters a circular first-eligible fallback.
If that still returns null, the caller clears both removal bitsets for every
entry, advances the local copy and tries again.

The persistent pool object is left after the seven pre-rolls.  The weighted
local draw is not written back.  The selected id is marked in the manager's
per-level removal bitset at manager `+0x8BC`.

At the outer attempt-loop head, RVA `0x003382C0` clears only that per-level
bitset.  A failed Boss/Type8/Shop/Treasure geometry attempt therefore retains
the seven persistent advances, but does not permanently remove the failed
boss.  Success calls RVA `0x00021B50`, which merges the per-level bitset into
the permanent removed bitset and then clears it.  The exact field-by-field
transaction is recorded in `generation_retry_semantics.md`.

## Boss configuration is a separate step

Boss identity selection does not select the Boss room STB variant or geometry.
`Level::place_post_topology_rooms` then:

1. advances Level RNG at RVA `0x003394A4`;
2. selects Boss RoomConfig through RVA `0x00339080`, using private index 39 and
   per-call RoomConfig index 7;
3. rejects variants 3700..3849 with up to 50 additional private draws (51
   selections including the first);
4. passes the accepted shape/door mask to `LevelGenerator` at call RVA
   `0x003394F2`;
5. assigns the descriptor at call RVA `0x00339528`.

If no compatible distance>1 dead end exists, geometry returns null and the
outer generation loop rejects the topology.  This was observed as a static
control-flow consequence and exercised by differential seed `0x00000CAE`;
it is not a gameplay oracle observation.

## Implementation and tests

- mechanical reference: `src/isaacmap/boss_pool_reference.py`;
- readable implementation: `src/isaacmap/boss_pool.py`;
- comparator: `src/isaacmap/boss_pool_differential.py`;
- tests: `tests/unit/test_boss_pool.py`;
- inherited-state tests: `tests/unit/test_basement2_boss_pool.py`;
- combined mass report:
  `research/binary/basement1_pipeline_differential_report.json`.

The combined report covers 10,000 NORMAL and 10,000 HARD start seeds through
Treasure, including every outer retry and final persistent BossPool state.
The BossPool helper's optional noncanonical branches remain represented by
the explicit input contract; the public exact path refuses those states.
