# Basement I topology input state

Executable SHA-256:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

This note separates the actual binary inputs from the smaller public API we
eventually want.  It is based on the static `Level::Init` → ordinary
`Level::generate_dungeon` → `LevelGenerator::Generate` path.  The copied PE
was read and decompiled only; it was never started or loaded as a game.

## Frozen exact scope

The currently proved Basement I topology scope is:

| State | Required value |
|---|---|
| Stage | `STAGE1_1` / integer 1 |
| StageType | `STAGETYPE_ORIGINAL` / integer 0 |
| Difficulty | `NORMAL` (0) or `HARD` (1) |
| Generator family | ordinary dungeon generator at RVA `0x00340E10` |
| Challenge | none / 0 |
| Daily/custom run | false |
| Ascent/backwards state flag | false (`GameStateFlags` high-word bit `0x10000` clear) |
| Effective curse mask | 0; specifically Labyrinth, Lost and Giant clear |
| Player inventory dependency | no live player owns collectible 599 (Voodoo Head) |
| Stage seed | fresh `_stageSeeds[1]`, with no prior slot mutation |
| Room data | unmodified vanilla resources belonging to this executable profile |
| Seed effects | none that add/remove curses or filter flagged rooms |
| Blocked topology cells | all 169 false |
| Starting room | anchor `(6,6)`, GridIndex 84, Shape 1 |
| `LevelGenerator` flags | `isXL=false`, `isChapter6=false`, `isStageVoid=false` |

Within this scope, character identity is not read directly by the recovered
topology entry.  Character, challenge and unlock state can still matter
indirectly by changing the actual starting inventory.  Eden-like randomized
starts therefore cannot be reduced to `seed+difficulty` until their inventory
derivation is implemented.  The topology entry state that matters here is the
result of `PlayerManager::FirstCollectibleOwner(599, ..., true)`.

## Complete output-affecting entry state

### Stage seed and previous-stage state

`Level::Init` reads the current mutable value in `Seeds::_stageSeeds[slot]`:

```text
slot = stage + (StageType in {4,5} ? 1 : 0)
slot = min(slot, 13)
```

`Seeds::advance_stage_slot` at RVA `0x005EB980` mutates a stored slot using a
different fixed xorshift triple.  It has seven static callers.  Consequently,
the true input is the current stored stage seed, not unconditionally a pure
`get_stage_seed(start_seed, ...)` call.  For a fresh Basement I start the slot
has not been mutated, so the already-confirmed fresh-run derivation applies.

Previous-stage/runtime state can also affect later topology through current
inventory, effective curse sources, challenge/daily state and ascent flags.
Those are separate explicit state components; they are not hidden inside the
start seed.

### Difficulty and game mode

The current executable uses the global difficulty value as follows:

- 0: NORMAL, ordinary generator;
- 1: HARD, ordinary generator and `2 + (copied_rng.Next() & 1)` room bonus;
- 2/3: Greed/Greedier families, routed away from the ordinary generator.

NORMAL/HARD also select different default-room difficulty windows before the
allowed-shape mask is constructed.  Greed/Greedier are therefore not a
parameter variation of the currently proved generator.

### Curse, XL and seed-effect state

The effective curse byte repeatedly used by `Level::generate_dungeon` is:

```text
effective = (Level.curses | run_internal_mask | seed_effect_add_mask)
            & ~seed_effect_remove_mask
```

The add/remove helpers are RVAs `0x002F9400` and `0x002F95A0`.  Challenge and
daily setup can modify `Level.curses` earlier in `Level::Init`.  A nonzero
curse chance uses a copied Level RNG at call site RVA `0x00344F09`; a successful
chance roll consumes another draw at RVA `0x00344F34` to select the curse.
Those draws advance the copied stream later used for the HARD room bonus.

Topology-relevant bits and exact observed effects are:

| Bit | Effect before/during `Generate` |
|---:|---|
| `0x02` Labyrinth | `target=min(trunc(target*1.8),45)`; raises the ordinary required-dead-end base from 5 to 6 on Stage 1; sets `isXL`; enables the `%10` multi-neighbor RNG branch |
| `0x04` Lost | adds 4 rooms when Labyrinth is not active |
| `0x80` Giant | after HARD adjustment, `target=max(4,trunc(target*3/5))`; clears disallowed shape-mask bits at RVA `0x00341752` |

Other curse bits do not alter the recovered topology values on this entry
path, but remain part of the full Level state for later milestones.

Basement I normally suppresses the ordinary curse roll.  Daily/custom/challenge
state can change that decision, so `stage==1` alone is not sufficient proof of
an empty curse stream.

### Challenge and daily state

Challenge ID 21 (`XXXXXXXXL`, confirmed by the installed `challenges.xml`):

- consumes an extra Level RNG draw at RVA `0x00340FCC`;
- replaces target count with `40 + Next() % 5`;
- forces the `isXL` argument to `Generate`, even if curse bit `0x02` is clear.

Stage 12 subsequently has its own draw at RVA `0x0034103B` and overrides the
target with `50 + Next() % 5`.

Challenge ID 44 is routed to a different generator in `Level::Init`.  Challenge
parameters and daily configuration also supply curse add/remove masks and a
post-generation usability mode.  On the frozen challenge-free Basement I
scope, the usability byte at `LevelGenerator+0x393` is set true by `Generate`
and has no output-affecting write in the recovered topology call graph.

### Character and player state

There is no direct `PlayerType` read in the scoped call chain.  There is one
direct player query before `Generate`:

```text
PlayerManager::FirstCollectibleOwner(599, ..., true)
```

RVA `0x005BE080` proves this is an inventory query.  Installed resources map
collectible 599 to Voodoo Head.  If any live player owns it, required dead ends
increase by one.  Character, challenge, co-op and previous-stage state can all
affect this result.  Collectible 260 is also queried by `Level::Init` as a
curse-suppression input when a curse roll is otherwise possible.

### StageType and route

StageType affects:

1. the selected stage-seed slot for StageTypes 4/5;
2. the room-config stage ID and therefore the allowed-shape source pool;
3. the alternate-path predicates at RVAs `0x0034EF70` and `0x0034EFD0`;
4. target count (`-3`) and required-dead-end count (`+1`) when those predicates
   are true;
5. generator routing for non-ordinary stage families.

The frozen proof uses StageType 0, so both alternate-path predicates are false.

### Room database, unlocks and achievements

The default-room query at RVA `0x0042CE40` filters the loaded 0x5C-byte room
records by stage, type, shape, variant range, difficulty range, doors, subtype
and mode.  It does not call `PersistentGameData::Unlocked` and does not consume
the LevelGenerator RNG.  Its only extra flag filter in this path is tied to a
seed-effect record, not a persistent achievement lookup.

For current vanilla Basement resources, both relevant difficulty windows
contain at least one default room of every Shape 1..12.  The resulting mask is
`0x1FFE`.  Therefore persistent achievements do not directly change scoped
geometry once StageType, actual player inventory and the vanilla room database
are fixed.

Unlock state can still matter outside this boundary by deciding route/stage
availability and randomized starting inventories.  It must not be globally
declared irrelevant.

### Direct `LevelGenerator::Generate` inputs

The call at RVA `0x00341A20` supplies:

```text
targetRoomCount
isChapter6 = (stage == 11)
isXL       = effective Labyrinth OR challenge == 21
isVoid     = (stage == 12)
allowedShapes bitset
requiredDeadEnds
starting LevelGenerator_Room
```

`LevelGenerator` also contains `blockedPositions[169]`, initialized by its
constructor.  Other stage paths can populate blocks before generation.  The
ordinary Basement I path leaves all entries false.

## Conclusion

`start seed + difficulty` is sufficient only under the frozen state contract
above.  The general offline API needs a `FloorSpec` plus a run-state object (or
an exact derivation of that object) carrying the current stage seed, curses,
challenge/daily/ascent flags, relevant inventory queries, room-data profile and
generator blocked positions.

