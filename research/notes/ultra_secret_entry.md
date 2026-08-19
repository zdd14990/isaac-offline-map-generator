# Ultra Secret entry boundary

Executable profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Status: entry and complete placement are now `CONFIRMED_BINARY` for canonical
Basement I. External validation:
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Position in the call chain

After the Secret loop, the caller first contains a Stage-11 ORIGINAL
mandatory subtype-3 end-room block at RVA `0x0033C83B..0x0033C902`.
Canonical Basement I always skips it. The next operation is the Ultra Secret
block:

```text
Secret completion
  -> skipped Stage-11 ORIGINAL end-room block
  -> type-29 RoomConfig selection
  -> red-room/exclusion set construction
  -> LevelGenerator::PlaceUltraSecretRoom
  -> descriptor assignment when non-null
  -> collect ordinary rooms
```

Callsite `0x0033CB05` invokes `LevelGenerator::PlaceUltraSecretRoom` at RVA
`0x005AE640`; assignment is at `0x0033CB1B`.

## Confirmed entry inputs

- the current `LevelGenerator` 169-entry room map, shapes and connections;
- all materialized special-room descriptors, including the just-created
  Secret descriptor when Secret placement succeeded;
- a red-room/forbidden ordered set prepared at
  `0x0033C9EF..0x0033CAB6`, with special treatment for Boss (5), Super Secret
  (8), Secret (7), Curse (10), and missing concrete door slots;
- concrete RoomType 29 RoomConfig selected before geometry, using current
  stage with stage-0 fallback;
- a distinct temporary index-71 `(13,3,17)` RNG seeded from the same saved
  post-Type8 snapshot and advanced once for the type-29 RoomConfig seed;
- the continuing persistent LevelGenerator index-35 RNG for geometry candidate
  and final tie draws;
- current blocked positions and grid bounds.

The index-71 object is not the continuing Level RNG, persistent LevelGenerator
RNG, or Secret index-1 stream. Geometry itself does use the persistent
LevelGenerator RNG; see `ultra_secret_rng_ledger.md`.

## Entry failure behavior

At callsite `0x0033CB0C`, a null geometry result branches past descriptor
assignment and continues to the late ordinary-room collection. It does not
directly return false or trigger a floor retry. RoomConfig weight/RNG side
effects performed before the null result remain.

The red-room search, scoring, descriptor mutation and connection writes are
implemented and proven in `ultra_secret_binary_proof.md`. Exact complete-map
output still remains fail closed because the later ordinary ROOM_DEFAULT
RoomConfig pass can reject the attempt and has not yet been implemented.
