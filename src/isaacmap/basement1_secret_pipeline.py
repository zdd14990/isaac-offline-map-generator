"""Clean frozen-profile continuation from Treasure through Secret.

The earlier M5 implementation is intentionally left untouched.  This module
starts from its completed attempt snapshot and follows the binary call order
through the Secret-room descriptor assignment.  Ultra Secret and late normal
ROOM_DEFAULT selection are outside this executable path's implemented scope.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import struct

from .basement1_pipeline import (
    ConfigTrace,
    ConditionTrace,
    PipelineRNGDraw,
    PostTopologyAttemptResult,
    _append_config_draws,
    _assign,
    _consume_end_room,
    _draw,
    _topology_snapshot,
    run_post_topology_through_treasure,
)
from .boss_pool import BossPoolEntry, BossPoolRuntimeState
from .floor_init import derive_basement1_topology_inputs
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
    RoomConfigQuery,
    RoomConfigSelection,
    select_room,
    select_room_with_stage_fallback,
    entries_from_definitions,
    RoomConfigMutableState,
)
from .secret import (
    SecretGeometryState,
    SecretPlacementResult,
    SecretRNGTransition,
    build_secret_forbidden_indices,
    place_secret_room,
)
from .special_rooms import CandidateTrace, GeneratedRoom, PostTopologyState
from .topology import LevelGeneratorResearch, LevelGeneratorRoom, TopologyResearchResult
from .topology_geometry import RoomShape


LEVEL_SHIFT_INDEX = 35
CURSE_PRIVATE_SHIFT_INDEX = 66
SECRET_CONFIG_SHIFT_INDEX = 1


@dataclass(frozen=True)
class InterveningBlockTrace:
    operation: str
    binary_range: str
    room_type: int
    subtype: int
    candidate_before: tuple[int, ...]
    candidate_room: int
    assigned: bool
    candidate_after: tuple[int, ...]
    config: RoomConfigKey | None
    predicate: str
    persistent_bit_write: int | None = None


@dataclass(frozen=True)
class SecretConfigRNGTransition:
    iteration: int
    binary_rva: int
    pre_state: int
    post_state: int
    shift_index: int
    reason: str


@dataclass(frozen=True)
class SecretDescriptorMutation:
    created: bool
    generator_room_id: int
    list_index: int
    grid_index: int
    safe_grid_index: int
    room_shape: int
    room_type: int
    descriptor_count_before: int
    descriptor_count_after: int
    dead_ends_before: tuple[int, ...]
    dead_ends_after: tuple[int, ...]


@dataclass(frozen=True)
class PostTreasureThroughSecretResult:
    completed: bool
    abort_operation: str | None
    blocks: tuple[InterveningBlockTrace, ...]
    secret_room: int
    secret_config: RoomConfigKey | None
    rooms: tuple[GeneratedRoom, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    blocked_positions: tuple[bool, ...]
    descriptor_configs: tuple[tuple[int, RoomConfigKey], ...]
    rng_draws: tuple[PipelineRNGDraw, ...]
    config_traces: tuple[ConfigTrace, ...]
    candidate_traces: tuple[CandidateTrace, ...]
    conditions: tuple[ConditionTrace, ...]
    secret_config_rng: tuple[SecretConfigRNGTransition, ...]
    secret_geometry: SecretPlacementResult
    secret_descriptor: SecretDescriptorMutation
    final_level_rng_state: int
    final_generator_rng_state: int
    used_bits_after: tuple[int, ...]


@dataclass(frozen=True)
class SecretGenerationAttemptResult:
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
    used_bits_before: tuple[int, ...]
    used_bits_after: tuple[int, ...]
    room_config_mutations: tuple[tuple[RoomConfigKey, float, float], ...]
    through_treasure: PostTopologyAttemptResult | None
    through_secret: PostTreasureThroughSecretResult | None


@dataclass(frozen=True)
class Basement1ThroughSecretResult:
    boundary_completed: bool
    start_seed: int
    difficulty: str
    stage_seed: int
    attempts: tuple[SecretGenerationAttemptResult, ...]
    final_level_rng_state: int
    final_generator_rng_state: int
    final_boss_pool_state: int
    permanent_removed_bosses: tuple[int, ...]
    pending_boss_blacklist: tuple[int, ...]
    final_room_config_weights: tuple[tuple[RoomConfigKey, float], ...]
    final_special_room_used_bits: tuple[int, ...]
    rooms: tuple[GeneratedRoom, ...]


def _f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


def _unit_from_state(value: int) -> float:
    scale = struct.unpack("<f", struct.pack("<I", 0x2F7FFFFE))[0]
    return _f32(_f32(float(value & 0xFFFFFFFF)) * scale)


def _clone_post(post: PostTopologyAttemptResult, level_rng: IsaacRNG) -> PostTopologyState:
    return PostTopologyState(
        rooms=[replace(room, neighbors=set(room.neighbors)) for room in post.rooms],
        room_map=list(post.room_map),
        dead_ends=list(post.dead_ends),
        level_rng=level_rng,
    )


def _entry_map(entries: tuple[RoomConfigEntry, ...]) -> dict[RoomConfigKey, RoomConfigEntry]:
    return {entry.key: entry for entry in entries}


def _selected_entries(post: PostTopologyAttemptResult, entries: tuple[RoomConfigEntry, ...]) -> dict[int, RoomConfigEntry]:
    by_key = _entry_map(entries)
    result: dict[int, RoomConfigEntry] = {}
    if post.boss_config is not None:
        result[post.boss_room] = by_key[post.boss_config]
    for room_id, key in zip(
        post.additional_boss_rooms, post.additional_boss_configs
    ):
        result[room_id] = by_key[key]
    type8_entries = [
        trace.selections[-1].entry for trace in post.config_traces
        if trace.operation == "RoomType8" and trace.selections[-1].entry is not None
    ]
    for room_id, entry in zip(post.type8_rooms, type8_entries):
        result[room_id] = entry
    if post.shop_config is not None:
        result[post.shop_room] = by_key[post.shop_config]
    if post.treasure_config is not None:
        result[post.treasure_room] = by_key[post.treasure_config]
    for room_id, key in zip(post.treasure_rooms[1:], post.treasure_configs[1:]):
        result[room_id] = by_key[key]
    return result


def _select(
    operation: str,
    seed: int,
    entries: tuple[RoomConfigEntry, ...],
    run_state: RunGenerationState,
    ledger: list[PipelineRNGDraw],
    configs: list[ConfigTrace],
    *,
    room_type: int,
    subtype: int = -1,
    reduce_weight: bool = True,
    min_difficulty: int = 1,
    max_difficulty: int = 10,
) -> RoomConfigEntry:
    selection = select_room(
        entries, run_state.room_config,
        RoomConfigQuery(
            seed, reduce_weight, 0, room_type, subtype=subtype,
            min_difficulty=min_difficulty, max_difficulty=max_difficulty,
        ),
    )
    configs.append(ConfigTrace(operation, (0,), (selection,)))
    _append_config_draws(ledger, operation, (selection,))
    if selection.entry is None:
        raise AssertionError(f"frozen resources have no {operation} RoomConfig")
    return selection.entry


def _consume_and_dispose(
    state: PostTopologyState,
    entry: RoomConfigEntry,
    operation: str,
    *,
    assign: bool,
    descriptor_configs: dict[int, RoomConfigEntry],
    blocks: list[InterveningBlockTrace],
    binary_range: str,
    predicate: str,
    persistent_bit_write: int | None = None,
) -> int:
    before = tuple(state.dead_ends)
    room_id = _consume_end_room(state, entry, f"GetNewEndRoom({operation})")
    assigned = room_id >= 0 and assign
    if room_id >= 0:
        if assigned:
            _assign(state, room_id, entry)
            descriptor_configs[room_id] = entry
        else:
            state.dead_ends.append(room_id)
    blocks.append(InterveningBlockTrace(
        operation, binary_range, entry.room_type, entry.subtype, before,
        room_id, assigned, tuple(state.dead_ends), entry.key, predicate,
        persistent_bit_write if assigned else None,
    ))
    return room_id if assigned else -1


def run_treasure_to_secret(
    post: PostTopologyAttemptResult,
    *,
    generator: LevelGeneratorResearch,
    run_state: RunGenerationState,
    entries: tuple[RoomConfigEntry, ...],
    profile: CanonicalBasement1Profile | CanonicalBasement2Profile | CanonicalCaves1Profile,
) -> PostTreasureThroughSecretResult:
    """Continue one successful M5 attempt to the Secret completion point."""

    profile.validate()
    if not post.completed:
        raise ValueError("M6 continuation requires a completed M5 attempt")
    state = _clone_post(post, post_level_rng := generator_level_rng(post, generator))
    # ``generator_level_rng`` returns the exact Level RNG object installed by
    # the caller.  The assignment above makes its distinct identity explicit.
    del post_level_rng
    ledger: list[PipelineRNGDraw] = []
    configs: list[ConfigTrace] = []
    conditions: list[ConditionTrace] = []
    blocks: list[InterveningBlockTrace] = []
    descriptor_configs = _selected_entries(post, entries)

    # Planetarium (RoomType 24).  The binary gates the whole block after the
    # selector-seed draw (0x0033A8F7..0x0033AB45): enter only when
    # level_stage < 7, or level_stage < 9 with Planetarium item (collectible
    # 0x6e), or the stage-10 route cases.  Canonical Womb I/II (stage 7/8,
    # no collectibles) consume the draw and skip the block.
    seed = _draw(state.level_rng, ledger, rva=0x0033A961, identity="Level._generationRNG", shift_index=35, reason="Planetarium RoomConfig", usage="type 24 selector seed")
    planetarium_gate = (
        profile.level_stage < 7
        or (profile.level_stage < 9 and 0x6e in profile.collectible_ids)
        or profile.level_stage == 10
    )
    entry = None
    before = tuple(state.dead_ends)
    rid = -1
    place = False
    if planetarium_gate:
        entry = _select("Planetarium", seed, entries, run_state, ledger, configs, room_type=24)
        rid = _consume_end_room(state, entry, "GetNewEndRoom(Planetarium)")
        absent = not ({24, 4} & profile.visited_room_types)
        if rid >= 0 and absent:
            chance_state = _draw(state.level_rng, ledger, rva=0x0033AA9B, identity="Level._generationRNG", shift_index=35, reason="Planetarium chance", usage="binary32 RandomFloat < 0.01")
            place = (
                _unit_from_state(chance_state) < _f32(profile.planetarium_chance)
                and profile.planetarium_unlocked
            )
        if rid >= 0:
            if place:
                _assign(state, rid, entry); descriptor_configs[rid] = entry
            else:
                state.dead_ends.append(rid)
    blocks.append(InterveningBlockTrace("Planetarium", "0x0033A8F7..0x0033AB45", 24, entry.subtype if entry is not None else 0, before, rid, rid >= 0 and place, tuple(state.dead_ends), entry.key if entry is not None else None, f"gate={planetarium_gate}; skipped" if not planetarium_gate else f"gate={planetarium_gate}; visited types 24/4 absent; unlocked; f32(Level.Next()) < {profile.planetarium_chance}"))

    # Dice (21) / Sacrifice (13).
    choice = _draw(state.level_rng, ledger, rva=0x0033AB94, identity="Level._generationRNG", shift_index=35, reason="Dice/Sacrifice first choice", usage="state % 50")
    if choice % 50 == 0:
        room_type = 21
    else:
        choice2 = _draw(state.level_rng, ledger, rva=0x0033ABFB, identity="Level._generationRNG", shift_index=35, reason="Dice/Sacrifice second choice", usage="state % 5 and max hearts")
        room_type = 21 if choice2 % 5 == 0 and profile.player0_max_hearts > 1 else 13
    config_seed = _draw(state.level_rng, ledger, rva=0x0033ACC6 if room_type == 21 else 0x0033AE4E, identity="Level._generationRNG", shift_index=35, reason="Dice/Sacrifice RoomConfig", usage=f"type {room_type} selector seed")
    entry = _select("Dice" if room_type == 21 else "Sacrifice", config_seed, entries, run_state, ledger, configs, room_type=room_type)
    before = tuple(state.dead_ends); rid = _consume_end_room(state, entry, f"GetNewEndRoom({'Dice' if room_type == 21 else 'Sacrifice'})")
    place = False
    if rid >= 0 and room_type not in profile.visited_room_types:
        decision = _draw(state.level_rng, ledger, rva=0x0033AD68, identity="Level._generationRNG", shift_index=35, reason="Dice/Sacrifice primary gate", usage="state % 7")
        place = decision % 7 == 0
        if not place:
            decision2 = _draw(state.level_rng, ledger, rva=0x0033AE83, identity="Level._generationRNG", shift_index=35, reason="Dice/Sacrifice secondary gate", usage="state & 3 and player condition")
            place = (decision2 & 3) == 0 and profile.player0_full_health
    if rid >= 0:
        if place: _assign(state, rid, entry); descriptor_configs[rid] = entry
        else: state.dead_ends.append(rid)
    blocks.append(InterveningBlockTrace("Dice" if room_type == 21 else "Sacrifice", "0x0033AB45..0x0033AF08", room_type, entry.subtype, before, rid, rid >= 0 and place, tuple(state.dead_ends), entry.key, "1/50 Dice, else 1/5 with hearts; then 1/7 or 1/4 full-health gate"))

    # Library (12).  Its selector's reduceWeight argument is zero.
    subtype_state = _draw(state.level_rng, ledger, rva=0x0033AF8E, identity="Level._generationRNG", shift_index=35, reason="Library subtype", usage=f"RandomInt({profile.library_subtype_max + 1})")
    subtype = subtype_state % (profile.library_subtype_max + 1)
    seed = _draw(state.level_rng, ledger, rva=0x0033AFF7, identity="Level._generationRNG", shift_index=35, reason="Library RoomConfig", usage="type 12 selector seed")
    entry = _select("Library", seed, entries, run_state, ledger, configs, room_type=12, subtype=subtype, reduce_weight=False)
    before = tuple(state.dead_ends); rid = _consume_end_room(state, entry, "GetNewEndRoom(Library)")
    place = False
    if rid >= 0 and 12 not in profile.visited_room_types:
        decision = _draw(state.level_rng, ledger, rva=0x0033B08F, identity="Level._generationRNG", shift_index=35, reason="Library primary gate", usage="state % 20")
        place = decision % 20 == 0
        if not place:
            decision2 = _draw(state.level_rng, ledger, rva=0x0033B108, identity="Level._generationRNG", shift_index=35, reason="Library secondary gate", usage="state & 3 plus persistent bit 8")
            place = (decision2 & 3) == 0 and 8 in run_state.special_room_used_bits
    if rid >= 0:
        if place: _assign(state, rid, entry); descriptor_configs[rid] = entry
        else: state.dead_ends.append(rid)
    blocks.append(InterveningBlockTrace("Library", "0x0033AF71..0x0033B10D", 12, subtype, before, rid, rid >= 0 and place, tuple(state.dead_ends), entry.key, "1/20, or 1/4 with Game+0x26548 bit 8; no weight decay"))

    # Curse Room (10) uses a temporary index-66 RNG seeded by one Level draw.
    private_seed = _draw(state.level_rng, ledger, rva=0x0033B166, identity="Level._generationRNG", shift_index=35, reason="Curse private seed", usage="construct temporary index-66 RNG")
    private = IsaacRNG.game_constructor(private_seed, CURSE_PRIVATE_SHIFT_INDEX)
    config_seed = _draw(private, ledger, rva=0x0033B200, identity="Curse.private", shift_index=66, reason="Curse RoomConfig", usage="type 10 subtype 0 selector seed")
    entry = _select("Curse", config_seed, entries, run_state, ledger, configs, room_type=10, subtype=0)
    before = tuple(state.dead_ends); rid = _consume_end_room(state, entry, "GetNewEndRoom(Curse)")
    place = rid >= 0 and 10 not in profile.visited_room_types
    if place:
        room_seed = _draw(private, ledger, rva=0x0033B301, identity="Curse.private", shift_index=66, reason="Curse descriptor seed", usage="advance once; odd state advances again")
        if room_seed & 1:
            _draw(private, ledger, rva=0x0033B351, identity="Curse.private", shift_index=66, reason="Curse odd-state extra advance", usage="final descriptor seed")
        _assign(state, rid, entry); descriptor_configs[rid] = entry
    elif rid >= 0:
        state.dead_ends.append(rid)
    blocks.append(InterveningBlockTrace("Curse", "0x0033B10D..0x0033B3A8", 10, 0, before, rid, place, tuple(state.dead_ends), entry.key, "fresh canonical profile always assigns a compatible candidate"))

    # MiniBoss (6): stable subtype vector built from Game+0x26548 bits.
    subtype_bits = ((2, 9), (3, 10), (1, 11), (0, 12), (5, 13), (6, 14))
    available = [sub for sub, bit in subtype_bits if bit not in run_state.special_room_used_bits]
    subtype_draw = _draw(state.level_rng, ledger, rva=0x0033B7F2, identity="Level._generationRNG", shift_index=35, reason="MiniBoss subtype", usage=f"RandomInt({len(available)})")
    subtype = available[subtype_draw % len(available)]
    seed = _draw(state.level_rng, ledger, rva=0x0033B8AB, identity="Level._generationRNG", shift_index=35, reason="MiniBoss RoomConfig exact difficulty", usage="type 6 selector seed")
    selection = select_room(entries, run_state.room_config, RoomConfigQuery(seed, True, 0, 6, subtype=subtype, min_difficulty=1, max_difficulty=1))
    configs.append(ConfigTrace("MiniBoss", (0,), (selection,))); _append_config_draws(ledger, "MiniBoss", (selection,))
    entry = selection.entry
    if entry is None:
        seed = _draw(state.level_rng, ledger, rva=0x0033B918, identity="Level._generationRNG", shift_index=35, reason="MiniBoss RoomConfig fallback", usage="difficulty 1..10 selector seed")
        entry = _select("MiniBossFallback", seed, entries, run_state, ledger, configs, room_type=6, subtype=subtype)
    before = tuple(state.dead_ends); rid = _consume_end_room(state, entry, "GetNewEndRoom(MiniBoss)")
    place = False
    if rid >= 0 and 6 not in profile.visited_room_types:
        decision = _draw(state.level_rng, ledger, rva=0x0033B9C3, identity="Level._generationRNG", shift_index=35, reason="MiniBoss primary gate", usage="state & 3")
        place = (decision & 3) == 0
        if not place:
            decision2 = _draw(state.level_rng, ledger, rva=0x0033BA27, identity="Level._generationRNG", shift_index=35, reason="MiniBoss stage-one fallback", usage="state % 3")
            place = profile.adjusted_level_stage == 1 and decision2 % 3 == 0
    written_bit = dict(subtype_bits)[subtype]
    if rid >= 0:
        if place:
            _assign(state, rid, entry); descriptor_configs[rid] = entry
            run_state.special_room_used_bits.add(written_bit)
        else: state.dead_ends.append(rid)
    blocks.append(InterveningBlockTrace("MiniBoss", "0x0033B3A8..0x0033BBAE", 6, subtype, before, rid, rid >= 0 and place, tuple(state.dead_ends), entry.key, "ordered unused-subtype vector; 1/4 or Basement-I 1/3 fallback", written_bit if place else None))

    # Challenge (11): Stage 2 admits the even gate when the canonical player
    # condition is true; Stage 1 remains below the assignment threshold.
    seed = _draw(state.level_rng, ledger, rva=0x0033BC1E, identity="Level._generationRNG", shift_index=35, reason="Challenge RoomConfig", usage="type 11 subtype 0 selector seed")
    entry = _select("Challenge", seed, entries, run_state, ledger, configs, room_type=11, subtype=0)
    before = tuple(state.dead_ends); rid = _consume_end_room(state, entry, "GetNewEndRoom(Challenge)")
    place = False
    if rid >= 0 and 11 not in profile.visited_room_types:
        challenge = _draw(state.level_rng, ledger, rva=0x0033BCF5, identity="Level._generationRNG", shift_index=35, reason="Challenge gate", usage="even draw or Stage >= 3, player condition, Stage >= 2")
        stage_gate = (challenge & 1) == 0 or profile.adjusted_level_stage >= 3
        place = stage_gate and profile.player0_full_health and profile.adjusted_level_stage >= 2
        if place: _assign(state, rid, entry); descriptor_configs[rid] = entry
        else: state.dead_ends.append(rid)
    blocks.append(InterveningBlockTrace("Challenge", "0x0033BBAE..0x0033BD87", 11, 0, before, rid, rid >= 0 and place, tuple(state.dead_ends), entry.key, "even draw or Stage >= 3; eligible player; Stage >= 2"))

    # Chest (20) / Arcade (9). Under the canonical zero-coin Stage-2 state,
    # only Chest can pass the even-floor post-config gate.
    first = _draw(state.level_rng, ledger, rva=0x0033BDD2, identity="Level._generationRNG", shift_index=35, reason="Chest/Arcade first choice", usage="state % 10")
    if first % 10 == 0:
        room_type = 20
    else:
        second = _draw(state.level_rng, ledger, rva=0x0033BE31, identity="Level._generationRNG", shift_index=35, reason="Chest/Arcade second choice", usage="state % 3 and max hearts")
        room_type = 20 if second % 3 == 0 and profile.player0_max_hearts > 1 else 9
    seed = _draw(state.level_rng, ledger, rva=0x0033BF11 if room_type == 20 else 0x0033BFB6, identity="Level._generationRNG", shift_index=35, reason="Chest/Arcade RoomConfig", usage=f"type {room_type} selector seed")
    entry = _select("Chest" if room_type == 20 else "Arcade", seed, entries, run_state, ledger, configs, room_type=room_type, subtype=-1 if room_type == 20 else 0)
    before = tuple(state.dead_ends); rid = _consume_end_room(state, entry, f"GetNewEndRoom({'Chest' if room_type == 20 else 'Arcade'})")
    if profile.stage_type in (4, 5):
        # Binary (0x73c035..0x73c09a): the chosen Chest room is assigned when
        # the ADJUSTED stage is in {2,4,6,8} and player max hearts > 1; the
        # Arcade needs coins >= 5, which the canonical profile never meets.
        place = (
            rid >= 0
            and profile.adjusted_level_stage in (2, 4, 6, 8)
            and room_type == 20
            and profile.player0_max_hearts > 1
        )
    else:
        place = (
            rid >= 0
            and profile.level_stage == 2
            and room_type == 20
            and profile.player0_max_hearts >= 2
        )
    if rid >= 0:
        if place: _assign(state, rid, entry); descriptor_configs[rid] = entry
        else: state.dead_ends.append(rid)
    blocks.append(InterveningBlockTrace("Chest" if room_type == 20 else "Arcade", "0x0033BD87..0x0033C0B6", room_type, entry.subtype, before, rid, rid >= 0 and place, tuple(state.dead_ends), entry.key, "canonical Stage 2 assigns Chest; zero-coin Arcade remains unassigned"))

    # Isaac (18) / Barren (19).  With neither visited and canonical route state,
    # the first draw is consumed but type 18 is selected deterministically.
    _draw(state.level_rng, ledger, rva=0x0033C1C5, identity="Level._generationRNG", shift_index=35, reason="Isaac/Barren type choice", usage="canonical chooses type 18")
    room_type = 18
    seed = _draw(state.level_rng, ledger, rva=0x0033C1E5, identity="Level._generationRNG", shift_index=35, reason="Isaac/Barren RoomConfig", usage="type 18 selector seed")
    entry = _select("Isaac", seed, entries, run_state, ledger, configs, room_type=room_type)
    before = tuple(state.dead_ends); rid = _consume_end_room(state, entry, "GetNewEndRoom(Isaac)")
    place = False
    if rid >= 0 and room_type not in profile.visited_room_types:
        decision = _draw(state.level_rng, ledger, rva=0x0033C336, identity="Level._generationRNG", shift_index=35, reason="Isaac primary gate", usage="state % 50")
        place = decision % 50 == 0
        if not place:
            _draw(state.level_rng, ledger, rva=0x0033C393, identity="Level._generationRNG", shift_index=35, reason="Isaac low-health fallback", usage="fresh full-health profile cannot assign")
    if rid >= 0:
        if place: _assign(state, rid, entry); descriptor_configs[rid] = entry
        else: state.dead_ends.append(rid)
    blocks.append(InterveningBlockTrace("Isaac", "0x0033C0F0..0x0033C416", 18, entry.subtype, before, rid, rid >= 0 and place, tuple(state.dead_ends), entry.key, "1/50; low-health 1/5 fallback is false for fresh Isaac"))

    conditions.extend((
        ConditionTrace("0x0033C416..0x0033C4D1", "alternate-path first-half mandatory end room", False, "skip"),
        ConditionTrace("0x0033C554..0x0033C640", "alternate-path second-half collectible-626 end room", False, "skip"),
        ConditionTrace("0x0033C645..0x0033C69E", "route-specific end-room state flag", False, "skip"),
    ))

    # Secret RoomConfig is chosen first from the saved post-Type8 seed.  Its
    # geometry is then scored with the persistent LevelGenerator RNG object.
    secret_seed = post.post_type8_seed_snapshot
    secret_selections = select_room_with_stage_fallback(
        entries, run_state.room_config,
        RoomConfigQuery(secret_seed, True, profile.room_config_stage, 7, subtype=-1),
        profile.fallback_room_config_stage,
    )
    configs.append(ConfigTrace("Secret", tuple(profile.room_config_stage if i == 0 else profile.fallback_room_config_stage for i in range(len(secret_selections))), secret_selections))
    _append_config_draws(ledger, "Secret", secret_selections)
    secret_entry = secret_selections[-1].entry
    if secret_entry is None:
        raise AssertionError("frozen resources have no Secret RoomConfig")
    forbidden = build_secret_forbidden_indices(state.rooms, descriptor_configs, level_stage=profile.level_stage)
    descriptor_count_before = len(descriptor_configs)
    dead_ends_before_secret = tuple(state.dead_ends)
    secret_state = SecretGeometryState(state.rooms, state.room_map, list(generator.blocked_positions), generator.rng)
    geometry = place_secret_room(secret_state, forbidden)
    if geometry.room_id >= 0:
        _assign(state, geometry.room_id, secret_entry)
        descriptor_configs[geometry.room_id] = secret_entry
    descriptor_mutation = SecretDescriptorMutation(
        geometry.room_id >= 0, geometry.room_id,
        descriptor_count_before if geometry.room_id >= 0 else -1,
        geometry.grid_index, geometry.grid_index,
        1 if geometry.room_id >= 0 else 0,
        7 if geometry.room_id >= 0 else 0,
        descriptor_count_before, len(descriptor_configs),
        dead_ends_before_secret, tuple(state.dead_ends),
    )

    private = IsaacRNG.game_constructor(secret_seed, SECRET_CONFIG_SHIFT_INDEX)
    pre = private.seed; post_private = private.next()
    secret_private = (SecretConfigRNGTransition(0, 0x0033C802, pre, post_private, 1, "advance saved Secret iteration seed after placement attempt"),)
    conditions.append(ConditionTrace(
        "0x0033C83B..0x0033C902",
        "post-Secret Stage 11 ORIGINAL mandatory subtype-3 end room",
        False,
        "skip; next canonical operation is Ultra Secret entry",
    ))

    return PostTreasureThroughSecretResult(
        True, None, tuple(blocks), geometry.room_id, secret_entry.key,
        tuple(replace(room, neighbors=set(room.neighbors)) for room in state.rooms),
        tuple(state.room_map), tuple(state.dead_ends),
        tuple(generator.blocked_positions),
        tuple(sorted((rid, entry.key) for rid, entry in descriptor_configs.items())),
        tuple(ledger), tuple(configs), tuple(state.candidate_trace), tuple(conditions),
        secret_private, geometry, descriptor_mutation,
        state.level_rng.seed, generator.rng.seed,
        tuple(sorted(run_state.special_room_used_bits)),
    )


def generator_level_rng(
    post: PostTopologyAttemptResult, generator: LevelGeneratorResearch
) -> IsaacRNG:
    """Retrieve the caller-installed Level RNG without conflating identities.

    M5 records its final state but does not retain the object in its immutable
    result.  The M6 caller installs the object on ``_m6_level_rng`` before this
    continuation; the fallback constructor is only for isolated leaf tests.
    """

    existing = getattr(generator, "_m6_level_rng", None)
    if isinstance(existing, IsaacRNG):
        return existing
    final_level = next(
        draw.post_state for draw in reversed(post.rng_draws)
        if draw.object_identity == "Level._generationRNG"
    )
    return IsaacRNG.game_constructor(final_level, LEVEL_SHIFT_INDEX)


def generate_basement1_through_secret(
    start_seed: int,
    difficulty: str,
    *,
    boss_entries: tuple[BossPoolEntry, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> Basement1ThroughSecretResult:
    """Replay outer attempts to the pre-Ultra M6 boundary.

    ``boundary_completed`` is deliberately not called floor success: the late
    default-room selector can still reject this attempt.
    """

    profile = CanonicalBasement1Profile(difficulty=difficulty)
    profile.validate()
    inputs = derive_basement1_topology_inputs(start_seed, difficulty)
    entries = (
        entries_from_definitions(special_definitions, stage=0)
        + entries_from_definitions(basement_definitions, stage=1)
    )
    run_state = RunGenerationState(
        start_seed,
        BossPoolRuntimeState.fresh_basement(start_seed, boss_entries),
        RoomConfigMutableState(),
        special_room_used_bits=set(profile.special_room_used_bits),
    )
    run_state.room_config.reset(entries)
    generator = LevelGeneratorResearch(inputs.generator_seed)
    level_rng = IsaacRNG.game_constructor(inputs.generator_seed, LEVEL_SHIFT_INDEX)
    generator._m6_level_rng = level_rng
    floor_state = FloorGenerationState(
        inputs.stage_seed, target_room_count=inputs.target_room_count,
        level_rng=level_rng, level_generator=generator,
    )
    attempts: list[SecretGenerationAttemptResult] = []

    for attempt_number in range(1, max_attempts + 1):
        floor_state.retry_count = attempt_number - 1
        run_state.boss_pools.begin_attempt()
        start_level = level_rng.seed
        start_generator = generator.rng.seed
        start_boss = run_state.boss_pools.pool_rngs[1].seed
        used_before = tuple(sorted(run_state.special_room_used_bits))
        weights_before = dict(run_state.room_config.weights)
        generator.blocked_positions[:] = [False] * len(generator.blocked_positions)
        generator.generate_once(
            floor_state.target_room_count, inputs.required_dead_ends,
            inputs.allowed_shapes_mask,
            LevelGeneratorRoom(6, 6, RoomShape.ROOMSHAPE_1x1),
        )
        topology = _topology_snapshot(generator, floor_state.target_room_count)
        usable = len(generator.dead_ends) >= inputs.required_dead_ends
        m5 = None
        m6 = None
        if usable:
            m5 = run_post_topology_through_treasure(
                generator, run_state=run_state, floor_state=floor_state,
                entries=entries, profile=profile,
            )
            if m5.completed:
                m6 = run_treasure_to_secret(
                    m5, generator=generator, run_state=run_state,
                    entries=entries, profile=profile,
                )
        elif attempt_number >= 10 and attempt_number % 5 == 0 and floor_state.target_room_count < 64:
            floor_state.target_room_count += 1

        mutations = tuple(
            (key, weights_before.get(key, value), value)
            for key, value in sorted(run_state.room_config.weights.items())
            if weights_before.get(key, value) != value
        )
        attempts.append(SecretGenerationAttemptResult(
            attempt_number, topology.target_room_count, usable, topology,
            start_level, level_rng.seed, start_generator, generator.rng.seed,
            start_boss, run_state.boss_pools.pool_rngs[1].seed,
            used_before, tuple(sorted(run_state.special_room_used_bits)), mutations,
            m5, m6,
        ))
        if m6 is not None and m6.completed:
            run_state.current_stage_lifecycle = "basement1-replayed-to-pre-ultra-boundary"
            return Basement1ThroughSecretResult(
                True, start_seed, difficulty, inputs.stage_seed, tuple(attempts),
                level_rng.seed, generator.rng.seed,
                run_state.boss_pools.pool_rngs[1].seed,
                tuple(sorted(run_state.boss_pools.removed)),
                tuple(sorted(run_state.boss_pools.level_blacklist)),
                tuple(sorted(run_state.room_config.weights.items())),
                tuple(sorted(run_state.special_room_used_bits)), m6.rooms,
            )

    return Basement1ThroughSecretResult(
        False, start_seed, difficulty, inputs.stage_seed, tuple(attempts),
        level_rng.seed, generator.rng.seed,
        run_state.boss_pools.pool_rngs[1].seed,
        tuple(sorted(run_state.boss_pools.removed)),
        tuple(sorted(run_state.boss_pools.level_blacklist)),
        tuple(sorted(run_state.room_config.weights.items())),
        tuple(sorted(run_state.special_room_used_bits)), (),
    )
