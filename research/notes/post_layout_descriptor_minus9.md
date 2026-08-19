# Post-layout descriptor -9 (grid index -9)

Status: **reconstructed from the frozen binary** (SHA256
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`).

Evidence: `scripts/disassemble_range.py --start-va 0x0073D1D6 --end-va 0x0073D950`,
region `0x0033D5E8..0x0033D643` (between the -7 and -8 descriptors).

## Branch location and predicate

After the -7 descriptor is placed, the -8 slot is selected:

```text
0x0033D5E8  cmp dword ptr [ebp-0x128], 0xd   ; room_config_stage vs 13
0x0033D5F6  jne 0x0033D645                    ; rcs != 13 -> place -8
0x0033D5F8  push -9                           ; rcs == 13 -> place -9 instead
```

**Predicate: `room_config_stage == 13`** (Blue Womb chapter only).

## Effect (1 persistent Level RNG draw, replacing the -8 draw)

The -9 path mirrors the -8 path exactly in RNG cost:

```text
0x0033D613  call 0x7e90f0                     ; Level RNG draw
... pushes (variant 1, subtype 13, stage 13, ...)
0x0033D63A  call 0x82c7d0                     ; RoomConfig selector
0x0033D641  push -9                           ; grid index -9
0x0033D643  jmp  0x0033D690                   ; join the -8 write epilogue
```

The -8 path (rcs != 13) at `0x0033D645..0x0033D68C` is identical except it
pushes grid -8 and jumps to the same epilogue. Both consume **exactly one**
persistent Level RNG draw (`0x7e90f0`), so the branch does not change the
total draw count.

## Who triggers it

`room_config_stage == 13` is the Blue Womb chapter (stages.xml stage id 13 =
`13.Blue Womb.xml`). None of the eight target floors use rcs 13:
- MAIN Womb I/II: rcs 10 (predicted; see `floors/womb1.md`).
- ALT Downpour/Mines/Mausoleum: rcs 27..32 (stages.xml stage ids 27..32).

## Impact on the supported floor set

The `-9` branch never fires for MAIN 7/8 or ALT 1+..6+. The existing
`skipped_optional_grid_indices=(-9, -10)` behavior is correct for all eight
target floors. Note: the **-8** descriptor (grid -8, room type 1, stage 13,
subtype 1) is still placed on every floor using stage-13 entries, exactly as
the clean `_CANONICAL_FIXED_SPECS` models it.

## Purpose

-9 is the Blue Womb's extra fixed room (the second special-room slot) that
replaces the -8 slot on that chapter. Both -8 and -9 draw one config seed and
write the concrete RoomConfig to the descriptor's config field
(`[eax+0x10]`).
