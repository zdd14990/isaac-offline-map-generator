# Binary and Format Evidence Ledger

Executable profile:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Addresses are RVAs unless explicitly marked as virtual addresses. Raw Capstone
listings are under `research/decomp/`.

## Seed display encoding

Feature: `uint32 ↔ XXXX XXXX`, checksum, alphabet, invalid-seed rules

Binary function: `Seeds::Seed2String`, `Seeds::String2Seed`, validation wrapper

Address/RVA: `0x005EB5B0`, `0x005EB6B0`, `0x005EB590`

Callers: not yet exhaustively mapped

RNG calls: none

Inputs: nonzero 32-bit ordinary run seed or 9-byte seed string

Outputs: canonical display seed, decoded seed, or zero invalid sentinel

Confidence: `CONFIRMED_BINARY`

Evidence:

- alphabet at RVA `0x00780D30` is
  `ABCDEFGHJKLMNPQRSTWXYZ01234V6789`;
- XOR mask is `0x0FEF7FFD`;
- eight five-bit symbols encode 32 obfuscated seed bits plus an eight-bit
  checksum;
- checksum repeatedly adds the low byte, shifts seed right by five, then
  rotates the checksum byte left by one;
- decoder requires length 9 and literal space at index 4, rejects unmapped
  bytes, recomputes checksum, and returns zero on any failure;
- wrapper at RVA `0x005EB590` treats decoded zero as invalid.

Implementation: `src/isaacmap/seed.py`

Tests: `tests/unit/test_seed.py`

Known limitations: Easter Egg/special seed dispatch is a separate path and is
not implemented. Ordinary run seeds only.

## RNG core

Feature: state layout, shifts, `SetSeed`, `Next`, `RandomInt`, `RandomFloat`

Binary functions:

- game constructor RVA `0x003E8F90`
- `SetSeed` RVA `0x003E8FE0`
- `RandomInt` RVA `0x003E9020`
- `RandomFloat` RVA `0x003E9080`
- `Next` RVA `0x003E90F0`

Callers: core callers are numerous; ordinary floor stream ownership is now
mapped through `Level::Init` and the dungeon generator

RNG calls: each of `Next`, `RandomInt`, and `RandomFloat` performs exactly one
xorshift advance; `RandomInt(0)` still advances and then returns zero

Inputs: 16-byte state `{seed, shift1, shift2, shift3}`

Outputs: new `uint32`, unsigned remainder, or binary32 float

Confidence: `CONFIRMED_BINARY`

Evidence:

- `Next`: `x ^= x >> a; x ^= x << b; x ^= x >> c`, with 32-bit wrap;
- `SetSeed` clamps unsigned shift index to 80;
- constructor asserts for index >= 81;
- all 243 dwords in the 81-entry table at RVA `0x0071F4C8` match the Python
  profile (`research/binary/rng_binary_verification.json`);
- index 60 is current-binary-specific `(9,5,14)`;
- `RandomInt` uses x86 unsigned `div` remainder;
- `RandomFloat` uses unsigned correction `{0.0, 4294967296.0}` and binary32
  scale bit pattern `0x2F7FFFFE`, not an idealized exact `2^-32` constant;
- zero-state draw follows an assertion/int3 path; Python raises instead of
  emulating a crash.

Implementation: `src/isaacmap/rng.py`

Tests: `tests/unit/test_rng.py`, plus static table/constant verifier

Known limitations: many later special-room RNG streams and offsets remain
unproven. The scoped Basement I pre-topology stream is covered separately
below; this still does not prove a complete floor.

## Packed resource and STB database

Feature: named XML/STB extraction and room-record parsing

Binary function: data format; not a generator function

Address/RVA: not applicable

Confidence: `CONFIRMED_OPEN_SOURCE` plus local checksum/EOF validation

Evidence: current archive checksums validate; all 61 merged room STBs parse as
`STB1` to exact EOF; format is independently cross-checked with Gibbed.Rebirth
and Basement Renovator.

Implementation: `src/isaacmap/archive.py`, `src/isaacmap/resources.py`

Tests: `tests/unit/test_resources.py`; full local database index run

Known limitations: archive raw-encrypted MiniZ transitions are not implemented,
but no current named XML/STB target uses that transition.

## LevelGenerator topology family

Feature: floor-topology generator entry and supporting placement functions

Binary functions / RVAs:

- `Level::Init`: `0x00344940`
- ordinary dungeon generator: `0x00340E10`
- `LevelGenerator` constructor: `0x005ADAF0`
- `LevelGenerator::Generate`: `0x005ADBB0`
- room-expansion loop: `0x005B04D0`
- neighbor-candidate builder: `0x005B0B00`
- candidate shuffle: `0x005B1B20`
- forced-dead-end helper: `0x005AF1E0`
- `LevelGenerator::DetermineBossRoom`: `0x005AED50`
- `LevelGenerator::mark_dead_ends`: `0x005AFB10`

Callers: the ordinary dungeon call at VA `0x007453F2` is inside the
`Level::Init` function beginning at VA `0x00744940`; the dungeon path
constructs and calls `LevelGenerator`

RNG calls: branch-specific draw order is recovered for candidate generation,
shuffle, expansion selection, loop acceptance, queue insertion, forced
dead-end candidates, and retry control

Inputs/outputs: signature and 13×13 structure are strongly supported by the
REPENTOGON ZHL layout; current binary signatures match

Confidence: scoped topology output `CONFIRMED_BINARY`; external gameplay
dimension `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`

Evidence: current-binary byte signatures match the pinned REPENTOGON
definitions; `LevelGenerator` owns a 169-entry room map, blocked positions,
RNG, rooms, dead ends, and non-dead ends. Headless static decompilation recovers
the main expansion loop after correcting a false `noreturn` classification on
the internal logger. The shuffle is Fisher-Yates. The neighbor builder consumes
13 draws per valid/free door target for its ordered large-room candidates.
Expansion consumes one or four branch draws plus one queue-insertion draw after
each placed room.  Full branch order and every dynamic ledger field are in
`research/notes/topology_rng_ledger.md` and
`src/isaacmap/topology_reference.py`.

Implementation: binary-derived geometry in
`src/isaacmap/topology_geometry.py`, mechanical reference in
`src/isaacmap/topology_reference.py`, readable port in
`src/isaacmap/topology.py`, and structural comparator in
`src/isaacmap/topology_differential.py`

Tests: `tests/unit/test_topology_geometry.py`, `tests/unit/test_topology.py`,
`tests/unit/test_topology_reference.py`, static constant verifier, 20,000
NORMAL/HARD differential cases and targeted retry/ordering fixtures

Evidence summary: the two independent implementations compare target count,
full 169-entry room map, anchors, shapes, occupied cells, doors, connection
sets, expansion/dead-end order, retries, every generator RNG transition and
final state.  The 20,000-case report contains 7,285,534 matching transitions.
Static proof and entry-state boundaries are recorded in
`research/notes/topology_binary_proof.md` and
`research/notes/topology_inputs.md`.

Known limitations: no accepted current-version gameplay fixture independently
validates the port.  Inputs outside the frozen Basement I contract and all
special-room placement remain incomplete.  Complete-floor output remains
fail-closed.

## Isolated topology instruction emulation

Feature: execute selected topology leaf instructions without loading or
starting the game executable

Binary functions / RVAs:

- canonical grid index: `0x005AFD70`;
- shape-slot predicate: `0x005AF370`.

Method: `scripts/emulate_topology_helpers.py` hash-checks the PE copy, extracts
only the exact function bytes and constants as data, and maps them into
Unicorn-owned x86 memory.  It invokes no Windows loader, PE entry point,
import, game process, Steam component or game loop.

Confidence: instruction results `CONFIRMED_BINARY` for the isolated leaf
functions

Evidence: `research/binary/topology_instruction_emulation.json` records
289/289 canonical-index boundary matches and 192/192 shape/slot/restriction
matches, together with the emulated byte hashes.

Known limitations: whole-`Generate` emulation is
`HIGH_ISOLATION_COST_NOT_BLOCKING_STATIC_PROOF`.  MSVC containers/allocation,
SEH/TLS, security cookies, logging and global data would all need exact stubs.
The leaf emulator is a development verifier, not an Isaac gameplay oracle.

## Start seed to stage seed

Feature: run seed → per-stage generation seed

Binary function: `Seeds::set_start_seed`

Address/RVA: `0x005EB880`

Callers: initial floor consumer is `Level::Init` at RVA `0x00344940`

RNG calls: 14 consecutive advances are stored in `_stageSeeds[0..13]`, then
one additional advance is stored as `_playerInitSeed`

Inputs: nonzero start seed; zero invokes the game's nondeterministic global
random fallback and is rejected by the offline ordinary-seed API

Outputs: `_stageSeeds[14]` and `_playerInitSeed`

Confidence: `CONFIRMED_BINARY` for initial derivation

Evidence:

- input is stored at object offset `+0x4`;
- RNG state is initialized at `+0x8` with literal triple `(3,23,25)` from RVA
  `0x0071F60C`;
- loop counter immediate `0x0E` produces and stores 14 consecutive states at
  `+0x18..+0x4C`;
- one further identical xorshift stores the player-init seed at `+0x50`;
- REPENTOGON's `SetStageSeed` interface independently confirms that a
  `LevelStage` value directly indexes `_stageSeeds[stage]` for `0..13`.
- `Level::Init` selects slot `LevelStage`, except StageType 4/5 increments it;
  the result is capped at 13.

Implementation: `src/isaacmap/stage_seed.py`

Tests: `tests/unit/test_stage_seed.py`; static constant verifier

Known limitations: the binary also has a per-stage mutation/forget path using
another RNG triple. Its exact external conditions remain unmapped. The fresh
ordinary new-run initial selection and transfer are confirmed.

## Basement I pre-topology parameters

Feature: selected stage seed → ordinary Basement I `LevelGenerator` inputs

Binary functions: `Level::Init`, ordinary dungeon generator,
`LevelGenerator` constructor

Address/RVA: `0x00344940`, `0x00340E10`, `0x005ADAF0`

RNG calls: Level RNG uses `(5,9,7)`; on the scoped no-curse path, its third
draw controls the base room-count bit and its fourth draw seeds
`LevelGenerator`. A copied stack RNG produces the same third state and supplies
the HARD bonus bit.

Inputs: fresh ordinary `STAGE1_1`, `STAGETYPE_ORIGINAL`, NORMAL/HARD, no
challenge/daily/ascent state, effective curse, seed effect, Voodoo Head owner,
blocked cell, or prior stage-seed mutation

Outputs: stage seed, four Level RNG draws, generator seed, target count,
required dead ends, allowed-shape mask, and starting room

Confidence: `CONFIRMED_BINARY` within the stated scope

Evidence:

- Level RNG triple `(5,9,7)` at RVA `0x0071F66C`;
- starting constants column 6, line 6 at RVA `0x007AAF30`;
- target NORMAL `8 + bit`, HARD `10 + 2*bit` on Basement I;
- required dead ends 5;
- both Basement difficulty windows contain default rooms of every shape 1..12,
  producing mask `0x1FFE`;
- raw geometry constants match
  `research/binary/topology_binary_verification.json`.

Implementation: `src/isaacmap/floor_init.py`

Tests: `tests/unit/test_floor_init.py`

Known limitations: this section describes only entry values.  The separate
LevelGenerator section proves the scoped room topology; neither section assigns
special-room types.

## Special-room placement after topology

Feature: complete call order and canonical Basement I Boss → RoomType 8 →
Shop → Treasure pipeline after the confirmed topology milestone

Binary functions / RVAs:

- outer dungeon generator: `0x00340E10`;
- topology call: `0x00341A20` → `0x005ADBB0`;
- post-topology call: `0x00341B08` → `0x00339370`;
- Boss identity: `0x00022830`;
- Boss RoomConfig selector: `0x00339080`;
- Boss geometry dispatch / selector: `0x005AEF10`, `0x005AED50`;
- Type8 end-room selector: `0x005AE0E0`;
- shape/door matcher and mutator: `0x005B1220`.

Call order confidence: `CONFIRMED_BINARY`

Generation retry, RoomConfig core, Boss, Type8, Shop and Treasure confidence:
`CONFIRMED_BINARY` under the fresh ordinary Basement state contract

External validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`

Evidence:

- ordinary Basement order begins Boss identity → Boss concrete RoomConfig →
  Boss geometry/assignment → RoomType 8 → saved seed snapshot → Shop →
  Treasure;
- later code order is Planetarium, Dice/Sacrifice, Library, Curse, MiniBoss,
  Challenge, Chest/Arcade, Isaac/Barren, conditional route rooms, Secret,
  Ultra, then ordinary default RoomConfig/Variant assignment;
- special-room concrete STB selection is interleaved before each special
  geometry decision, not deferred to the late ordinary-variant loop;
- M4's ordered dead-end vector is consumed directly; `DetermineBossRoom` and
  `GetNewEndRoom` scan begin-to-end and use `memmove` stable erase;
- Boss requires stored generation distance > 1;
- the matcher can shrink/re-anchor a generated large/L dead end and updates
  occupied cells/connections;
- Type8 transforms an existing generated dead end; it does not append a room;
- Type8 count is 1, or 2 when `FirstCollectibleOwner(0x24D)` succeeds;
- mandatory placement failure returns false, causing the outer generator at
  RVA `0x00341760` to reject that topology and retry without rewinding its
  persistent RNG objects;
- loop-head RVA `0x003382C0` clears only the per-attempt BossPool blacklist;
  success-only RVA `0x00021B50` commits it to permanent removal;
- Level RNG, LevelGenerator RNG, seven BossPool pre-rolls and RoomConfig weight
  decay survive failure, while topology/descriptors/dead-end temporaries are
  discarded;
- Shop uses its own index-19 subtype stream, then selects and stable-erases a
  concrete type-2 end room;
- Treasure runs after Shop mutation, preserves its conditional Level draws,
  uses stage-1 then stage-0 RoomConfig fallback with one seed, and can return
  the same whole-attempt failure signal.

RNG objects / calls:

- Level RNG index 35 persists through post-topology and outer retries;
- Boss RoomConfig uses a private index-39 stream seeded by the Level draw at
  RVA `0x003394A4`, then one-call index-7 RoomConfig selectors;
- Type8 uses private index 9 seeded at `0x00339A87`, with per-iteration draw
  at `0x00339B1E`;
- the post-Type8 Level draw at `0x00339BE7` is saved as a snapshot; Secret and
  Ultra later copy this same numeric seed into distinct index-1 and index-71
  streams while Shop/Treasure continue the Level RNG.

Implementation:

- `src/isaacmap/special_rooms_reference.py`;
- `src/isaacmap/special_rooms.py`;
- `src/isaacmap/special_rooms_differential.py`;
- `src/isaacmap/room_config_reference.py`;
- `src/isaacmap/room_config.py`;
- `src/isaacmap/basement1_pipeline_reference.py`;
- `src/isaacmap/basement1_pipeline.py`;
- `src/isaacmap/basement1_pipeline_differential.py`.

Tests: `tests/unit/test_special_rooms.py`, `tests/unit/test_room_config.py`,
and `tests/unit/test_basement1_pipeline.py`. The assembled 20,000-case
NORMAL/HARD differential compares every attempt, candidate/config/geometry
trace, binary condition trace, RNG transition and final persistent state. It
records 1,433 retrying seeds, including three Boss-geometry and 1,523
Treasure-geometry failure attempts. Across 21,526 attempts it compares
400,499 post-topology RNG transitions, 114,244 RoomConfig selector calls,
90,493 candidate tests and 107,615 condition traces; Shapes 1..12 are reached
in both topology and geometry-candidate coverage.

Detailed evidence:

- `research/notes/post_topology_callgraph.md`;
- `research/notes/special_room_rng_ledger.md`;
- `research/notes/special_room_binary_proof.md`;
- `research/notes/generation_retry_semantics.md`;
- `research/notes/room_config_binary_proof.md`;
- `research/binary/special_room_differential_report.json`;
- `research/binary/basement1_pipeline_differential_report.json`.

Known limitations: this section is the M5 boundary. Later sections extend the
canonical proof through Secret, Ultra and the accepted late ordinary pass.

## BossPool initialization and selection streams

Feature: 37 fixed BossPools, start-seed derivation, deterministic entry
shuffle, persistent selection RNG and local weighted selector

Binary functions / RVAs:

- BossPools XML/init consumer: `0x000218E0`;
- BossPool weighted picker: `0x00022620`;
- Level boss identity selector: `0x00022830`;
- Game initialization owner / exact call: `0x002F8140`, `0x002F8579`;
- continue/state loader: `0x0028CDC0`;
- MT19937 seed/next: `0x004FD3C0`, `0x004FD410`.

Inputs: `Seeds._gameStartSeed` at `Game+0x1BB88`, BossPools owner at
`Game+0x1AF70`, config-stage mapping, achievements/unlocks, character/game
mode, shuffled XML entries and removed/per-level boss bitsets

Outputs: 37 persistent per-pool RNG objects, shuffled entry vectors, chosen
Boss id and updated removal state

Confidence: initialization/shuffle/object identity, fresh ordinary weighted
core, Basement I retry/commit lifecycle and inherited canonical Basement-II
remap/fallback/reset leaf `CONFIRMED_BINARY`; optional override/continue
profiles are rejected by the current canonical entry point; external validation
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`

Evidence:

- call RVA `0x002F8579` loads `Game+0x1BB88`, sets
  `ECX=Game+0x1AF70`, and calls `0x000218E0`;
- exactly 37 chained index-26 `(3,13,7)` advances seed the fixed slots;
- each pool's persistent RNG uses index 17 `(2,21,9)`;
- a separately seeded MT19937 performs per-pool init-time Fisher-Yates without
  advancing the persistent xorshift;
- pool stride is `0x3C`; entry stride is `0x14` with current/initial weight,
  achievement condition and alternate boss id;
- the current XML has 25 named pools but the runtime table has 37 slots;
- original Basement maps to config-stage/pool index 1;
- ordinary boss selection advances the persistent selected pool seven times,
  then performs weighted selection on a local copy whose final state is not
  stored back;
- the persistent state remains at
  `Game+0x1AF70+poolIndex*0x3C+0x28`.
- an unavailable inherited entry remaps the same binary32 target without an
  RNG draw; the tenth scan enters circular fallback;
- a null picker result clears both manager removal bitsets for the pool and
  retries a newly advanced local threshold, with a ten-try Monstro fallback;
- 20,000 Basement-II inherited-state comparisons cover 140,000 persistent
  pre-rolls and 2,127 natural repicking seeds, with up to three remaps.

Implementation:

- `src/isaacmap/boss_pool_reference.py`;
- `src/isaacmap/boss_pool.py`;
- `src/isaacmap/boss_pool_differential.py`.

Tests: `tests/unit/test_boss_pool.py` and
`tests/unit/test_basement2_boss_pool.py`; combined Basement-I pipeline corpus
plus `research/binary/basement2_boss_pool_differential_report.json`

Detailed proof: `research/notes/boss_pool_binary_proof.md`

Known limitations: achievement/character/game-mode special-boss branches and
arbitrary continue state are not exposed through an exact offline state API.
They are outside the canonical profile and fail closed.

## Post-Treasure blocks and Secret Room

Feature: canonical Basement I Treasure -> conditional special-room family ->
Secret Room, plus the downstream Ultra and late ordinary call boundaries

Binary functions / RVAs:

- post-topology caller: `0x00339370`;
- Secret forbidden-cell builder: `0x00338D70`;
- `LevelGenerator::PlaceSecretRoom`: `0x005AE170`;
- Secret callsites: config `0x0033C716`, forbidden set `0x0033C72E`, geometry
  `0x0033C741`, assignment `0x0033C7B0`;
- Ultra entry call: `0x0033CB05` -> `0x005AE640`;
- late default-room collection: `0x0033CB97` -> `0x005AF0E0`;
- late default selector/assignment: `0x0033CCDE`, `0x0033CD07`;
- late false return: `0x0033CF06`.

Inputs: confirmed M5 attempt state, current ordered dead-end vector and
descriptors, saved post-Type8 snapshot, persistent Level and LevelGenerator
RNGs, RoomConfig mutable weights, health/coins/unlock/visitation profile and
special-room used bits

Outputs: ordered middle special-room mutations, possible new type-7 1x1 room,
updated 169-cell map/connections, persistent RNG/weight/used-bit state, and an
uncommitted current-attempt BossPool blacklist

Confidence: through Secret `CONFIRMED_BINARY` for the frozen fresh ordinary
Basement I NORMAL/HARD profile. Ultra and the complete late pass are covered by
their own `CONFIRMED_BINARY` sections below. External gameplay dimension:
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Evidence:

- the exact order is Planetarium, Dice/Sacrifice, Library, Curse, MiniBoss,
  Challenge, Chest/Arcade, Isaac/Barren, three route conditions, Secret, a
  Stage-11 condition, Ultra, then ordinary default selection;
- concrete configurations precede each middle end-room geometry pass;
- rejected conditional end-room candidates are appended to the vector end,
  so skipped assignments still mutate later candidate order;
- MiniBoss assignment immediately writes one of the persistent
  `Game+0x26548` bits and a later floor-attempt failure does not clear it;
- Secret config begins from the saved post-Type8 snapshot through separate
  index-1 and index-7 temporary RNG identities;
- Secret geometry scans GridIndex 0..168, draws once for every eligible empty
  cell from persistent LevelGenerator index 35, retains only the maximum score
  in stable scan order, then draws once to resolve that vector;
- scoring penalties are `-6`, `-3`, `0` for one, two, or at least three valid
  cardinal adjacencies; an invalid neighbor door target subtracts 100;
- Secret appends a new 1x1 room/descriptor and refreshes connections rather
  than mutating a topology dead end;
- no-candidate Secret and null Ultra results continue without false return;
- the subsequent ordinary default selector can return false, causing an outer
  retry without rewinding persistent RNGs, weights or used bits; therefore no
  boss removal is committed at the pre-Ultra M6 boundary.

Implementation:

- `src/isaacmap/secret_reference.py`;
- `src/isaacmap/secret.py`;
- `src/isaacmap/basement1_secret_pipeline_reference.py`;
- `src/isaacmap/basement1_secret_pipeline.py`;
- `src/isaacmap/basement1_secret_pipeline_differential.py`.

Tests: `tests/unit/test_basement1_secret_pipeline.py` plus the 10,000 NORMAL +
10,000 HARD differential corpus recorded in
`research/binary/basement1_secret_differential_report.json`. The corpus has
20,000 comparisons over 21,526 attempts and reaches 1/2/3/4-neighbor
candidates, tie vectors of sizes 1..7, map boundaries, large-room neighbors
and every L shape; the no-candidate path is a synthetic unit fixture.

Detailed proof:

- `research/notes/post_treasure_callgraph.md`;
- `research/notes/basement1_condition_matrix.md`;
- `research/notes/secret_rng_ledger.md`;
- `research/notes/secret_binary_proof.md`;
- `research/notes/ultra_secret_entry.md`;
- `research/notes/late_variant_failure_semantics.md`.

Known limitations: this section alone stops at Secret. The assembled accepted
layout is covered below.

## Ultra Secret placement

Feature: type-29 config selection, red-door exclusion/candidate scan, ordinary
13x13 descriptor insertion and red-door bit mutation

Binary functions / RVAs:

- caller/config/exclusion: `0x0033C902..0x0033CB36`;
- `LevelGenerator::PlaceUltraSecretRoom`: `0x005AE640`;
- Level descriptor assignment: `0x0033CB1B`.

Confidence: `CONFIRMED_BINARY` for canonical fresh Basement I NORMAL/HARD;
external gameplay dimension `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Evidence includes static function/control-transfer/constant verification,
complete candidate order/scoring, index-71 config versus persistent index-35
geometry ownership, null semantics, type-29 RoomConfig weight effects, 1x1
descriptor/map mutation and red-door writes. Independent reference and clean
implementations match over 10,000 NORMAL and 10,000 HARD seeds (20,000 total,
21,526 preceding attempts), including natural null, boundary, large/L shape
and tie cases.

Implementation: `src/isaacmap/ultra_secret_reference.py`,
`src/isaacmap/ultra_secret.py`, and `basement1_ultra_pipeline*.py`.

Artifacts: `research/binary/ultra_secret_binary_verification.json`,
`research/binary/basement1_ultra_differential_report.json`,
`research/notes/ultra_secret_binary_proof.md`, and
`research/notes/ultra_secret_rng_ledger.md`.

## Late ordinary RoomConfig and accepted Basement I layout

Feature: post-Ultra ROOM_DEFAULT collection, concrete config assignment,
failure/retry edge and final accepted-attempt transaction

Binary functions / RVAs:

- late caller slice: `0x0033CB5D..0x0033CF22`;
- `LevelGenerator::collect_rooms`: `0x005AF0E0`;
- selector seed draw: `0x0033CCA5`;
- direct RoomConfig selector: `0x0033CCDE`;
- descriptor assignment: `0x0033CD07`;
- excluded-room Level RNG advance: `0x0033CDD2`;
- false return: `0x0033CF06`.

Confidence: canonical fresh Basement I NORMAL/HARD accepted 13x13 layout
`CONFIRMED_BINARY`; external gameplay dimension
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Evidence:

- static byte and transfer verification pins collection order, Start variant,
  HARD minimum gate, shape/door inputs, selector semantics and false return;
- clean and independently mechanical reference leaves compare every query,
  candidate/weight decision, RNG transition, assignment and failure state;
- the full clean/reference pipelines preserve all confirmed retry state and
  commit the BossPool blacklist only after late success;
- 10,000 NORMAL and 10,000 HARD results match over 21,526 attempts, 1,433
  retrying seeds and 126,493 late ordinary assignments;
- final equality includes accepted rooms/map/configs and every persistent
  state owner through the accepted-layout boundary.

Implementation: `src/isaacmap/late_room_config.py`,
`late_room_config_reference.py`, `basement1_full_pipeline.py`,
`basement1_full_pipeline_reference.py` and their differential modules.

Artifacts: `research/binary/late_room_config_binary_verification.json`,
`research/binary/basement1_full_differential_report.json`,
`research/notes/late_room_config_binary_proof.md` and
`research/notes/basement1_full_layout_proof.md`.

Known limitation: the subsequent successful negative-GridIndex descriptor
tail cannot change layout acceptance, but its persistent mutations are needed
before Basement II replay.

## Basement I successful post-layout lifecycle

Feature: fixed negative-GridIndex descriptors and persistent state handoff
after accepted Basement I layout

Binary functions / RVAs:

- successful tail slice: `0x0033D1D6..0x0033D94B`;
- descriptor seed helper: `0x00028940`;
- RoomConfig selector: `0x0042C7D0`;
- explicit Level RNG calls: `0x003E90F0`.

Confidence: canonical fresh Basement I NORMAL/HARD `CONFIRMED_BINARY`;
external gameplay dimension `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Evidence:

- static byte/control-transfer verification pins eight helper calls, eight
  selectors, the negative GridIndexes/types/subtypes and success return;
- two probability draws plus six persistent four-draw descriptor assignments
  and two private-stream seeds consume exactly 28 persistent Level draws;
- Shop index 19 and Angel index 20 keep their private RNG transitions separate;
- clean/reference equality covers descriptor seeds/configs, binary32
  selections/weights, used bits and final Level state;
- 10,000 NORMAL plus 10,000 HARD comparisons recheck 21,526 accepted-layout
  attempts and then compare 560,000 persistent draws and 160,000 fixed
  assignments with no missing config.

Implementation: `src/isaacmap/post_layout_lifecycle.py`,
`post_layout_lifecycle_reference.py`, `basement1_lifecycle.py` and the explicit
generation snapshot in `generation_state.py`.

Artifacts: `research/binary/post_layout_lifecycle_binary_verification.json`,
`research/binary/basement1_lifecycle_differential_report.json` and
`research/notes/post_layout_lifecycle_binary_proof.md`.

## Basement II accepted layout and lifecycle replay

Feature: canonical Stage-2 floor entry through accepted descriptors, second
Basement BossPool commit and successful generation-state handoff to Stage 3

Binary functions / evidence boundaries:

- shared post-topology caller `0x00339370` with Stage-2 predicate inputs;
- current RoomConfig stage call `0x0042D030` at caller `0x003393DF`;
- shared Ultra, late default and successful tail slices already locked above;
- Stage-2 floor-init and inherited BossPool leaves recorded separately.

Confidence: canonical ORIGINAL Basement II NORMAL/HARD accepted layout and
successful lifecycle `CONFIRMED_BINARY`; external gameplay dimension
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Evidence:

- Basement I's lifecycle snapshot is replayed from the game start seed; the
  Stage-2 entry retains persistent state and resets only current stage-1 room
  config weights;
- exact Stage-2 Planetarium chance is float32 bits `0x3E570A3E`; MiniBoss,
  Challenge and Chest use their statically verified Stage-2 predicates;
- Ultra and late selectors receive the current RoomConfig stage, late null is
  the whole-attempt failure edge, and the second boss commits only on success;
- the Stage-2 tail consumes the same 28 persistent draws and advances the
  immutable generation snapshot to LevelStage 3;
- independent clean/reference pipelines match for 10,000 NORMAL plus 10,000
  HARD start seeds: 20,000 accepted results, 20,852 Stage-2 attempts, 826
  retrying seeds and a maximum of three attempts;
- lifecycle equality covers 560,000 persistent draws, 160,000 fixed descriptor
  assignments and 160,000 private-stream transitions with no missing config.

Implementation: `src/isaacmap/basement2_full_pipeline.py`,
`basement2_full_pipeline_reference.py` and `basement2_lifecycle.py`.

Artifacts: `research/binary/basement2_accepted_layout_binary_verification.json`,
`basement2_post_layout_lifecycle_binary_verification.json`,
`basement2_full_differential_report.json` and
`research/notes/floors/basement2.md`.

## Research Preview minimap presentation

Feature: RoomShape icon geometry, official minimap ANM2 indexing and complete
frozen RoomType presentation registry

Static sources:

- `resources/scripts/enums.lua` from the frozen installation;
- `resources/gfx/ui/minimap_icons.anm2` and `minimap_icons.png` read from
  `afterbirthp.a` without loading the game.

Confidence: enum numbers and source frame metadata `CONFIRMED_STATIC_RESOURCE`;
renderer behavior `TESTED_PRESENTATION`. This does not elevate generation or
external gameplay evidence.

Evidence:

- RoomType values 0..30 match the installed enum file;
- the ANM2 parser indexes all animations/layers/frames/sheets and derives crop
  rectangles from frame attributes;
- 22 RoomTypes have verified official icon animations; every remaining known
  special type has an explicit text fallback;
- icon centers are calculated from the exact rendered RoomShape union mask,
  and official visible pixels are aligned by alpha centroid;
- the legend is derived only from special RoomTypes in final accepted
  descriptors.

Implementation: `src/isaacmap/ui/minimap_assets.py`, `icons.py`, `models.py`,
`renderer.py`, `app.py`.

Tests: `tests/unit/test_minimap_assets.py`,
`tests/unit/test_ui_renderer.py`; full local suite 319 passed.

Detailed note: `research/notes/ui_icon_geometry.md` and
`research/notes/ui_icon_sources.md`.

## Complete floor support

FIRST_RELEASE_SCOPE_COMPLETE. The six ORIGINAL-route NORMAL/HARD accepted
13x13 layouts — Basement I, Basement II, Caves I, Caves II, Depths I and
Depths II — are all `CONFIRMED_BINARY`, each backed by an independent
mechanical reference compared over 20,000 seeds with zero mismatch. The
Research Preview dispatches all six through a fail-closed support registry and
plainly labels the external evidence dimension
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Differential artifacts:

- `research/binary/caves1_full_differential_report.json`;
- `research/binary/caves2_full_differential_report.json`;
- `research/binary/depths1_full_differential_report.json`;
- `research/binary/depths2_full_differential_report.json`.

Womb I (Stage 7), later floors, alternate routes and noncanonical profiles
remain `UNSUPPORTED — FAIL CLOSED`.

## Post-layout lifecycle tail: Womb/alternate floor blockers (2026-08-18)

Disassembly source: `scripts/disassemble_range.py` on
`research/input/isaac-ng.exe` (hash-locked), range `0x0073D1D6..0x0073D950`
(tail `0x0033D1D6..0x0033D925` plus epilogue).

Findings (see `research/notes/post_layout_descriptor_minus9.md` and
`post_layout_descriptor_minus10.md`):

- The `-10` descriptor branch (`0x0033D874..0x0033D925`) fires only for
  `stage_type in (4,5) AND level_stage in (7,8)` (Corpse chapter pair). It
  draws 2 persistent Level RNG values and writes GridIndex -10 via the shared
  RoomConfig selector. All eight target floors skip it.
- The `-9` descriptor branch (`0x0033D5E8..0x0033D643`) fires only for
  `room_config_stage == 13` (Blue Womb) and replaces the `-8` slot with the
  same single-draw cost. All eight target floors skip it.
- The door-chance flag writes use a local `IsaacRNG::Next` (raw xorshift at
  `0x3E9020`) seeded from the current Level RNG state; they never advance the
  persistent Level RNG (`0x7e90f0` wrapper). The 28-persistent-draw invariant
  therefore holds for every target floor's tail.
- `stages.xml` is the authoritative chapter/resource-stage table (Womb 10,
  Utero 11, Downpour 27, Mines 29, Mausoleum 31, ...); `boss_pool.py`
  confirms pool index == ORIGINAL room-config stage; `stage_seed.py` confirms
  the alternate seed-slot rule.

The generation pipelines for the eight floors remain unimplemented and
`FAIL CLOSED`; the open items are listed in `STATUS.md` (round 2 section) and
`research/notes/floors/womb1.md` / `womb2.md`.

## Level::get_room_config_stage reconstruction (2026-08-18, round 3)

`research/decomp/ghidra/Level__get_room_config_stage.c` (Ghidra export of the
hash-locked PE) resolves the canonical chapter mapping:

- ORIGINAL: `rcs = 1 + ((stage-1)>>1)*3` -> (7,0)=10, (8,0)=10 (Womb II is
  NOT Utero 11).
- stage_type 4 (alt I floors): `rcs = ((stage-1)&~1) + 27` -> 27/29/31.
- stage_type 5 (alt II floors): `rcs = ((stage-1)>>1)*2 + 28` -> 28/30/32.
- (7/8, 4/5) -> 33 (Corpse) cross-checks the -10 descriptor domain.

Full table in `research/notes/get_room_config_stage_stage7_8_alt.md`.

## Womb floor-init confirmation (2026-08-18, round 3 cont.)

`Level__generate_dungeon.c` (decompiled) confirms the floor-init formulas for
the canonical ORIGINAL route:

- `target = min(stage*10/3 + 5 + (rng&1), 20)`; stage 7/8 -> 20; HARD adds
  `2 + (rng&1)` (22/23).
- XL (Labyrinth): `target = max(4, target*3/5)` -> Womb I XL 12 (N) / 13 (H).
- required dead ends = `(stage != 1) + 5` = 6 for stages 2..8.
- Alternate floors (stage_type 4/5, alt-half predicate) subtract 3 from the
  target (`target - 3`) — the alt floor-init differs from ORIGINAL, so it
  cannot be extrapolated; this is now documented as a confirmed difference.

## Womb through-Treasure + BossPool 10 (2026-08-18, round 4)

- Boss path is stage-parameterized: `Level__select_boss_id(level_stage,
  stage_type, pool)` with pool derived from rcs (10 for Womb); XL second boss
  uses `select_boss_id(level_stage + 1, stage_type)` (pool 10 for stage 7
  XL since rcs(8,0)=10) with the persistent Level RNG saved and restored
  (rewound) after the XL boss.
- Labyrinth/XL gate = curse bit 0x02 (`(~remove & (add|curse|used) & 2) == 0`),
  matching the repo curse encoding.
- Pool index == XML pool position + 1 (basement 1, caves 4, depths 7,
  womb 10). Womb pool: Scolex(7), Mama Gurdy(49), Lokii(31), Mr. Fred(53),
  Blastocyst(16) w=1, The Matriarch(72) w=0.25; Womb I/II share pool 10 with
  RNG/removal inheritance via the existing 37-state snapshot.
- Type8/Shop/Treasure (`0x00339A87..0x0033A3FF`) and the post-Treasure
  region (`0x0033A410..0x0033A940`) re-read line-by-line for stage 7/8: the
  only stage gate in the section is `cmp [esi], 0xa` (level_stage==10); no
  stage-7/8-specific gate exists, so the ordinary Boss/Type8/Shop/Treasure
  blocks execute unconditionally on canonical Womb (CONFIRMED_BINARY).
- Planetarium (`0x0033A8F7..0x0033AB45`): gate
  `stage<7 || (stage<9 && collectible 0x6e) || stage==10`; canonical Womb
  (no collectible) skips select/geometry/chance but consumes the
  unconditional 0x0033A961 selector-seed Level draw (CONFIRMED_BINARY).
- **Reference bug fixed**: the Womb reference originally resumed pool 10
  with the Depths pool-7 state (`d2.final_boss`); per-pool BossPool RNGs are
  independent, so pool 10 starts from its own game-start seed at Womb. Both
  floors now pass 100/100 clean-vs-reference differentials (0 mismatches).

## Womb I/II implementation complete (2026-08-18, round 4 cont.)

- Womb I: `derive_womb1_topology_inputs` (stage 7, XL-capable, target 20 /
  XL 36, dead ends 7/6), `CanonicalWomb1Profile` (rcs 10, stage_type 0),
  `womb1_full_pipeline(_reference).py`, `womb1_lifecycle.py`
  (next_level_stage=8). 100 ordered differentials (50 N + 50 H), 0
  mismatches: `research/binary/womb1_100_differential_report.json`.
  Targeted XL fixture seeds 106/244/1381 (NORMAL, curse mask 2, target 36,
  dead ends 7; seed 106 accepted 37 rooms + additional boss (7, pool 10) at
  room 37).
- Womb II: `derive_womb2_topology_inputs` (stage 8, never XL, target 20,
  dead ends 6, window (5,10)/(10,15)), `CanonicalWomb2Profile`,
  `womb2_full_pipeline(_reference).py`, `womb2_lifecycle.py`
  (next_level_stage=9 = Sheol, not implemented). 100 ordered differentials
  (50 N + 50 H), 0 mismatches:
  `research/binary/womb2_100_differential_report.json`.
- Registry: `SUPPORTED_FLOORS` gains Womb I/Womb II; preview resources load
  `10.womb.stb` + `pools["womb"]`; `bot_api` stage 7/8 open with
  `algorithm_evidence` (CONFIRMED_BINARY vs PARTIAL_BINARY derived from
  `generation_status`, persisted for cache hits); fraq bot caption prints
  the real evidence grade.
- Full generator suite: `494 passed` (462 baseline + 32 Womb tests). fraq
  bot: 94 passed, typecheck/build green.
- Bot smoke (real CLI path): `/map B911 99AC 0 7` -> Womb I NORMAL PNG,
  `/map B911 99AC 1 8` -> Womb II HARD PNG; both PARTIAL_BINARY.
- Discipline: Womb I/II are `PARTIAL_BINARY` on the 100-sample corpus, never
  `CONFIRMED_BINARY`. ALT route and Sheol+ remain FAIL CLOSED.

## Round 5 (2026-08-18): ALT route reconstruction + fixed-boss correction

- **`Level::select_boss_id` fixed-boss switch (0x422830)** — CONFIRMED. The
  function switches on level_stage 6..12 before any pool selection:
  ORIGINAL (stage_type not 4/5): level 6 -> Mom (6), level 8 -> Mom's Heart
  (8) or It Lives! (25) under a flag condition, level 10 -> Satan (24)/
  Isaac (39), level 11 -> The Lamb (54)/???, level 12 -> Delirium (70);
  ALT (stage_type 4/5): level 6 -> Mom-Mausoleum (89), level 8 -> Mother
  (88), level 10/11 -> ??? (40), level 12 -> Delirium (70). Boss-room ids
  verified against the bossportraits table and the room sets (89 in
  `31.mausoleum.stb`, 88 in `33.corpse.stb`, all ids in
  `00.special rooms.stb`). Implemented as `select_floor_boss` in both
  leaves; Depths II / Womb II / XL-second-boss pool picks corrected.
- **ALT StageType sequence 4,5,4,5,4,5** — CONFIRMED (forced by
  `get_room_config_stage` + `stages.xml`); slot = stage+1 gated on stage_type
  (Level::Init 0x744940); stage/type setter 0x7466d0; pre-Init alt fixup
  0x7467c0 with per-stage chapter table `Game+0x6746c + stage*0x320`.
- **ALT BossPool index == rcs (27..32)** — CONFIRMED hardcoded name->index
  table in the bosspools.xml parser (0x421bf0): downpour 27, mines 29,
  mausoleum 31, corpse 33, dross 28, ashpit 30, gehenna 32. The earlier
  "XML position + 1" guess for alt pools (19..24) was wrong.
- **ALT floor-init** — CONFIRMED from `generate_dungeon` (0x740e10):
  target = min(stage*10/3+5+bit, 20); -3 via first/second-half predicates
  (stages 1-4, odd stages XL-gated); XL = min(target*1.8, 45); dead_ends =
  (stage!=1)+5 (+1 alt 1-4); difficulty windows by stage parity; Labyrinth
  only on odd stages < 8 (`can_apply_labyrinth` 0x7385c0).
- **ALT M5 (through-Treasure) stage_type-independent**; M6 specials use
  adjusted-stage (stage+1) gates at sites 0x73b3ea/0x73b497/0x73ba3b/
  0x73bcff/0x73bd31/0x73bfe7; alternate-path blocks 0x0033C416..0x0033C69E
  (first-half mandatory end room for Dross / Downpour-XL; second-half needs
  collectible 626; third branch ORIGINAL-only flag) — CONFIRMED;
  Secret/Ultra shared; late branches 0x73e422 (ORIGINAL-only
  achievement-187 gate) and 0x73ea83 (Mines/Ashpit chapter) — OPEN.

## Round 5 (2026-08-18, complete): ALT floors 1+..6+ OPEN

- **All six ALT floors implemented and registered** (Downpour I, Dross,
  Mines I, Ashpit, Mausoleum I, Gehenna). Each floor: 50 NORMAL + 50 HARD
  ordered clean-vs-reference comparisons, 0 mismatches (artifacts
  `research/binary/alt{downpour1,dross,mines1,ashpit,mausoleum1,gehenna}_
  100_differential_report.json`; the downpour/dross pairs keep their
  round-5 file names `alt1_/alt2_`). Evidence grade per floor:
  `PARTIAL_BINARY` (intentionally capped — 100 samples, not 20k-class).
- **12 targeted XL fixtures all match** (seeds 143/158/229/236/344/520/787/
  925/987 across N+H): Downpour I XL exercises the first-half mandatory end
  room; Mines I XL exercises the second-half predicate with the
  collectible-626 gate keeping it a no-op; Mausoleum I XL exercises
  XL target/dead-end arithmetic on a level outside both half sets.
- **Gehenna fixed boss verified in the clean pipeline**: `select_floor_boss`
  returns 89 (Mom-Mausoleum) with pool-32 RNG pre == post state across
  seeds 1/2/7 (differential also covers 100 seeds).
- **Alternate-path mandatory end room** implemented in both M6 leaves:
  first-half fires on Dross always and Downpour I on XL; second-half is a
  canonical no-op (needs collectible 626); stages 5/6 evaluate the branch
  and skip (config None) — block traces asserted per floor in
  `tests/differential/test_{floor}_full_pipeline_differential.py`.
- **Registry/bot**: `SUPPORTED_FLOORS` opens `1+..6+`; `/map B911 99AC
  {0,1} {1+..6+}` produce real 1400x900 PNGs (`B91199AC_ALT_{NORMAL|HARD}_
  stage{N}_{ver}.png`, PARTIAL_BINARY in the JSON payload); MAIN `stage1`
  vs ALT `stage1` cache filenames stay separated by route.
- **UI**: ALT floor dropdown entries (Downpour I, Dross, Mines I, Ashpit,
  Mausoleum I, Gehenna) tagged SUPPORTED; `supported_stage_summary()` is
  route-aware: "stage 1-8（Baseline I 到 Womb II）；stage 1+-6+（Downpour I
  到 Gehenna）".
- Generator tests: 617 passed (545 baseline + 72 ALT). MAIN 1..8 unchanged
  this round.
- Remaining boundary: Corpse (rcs 33, `-10` descriptor domain, level 8
  fixed Mother 88) and the Sheol/Cathedral/Chest/Dark Room/Void endings
  remain FAIL CLOSED.

## 2026-08-21 StageType5 / natural XL debug audit

The user-visible ALT 2+/4+ failures were not generation-algorithm failures.
On the incoming worktree, the factual bot names were `Dross` and `Ashpit`, but
the single support registry still used `Downpour II` and `Mines II`. Gehenna
had the same `Gehenna` versus `Mausoleum II` mismatch, so 6+ also failed. All
three requests returned `UNSUPPORTED_FLOOR` in
`bot_api.generate_map_image_for_bot` before `generate_preview` dispatched a
pipeline. The registry keys/spec labels were synchronized; the fail-closed
guard remains intact.

Exact-offset static recheck against SHA-256
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`:

- StageType5 compare: VA `0x0082D0BE`, RVA `0x0042D0BE`, file
  `0x0042C4BE`, bytes `83 fa 05` (`cmp edx,5`);
- branch target/formula: VA `0x0082D0C3`, RVA `0x0042D0C3`, file
  `0x0042C4C3`, bytes `8d 04 4d 1c 00 00 00`
  (`28 + 2*((stage-1)>>1)` -> 28/30/32);
- Labyrinth eligibility entry: VA `0x007385C0`, RVA `0x003385C0`, file
  `0x003379C0`; odd-stage compare at VA `0x007385DF`, stage<8 at
  `0x007385E4`, game-mode 2/3 rejects at `0x007385EF/0x007385F4`;
- curse rate starts at VA `0x00744CF3` (`80`), HARD selects `40` at
  `0x00744DB5`; gate call is VA `0x00744F03`; selector `%6` dispatch is VA
  `0x00744F6C`; Labyrinth sets bit 2 at VA `0x00744F84`.

`DKM8 9MNM` HARD 1+ clean/reference trace: uint32 `364417104`, slot 2,
stage seed `362265690`, StageType 4, rcs 27, curse RNG copied state
`2722452983`, gate draw `163224774`, rate 40, remainder 14, selector not
consumed, mask 0, `can_apply_labyrinth=true`, effective `is_xl=false`, target
10, required dead ends 5. Counterfactual next draw `3869886000 % 6 == 0`
matters only to a progressed rate-6/rate-3 profile.

The four exact denominator pairs are exposed as reproducible generation
profiles rather than inferred achievement names: `BASE_80_40`, `RATE_30_20`,
`RATE_10_6`, and `RATE_5_3`. User-reported HARD 1+ controls identify
`RATE_5_3` for the target Bot environment: `BJPK 79MF` is XL (rate-3-only),
`BJPK 72ME` is XL (rate-6/rate-3 positive control), and `BJPK 79FB` is non-XL
(negative control). Clean and mechanical-reference traces agree for every
profile/seed pair. This is profile selection evidence, not an independently
operated gameplay oracle, so the external-validation grade remains unchanged.

Validation: ALT 1+..6+ each reran 50 NORMAL + 50 HARD full clean/reference
comparisons (600 total, zero mismatch); targeted automatic XL pipelines for
Downpour I, Mines I and Mausoleum I matched. The same 600 ALT comparisons also
match under `RATE_5_3`; complete suite `641 passed`.
External gameplay remains `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## 2026-08-22 DKM XL topology propagation audit

The accepted-layout I-floor wrappers on both the clean and mechanical-
reference sides constructed a LevelGenerator without copying the already
derived `profile.is_xl` state.  Target/dead-end arithmetic was XL, but the
generator's binary XL candidate-link branch remained disabled.  The shared
integration omission explains why the previous full-pipeline differential
could agree while producing a non-XL topology.  Clean and reference wrappers
now set `generator.is_xl = profile.is_xl`; the cache version was bumped.

`DKM8 9MNM` HARD 1+ under `RATE_5_3` now reaches the full pipeline with stage
seed `362265690`, generator seed `3869886000`, curse mask `0x02`, XL target
12, seven required dead ends, and shape mask `0x1FFE`.  The resulting floor
has the XL room-count semantics (two Boss and two Treasure rooms).

The supplied gameplay capture still has a different topology: exactly four
multi-cell footprints versus two in the corrected offline topology.  A
footprint matcher allowing translation and all eight dihedral transforms found
no match for (a) target 4..30/dead ends 5..12/XL on-off at the current seed,
(b) 5000 legal stage-slot mutations that retain the Labyrinth roll, or (c) a
binary-reachable matrix spanning all 14 stage slots, 64 Level-RNG phases,
targets 7..20, dead ends 5..9, and normal/Giant masks.  `0x802980` is a
post-generation current-room/entity update; `0x74F0C0` reassigns configs but
retains geometry; `0x74F360` is not reached by ordinary Downpour I XL.

No screenshot-specific topology change is justified.  The formal fix is the
binary-supported XL state propagation only; the remaining captured-layout
mismatch stays open until a new binary-confirmed state input or environmental
cause is identified.  No seed special case was added.

Final regression: generator `642 passed`; `RATE_5_3` ALT 1+..6+ ran 50 NORMAL
and 50 HARD clean/reference comparisons per floor (600 total, zero mismatch);
fraq Bot `95 passed`, typecheck/build green, and real subprocess PNG smoke
passed for DKM XL plus Dross/Ashpit NORMAL/HARD. `NO_ISAAC_PROCESS`.
