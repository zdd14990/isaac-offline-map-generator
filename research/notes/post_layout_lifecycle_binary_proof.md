# Basement I successful post-layout lifecycle proof

Frozen executable SHA-256:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

This note covers the successful canonical Basement I tail after the accepted
13x13 layout is already complete. The copied PE was read as bytes and
statically decompiled/disassembled only. It was not executed or loaded.

## Boundary

The recovered slice is RVA `0x0033D1D6..0x0033D94B` inside
`Level::place_post_topology_rooms`. At this point Ultra Secret and the late
ordinary `ROOM_DEFAULT` pass have succeeded. This tail has no false return and
does not alter the accepted ordinary map. It initializes fixed descriptors at
negative GridIndexes and advances generation state that must be accounted for
before a later-floor replay.

The verified slice is 1,914 bytes with SHA-256
`a21990350bea6c0557db4208de080246c67be678171774d8749362a5311c6d37`.

## Canonical descriptor order

The ORIGINAL Stage 1 branch assigns these descriptors in order:

| GridIndex | RoomType | Stage query | Subtype | RNG owner |
|---:|---:|---:|---:|---|
| `-2` | 3 Error | 0 | -1 | persistent Level index 35 |
| `-6` | 22 Black Market | 0 | -1 | persistent Level index 35 |
| `-4` | 16 Dungeon | 0 | -1 | persistent Level index 35 |
| `-5` | 17 Boss Rush | 0 | -1 | persistent Level index 35 |
| `-7` | 5 Boss | 0 | 55 | persistent Level index 35 |
| `-8` | 1 Default | 13 | 1 | persistent Level index 35 |
| `-13` | 2 Shop | 0 | 0 | private index 19 |
| `-18` | 15 Angel | 0 | 1 | private index 20 |

The Stage 13 query for `-8` is backed by `rooms/13.blue womb.stb`. Optional
GridIndex `-10` is limited to other stage/stage-type conditions and is skipped;
`-9` is also skipped in this profile.

Each assignment calls the helper at RVA `0x00028940`. It consumes three draws
from the descriptor's RNG owner and stores them as descriptor seeds. A fourth
seed is derived from the third by one index-66 `(11,7,12)` advance without
advancing the owner. One additional owner draw seeds the index-7 RoomConfig
selector. The helper byte hash is
`8256b881b5c4e4b9d1ac855891ff84e3c54e900762fd01f260cc3681be0b4a7c`.

The Shop consumes one persistent Level draw to seed an index-19 `(3,3,26)`
private stream. That stream makes two `RandomInt(1)` subtype draws before its
three helper draws and selector draw. The Angel consumes one persistent Level
draw to seed an index-20 `(3,3,28)` private stream and then makes its helper
and selector draws.

## Persistent Level RNG ledger

Before the fixed descriptors, two probability sites always advance the
persistent Level RNG. On canonical Stage 1 their later descriptor-flag writes
are gated off, but their binary32 chance arithmetic and draws still happen.
Special-room used bits 30 and 31, if present, contribute one-shot bonuses of
`0.1f` and `0.02f` and are cleared. The canonical empty-player/counter base is
`1.0f / 3.0f`.

Persistent index-35 consumption is therefore exactly:

```text
2 probability draws
+ 6 * (3 descriptor seeds + 1 selector seed)
+ 1 Shop private-stream seed
+ 1 Angel private-stream seed
= 28 Level RNG draws
```

The private Shop/Angel transitions are retained separately and do not change
the persistent Level count.

## State handoff

`generate_basement1_lifecycle` composes the already confirmed accepted-layout
pipeline with this leaf and returns an immutable generation snapshot. It
contains the 37 BossPool states with the committed Basement pool state,
permanent boss removals, final RoomConfig weights, special-room used bits and
the post-tail Level RNG state. This is a generation-only boundary; it does not
claim that all later-floor inputs can be inferred from a seed without an
explicit canonical gameplay/profile contract.

## Verification

The clean leaf is `src/isaacmap/post_layout_lifecycle.py`; the independent
mechanical reference is `post_layout_lifecycle_reference.py`. Static transfer
and constant checks are recorded in
`research/binary/post_layout_lifecycle_binary_verification.json`. Unit tests
cover exact transitions, selection/config equality, all eight descriptor
identities, the 28-draw replay, used-bit clearing and strict rejection of
noncanonical state.

Algorithm confidence for this scoped tail: `CONFIRMED_BINARY`.

External gameplay fixture status remains independently:
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.
