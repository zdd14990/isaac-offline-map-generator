# Ghidra Static Analysis Record

The copied executable was imported as a PE into Ghidra 12.1.2 headless. Ghidra
performed static analysis and decompilation only; no target code was executed.

- Ghidra archive SHA-256:
  `b62e81f17cb9e385895f6d37d0da2402a166fe0687e297bb835dcf19f898751c`
- Temurin JDK archive SHA-256:
  `9ba9638283c472bb541f1812797154628f509ca8347a6b4feac03a7d42603699`
- imported PE SHA-256:
  `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Reproducible scripts:

- `scripts/ghidra_import.ps1` validates the copied path and hash before import;
- `scripts/export_decomp.ps1` processes the existing static project;
- `scripts/ghidra/ExportIsaacFunctions.java` renames and exports selected
  functions.

Ghidra initially marked the game's internal varargs logger at VA `0x00A112C0`
as `noreturn`, truncating generator control flow after logging calls. The
export script corrects that function property, restores call fallthroughs and
forces the raw-disassembly-proven extents of the two affected generator
functions before decompilation.

The first import created Ghidra 12.1.2 settings/caches in the default user
AppData locations before the isolation variables were corrected. Their
creation timestamps uniquely matched that import and the Ghidra parent
directories contained no other entries. Those three exact directories were
moved intact to:

`research/ghidra-user/initial-default-appdata/`

Subsequent scripts set `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, application
settings, cache and temp paths to `research/ghidra-user/`.
