# Product input sufficiency

Profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

## Basement I fresh run

`seed + difficulty` is sufficient only after selecting a canonical generation
profile. The currently implemented profile is:

```text
fresh ordinary vanilla run
Stage 1 / StageType ORIGINAL / main route
no challenge, daily, ascent, seed effect, effective curse, or XL
canonical character with no generation-affecting collectibles
max hearts 6, full health, zero coins
canonical installed achievements/unlocks, including Planetarium availability
no previously visited special room-type state
empty special-room used-bit set at the fresh-run boundary
installed room resources and Boss pools from the frozen executable profile
all relevant installed special-room entries available
```

Under that profile, every state value through the accepted Basement I layout is either fixed or can
be deterministically replayed from the start seed. `RunGenerationState` and
`FloorGenerationState` keep the independently owned streams and mutable
tables distinct.

## Stage 2+

`seed + difficulty + stage` is not generally sufficient for a direct isolated
call. A correct offline tool has two possible contracts:

1. replay the canonical run-generation lifecycle from the start seed through
   every prior floor; or
2. accept a serialized `RunGenerationState` containing all persistent owners.

The first option preserves a simple user interface. The second is required to
represent arbitrary in-progress gameplay state.

## State classification

| State | Seed-replayable under canonical profile? | Can depend on gameplay choices? |
|---|---|---|
| 37 BossPool initial seeds and shuffles | Yes, from gameStartSeed | No |
| BossPool persistent RNG after prior generated floors/retries | Yes if prior generation is replayed | Continue/save timing can supply restored state |
| permanent removed bosses | Yes for canonical replay | Yes for arbitrary route/continued run |
| RoomConfig current weights | Reset by each Level::Init for relevant pools | Mods/custom resource lifecycle can differ |
| prior floor topology failures/retries | Yes | No, under fixed state profile |
| route and StageType | No, must be selected/profiled | Yes |
| character | No, must be selected/profiled | Yes |
| collectibles | No | Yes |
| challenge/game mode/daily | No, must be selected/profiled | Yes |
| achievements/unlocks | No | Yes, save-specific |
| curse/XL | Sometimes seed-derived, but state effects can override | Yes through items/effects/routes |
| room visitation/type state | No for arbitrary continued run | Yes |
| MiniBoss/special-room used bits (`Game+0x26548`) | Yes when every prior attempt/floor is replayed | Yes for an arbitrary continued/save state |
| health, max hearts and coins | Fixed by the fresh canonical profile only | Yes |
| Planetarium and other room unlock gates | Fixed by the named unlock profile only | Yes, save-specific |

## Recommended product contract

Keep the public inputs `Seed`, `Difficulty`, and `Floor`, but bind them to a
named canonical profile. For Floor N, replay all generation-only state from a
fresh run to N without simulating gameplay. If a needed branch depends on a
player choice (route, character, collectible, challenge, unlock profile),
require it explicitly or fail closed. Never silently substitute a default in
exact mode.

The canonical Basement I NORMAL/HARD accepted 13x13 layout is now supported by
the research API. Other floors remain `UNSUPPORTED — FAIL CLOSED`. Before
Stage 2 can be replayed, the non-layout post-success lifecycle tail must also
be recovered because it mutates persistent RNG/config state.

## Basement I accepted-layout conclusion

The public-input conclusion does not change for the named fresh Basement I
profile: `seed + difficulty` is sufficient because all C/D inputs are fixed by
that profile and A/B state is replayed. It is not sufficient for an arbitrary
Basement I game state unless health/coins, collectibles, character,
achievements, visitation and special-room used bits are also supplied.

For Stage 2+ a direct stateless `get_floor(seed, stage, difficulty)` remains
unsound. BossPool progression, RoomConfig weights, used bits and prior floor
generation must be replayed; route and gameplay choices that are not a
function of the seed require explicit input or a canonical policy.
