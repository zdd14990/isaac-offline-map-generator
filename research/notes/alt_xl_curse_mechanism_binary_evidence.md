# ALT XL / curse mechanism — binary evidence (round 6)

Frozen binary: `Binding of Isaac: Repentance+ v1.9.7.17.J460`, SHA256
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`.
All addresses below are VAs; RVA = VA - 0x400000.  Decoding was re-verified
with exact-offset disassembly (a linear `disasm(code, base+start)` bug in the
earlier tooling decoded the wrong bytes and produced phantom instructions;
the earlier "state machine sets the ALT flag on every stage-1..6 floor"
conclusion came from that drift and is retracted).

## What was verified byte-exact

1. **The curse gate** (`Level::Init`, VA `0x744CF3..0x74503D`, RVA
   `0x344CF3..0x34503D`):
   - rate denominator chain: `80/40` base (`0x344CF3/0x344DB5`, mode 1 -> 40),
     then `30/20` (`0x344DE8`), `10/6` (`0x344E24`), `5/3` (`0x344E48`) — the
     overrides fire on `[Manager+0x50]`, `[Manager+8]==2`,
     `[Game+0x26630]>0`, `[Game+0x26589]!=0`, `[Manager+0x2fc]>0`.
   - stage 1..6 with `Game+0x2654c & 0x10000` set -> jump to `0x345018`
     (curse = 0, no draw).  Otherwise `RandomInt(rate)==0` -> selector draw
     `% 6` -> Labyrinth(2)/Lost(4)/Darkness(1)/Unknown(8)/Maze(0x20)/Blind(0x40).
   - Labyrinth is further gated by `0x7385c0` (first floor of chapter).

2. **The ALT flag** (`Game+0x2654c` bit 0x10000) is written ONLY at
   `0x52FBE5` (transition state machine case 2, transition type 5 =
   `StartStageTransition(_, 5, _)`) and cleared ONLY at `0x2F45D1` (Game
   recreation / run start, reset fn `0x2F4520`).  The type-5 transition
   (90-frame timer from a boss room with the ALT-exit attachment) is the
   *mirrored-world / special* flow; the canonical ALT floors are entered via
   the ALT door from the corresponding MAIN floor, and their `Level::Init`
   runs with the flag clear — the ordinary curse gate applies.

3. **The ALT floor fixup** (`0x342EF0`) is the flag-set path: it reads the
   per-stage pairing flag (`Game+0x6746c + stage'*0x320, +0x31c`, with
   `stage' = stage+1` for stage_type 4/5) and forces `curse |= 2` + target
   +6 when set.  The pairing flag is computed by `InitStageTable`
   (`0x308050`) = "the current floor's placed room list has >1 boss rooms"
   (= the preceding floor was XL), written only while the ALT flag is clear.

4. **Real-game cross-check** (wiki.gg + community): XL Downpour/Dross/Mines/
   Ashpit/Mausoleum exist; "XL Downpour requires Labyrinth on Basement I";
   "alternate floors always attach as a second floor (.5)".

## Canonical verdict for the reported seed

**DKM89MNM HARD 1+ canonical is NOT XL.**

- canonical fresh-save profile uses the base rate **40** (HARD):
  gate draw `163224774` -> `% 40 = 14` -> gate fails -> **NOT XL**
  (the generator's current output is correct).
- progression rates would flip it: `% 6 == 0` and `% 3 == 0`, and the
  selector draw `3869886000 % 6 == 0` (Labyrinth) — those rates fire only
  with the non-canonical save-progression flags ("Everything is Terrible"
  / "Killed Isaac"), which explains an in-game XL observation.
- the pairing model agrees: Basement I's gate draw `3946623396 % 40 = 36`
  fails, so the ALT pairing flag is 0.

The natural generation is left unchanged.  `/map` remains
`/map 种子 0/1 层数`; the earlier `B`/`--force-xl` force mode was removed
after review.

## Profile identification controls

The denominator tier is now explicit process configuration, not a force-XL
flag. User-reported HARD 1+ results distinguish the target environment:

| Seed | RATE_10_6 | RATE_5_3 | Reported |
|---|---|---|---|
| `BJPK 79MF` | non-XL | XL | XL |
| `BJPK 72ME` | XL | XL | XL |
| `BJPK 79FB` | non-XL | non-XL | non-XL |

This identifies `RATE_5_3`. The clean and mechanical-reference RNG paths
agree on all three traces. The report does not identify the save flag by name
and does not change the external gameplay-validation grade.

## Exact-offset anchors (2026-08-21 recheck)

All ranges were decoded from their actual instruction boundary, not from a
shifted linear buffer:

| Meaning | VA | RVA | File offset | Bytes |
|---|---:|---:|---:|---|
| base rate 80 | `0x744CF3` | `0x344CF3` | `0x3440F3` | `ba 50 00 00 00` |
| HARD chooses 40 | `0x744DB5` | `0x344DB5` | `0x3441B5` | `0f 44 d0` |
| transition flag test | `0x744E92` | `0x344E92` | `0x344292` | `8b 8e 4c 65 02 00` |
| skip when bit 0x10000 | `0x744EA2` | `0x344EA2` | `0x3442A2` | `0f 85 70 01 00 00` -> `0x745018` |
| curse gate draw | `0x744F03` | `0x344F03` | `0x344303` | `ff 75 d8` |
| selector dispatch | `0x744F6C` | `0x344F6C` | `0x34436C` | `ff 24 b5 90 5a 74 00` |
| Labyrinth eligibility call | `0x744F73` | `0x344F73` | `0x344373` | call target `0x7385C0` |
| set Labyrinth bit | `0x744F84` | `0x344F84` | `0x344384` | `83 4f 0c 02` |
| eligibility entry | `0x7385C0` | `0x3385C0` | `0x3379C0` | `8b 15 78 16 c7 00` |

## Full-pipeline XL propagation audit (2026-08-22)

The curse/floor-init trace was correct, but the accepted-layout wrappers had
an integration defect.  They constructed `LevelGeneratorResearch` or
`LevelGeneratorReference` and left the object's `is_xl` byte at its default
false value.  The already-derived XL target and dead-end count were passed,
but the binary `%10` multi-neighbor branch inside topology generation was not
enabled.  This affected both sides of the earlier full-pipeline differential,
so clean/reference equality did not validate this integration point.

The I-floor wrappers now explicitly copy `profile.is_xl` into their clean and
reference generator objects.  No force input or seed special case was added.
The public cache support version changed so a pre-fix non-XL PNG cannot mask
the correction.

For `DKM8 9MNM` HARD Downpour I under `RATE_5_3`, the corrected full-pipeline
input is:

- stage seed `362265690`, generator seed `3869886000`;
- gate `163224774 % 3 == 0`, selector `3869886000 % 6 == 0`;
- curse mask `0x02`, `is_xl=true`, target 12, required dead ends 7;
- allowed-shape mask `0x1FFE`.

The corrected offline result is an XL floor (two Boss rooms and two Treasure
rooms), but its topology still does not equal the supplied game capture.  The
capture has exactly four multi-cell footprints in a different arrangement;
the corrected topology has two.  Matching uses occupied cells, not renderer
coordinates or shape labels, and accepts all eight rotations/reflections plus
translation.

Static negative searches produced no match:

- current generator seed, target 4..30, dead ends 5..12, XL on/off: none;
- the first 5000 binary `Seeds::advance_stage_slot` mutations that still roll
  Labyrinth: none;
- all 14 initial stage slots, the first 64 Level-RNG phases per slot, targets
  7..20, dead ends 5..9, and normal/Giant shape masks: none.

The LevelGenerator flag mapping was also rechecked at the exact function
entry: `+0x390` is XL, `+0x391` is chapter 6, and `+0x392` is Void.  Static
decompilation excludes `0x802980` as a topology rebuild (it updates the
current room/entities), excludes `0x74F0C0` as a geometry source (it reassigns
configs while retaining anchors/shapes/connections), and confirms that the
fixed-geometry helper `0x74F360` belongs to the other ALT pairing flow and is
not reached by ordinary Downpour I XL.

Therefore the PE-backed correction is limited to propagating `is_xl`.  The
captured four-large-room topology is not currently reachable from the
recovered canonical state families, so changing the topology algorithm to
imitate it would be an unsupported approximation.  The remaining mismatch is
open pending a new binary-confirmed input or environmental cause.

Regression: generator `642 passed`; `RATE_5_3` ALT 1+..6+ clean/reference
matrix 600 comparisons, zero mismatch; fraq Bot `95 passed`, typecheck/build
green, and real DKM/Dross/Ashpit PNG smoke passed.
