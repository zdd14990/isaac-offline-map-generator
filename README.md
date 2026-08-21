# Isaac Offline Map Generator

Offline reconstruction of The Binding of Isaac: Repentance+ floor generation
from a seed, based on static binary analysis and local game resources —
without launching the game.

## What it does

Given a seed, difficulty and floor, this project replays the game's dungeon
generation offline and produces the reconstructed floor as a map image or
interactive preview:

```text
seed + difficulty + floor
        ↓
  offline generation replay
        ↓
  reconstructed room layout
        ↓
  PNG export / research preview UI
```

A headless API (`isaacmap.bot_api`, `scripts/map_export.py`) exposes the same
pipeline to other programs (e.g. chat bots) without a GUI.

## Why this is interesting

- **Static reverse engineering.** The generation pipeline is reconstructed
  from a frozen copy of the game executable using static analysis (RVA /
  control-flow notes, disassembly listings, emulated function traces). The
  game executable is never executed, attached to, or read at runtime.
- **Deterministic RNG reconstruction.** All shift triples of the game RNG,
  `SetSeed`/`Next`/`RandomInt`/`RandomFloat` and stage-seed derivation are
  reproduced bit-for-bit.
- **Cross-floor persistent generation state.** Boss pools, RoomConfig weights,
  special-room used bits and RNG streams carry across floors exactly like the
  game's `RunGenerationState`.
- **Full special-room reconstruction.** Secret, Super Secret, Ultra Secret,
  Shop, Treasure, Boss and the conditional special-room family are placed
  through the same retry/commit transaction as the binary.
- **Reference-vs-clean differential testing.** An independent mechanical
  reference implementation is compared against the clean implementation over
  20,000 seeds per floor with zero mismatch — no runtime game oracle involved.

To the best of the author's current knowledge this is a relatively uncommon
approach; no claim of priority is made here.

## Supported game version

The reconstruction is frozen to one exact executable:

```text
The Binding of Isaac: Repentance+ v1.9.7.17.J460
SHA256 3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b
```

Other game versions are not guaranteed to be compatible.

## Supported floors

Current support registry (`SUPPORTED_FLOORS`, canonical vanilla NORMAL /
HARD):

```text
MAIN:
1  Basement I      CONFIRMED_BINARY
2  Basement II     CONFIRMED_BINARY
3  Caves I         CONFIRMED_BINARY
4  Caves II        CONFIRMED_BINARY
5  Depths I        CONFIRMED_BINARY
6  Depths II       CONFIRMED_BINARY
7  Womb I          PARTIAL_BINARY
8  Womb II         PARTIAL_BINARY

ALT:
1+ Downpour I      PARTIAL_BINARY
2+ Dross           PARTIAL_BINARY
3+ Mines I         PARTIAL_BINARY
4+ Ashpit          PARTIAL_BINARY
5+ Mausoleum I     PARTIAL_BINARY
6+ Gehenna         PARTIAL_BINARY
```

MAIN `1`..`6` are `CONFIRMED_BINARY` (20,000-seed differentials, zero
mismatch). MAIN `7`/`8` and ALT `1+`..`6+` are `PARTIAL_BINARY` (100 ordered
comparisons per floor, zero mismatch — intentionally capped; that grade is
reserved below `CONFIRMED_BINARY`). `PARTIAL_BINARY` never implies
`EXTERNALLY_VALIDATED_GAMEPLAY`.

Everything else — ALT `7+`/`8+` (Corpse, Mother route), Sheol, Cathedral,
The Chest, Dark Room, Void, mods, arbitrary gameplay state — is
**UNSUPPORTED — FAIL CLOSED**: the generator rejects it instead of
approximating. The registry in `src/isaacmap/preview.py` is the single
source of truth; the headless API (`isaacmap.bot_api`) validates tokens
route-aware (`MAIN 1..8`, `ALT 1+..6+`) and never opens ALT 7/8.

## Evidence model

Two independent evidence dimensions are tracked separately:

- `CONFIRMED_BINARY` — behavior reproduced from the exact frozen executable
  via static analysis and differential comparison against an independent
  mechanical reference (20,000 seeds per floor, zero mismatch).
- `PARTIAL_BINARY` — implemented from binary-confirmed parameters with a
  100-comparison per-floor corpus (Womb I/II, all ALT floors).
- `NOT_EXTERNALLY_VALIDATED_GAMEPLAY` — the reconstruction has not been
  compared against live in-game runs on a real save.

`CONFIRMED_BINARY` / `PARTIAL_BINARY` do not imply
`EXTERNALLY_VALIDATED_GAMEPLAY`. See `STATUS.md` for the precise input
contract and evidence boundary.

## How it works

```text
isaac-ng.exe static analysis (RVA / control flow / disassembly)
        ↓
RNG, stage seed, topology, RoomConfig, BossPool reconstruction
        ↓
local game resource parsing (STB/XML/ANM2/PNG from the user's install)
        ↓
independent reference implementation
        ↓
clean implementation
        ↓
reference-vs-clean differential tests (20,000 seeds / floor)
        ↓
offline map rendering (Pillow) / research preview UI (Tk)
```

The safety boundary is strict: `isaac-ng.exe` is never executed, Steam is
never launched, no code is injected, no Lua mod is used, and no running game
process is read. Analysis uses only static reads of a copied executable,
static disassembly/decompilation output, extracted resources and our own
tests.

## Installation

Requires Python 3.11+.

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

`requirements-research.txt` contains optional tooling used during
reverse-engineering research (disassembly/emulation); it is not required to
run the generator, tests or UI.

## Running the UI

```powershell
.venv\Scripts\python.exe scripts\launch_preview.py
```

or double-click `Launch Isaac Offline Map.bat`.

The research preview UI accepts checksum-valid seeds, NORMAL/HARD, and calls
only the clean `src/isaacmap/` implementation. Selecting a later floor replays
the preceding floors' generation-only lifecycle from the run seed. JSON export
goes to `output/maps/`; PNG export is also available.

Headless map generation for programs:

```powershell
.venv\Scripts\python.exe scripts\map_export.py --seed "B911 99AC" --difficulty NORMAL --stage 5 --output-dir output/maps
.venv\Scripts\python.exe scripts\map_export.py --supported
```

## Testing

```powershell
.venv\Scripts\python.exe -m pytest -q
```

Resource-independent tests (seed/RNG/floor-init/topology/renderer) always run.
Resource-dependent tests are skipped automatically when the extracted game
resources are not present (see below).

## Game resources

**This repository does not redistribute The Binding of Isaac game assets.**

A locally installed compatible copy of the game is required for
resource-dependent functionality (STB/XML room databases, official minimap
icons). From that legal install, extract the resources you need:

```powershell
.venv\Scripts\python.exe scripts\extract_resources.py
.venv\Scripts\python.exe scripts\prepare_resource_extraction.py
```

The extraction output lands under `research/input/extracted_resources/` and is
git-ignored. The standard Steam install path is used by default; set the
`ISAAC_GAME_ROOT` environment variable to point elsewhere.

## Disclaimer

This is an independent fan/research project. It is not affiliated with,
endorsed by, or connected to Edmund McMillen, Nicalis, or their licensors.
The Binding of Isaac and its assets belong to their respective owners.
