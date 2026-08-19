# ALT floor-init matrix (1+..6+) — BINARY-CONFIRMED

Frozen binary: `Binding of Isaac: Repentance+ v1.9.7.17.J460`, SHA256
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`.
Source function: `Level__generate_dungeon` @ 0x740e10 (disassembly read
line-by-line; RVAs below are VAs).

## Per-floor matrix

```text
Token  Level StageType SeedSlot RCS TargetN TargetH  XL?  XLTarget  DeadEnds  DiffN   DiffH   BossPool  Boss
1+     1    4        2        27  8/9    10/12*    yes  9/10*     5 (7 XL)  1..5    5..10   27        pool pick
2+     2    5        3        28  8/9    10/12*    no   -        7         5..10   10..15  28        pool pick
3+     3    4        4        29  15/16  17/19*    yes  21/23*    6 (8 XL)  1..5    5..10   29        pool pick
4+     4    5        5        30  15/16  17/19*    no   -        7         5..10   10..15  30        pool pick
5+     5    4        6        31  20     22/23*    yes  36       6 (7 XL)  1..5    5..10   31        pool pick
6+     6    5        7        32  20     22/23*    no   -        6         5..10   10..15  32        FIXED 89
```

*HARD target = NORMAL base + 2 + (rng&1); XL target = min((base-3)*1.8, 45)
for stages 1/3 (which carry the -3), min(base*1.8,45) for stage 5.

## Formulas (from generate_dungeon, all CONFIRMED_BINARY)

1. **Base target** (0x740ec1-0x740ee0):
   `target = min(floor(stage*10/3) + 5 + (LevelRNG&1), 20)`.
   Stage 1 -> 8/9; 2 -> 11/12; 3 -> 15/16; 4 -> 18/19; 5 -> 20; 6 -> 20.
2. **ALT -3 modifier** (0x740eec-0x740f0f): if `[Level+4]` (stage_type) is
   4 or 5 AND (`second_half` OR `first_half` predicate): `target -= 3`.
   Predicates (0x74ef70/0x74efd0): stage 2/4 unconditional; stage 1/3 only
   when the Labyrinth curse (bit 2) is active. Stages 5/6 never.
3. **XL** (0x740f35-0x740f5b, const 0xbaa628 = 1.8): if Labyrinth bit 2:
   `target = min(target * 1.8, 45)`. So 1+ XL = min((8/9-3)*1.8,45) = 9/10;
   3+ XL = min((15/16-3)*1.8,45) = 21/23; 5+ XL = min(20*1.8,45) = 36.
4. **Lost curse** (0x740f89-0x740f8d): bit 4 -> `target += 4` (non-XL only).
5. **HARD** (0x7410c5-0x7410de): game mode 1 (`Game+0x269c8`) ->
   `target += 2 + (LevelRNG&1)`.
6. **Dead ends** (0x74112c-0x7411d8):
   `dead_ends = (stage != 1) + 5`; XL -> `(stage != 1) + 6`; the
   `[Game+0x1baa8 / achievement-ish 0x257]` check adds +1 (returns 0 in the
   canonical profile — proven by the MAIN 20k corpus where dead_ends is
   binary-confirmed as `(stage!=1)+5`); the first/second-half predicates add
   +1 for ALT stages 1-4 (stages 2/4 always, 1/3 only when XL).
   Final: 1+ -> 5 (XL 7); 2+ -> 7; 3+ -> 6 (XL 8); 4+ -> 7; 5+ -> 6 (XL 7);
   6+ -> 6.
7. **Difficulty window** (0x741275-0x741324), stage < 9 non-XL:
   even stage -> NORMAL (5,10) / HARD (10,15); odd stage -> NORMAL (1,5) /
   HARD (5,10). XL or stage >= 9 -> NORMAL (1,10) / HARD (5,15).
8. **Labyrinth/XL eligibility** (`Level__can_apply_labyrinth` 0x7385c0):
   stage odd (`stage & 1`) AND stage < 8 AND game mode not 2/3. So stages
   1/3/5 can be XL, 2/4/6 never.
9. **Stage-seed slot** (Level::Init 0x744940): stage + 1 for stage_type 4/5,
   capped at 13 -> slots 2..7 for 1+..6+.
10. **Boss** (select_boss_id 0x422830): levels 1-5 weighted pool pick from
    pool = rcs (27..31); level 6 FIXED boss 89 (Mom-Mausoleum), pool 32 RNG
    untouched. See `alt_route_stage_type_lifecycle.md`.

## Unchanged vs ORIGINAL (parameterized, not duplicated)

- Topology engine: 13x13 grid, start GridIndex 84 (room 6,6 shape 1x1),
  shape mask = ALL_GENERATED_ROOM_SHAPES_MASK (0x1FFE, dynamic in the
  binary from the loaded room set + curse cleanup), large-room candidates,
  branch expansion, blocked rules — all identical to the ORIGINAL route
  (`generate_dungeon` passes only target/dead_ends/shapes/start).
- RoomConfig weights init (`0x82ce40` + `Game+0x18910`), per-stage
  pre-warm loop 1..17.
- Post-layout tail: 28 persistent Level RNG draws (the -9/-10 branches are
  skipped: rcs 27..32 != 13, level_stage 1..6 not in (7,8)).

## Open / to verify during implementation

- `0x9be080` (dead-end +1 check): identity unconfirmed, but provably 0 for
  the canonical profile (MAIN corpus).
- The `[Game+0x1baa8, 0x257]` flag semantics beyond canonical.
