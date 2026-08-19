# Continuation checkpoint

Frozen target: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

EXE SHA256:
`3BDFC8BAE0DC7E334B76009D0AD45DFBB16EE5F00C06FFBC3A0094E34D44616B`

Safety: do not execute/load `isaac-ng.exe`, create a game/Steam process, use a
Lua mod, or use a runtime memory oracle. Static reads of the PE copy under
`research/input/` only.

## Status: FIRST_RELEASE_SCOPE_COMPLETE

The six ORIGINAL-route floors are all `CONFIRMED_BINARY`:

```text
Basement I   CONFIRMED_BINARY
Basement II  CONFIRMED_BINARY
Caves I      CONFIRMED_BINARY
Caves II     CONFIRMED_BINARY
Depths I     CONFIRMED_BINARY
Depths II    CONFIRMED_BINARY
```

Womb I and later / alternate routes: `UNSUPPORTED — FAIL CLOSED`.

External gameplay validation remains `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Depths II (Stage 6) summary

- Stage seed slot 6; target `min(floor(6*10/3)+5+bit, 20)` = capped 20; Lost
  +4; HARD +2+bit; required dead ends 6.
- Even Stage 6 never satisfies the Labyrinth predicate → never XL.
- `get_room_config_stage(6, ORIGINAL)` = 7 → shared Depths RoomConfig stage and
  Depths BossPool (index 7), inherited (advanced) from Depths I.
- Difficulty window NORMAL (5..10), HARD (10..15); planetarium
  `f32(5*0.2+0.01)`.
- Post-layout tail reuses the shared `0x0033D1D6..0x0033D94B` helper.

Implementation: `floor_init(_reference).py` (`derive_depths2_topology_inputs`),
`depths2_full_pipeline(_reference).py`, `depths2_lifecycle.py`,
`tests/differential/test_depths2_full_pipeline_differential.py`,
`tests/unit/test_depths2_floor_init.py`, `scripts/differential_depths2_full.py`,
`research/notes/floors/depths2.md`.

## Depths II differential result

`research/binary/depths2_full_differential_report.json`:

```text
comparisons          20,000
attempts             20,372
retrying_seeds       363
max_attempts         4
xl_floors            0
rng_transitions      720,000
room_config_selections 160,000
boss_selections      20,000
secret_placements    20,000
ultra_placements     20,000
mismatches           0
```

## First-release packaging

- `Launch Isaac Offline Map.bat`: one-click launcher (checks `.venv`, runs
  `scripts/launch_preview.py`).
- `README.md`: user-facing run/support/not-supported sections.
- `SUPPORTED_FLOORS` registry: six floors, each with `level_stage`, replay
  chain and generator callable.
- 120-case smoke matrix (6 floors x 2 difficulties x 10 seeds): all complete
  and deterministic.

## Tests

`448 passed`.

## Womb I/II and alternate floors: status (2026-08-18)

User-facing token surface is DONE and verified:

- `isaacmap.bot_api`: `parse_stage_token` (main `1..8`, alt `1+..6+`),
  `floor_name_for`, route-aware cache keys (`MAIN`/`ALT` in the file name),
  `--route` CLI flag, `--supported` now returns the full route table plus
  per-route supported lists.
- fraq bot `/map`: parses the new tokens, passes `route` through to the
  generator, cache key includes route, and new floors reply FAIL CLOSED with
  the floor name (e.g. "该层当前未支持（Womb I）..."). Tests: 94 fraq + 14
  generator bot_api tests; fraq typecheck/build green.

## Round 2 (2026-08-18): post-layout lifecycle analysis done, floors still not implemented

Checkpoint 1 of the task plan is complete: the `-9`/`-10` descriptor branches
are reconstructed from the binary and the draw-count question is resolved.

**Confirmed (binary):**

1. `-10` descriptor = Corpse (Mother route) floors only:
   predicate `stage_type in (4,5) AND level_stage in (7,8)`; 2 extra Level
   RNG draws; GridIndex -10 write. Skipped by all 8 target floors.
2. `-9` descriptor = Blue Womb only: predicate `room_config_stage == 13`;
   replaces the `-8` slot with the same 1-draw cost. Skipped by all 8
   target floors.
3. Door-chance flag writes use a local `IsaacRNG::Next` copy (raw xorshift
   `0x3E9020`) — no persistent Level RNG consumption.
4. => 28 persistent Level RNG draws, identical to Depths II, for every
   target floor. The tail guard can be relaxed on this evidence.
5. `stages.xml` authoritative resource stages; `boss_pool.py` pool == rcs on
   ORIGINAL; `stage_seed.py` alt slot rule (`level_stage + 1`).

**Still required before generation can be implemented:**

1. Binary verify `get_room_config_stage(7..8, 0)` and `(1..6, 4/5)`
   (Womb II may be rcs 11/Utero, not 10; alt floors 27..32).
2. Floor-init topology inputs for stage_type 4/5 (NOT extrapolated from
   ORIGINAL) and for stage 7 (XL-capable; Labyrinth valid on odd stages).
3. Through-Treasure / Secret / Ultra / late RoomConfig stage gates for
   level_stage 7/8 and stage_type 4/5 (every stage-dependent branch verified
   against the binary, not pattern-extended).
4. Womb I XL (existing XL machinery gated to stages 3/5).
5. Alternate-route RunGenerationState fields and BossPool indices/lists.
6. Then: profiles + floor_init + clean/reference pipelines + ~100
   differentials per floor (800 total), grade at most PARTIAL_BINARY /
   PREVIEW_SUPPORTED, register, update UI selector.

Notes written this round: `research/notes/post_layout_descriptor_minus9.md`,
`post_layout_descriptor_minus10.md`,
`research/notes/stage_type_4_5_binary_proof.md`,
`research/notes/floors/womb1.md`, `research/notes/floors/womb2.md`.
Evidence appended to `research/evidence.md`; `STATUS.md` round-2 section
updated.

Verification command:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

Result: 462 passed (448 + 14 bot_api stage-token tests), confirmed at the
start of round 2.
