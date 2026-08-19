# Late ordinary RoomConfig binary proof

Frozen executable SHA256:
`3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b`

Status: `CONFIRMED_BINARY` for canonical fresh Basement I NORMAL/HARD.
External gameplay validation: `NOT_EXTERNALLY_VALIDATED_GAMEPLAY`.

## Static anchors

The verified caller slice is RVA `0x0033CB5D`, size 966, SHA256
`edccc3e8e941a1c5b9759ad1f145b55e5305db7653a5e0cb9b132f9e342cb8ed`.
The verified `collect_rooms` slice is RVA `0x005AF0E0`, size 254, SHA256
`34bf078b58f329e1aea931d7b5cf65712fce754b78729e0c91c4ae2fc4137b77`.

Static instruction checks pin:

- collection call `0x0033CB97 -> 0x005AF0E0`;
- non-dead-end vector `+0x37c` before dead-end vector `+0x370`;
- Start lookup and fixed variant 2;
- pre-draw HARD minimum gate;
- final GeneratedRoom shape and door-mask inputs;
- Level RNG draw at `0x0033CCA5`;
- direct RoomConfig selector at `0x0033CCDE`, ROOM_DEFAULT and reduce-weight;
- descriptor assignment at `0x0033CD07`;
- excluded-room RNG advance at `0x0033CDD2`;
- selector-null branch and false return at `0x0033CF06`.

The machine-readable result is
`research/binary/late_room_config_binary_verification.json` and is reproduced
by `scripts/verify_late_room_config_binary.py`. It reads the copied PE only as
bytes and never loads or executes it.

## Independent implementations

The clean leaf is `src/isaacmap/late_room_config.py`. The mechanical reference
is `src/isaacmap/late_room_config_reference.py`; it does not call the clean
assignment function. `late_room_config_differential.py` compares collection,
every query/selection, weights, RNG transitions, assignments, failure room,
descriptors and final states.

Unit coverage includes all 12 RoomShapes, both difficulties, fixed Start,
pre-draw HARD lowering, exact-door selection, excluded-special advances and a
forced missing-config failure. The accepted-pipeline mass corpus adds 20,000
natural complete passes with 126,493 ordinary assignments.

## Scope boundary

This proof establishes every ordinary config used by the accepted canonical
Basement I 13x13 layout and the false/retry edge. It does not establish the
successful post-layout negative-GridIndex descriptor tail used to carry
persistent generation state into later floors.
