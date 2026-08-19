# Post-layout descriptor -10 (grid index -10)

Status: **reconstructed from the frozen binary** (SHA256
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`).

Evidence: `scripts/disassemble_range.py --start-va 0x0073D838 --end-va 0x0073D950`
(level tail `0x0033D1D6..0x0033D94B`), region after the Angel descriptor.

## Branch location and predicate

The branch lives at `0x0033D874..0x0033D925`, immediately after the Angel
(GridIndex -18) assignment:

```text
0x0033D874  mov eax, [edi+4]              ; stage_type field
0x0033D877  cmp eax, 4
0x0033D87A  je 0x0033D885                 ; stage_type == 4 -> enter
0x0033D87C  cmp eax, 5
0x0033D87F  jne 0x0033D925                ; stage_type not 4/5 -> skip
0x0033D885  mov eax, [edi]                ; level_stage field
0x0033D887  cmp eax, 8
0x0033D88A  je 0x0033D8BF                 ; level_stage == 8 -> enter
0x0033D88C  cmp eax, 7
0x0033D88F  jne 0x0033D925                ; level_stage not 7/8 -> skip
```

**Predicate: `stage_type in (4, 5) AND level_stage in (7, 8)`** (both must
hold). A third gate follows:

```text
0x0033D895  mov eax, [0xc71678]           ; Game object
0x0033D89A  mov esi, [eax + 0x26550]      ; special-room used bits (Game+0x26550)
0x0033D8A0  or  esi, [edi + 0xc]          ; OR with descriptor used-bits field
0x0033D8A3  call 0x6f9400                 ; bitset helper
0x0033D8A8  mov edi, eax
0x0033D8AA  or  edi, esi
0x0033D8AC  call 0x6f95a0                 ; bitset helper (negated later)
0x0033D8B1  not eax
0x0033D8B3  and eax, edi
0x0033D8B5  test al, 2                    ; require bit 1 set
0x0033D8B7  je  0x0033D925                ; else skip
```

## Effect when entered (2 persistent Level RNG draws)

```text
0x0033D8C1  call 0x7e90f0                 ; Level RNG draw #1
0x0033D8C8  push -0xa                     ; grid index -10
0x0033D8CC  call 0x740bc0                 ; GetDescriptor(-10)
0x0033D8D4  call 0x428940                 ; descriptor -> RoomConfigQuery
0x0033D8E5  call 0x7e90f0                 ; Level RNG draw #2
... pushes (variant 5, subtype 13, stage 10, ...)
0x0033D910  call 0x82c7d0                 ; RoomConfig selector
0x0033D917  push -0xa                     ; grid index -10
0x0033D91D  call 0x740bc0                 ; GetDescriptor(-10)
0x0033D922  mov [eax+0x10], esi           ; descriptor.config = selected
```

- **Two persistent Level RNG draws** (`0x7e90f0`), plus a concrete RoomConfig
  selection via the same selector (`0x82c7d0`) used by the fixed descriptors.
- Descriptor write target: GridIndex -10.
- RoomConfig query pushes observed: variant `5`, subtype `13` (`0xd`), stage
  `10` (`0xa`) in the frame, consistent with a Womb-stage special room.
  (Exact field order of `0x82c7d0` still to be pinned against the clean
  `_assign`/`_query` mapping.)

## Who triggers it

`level_stage in (7, 8)` with `stage_type in (4, 5)` is the **Corpse (Mother
route) chapter pair** — the Repentance alternate path's final floors. It is
NOT Downpour/Mines/Mausoleum (those use level_stage 1..6) and NOT Womb I/II
(stage_type 0).

## Impact on the supported floor set

- MAIN Womb I/II (`7`, `8`): stage_type 0 -> branch skipped.
- ALT Downpour/Mines/Mausoleum (`1+..6+`): level_stage 1..6 -> branch
  skipped.
- Therefore the current `skipped_optional_grid_indices=(-9, -10)` behavior is
  **correct for all eight target floors**, and the branch adds no RNG draws
  to them. The extra 2 draws apply only to Corpse floors (out of scope).

## RNG identity

Both draws are `Level._generationRNG` (index 35) via the `0x7e90f0` wrapper.
`0x7e9020` (used in the door-chance write path earlier in the tail) is
`IsaacRNG::Next` operating on a **local stack copy** seeded from the current
Level RNG state; it does NOT advance the persistent Level RNG (verified by
disassembling `0x3E9020..0x3E90F0`: the shift/xor triple on `[ecx+4]/[ecx+8]/
[ecx+0xc]`).

Open items for a future Corpse implementation (out of scope this round): exact
`0x82c7d0` argument order, the two `0x6f9400`/`0x6f95a0` bitset helpers'
semantics, and the `test al, 2` bit source.
