# Ultra Secret RNG ledger

Profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Status: `CONFIRMED_BINARY` for canonical Basement I NORMAL/HARD.

## Two distinct objects

Earlier entry notes identified the index-71 stream but did not yet prove which
object owned geometry draws. The complete callsite now establishes two
independent objects:

| Object | Seed source | Shift index | Consumption |
|---|---|---:|---|
| `Ultra.config.private` | saved post-Type8 numeric snapshot | 71 `(13,3,17)` | exactly one `Next` at `0x0033C977..0x0033C9B0`; resulting state seeds type-29 RoomConfig selection and Level assignment |
| `RoomConfig::select_room.local` | index-71 result | 7 `(1,21,20)` | weighted threshold, optional exact-door gate, and mutable weight decay |
| `LevelGenerator._rng` | persistent generator state after topology, retries and Secret geometry | 35 `(5,9,7)` | one draw per eligible Ultra candidate at `0x005AE755..0x005AE795`, plus one final tie draw at `0x005AEAE6..0x005AEB25` only if the best vector is nonempty |

`PlaceUltraSecretRoom` is invoked with the actual LevelGenerator pointer in
ECX at `0x0033CAF8`; index-71 is not its `this` object. Thus the correct chain
is:

```text
post-Type8 snapshot
  -> construct index-71 temporary
  -> one Next
  -> type-29 RoomConfig local index-7 selector

post-Secret persistent LevelGenerator index-35 state
  -> eligible candidate draws in GridIndex order
  -> optional final maximum-tie draw
```

Candidate rejection after the initial eligibility test still retains its
index-35 draw. Occupied, blocked, or red-excluded cells consume none. A null
result has no final selection draw.

Both reference and clean ledgers are compared in the 20k artifact
`research/binary/basement1_ultra_differential_report.json`.

