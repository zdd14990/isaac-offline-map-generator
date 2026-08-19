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

## NEXT: (optional, out of first-release scope) Womb I / Stage 7

Do not start Stage 7 unless explicitly requested. Womb I is odd (XL possible),
with `get_room_config_stage(7, ORIGINAL)` = 10 (Womb BossPool index 10), a
fresh pool starting from its run-start state, and its own Stage-7
`Level::Init`/`generate_dungeon` branch. It is outside the frozen first-release
scope.

Previous verification command:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

Result: 448 passed.
