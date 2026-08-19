# Basement I post-Treasure condition matrix

Executable profile: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Scope: fresh ordinary vanilla Basement I, ORIGINAL, NORMAL/HARD, canonical
Isaac profile. Algorithm evidence: `CONFIRMED_BINARY`. External validation:
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Input classes

- **A — seed-derived:** continuing Level/LevelGenerator states and chance
  draws. These are replayable from `gameStartSeed` under the profile.
- **B — replayable persistent generation state:** BossPool state,
  RoomConfig mutable weights, special-room used bits and prior attempt/floor
  mutations. Replayable only if the complete generation lifecycle is replayed.
- **C — gameplay/save choice:** health, coins, collectibles, character,
  visited room types, challenge/mode, achievements and unlocks.
- **D — frozen profile constant:** Stage 1, ORIGINAL, ordinary route, no
  challenge/daily/ascent, character 0, no generation-affecting collectibles,
  max hearts 6, full health, zero coins, installed unlock profile, empty
  visited-type state and initially empty special-room used bits.

## Predicates

| Block | Near-binary predicate | Input classes | Frozen-profile result |
|---|---|---|---|
| Planetarium | `not visited(type24/type4) && planetariumUnlocked && f32(Level.Next()) < 0.01` plus resource/candidate availability | A, C, D | Block always executes; assignment seed-dependent. |
| Dice vs Sacrifice | `Level.Next()%50 == 0`, otherwise `Level.Next()%5 == 0 && maxHearts > 1` selects Dice; otherwise Sacrifice | A, C/D | Alternative seed-dependent. |
| Dice/Sac assignment | `Level.Next()%7 == 0 || ((Level.Next()&3)==0 && playerCondition)` | A, C/D | Seed-dependent. |
| Library | subtype `RandomInt(maxSubtype+1)`; assign if `%20==0`, or if `(&3)==0 && usedBit8` | A, B, D | Seed-dependent first arm; used-bit fallback initially false. |
| Curse | compatible type-10 config/end room exists | B, D, resources | Canonical current resources assign the first compatible candidate. |
| MiniBoss subtype | choose from ordered unused subtype/bit pairs `(2,9),(3,10),(1,11),(0,12),(5,13),(6,14)` | A, B | Seed-dependent subtype; successful assignment immediately sets its bit. |
| MiniBoss assignment | `(Level.Next()&3)==0 || (stage==1 && Level.Next()%3==0)` | A, D | Seed-dependent. |
| Challenge assignment | stage thresholds and challenge-room eligibility | C, D | Always false at canonical Stage 1; candidate is re-appended. |
| Chest vs Arcade | `%10==0` selects Chest; otherwise a `%3`/hearts branch can select Chest, else Arcade | A, C/D | Alternative seed-dependent. |
| Chest/Arcade assignment | coin/stage/character and visitation predicate | C, D | Always false for fresh canonical Stage 1. |
| Isaac vs Barren | route/visitation choice, then Isaac `%50==0`; low-health fallback `%5==0` | A, C, D | Isaac selected; assignment seed-dependent. Full-health fallback false. |
| Alternate first-half | alternate-path stage/type predicate | C/D | Always false for Stage 1 ORIGINAL. |
| Alternate second-half | alternate-path half plus collectible 626/state predicate | C/D | Always false. |
| Route-state end room | route-specific state flag | C/D | Always false. |
| Secret count | base 1; player state id `0x66` can make 2; collectible 589 adds one | C, D | Exactly one iteration. |
| Post-Secret end room | `stage == 11 && stageType == ORIGINAL` | D | Always false. |
| Ultra entry | no existing type-29 descriptor and eligible ordinary generation path | B, D | Entry executes; placement result may be null. |
| Late ordinary variants | one compatible concrete config for every collected default generated room | B, resources | Always attempted; resource/weight/door compatibility can reject the attempt. |

## Why skipped blocks remain modeled

The clean and reference M6 traces retain all three pre-Secret route predicates
and the post-Secret Stage-11 predicate even though the frozen profile makes
them false. This prevents the frozen implementation from silently becoming a
different call graph and documents exactly which additional state must be
provided before another profile can be supported.
