# Post-topology generation call graph

Profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Safety: all addresses below come from static analysis of the copied PE.  The
executable was not run, loaded as a PE module, or used as a runtime oracle.

Algorithm evidence: `CONFIRMED_BINARY` for call order and the stated branches.

External validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Outer generation loop

`Level::generate_dungeon` begins an outer loop at RVA `0x00341760`.  The
important calls are:

1. `LevelGenerator::Generate` at call RVA `0x00341A20`, callee RVA
   `0x005ADBB0`;
2. validate usability and required dead-end count;
3. clear the partial Level room-descriptor array;
4. `Level::place_post_topology_rooms` at call RVA `0x00341B08`, callee RVA
   `0x00339370`;
5. if that call returns zero, call the partial-Level cleanup helper at call
   RVA `0x00341B15` and jump back to `0x00341760`.

This is an output-affecting contract discovered during the M5 differential.
The topology generator object is constructed before this loop.  Therefore a
post-topology failure rejects the just-generated topology and the next attempt
continues the existing generator RNG; it does not recreate the first topology
from the stage seed.  The Level RNG, BossPool state and mutable RoomConfig
weights have also already been consumed/mutated and are preserved by the
implemented full-loop state model.

The full loop is now implemented by the paired
`basement1_pipeline_reference.py` / `basement1_pipeline.py` research paths.
Static analysis of loop-head helper RVA `0x003382C0`, failure cleanup RVA
`0x00338650`, and success commit RVA `0x00021B50` proves that a failure
discards partial topology/descriptors and clears only the attempt blacklist;
Level RNG, LevelGenerator RNG, persistent BossPool pre-rolls and RoomConfig
weight decay continue into the next attempt. See
`research/notes/generation_retry_semantics.md`.

The permanent retry fixtures are NORMAL `0x00000CAE`, NORMAL `0x0000247A`,
HARD `0x000022CD`, plus NORMAL seed 1 for a later Treasure-geometry failure.
The assembled 20,000-seed report is
`research/binary/basement1_pipeline_differential_report.json`.

## Ordinary Basement I order

The following table follows `Level::place_post_topology_rooms` in increasing
instruction order.  A row marked conditional is still part of the real call
graph; it is not necessarily entered by the frozen ordinary Basement I state.

| Order | Operation | Principal call RVAs | Input / mutation | RNG and condition |
|---:|---|---|---|---|
| 1 | Resolve current RoomConfig stage | `0x003393DF` → `0x0042D030` | Level stage/stage type → config-stage id | No draw |
| 2 | Primary Boss identity | `0x00339475` → `0x00022830` | `BossPools` at `Game+0x1AF70`; marks chosen boss in removal/level bitset | Selected persistent BossPool RNG; stage, stage type, character/game mode/unlocks and previous boss state control branches |
| 3 | Primary Boss RoomConfig | `0x003394C3` → `0x00339080` | Concrete type 5 STB entry; mutable RoomConfig weight decay | One Level RNG draw begins at `0x003394A4`; private index-39 selector plus index-7 RoomConfig selector |
| 4 | Primary Boss geometry | `0x003394F2` → `0x005AEF10`; internally `0x005AED50` | Scans ordered generator dead ends, may shrink/re-anchor a large/L dead end, stable-erases selection | No placement RNG on ordinary non-XL path; failure returns zero to the outer loop |
| 5 | Assign Boss descriptor/config | `0x00339528` → `0x00338AB0` | Mutates selected generated room into type 5 and stores config/seed metadata | No new draw at this call boundary |
| 6 | Additional Boss block (conditional) | `0x00339540..0x003398AB` | Stage-specific multi-boss generation | Level RNG; skipped by ordinary Basement I |
| 7 | XL second Boss (conditional) | Boss id call `0x00339926`, config `0x0033997D`, geometry `0x0033999B`, assign `0x003399C7`, link `0x00339A0D` | Second boss and boss-link mutation | Effective XL curse only; may also consume LevelGenerator RNG inside `0x005AEF10` |
| 8 | ROOM_SUPERSECRET / RoomType 8 | state check `0x00339A3E`; config `0x00339B64`; end-room `0x00339B78`; assign `0x00339B8D` | Selects and stable-erases an existing compatible generated dead end, then mutates/re-anchors it | Level RNG draw `0x00339A87`; temporary index-9 stream; count is 1 or 2 if collectible 589 is owned |
| 9 | Capture post-Type8 seed | inline draw `0x00339BE7..0x00339C08` | Advances Level RNG and saves the resulting value in a stack local as a seed snapshot | This snapshot later seeds distinct Secret and Ultra streams; object identity must not be merged with the continuing Level RNG |
| 10 | ROOM_SHOP / type 2 | config `0x0033A205`; end-room `0x0033A219`; assign `0x0033A256` | Stable-erases and mutates the next compatible dead end | Eligibility depends on stage, achievements/unlocks, players, game/challenge state and visit state; concrete config consumes Level/RoomConfig RNG |
| 11 | ROOM_TREASURE / type 4 | probability draw `0x0033A455`; optional draw `0x0033A4B8`; selection draw `0x0033A76B`; config `0x0033A7AD`; end-room `0x0033A7C1`; assign `0x0033A7EA` | Stable-erases/mutates a compatible dead end | Level RNG; stage wrapper may fall back to config stage 0 |
| 12 | ROOM_PLANETARIUM / type 24 (conditional) | config `0x0033A963`; end-room `0x0033A97B` | Candidate-pool mutation if eligible | Level RNG plus unlock/chance/state predicates |
| 13 | ROOM_DICE / type 21 or ROOM_SACRIFICE / type 13 (conditional alternatives) | config calls `0x0033ACC8` / `0x0033AE50`; end-room paths immediately after | Candidate-pool mutation | Level RNG; character, stage and existing-type predicates |
| 14 | ROOM_LIBRARY / type 12 (conditional) | config `0x0033AFF9`; end-room `0x0033B00D` | Candidate-pool mutation | Level RNG and library eligibility |
| 15 | ROOM_CURSE / type 10 (conditional, possibly repeated) | config `0x0033B200` or fallback `0x0033B26D`; end-room `0x0033B287` | Candidate-pool mutation | Dedicated temporary loop seed plus RoomConfig RNG; player state changes count/subtype |
| 16 | ROOM_MINIBOSS / type 6 (conditional) | config `0x0033B8AD` / fallback `0x0033B91A`; end-room `0x0033B940` | Candidate-pool mutation | Level RNG; subtype and difficulty windows are state-dependent |
| 17 | ROOM_CHALLENGE / type 11 (conditional) | config `0x0033BC20`; end-room `0x0033BC34` | Candidate-pool mutation | Level RNG and challenge-room eligibility |
| 18 | ROOM_CHEST / type 20 or ROOM_ARCADE / type 9 selector block (conditional alternatives) | config `0x0033BF13` / `0x0033BFBF`; end-room `0x0033BFD3` | Candidate-pool mutation | Level RNG, stage/chance/unlocks/game state |
| 19 | ROOM_ISAAC / type 18 or ROOM_BARREN / type 19 (conditional alternatives) | config `0x0033C236`; end-room `0x0033C24F`; assign `0x0033C405` | Candidate-pool mutation | Several Level RNG draws and player/state predicates |
| 20 | Route-specific default/end rooms (conditional) | original-stage config `0x0033C498`, end-room `0x0033C4A8`, assign `0x0033C4C2`; alternate wrapper `0x0033C604`, end-room `0x0033C618`, assign `0x0033C631` | Alternate-route candidate mutation | Skipped on the frozen ordinary Basement I main path |
| 21 | ROOM_SECRET / type 7 | config `0x0033C716`; candidate-prep `0x0033C72E`; placement helper `0x0033C741`; assign `0x0033C7B0` | Builds a separate cell candidate container; not `GetNewEndRoom` | Seed snapshot from order 9; a distinct index-1 progression stream for repeated secrets; RoomConfig uses index 7 |
| 22 | Stage-specific post-Secret end room (conditional) | config `0x0033C8CE`; end-room `0x0033C8E2`; assign `0x0033C8FD` | Candidate-pool mutation | Specific stage branch; skipped on ordinary Basement I |
| 23 | ROOM_ULTRASECRET / type 29 | config `0x0033C9CD`; red-grid preparation `0x0033C9EF..0x0033CAB6`; placement helper `0x0033CB05`; assign `0x0033CB1B` | Adds/assigns the ultra-secret descriptor using a separate candidate set | Same seed snapshot as Secret but copied into a distinct index-71 stream; not the same RNG object |
| 24 | Collect all generated rooms | `0x0033CB97` → `0x005AF0E0` | Constructs ordinary-room iteration list | No conclusion that this is RNG-free beyond the helper boundary |
| 25 | Ordinary ROOM_DEFAULT concrete RoomConfig/Variant assignment | selection `0x0033CCDE`; assign `0x0033CD07` inside loop | Assigns each remaining default generated room its concrete STB room | Continuing Level RNG plus per-call index-7 RoomConfig selector |
| 26 | Late fixed/special descriptor configuration | `0x0033CF58..0x0033D925` | Configures fixed negative indices and several stage-specific descriptors | Multiple Level/private streams; outside current implementation slice |

## RoomConfig / RoomVariant position

There is no single late "variant selection" phase:

- each special room selects its concrete STB `RoomConfig_Room` before its
  geometry candidate is accepted (Boss, Type 8, Shop, Treasure, and the later
  special blocks above);
- the remaining ordinary `ROOM_DEFAULT` rooms select their concrete variants
  only after Secret and Ultra, beginning after `collect_rooms` at
  `0x0033CB97`.

Consequently special RoomConfig selection cannot be skipped merely because a
layout-only UI does not display variants.  Its RNG consumption and mutable
weights are upstream of later placement.

## Secret predecessor

The direct code-order predecessor is the pair of conditional route-specific
default/end-room blocks at `0x0033C498..0x0033C631`.  For ordinary main-path
Basement I those predicates are false, so control falls through from the
earlier Isaac/Barren and arcade/chest family blocks to the Secret state check.
