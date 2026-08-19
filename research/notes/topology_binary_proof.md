# Basement I topology binary proof

Executable SHA-256:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Evidence dimension: `CONFIRMED_BINARY`.

Gameplay-fixture dimension: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

Those dimensions are independent.  The lack of a public, version-qualified
gameplay fixture does not weaken a complete static control-flow proof, and the
static proof is not presented as a captured gameplay comparison.

## Recovered function family

| Function | RVA | Proof role |
|---|---:|---|
| `Level::Init` | `0x00344940` | stage slot, Level RNG, curses, generator routing |
| ordinary `Level::generate_dungeon` | `0x00340E10` | target/dead-end/room-pool inputs and outer retry |
| `LevelGenerator` constructor | `0x005ADAF0` | RNG state, maps, blocked cells |
| `LevelGenerator::Generate` | `0x005ADBB0` | resets, expansion, force loop, dead-end selection sort |
| `generate_rooms` | `0x005B04D0` | queue expansion and placement loop |
| `get_neighbor_candidates` | `0x005B0B00` | 1x1 and 13 ordered large candidates per door |
| candidate shuffle | `0x005B1B20` | exact Fisher-Yates order |
| position/free/valid/place helpers | `0x005AFD70`, `0x005B0180..0x005B0330` | boundary, occupancy and door compatibility |
| door/shape/offset helpers | `0x005AF370..0x005B0180` | all Shape and L-room geometry |
| connection rebuild | `0x005AF980` | door masks and neighbor sets |
| mark/classify dead ends | `0x005AFB10`, `0x005AFC70` | two-pass dead-end logic |
| force new dead end | `0x005AF1E0` | unshuffled first-valid correction path |

All decompilations are stored under `research/decomp/ghidra/`.  Raw Capstone
disassembly was used to resolve draw addresses, inline xorshift sequences,
tables and a Ghidra logger `noreturn` misclassification.

## Proven control flow

The mechanical implementation is
`src/isaacmap/topology_reference.py`.  It intentionally duplicates the binary
tables and preserves while-loop/branch order.  It does not call the clean
geometry helpers.

The readable implementation remains `src/isaacmap/topology.py`.  Differential
testing found and corrected two high-level transformations that were not
binary-equivalent:

1. outer target escalation must occur after failed attempts 10, 15, 20, ...;
   the earlier clean counter was one attempt late;
2. dead ends use in-place descending selection sort at
   `0x005ADCA9..0x005ADD20`; Python's stable sort produced a different order
   for equal distances after earlier swaps.

The reference and clean versions now compare:

- initial/final target count and per-attempt targets;
- room generation indices and anchors;
- RoomShape and every occupied cell;
- full 169-entry room map;
- door masks and connection sets;
- expansion-source order;
- dead-end and non-dead-end order;
- forced-dead-end and outer retry counts;
- every LevelGenerator RNG pre/post state;
- per-attempt and final generator RNG state.

## Geometry and RoomShape proof

The executable dimension table at RVA `0x0085D378`, direction table at
`0x0085D3E0`, placement-offset function at `0x005AFDB0`, door-source function
at `0x005AF3F0` and door-target function at `0x005AF620` cover Shapes 1..12,
including the four distinct L tables.  The allowed-shape source pool for both
Basement I difficulty windows was indexed from the installed resources and
contains every Shape 1..12, yielding mask `0x1FFE`.

The static constant verifier is
`research/binary/topology_binary_verification.json`.

## Connection and dead-end proof

`update_room_connections` clears each room's door mask and neighbor set, scans
door slots 0..7, computes the target with normal thin-room restrictions and
adds the mapped room index when occupied.

`mark_dead_ends` first marks every non-start room whose canonical link cell has
fewer than two distinct cardinal neighbor room IDs.  Its second pass follows
each room's stored origin direction and clears the parent room's dead-end flag.
`classify_dead_ends` rebuilds connections and appends room indices in generation
order before `Generate` applies its exact selection sort.

If the required count is short, `Generate` calls `force_new_dead_end` at most
five times.  Each call scans generation-order rooms and unshuffled candidates,
retains all 13 gate draws per usable door, ignores the random result, and
places the first free candidate with fewer than two links.  It deliberately
does not call `is_placement_valid` and consumes no post-placement queue draw.

## RNG proof

The exhaustive static/dynamic draw-site ledger is
`research/notes/topology_rng_ledger.md`.  For 20,000 NORMAL/HARD cases, the
independent clean recorder matched 7,285,534 reference `(pre,post)` transitions
and every final state.  The draw shift index is 35 (`5,9,7`) throughout the
scoped generator and retry stream.

## Isolated instruction emulation

`scripts/emulate_topology_helpers.py` copies exact leaf-function bytes into
Unicorn-owned x86 memory.  It never invokes the Windows loader, PE entry point,
imports or game loop and never creates a target process.

`research/binary/topology_instruction_emulation.json` records:

- `canonical_grid_index` RVA `0x005AFD70`: 289/289 boundary cases match;
- `has_shape_slot` RVA `0x005AF370`: 192/192 shape/slot/restriction cases match.

Whole-`Generate` instruction emulation is feasible in principle but currently
has high isolation cost: MSVC vector/deque/set helpers, allocation, SEH/TLS,
security cookies, logger and global-data dependencies all require deterministic
stubs.  This is recorded as `HIGH_ISOLATION_COST_NOT_BLOCKING_STATIC_PROOF`, not
as a generator blocker and not as an external gameplay oracle.

## Status by Milestone 4 acceptance item

| Item | Binary status | External gameplay status |
|---|---|---|
| geometry | `CONFIRMED_BINARY` | not externally validated |
| RoomShape | `CONFIRMED_BINARY` | not externally validated |
| connection logic | `CONFIRMED_BINARY` | not externally validated |
| retry logic | `CONFIRMED_BINARY` | not externally validated |
| dead-end logic/order | `CONFIRMED_BINARY` | not externally validated |
| RNG consumption | `CONFIRMED_BINARY` | not externally validated |
| final generator RNG state | `CONFIRMED_BINARY` | not externally validated |

This completes Milestone 4 only for the frozen input contract in
`topology_inputs.md`.  This work does not enter Boss, Secret, Super Secret or
Ultra Secret placement, and it does not widen exact support to challenges,
daily runs, XL, alternate routes or mutated stage state.
