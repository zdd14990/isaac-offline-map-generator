# Late normal RoomConfig failure semantics

Executable profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Status: complete canonical Basement I NORMAL/HARD pass `CONFIRMED_BINARY`.
External validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Exact position

The pass begins only after Secret and Ultra Secret:

```text
Secret
-> Ultra Secret
-> collect still-unconfigured generated rooms (`0x0033CB97` -> `0x005AF0E0`)
-> select concrete ROOM_DEFAULT RoomConfig (`0x0033CCDE`)
-> assign descriptor (`0x0033CD07`)
```

This proves ordinary ROOM_DEFAULT Variant selection cannot be moved before
special-room type assignment without changing control flow and RNG/weight
consumption.

## Exact canonical assignment

`LevelGenerator::collect_rooms` reads the non-dead-end vector at `+0x37c`
first and the current remaining dead-end vector at `+0x370` second. All rooms
removed by special placement, plus appended Secret/Ultra descriptors, are
excluded. GridIndex 84 receives the fixed stage-0 ROOM_DEFAULT variant 2 and
does not consume a selector seed.

For every other collected descriptor the binary:

- reads final RoomShape and required door bits from the GeneratedRoom;
- advances persistent Level RNG index 35 once for the selector seed;
- selects stage 1, ROOM_DEFAULT, subtype 0, mode 0 with weight reduction;
- uses difficulty 1..5 for NORMAL and normally 5..10 for HARD;
- lowers HARD minimum to 1 when the pre-draw Level RNG state has low three
  bits zero;
- assigns the returned config immediately before visiting the next room.

After successful assignment, the caller advances Level RNG once for each
GeneratedRoom excluded from the ordinary collection. The canonical frozen
Basement I shortage/repair count is zero; its noncanonical helper path is not
entered.

## Failure behavior

For each collected ordinary room the caller requests a concrete compatible
RoomConfig. If the selector returns null, the function follows the warning and
cleanup path ending at RVA `0x0033CF06` and returns false. A later repair/
shortage path can reach the same false result. The outer dungeon loop treats
this exactly like Boss/Treasure geometry failure: the partial topology and
descriptors are discarded and a new entire-floor attempt begins.

The outer retry does not rewind:

- persistent Level RNG;
- persistent LevelGenerator RNG;
- BossPool seven-draw pre-roll state;
- RoomConfig mutable weight decay from Boss through Ultra and any already
  selected ordinary rooms;
- immediately written special-room used bits.

It clears the per-attempt boss blacklist and discards topology, descriptors,
dead-end arrays and temporary candidate lists. Permanent boss removal remains
unmodified because it is committed only after the full attempt returns true.

## Accepted-layout consequence

“Completed through Secret” was not “accepted floor.” The full Basement I
research pipeline now runs Ultra and this pass before committing the BossPool
attempt blacklist, so its returned descriptors are the accepted layout. The
20,000-case clean/reference corpus observed no natural missing-config failure;
directed fixtures cover that branch and outer transaction behavior.

The successful function continues into a fixed negative-GridIndex descriptor
lifecycle tail. That tail cannot reject or change the accepted 13x13 layout,
but its RNG and RoomConfig mutations must be recovered before Basement II
generation state can be replayed.
