# Isaac Offline Map Generator

Generate *The Binding of Isaac: Repentance+* floor maps from a seed without
launching the game. The project provides a desktop preview and a headless CLI
that exports PNG and JSON files.

## Features

- Deterministic offline reconstruction from seed, difficulty and floor.
- NORMAL and HARD support.
- Automatic curse and Labyrinth / XL selection; there is no force-XL option.
- Static game-resource reading only. Isaac and Steam are never launched.
- Unsupported floors fail closed instead of using approximate generation.

The generator uses a fixed, reproducible generation profile and does not read
the player's save. Progression can affect curse rates, so a real save may
produce a different curse result.

## Supported floors

| Route | Tokens | Floors |
| --- | --- | --- |
| MAIN | `1`-`8` | Basement I/II, Caves I/II, Depths I/II, Womb I/II |
| ALT | `1+`-`6+` | Downpour I, Dross, Mines I, Ashpit, Mausoleum I, Gehenna |

MAIN 1-6 are `CONFIRMED_BINARY`. MAIN 7-8 and ALT 1+-6+ are
`PARTIAL_BINARY`. Other floors, routes, mods and arbitrary gameplay state are
unsupported.

The implementation targets this exact executable:

```text
The Binding of Isaac: Repentance+ v1.9.7.17.J460
SHA256 3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b
```

## Setup

Requires Python 3.11+ and a compatible local game installation.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e .
```

The repository does not include game assets. Extract the required XML/STB
resources from your own installation:

```powershell
.venv\Scripts\python.exe scripts\extract_resources.py `
  "C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth" `
  research\input\extracted_resources
```

Extracted files are stored under `research/input/extracted_resources/` and are
ignored by Git.

## Usage

Launch the desktop preview:

```powershell
.venv\Scripts\python.exe scripts\launch_preview.py
```

Generate a MAIN or ALT floor from the CLI:

```powershell
.venv\Scripts\python.exe scripts\map_export.py --seed "B911 99AC" --difficulty NORMAL --route MAIN --stage 5 --output-dir output\maps
.venv\Scripts\python.exe scripts\map_export.py --seed "B911 99AC" --difficulty HARD --route ALT --stage 2 --output-dir output\maps
.venv\Scripts\python.exe scripts\map_export.py --supported
```

For ALT, `--stage 2` means `2+`; the route is supplied separately. The same
CLI is used by bot integrations.

## Tests

```powershell
.venv\Scripts\python.exe -m pip install pytest
.venv\Scripts\python.exe -m pytest -q
```

Resource-dependent tests skip automatically when extracted assets are absent.

## Evidence and safety

The generator was reconstructed from static disassembly, local STB/XML assets
and clean-vs-reference differential tests. It does not execute or attach to
`isaac-ng.exe`, inspect runtime memory, inject code, use Lua, or launch Steam.

See [STATUS.md](STATUS.md) for the current accuracy boundary and
[research/evidence.md](research/evidence.md) for binary evidence.

## Disclaimer

This independent fan/research project is not affiliated with Edmund McMillen,
Nicalis, or their licensors. The Binding of Isaac and its assets belong to
their respective owners.
