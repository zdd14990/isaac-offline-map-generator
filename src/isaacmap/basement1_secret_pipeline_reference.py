"""Mechanical reference continuation from Treasure through Secret."""

from __future__ import annotations

from dataclasses import dataclass
import struct

from .basement1_pipeline_reference import (
    LEVEL_SHIFTS,
    ReferenceConfigTrace,
    ReferenceConditionTrace,
    ReferencePipelineDraw,
    ReferencePostResult,
    _PostState,
    _advance,
    _assign,
    _config_draws,
    _consume,
    run_post_reference,
)
from .basement1_secret_pipeline import (
    InterveningBlockTrace,
    PostTreasureThroughSecretResult,
    SecretConfigRNGTransition,
    SecretDescriptorMutation,
)
from .boss_pool_reference import BossPoolEntryReference, BossPoolRuntimeReference
from .floor_init import derive_basement1_topology_inputs
from .generation_state import CanonicalBasement1Profile, CanonicalCaves1Profile
from .resources import RoomDefinition
from .room_config_reference import (
    RoomConfigEntryReference,
    RoomConfigKey,
    RoomConfigMutableStateReference,
    RoomConfigQueryReference,
    RoomConfigSelectionReference,
    entries_from_definitions_reference,
    select_room_reference,
    select_room_with_stage_fallback_reference,
)
from .secret_reference import (
    ReferenceSecretGeometryState,
    build_secret_forbidden_indices_reference,
    place_secret_room_reference,
)
from .special_rooms import CandidateTrace, GeneratedRoom
from .topology_reference import LevelGeneratorReference, ReferenceRoom


CURSE_SHIFTS = (11, 7, 12)
SECRET_SHIFTS = (1, 5, 16)


@dataclass(frozen=True)
class ReferenceSecretAttempt:
    attempt: int
    target_room_count: int
    usable: bool
    topology_signature: tuple[object, ...]
    start_level: int
    end_level: int
    start_generator: int
    end_generator: int
    start_boss: int
    end_boss: int
    used_before: tuple[int, ...]
    used_after: tuple[int, ...]
    weight_mutations: tuple[tuple[RoomConfigKey, float, float], ...]
    through_treasure: ReferencePostResult | None
    through_secret: PostTreasureThroughSecretResult | None


@dataclass(frozen=True)
class ReferenceBasement1ThroughSecretResult:
    boundary_completed: bool
    attempts: tuple[ReferenceSecretAttempt, ...]
    final_level: int
    final_generator: int
    final_boss: int
    removed: tuple[int, ...]
    pending_blacklist: tuple[int, ...]
    weights: tuple[tuple[RoomConfigKey, float], ...]
    used_bits: tuple[int, ...]


def _topology_signature(generator: LevelGeneratorReference) -> tuple[object, ...]:
    return (
        tuple((r.generation_index, r.column, r.line, int(r.shape), tuple(sorted(r.neighbors)), r.doors, r.distance_from_start) for r in generator.rooms),
        tuple(generator.room_map), tuple(generator.dead_ends),
        tuple(generator.non_dead_ends), tuple(generator.expansion_order),
    )


def _f32(value: float) -> float:
    return struct.unpack("<f", struct.pack("<f", value))[0]


def _unit(value: int) -> float:
    scale = struct.unpack("<f", struct.pack("<I", 0x2F7FFFFE))[0]
    return _f32(_f32(float(value & 0xFFFFFFFF)) * scale)


def _state(post: ReferencePostResult) -> _PostState:
    return _PostState(
        [GeneratedRoom(
            room.generation_index, room.column, room.line, room.shape,
            room.origin_direction, room.link_column, room.link_line,
            room.distance_from_start, room.doors, set(room.neighbors),
            room.room_type, room.variant, room.subtype,
        ) for room in post.rooms],
        list(post.room_map), list(post.dead_ends), post.final_level_rng_state,
    )


def _draw_level(state: _PostState, draws: list[ReferencePipelineDraw], rva: int, reason: str) -> int:
    before = state.level_rng_state
    after = _advance(before, LEVEL_SHIFTS)
    state.level_rng_state = after
    draws.append(ReferencePipelineDraw(rva, "Level._generationRNG", 35, before, after, reason))
    return after


def _draw_private(box: list[int], shifts: tuple[int, int, int], index: int, draws: list[ReferencePipelineDraw], rva: int, identity: str, reason: str) -> int:
    before = box[0]
    after = _advance(before, shifts)
    box[0] = after
    draws.append(ReferencePipelineDraw(rva, identity, index, before, after, reason))
    return after


def _select(
    operation: str,
    seed: int,
    entries: tuple[RoomConfigEntryReference, ...],
    weights: RoomConfigMutableStateReference,
    draws: list[ReferencePipelineDraw],
    configs: list[ReferenceConfigTrace],
    *, room_type: int, subtype: int = -1, reduce: bool = True,
    minimum: int = 1, maximum: int = 10,
) -> RoomConfigEntryReference:
    selection = select_room_reference(
        entries, weights,
        RoomConfigQueryReference(seed, reduce, 0, room_type, subtype=subtype, min_difficulty=minimum, max_difficulty=maximum),
    )
    configs.append(ReferenceConfigTrace(operation, (selection,)))
    _config_draws(draws, operation, (selection,))
    if selection.selected is None:
        raise AssertionError(f"no reference RoomConfig for {operation}")
    return selection.selected


def _descriptor_map(post: ReferencePostResult, entries: tuple[RoomConfigEntryReference, ...]) -> dict[int, RoomConfigEntryReference]:
    by_key = {entry.key: entry for entry in entries}
    result: dict[int, RoomConfigEntryReference] = {}
    if post.boss_config is not None: result[post.boss_room] = by_key[post.boss_config]
    for room_id,key in zip(post.additional_boss_rooms,post.additional_boss_configs): result[room_id]=by_key[key]
    type8 = [trace.selections[-1].selected for trace in post.configs if trace.operation == "RoomType8" and trace.selections[-1].selected is not None]
    for room_id, entry in zip(post.type8_rooms, type8): result[room_id] = entry
    if post.shop_config is not None: result[post.shop_room] = by_key[post.shop_config]
    if post.treasure_config is not None: result[post.treasure_room] = by_key[post.treasure_config]
    for room_id,key in zip(post.treasure_rooms[1:],post.treasure_configs[1:]): result[room_id]=by_key[key]
    return result


def _finish_candidate(
    state: _PostState, entry: RoomConfigEntryReference, operation: str,
    room_id: int, assign: bool, descriptors: dict[int, RoomConfigEntryReference],
    blocks: list[InterveningBlockTrace], before: tuple[int, ...], binary_range: str,
    predicate: str, bit: int | None = None,
) -> int:
    if room_id >= 0:
        if assign:
            _assign(state, room_id, entry); descriptors[room_id] = entry
        else:
            state.dead_ends.append(room_id)
    blocks.append(InterveningBlockTrace(operation, binary_range, entry.room_type, entry.subtype, before, room_id, room_id >= 0 and assign, tuple(state.dead_ends), entry.key, predicate, bit if room_id >= 0 and assign else None))
    return room_id if room_id >= 0 and assign else -1


def run_treasure_to_secret_reference(
    post: ReferencePostResult,
    *, generator: LevelGeneratorReference,
    weights: RoomConfigMutableStateReference,
    entries: tuple[RoomConfigEntryReference, ...],
    profile,
    used_bits: set[int],
) -> PostTreasureThroughSecretResult:
    profile.validate()
    state = _state(post)
    draws: list[ReferencePipelineDraw] = []
    configs: list[ReferenceConfigTrace] = []
    conditions: list[ReferenceConditionTrace] = []
    blocks: list[InterveningBlockTrace] = []
    descriptors = _descriptor_map(post, entries)

    seed = _draw_level(state, draws, 0x0033A961, "Planetarium RoomConfig")
    planetarium_gate = (
        profile.level_stage < 7
        or (profile.level_stage < 9 and 0x6e in profile.collectible_ids)
        or profile.level_stage == 10
    )
    entry = None
    rid = -1
    place = False
    if planetarium_gate:
        entry = _select("Planetarium", seed, entries, weights, draws, configs, room_type=24)
        before = tuple(state.dead_ends)
        rid = _consume(state, entry, "GetNewEndRoom(Planetarium)")
        if rid >= 0 and not ({24, 4} & profile.visited_room_types):
            chance = _draw_level(state, draws, 0x0033AA9B, "Planetarium chance")
            place = _unit(chance) < _f32(profile.planetarium_chance) and profile.planetarium_unlocked
        _finish_candidate(state, entry, "Planetarium", rid, place, descriptors, blocks, before, "0x0033A8F7..0x0033AB45", f"gate={planetarium_gate}; visited types 24/4 absent; unlocked; f32(Level.Next()) < {profile.planetarium_chance}")
    else:
        blocks.append(InterveningBlockTrace("Planetarium", "0x0033A8F7..0x0033AB45", 24, 0, tuple(state.dead_ends), -1, False, tuple(state.dead_ends), None, f"gate={planetarium_gate}; skipped"))

    first = _draw_level(state, draws, 0x0033AB94, "Dice/Sacrifice first choice")
    if first % 50 == 0: room_type = 21
    else:
        second = _draw_level(state, draws, 0x0033ABFB, "Dice/Sacrifice second choice")
        room_type = 21 if second % 5 == 0 and profile.player0_max_hearts > 1 else 13
    seed = _draw_level(state, draws, 0x0033ACC6 if room_type == 21 else 0x0033AE4E, "Dice/Sacrifice RoomConfig")
    name = "Dice" if room_type == 21 else "Sacrifice"
    entry = _select(name, seed, entries, weights, draws, configs, room_type=room_type)
    before = tuple(state.dead_ends); rid = _consume(state, entry, f"GetNewEndRoom({name})")
    place = False
    if rid >= 0 and room_type not in profile.visited_room_types:
        decision = _draw_level(state, draws, 0x0033AD68, "Dice/Sacrifice primary gate")
        place = decision % 7 == 0
        if not place:
            decision = _draw_level(state, draws, 0x0033AE83, "Dice/Sacrifice secondary gate")
            place = (decision & 3) == 0 and profile.player0_full_health
    _finish_candidate(state, entry, name, rid, place, descriptors, blocks, before, "0x0033AB45..0x0033AF08", "1/50 Dice, else 1/5 with hearts; then 1/7 or 1/4 full-health gate")

    subtype_draw = _draw_level(state, draws, 0x0033AF8E, "Library subtype")
    subtype = subtype_draw % (profile.library_subtype_max + 1)
    seed = _draw_level(state, draws, 0x0033AFF7, "Library RoomConfig")
    entry = _select("Library", seed, entries, weights, draws, configs, room_type=12, subtype=subtype, reduce=False)
    before = tuple(state.dead_ends); rid = _consume(state, entry, "GetNewEndRoom(Library)")
    place = False
    if rid >= 0 and 12 not in profile.visited_room_types:
        decision = _draw_level(state, draws, 0x0033B08F, "Library primary gate")
        place = decision % 20 == 0
        if not place:
            decision = _draw_level(state, draws, 0x0033B108, "Library secondary gate")
            place = (decision & 3) == 0 and 8 in used_bits
    _finish_candidate(state, entry, "Library", rid, place, descriptors, blocks, before, "0x0033AF71..0x0033B10D", "1/20, or 1/4 with Game+0x26548 bit 8; no weight decay")

    private = [_draw_level(state, draws, 0x0033B166, "Curse private seed")]
    seed = _draw_private(private, CURSE_SHIFTS, 66, draws, 0x0033B200, "Curse.private", "Curse RoomConfig")
    entry = _select("Curse", seed, entries, weights, draws, configs, room_type=10, subtype=0)
    before = tuple(state.dead_ends); rid = _consume(state, entry, "GetNewEndRoom(Curse)")
    place = rid >= 0 and 10 not in profile.visited_room_types
    if place:
        value = _draw_private(private, CURSE_SHIFTS, 66, draws, 0x0033B301, "Curse.private", "Curse descriptor seed")
        if value & 1: _draw_private(private, CURSE_SHIFTS, 66, draws, 0x0033B351, "Curse.private", "Curse odd-state extra advance")
    _finish_candidate(state, entry, "Curse", rid, place, descriptors, blocks, before, "0x0033B10D..0x0033B3A8", "fresh canonical profile always assigns a compatible candidate")

    subtype_bits = ((2, 9), (3, 10), (1, 11), (0, 12), (5, 13), (6, 14))
    available = [sub for sub, bit in subtype_bits if bit not in used_bits]
    pick = _draw_level(state, draws, 0x0033B7F2, "MiniBoss subtype")
    subtype = available[pick % len(available)]
    seed = _draw_level(state, draws, 0x0033B8AB, "MiniBoss exact-difficulty RoomConfig")
    selection = select_room_reference(entries, weights, RoomConfigQueryReference(seed, True, 0, 6, subtype=subtype, min_difficulty=1, max_difficulty=1))
    configs.append(ReferenceConfigTrace("MiniBoss", (selection,))); _config_draws(draws, "MiniBoss", (selection,))
    entry = selection.selected
    if entry is None:
        seed = _draw_level(state, draws, 0x0033B918, "MiniBoss fallback RoomConfig")
        entry = _select("MiniBossFallback", seed, entries, weights, draws, configs, room_type=6, subtype=subtype)
    before = tuple(state.dead_ends); rid = _consume(state, entry, "GetNewEndRoom(MiniBoss)")
    place = False
    if rid >= 0 and 6 not in profile.visited_room_types:
        decision = _draw_level(state, draws, 0x0033B9C3, "MiniBoss primary gate")
        place = (decision & 3) == 0
        if not place:
            decision = _draw_level(state, draws, 0x0033BA27, "MiniBoss stage-one fallback")
            place = profile.level_stage == 1 and decision % 3 == 0
    bit = dict(subtype_bits)[subtype]
    if rid >= 0 and place: used_bits.add(bit)
    _finish_candidate(state, entry, "MiniBoss", rid, place, descriptors, blocks, before, "0x0033B3A8..0x0033BBAE", "ordered unused-subtype vector; 1/4 or Basement-I 1/3 fallback", bit)

    seed = _draw_level(state, draws, 0x0033BC1E, "Challenge RoomConfig")
    entry = _select("Challenge", seed, entries, weights, draws, configs, room_type=11, subtype=0)
    before = tuple(state.dead_ends); rid = _consume(state, entry, "GetNewEndRoom(Challenge)")
    place = False
    if rid >= 0 and 11 not in profile.visited_room_types:
        decision = _draw_level(state, draws, 0x0033BCF5, "Challenge gate")
        place = ((decision & 1) == 0 or profile.level_stage >= 3) and profile.player0_full_health and profile.level_stage >= 2
    _finish_candidate(state, entry, "Challenge", rid, place, descriptors, blocks, before, "0x0033BBAE..0x0033BD87", "even draw or Stage >= 3; eligible player; Stage >= 2")

    first = _draw_level(state, draws, 0x0033BDD2, "Chest/Arcade first choice")
    if first % 10 == 0: room_type = 20
    else:
        second = _draw_level(state, draws, 0x0033BE31, "Chest/Arcade second choice")
        room_type = 20 if second % 3 == 0 and profile.player0_max_hearts > 1 else 9
    seed = _draw_level(state, draws, 0x0033BF11 if room_type == 20 else 0x0033BFB6, "Chest/Arcade RoomConfig")
    name = "Chest" if room_type == 20 else "Arcade"
    entry = _select(name, seed, entries, weights, draws, configs, room_type=room_type, subtype=-1 if room_type == 20 else 0)
    before = tuple(state.dead_ends); rid = _consume(state, entry, f"GetNewEndRoom({name})")
    place = rid >= 0 and profile.level_stage == 2 and room_type == 20 and profile.player0_max_hearts >= 2
    _finish_candidate(state, entry, name, rid, place, descriptors, blocks, before, "0x0033BD87..0x0033C0B6", "canonical Stage 2 assigns Chest; zero-coin Arcade remains unassigned")

    _draw_level(state, draws, 0x0033C1C5, "Isaac/Barren type choice")
    seed = _draw_level(state, draws, 0x0033C1E5, "Isaac RoomConfig")
    entry = _select("Isaac", seed, entries, weights, draws, configs, room_type=18)
    before = tuple(state.dead_ends); rid = _consume(state, entry, "GetNewEndRoom(Isaac)")
    place = False
    if rid >= 0 and 18 not in profile.visited_room_types:
        decision = _draw_level(state, draws, 0x0033C336, "Isaac primary gate")
        place = decision % 50 == 0
        if not place: _draw_level(state, draws, 0x0033C393, "Isaac low-health fallback")
    _finish_candidate(state, entry, "Isaac", rid, place, descriptors, blocks, before, "0x0033C0F0..0x0033C416", "1/50; low-health 1/5 fallback is false for fresh Isaac")

    conditions.extend((
        ReferenceConditionTrace("0x0033C416..0x0033C4D1", "alternate-path first-half mandatory end room", False, "skip"),
        ReferenceConditionTrace("0x0033C554..0x0033C640", "alternate-path second-half collectible-626 end room", False, "skip"),
        ReferenceConditionTrace("0x0033C645..0x0033C69E", "route-specific end-room state flag", False, "skip"),
    ))

    secret_seed = post.snapshot
    selections = select_room_with_stage_fallback_reference(entries, weights, RoomConfigQueryReference(secret_seed, True, profile.room_config_stage, 7, subtype=-1), profile.fallback_room_config_stage)
    configs.append(ReferenceConfigTrace("Secret", selections)); _config_draws(draws, "Secret", selections)
    secret_entry = selections[-1].selected
    if secret_entry is None: raise AssertionError("no reference Secret RoomConfig")
    forbidden = build_secret_forbidden_indices_reference(state.rooms, descriptors, level_stage=profile.level_stage)
    descriptor_count_before = len(descriptors)
    dead_ends_before_secret = tuple(state.dead_ends)
    geometry_state = ReferenceSecretGeometryState(state.rooms, state.room_map, list(generator.blocked_positions), generator.rng.seed)
    geometry = place_secret_room_reference(geometry_state, forbidden)
    generator.rng.seed = geometry_state.generator_rng_state
    if geometry.room_id >= 0:
        _assign(state, geometry.room_id, secret_entry); descriptors[geometry.room_id] = secret_entry
    descriptor_mutation = SecretDescriptorMutation(
        geometry.room_id >= 0, geometry.room_id,
        descriptor_count_before if geometry.room_id >= 0 else -1,
        geometry.grid_index, geometry.grid_index,
        1 if geometry.room_id >= 0 else 0,
        7 if geometry.room_id >= 0 else 0,
        descriptor_count_before, len(descriptors),
        dead_ends_before_secret, tuple(state.dead_ends),
    )
    post_private = _advance(secret_seed, SECRET_SHIFTS)
    secret_rng = (SecretConfigRNGTransition(0, 0x0033C802, secret_seed, post_private, 1, "advance saved Secret iteration seed after placement attempt"),)
    conditions.append(ReferenceConditionTrace(
        "0x0033C83B..0x0033C902",
        "post-Secret Stage 11 ORIGINAL mandatory subtype-3 end room",
        False,
        "skip; next canonical operation is Ultra Secret entry",
    ))
    return PostTreasureThroughSecretResult(
        True, None, tuple(blocks), geometry.room_id, secret_entry.key,
        tuple(state.rooms), tuple(state.room_map), tuple(state.dead_ends),
        tuple(generator.blocked_positions),
        tuple(sorted((room_id, entry.key) for room_id, entry in descriptors.items())),
        tuple(draws), tuple(configs), tuple(state.candidate_trace), tuple(conditions),
        secret_rng, geometry, descriptor_mutation,
        state.level_rng_state, generator.rng.seed,
        tuple(sorted(used_bits)),
    )


def generate_basement1_through_secret_reference(
    start_seed: int, difficulty: str, *,
    boss_entries: tuple[BossPoolEntryReference, ...],
    special_definitions: tuple[RoomDefinition, ...],
    basement_definitions: tuple[RoomDefinition, ...],
    max_attempts: int = 100,
) -> ReferenceBasement1ThroughSecretResult:
    profile = CanonicalBasement1Profile(difficulty)
    profile.validate()
    inputs = derive_basement1_topology_inputs(start_seed, difficulty)
    entries = entries_from_definitions_reference(special_definitions, stage=0) + entries_from_definitions_reference(basement_definitions, stage=1)
    weights = RoomConfigMutableStateReference(); weights.reset_pool(entries)
    bosses = BossPoolRuntimeReference.fresh_basement(start_seed, boss_entries)
    generator = LevelGeneratorReference(inputs.generator_seed, [])
    level_state = inputs.generator_seed
    target = inputs.target_room_count
    used_bits: set[int] = set(profile.special_room_used_bits)
    attempts: list[ReferenceSecretAttempt] = []
    for number in range(1, max_attempts + 1):
        attempt_target = target
        bosses.begin_attempt()
        start_level, start_gen, start_boss = level_state, generator.rng.seed, bosses.pool_states[1]
        used_before = tuple(sorted(used_bits)); before_weights = dict(weights.weights)
        generator.blocked_positions[:] = [False] * 169; generator.attempt = number
        generator.generate_once(target, inputs.required_dead_ends, inputs.allowed_shapes_mask, ReferenceRoom(6, 6, 1))
        signature = _topology_signature(generator)
        usable = len(generator.dead_ends) >= inputs.required_dead_ends
        m5 = None; m6 = None
        if usable:
            m5 = run_post_reference(generator, level_state, bosses, weights, entries, profile)
            level_state = m5.final_level_rng_state
            if m5.completed:
                m6 = run_treasure_to_secret_reference(m5, generator=generator, weights=weights, entries=entries, profile=profile, used_bits=used_bits)
                level_state = m6.final_level_rng_state
        elif number >= 10 and number % 5 == 0 and target < 64:
            target += 1
        mutations = tuple((key, before_weights.get(key, value), value) for key, value in sorted(weights.weights.items()) if before_weights.get(key, value) != value)
        attempts.append(ReferenceSecretAttempt(number, attempt_target, usable, signature, start_level, level_state, start_gen, generator.rng.seed, start_boss, bosses.pool_states[1], used_before, tuple(sorted(used_bits)), mutations, m5, m6))
        if m6 is not None and m6.completed:
            return ReferenceBasement1ThroughSecretResult(True, tuple(attempts), level_state, generator.rng.seed, bosses.pool_states[1], tuple(sorted(bosses.removed)), tuple(sorted(bosses.level_blacklist)), tuple(sorted(weights.weights.items())), tuple(sorted(used_bits)))
    return ReferenceBasement1ThroughSecretResult(False, tuple(attempts), level_state, generator.rng.seed, bosses.pool_states[1], tuple(sorted(bosses.removed)), tuple(sorted(bosses.level_blacklist)), tuple(sorted(weights.weights.items())), tuple(sorted(used_bits)))
