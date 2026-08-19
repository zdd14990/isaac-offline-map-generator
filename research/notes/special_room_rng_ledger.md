# Special-room RNG object and consumption ledger

Profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Algorithm evidence: object ownership and all draws on the canonical fresh
Basement I path through Ultra are `CONFIRMED_BINARY`. External gameplay
status is `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Object identities

| Object / owner | Seed source and construction | Shift index | Lifetime | First / last established consumer |
|---|---|---:|---|---|
| `Level._generationRNG` at Level `+0x182D4` | selected stage seed; initialized before topology | 35 `(5,9,7)` | Persistent across outer topology/post-topology retries | floor initialization through post-topology and ordinary variant assignment |
| `LevelGenerator._rng` | one Level RNG draw passed to constructor at RVA `0x00341202` | 35 `(5,9,7)` | One generator object, persistent across outer retries; map/vectors are reset, RNG is not | topology and XL-only boss extension |
| BossPool master derivation scalar | `Seeds._gameStartSeed` at `Game+0x1BB88`; call RVA `0x002F8579` | 26 `(3,13,7)` | Temporary initialization chain of exactly 37 advances | produces pool seeds 0..36 |
| `BossPools.pool[i]._rng` at pool `+0x28` | chained master state for that pool | 17 `(2,21,9)` | Persistent BossPool object; selected pool advances seven times per ordinary `select_boss_id` invocation | boss identity selection and later stage boss selections |
| BossPool init-time shuffle MT19937 | reseeded from each `pool[i]._rng.seed` without advancing that xorshift object | N/A | Fresh MT state per pool during BossPool initialization/reload | Fisher-Yates only; not retained for Boss selection |
| `Level::select_boss_id` stack copy | copy of selected persistent pool RNG after its seven pre-rolls | 17 `(2,21,9)` | One weighted-pick attempt/loop local | `BossPool::PickBoss`; final local state is not stored back |
| Boss RoomConfig private RNG | one Level RNG draw at RVA `0x003394A4` | 39 `(5,15,17)` | Primary boss-config selector and its double-room rejection retries | RVA `0x0033930E` |
| `RoomConfig::select_room` local selector | caller-provided seed | 7 `(1,21,20)` | One concrete weighted selection call | xorshift at RVA `0x0042CBDE`; selected config weight then decays |
| Type 8 private RNG | one Level RNG draw at RVA `0x00339A87` | 9 `(2,5,15)` | 1 iteration, or 2 with collectible 589 | draw at RVA `0x00339B1E` per iteration |
| post-Type8 seed snapshot | one Level RNG draw at `0x00339BE7..0x00339C08`; copied to stack local and also stored back to Level RNG | initially same numeric state as Level RNG, but retained as a distinct seed value | Survives Shop/Treasure and later Level RNG mutation | seeds Secret and Ultra private streams |
| Shop subtype private stream | one continuing Level RNG draw at RVA `0x00339DB4` after the saved snapshot | 19 `(3,3,26)` | Shop subtype block only | four draws on the canonical fresh no-collectible path |
| Secret repeated-placement stream | copy of the post-Type8 seed snapshot | 1 (table at VA `0x00B1F4D4`) | Secret placement loop only | first config uses the snapshot directly; each subsequent iteration advances this private stream |
| Ultra config private stream | independent copy of the same post-Type8 seed snapshot | 71 (table at VA `0x00B1F81C`) | Ultra config block only | exactly one advance before type-29 RoomConfig selection; it does not own geometry |
| Curse private stream | one continuing Level RNG draw at RVA `0x0033B166` | 66 `(11,7,12)` | Curse block only | type-10 config seed, descriptor seed and conditional odd-state extra advance |

Equal seed values do not make these the same object.  In particular the Level
RNG continues through Shop/Treasure while Secret and Ultra later restart from
copies of the saved post-Type8 value, and Secret/Ultra use different shift
indices.

## BossPool initialization ledger

Call site RVA `0x002F8579` loads:

```text
seed = *(Game + 0x1BB88)          // Seeds._gameStartSeed
this = Game + 0x1AF70             // BossPools owner
BossPools::initialize(this, seed) // callee RVA 0x000218E0
```

Inside `0x000218E0`:

```text
state = gameStartSeed
for pool_index in 0..36:
    state = xorshift(state, index=26, shifts=(3,13,7))
    pool[pool_index].rng = RNG(state, index=17, shifts=(2,21,9))
```

This proves `pool[N] = f(pool[N-1])`; the pools are not independently hashed
from `(gameStartSeed, N)`.

## Fresh ordinary Basement Boss draw ledger

For original Basement, `Level::get_room_config_stage` returns pool index 1.
The selected pool object is `BossPools.pool[1]._rng`; the following seven
advances always occur before the ordinary weighted path:

| Draw | Binary RVA | Object identity | Shift | Reason / use |
|---:|---:|---|---:|---|
| 0 | `0x000229F8` | persistent `pool[1]._rng` | 17 | optional special-boss predicate 0 |
| 1 | `0x00022A02` | persistent `pool[1]._rng` | 17 | optional special-boss predicate 1 |
| 2 | `0x00022A0D` | persistent `pool[1]._rng` | 17 | optional special-boss predicate 2 |
| 3 | `0x00022A18` | persistent `pool[1]._rng` | 17 | optional double/alternate predicate |
| 4 | `0x00022A23` | persistent `pool[1]._rng` | 17 | optional special-boss predicate 4 |
| 5 | `0x00022A2E` | persistent `pool[1]._rng` | 17 | unconditionally consumed pre-roll |
| 6 | `0x00022A36` | persistent `pool[1]._rng` | 17 | unconditionally consumed pre-roll |
| 7 | `0x00022D04` | stack copy of `pool[1]._rng` | 17 | binary32 weighted BossPool selection; not written back |

The persistent final state is stored at:

```text
Game + 0x1AF70 + pool_index * 0x3C + 0x28
```

and remains the state after draw 6, not draw 7.

## Early ordinary Basement post-topology ledger

For a concrete run, `pre-state`/`post-state` fields are emitted by both
`special_rooms_reference.py` and `special_rooms.py`.  Static sites and object
boundaries are:

| Sequence | Binary RVA | Object | Shift index | Control-flow reason | Result use |
|---:|---:|---|---:|---|---|
| 0 | `0x003394A4` | persistent Level RNG | 35 | primary Boss selected | seed Boss-config private RNG |
| 1 | `0x0033930E` | Boss-config private RNG | 39 | first config or rejected 3700..3849 retry | seed one RoomConfig weighted selection |
| 2 | `0x0042CBDE` | one-call RoomConfig local | 7 | concrete boss STB selection | binary32 weighted threshold and weight decay |
| 3 | `0x00339A87` | persistent Level RNG | 35 | begin Type 8 pass | seed Type8 private RNG |
| 4 | `0x00339B1E` | Type8 private RNG | 9 | Type8 iteration 0/1 | seed concrete Type8 RoomConfig selection |
| 5 | `0x0042CBDE` | one-call RoomConfig local | 7 | concrete Type8 STB selection | binary32 weighted threshold and weight decay |
| 6 | `0x00339BE7` | persistent Level RNG | 35 | post-Type8 snapshot | saved seed for later Secret/Ultra and current Level state |
| 7 | `0x00339DB4` | persistent Level RNG | 35 | canonical Shop eligible | seed index-19 Shop subtype stream |
| 8..11 | `0x00339E04`, `0x00339E52`, `0x00339EB2`, `0x00339F46` | Shop subtype private RNG | 19 | canonical no-collectible subtype control flow | produces Shop subtype 11 |
| 12 | `0x0033A1C7` | persistent Level RNG | 35 | select Shop RoomConfig | seed stage-0 index-7 selector |
| 13 | `0x0042CBDE` | one-call RoomConfig local | 7 | concrete Shop STB selection | threshold and weight decay |
| 14 | `0x0033A455` | persistent Level RNG | 35 | Treasure rare subtype | `%100 == 0` selects subtype 1 |
| 15 conditional | `0x0033A4B8` | persistent Level RNG | 35 | non-rare Treasure branch | canonical no-collectible subtype 0 |
| 16 | `0x0033A76B` | persistent Level RNG | 35 | select Treasure RoomConfig | same seed is used by stage-1 then stage-0 fallback |
| 17 | `0x0042CBDE` | one-call RoomConfig local | 7 | concrete Treasure STB selection | threshold and weight decay |

Candidate scans (`DetermineBossRoom`, `GetNewEndRoom`) do not draw RNG.  Their
ordered vector scan and stable erase are deterministic but output-affecting.

## Post-Treasure through Secret

Planetarium, Dice/Sacrifice, Library, MiniBoss, Challenge, Chest/Arcade and
Isaac/Barren continue the persistent Level RNG at the callsites recorded in
`post_treasure_callgraph.md`. Each concrete RoomConfig selection creates a
one-call index-7 local selector. Curse alone receives a Level-draw seed for an
index-66 private stream.

The Secret type-7 config does **not** use the now-advanced Level RNG. It begins
from the saved post-Type8 snapshot. Its geometry helper then advances the
persistent `LevelGenerator._rng` once per eligible empty cell at RVA
`0x005AE2B4` and once more at RVA `0x005AE4A5` only when a maximum-score
candidate exists. The complete field-by-field ledger is in
`secret_rng_ledger.md` and is emitted dynamically by both implementations.

## Ultra Secret

The type-29 config seed is one index-71 advance from the saved post-Type8
snapshot. `PlaceUltraSecretRoom`, however, is a method on the persistent
LevelGenerator and continues its index-35 RNG after Secret: one draw for every
empty/unblocked/not-red-excluded position and one final draw only when the
maximum-score vector is nonempty. Full ownership and sites are recorded in
`ultra_secret_rng_ledger.md`.

## Differential artifact

`research/binary/special_room_differential_report.json` covers 10,000 start
seeds each for NORMAL and HARD.  It compares 292,367 transitions plus object
identity, candidates, stable erases, mutations and final Level state for the
currently implemented Boss→Type8 slice.  Three cases return the binary outer
retry signal at Boss placement; they are not silently accepted as complete
floors.

The assembled transaction report
`research/binary/basement1_pipeline_differential_report.json` extends this
comparison through Shop and Treasure, including every attempt boundary,
RoomConfig mutation, candidate/geometry decision and final persistent state.
It also compares the binary condition trace so skipped multi-boss/XL branches
remain part of the reference control flow rather than being optimized away.
The completed corpus compares 400,499 post-topology RNG transitions across
21,526 attempts.
