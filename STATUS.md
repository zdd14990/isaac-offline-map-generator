# Exact Isaac Offline Generator Status

Game executable: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Steam build ID: `22878971`

Safety: `isaac-ng.exe` has never been executed. Binary work is static and uses
the hash-identical copy under `research/input/`. Isolated Unicorn checks copy
individual function bytes into emulator-owned memory; they do not invoke the
PE loader, entry point, imports, game process or game loop.

Two evidence dimensions remain independent:

- algorithm reconstruction from this exact binary;
- current-version external gameplay fixture parity.

`CONFIRMED_BINARY` does not imply `EXTERNALLY_VALIDATED_GAMEPLAY`, and
reference/clean equality alone is not sufficient for `CONFIRMED_BINARY`.

## Confirmed

Seed encoding: `CONFIRMED_BINARY` for ordinary nonzero run seeds, including
alphabet, XOR, checksum, canonical format and invalid-seed rejection.

RNG: `CONFIRMED_BINARY` for all 81 shift triples, `SetSeed`, `Next`,
`RandomInt`, and the current x86 binary32 `RandomFloat` path.

Resources: `CONFIRMED_OPEN_SOURCE` plus local checksum/EOF validation. All 61
merged STBs parse to exact EOF: 30,845 rooms.

Stage seed: `CONFIRMED_BINARY` for fresh-run derivation and initial-floor slot
selection. Later mutation/continue state is separate.

Basement I topology: `CONFIRMED_BINARY` for the frozen contract in
`research/notes/topology_inputs.md`:

- `STAGE1_1`, `STAGETYPE_ORIGINAL`, ordinary vanilla generator;
- NORMAL or HARD, challenge 0, not daily/custom/ascent;
- effective curse 0, hence not XL/Lost/Giant;
- no player owns collectible 599 (Voodoo Head);
- fresh unmutated stage seed, no topology blocks, unmodified profiled rooms;
- start anchor `(6,6)`, GridIndex 84, Shape 1.

Within that contract Milestone 4 geometry, Shapes 1..12, occupied cells,
connections, expansion order, large-room behavior, dead-end classification and
ordering, forced correction, retry logic, every topology RNG draw and final
generator RNG state are all `CONFIRMED_BINARY`.

Post-topology call order: `CONFIRMED_BINARY`. The ordinary Basement sequence
begins:

```text
Boss identity
→ Boss RoomConfig
→ Boss geometry/assignment
→ RoomType 8 (Super Secret end-room pass)
→ saved post-Type8 seed snapshot
→ Shop
→ Treasure
→ later conditional special-room family
→ Secret
→ Ultra Secret
→ ordinary ROOM_DEFAULT RoomConfig/Variant assignment
```

The full branch graph and call RVAs are in
`research/notes/post_topology_callgraph.md`.

BossPool initialization: `CONFIRMED_BINARY`:

- call RVA `0x002F8579` passes `Game+0x1BB88`
  (`Seeds._gameStartSeed`) to BossPools at `Game+0x1AF70`;
- 37 fixed slots receive a chained index-26 `(3,13,7)` seed stream;
- each persistent pool RNG uses index 17 `(2,21,9)`;
- each pool's entries are shuffled once at initialization using a separately
  seeded MT19937 Fisher-Yates pass; this does not advance the pool xorshift;
- the ordinary selector advances the persistent selected pool seven times and
  performs weighted selection on a non-persisted local copy.

Generation retry transaction: `CONFIRMED_BINARY` for the canonical Basement I
path. The outer loop retains Level RNG, LevelGenerator RNG, the seven
persistent BossPool pre-rolls, RoomConfig weight decay, target count and retry
counter. It discards topology/descriptors/dead-end temporaries and clears the
per-attempt boss blacklist. Only a successful attempt commits that blacklist
to permanent boss removal.

RoomConfig special selector: `CONFIRMED_BINARY` for Boss, RoomType 8, Shop and
Treasure. Ordered filters, exact-door subset, index-7 draws, x86 binary32
weighted scan, minimum weight and `0.1f` decay are implemented. Weights reset
once in `Level::Init`, outside the retry loop, so failed-attempt decay is
retained.

Boss pipeline: `CONFIRMED_BINARY` for the canonical fresh ordinary Basement I
profile. Boss identity, Boss RoomConfig, geometry and descriptor assignment
are distinct operations. The implementation preserves pool RNG persistence,
per-attempt blacklist/commit behavior, config rejection draws, ordered
distance>1 candidates, reshape/re-anchor, stable erase and whole-attempt
failure.

RoomType 8 / Super Secret pipeline: `CONFIRMED_BINARY` within the same
profile. One Level draw seeds a distinct index-9 stream; concrete type-8
RoomConfig is selected before geometry; `GetNewEndRoom` reshapes and mutates
an existing dead end and stable-erases it. It does not append a room. Its
failure and weight/RNG retry effects are integrated.

Shop pipeline: `CONFIRMED_BINARY` within the same profile. It runs after the
post-Type8 seed snapshot, uses a separate index-19 subtype stream, resolves
canonical subtype 11, selects the concrete stage-0 config, and mutates/stable-
erases the next compatible end room. NORMAL/HARD has no direct Shop branch;
differences arrive through upstream topology/RNG state.

Treasure pipeline: `CONFIRMED_BINARY` within the same profile. It runs after
Shop candidate mutation, preserves the rare/ordinary subtype draw split,
uses stage-1 then stage-0 fallback with the same selector seed, and returns
the same outer retry signal on geometry failure.

RoomConfig timing: `CONFIRMED_BINARY`. Special rooms choose concrete STB
entries before their geometry placement; ordinary default-room concrete
selection occurs only after Secret and Ultra. Variant RNG consumption cannot
be globally deferred.

Reference/clean differential status through Treasure: passed for 10,000
NORMAL and 10,000 HARD start seeds, including every outer retry, binary
condition trace, candidate/config/geometry mutation and restored RNG state.

Treasure-to-Secret call chain: `CONFIRMED_BINARY` under the same profile.
The actual blocks are Planetarium, Dice/Sacrifice, Library, Curse, MiniBoss,
Challenge, Chest/Arcade, Isaac/Barren, three route-dependent blocks, then
Secret. Canonical Stage 1 executes every named ordinary block, skips the three
route blocks, and retains all skip predicates in the reference trace.

Secret Room: `CONFIRMED_BINARY` under the frozen profile. Concrete type-7
RoomConfig selection precedes geometry. The helper scans empty GridIndex
0..168, consumes persistent index-35 `LevelGenerator._rng` once per eligible
candidate and preserves stable scan/tie order. It appends a new 1x1 descriptor
and refreshes graph connections; it is not an existing-dead-end mutation. A
null candidate is allowed and does not retry the floor.

Ultra Secret: `CONFIRMED_BINARY` for canonical Basement I NORMAL/HARD. It
follows Secret and a canonical-skipped Stage-11 block, selects a concrete
type-29 config from one index-71 advance of the saved post-Type8 snapshot, and
performs geometry with the continuing persistent LevelGenerator index-35 RNG.
It scans the ordinary 13x13 map, appends a 1x1 descriptor, updates the normal
map and writes red-door bits across empty intermediary cells. A null candidate
is allowed and does not retry. Full proof is in
`research/notes/ultra_secret_binary_proof.md`.

Late ordinary RoomConfig pass: `CONFIRMED_BINARY`. After Ultra, the binary
collects topology non-dead ends followed by remaining dead ends. Start receives
fixed variant 2; every other ordinary descriptor selects a compatible stage-1
ROOM_DEFAULT using final shape/doors, the confirmed NORMAL/HARD difficulty
window, persistent Level RNG and mutable RoomConfig weights. A missing config
returns false and retries the whole floor while persistent state stays
advanced.

Basement I accepted 13x13 layout: `CONFIRMED_BINARY` for canonical fresh
NORMAL/HARD. The full clean pipeline does not commit the BossPool attempt
blacklist until Ultra and late ordinary assignment succeed. Its final room
map/descriptors therefore represent only the accepted attempt, including
Secret, Ultra and all ordinary concrete configs.

Basement I successful post-layout lifecycle tail: `CONFIRMED_BINARY` for the
same canonical profile. After layout acceptance it creates eight fixed
negative-GridIndex descriptors, consumes exactly 28 persistent Level RNG
draws, runs the Shop/Angel private streams, mutates RoomConfig weights and
clears the one-shot special bits read by this branch. It cannot reject or
alter the accepted 13x13 map. The generation-only handoff records all 37
BossPool states and the committed Basement removal state for later replay.

Basement II accepted 13x13 layout and successful lifecycle handoff:
`CONFIRMED_BINARY` for canonical ORIGINAL NORMAL/HARD. Generation starts from
the accepted Basement-I lifecycle snapshot, applies the Stage-2 curse/count
profile, resets only the current stage-1 RoomConfig entries, resumes the
Basement BossPool and carries all persistent RNG/weight/used-bit state. The
final result exposes only the accepted Stage-2 descriptors and commits the
second boss only after Ultra and late ordinary assignment succeed. The shared
successful tail advances the generation snapshot to LevelStage 3.

External gameplay status for all of the above remains independently
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Partial / not yet complete

Womb I (LevelStage 7) and Womb II (LevelStage 8) are implemented with
`PARTIAL_BINARY` evidence (100 ordered clean-vs-reference comparisons each).
All alternate-route floors (Downpour/Dross/Mines/Ashpit/Mausoleum/Gehenna)
remain unsupported and fail closed: their StageType lifecycle, floor-init
matrix and BossPool mapping are binary-confirmed, but the special-room gate
shapes (Challenge/Chest/Arcade/super-secret adjusted-stage gates and the
alternate-path mandatory end room) are still being reconstructed — see
`research/notes/alt_special_room_condition_matrix.md`. Stage-7/8 constants
and RoomConfig/BossPool profiles were reconstructed from the binary; nothing
was copied from earlier floors.

### Womb I/II and alternate-route floors: status (2026-08-18, round 5)

**Womb I/II generation is OPEN on the MAIN route** (bot tokens `7`/`8`).
Evidence grade `PARTIAL_BINARY` per floor: 50 NORMAL + 50 HARD ordered
clean-vs-reference comparisons with 0 mismatches
(`research/binary/womb1_100_differential_report.json`,
`womb2_100_differential_report.json`), plus a targeted Womb I XL fixture
(seeds 106/244/1381). **Round 5 correction:** `select_boss_id` returns FIXED
bosses for levels 6/8/10/11/12 — Depths II = Mom (6), Womb II = Mom's Heart
(8), ALT Gehenna = Mom-Mausoleum (89), ALT Corpse II = Mother (88) — so the
earlier pool picks for Depths II / Womb II (and XL second bosses at level
6/8) were corrected in both leaves. ALT 1+..6+ remain FAIL CLOSED until the
special-room gate shapes are reconstructed.

New binary findings this round (post-layout lifecycle tail
`0x0033D1D6..0x0033D925`, disassembled with `scripts/disassemble_range.py`):

- **`-10` descriptor** (`post_layout_descriptor_minus10.md`): predicate is
  `stage_type in (4, 5) AND level_stage in (7, 8)` — i.e. the Corpse (Mother
  route) chapter pair, which is **out of scope**. Every target floor skips
  it: Womb (stage_type 0) and Downpour/Mines/Mausoleum (level_stage 1..6).
  It consumes 2 extra Level RNG draws only when entered.
- **`-9` descriptor** (`post_layout_descriptor_minus9.md`): predicate is
  `room_config_stage == 13` (Blue Womb). It replaces the `-8` slot with the
  same 1-draw cost. Never fires for the eight target floors (rcs 10 / 27..32).
- **28-draw invariant holds for all eight target floors.** The door-chance
  flag writes in the tail use a local `IsaacRNG::Next` copy seeded from the
  current Level RNG state (`0x3E9020` disassembly) and do NOT advance the
  persistent Level RNG; the `-9`/`-10` branches are skipped; therefore the
  persistent Level RNG sequence is identical to Depths II for every target
  floor. The tail guard can be relaxed on this binary evidence, but that is
  deferred until the pipelines that would call it exist.
- Chapter resources are authoritative in `stages.xml` (Womb 10, Utero 11,
  Downpour 27, Dross 28, Mines 29, Ashpit 30, Mausoleum 31, Gehenna 32);
  `boss_pool.py` confirms pool index == ORIGINAL room-config stage.
  `stage_seed.py` already confirms the alt route seed-slot rule
  (`level_stage + 1`, capped at Home).
- **`get_room_config_stage` fully reconstructed**
  (`research/decomp/ghidra/Level__get_room_config_stage.c`, note
  `get_room_config_stage_stage7_8_alt.md`): ORIGINAL `(7,0)->10` and
  `(8,0)->10` (Utero 11 is NOT the canonical Womb II rcs); alt I floors
  `(1..6, stage_type 4) -> 27/29/31`; alt II floors `(1..6, stage_type 5)
  -> 28/30/32` (Dross/Ashpit/Gehenna are stage_type 5, the "second chapter"
  variant); `(7/8, 4/5) -> 33` Corpse (the `-10` domain); Greed-mode special
  mapping documented.

Remaining open work for alternate/later floors (Womb itself is DONE; see
`research/notes/floors/womb1.md`, `womb2.md`,
`research/notes/stage_type_4_5_binary_proof.md`):

1. alt floor-init parameters for stage_type 4/5 (target-3 confirmed;
   everything else must not be extrapolated from ORIGINAL);
2. through-Treasure / Secret / Ultra / late RoomConfig stage gates for
   stage_type 4/5;
3. route-progression stage_type assignment (I floors = 4, II floors = 5)
   in the level-transition code;
4. alternate-route RunGenerationState fields and BossPool entries for the
   alt chapters (pools 27..32).

Validation target when implemented: 50 NORMAL + 50 HARD per floor (~100
comparisons per floor), graded at most `PARTIAL_BINARY` /
`PREVIEW_SUPPORTED` — never `CONFIRMED_BINARY` on 100 samples.


Noncanonical character, collectible, challenge/game-mode, unlock and continue
profiles are rejected rather than silently taking the canonical branch.

## New output-affecting state found in M5/M6

M4's standalone topology input contract is sufficient for the scoped
`LevelGenerator::Generate` result, but not for acceptance of the final floor.
Post-topology adds:

- `_gameStartSeed`, independently of the stage seed;
- 37 persistent BossPool RNG objects, shuffled entry order and manager
  removed/per-level bitsets;
- mutable RoomConfig weights and their previous-floor/previous-attempt state;
- outer generation-loop count and continuing Level/LevelGenerator RNG state;
- achievements/unlocks, character, challenge/game mode and previous boss
  lifecycle;
- players and collectibles, including ids 589 and 599;
- room-type visitation/state, shop visits and related counters;
- health/max-hearts/coins and Planetarium/unlock gates;
- persistent special-room used bits at `Game+0x26548`, including immediate
  MiniBoss subtype writes which survive a later attempt failure;
- effective curses/XL, stage type/route and route predicates;
- vanilla resource overlays/mod state (exact mode remains vanilla-only).

## Current exactness

Basement I NORMAL topology-only under the frozen state:
`CONFIRMED_BINARY`.

Basement I HARD topology-only under the frozen state:
`CONFIRMED_BINARY`.

Basement I NORMAL/HARD, canonical profile, Topology through Secret:
`CONFIRMED_BINARY`.

Basement I NORMAL/HARD, canonical profile, through Ultra Secret:
`CONFIRMED_BINARY`.

Basement I NORMAL/HARD canonical accepted 13x13 layout parity, including late
ordinary RoomConfig assignment: `CONFIRMED_BINARY`.

Basement I NORMAL/HARD canonical successful lifecycle/handoff tail:
`CONFIRMED_BINARY`.

Basement II NORMAL/HARD canonical accepted 13x13 layout and successful
lifecycle/handoff tail: `CONFIRMED_BINARY`.

Caves I (LevelStage 3) NORMAL/HARD canonical accepted 13x13 layout and
successful lifecycle/handoff tail: `CONFIRMED_BINARY`. The floor-init and
topology leaf are `CONFIRMED_BINARY` (10k NORMAL + 10k HARD differential),
the Caves BossPool (index 4, `bosspools.xml["caves"]`) resume/select leaf is
`CONFIRMED_BINARY`, and the full layout plus post-layout lifecycle is
`CONFIRMED_BINARY` via an independent mechanical reference compared over
20,000 seeds with zero mismatch. The shared post-layout tail (RVA
`0x0033D1D6..0x0033D94B`) advances the snapshot to LevelStage 4 (Caves II).
Caves II (LevelStage 4) NORMAL/HARD canonical accepted 13x13 layout and
successful lifecycle/handoff tail: `CONFIRMED_BINARY`. It shares the Caves
RoomConfig stage (4) and the Caves BossPool (index 4) with Caves I; the pool
RNG state is inherited (advanced) from the Caves-I snapshot. The full layout
and post-layout lifecycle are confirmed via an independent mechanical
Depths I (LevelStage 5) NORMAL/HARD canonical accepted 13x13 layout and
successful lifecycle/handoff tail: `CONFIRMED_BINARY`. It uses the Depths
RoomConfig stage (7) and the Depths BossPool (index 7, `bosspools.xml["depths"]`),
which starts from its run-start state (no earlier floor selects it). The
full layout, XL dual Boss/Treasure, and post-layout lifecycle are confirmed
via an independent mechanical reference compared over 20,000 seeds with zero
Depths II (LevelStage 6) NORMAL/HARD canonical accepted 13x13 layout and
successful lifecycle/handoff tail: `CONFIRMED_BINARY`. It shares the Depths
RoomConfig stage (7) and the Depths BossPool (index 7) with Depths I; the
pool-7 RNG state is inherited (advanced) from the Depths-I snapshot. Even
Stage 6 is never XL. The full layout and post-layout lifecycle are confirmed
via an independent mechanical reference compared over 20,000 seeds with zero
mismatch. Womb I and later alternate routes: `UNSUPPORTED — FAIL CLOSED`.

FIRST_RELEASE_SCOPE_COMPLETE: the six ORIGINAL-route floors Basement I,
Basement II, Caves I, Caves II, Depths I and Depths II are all
`CONFIRMED_BINARY`. External gameplay validation remains
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Research Preview UI: canonical Basement I, Basement II, Caves I, Caves II,
Depths I and Depths II NORMAL/HARD. It dispatches through a
`SUPPORTED_FLOORS` registry, replays the preceding floors' generation-only
lifecycle when a later Stage is requested, and renders the selected clean
pipeline's accepted descriptors/map/connections after all special-room
geometry succeeds. Failed-attempt descriptors are never combined with the
accepted map. Womb I and later floors remain fail closed in the UI.

UI P0/P1 integration: completed. Icons are positioned at the centroid of the
actual rendered RoomShape union mask and official sprites are aligned by their
visible alpha centroid, fixing large/L-room and transparent-frame offsets.
RoomShape 1..12 are covered by geometry tests. The frozen `RoomType` enum is
represented for values 0..30; every known special type has an official
minimap animation or an explicit text fallback. All M6-assignable special
types have official icons. Legend entries are derived from the final accepted
descriptor collection instead of a hard-coded list. This is presentation-only
and changes no generation algorithm or evidence boundary.

The product-facing UI remains explicitly a Research Preview because external
gameplay validation is unavailable. No later floor or noncanonical profile is
silently approximated.

## Tests

Current local result: `494 passed` (462 baseline + 32 new Womb tests:
`tests/unit/test_womb_floor_init.py` and
`tests/differential/test_womb_full_pipeline_differential.py`).

Caves I full-layout/lifecycle differential: 10,000 NORMAL and 10,000 HARD
start seeds (20,000 comparisons) against an independent mechanical reference,
with zero mismatch. The corpus covers 20,660 attempts, 632 retrying seeds, a
maximum of seven attempts, 76 natural XL floors, 720,000 post-layout RNG
transitions, 160,000 RoomConfig selections and 20,076 boss selections.
Artifact: `research/binary/caves1_full_differential_report.json`.

Caves II full-layout/lifecycle differential: 10,000 NORMAL and 10,000 HARD
start seeds (20,000 comparisons) against an independent mechanical reference,
with zero mismatch. The corpus covers 20,413 attempts, 406 retrying seeds, a
maximum of three attempts, 720,000 post-layout RNG transitions, 160,000
RoomConfig selections and 20,000 boss selections. Caves II is never XL.
Artifact: `research/binary/caves2_full_differential_report.json`.

Depths I full-layout/lifecycle differential: 10,000 NORMAL and 10,000 HARD
start seeds (20,000 comparisons) against an independent mechanical reference,
with zero mismatch. The corpus covers 20,413 attempts, 389 retrying seeds, a
maximum of eight attempts, 47 natural XL floors, 720,000 post-layout RNG
transitions, 160,000 RoomConfig selections and 20,047 boss selections.
Artifact: `research/binary/depths1_full_differential_report.json`.

Depths II full-layout/lifecycle differential: 10,000 NORMAL and 10,000 HARD
start seeds (20,000 comparisons) against an independent mechanical reference,
with zero mismatch. The corpus covers 20,372 attempts, 363 retrying seeds, a
maximum of four attempts, 720,000 post-layout RNG transitions, 160,000
RoomConfig selections and 20,000 boss selections. Depths II is never XL.
Artifact: `research/binary/depths2_full_differential_report.json`.

Womb I full-layout/lifecycle differential: 50 NORMAL and 50 HARD start seeds
(100 comparisons) against an independent mechanical reference, with zero
mismatch, plus a targeted XL fixture (seeds 106/244/1381, NORMAL; curse mask
2, target 36, dead ends 7, additional boss verified). Evidence grade
`PARTIAL_BINARY` — 100 samples, not 20k-class.
Artifact: `research/binary/womb1_100_differential_report.json`.

Womb II full-layout/lifecycle differential: 50 NORMAL and 50 HARD start seeds
(100 comparisons) against an independent mechanical reference, with zero
mismatch. Womb II is never XL. Evidence grade `PARTIAL_BINARY`.
Artifact: `research/binary/womb2_100_differential_report.json`.

Topology mass differential: 20,000 NORMAL/HARD cases and 7,285,534 generator
RNG transitions, covering all Shapes 1..12, all L shapes, large-room
success/failure, forced dead ends, boundaries and a targeted retry fixture.

Assembled through-Treasure differential: 20,000 NORMAL/HARD start seeds. The
last completed corpus contains 1,433 retrying seeds and 21,526 total attempts,
with maximum four attempts. It exercises two NORMAL and one HARD Boss-geometry
failures plus 1,523 Treasure-geometry failures. Comparison includes target
count, complete topology state, BossPool state/bitsets, RoomConfig ordered
candidates/weights, all end-room candidates and geometry events, descriptor
mutations, condition traces, every recovered post-topology RNG transition and
all final persistent states. The corpus compares 400,499 post-topology RNG
transitions, 114,244 RoomConfig selector calls, 90,493 candidate tests and
107,615 condition traces; topology and geometry candidate Shapes 1..12 are
all reached.

Assembled through-Secret differential: an independent mechanical reference
and clean implementation compare the full M4/M5 attempts, every post-Treasure
block/re-append, every Secret candidate/score/neighbor mask, RoomConfig and
RNG transition, descriptor/map/connection mutation, final persistent state
and pending BossPool attempt blacklist. The corpus artifact is
`research/binary/basement1_secret_differential_report.json`.

The completed M6 corpus covers seeds 1..10,000 independently for NORMAL and
HARD: 20,000 comparisons and 21,526 attempts, with 1,433 retrying seeds. It
reaches Secret candidates with 1, 2, 3 and 4 neighbors, tie vectors of sizes
1..7, 19 boundary placements, 4,423 large-room neighbor cases and 3,786
L-shape neighbor cases. The natural corpus always found a Secret candidate;
the no-candidate/no-final-draw path is covered by a synthetic unit fixture.

The completed M7 Ultra corpus covers seeds 1..10,000 independently for NORMAL
and HARD: 20,000 comparisons over the same 21,526 preceding attempts. It
reaches 2 natural NORMAL null results, 289 boundary placements, diagonal and
distance-two outer neighbors, neighbor counts 1..6, tie sizes 0..9, 3,130
large-room cases, 2,691 L-shape cases, red-door write counts 0..13 and all nine
current type-29 variants. Clean/reference equality includes every candidate,
RNG transition, config/weight mutation, descriptor/map field and red-door bit.

The completed accepted-layout corpus covers the same 10,000 NORMAL and 10,000
HARD seeds: 20,000 matching clean/reference results over 21,526 attempts, with
1,433 retrying seeds and a maximum of four attempts. NORMAL makes 55,127 late
ordinary assignments and HARD 71,366. It verifies collection/query/selection,
Level RNG and weight mutations, every final descriptor/config and BossPool
commit. No natural late missing-config case occurs; directed fixtures cover
that false/retry edge. Artifact:
`research/binary/basement1_full_differential_report.json`.

The completed successful-lifecycle corpus rechecks those 20,000 layouts and
then compares the fixed tail independently: 560,000 persistent Level draws,
160,000 fixed descriptor assignments and 160,000 private-stream transitions
match, with no missing config. Artifact:
`research/binary/basement1_lifecycle_differential_report.json`.

The Basement-II topology leaf corpus covers 10,000 NORMAL and 10,000 HARD
start seeds, 9,733,462 generator draws, every curse-selector outcome and every
RoomShape 1..12. Artifact:
`research/binary/basement2_topology_differential_report.json`.

The inherited Basement-II BossPool corpus first replays the matching accepted
Basement-I layout state, then compares the resumed pool picker for 10,000
NORMAL and 10,000 HARD seeds. It covers 140,000 persistent pre-rolls, 20,000
local draws and 2,127 natural repicking seeds (up to three remaps). Natural
fallback/pool-reset counts are zero; directed tests cover those exhaustion
paths. Artifact:
`research/binary/basement2_boss_pool_differential_report.json`.

The complete Basement-II accepted-layout plus successful-lifecycle corpus
covers 10,000 NORMAL and 10,000 HARD start seeds. NORMAL produces 10,449
Stage-2 attempts with 432 retrying seeds; HARD produces 10,403 attempts with
394 retrying seeds; the maximum is three attempts. It compares every M5/M6/M7
mutation, late query/assignment, accepted descriptor/map/config, second boss
commit and next-run snapshot. The lifecycle portion matches 560,000 persistent
Level draws, 160,000 fixed assignments and 160,000 private-stream transitions,
with no missing config. Artifact:
`research/binary/basement2_full_differential_report.json`.

Artifacts:

- `research/binary/topology_differential_report.json`;
- `research/binary/topology_instruction_emulation.json`;
- `research/binary/topology_binary_verification.json`;
- `research/binary/special_room_differential_report.json`;
- `research/binary/basement1_pipeline_differential_report.json`;
- `research/binary/basement1_secret_differential_report.json`;
- `research/binary/basement1_ultra_differential_report.json`;
- `research/binary/late_room_config_binary_verification.json`;
- `research/binary/basement1_full_differential_report.json`;
- `research/binary/post_layout_lifecycle_binary_verification.json`;
- `research/binary/basement1_lifecycle_differential_report.json`;
- `research/binary/basement2_floor_init_binary_verification.json`;
- `research/binary/basement2_topology_differential_report.json`;
- `research/binary/boss_pool_repick_binary_verification.json`;
- `research/binary/basement2_boss_pool_differential_report.json`;
- `research/binary/basement2_through_treasure_binary_verification.json`;
- `research/binary/basement2_through_treasure_differential_report.json`;
- `research/binary/basement2_post_treasure_binary_verification.json`;
- `research/binary/basement2_secret_differential_report.json`;
- `research/binary/basement2_accepted_layout_binary_verification.json`;
- `research/binary/basement2_post_layout_lifecycle_binary_verification.json`;
- `research/binary/basement2_full_differential_report.json`;
- `research/binary/ultra_secret_binary_verification.json`;
- `research/notes/boss_pool_binary_proof.md`;
- `research/notes/generation_retry_semantics.md`;
- `research/notes/room_config_binary_proof.md`;
- `research/notes/special_room_binary_proof.md`;
- `research/notes/post_treasure_callgraph.md`;
- `research/notes/secret_binary_proof.md`;
- `research/notes/ultra_secret_entry.md`;
- `research/notes/ultra_secret_binary_proof.md`;
- `research/notes/ultra_secret_rng_ledger.md`;
- `research/notes/late_variant_failure_semantics.md`;
- `research/notes/late_room_config_binary_proof.md`;
- `research/notes/basement1_full_layout_proof.md`.
- `research/notes/post_layout_lifecycle_binary_proof.md`;
- `research/notes/canonical_run_profile.md`.
- `research/binary/womb1_100_differential_report.json`;
- `research/binary/womb2_100_differential_report.json`;

## Blockers

No binary-proof blocker remains for the canonical ORIGINAL-route accepted
13x13 layouts (Basement I..Womb II) and their successful post-layout
generation-state tails.

Whole-function instruction emulation remains
`HIGH_ISOLATION_COST_NOT_BLOCKING_STATIC_PROOF`; exact leaf emulation is kept
for suitable helpers only.

No qualified current-version public complete-floor fixture has been accepted.
This keeps external validation independent and unvalidated, but does not
downgrade the complete static-binary proofs. The next reconstruction boundary
is the alternate-route chapters (Downpour/Dross/Mines/Ashpit/Mausoleum/
Gehenna): Stage-1..6 floor initialization for stage_type 4/5, alt BossPool
entries, post-topology predicate changes and the successful lifecycle
handoff.
