# Caves I — ORIGINAL route reconstruction

Frozen executable: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

SHA256: `3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

External gameplay validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

This note covers canonical LevelStage 3 entered from the confirmed Basement-II
generation snapshot. Caves I is `CONFIRMED_BINARY`: floor-init, topology,
BossPool, the full accepted layout, the post-layout lifecycle tail and the
Caves I → Caves II snapshot are all binary-confirmed (20,000-seed
reference/clean differential, zero mismatch).

## Completion summary

**Status: `CONFIRMED_BINARY`** for canonical Caves I NORMAL/HARD with inherited
Basement II lifecycle snapshot.

- Floor-init/topology leaf: `CONFIRMED_BINARY` (10k + 10k reference differential);
- Caves BossPool resume/select leaf: `CONFIRMED_BINARY` (index 4, caves entries);
- Full accepted-layout composition: `CONFIRMED_BINARY` (independent reference);
- Post-layout lifecycle tail: `CONFIRMED_BINARY` (shared `0x0033D1D6..0x0033D94B`);
- Caves I → Caves II snapshot: `CONFIRMED_BINARY`.

See `research/notes/floors/caves1_post_layout_binary_proof.md` and
`research/notes/floors/caves1_predicates_binary_proof.md` for the tail and
blocked/XL evidence.

## Floor entry and natural Labyrinth

The Level RNG is constructed from initial stage-seed slot 3 with shift index
35. `Level::Init` advances it twice, then copies that state into the ordinary
curse/room-count stack RNG. The canonical curse gate denominator is 80 on
NORMAL and 40 on HARD. A successful gate consumes a modulo-six selector.

Unlike even Basement II, odd Stage 3 satisfies the frozen Labyrinth predicate:

- LevelStage is odd and below 8;
- ordinary game mode is neither 2 nor 3;
- the excluded runtime state at `Game+0x26584` is absent.

Selector result 0 therefore retains curse bit `0x02` and makes the floor XL.
Results 1..5 retain Lost, Darkness, Unknown, Maze and Blind as before. The
canonical no-mod curse normalizer remains the identity.

## Topology contract

The shared dungeon formula computes:

```text
base = min(floor(LevelStage * 10 / 3) + 5 + (Level.Next() & 1), 20)
```

For Stage 3 this is 15 or 16. Non-XL Lost adds four. XL instead applies the
frozen binary64 constant 1.8 (`cdccccccccccfc3f`) with truncation and a cap of
45, producing 27 or 28 before the HARD bonus. The copied stack RNG always
advances once; HARD uses its low bit to add `2 + bit`, while NORMAL discards
the value.

Required dead ends are six normally and seven under XL. The ordinary Caves
RoomConfig stage is 4. Difficulty windows are:

| Profile | Non-XL | XL |
|---|---:|---:|
| NORMAL | 1..5 | 1..10 |
| HARD | 5..10 | 5..15 |

The frozen `04.caves.stb` contains ROOM_DEFAULT definitions for Shapes 1..12
in all four windows, so the allowed-shape mask is `0x1FFE`.

The existing clean and mechanical topology implementations already preserve
the binary XL-specific multi-neighbor rule. When a free candidate would link
to at least two rooms, non-XL rejects it; XL consumes the continuing generator
RNG and accepts only when `Next() % 10 == 0`. Static bytes at RVA
`0x005B0768..0x005B07D7` lock the XL/Void flags, modulo-ten draw and zero test.

Static artifact:
`research/binary/caves1_floor_init_binary_verification.json`.

The aggregate clean/reference corpus covers 10,000 NORMAL and 10,000 HARD
start seeds with 20,000/20,000 matches and 11,344,955 generator RNG
transitions. It reaches every curse selector value and every RoomShape 1..12.
Natural XL occurs 27 times on NORMAL and 49 on HARD and consumes 570/1,166
multi-neighbor exception draws respectively. No topology-only outer retry is
needed in this corpus.

Aggregate artifact:
`research/binary/caves1_topology_differential_report.json`.

Status of the isolated floor-init/topology leaf: `CONFIRMED_BINARY`.

## Persistent entry state composition — COMPLETED

Stage 3 starts from `Basement2LifecycleResult.next_run_state` with
`completed_level_stage=2` and `next_level_stage=3`. The full composition:

- inherits all 37 BossPool RNG states and the committed Basement removals;
- initializes the Caves pool (index 4) from `bosspools.xml["caves"]`;
- preserves special/previous-stage mutable RoomConfig state and resets only
  the stage-4 entries;
- reuses the confirmed post-topology leaves (no Stage-3-specific predicates);
- executes the shared post-layout tail (8 fixed descriptors, 28 Level draws,
  Shop/Angel private streams) that reuses the Basement I/II helper;
- commits both bosses/treasures only after all geometry succeeds;
- emits `completed_level_stage=3`, `next_level_stage=4` (Caves II).

Implementation files:

- `src/isaacmap/caves1_full_pipeline.py`: layout composition;
- `src/isaacmap/caves1_full_pipeline_reference.py`: mechanical reference;
- `src/isaacmap/caves1_lifecycle.py`: lifecycle entry point;
- `src/isaacmap/caves1_lifecycle_reference.py`: lifecycle reference;
- `tests/differential/test_caves1_full_pipeline_differential.py`: differential.

Status: Caves I is `CONFIRMED_BINARY`.
