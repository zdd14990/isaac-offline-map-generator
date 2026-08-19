# Secret Room binary proof

Executable profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Status: `CONFIRMED_BINARY` in the frozen fresh ordinary Basement I
NORMAL/HARD profile. External validation:
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Functions and call order

| Purpose | RVA / callsite |
|---|---:|
| post-topology caller | `0x00339370` |
| Secret stage-fallback RoomConfig call | `0x0033C716` -> `0x0042CDD0` |
| build forbidden candidate set | `0x0033C72E` -> `0x00338D70` |
| place Secret geometry | `0x0033C741` -> `0x005AE170` |
| assign concrete descriptor | `0x0033C7B0` -> `0x00338AB0` |
| advance repeat-loop seed | `0x0033C802` |

The concrete type-7 RoomConfig is selected before candidate geometry. The
selection query uses current RoomConfig stage with stage-0 fallback, wildcard
shape, subtype `-1`, doors `0`, difficulty window `1..10`, and
`reduceWeight=true`.

## Forbidden-cell construction (`0x00338D70`)

The helper builds an ordered set from already materialized Level descriptors.
Unconfigured ordinary generator rooms do not yet have descriptors and are not
visited by this pass.

For each descriptor it materializes up to eight rectangular perimeter target
positions. Slots are scanned as follows:

- shape 1: `0,1,2,3`;
- shape 4: `0,1,2,3,4,6`;
- shape 6: `0,1,2,3,5,7`;
- all other shapes: `0..7`.

A valid in-bounds target is forbidden when the concrete descriptor has no
door bit for that slot, or when its type is Boss (5), Super Secret (8), or
Secret (7). Stage 11 also forbids the four cardinal start-room neighbors;
canonical Basement I skips that branch.

## Candidate scan (`0x005AE170`)

The helper scans GridIndex `0..168` in strictly ascending order. A cell is
eligible only if it is empty, absent from the ordered forbidden set and not
marked in `LevelGenerator._blockedPositions`.

Every eligible cell consumes exactly one persistent generator RNG draw and
starts with score `10 + state % 5`. Neighbors are enumerated in the cardinal
order LEFT, UP, RIGHT, DOWN. For each occupied cardinal neighbor, the helper
asks that neighbor shape for the opposite door target:

- an invalid door target subtracts 100 from the score;
- a valid target increments adjacency and sets the corresponding neighbor
  mask bit.

Zero-adjacency and negative-score cells are discarded. Otherwise the adjusted
score is:

```text
1 neighbor: base - 6
2 neighbors: base - 3
3 or 4:      base
```

Only the maximum-score tier is retained. A higher score clears the vector and
inserts the current GridIndex; an equal score appends; a lower score is
ignored. Thus tie order is the original ascending grid scan. There is no
shuffle, sort, duplicate pass, or neighbor-count fallback tier. When the best
vector is nonempty, one final generator draw selects
`best[state % best.size()]`.

## Descriptor and graph mutation

Secret is not an existing-room type mutation. On success the helper appends a
new 1x1 generated room at the selected empty GridIndex. The caller then assigns
its concrete type-7 RoomConfig descriptor. For a 1x1 room:

```text
GridIndex     = selected empty index
SafeGridIndex = GridIndex
RoomShape     = 1
RoomType      = 7
ListIndex     = newly appended descriptor index
```

The 169-entry map points the selected cell to the new room id. Connections are
refreshed first for the new room and then for cardinal occupied neighbors in
LEFT, UP, RIGHT, DOWN order. Room/descriptor count increases by one. The
dead-end candidate vector is unchanged.

This mutation occurs before Ultra Secret preparation, so Ultra sees the new
occupied cell, descriptor type, door exclusions and updated graph.

## Failure semantics

When no best candidate exists, `PlaceSecretRoom` returns null. The caller does
not return false: it advances the Secret loop stream and continues. Therefore
Secret geometry failure permits a floor with no Secret and does not itself
trigger the outer floor retry. Any RoomConfig selector weight decay and all
per-candidate generator RNG advances already performed remain committed to the
attempt's persistent streams.

The later ordinary default RoomConfig pass is a separate failure site and can
still reject this attempt.

## Implementations and comparison

- mechanical reference: `src/isaacmap/secret_reference.py` and
  `src/isaacmap/basement1_secret_pipeline_reference.py`;
- clean port: `src/isaacmap/secret.py` and
  `src/isaacmap/basement1_secret_pipeline.py`;
- deep comparator: `src/isaacmap/basement1_secret_pipeline_differential.py`.

The comparator includes all 169 candidate evaluations, scan/tie action,
neighbor masks, scores, candidate order, RoomConfig result and weight
transition, every RNG transition, selected GridIndex, descriptor mutation,
connection refreshes, room map, dead-end order and final persistent states.

The final offline corpus covers start seeds 1..10,000 for both NORMAL and
HARD (20,000 comparisons, 21,526 attempts). It reaches 1/2/3/4-neighbor
candidates, stable tie vectors of sizes 1..7, map boundaries, large-room and
all L-shape adjacency. A synthetic all-occupied map fixes the no-candidate
path and proves the absence of a final selection draw there.
