# RoomConfig special-room selector binary proof

Profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Algorithm evidence: `CONFIRMED_BINARY` for the ordinary fresh Basement I
Boss, RoomType 8, Shop, and Treasure calls. External validation:
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Functions

| Function | RVA | Role |
|---|---:|---|
| RoomConfig selector | `0x0042C7D0` | filters ordered resource entries and performs weighted choice |
| RoomConfig query | `0x0042CE40` | stage/mode/type/shape/variant/difficulty/doors/subtype filters |
| exact-door predicate | `0x002DA750` | enables exact-door subset only when required mask is nonzero |
| stage fallback wrapper | `0x0042CDD0` | current stage, then fallback stage with the same numeric seed |
| weight write | `0x0042CD95` | selected current weight decay |
| ResetRoomWeights loop | VA `0x0082A9C0` / RVA `0x0042A9C0` | copies entry `+0x30` to `+0x34` |

## Query order and filters

The stage/mode pool is scanned in installed resource order. Entry stride is
`0x5C`. The query retains entries satisfying, in control-flow order:

1. exact RoomType;
2. exact RoomShape, unless requested shape is wildcard `0x0D`;
3. inclusive variant range;
4. inclusive room-difficulty range;
5. `(requiredDoors & entryDoors) == requiredDoors`;
6. exact subtype unless query subtype is `-1`;
7. the entry unlock/flag predicate.

The canonical profile exposes every installed special-room entry. The
unlock-gated branch remains explicit in the state contract rather than being
silently treated as seed-derived.

## RNG and weighted selection

Each selector constructs a temporary index-7 RNG `(1,21,20)` from the caller
seed. Binary32 arithmetic is used for every sum and comparison.

1. Sum current weights (`+0x34`) in resource order.
2. Draw a binary32 unit float for the cumulative threshold.
3. If requiredDoors is nonzero and exact-mask entries exist, sum that subset,
   draw a second unit float, and choose the exact subset when
   `unit2 < (exactWeight / totalWeight) * 9.99f`.
4. Scan the selected vector in stable resource order until
   `unit1 * selectedTotal < cumulative`.
5. If reduceWeight is true, write
   `max(binary32(old * 0.1f), 1.0e-7f)`.

The relevant raw constants are `9.989999771118164f`,
`0.10000000149011612f`, and `1.0000000116860974e-7f`.

All four current special-room calls pass requiredDoors=0, so they consume one
index-7 draw. The second-draw path is nevertheless implemented and unit
tested as part of the common selector.

## Lifecycle and retry

Level::Init resets the current RoomConfig stage and special stage 0 before
entering `Level::generate_dungeon`. It does not repeat this reset at the outer
generation attempt loop. Therefore:

- selected config decay happens before geometry;
- a rejected double-room Boss variant remains decayed;
- geometry failure does not restore the selected weight;
- the next attempt observes the decayed weight;
- a new floor's Level::Init restores initial weights for its relevant pools.

For these pools, direct Stage N generation is not stateful through RoomConfig
weight history, because Level::Init performs the reset. BossPool and other run
state still require separate treatment.

## Installed resources and geometry relevance

- stage 0: `rooms/00.special rooms.stb`;
- stage 1: `rooms/01.basement.stb`;
- Treasure has no matching type-4 entries in stage 1 and uses the stage-0
  fallback with the same selector seed.

Relevant shapes in the current resources are:

```text
Boss type 5:       1, 2, 3, 4, 6, 8
RoomType 8:        1
Shop type 2:       1
Treasure type 4:   1, 2, 3
```

All corresponding STB door masks and the 14 ordered end-room reshape
candidates are implemented. The last narrow-shape candidate is not
output-affecting for these installed special-room pools.

