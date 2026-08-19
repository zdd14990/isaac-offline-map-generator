# Secret Room RNG ledger

Executable profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Algorithm evidence: `CONFIRMED_BINARY` for canonical Basement I. External
validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Secret placement does not have one monolithic RNG. Three distinct object
identities participate.

## Objects

| Object identity | Seed source | Shift index | Lifetime | Use |
|---|---|---:|---|---|
| Saved post-Type8 snapshot | one persistent Level RNG draw at RVA `0x00339BE7` | numeric snapshot only | retained stack value across Shop, Treasure and all middle blocks | common seed material for distinct Secret and Ultra streams |
| Secret loop private RNG | copy of the saved snapshot | 1 `(1,5,16)`, table VA `0x00B1F4D4` | Secret repeat loop | first Secret RoomConfig uses the snapshot directly; RVA `0x0033C802` advances the private stream after each attempted placement for a possible next iteration |
| RoomConfig selector local | caller-provided Secret config seed | 7 `(1,21,20)` | one `RoomConfig::select_room` call | binary32 weighted selection and optional mutable-weight decay at RVA `0x0042CBDE` |
| `LevelGenerator._rng` | generator seed established before topology | 35 `(5,9,7)` | same persistent object across topology, retries and Secret geometry | one draw for every eligible empty grid candidate, plus one final best-candidate selection draw |

Equal numeric seeds do not merge these objects. The continuing Level RNG is
advanced by Shop, Treasure and the intervening blocks, but Secret RoomConfig
starts from the saved post-Type8 value. The Secret geometry pass instead
continues the existing LevelGenerator RNG after topology and prior geometry.

## Static draw sites

| Draw | Binary RVA | Object | Pre/post relation | Control-flow reason | Result use |
|---:|---:|---|---|---|---|
| 0 | `0x0042CBDE` | one-call RoomConfig local, index 7 | `post=xorshift7(configSeed)` | concrete type-7 STB choice | binary32 weighted threshold; selected weight decays |
| 1..N | `0x005AE2B4` | persistent `LevelGenerator._rng`, index 35 | one advance per eligible empty GridIndex in ascending scan | construct randomized base score | `10 + post % 5` |
| N+1, conditional | `0x005AE4A5` | persistent `LevelGenerator._rng`, index 35 | one advance only when the maximum-score vector is nonempty | resolve equal maximum-score candidates | `best[post % bestCount]` |
| loop tail | `0x0033C802` | Secret private loop stream, index 1 | advance after every attempted Secret iteration | seed a possible subsequent Secret config | next iteration's config seed |

If there is no eligible valid candidate, the final selection draw is absent.
The geometry pass still retains every earlier per-eligible-cell draw.

## Data dependencies from earlier blocks

- Boss, Type8, Shop, Treasure and assigned middle special rooms contribute
  concrete descriptors used by the forbidden-cell builder.
- Middle blocks mutate RoomConfig weights and end-room types, thereby changing
  concrete descriptor door masks and the forbidden set.
- Middle Level RNG draws do not change the saved Secret config seed.
- No middle block advances `LevelGenerator._rng`; Secret starts from the
  generator state left by topology/geometry.

Both implementations emit, for every transition, the binary RVA, object
identity, shift index, pre-state, post-state, reason and semantic result.
