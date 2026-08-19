# Basement I special-room binary proof through Treasure

Profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Scope:

```text
Topology -> Boss identity -> Boss RoomConfig -> Boss geometry
         -> RoomType 8 / Super Secret -> Shop -> Treasure -> stop
```

Algorithm evidence: `CONFIRMED_BINARY` for the canonical fresh ordinary
Basement I profile. External validation:
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

This M5 proof deliberately stops before Secret. M6 confirms Secret in
`secret_binary_proof.md`, and M7 confirms Ultra placement in
`ultra_secret_binary_proof.md`. Complete-map output remains
`UNSUPPORTED — FAIL CLOSED` pending the late ordinary RoomConfig pass.

## Ordered pipeline

| Operation | Principal RVAs | Result / failure behavior |
|---|---|---|
| Boss identity | call `0x00339475` -> `0x00022830` | chooses id and sets per-attempt boss bit |
| Boss RoomConfig | Level draw `0x003394A4`; helper `0x00339080`; selector `0x0042C7D0` | concrete type-5 config; selected weight decays |
| Boss geometry | call `0x003394F2` -> `0x005AEF10` / `0x005AED50` | stable-erases first compatible distance>1 end room; failure aborts attempt |
| Boss assignment | `0x00339528` -> `0x00338AB0` | mutates existing generated descriptor |
| Type 8 | Level draw `0x00339A87`; private draw `0x00339B1E`; config `0x00339B64`; end room `0x00339B78`; assign `0x00339B8D` | stable-erases/mutates existing end room; first failure aborts |
| post-Type8 snapshot | `0x00339BE7..0x00339C08` | advances Level RNG and saves seed for later Secret/Ultra streams |
| Shop | private seed draw `0x00339DB4`; config-seed draw `0x0033A1C7`; config call `0x0033A205`; end room `0x0033A219`; assign `0x0033A256` | canonical subtype 11; failure aborts |
| Treasure | chance `0x0033A455`; optional draw `0x0033A4B8`; config seed `0x0033A76B`; wrapper `0x0033A7AD`; end room `0x0033A7C1`; assign `0x0033A7EA` | stage 1 miss then stage 0 fallback; failure aborts |

The additional/multi-boss and XL second-boss blocks lie between Boss and
Type8 in the binary. They are retained as explicit false conditions in the
canonical reference path; they are not removed or reordered.

The paired implementations also retain the two Shop eligibility checks and
the Treasure eligibility check with their exact binary ranges. Their ordered
condition traces are part of the deep differential, even though the canonical
fresh Basement I profile makes the first two branches false and the latter
three true.

## Candidate and distance semantics

The M4 dead-end vector at `LevelGenerator+0x370..+0x374` is consumed directly.
There is no new graph-distance pass, Manhattan score, shuffle, or sort in this
slice.

- order is M4's descending generation-depth selection-sort order;
- `DetermineBossRoom` requires stored `distance_from_start > 1`;
- `GetNewEndRoom` has no distance requirement;
- both scan begin-to-end;
- successful removal uses `memmove`, hence stable erase;
- Type8, then Shop, then Treasure see the exact pool left by predecessors.

## Geometry matcher

RVA `0x005B1220` builds 14 ordered reshape candidates: a 1x1 at the original
link cell followed by the 13 anchor/shape templates used by the large-room
topology builder. It checks:

1. concrete RoomConfig shape;
2. configured door at the candidate's parent connection slot;
3. all candidate occupied cells are free or owned by the same generated room;
4. every adjacent generated room has a corresponding configured door;
5. fewer than two non-exempt external neighbors.

Success clears the previous occupied cells, writes the new anchor, dimensions
and shape, repopulates the 13x13 room map, and rebuilds connections. It is a
mutating predicate, not a read-only compatibility test.

The installed pools exercise Boss shapes 1,2,3,4,6,8; Type8/Shop shape 1;
Treasure shapes 1,2,3. Their STB door coordinates are mapped to all relevant
door slots. Type8, Shop, and Treasure mutate existing generated rooms; they do
not append descriptors.

## Boss pipeline and persistent state

The original Basement pool is fixed slot 1. It is seeded from the chained
37-pool start-seed stream and shuffled once with a separate MT19937. On each
ordinary attempt:

1. persistent index-17 BossPool RNG advances seven times;
2. a stack copy advances for weighted selection;
3. only the seven persistent advances are written back;
4. selected boss is added to the per-attempt blacklist;
5. concrete Boss RoomConfig uses Level/private/RoomConfig RNGs;
6. variants 3700..3849 are rejected with up to 50 additional private config
   iterations, and every selected config decay remains effective;
7. geometry selects and validates the room in separate calls;
8. success-only floor commit merges the chosen boss into permanent removed.

Geometry failure does not undo the seven pre-rolls or RoomConfig weight decay.
It does prevent the failed boss bit from entering permanent removed state.

## Type8 / Super Secret

Type8 uses a private index-9 `(2,5,15)` stream seeded by one Level draw. The
canonical profile places one. Collectible 589 would request two, but that
noncanonical input is rejected by the current through-Treasure entry point.

The first Type8 placement is mandatory. It stable-erases an existing end room
and assigns the selected type-8 RoomConfig. This is why it must execute before
Shop/Treasure even though Secret/Ultra work is deferred.

## Shop

For fresh ordinary Basement I, the stage and unvisited Shop-state predicates
enter the Shop block. The binary:

1. consumes the post-Type8 snapshot draw regardless of later Shop placement;
2. advances Level RNG again to seed an index-19 `(3,3,26)` private stream;
3. consumes four private draws on the canonical no-collectible state path;
4. resolves subtype 11;
5. advances Level RNG for a stage-0 type-2 RoomConfig selection;
6. stable-erases the first compatible remaining end room.

NORMAL/HARD does not directly branch this Shop placement. Differences arise
upstream through topology and resulting stream states. Character, collectible,
challenge, route, visit and Shop-state branches are explicit profile inputs
and fail closed outside the canonical profile.

## Treasure

Fresh ordinary Basement I enters the Treasure block after Shop mutation.

- the first Level draw chooses the rare subtype-1 branch when `%100 == 0`;
- otherwise a second Level draw is consumed and canonical no-collectible
  state chooses subtype 0;
- a final Level draw seeds the concrete RoomConfig selector;
- `select_room_with_stage` queries stage 1 then stage 0 with the same numeric
  seed; current resources have no matching stage-1 type-4 rooms;
- the selected stage-0 config is geometry-matched against Shop's remaining
  candidate vector.

Treasure geometry failure returns false to the same outer transaction loop.
NORMAL seed 1 is a permanent regression fixture for this later failure site.

## Retry integration

The full state table is in `generation_retry_semantics.md`. In short:

```text
discard: topology, partial descriptors, dead-end arrays, level blacklist
retain:  Level RNG, LevelGenerator RNG, BossPool RNGs/shuffle/permanent bits,
         RoomConfig current weights, stage seed, retry/target counters
```

The next attempt begins with a new topology generated from the continuing
LevelGenerator RNG and a new Boss selected from the continuing BossPool RNG.

## Implementations and tests

- RoomConfig reference/clean: `src/isaacmap/room_config_reference.py`,
  `src/isaacmap/room_config.py`;
- geometry reference/clean: `src/isaacmap/special_room_geometry_reference.py`,
  `src/isaacmap/special_room_geometry.py`;
- full reference/clean pipeline:
  `src/isaacmap/basement1_pipeline_reference.py`,
  `src/isaacmap/basement1_pipeline.py`;
- deep comparator: `src/isaacmap/basement1_pipeline_differential.py`;
- retry fixtures: `tests/fixtures/boss_geometry_retries.json` and
  `tests/fixtures/treasure_geometry_retry.json`.

Reference/clean equality is supporting implementation evidence only. The
`CONFIRMED_BINARY` rating is based on the listed current-executable control
flow, constants, object ownership, vector mutation, tables, and RNG sites.
The mass artifact is
`research/binary/basement1_pipeline_differential_report.json`; it covers
10,000 NORMAL and 10,000 HARD start seeds and all attempts until the chain
succeeds through Treasure. The completed report contains 21,526 attempts,
400,499 post-topology RNG transitions, 114,244 RoomConfig selector calls,
90,493 candidate tests and 107,615 condition traces, with Shapes 1..12 reached
by both topology rooms and ordered geometry candidates.
