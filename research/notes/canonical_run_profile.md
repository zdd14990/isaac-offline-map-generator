# Canonical Vanilla Run generation profile

Frozen executable SHA-256:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Later floors are not functions of `start seed + difficulty` alone. This file
defines the explicit research profile under which sequential floor support is
recovered. It is intentionally narrow and fail-closed; it is not a claim that
every real save or playthrough produces the same map.

## Identity and route

- ordinary single-player Isaac (`PlayerType 0`);
- NORMAL or HARD only;
- no challenge, daily, custom seed effect, ascent, online/co-op or greed mode;
- `STAGETYPE_ORIGINAL` and ordinary main-route progression;
- frozen vanilla Repentance+ resources, no mods or overlays;
- no continue/load-state mutation and no manual stage-seed mutation.

## Persistent/unlock profile

The profile uses the base fresh-save generation gates:

- optional achievement-gated boss overrides are false;
- optional achievement/progression bytes read directly by generation are
  false and their associated counters/vectors are empty;
- room resources are the complete frozen vanilla STB database, but the API
  rejects any selector branch that requires an unmodeled runtime unlock
  predicate;
- the character has no unlock-dependent D6 starting item.

This is deliberately different from an "all unlocks" save. Unlock profile is
part of the generator cache key and cannot be changed without a separate
binary proof/corpus.

## Canonical between-floor gameplay state

Only generation-affecting state is represented. The canonical transition
assumes:

- no optional pickup is collected, including treasure, shop, boss, devil,
  angel, trinket, card, pill or pickup resources;
- no optional room is entered for purposes of visit counters;
- no donation, beggar, sacrifice, dice, reroll or active-item effect occurs;
- health remains six full red-heart containers, coins remain zero, and no
  collectible is added;
- no damage/deal penalty, shop visit, donation or other optional persistent
  generation modifier is introduced;
- the mandatory boss is defeated and the ordinary next-floor transition is
  taken, but combat/movement/drop simulation is otherwise outside scope.

These rules are a profile definition, not inferred gameplay. They make the
generation-only replay deterministic while preserving the binary's actual
floor lifecycle, RNG owners, BossPool removals, RoomConfig weights and
special-room used bits.

## State replay contract

To generate a supported later floor, the implementation starts from the run
seed and replays every preceding supported floor in order. A floor snapshot
includes at least:

- all 37 persistent BossPool RNG states and permanent removed-boss bits;
- current RoomConfig weights, including pools that the next `Level::Init`
  does and does not reset;
- persistent special-room used bits and relevant generation counters;
- current stage-seed slots and their mutation status;
- the explicit canonical player/unlock/route state above.

The previous floor's Level RNG is recorded for proof, but the next ordinary
floor initializes its Level RNG from that floor's own stored stage seed. It is
not silently substituted for the next stage seed.

## Non-seed inputs that remain real gameplay choices

Arbitrary play can change later maps through collected items (notably Voodoo
Head), health/coins, shop and room visits, devil/angel state, special-room
used bits, curses/seed effects, achievement/unlock gates, route choice,
character-specific starts, co-op state, rerolls and stage-seed mutations.
Those values cannot generally be recovered from the start seed. A future
general API must accept them explicitly or replay a supplied gameplay event
record. The ordinary Research Preview supports only the profile above.

External gameplay validation remains:
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.
