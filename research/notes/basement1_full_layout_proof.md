# Basement I accepted-layout proof

Frozen executable SHA256:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Status: `CONFIRMED_BINARY` for the canonical fresh ordinary vanilla profile,
Basement I / ORIGINAL, NORMAL and HARD. External gameplay validation remains
`NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Accepted transaction

`src/isaacmap/basement1_full_pipeline.py` owns only the outer transaction. It
composes the existing clean confirmed leaves in binary order:

```text
topology -> Boss -> Super Secret -> Shop -> Treasure
-> canonical conditional specials -> Secret -> Ultra Secret
-> late ordinary RoomConfig assignment -> accept/commit
```

Persistent Level/LevelGenerator/BossPool RNGs, RoomConfig weights, special
used bits and target-count/retry state survive a failed attempt. Per-attempt
descriptors and blacklist are discarded. The BossPool blacklist is committed
only after the late pass succeeds. UI and export adapters use only that final
accepted descriptor/map collection.

## Differential corpus

`research/binary/basement1_full_differential_report.json` records independent
clean/reference equality for start seeds 1..10,000 in each difficulty:

| Difficulty | Comparisons | Attempts | Retrying seeds | Late assignments | Ultra null |
|---|---:|---:|---:|---:|---:|
| NORMAL | 10,000 | 10,785 | 740 | 55,127 | 2 |
| HARD | 10,000 | 10,741 | 693 | 71,366 | 0 |

All 20,000 comparisons match. The corpus includes 1,433 retrying seeds, a
maximum of four attempts, three Boss-geometry aborts and 1,523
Treasure-geometry aborts. The differential compares every attempt's complete
topology and post-topology leaves, RNG states, RoomConfig mutations,
descriptors, room map, Secret/Ultra geometry, late selections and final
BossPool commit boundary.

No natural late missing-config failure occurred in this frozen resource
corpus; directed leaf and outer-transaction fixtures cover the binary false
edge. The final project suite is 223 passing tests.

## Boundary for later floors

The returned map is the complete accepted canonical Basement I 13x13 layout.
After acceptance, the binary constructs several fixed negative-GridIndex
descriptors and consumes additional persistent state before returning. Those
objects do not alter the displayed 13x13 layout or acceptance decision, but
the tail must be recovered before Basement II replay. Stage 2+ therefore
remains `UNSUPPORTED — FAIL CLOSED`.
