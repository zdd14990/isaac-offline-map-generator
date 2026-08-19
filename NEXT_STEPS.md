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

Generation for the eight floors (Womb I/II, Downpour I/II, Mines I/II,
Mausoleum I/II) is **FAIL CLOSED, not implemented**. Blocker:

1. `post_layout_lifecycle.run_post_layout_lifecycle` guard rejects
   `level_stage` 7/8 and `stage_type` 4/5; the `-10` fixed descriptor
   (stage-type 4/5 plus level-stage 7/8) and the `-9` (room-config-stage 13)
   descriptor are unimplemented; the 28-draw invariant would change.
2. No binary evidence exists: no RVAs/selection seeds for the `-10` branch,
   no Womb/Downpour/Mines/Mausoleum floor-init analysis, no notes.

Next concrete steps (each needs static analysis of the frozen binary):

- Disassemble the shared tail `0x0033D1D6..0x0033D94B` for level-stage 7/8
  and stage-type 4/5; extract the `-10` descriptor selection (RVAs, room
  type, subtype, seeds) and its extra RNG consumption.
- Derive floor-init topology inputs for Womb I/II (slot 7/8; Womb I is odd
  and XL-capable; `get_room_config_stage(7, ORIGINAL)` = 10, Womb BossPool
  index 10) and for the alt floors (slot `level_stage + 1`, stage type 4).
- Implement clean + reference pipelines, ~100 differentials per floor
  (50 NORMAL + 50 HARD), and grade honestly (PARTIAL_BINARY / PREVIEW
  at most until the corpus grows) — never `CONFIRMED_BINARY` on 100 samples.
- Register in `SUPPORTED_FLOORS`/bot_api and update the UI floor selector.

Verification command:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

Result: 462 passed (448 + 14 bot_api stage-token tests).
