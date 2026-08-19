# Post-Treasure generation call graph

Executable profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Algorithm evidence: `CONFIRMED_BINARY` for the frozen fresh ordinary
Basement I NORMAL/HARD profile. External validation:
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

The evidence is static control-flow and data-flow recovery from the copied PE.
The executable was not loaded or executed.

## Confirmed order

The post-topology function at RVA `0x00339370` continues after the confirmed
Treasure block in this order:

```text
Treasure completion
  -> Planetarium (type 24)
  -> Dice (21) or Sacrifice (13)
  -> Library (12)
  -> Curse Room (10)
  -> MiniBoss (6)
  -> Challenge (11)
  -> Chest (20) or Arcade (9)
  -> Isaac (18) or Barren (19)
  -> alternate-path first-half mandatory end room
  -> alternate-path second-half collectible-626 end room
  -> route-state end-room block
  -> Secret (7)
  -> Stage-11 ORIGINAL subtype-3 end room
  -> Ultra Secret (29)
  -> collect ordinary rooms
  -> ordinary ROOM_DEFAULT RoomConfig assignment
```

The type alternatives are selected by control flow. They are not parallel
passes and do not share one selected descriptor. Every block that obtains an
end-room candidate uses the current `LevelGenerator._deadEnds` order after all
earlier stable erases or append-to-end rejections.

## Canonical Basement I blocks

| Block / binary range | Concrete selection and geometry calls | Canonical status | Mutation and failure behavior |
|---|---|---|---|
| Planetarium, `0x0033A8F7..0x0033AB45` | config `0x0033A963`; `GetNewEndRoom` `0x0033A97B`; descriptor assignment `0x0033AB10` | `ALWAYS_EXECUTED`; assignment is seed-dependent | Compatible candidate is stable-erased, then either assigned or appended to the vector end. No false return. |
| Dice/Sacrifice, `0x0033AB45..0x0033AF08` | Dice config `0x0033ACC8`, candidate `0x0033ACE2`; Sacrifice config `0x0033AE50`; assignment `0x0033AE83` | `ALWAYS_EXECUTED`; alternative and assignment are seed-dependent | Candidate rejection appends to end. No false return. |
| Library, `0x0033AF71..0x0033B10D` | config `0x0033AFF9`; candidate `0x0033B00D`; assignment `0x0033B108` | `ALWAYS_EXECUTED`; assignment seed-dependent | Selector is called with `reduceWeight=false`. Rejection appends to end. No false return. |
| Curse Room, `0x0033B10D..0x0033B3A8` | config `0x0033B200`, stage fallback `0x0033B26D`; candidate `0x0033B287`; assignment `0x0033B38F` | `ALWAYS_EXECUTED`; a compatible candidate is assigned in the frozen resource/profile path | Uses a temporary index-66 RNG. No false return. |
| MiniBoss, `0x0033B3A8..0x0033BBAE` | exact-difficulty config `0x0033B8AD`, fallback `0x0033B91A`; candidate `0x0033B940`; assignment `0x0033BAB6` | `ALWAYS_EXECUTED`; subtype and assignment are seed/state-dependent | Successful assignment immediately writes the corresponding `Game+0x26548` used bit. Rejection appends to end. No false return. |
| Challenge, `0x0033BBAE..0x0033BD87` | config `0x0033BC20`; candidate `0x0033BC34`; assignment site `0x0033BD66` | block `ALWAYS_EXECUTED`; assignment `ALWAYS_SKIPPED` for Stage 1 canonical | Candidate is appended to end. No false return. |
| Chest/Arcade, `0x0033BD87..0x0033C0B6` | Chest config `0x0033BF13`, Arcade config `0x0033BFBF`; candidate `0x0033BFD3`; assignment `0x0033C0B1` | block `ALWAYS_EXECUTED`; alternative seed-dependent; assignment `ALWAYS_SKIPPED` for fresh Stage 1 canonical | Candidate is appended to end. No false return. |
| Isaac/Barren, `0x0033C0F0..0x0033C416` | config `0x0033C236`; candidate `0x0033C24F`; assignment `0x0033C405` | Isaac block `ALWAYS_EXECUTED`; Isaac assignment seed-dependent; Barren `ALWAYS_SKIPPED` in canonical route state | Rejection appends to end. No false return. |
| Alternate-path first-half, `0x0033C416..0x0033C4D1` | config `0x0033C498`; candidate `0x0033C4A8`; assignment `0x0033C4C2` | `ALWAYS_SKIPPED` | Outside ORIGINAL Stage 1 profile; mandatory failure behavior is retained in the reference branch. |
| Alternate-path second-half, `0x0033C554..0x0033C640` | config `0x0033C604`; candidate `0x0033C618`; assignment `0x0033C631` | `ALWAYS_SKIPPED` | Requires the route/collectible predicate. |
| Route-state end room, `0x0033C645..0x0033C69E` | inline condition and end-room path | `ALWAYS_SKIPPED` | Requires a noncanonical route-state flag. |
| Secret, `0x0033C6A4..0x0033C83B` | stage fallback config `0x0033C716`; forbidden-set helper `0x0033C72E`; geometry `0x0033C741`; assignment `0x0033C7B0` | `ALWAYS_EXECUTED`; placement can yield no candidate | Adds a new descriptor on success. A null geometry result is allowed and does not return false. |
| Post-Secret Stage 11, `0x0033C83B..0x0033C902` | config around `0x0033C8CE`; candidate `0x0033C8E2`; assignment `0x0033C8FD` | `ALWAYS_SKIPPED` | Predicate is Stage 11 plus ORIGINAL. |
| Ultra Secret, `0x0033C902..0x0033CB36` | type-29 config `0x0033C9CD`; red/exclusion set `0x0033C9EF..0x0033CAB6`; placement `0x0033CB05` -> `0x005AE640`; assignment `0x0033CB1B` | `ALWAYS_EXECUTED` in fresh canonical profile; placement `CONFIRMED_BINARY` in M7 | Null placement is allowed and continues. Full placement proof is in `ultra_secret_binary_proof.md`. |
| Late ordinary defaults, `0x0033CB36..0x0033CF06` | collect `0x0033CB97` -> `0x005AF0E0`; select `0x0033CCDE`; assign `0x0033CD07` | `ALWAYS_EXECUTED` | A missing compatible config returns false and rejects the entire attempt. |

## Candidate and RoomConfig ordering

Except Secret, each canonical middle special-room block selects a concrete
RoomConfig before calling `GetNewEndRoom` at RVA `0x005AE0E0`. That helper
scans the current dead-end vector from beginning to end, reshapes/re-anchors
the first compatible generated room and stable-erases it. A conditional
placement rejection appends that same room id to the vector end. Consequently
even a room type that is not ultimately displayed can change every later
candidate order and RNG/config result.

Secret is a separate path: its concrete type-7 RoomConfig is selected first,
then a forbidden grid set is built, then `PlaceSecretRoom` scans empty grid
positions and appends a new generated room. It does not consume the dead-end
vector.

## Attempt result boundary

No canonical middle block and no Secret null result directly returns false.
Ultra null is also allowed at its caller. The next ordinary RoomConfig pass can
return false, so completion through Secret is only a pre-Ultra research
boundary, not a committed successful floor. Boss removal is committed only
after the complete post-topology function eventually returns true.
