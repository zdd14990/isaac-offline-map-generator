# ALT special-room condition matrix (1+..6+) — reconstruction status

Frozen binary: `Binding of Isaac: Repentance+ v1.9.7.17.J460`, SHA256
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`.
Source: `Level::place_post_topology_rooms` @ 0x739370 (decompiled, 2735
lines). `adjusted_stage = level_stage + 1` for stage_type 4/5, else
level_stage (the same +1 the slot rule uses).

## Legend

- `EXEC` / `SKIP` per (stage_type 4/5) x level 1..6; `D` = draw effect on the
  persistent Level RNG.
- `adj` = adjusted stage. `CONFIRMED` rows are read from the binary;
  `OPEN` rows are the repo's clean-vs-reference-validated ORIGINAL shapes
  whose exact ALT semantics are still being reconstructed.

## Through-Treasure (M5, 0x739370..0x0033A3FF) — CONFIRMED stage_type-independent

| block | RVA | 1+ | 2+ | 3+ | 4+ | 5+ | 6+ | predicate | D |
|---|---|---|---|---|---|---|---|---|---|
| Boss | 0x003394A4 | EXEC | EXEC | EXEC | EXEC | EXEC | **FIXED 89** | level 1-5 pool pick (pool=rcs); level 6 -> fixed boss 89 | config seed + geometry |
| Type8 | 0x00339A87 | EXEC | EXEC | EXEC | EXEC | EXEC | EXEC | unconditional (only a level==10 gate exists) | seed + private draws |
| Shop | 0x00339DB4 | EXEC | EXEC | EXEC | EXEC | EXEC | EXEC | unconditional | seed + subtype draws |
| Treasure | 0x0033A76B | EXEC | EXEC | EXEC | EXEC | EXEC | EXEC | unconditional | snapshot + seed |

## Post-Treasure specials (M6) — adjusted-stage gates CONFIRMED at the sites

| block | RVA | site | predicate (binary) | 1+ | 2+ | 3+ | 4+ | 5+ | 6+ |
|---|---|---|---|---|---|---|---|---|---|
| Planetarium | 0x0033A8F7 | — | gate uses RAW stage (`<7 || (<9 && 0x6e) || ==10`); no +1 | SKIP | SKIP | SKIP | SKIP | SKIP | SKIP |
| Dice/Sacrifice, Library, Curse | 0x0033AB45..0x0033B3A8 | — | no stage_type branch | EXEC | EXEC | EXEC | EXEC | EXEC | EXEC |
| MiniBoss | 0x0033B3A8..0x0033BBAE | 0x73b3ea/0x73b497 | **adjusted-stage threshold**: `adj < 3` floors (Basement I, Downpour) take the direct subtype-vector path; `adj >= 3` floors additionally run the `%10 == 0` + bit-0x20 RNG flow (0x73b4d5..0x73b538). The repo's 20k-validated shape models the ORIGINAL stages; the adj<3/adj>=3 equivalence for ALT is OPEN | EXEC | EXEC | EXEC | EXEC | EXEC | EXEC |
| Challenge | 0x0033BCF5 | 0x73bcff/0x73bd31 | odd-draw: `adj > 2`; even-draw: `full_health && adj > 1` (CONFIRMED; `condition_9beb30` = full health) | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Chest/Arcade | 0x0033BD87..0x0033C0B6 | 0x73bfe7 | assign iff player checks pass AND `adj in {2,4,6,8}`; chest needs `coins <= 1`, arcade needs `hearts >= 5` (canonical: both pass); first clause is a float-bits comparison (effectively no-op) | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Isaac | 0x0033C0F0 | — | `stage < 7` RAW gate + 1/50 | EXEC | EXEC | EXEC | EXEC | EXEC | EXEC |

## Alternate-path blocks (0x0033C416..0x0033C69E) — CONFIRMED

These were modeled as SKIP for the ORIGINAL route in round 1; they FIRE on
the ALT route:

| block | RVA | predicate (binary) | effect | D |
| first-half mandatory end room | 0x0033C416..0x0033C4D1 | `alt_path_first_half_predicate` = stage_type 4/5 AND (stage 2 OR (1 AND Labyrinth)) | places NORMAL room (type 1, variant 13) via GetNewEndRoom + assign; sets the local flag | 1 Level draw + select + geometry |
| second-half collectible-626 room | 0x0033C554..0x0033C640 | `alt_path_second_half_predicate` = stage_type 4/5 AND (stage 4 OR (3 AND Labyrinth)) AND collectible 626 | canonical (no collectible): NO-OP, no draw | 0 (canonical) |
| ORIGINAL third flag | 0x0033C645..0x0033C69E | `condition_74f030` = stage_type NOT 4/5 AND (stage 6 OR (5 AND Labyrinth)) + flag condition | sets the local flag only (canonical ORIGINAL: flag condition false) | 0 (canonical) |

So for the canonical profile: **2+ (Dross) ALWAYS places the mandatory end
room; 1+ (Downpour) XL places it; non-XL Downpour, Mines/Ashpit,
Mausoleum/Gehenna do not.**

## Secret (0x0033C802) / Ultra (0x0033CB20) / late — stage_type-independent (CONFIRMED)

- Secret Room placement: shared helper; the only stage_type branches in the
  region are the Corpse -10 descriptor (level 7/8 — skipped for ALT 1..6) and
  room-type checks (types 5/7/8/10) inside the Ultra neighbor scan.
- Ultra Secret: `PlaceUltraSecretRoom` shared; no stage_type branch.
- Late/default RoomConfig: two stage_type branches exist — (a) 0x73e422:
  ORIGINAL-only achievement-187-gated path (ALT skips the check); (b)
  0x73ea83: stage_type 4/5 AND (stage 4 OR 3+Labyrinth) — a Mines/Ashpit-
  chapter-specific branch. Both are OPEN (exact RNG/assignment effects).

## Post-layout tail

- `-9` (rcs 13) skipped and `-10` (stage_type 4/5 AND level 7/8) skipped for
  ALT 1..6: **28 persistent Level RNG draws**, same sequence as ORIGINAL.

## Blocker for opening ALT floors (precise)

To open even 1+ (Downpour) the OPEN rows above must be reconstructed
exactly: the Challenge gate shape (0x0033BCF5..0x0033BD87), the Chest/Arcade
assignment clauses (0x0033BD87..0x0033C0B6), the super-secret loop
(0x73bc80), and the late branches (0x73e422, 0x73ea83). For 2+ the mandatory
end room (0x0033C416..0x0033C4D1) draw/geometry accounting is additionally
required. Until then every ALT floor stays `UNSUPPORTED — FAIL CLOSED`
per the project discipline (no approximate maps).
