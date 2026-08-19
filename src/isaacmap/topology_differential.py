"""Independent clean/reference differential harness for Milestone 4."""

from __future__ import annotations

from dataclasses import dataclass

from .floor_init import Basement1TopologyInputs
from .rng import IsaacRNG
from .topology import LevelGeneratorResearch, LevelGeneratorRoom
from .topology import TopologyInputs
from .topology_geometry import RoomShape, occupied_cells
from .topology_reference import (
    ReferenceAttempt,
    TopologyReferenceResult,
    generate_basement1_topology_reference,
)


@dataclass(frozen=True)
class CleanRNGState:
    pre_state: int
    post_state: int


class _RecordingRNG:
    def __init__(self, rng: IsaacRNG) -> None:
        self._rng = rng
        self.states: list[CleanRNGState] = []

    @property
    def seed(self) -> int:
        return self._rng.seed

    def next(self) -> int:
        pre_state = self._rng.seed
        post_state = self._rng.next()
        self.states.append(CleanRNGState(pre_state, post_state))
        return post_state


@dataclass(frozen=True)
class CleanTraceResult:
    rooms: tuple[LevelGeneratorRoom, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    non_dead_ends: tuple[int, ...]
    target_room_count: int
    retries: int
    expansion_order: tuple[int, ...]
    final_rng_state: int
    rng_states: tuple[CleanRNGState, ...]
    attempts: tuple[ReferenceAttempt, ...]


@dataclass(frozen=True)
class DifferentialSummary:
    target_room_count: int
    room_count: int
    retries: int
    rng_draw_count: int
    final_rng_state: int
    shapes: tuple[int, ...]
    forced_dead_end_attempts: int


def _run_clean_with_trace(inputs: TopologyInputs) -> CleanTraceResult:
    generator = LevelGeneratorResearch(inputs.generator_seed)
    generator.is_xl = bool(getattr(inputs, "is_xl", False))
    recording_rng = _RecordingRNG(generator.rng)
    generator.rng = recording_rng  # type: ignore[assignment]
    target_count = inputs.target_room_count
    retries = 0
    attempt = 0
    attempts: list[ReferenceAttempt] = []
    while True:
        attempt += 1
        generator.blocked_positions[:] = [False] * len(generator.blocked_positions)
        generator.generate_once(
            target_count=target_count,
            required_dead_ends=inputs.required_dead_ends,
            allowed_shapes=inputs.allowed_shapes_mask,
            start_room=LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        attempts.append(
            ReferenceAttempt(
                attempt=attempt,
                target_room_count=target_count,
                expansion_order=tuple(generator.expansion_order),
                dead_end_order=tuple(generator.dead_ends),
                forced_dead_end_attempts=generator.forced_dead_end_attempts,
                final_rng_state=recording_rng.seed,
            )
        )
        if len(generator.dead_ends) >= inputs.required_dead_ends:
            break
        retries += 1
        if attempt >= 10 and attempt % 5 == 0 and target_count < 64:
            target_count += 1
    return CleanTraceResult(
        rooms=tuple(generator.rooms),
        room_map=tuple(generator.room_map),
        dead_ends=tuple(generator.dead_ends),
        non_dead_ends=tuple(generator.non_dead_ends),
        target_room_count=target_count,
        retries=retries,
        expansion_order=tuple(generator.expansion_order),
        final_rng_state=recording_rng.seed,
        rng_states=tuple(recording_rng.states),
        attempts=tuple(attempts),
    )


def _room_signature_clean(room: LevelGeneratorRoom) -> tuple[object, ...]:
    return (
        room.generation_index,
        (room.column, room.line),
        int(room.shape),
        occupied_cells(room.column, room.line, room.shape),
        room.doors,
        tuple(sorted(room.neighbors)),
        room.origin_neighbor_connect_dir,
        room.origin_neighbor_door_slot,
        room.link_position,
        room.dead_end,
        room.distance_from_start,
    )


def _room_signature_reference(room: object) -> tuple[object, ...]:
    # Attribute access is kept explicit so a reference model change cannot be
    # hidden by sharing a serializer with the clean implementation.
    return (
        room.generation_index,  # type: ignore[attr-defined]
        (room.column, room.line),  # type: ignore[attr-defined]
        room.shape,  # type: ignore[attr-defined]
        room.occupied_cells,  # type: ignore[attr-defined]
        room.doors,  # type: ignore[attr-defined]
        tuple(sorted(room.neighbors)),  # type: ignore[attr-defined]
        room.origin_neighbor_connect_dir,  # type: ignore[attr-defined]
        room.origin_neighbor_door_slot,  # type: ignore[attr-defined]
        room.link_position,  # type: ignore[attr-defined]
        room.dead_end,  # type: ignore[attr-defined]
        room.distance_from_start,  # type: ignore[attr-defined]
    )


def compare_topology_results(
    inputs: TopologyInputs,
    reference: TopologyReferenceResult,
) -> tuple[TopologyReferenceResult, DifferentialSummary]:
    """Assert all structural and generator-RNG dimensions are equal."""

    clean = _run_clean_with_trace(inputs)

    assert clean.target_room_count == reference.target_room_count, "target room count"
    assert clean.room_map == reference.room_map, "occupied GridIndex map"
    assert clean.dead_ends == reference.dead_ends, "dead-end order"
    assert clean.non_dead_ends == reference.non_dead_ends, "non-dead-end order"
    assert clean.retries == reference.retries, "outer retry count"
    assert clean.expansion_order == reference.expansion_order, "expansion order"
    assert clean.attempts == reference.attempts, "per-attempt intermediate states"
    assert clean.final_rng_state == reference.final_rng_state, "final generator RNG state"

    clean_rooms = tuple(_room_signature_clean(room) for room in clean.rooms)
    reference_rooms = tuple(_room_signature_reference(room) for room in reference.rooms)
    assert clean_rooms == reference_rooms, "anchors/shapes/cells/doors/connections"

    clean_rng = tuple((draw.pre_state, draw.post_state) for draw in clean.rng_states)
    reference_rng = tuple(
        (draw.pre_state, draw.post_state) for draw in reference.generator_rng_ledger
    )
    assert clean_rng == reference_rng, "every generator RNG pre/post state"

    return reference, DifferentialSummary(
        target_room_count=reference.target_room_count,
        room_count=len(reference.rooms),
        retries=reference.retries,
        rng_draw_count=len(reference.generator_rng_ledger),
        final_rng_state=reference.final_rng_state,
        shapes=tuple(room.shape for room in reference.rooms),
        forced_dead_end_attempts=reference.coverage.forced_dead_end_attempts,
    )


def compare_clean_and_reference(
    inputs: Basement1TopologyInputs,
) -> tuple[TopologyReferenceResult, DifferentialSummary]:
    """Compatibility comparator for the verified Basement I entry ledger."""

    return compare_topology_results(
        inputs, generate_basement1_topology_reference(inputs)
    )
