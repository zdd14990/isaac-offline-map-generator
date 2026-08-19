# Generation retry transaction semantics

Profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Algorithm evidence: `CONFIRMED_BINARY` for the ordinary fresh Basement I
branch. External validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

All evidence is static analysis of the copied PE. The executable was never
executed or loaded.

## Transaction boundary

The outer attempt loop begins at RVA `0x00341760` in
`Level::generate_dungeon` (RVA `0x00340E10`). It owns topology usability
retries and failures returned by `Level::place_post_topology_rooms` alike.

At every loop head, call RVA `0x0034176C` passes `Game+0x1AF70` to
`Level__attempt_reset` (RVA `0x003382C0`). That helper only fills the
BossPools per-level blacklist vector at manager offset `+0x8BC` with false.
It does not reset an RNG or a RoomConfig weight.

If post-topology placement returns false, call RVA `0x00341B15` invokes
`Level__Init_helper_738650(0)` and jumps to the loop head. That helper clears
the partial Level/RoomDescriptor result. On success, call RVA `0x00341C22`
invokes `BossPool__commit_floor` (RVA `0x00021B50`), which performs:

```text
permanentRemoved |= levelBlacklist
clear(levelBlacklist)
```

## State ledger

| State | Owner | Attempt start | Mutation evidence | Failure value | Rollback? | Next attempt |
|---|---|---|---|---|---|---|
| Level RNG | Level, fields used at `+0x182D4` | Previous persistent state | Boss/type8/shop/treasure inline draws in `0x003394A4..0x0033A76B` | Advanced | No | Exact failure-time state |
| LevelGenerator RNG | one `LevelGenerator` constructed before loop | Previous persistent state | topology and force-dead-end paths under RVA `0x005ADBB0` | Advanced | No | Exact failure-time state |
| BossPool RNG | each of 37 pool objects, `+0x28` | Previous pool state | seven pre-rolls in RVA `0x00022830` | Advanced by seven | No | Exact failure-time state |
| BossPool local weighted RNG | stack copy | Constructed after seven pre-rolls | one weighted draw in `BossPool::PickBoss` | Dies at return | N/A | Recreated from the next attempt's post-pre-roll persistent state |
| Boss level blacklist | BossPools manager `+0x8BC` | Explicitly zeroed | selected boss bit set at RVA `0x00022620` | Contains failed-attempt boss | Yes: cleared, not restored | Empty |
| Permanent removed bosses | BossPools manager `+0x8AC` | Prior successful-floor state | success-only RVA `0x00021B50` | Unchanged on failure | N/A | Unchanged |
| Init-time BossPool shuffle | pool entry vector | Fixed at run initialization | MT19937 Fisher-Yates at RVA `0x000218E0` | Unchanged | No reset needed | Same order |
| RoomConfig current weights | global RoomConfig entry `+0x34` | reset once by Level::Init | selected entry write RVA `0x0042CD95` | Decayed | No | Decayed value |
| RoomConfig initial weights | entry `+0x30` | resource value | never mutated by selector | Unchanged | N/A | Unchanged |
| RoomConfig candidate vectors | selector stack/heap temporaries | reconstructed per call | query and exact-door subset | destroyed | N/A | Reconstructed in resource order |
| dead-end candidate array | LevelGenerator `+0x370..+0x374` | rebuilt by topology | stable erase in Determine/GetNewEndRoom | partially consumed | Discarded with topology | New topology order |
| generated topology rooms/map | LevelGenerator | `Generate` clears/rebuilds | topology and reshape functions | partially reshaped | Discarded | Fresh topology using continuing generator RNG |
| Level RoomDescriptors | Level | cleared before placement | assignment RVA `0x00338AB0` | partial | Discarded by `0x00338650` | Empty |
| stage seed | Seeds/Level | fixed for the floor | no attempt mutation | unchanged | N/A | same stage seed |
| target room count | outer local | prior value | increments only after an insufficient-dead-end attempt when loop number is >=10 and divisible by 5 | current value | No | current/incremented value |
| retry counter | outer local | incremented at loop head | RVA `0x00341771` | incremented | No | next integer |
| special-room used bits | `Game+0x26548` | prior run/attempt state | MiniBoss assignment in `0x0033BAB6..0x0033BBAE` | may contain an immediately assigned subtype bit | No | exact failure-time bitset |

## High-value regression cases

`tests/fixtures/boss_geometry_retries.json` locks the first two attempts for:

- NORMAL `0x00000CAE`: failed Boss 56, next Boss 13;
- NORMAL `0x0000247A`: failed Boss 84, next Boss 56;
- HARD `0x000022CD`: failed Boss 1, next Boss 44.

In all three, attempt 1 starts with attempt 0's final Level,
LevelGenerator, and persistent BossPool RNG states. Attempt 0's boss bit is
not committed, while its selected Boss RoomConfig weight remains decayed.

`tests/fixtures/treasure_geometry_retry.json` additionally locks NORMAL seed
1, whose first attempt reaches Treasure and then fails geometry. This proves
the transaction semantics are not specific to the Boss failure site.

## Consequence

The retry operation is not an all-state snapshot/rollback transaction. Only
the partial geometry/descriptors and per-attempt boss blacklist are discarded.
Any offline implementation that recreates Level RNG, LevelGenerator,
BossPools, or RoomConfig weights from the stage seed after a placement failure
will diverge on the immediately following attempt.

## M6 and late-variant extensions

The canonical blocks from Planetarium through Secret do not return false.
`PlaceSecretRoom` returning null is an allowed result: its earlier
RoomConfig-weight and LevelGenerator-RNG effects remain and the caller
continues. Ultra placement null is handled the same way at its direct caller.

The ordinary `ROOM_DEFAULT` configuration pass after Ultra is different. A
missing compatible config reaches the false return at RVA `0x0033CF06`; its
outer-loop rollback is exactly the transaction described above. All
post-Treasure Level draws, Secret candidate draws, RoomConfig decays and
immediate special-room used-bit writes survive into the next attempt. The
topology, Secret/Ultra descriptors and connection mutations are discarded.

Therefore the M6 “through Secret” result is not a successful transaction
commit. The current floor's boss blacklist must remain per-attempt until Ultra
and all late ordinary RoomConfig assignments have succeeded. Only the full
post-topology true return permits `BossPool__commit_floor` at RVA `0x00021B50`.
