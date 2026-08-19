"""Clean Basement I pipeline through Treasure, stopping before Secret.

The entry point remains research-only.  It models the outer generation loop
as a transaction with explicitly non-transactional RNG/weight owners.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path

from .boss_pool import (
    BossPoolEntry,
    BossPoolRuntimeSelection,
    BossPoolRuntimeState,
)
from .floor_init import Basement1TopologyInputs, derive_basement1_topology_inputs
from .generation_state import (
    CanonicalBasement1Profile,
    CanonicalBasement2Profile,
    CanonicalCaves1Profile,
    FloorGenerationState,
    RunGenerationState,
)
from .resources import RoomDefinition
from .rng import IsaacRNG
from .room_config import (
    RoomConfigEntry,
    RoomConfigKey,
    RoomConfigMutableState,
    RoomConfigQuery,
    RoomConfigSelection,
    entries_from_definitions,
    select_room,
    select_room_with_stage_fallback,
)
from .special_rooms import CandidateTrace, GeneratedRoom, PostTopologyState
from .special_room_geometry import EndRoomGeometryEvent, reshape_end_room
from .topology import LevelGeneratorResearch, LevelGeneratorRoom, TopologyResearchResult
from .topology_geometry import DIRECTION_OFFSETS, GRID_HEIGHT, GRID_WIDTH, RoomShape


LEVEL_SHIFT_INDEX = 35
BOSS_CONFIG_SHIFT_INDEX = 39
TYPE8_SHIFT_INDEX = 9
SHOP_PRIVATE_SHIFT_INDEX = 19


@dataclass(frozen=True)
class PipelineRNGDraw:
    binary_rva: int
    object_identity: str
    shift_index: int
    pre_state: int
    post_state: int
    reason: str
    usage: str


@dataclass(frozen=True)
class ConditionTrace:
    binary_range: str
    condition: str
    value: bool
    consequence: str


@dataclass(frozen=True)
class ConfigTrace:
    operation: str
    stages_tried: tuple[int, ...]
    selections: tuple[RoomConfigSelection, ...]


@dataclass(frozen=True)
class PostTopologyAttemptResult:
    completed: bool
    abort_operation: str | None
    boss_selection: BossPoolRuntimeSelection
    boss_room: int
    boss_config: RoomConfigKey | None
    type8_rooms: tuple[int, ...]
    shop_room: int
    shop_config: RoomConfigKey | None
    treasure_room: int
    treasure_config: RoomConfigKey | None
    post_type8_seed_snapshot: int
    rooms: tuple[GeneratedRoom, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    rng_draws: tuple[PipelineRNGDraw, ...]
    config_traces: tuple[ConfigTrace, ...]
    candidate_traces: tuple[CandidateTrace, ...]
    geometry_traces: tuple[EndRoomGeometryEvent, ...]
    conditions: tuple[ConditionTrace, ...]
    additional_boss_selections: tuple[BossPoolRuntimeSelection, ...] = ()
    additional_boss_rooms: tuple[int, ...] = ()
    additional_boss_configs: tuple[RoomConfigKey, ...] = ()
    treasure_rooms: tuple[int, ...] = ()
    treasure_configs: tuple[RoomConfigKey, ...] = ()


@dataclass(frozen=True)
class GenerationAttemptResult:
    attempt: int
    target_room_count: int
    topology_usable: bool
    topology: TopologyResearchResult
    start_level_rng_state: int
    end_level_rng_state: int
    start_generator_rng_state: int
    end_generator_rng_state: int
    start_boss_pool_state: int
    end_boss_pool_state: int
    level_blacklist_after: tuple[int, ...]
    permanent_removed_after: tuple[int, ...]
    room_config_mutations: tuple[tuple[RoomConfigKey, float, float], ...]
    post_topology: PostTopologyAttemptResult | None


@dataclass(frozen=True)
class Basement1ThroughTreasureResult:
    completed: bool
    start_seed: int
    difficulty: str
    stage_seed: int
    attempts: tuple[GenerationAttemptResult, ...]
    final_level_rng_state: int
    final_generator_rng_state: int
    final_boss_pool_state: int
    permanent_removed_bosses: tuple[int, ...]
    final_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    rooms: tuple[GeneratedRoom, ...]


def _topology_snapshot(generator: LevelGeneratorResearch, target: int) -> TopologyResearchResult:
    return TopologyResearchResult(
        rooms=tuple(replace(room, neighbors=set(room.neighbors)) for room in generator.rooms),
        room_map=tuple(generator.room_map),
        dead_ends=tuple(generator.dead_ends),
        non_dead_ends=tuple(generator.non_dead_ends),
        target_room_count=target,
        retries=0,
        final_rng_seed=generator.rng.seed,
        expansion_order=tuple(generator.expansion_order),
        forced_dead_end_attempts=generator.forced_dead_end_attempts,
    )


def _state_from_generator(generator: LevelGeneratorResearch, level_rng: IsaacRNG) -> PostTopologyState:
    state = PostTopologyState(
        rooms=[
            GeneratedRoom(
                room.generation_index, room.column, room.line, room.shape,
                room.origin_neighbor_connect_dir, room.link_column, room.link_line,
                room.distance_from_start, room.doors, set(room.neighbors),
            ) for room in generator.rooms
        ],
        room_map=list(generator.room_map), dead_ends=list(generator.dead_ends),
        level_rng=level_rng,
    )
    return state


def _draw(
    rng: IsaacRNG, ledger: list[PipelineRNGDraw], *, rva: int,
    identity: str, shift_index: int, reason: str, usage: str,
) -> int:
    pre = rng.seed
    post = rng.next()
    ledger.append(PipelineRNGDraw(rva, identity, shift_index, pre, post, reason, usage))
    return post


def _append_config_draws(
    ledger: list[PipelineRNGDraw], operation: str,
    selections: tuple[RoomConfigSelection, ...],
) -> None:
    for selection in selections:
        for draw in selection.draws:
            ledger.append(PipelineRNGDraw(
                draw.binary_rva,
                f"RoomConfig::select_room.local({operation})",
                7, draw.pre_state, draw.post_state, draw.reason,
                "concrete STB RoomConfig weighted choice",
            ))


def _consume_end_room(
    state: PostTopologyState, entry: RoomConfigEntry, operation: str,
    *, minimum_distance: int | None = None,
) -> int:
    original = tuple(state.dead_ends)
    position = 0
    while position < len(state.dead_ends):
        room_id = state.dead_ends[position]
        accepted = (
            (minimum_distance is None or state.rooms[room_id].distance_from_start > minimum_distance)
            and reshape_end_room(
                state, room_id, entry.shape, entry.door_mask,
                events=state.geometry_trace,
            )
        )
        after = tuple(
            state.dead_ends[:position] + state.dead_ends[position + 1:]
            if accepted else state.dead_ends
        )
        state.candidate_trace.append(CandidateTrace(operation, original, room_id, accepted, after))
        if accepted:
            del state.dead_ends[position]
            return room_id
        position += 1
    return -1


def _assign(state: PostTopologyState, room_id: int, entry: RoomConfigEntry) -> None:
    room = state.rooms[room_id]
    room.room_type = entry.room_type
    room.variant = entry.variant
    room.subtype = entry.subtype


def _select_boss_config(
    state: PostTopologyState,
    *,
    selection: BossPoolRuntimeSelection,
    entries: tuple[RoomConfigEntry, ...],
    run_state: RunGenerationState,
    ledger: list[PipelineRNGDraw],
    config_traces: list[ConfigTrace],
    operation: str,
    seed_rva: int,
) -> RoomConfigEntry | None:
    boss_seed = _draw(
        state.level_rng,
        ledger,
        rva=seed_rva,
        identity="Level._generationRNG",
        shift_index=35,
        reason=f"{operation} RoomConfig",
        usage="seed private index-39 stream",
    )
    private = IsaacRNG.game_constructor(boss_seed, BOSS_CONFIG_SHIFT_INDEX)
    retries_left = 50
    while True:
        selector_seed = _draw(
            private,
            ledger,
            rva=0x0033930E,
            identity=f"{operation} RoomConfig.private",
            shift_index=39,
            reason=f"{operation} config iteration",
            usage="RoomConfig selector seed",
        )
        selected = select_room(
            entries,
            run_state.room_config,
            RoomConfigQuery(
                selector_seed,
                True,
                0,
                5,
                subtype=abs(selection.boss_id),
            ),
        )
        config_traces.append(ConfigTrace(operation, (0,), (selected,)))
        _append_config_draws(ledger, operation, (selected,))
        entry = selected.entry
        if entry is None:
            return None
        if not (3700 <= entry.variant < 3850) or retries_left <= 0:
            return entry
        retries_left -= 1


def _sync_generator_from_post_state(
    generator: LevelGeneratorResearch,
    state: PostTopologyState,
) -> None:
    """Project the shared descriptor geometry back onto LevelGenerator.

    The binary has one mutable generator object.  The earlier non-XL clean
    leaf keeps a presentation-friendly descriptor snapshot, so the XL-only
    extra-boss branch explicitly resynchronizes that snapshot before calling
    the already recovered candidate/shuffle/place implementation.
    """

    dead_ends = set(state.dead_ends)
    generator.rooms = [
        LevelGeneratorRoom(
            room.column,
            room.line,
            room.shape,
            generation_index=room.generation_index,
            doors=room.doors,
            origin_neighbor_connect_dir=room.origin_direction,
            origin_neighbor_door_slot=room.origin_direction,
            link_column=room.link_column,
            link_line=room.link_line,
            neighbors=set(room.neighbors),
            dead_end=room.generation_index in dead_ends,
            distance_from_start=room.distance_from_start,
        )
        for room in state.rooms
    ]
    generator.room_map[:] = state.room_map
    generator.dead_ends[:] = state.dead_ends


def _prepare_xl_extra_boss_room(
    state: PostTopologyState,
    generator: LevelGeneratorResearch,
    primary_room: int,
    required_doors: int,
) -> int:
    """Port the XL-only extra-room arm of RVA 0x005AEF10."""

    _sync_generator_from_post_state(generator, state)
    generator.num_boss_rooms = 1
    candidates = generator.get_neighbor_candidates(primary_room)
    generator.shuffle_candidates(candidates)
    pending = -1
    for candidate in candidates:
        position = (candidate.column, candidate.line)
        if not generator.is_pos_free(position, candidate.shape):
            continue
        if generator.count_neighbor_links(candidate.link_position) >= 2:
            continue
        if required_doors & (1 << candidate.origin_neighbor_door_slot) == 0:
            continue
        placed = generator.place_room(candidate)
        placed.dead_end = True
        pending = placed.generation_index
        generator.next_boss_room_index = pending
        break

    for room in generator.rooms:
        generator.update_room_connections(room)
    for room_id, room in enumerate(state.rooms):
        room.doors = generator.rooms[room_id].doors
        room.neighbors = set(generator.rooms[room_id].neighbors)
    if pending >= 0:
        placed = generator.rooms[pending]
        state.rooms.append(
            GeneratedRoom(
                placed.generation_index,
                placed.column,
                placed.line,
                placed.shape,
                placed.origin_neighbor_connect_dir,
                placed.link_column,
                placed.link_line,
                placed.distance_from_start,
                placed.doors,
                set(placed.neighbors),
            )
        )
        state.room_map[:] = generator.room_map
    return pending


def _mark_boss_perimeter_blocked(
    generator: LevelGeneratorResearch,
    state: PostTopologyState,
    room_id: int,
) -> None:
    """Port RVA 0x005B1860's center-plus-four-neighbors writes."""

    offsets = ((0, 0),) + DIRECTION_OFFSETS
    for column, line in state.rooms[room_id].cells:
        for dx, dy in offsets:
            x, y = column + dx, line + dy
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                generator.blocked_positions[y * GRID_WIDTH + x] = True


def _failure(
    state: PostTopologyState, operation: str,
    boss: BossPoolRuntimeSelection, boss_room: int,
    boss_config: RoomConfigEntry | None, type8: list[int],
    snapshot: int, shop_room: int, shop_config: RoomConfigEntry | None,
    treasure_room: int, treasure_config: RoomConfigEntry | None,
    ledger: list[PipelineRNGDraw], configs: list[ConfigTrace],
    conditions: list[ConditionTrace],
    *,
    additional_bosses: tuple[BossPoolRuntimeSelection, ...] = (),
    additional_boss_rooms: tuple[int, ...] = (),
    additional_boss_configs: tuple[RoomConfigKey, ...] = (),
    treasure_rooms: tuple[int, ...] = (),
    treasure_configs: tuple[RoomConfigKey, ...] = (),
) -> PostTopologyAttemptResult:
    return PostTopologyAttemptResult(
        False, operation, boss, boss_room,
        None if boss_config is None else boss_config.key, tuple(type8),
        shop_room, None if shop_config is None else shop_config.key,
        treasure_room, None if treasure_config is None else treasure_config.key,
        snapshot,
        tuple(replace(room, neighbors=set(room.neighbors)) for room in state.rooms),
        tuple(state.room_map), tuple(state.dead_ends), tuple(ledger), tuple(configs),
        tuple(state.candidate_trace), tuple(state.geometry_trace), tuple(conditions),
        additional_bosses,
        additional_boss_rooms,
        additional_boss_configs,
        treasure_rooms,
        treasure_configs,
    )


def run_post_topology_through_treasure(
    generator: LevelGeneratorResearch,
    *, run_state: RunGenerationState, floor_state: FloorGenerationState,
    entries: tuple[RoomConfigEntry, ...],
    profile: CanonicalBasement1Profile | CanonicalBasement2Profile | CanonicalCaves1Profile,
) -> PostTopologyAttemptResult:
    profile.validate()
    if profile.level_stage not in (1, 2, 3, 4, 5, 6) or (
        profile.is_xl and profile.level_stage not in (3, 5)
    ) or 589 in profile.collectible_ids:
        raise ValueError("through-Treasure leaf supports canonical Basement I/II/Caves I/II/Depths I/II")
    assert isinstance(floor_state.level_rng, IsaacRNG)
    state = _state_from_generator(generator, floor_state.level_rng)
    ledger: list[PipelineRNGDraw] = []
    config_traces: list[ConfigTrace] = []
    conditions: list[ConditionTrace] = []
    boss = run_state.boss_pools.select_canonical_stage(profile.room_config_stage)
    boss_entry = _select_boss_config(
        state,
        selection=boss,
        entries=entries,
        run_state=run_state,
        ledger=ledger,
        config_traces=config_traces,
        operation="Boss",
        seed_rva=0x003394A4,
    )
    if boss_entry is None:
        return _failure(state, "Boss RoomConfig", boss, -1, None, [], 0, -1, None, -1, None, ledger, config_traces, conditions)

    boss_room = _consume_end_room(state, boss_entry, "DetermineBossRoom", minimum_distance=1)
    if boss_room < 0:
        return _failure(state, "Boss geometry", boss, -1, boss_entry, [], 0, -1, None, -1, None, ledger, config_traces, conditions)
    if not reshape_end_room(state, boss_room, boss_entry.shape, boss_entry.door_mask, events=state.geometry_trace):
        return _failure(state, "Boss geometry validation", boss, boss_room, boss_entry, [], 0, -1, None, -1, None, ledger, config_traces, conditions)
    _assign(state, boss_room, boss_entry)

    conditions.append(ConditionTrace("0x00339540..0x003398AB", "additional multi-boss Stage 12 block", False, "skip"))
    additional_bosses: list[BossPoolRuntimeSelection] = []
    additional_boss_rooms: list[int] = []
    additional_boss_configs: list[RoomConfigKey] = []
    last_boss_room = boss_room
    if profile.is_xl:
        pending_room = _prepare_xl_extra_boss_room(
            state,
            generator,
            boss_room,
            boss_entry.door_mask,
        )
        level_snapshot = state.level_rng.seed
        second_boss = run_state.boss_pools.select_canonical_stage(profile.room_config_stage)
        additional_bosses.append(second_boss)
        second_entry = _select_boss_config(
            state,
            selection=second_boss,
            entries=entries,
            run_state=run_state,
            ledger=ledger,
            config_traces=config_traces,
            operation="Boss[1]",
            seed_rva=0x00339951,
        )
        if second_entry is None:
            return _failure(
                state, "Boss[1] RoomConfig", boss, boss_room, boss_entry,
                [], 0, -1, None, -1, None, ledger, config_traces, conditions,
                additional_bosses=tuple(additional_bosses),
            )
        if pending_room < 0 or not reshape_end_room(
            state,
            pending_room,
            second_entry.shape,
            second_entry.door_mask,
            events=state.geometry_trace,
        ):
            return _failure(
                state, "Boss[1] geometry", boss, boss_room, boss_entry,
                [], 0, -1, None, -1, None, ledger, config_traces, conditions,
                additional_bosses=tuple(additional_bosses),
            )
        _assign(state, pending_room, second_entry)
        additional_boss_rooms.append(pending_room)
        additional_boss_configs.append(second_entry.key)
        generator.num_boss_rooms = 2
        generator.next_boss_room_index = -1
        state.level_rng.set_seed(level_snapshot, LEVEL_SHIFT_INDEX)
        last_boss_room = pending_room
        conditions.append(ConditionTrace(
            "0x00339926..0x00339A0D",
            "effective XL",
            True,
            "place second Boss; restore Level RNG only after success",
        ))
    else:
        conditions.append(ConditionTrace(
            "0x00339926..0x00339A0D", "effective XL", False, "skip"
        ))
    # Stage-3 recovery explicitly includes FUN_009b1860's Boss-perimeter
    # blocked-cell write.  Keep the already frozen Basement-I/II leaf byte-for-
    # byte stable while the earlier-stage evidence snapshots remain immutable.
    if profile.level_stage == 3:
        _mark_boss_perimeter_blocked(generator, state, last_boss_room)

    type8_seed = _draw(state.level_rng, ledger, rva=0x00339A87, identity="Level._generationRNG", shift_index=35, reason="RoomType8", usage="seed private index-9 stream")
    type8_private = IsaacRNG.game_constructor(type8_seed, TYPE8_SHIFT_INDEX)
    type8_rooms: list[int] = []
    wanted = 2 if 589 in profile.collectible_ids else 1
    for iteration in range(wanted):
        selector_seed = _draw(type8_private, ledger, rva=0x00339B1E, identity="RoomType8.private", shift_index=9, reason=f"RoomType8 iteration {iteration}", usage="RoomConfig selector seed")
        selection = select_room(entries, run_state.room_config, RoomConfigQuery(selector_seed, True, 0, 8, subtype=-1))
        config_traces.append(ConfigTrace("RoomType8", (0,), (selection,)))
        _append_config_draws(ledger, "RoomType8", (selection,))
        entry = selection.entry
        if entry is None:
            return _failure(
                state, "RoomType8 RoomConfig", boss, boss_room, boss_entry,
                type8_rooms, 0, -1, None, -1, None, ledger, config_traces,
                conditions,
                additional_bosses=tuple(additional_bosses),
                additional_boss_rooms=tuple(additional_boss_rooms),
                additional_boss_configs=tuple(additional_boss_configs),
            )
        room_id = _consume_end_room(state, entry, "GetNewEndRoom(RoomType8)")
        if room_id < 0:
            if iteration == 0:
                return _failure(
                    state, "RoomType8 geometry", boss, boss_room, boss_entry,
                    type8_rooms, 0, -1, None, -1, None, ledger,
                    config_traces, conditions,
                    additional_bosses=tuple(additional_bosses),
                    additional_boss_rooms=tuple(additional_boss_rooms),
                    additional_boss_configs=tuple(additional_boss_configs),
                )
            break
        _assign(state, room_id, entry)
        type8_rooms.append(room_id)

    snapshot = _draw(state.level_rng, ledger, rva=0x00339BE7, identity="Level._generationRNG", shift_index=35, reason="post-Type8 seed snapshot", usage="later independent Secret/Ultra seed source")

    conditions.append(ConditionTrace("0x00339C0A..0x00339C81", f"ordinary Stage {profile.level_stage} Shop eligibility", True, "enter Shop"))
    conditions.append(ConditionTrace("0x00339CAA..0x00339CD1", "fresh Shop visit/count state", True, "enter Shop"))
    shop_private_seed = _draw(state.level_rng, ledger, rva=0x00339DB4, identity="Level._generationRNG", shift_index=35, reason="Shop subtype", usage="seed private index-19 stream")
    shop_private = IsaacRNG.game_constructor(shop_private_seed, SHOP_PRIVATE_SHIFT_INDEX)
    for index, reason in enumerate(("first shop count choice", "second shop count choice", "route parity choice", "collectible shop subtype choice")):
        _draw(shop_private, ledger, rva=(0x00339E04, 0x00339E52, 0x00339EB2, 0x00339F46)[index], identity="Shop subtype.private", shift_index=19, reason=reason, usage="canonical no-collectible subtype path")
    shop_subtype = 11
    shop_config_seed = _draw(state.level_rng, ledger, rva=0x0033A1C7, identity="Level._generationRNG", shift_index=35, reason="Shop RoomConfig", usage="RoomConfig selector seed")
    shop_selection = select_room(entries, run_state.room_config, RoomConfigQuery(shop_config_seed, True, 0, 2, subtype=shop_subtype))
    config_traces.append(ConfigTrace("Shop", (0,), (shop_selection,)))
    _append_config_draws(ledger, "Shop", (shop_selection,))
    shop_entry = shop_selection.entry
    if shop_entry is None:
        return _failure(
            state, "Shop RoomConfig", boss, boss_room, boss_entry, type8_rooms,
            snapshot, -1, None, -1, None, ledger, config_traces, conditions,
            additional_bosses=tuple(additional_bosses),
            additional_boss_rooms=tuple(additional_boss_rooms),
            additional_boss_configs=tuple(additional_boss_configs),
        )
    shop_room = _consume_end_room(state, shop_entry, "GetNewEndRoom(Shop)")
    if shop_room < 0:
        return _failure(
            state, "Shop geometry", boss, boss_room, boss_entry, type8_rooms,
            snapshot, -1, shop_entry, -1, None, ledger, config_traces,
            conditions,
            additional_bosses=tuple(additional_bosses),
            additional_boss_rooms=tuple(additional_boss_rooms),
            additional_boss_configs=tuple(additional_boss_configs),
        )
    _assign(state, shop_room, shop_entry)

    conditions.append(ConditionTrace("0x0033A2C3..0x0033A383", f"ordinary Stage {profile.level_stage} Treasure eligibility", True, "enter Treasure"))
    treasure_rooms: list[int] = []
    treasure_configs: list[RoomConfigKey] = []
    treasure_entries: list[RoomConfigEntry] = []
    treasure_entry: RoomConfigEntry | None = None
    first_treasure_level_snapshot: int | None = None
    wanted_treasures = 2 if profile.is_xl else 1
    for iteration in range(wanted_treasures):
        operation = "Treasure" if iteration == 0 else f"Treasure[{iteration}]"
        treasure_probability = _draw(state.level_rng, ledger, rva=0x0033A455, identity="Level._generationRNG", shift_index=35, reason=f"{operation} subtype probability", usage="rare subtype branch if state % 100 == 0")
        if treasure_probability % 100 == 0:
            treasure_subtype = 1
        else:
            _draw(state.level_rng, ledger, rva=0x0033A4B8, identity="Level._generationRNG", shift_index=35, reason=f"{operation} collectible/chance path", usage="canonical no-collectible branch")
            treasure_subtype = 0
        treasure_config_seed = _draw(state.level_rng, ledger, rva=0x0033A76B, identity="Level._generationRNG", shift_index=35, reason=f"{operation} RoomConfig", usage="stage wrapper selector seed")
        treasure_selections = select_room_with_stage_fallback(
            entries, run_state.room_config,
            RoomConfigQuery(treasure_config_seed, True, profile.room_config_stage, 4, subtype=treasure_subtype),
            profile.fallback_room_config_stage,
        )
        config_traces.append(ConfigTrace(operation, tuple(profile.room_config_stage if i == 0 else profile.fallback_room_config_stage for i in range(len(treasure_selections))), treasure_selections))
        _append_config_draws(ledger, operation, treasure_selections)
        treasure_entry = treasure_selections[-1].entry
        if treasure_entry is None:
            return _failure(
                state, f"{operation} RoomConfig", boss, boss_room, boss_entry,
                type8_rooms, snapshot, shop_room, shop_entry, -1, None,
                ledger, config_traces, conditions,
                additional_bosses=tuple(additional_bosses),
                additional_boss_rooms=tuple(additional_boss_rooms),
                additional_boss_configs=tuple(additional_boss_configs),
                treasure_rooms=tuple(treasure_rooms),
                treasure_configs=tuple(treasure_configs),
            )
        treasure_room = _consume_end_room(state, treasure_entry, f"GetNewEndRoom({operation})")
        if treasure_room < 0:
            return _failure(
                state, f"{operation} geometry", boss, boss_room, boss_entry,
                type8_rooms, snapshot, shop_room, shop_entry, -1,
                treasure_entry, ledger, config_traces, conditions,
                additional_bosses=tuple(additional_bosses),
                additional_boss_rooms=tuple(additional_boss_rooms),
                additional_boss_configs=tuple(additional_boss_configs),
                treasure_rooms=tuple(treasure_rooms),
                treasure_configs=tuple(treasure_configs),
            )
        _assign(state, treasure_room, treasure_entry)
        treasure_rooms.append(treasure_room)
        treasure_configs.append(treasure_entry.key)
        treasure_entries.append(treasure_entry)
        if iteration == 0:
            first_treasure_level_snapshot = state.level_rng.seed

    if profile.is_xl:
        assert first_treasure_level_snapshot is not None
        state.level_rng.set_seed(first_treasure_level_snapshot, LEVEL_SHIFT_INDEX)
        conditions.append(ConditionTrace(
            "0x0033A8A1..0x0033A8EC",
            "effective XL Treasure count",
            True,
            "place second Treasure; restore Level RNG only after success",
        ))

    return PostTopologyAttemptResult(
        True, None, boss, boss_room, boss_entry.key, tuple(type8_rooms),
        shop_room, shop_entry.key, treasure_rooms[0], treasure_entries[0].key, snapshot,
        tuple(replace(room, neighbors=set(room.neighbors)) for room in state.rooms),
        tuple(state.room_map), tuple(state.dead_ends), tuple(ledger), tuple(config_traces),
        tuple(state.candidate_trace), tuple(state.geometry_trace), tuple(conditions),
        tuple(additional_bosses),
        tuple(additional_boss_rooms),
        tuple(additional_boss_configs),
        tuple(treasure_rooms),
        tuple(treasure_configs),
    )


def generate_basement1_through_treasure(
    start_seed: int, difficulty: str,
    *, boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Basement1ThroughTreasureResult:
    profile = CanonicalBasement1Profile(difficulty=difficulty)
    profile.validate()
    inputs = derive_basement1_topology_inputs(start_seed, difficulty)
    entries = entries_from_definitions(special_definitions, stage=0) + entries_from_definitions(basement_definitions, stage=1)
    boss_pools = BossPoolRuntimeState.fresh_basement(start_seed, boss_entries)
    run_state = RunGenerationState(start_seed, boss_pools, RoomConfigMutableState())
    # Level::Init resets both current-stage and special-stage pools once,
    # outside the outer attempt loop.
    run_state.room_config.reset(entries)
    generator = LevelGeneratorResearch(inputs.generator_seed)
    level_rng = IsaacRNG.game_constructor(inputs.generator_seed, LEVEL_SHIFT_INDEX)
    floor_state = FloorGenerationState(inputs.stage_seed, target_room_count=inputs.target_room_count, level_rng=level_rng, level_generator=generator)
    attempts: list[GenerationAttemptResult] = []
    final_rooms: tuple[GeneratedRoom, ...] = ()

    for attempt_number in range(1, max_attempts + 1):
        floor_state.retry_count = attempt_number - 1
        run_state.boss_pools.begin_attempt()
        start_level = level_rng.seed
        start_generator = generator.rng.seed
        start_boss = run_state.boss_pools.pool_rngs[1].seed
        weights_before = dict(run_state.room_config.weights)
        generator.blocked_positions[:] = [False] * len(generator.blocked_positions)
        generator.generate_once(
            floor_state.target_room_count, inputs.required_dead_ends,
            inputs.allowed_shapes_mask,
            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        topology = _topology_snapshot(generator, floor_state.target_room_count)
        usable = len(generator.dead_ends) >= inputs.required_dead_ends
        post = None
        if usable:
            post = run_post_topology_through_treasure(
                generator, run_state=run_state, floor_state=floor_state,
                entries=entries, profile=profile,
            )
        elif attempt_number >= 10 and attempt_number % 5 == 0 and floor_state.target_room_count < 64:
            floor_state.target_room_count += 1

        mutations = tuple(
            (key, weights_before.get(key, value), value)
            for key, value in sorted(run_state.room_config.weights.items())
            if weights_before.get(key, value) != value
        )
        attempts.append(GenerationAttemptResult(
            attempt_number, topology.target_room_count, usable, topology,
            start_level, level_rng.seed, start_generator, generator.rng.seed,
            start_boss, run_state.boss_pools.pool_rngs[1].seed,
            tuple(sorted(run_state.boss_pools.level_blacklist)),
            tuple(sorted(run_state.boss_pools.removed)), mutations, post,
        ))
        if post is not None and post.completed:
            final_rooms = post.rooms
            run_state.boss_pools.commit_floor()
            run_state.current_stage_lifecycle = "basement1-generated-through-treasure"
            return Basement1ThroughTreasureResult(
                True, start_seed, difficulty, inputs.stage_seed, tuple(attempts),
                level_rng.seed, generator.rng.seed,
                run_state.boss_pools.pool_rngs[1].seed,
                tuple(sorted(run_state.boss_pools.removed)),
                tuple(sorted(run_state.room_config.weights.items())), final_rooms,
            )
        # Failure cleanup discards topology/descriptors only. The state owners
        # above intentionally remain mutated for the next attempt.

    return Basement1ThroughTreasureResult(
        False, start_seed, difficulty, inputs.stage_seed, tuple(attempts),
        level_rng.seed, generator.rng.seed, run_state.boss_pools.pool_rngs[1].seed,
        tuple(sorted(run_state.boss_pools.removed)),
        tuple(sorted(run_state.room_config.weights.items())), final_rooms,
    )
