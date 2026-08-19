# Game Version Profile

All values below were obtained by static reads. `isaac-ng.exe` was never
executed.

Executable: `C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\isaac-ng.exe`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

File version: no Windows version-resource value

Product version: no Windows version-resource value

Static in-binary version: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

Size: `9,362,440` bytes

PE architecture: 32-bit x86 (`Machine=0x014c`, PE32 magic `0x010b`)

PE timestamp: `0x69e6e3a7` / `2026-04-21T02:40:39Z`

Steam build ID: `22878971`

## Version evidence

The executable has no populated Windows `FileVersion` or `ProductVersion`
resource. The exact version therefore comes from the full product/version
string at file offset `0x77c7b4`. The binary also contains a shorter
`v1.9.7.17` marker and a stale/internal `1.9.7.16` marker. The latter is not
used as the profile version because the product/crash strings identify
`v1.9.7.17.J460`.

The reproducible PE report is `research/binary/pe_fingerprint.json`.

## Installed DLC/resource sets

Steam `appmanifest_250900.acf` reports these installed depots:

| Depot | DLC app | Meaning | Manifest |
|---:|---:|---|---:|
| 250902 | — | Rebirth base | 4994611894646808503 |
| 250905 | 401920 | Afterbirth | 1709017229885880564 |
| 250908 | 570660 | Afterbirth+ | 7333987924869605149 |
| 250911 | 1426300 | Repentance | 7652847940910762229 |
| 3353471 | 3353470 | Repentance+ | 229910742625134068 |

There is one top-level `resources` directory. It contains `packed` and
`scripts`; there are no separate `resources-dlc*` directories. Relevant
packed archives include `config.a`, `rooms.a`, `afterbirth.a`,
`afterbirthp.a`, and `repentance.a` plus language, graphics, audio, animation,
and video archives.

The installation also contains third-party-looking surface files/directories,
including `mods`, `REPENTOGONLauncher`, `! CN PATCH`, `inject.dll`, and
`bootstp.dll`. They were not executed, loaded, or treated as vanilla resource
inputs. Exact-mode work is bound to the executable hash and packed resource
hashes, and will ignore mod overlays unless a future profile explicitly
supports them.

## ResourceExtractor

ResourceExtractor:
`C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\tools\ResourceExtractor\ResourceExtractor.exe`

Size: `274,432` bytes

File/Product version: no Windows version-resource values

The official tool was allowed by the task and was tried with a separate output
directory. On this system it terminated with an access violation/heap
corruption while processing current archives. It was not used to produce the
resource database. Failure logs are retained under `research/resources/`.
After that failure, extraction used only our static archive reader against the
original read-only archives.

## Safety statement

- The original executable and resource archives were not modified.
- The executable copied to `research/input/` hashes identically to the source.
- No save files, `options.ini`, mods, Steam userdata, or running process memory
  were read or modified.
- `isaac-ng.exe`, Steam, REPENTOGON, launchers, injectors, and mods were never
  executed.
