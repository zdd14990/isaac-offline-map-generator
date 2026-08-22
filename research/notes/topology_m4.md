# Milestone 4 Static Topology Reconstruction

Status: completed as `CONFIRMED_BINARY` for the frozen Basement I contract.
The canonical final proof, complete input boundary and RNG ledger are now
`topology_binary_proof.md`, `topology_inputs.md` and
`topology_rng_ledger.md`.  Historical investigation notes below are retained;
their earlier fixture-related promotion language is superseded by the explicit
`CONFIRMED_BINARY` / `NOT_EXTERNALLY_VALIDATED_GAMEPLAY` split.

Executable SHA-256:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

All addresses below are RVAs. The corresponding Ghidra exports under
`research/decomp/ghidra/` are static decompilations of the copied PE; the game
was never executed.

## Confirmed call chain

| Function | RVA | Status |
|---|---:|---|
| `Level::Init` | `0x00344940` | `CONFIRMED_BINARY` |
| ordinary dungeon generator | `0x00340E10` | `CONFIRMED_BINARY` |
| `LevelGenerator` constructor | `0x005ADAF0` | `CONFIRMED_BINARY` |
| `LevelGenerator::Generate` | `0x005ADBB0` | `CONFIRMED_BINARY` |
| room-expansion loop | `0x005B04D0` | `CONFIRMED_BINARY` |
| neighbor candidate builder | `0x005B0B00` | `CONFIRMED_BINARY` |
| candidate shuffle | `0x005B1B20` | `CONFIRMED_BINARY` |
| placement/free/valid helpers | `0x005B0180..0x005B0330` | `CONFIRMED_BINARY` |
| forced dead-end helper | `0x005AF1E0` | `CONFIRMED_BINARY` |
| dead-end marking/classification | `0x005AFB10`, `0x005AFC70` | `CONFIRMED_BINARY` |

The call to the ordinary dungeon generator at VA `0x007453F2` is inside the
`Level::Init` function beginning at VA `0x00744940`. This disambiguates the
otherwise generic `Level::Init` signature.

## Initial floor seed transfer

`Level::Init` obtains the global `Seeds` object and selects
`_stageSeeds[slot]`, where:

```text
slot = LevelStage
if StageType is REPENTANCE (4) or REPENTANCE_B (5):
    slot += 1
slot = min(slot, 13)
```

It initializes the Level RNG with shift triple `(5,9,7)`. The constants are at
RVA `0x0071F66C`. The selected stage seed itself is not modified.

For a fresh ordinary Basement I (`STAGE1_1`, `STAGETYPE_ORIGINAL`) path:

```text
L1 = level_rng.Next()       // early Level::Init
L2 = level_rng.Next()       // before curse setup
stack_rng = copy(level_rng) // same state as L2

C_gate = stack_rng.Next()    // RandomInt(curse_rate)
if C_gate % curse_rate == 0:
    C_selector = stack_rng.Next() // Next()%6 curse selection

L3 = level_rng.Next()       // base room-count low bit
C_difficulty = stack_rng.Next() // always advances; NORMAL discards the bit

target NORMAL = 8 + (L3 & 1)
target HARD   = 8 + (L3 & 1) + 2 + (C_difficulty & 1)

L4 = level_rng.Next()
LevelGenerator(seed=L4, shifts=(5,9,7))
```

The fresh run-start transition flag is clear, so ordinary Basement I executes
the curse gate. Required dead ends are 5 normally and 6 when the selector
retains Labyrinth. The starting room is shape 1 at column 6, line 6, hence
GridIndex 84. The Basement default-room pools contain all shapes 1 through 12
in both difficulty windows used here, producing allowed-shape mask `0x1FFE`.

The implemented scope in `src/isaacmap/floor_init.py` intentionally stops at
these pre-`Generate` values; it does not claim a completed floor.

## Room expansion and RNG order

The recovered main loop at RVA `0x005B04D0` is:

```text
place start room
queue.push_front(start.generationIndex)

while queue not empty and roomsPlaced < target:
    source = queue.pop_front()
    candidates = get_neighbor_candidates(source, forceAllLarge=false)
    fisher_yates_shuffle(candidates)  // n-1 RNG draws

    if source is start:
        if target < 16:
            wanted = 2 + (Next() & 1) // one draw
        else:
            wanted = candidate_count  // no draw
    else:
        wanted = min(candidate_count,
                     (Next()&1) + (Next()&1) +
                     (Next()&1) + (Next()&1))

    for candidate in shuffled order:
        require is_pos_free(candidate)
        links = count_neighbor_links(candidate.linkPosition)
        require links < 2, except XL/Void may consume one draw and
                accept when Next() % 10 == 0
        require is_placement_valid(candidate)
        place candidate
        if Next() % 3 == 0: queue.push_back(candidate)
        else:               queue.push_front(candidate)
        stop after wanted placements or target
```

The shuffle is an in-place Fisher-Yates pass from `n-1` down to 1. Each step
consumes one `Next()` and swaps with index `Next() % current_size`.

## Neighbor candidate builder

For each of the source room's eight door slots, in order:

1. compute the target grid coordinate;
2. skip an invalid/out-of-bounds/non-free 1x1 target without any large-room
   draws;
3. append a 1x1 candidate if shape 1 is allowed;
4. construct 13 large/thin candidates in fixed order;
5. consume exactly one RNG draw for every one of those 13 candidates before
   its allowed-shape and collision filters.

The divisors are:

```text
48, 24, 24, 24, 24, 72, 72, 36, 36, 36, 36, 24, 24
```

Normally a candidate passes its random gate when `Next() % divisor == 0`.
When shape 1 is unavailable, or when the dead-end-forcing caller passes its
override flag, the random gate is ignored, but the draw is still consumed.

RoomShape occupancy, DoorSlot tables and the ordered candidate templates are
ported in `src/isaacmap/topology_geometry.py`. Raw size and direction tables
are checked by `research/binary/topology_binary_verification.json`.

## Dead-end correction

After the initial expansion:

1. classify dead ends;
2. if fewer than required, try `force_new_dead_end` at most five times;
3. each attempt scans rooms and their unshuffled candidates in order, with the
   force-all-large flag, and places the first free candidate with fewer than
   two neighbor links;
4. rebuild the dead-end lists after each attempt;
5. sort the dead-end room indices by descending `distanceFromStart`.

The outer dungeon caller rejects an unusable result or a result still lacking
the required dead ends and retries. After more than nine attempts, every fifth
retry may increase the target by one, capped at 64.

## Current blocker

`src/isaacmap/topology.py` now ports the scoped ordinary expansion,
placement-validity, connection-set, forced-dead-end/classification and retry
paths. It passes typed L-shape/connection tests and 2,000 offline invariant
fuzz runs. These checks prove internal consistency, not parity with the game.

Remaining work:

- obtain a version-qualified offline fixture or another static/open-source
  independent validation source without using the game as an oracle;
- expand binary-derived trace tests to cover rare branch combinations and
  outer retry cases;
- prove complete room-config query/filter semantics beyond the scoped Basement
  pools, including unlock and custom-run flags.

Until these are complete, every floor remains unsupported in exact mode.
