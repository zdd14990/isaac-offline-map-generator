# Ultra Secret binary proof

Executable profile:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Algorithm evidence: `CONFIRMED_BINARY` for canonical fresh ordinary Basement I
NORMAL/HARD. External validation remains
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Safety: the copied PE was read and disassembled as bytes. `isaac-ng.exe` was
not loaded or executed.

## Direct call graph

| Operation | RVA |
|---|---:|
| post-topology caller | `0x00339370` |
| type-29 RoomConfig selection | `0x0033C9CD` |
| red-door exclusion construction | `0x0033C9EF..0x0033CAB6` |
| Ultra callsite | `0x0033CB05` |
| `LevelGenerator::PlaceUltraSecretRoom` | `0x005AE640` |
| Level room assignment | `0x0033CB1B` |
| successful descriptor tail-field write (`99`) | `0x0033CB24` |
| ordinary descriptor collection begins | `0x0033CB5D` |

The placement helper directly calls the confirmed Room constructor, normal
13x13 map insertion, door-target helper and connection refresh functions.
Control transfers and function bytes are verified in
`research/binary/ultra_secret_binary_verification.json`.

## Geometry model

Ultra is option A from the investigation: it creates a real 1x1 generated
room in an empty position of the ordinary 13x13 `room_map`. It is not stored
only in a separate virtual grid and no projection step creates its GridIndex.

Its connectivity is red-door-specific. The selected Ultra cell has no
immediately adjacent occupied cardinal cell. Existing rooms one step farther
away (or diagonally offset) receive door bits whose target is an empty
cardinal cell adjacent to Ultra. These are red-door paths across the empty
intermediate grid position, not ordinary adjacent-room graph edges.

## Red-door exclusion set

The caller iterates every already configured descriptor and all eight door
slots. It inserts the in-bounds target position when:

- the concrete RoomConfig does not provide the slot; or
- RoomType is Boss (5), Super Secret (8), Secret (7), or Curse (10), in which
  case every geometrically valid target is excluded.

Door target calculation uses the concrete RoomConfig shape and the binary's
`ignoreThinRestrictions=true` mode. The newly added Secret descriptor is
already present and therefore participates. This is why the 20k corpus never
selects an Ultra candidate that uses Secret or Super Secret as an outer
neighbor.

## Candidate construction and ordering

Candidates are scanned in exact GridIndex order `0..168`. A position is
initially eligible only when:

- the ordinary room map is empty;
- the LevelGenerator blocked byte is zero;
- the red-door exclusion set does not contain it.

Every initially eligible position consumes one persistent
`LevelGenerator._rng` draw and begins with score `10 + state % 5`.

The four immediate offsets, in order, are:

```text
(-1,0), (0,-1), (1,0), (0,1)
```

Any occupied or blocked immediate position subtracts 100 and rejects the
candidate. The ordered outer ring is loaded from the executable as:

```text
(-2,0), (-1,-1), (0,-2), (1,-1),
(2,0),  (1,1),   (0,2),  (-1,1)
```

For every occupied outer position, the helper tests each cardinal direction
whose dot product with that outer offset is positive. The existing room's
opposite door target must be in bounds and absent from the exclusion set.
Diagonal positions therefore test two relevant door targets. An invalid
target subtracts 100. Neighbor count is the number of occupied outer grid
positions, including multiple occupied cells belonging to one large room.

At least one compatible outer position is required. Final scoring is:

```text
1 outer occupied cell  -> base - 6
2 occupied cells       -> base - 3
3 or more              -> base
```

Only the highest score is retained. Ties preserve scan order. One final
generator RNG draw selects `best[state % len(best)]`. A null vector returns
null without this final draw.

## RoomConfig and descriptor mutation

The concrete type-29 RoomConfig is selected before geometry, using Basement
stage 1 with stage-0 fallback, wildcard query shape 13, subtype -1 and
difficulty 1..10. All nine current special-room type-29 definitions are 1x1.
Normal mutable-weight selection/decay applies.

On success:

- generated room count increases by one;
- the new room is shape 1 at the selected ordinary GridIndex;
- the normal room map points to the new generated-room id;
- Level assignment sets RoomType 29, Variant/Subtype and equal
  GridIndex/SafeGridIndex for shape 1;
- the caller writes `99` to the assigned descriptor's trailing field;
- dead-end candidates do not change;
- normal connection refresh runs for the new room;
- qualifying outer rooms receive red-door bits; normal neighbor sets are not
  fabricated across the empty intermediary position.

## Null and retry behavior

If no candidate survives, the helper returns null. The direct caller skips
assignment and continues to the late ordinary pass. It does not retry the
floor. Type-29 RoomConfig weight effects and all consumed generator RNG draws
remain. A later ordinary-config failure may still reject the entire attempt.

## Independent implementation and corpus

- mechanical reference: `src/isaacmap/ultra_secret_reference.py`;
- clean leaf: `src/isaacmap/ultra_secret.py`;
- clean/reference M6→Ultra continuations and deep comparator:
  `basement1_ultra_pipeline*.py`;
- exact disassembly: `research/decomp/ultra_secret_005ae640.tsv`;
- binary verification: `research/binary/ultra_secret_binary_verification.json`;
- 20k report: `research/binary/basement1_ultra_differential_report.json`.

The corpus compares start seeds 1..10,000 independently for NORMAL and HARD:
20,000 results and 21,526 preceding attempts. It covers natural Ultra null,
map boundaries, diagonal/distance-two candidates, neighbor counts 1..6, tie
vectors 0..9, large rooms, every L shape, red-door writes 0..13 and all nine
type-29 variants. No mismatch occurred.

