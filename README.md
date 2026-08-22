# Isaac Offline Map Generator

Generate *The Binding of Isaac: Repentance+* maps from a seed without
launching the game. It includes a desktop preview and a PNG/JSON command-line
export used by Bot integrations.

## Support

| Route | Floors |
| --- | --- |
| MAIN `1`-`8` | Basement I through Womb II |
| ALT `1+`-`6+` | Downpour I, Dross, Mines I, Ashpit, Mausoleum I, Gehenna |

NORMAL and HARD are supported. Unsupported floors fail closed instead of
using approximate generation.

Natural Labyrinth / XL is detected, but XL map generation is currently
unsupported and fails closed. There is no force-XL option. The generator does
not read player saves automatically.

## Install

Requires Python 3.11+ and a compatible local game installation.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e .
```

Extract the required XML/STB resources from your own installation:

```powershell
.venv\Scripts\python.exe scripts\extract_resources.py `
  "C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth" `
  research\input\extracted_resources
```

Extracted resources are ignored by Git.

## Usage

```powershell
# Desktop preview
.venv\Scripts\python.exe scripts\launch_preview.py

# CLI export
.venv\Scripts\python.exe scripts\map_export.py --seed "B911 99AC" --difficulty NORMAL --route MAIN --stage 5 --output-dir output\maps
.venv\Scripts\python.exe scripts\map_export.py --seed "B911 99AC" --difficulty HARD --route ALT --stage 2 --output-dir output\maps

# Show supported floors
.venv\Scripts\python.exe scripts\map_export.py --supported
```

For ALT, `--stage 2` means `2+` because the route is supplied separately.

## Tests

```powershell
.venv\Scripts\python.exe -m pytest tests\ -q
```

## Safety and accuracy

The project uses static disassembly and statically extracted resources. It
does not execute or attach to `isaac-ng.exe`, inspect runtime memory, inject
code, use Lua, or launch Steam.

Current accuracy details are in [STATUS.md](STATUS.md). Static evidence is in
[research/evidence.md](research/evidence.md).

This independent fan/research project is not affiliated with the game's
creators or publishers.
