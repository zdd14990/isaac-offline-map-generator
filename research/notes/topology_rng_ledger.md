# LevelGenerator topology RNG consumption ledger

Executable SHA-256:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Scope: the frozen ordinary Basement I topology path through the end of
`LevelGenerator::Generate`.  Special-room selection functions are deliberately
outside this milestone.

## Runtime ledger schema

`src/isaacmap/topology_reference.py` emits one `RNGDraw` for every dynamic draw:

```text
sequence
binary_rva / binary_range
rng_object
shift_index / shifts
pre_state / post_state
control_flow_reason
result_usage
attempt / source_room / door_slot / candidate_index
```

The frozen Level and LevelGenerator streams use shift index 35, triple
`(5,9,7)`.  The reference performs the x86 operations mechanically and the
clean differential recorder independently observes the existing `IsaacRNG`.
Every clean `(pre,post)` pair must equal the corresponding reference row.

## Entry draws for challenge-free Basement I

| Dynamic row | RVA/range | RNG object | Reason and use |
|---|---|---|---|
| L1 | `0x00344C1E..0x00344C42` | `Level._generationRNG` | first `Level::Init` progression |
| L2 | `0x00344CAA..0x00344CCE` | `Level._generationRNG` | second progression; state copied afterward |
| C-gate | call `0x00344F09` | stack copy made after L2 | ordinary curse `RandomInt(rate)`; always consumed on the canonical run-start path |
| C-selector | `0x00344F34..0x00344F56` | same stack copy | optional `Next()%6` when the gate succeeds |
| L3 | `0x00340E8E..0x00340EB8` | `Level._generationRNG` | low bit contributes to base target count |
| C-difficulty | `0x0034109F..0x003410C0` | same stack copy | unconditional advance; low bit supplies HARD `2+bit` and is discarded on NORMAL |
| L4 | `0x00341202..0x0034122D` | `Level._generationRNG` | seed passed to `LevelGenerator` constructor |

For start seed 1 the complete entry ledger is:

| Row | Pre | Post |
|---|---:|---:|
| L1 | `0x00100001` | `0x2152A305` |
| L2 | `0x2152A305` | `0x91146405` |
| L3 | `0x91146405` | `0xAD4AA83F` |
| C-gate | `0x91146405` | `0xAD4AA83F` |
| C-difficulty | `0xAD4AA83F` | `0xE809B57C` |
| L4 | `0xAD4AA83F` | `0xE809B57C` |

L3 and C-gate match because both streams start from L2. The failed gate still
advances the copied stream, so C-difficulty equals L4 rather than L3.

## Conditional pre-generator draws

These are statically proved but are not taken by the frozen state contract:

| RVA/range | RNG object | Condition | Use |
|---|---|---|---|
| `0x00340FCC..0x00340FF9` | Level RNG | challenge 21 | `40 + Next()%5` target override |
| `0x0034103B..0x00341066` | Level RNG | stage 12 | `50 + Next()%5` target override |

These rows explain why arbitrary challenge/curse state cannot reuse the simple
fresh Basement I entry sequence.

## LevelGenerator draw sites

The following table is exhaustive for topology generation at RVAs
`0x005ADBB0`, `0x005B04D0`, `0x005B0B00`, `0x005B1B20` and the forced-dead-end
path.

| RVA/range | Multiplicity and branch | Result use |
|---|---|---|
| `0x005B1030..0x005B104B` | 13 draws for every valid/free neighbor door target; retained under force override | candidate gate `Next()%{48,24,24,24,24,72,72,36,36,36,36,24,24}` |
| `0x005B1B8F..0x005B1BAA` | `candidateCount-1` draws per ordinary expanded source; none in force helper | Fisher-Yates swap index |
| `0x005B05F0..0x005B060E` | one for start when target `<16`; none when target `>=16` | `wanted=2+(Next()&1)` |
| `0x005B063A..0x005B0657` | non-start draw 1/4 | low-bit fanout sum |
| `0x005B0679..0x005B0696` | non-start draw 2/4 | low-bit fanout sum |
| `0x005B06B8..0x005B06D5` | non-start draw 3/4 | low-bit fanout sum |
| `0x005B06F4..0x005B0715` | non-start draw 4/4 | low-bit fanout sum |
| `0x005B07AA..0x005B07CC` | only when neighbor links `>=2` and XL or Void is true | accept exception when `Next()%10==0` |
| `0x005B0815..0x005B0837` | one after every successful ordinary placement | push expansion index back on `%3==0`, otherwise front |

`classify_dead_ends`, connection rebuilding and dead-end sorting consume no
RNG.  `force_new_dead_end` consumes only the candidate-gate rows above: it does
not shuffle, does not call placement-validity, and does not consume a queue-side
draw after placement.

The outer retry loop never reconstructs or reseeds `LevelGenerator`; the same
`LevelGenerator._rng` state continues into the next attempt.  The final ledger
post-state is asserted equal to the returned final generator state.

## Differential coverage

`research/binary/topology_differential_report.json` records 20,000 comparisons
(start seeds 1..10,000 for both NORMAL and HARD):

- 7,285,534 individual generator RNG `(pre,post)` pairs compared;
- all Shapes 1..12 placed, including all four L shapes;
- 6,235,996 large-candidate gate draws, containing both successes and failures;
- 13,159 forced-dead-end attempts, all traced at the same candidate RNG site;
- final RNG state equal for every case.

No natural standard Basement I outer retry appeared in this corpus.  A targeted
branch fixture with seed 290 and `requiredDeadEnds=6` (not a standard Basement I
parameter claim) makes attempt 1 exhaust all five force tries and attempt 2
succeed; both implementations agree on every draw and retry state.

## Persisted complete examples

`scripts/export_topology_rng_ledger.py` hash-checks the copied PE before
exporting every ledger row.  The committed development artifacts for internal
start seed 1 contain:

- NORMAL: 5 entry rows, 389 generator rows, final state `0xE58FE5EC`;
- HARD: 5 entry rows, 499 generator rows, final state `0x673E2228`.

They are stored as
`research/binary/topology_rng_ledger_seed_00000001_normal.json` and
`research/binary/topology_rng_ledger_seed_00000001_hard.json`.
