# Caves I post-layout lifecycle binary proof

Frozen executable: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Method: static read of the PE copy under `research/input/`. The executable was
never executed or loaded. Raw Capstone listing:
`research/decomp/post_layout_tail_0073d1d6.tsv`.

## Question

Does LevelStage 3 (Caves I) reuse the Basement I/II post-layout tail, or does
it take a distinct branch?

## Answer

**It reuses the same helper.** The tail is the shared end of
`Level::place_post_topology_rooms` (RVA `0x00339370`), slice
`0x0033D1D6..0x0033D94B`. There is no stage-specific dispatch into a distinct
Stage-3 tail. The only stage-dependent control flow in the slice is two
skippable descriptor branches, both inactive at Stage 3 (below).

## Caller / entry evidence

The function `place_post_topology_rooms` begins at VA `0x00739370`
(RVA `0x00339370`). Its prologue (`research/decomp/post_topology_prolog_00739370.tsv`)
loads the stage/stage-type pair from the `Level` object:

```text
0x003393B9  mov edi, [eax + 4]      ; edi = &stage info
0x003393BC  mov edx, edi
0x003393BE  mov esi, [eax]          ; esi = [Level] (stage value holder)
```

and computes the room-config stage:

```text
0x003393DB  mov ecx, esi
0x003393DF  call 0x82d030           ; get_room_config_stage(stage, stageType)
0x003393E7  mov [ebp - 0x128], eax  ; [ebp-0x128] = room-config stage
```

The tail slice is reached unconditionally at `0x0033D182` (`jmp 0x73d1d6`)
after the late ordinary RoomConfig pass; it is not behind a
`level_stage == N` dispatch.

## Stage-dependent branches inside the slice

### `-9` vs `-8` descriptor (room-config stage)

```text
0x0033D5E8  cmp dword ptr [ebp - 0x128], 0xd   ; room-config stage == 13 ?
0x0033D5F6  jne 0x73d645                        ; no  -> assign -8
0x0033D5F8  push -9                             ; yes -> assign -9
```

`[ebp-0x128]` is the room-config stage (4 for Caves I, 1 for Basement, 13 for
Blue Womb). At Stage 3 it is `4`, so the branch assigns `-8` exactly as
Basement I/II do; `-9` is skipped.

### `-10` descriptor (stage-type + level stage)

```text
0x0033D874  mov eax, [edi + 4]     ; stageType
0x0033D877  cmp eax, 4
0x0033D87A  je 0x73d885
0x0033D87C  cmp eax, 5
0x0033D87F  jne 0x73d925           ; stageType not in {4,5} -> skip -10
...
0x0033D885  mov eax, [edi]         ; levelStage
0x0033D887  cmp eax, 8
0x0033D88A  je 0x73d8bf
0x0033D88C  cmp eax, 7
0x0033D88F  jne 0x73d925           ; levelStage not in {7,8} -> skip -10
```

At Stage 3 (`stageType 0`, `levelStage 3`) both conditions fail, so `-10` is
skipped. This matches the recovered `skipped_optional_grid_indices=(-9, -10)`.

## Probability sites (door-chance flag writes)

Two probability sites at `0x0033D2B8` and `0x0033D363` each always consume one
persistent Level `Next` draw. Their optional descriptor-flag write
(`or [descriptor + 0x58], 0x10`) is gated by:

```text
0x0033D2EE  test bl, bl                       ; bl = [ebp-0x130]
0x0033D2F8  mov esi, [ebp - 0x148]            ; descriptor index
0x0033D2FE  test esi, esi
0x0033D300  js 0x73d361                       ; skip if index < 0
```

`[ebp-0x130]` is the achievement-16 door flag (`0x0033D16C..0x0033D17C`), and
`[ebp-0x148]` is the descriptor index loaded from `Level+0x182CC`
(`0x0033C794..0x0033C79A`). Neither is a function of `level_stage`: they depend
on the achievement/unlock profile and the special-room placement, which are
identical across Basement I/II and Caves I in the canonical profile. In that
profile the write is gated off for every stage, and the two draws still occur.

## Consequence for Stage 3

The persistent Level RNG consumption is unchanged:

```text
2 probability draws
+ 6 fixed descriptors * (3 descriptor seeds + 1 selector seed)
+ 1 Shop private-stream seed
+ 1 Angel private-stream seed
= 28 Level RNG draws
```

The eight fixed descriptors (`-2, -6, -4, -5, -7, -8, -13, -18`) and their
private Shop/Angel streams are unconditional and identical to Basement I/II.
The RoomConfig weight mutation and special-room used-bit clearing are part of
this shared slice and therefore also identical.

## Implementation

The clean leaf `src/isaacmap/post_layout_lifecycle.py` now accepts
`level_stage in (1,2,3)` with the matching `room_config_stage`
(1 for Basement, 4 for Caves). `generate_caves1_lifecycle` composes the
accepted-layout pipeline with this shared tail and propagates the Caves pool
(index 4) final RNG state.

Algorithm confidence: `CONFIRMED_BINARY`.

External gameplay fixture status: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.
