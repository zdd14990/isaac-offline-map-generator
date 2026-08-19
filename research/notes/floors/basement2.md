# Basement II — ORIGINAL route reconstruction

Frozen executable: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

External gameplay validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

This note records only the canonical base-profile generation replay defined in
`research/notes/canonical_run_profile.md`. Its complete accepted layout and
successful generation lifecycle tail are now `CONFIRMED_BINARY` and exposed
through the fail-closed Research Preview registry. External gameplay
validation remains an independent, unavailable evidence dimension.

## What remains identical to Basement I

- Initial stage seeds come from the same frozen 81-slot seed table.
- The persistent Level RNG uses shift index 35 `(5,9,7)`.
- `LevelGenerator` uses the confirmed topology geometry implementation,
  Shapes 1..12, a start room at GridIndex 84 and the same retry transaction.
- The ORIGINAL Basement RoomConfig stage remains stage 1; special rooms use
  stage 0 where the binary does so.
- Boss selection uses Basement BossPool index 1 and the same ordered binary32
  weighted picker.

## Stage-2 floor-entry differences

`Level::Init` makes a stack copy of the Level RNG after its second persistent
draw. Unlike Basement I, Stage 2 executes the ordinary curse gate:

- denominator 80 on NORMAL and 40 on HARD;
- selector modulo 6 after a successful gate;
- selector 0 (Labyrinth) consumes its draw but cannot set Labyrinth on even
  Stage 2;
- selectors 1..5 map to Lost, Darkness, Unknown, Maze and Blind;
- no-mod canonical curse normalization is the identity.

The persistent Level RNG independently supplies the base-count bit and
`LevelGenerator` constructor seed. The target count is the Stage-2 base 11/12,
plus four under Lost, plus `2 + bit` on HARD. Required dead ends are 6.
RoomConfig difficulty windows are 5..10 on NORMAL and 10..15 on HARD.

Static artifact:
`research/binary/basement2_floor_init_binary_verification.json`.

The independent clean/reference topology corpus covers 10,000 NORMAL and
10,000 HARD seeds and all Shapes 1..12:
`research/binary/basement2_topology_differential_report.json`.

Status of this isolated leaf: `CONFIRMED_BINARY`.

## Inherited Basement BossPool

Basement I commits its accepted boss to the permanent removal bitset. The
Stage-2 selector resumes pool index 1 from the committed persistent RNG state;
it must not reinitialize the pool or discard the removed id.

The ordinary selector again consumes seven persistent pool draws. Its local
weighted draw is not written back. If the target lands on the previously
removed entry, `BossPool::PickBoss` repeatedly remaps the same binary32 target
without another RNG draw. After ten unsuccessful scans it searches circularly
from the following shuffled entry. A null result makes the caller clear both
permanent and attempt-local bits for every pool entry, advance the local copy
again and retry, up to ten outer tries; terminal exhaustion returns Monstro
id 1.

Static evidence:

- `BossPool::PickBoss` RVA `0x00022620`, 362 bytes;
- `Level::select_boss_id` RVA `0x00022830`, 1498 bytes;
- `research/binary/boss_pool_repick_binary_verification.json`.

Clean/reference code restores only read-only generation state from the
accepted Basement-I result. It does not alter the confirmed Boss selection
algorithm. Natural remap fixtures are selected from the differential corpus;
the first in seeds 1..20 is start seed 7 for both NORMAL and HARD.

The aggregate report contains 10,000 NORMAL and 10,000 HARD comparisons,
140,000 persistent pre-rolls and 2,127 natural repicking seeds, with up to
three remaps:
`research/binary/basement2_boss_pool_differential_report.json`.

Status of this isolated leaf: `CONFIRMED_BINARY`. This does not by itself make
the complete Basement-II floor supported.

## Shared Boss through Treasure boundary

Static control-flow comparison of `Level::place_post_topology_rooms` at RVA
`0x00339370` shows that canonical Stage 2 uses the same recovered Boss,
RoomType 8, Shop and Treasure leaf calls. The floor-specific inputs are the
Stage-2 topology, current RoomConfig stage 1, inherited mutable weights and
resumed BossPool state described above. The current attempt's selected boss
remains uncommitted at this boundary.

The aggregate clean/reference report covers 10,000 NORMAL and 10,000 HARD
start seeds. NORMAL makes 10,449 Stage-2 attempts and HARD 10,403; Treasure
geometry rejects 448 and 403 attempts respectively. No failed attempt is
exposed as the accepted boundary result.

Artifacts:

- `research/binary/basement2_through_treasure_binary_verification.json`;
- `research/binary/basement2_through_treasure_differential_report.json`.

Status of this composed boundary: `CONFIRMED_BINARY`.

## Treasure through Secret

Stage 2 changes four canonical predicates before Secret:

- `Game::GetPlanetariumChance` computes
  `f32(f32(1 * 0.20f) + 0.01f)`. Its exact result is
  `0.21000000834465027`, float32 bits `0x3E570A3E`; a direct conversion of the
  decimal literal `0.21` would be one ULP lower and is not used.
- MiniBoss still consumes the second modulo-three RNG draw after a failed
  primary gate, but that fallback assignment is restricted to Stage 1.
- Challenge accepts an even gate on Stage 2 when the canonical single-player
  health predicate is true. Odd gates reappend the candidate.
- Chest can pass the explicit even-stage list on Stage 2 with canonical max
  hearts. The zero-coin Arcade alternative remains unassigned.

All remaining recovered blocks retain their existing ordered config lookup,
dead-end consume/reappend and persistent used-bit behavior. Secret still
selects type 7 config first and then runs the confirmed 169-cell geometry
leaf on the continuing LevelGenerator RNG.

The aggregate report contains 10,000 NORMAL and 10,000 HARD deep comparisons.
It reaches every named changed branch: Planetarium assigns 1,983/1,991 times,
Challenge 2,247/2,833, Chest 1,077/1,549 and MiniBoss 1,424/1,648. Secret
coverage includes adjacency counts 1..4, tie vectors 1..8, 97 boundary
placements, 5,145 large-room neighbor cases and 4,192 L-shape neighbor cases.
The natural corpus always finds a Secret candidate; the already retained
directed null-candidate fixture covers that allowed result.

Artifacts:

- `research/binary/basement2_post_treasure_binary_verification.json`;
- `research/binary/basement2_secret_differential_report.json`.

Status of this composed pre-Ultra boundary: `CONFIRMED_BINARY`.

## Ultra, late defaults and successful lifecycle

Static verification confirms that the type-29 and late ROOM_DEFAULT selectors
both receive the current RoomConfig stage returned by
`Level::get_room_config_stage`; neither embeds a Basement-I stage literal.
Ultra null remains allowed, late null remains the whole-attempt false return,
and the second Basement boss is committed only after the late pass succeeds.

The successful post-layout tail also shares its Stage-2 branch. Both door
chance RNG draws remain, but descriptor-flag writes require effective stages
above four and above three. The fixed negative descriptor sequence changes
only at current RoomConfig stage 13 or StageType 4/5, neither of which applies
to canonical Basement II ORIGINAL. The next-floor snapshot therefore advances
the persistent Level RNG by 28 draws and records two committed Basement boss
removals.

Static artifacts:

- `research/binary/basement2_accepted_layout_binary_verification.json`;
- `research/binary/basement2_post_layout_lifecycle_binary_verification.json`.

The aggregate clean/reference corpus covers 10,000 NORMAL and 10,000 HARD
start seeds. NORMAL produces 10,449 Basement-II attempts with 432 retrying
seeds; HARD produces 10,403 attempts with 394 retrying seeds. Both reach a
maximum of three attempts. All 20,000 accepted descriptor maps, RoomConfig
assignments, final RNG/weight/used-bit states, second BossPool commits and
lifecycle handoffs match. The tail comparison covers 560,000 persistent Level
RNG draws, 160,000 fixed descriptor assignments and 160,000 private-stream
transitions, with no missing config. Natural Ultra-null and late-null counts
are zero; their permitted edges remain covered by the existing directed tests.

Aggregate artifact:
`research/binary/basement2_full_differential_report.json`.

Status: complete canonical Basement II accepted layout and successful
lifecycle handoff `CONFIRMED_BINARY`.

## Preview integration and next boundary

`src/isaacmap/preview.py` dispatches through `SUPPORTED_FLOORS`; Basement II
replays Basement I's generation-only lifecycle, generates only the accepted
Stage-2 attempt, and exposes no failed-attempt descriptors. The UI shows both
floors as supported, reports the offline replay path and remains fail closed
for Caves I and later floors.

The next unsupported lifecycle boundary is canonical Caves I (LevelStage 3).
