"""Mechanical Basement I reference through Treasure for the frozen PE."""

from __future__ import annotations

from dataclasses import dataclass, field

from .boss_pool_reference import (
    BossPoolEntryReference,
    BossPoolRuntimeReference,
    BossPoolRuntimeSelectionReference,
)
from .floor_init import derive_basement1_topology_inputs
from .generation_state import (
    CanonicalBasement1Profile,
    CanonicalCaves1Profile,
)
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
from .special_rooms import CandidateTrace, GeneratedRoom
from .special_room_geometry import EndRoomGeometryEvent
from .special_room_geometry_reference import reshape_end_room_reference
from .topology_reference import LevelGeneratorReference, ReferenceRoom


UINT32_MASK = 0xFFFFFFFF
LEVEL_SHIFTS = (5, 9, 7)
BOSS_SHIFTS = (5, 15, 17)
TYPE8_SHIFTS = (2, 5, 15)
SHOP_SHIFTS = (3, 3, 26)


def _advance(state: int, shifts: tuple[int, int, int]) -> int:
    if state == 0:
        raise ValueError("zero RNG state")
    state ^= state >> shifts[0]
    state ^= (state << shifts[1]) & UINT32_MASK
    state ^= state >> shifts[2]
    return state & UINT32_MASK


@dataclass(frozen=True)
class ReferencePipelineDraw:
    rva: int
    identity: str
    shift_index: int
    pre: int
    post: int
    reason: str


@dataclass
class _PostState:
    rooms: list[GeneratedRoom]
    room_map: list[int]
    dead_ends: list[int]
    level_rng_state: int
    candidate_trace: list[CandidateTrace] = field(default_factory=list)
    geometry_trace: list[EndRoomGeometryEvent] = field(default_factory=list)


@dataclass(frozen=True)
class ReferenceConfigTrace:
    operation: str
    selections: tuple[RoomConfigSelectionReference, ...]


@dataclass(frozen=True)
class ReferenceConditionTrace:
    binary_range: str
    condition: str
    value: bool
    consequence: str


@dataclass(frozen=True)
class ReferencePostResult:
    completed: bool
    abort: str | None
    boss: BossPoolRuntimeSelectionReference
    boss_room: int
    boss_config: RoomConfigKey | None
    type8_rooms: tuple[int, ...]
    shop_room: int
    shop_config: RoomConfigKey | None
    treasure_room: int
    treasure_config: RoomConfigKey | None
    snapshot: int
    rooms: tuple[GeneratedRoom, ...]
    room_map: tuple[int, ...]
    dead_ends: tuple[int, ...]
    draws: tuple[ReferencePipelineDraw, ...]
    configs: tuple[ReferenceConfigTrace, ...]
    candidates: tuple[CandidateTrace, ...]
    geometry: tuple[EndRoomGeometryEvent, ...]
    conditions: tuple[ReferenceConditionTrace, ...]
    final_level_rng_state: int
    additional_bosses: tuple[BossPoolRuntimeSelectionReference, ...] = ()
    additional_boss_rooms: tuple[int, ...] = ()
    additional_boss_configs: tuple[RoomConfigKey, ...] = ()
    treasure_rooms: tuple[int, ...] = ()
    treasure_configs: tuple[RoomConfigKey, ...] = ()


@dataclass(frozen=True)
class ReferenceGenerationAttempt:
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
    blacklist: tuple[int, ...]
    removed: tuple[int, ...]
    weight_mutations: tuple[tuple[RoomConfigKey, float, float], ...]
    post: ReferencePostResult | None


@dataclass(frozen=True)
class ReferenceBasement1Result:
    completed: bool
    attempts: tuple[ReferenceGenerationAttempt, ...]
    final_level: int
    final_generator: int
    final_boss: int
    removed: tuple[int, ...]
    weights: tuple[tuple[RoomConfigKey, float], ...]


def _room_signature(generator: LevelGeneratorReference) -> tuple[object, ...]:
    return (
        tuple((r.generation_index, r.column, r.line, int(r.shape), tuple(sorted(r.neighbors)), r.doors, r.distance_from_start) for r in generator.rooms),
        tuple(generator.room_map), tuple(generator.dead_ends),
        tuple(generator.non_dead_ends), tuple(generator.expansion_order),
    )


def _post_state(generator: LevelGeneratorReference, level_state: int) -> _PostState:
    return _PostState(
        [GeneratedRoom(
            int(r.generation_index), int(r.column), int(r.line), int(r.shape),
            int(r.origin_neighbor_connect_dir), int(r.link_column), int(r.link_line),
            int(r.distance_from_start), int(r.doors), set(r.neighbors),
        ) for r in generator.rooms],
        list(generator.room_map), list(generator.dead_ends), level_state,
    )


def _draw(state: _PostState, draws: list[ReferencePipelineDraw], shifts, index, rva, identity, reason, *, private: list[int] | None = None) -> int:
    pre = state.level_rng_state if private is None else private[0]
    post = _advance(pre, shifts)
    if private is None: state.level_rng_state = post
    else: private[0] = post
    draws.append(ReferencePipelineDraw(rva, identity, index, pre, post, reason))
    return post


def _config_draws(draws: list[ReferencePipelineDraw], operation: str, selections: tuple[RoomConfigSelectionReference, ...]) -> None:
    for selection in selections:
        for draw in selection.draws:
            draws.append(ReferencePipelineDraw(draw.binary_rva, f"RoomConfig.local({operation})", 7, draw.pre_state, draw.post_state, draw.reason))


def _consume(state: _PostState, entry: RoomConfigEntryReference, operation: str, minimum: int | None = None) -> int:
    original=tuple(state.dead_ends); pos=0
    while pos < len(state.dead_ends):
        rid=state.dead_ends[pos]
        accepted=(minimum is None or state.rooms[rid].distance_from_start > minimum) and reshape_end_room_reference(state,rid,entry.shape,entry.door_mask,events=state.geometry_trace)
        after=tuple(state.dead_ends[:pos]+state.dead_ends[pos+1:] if accepted else state.dead_ends)
        state.candidate_trace.append(CandidateTrace(operation,original,rid,accepted,after))
        if accepted: del state.dead_ends[pos]; return rid
        pos += 1
    return -1


def _assign(state: _PostState, rid: int, entry: RoomConfigEntryReference) -> None:
    state.rooms[rid].room_type=entry.room_type; state.rooms[rid].variant=entry.variant; state.rooms[rid].subtype=entry.subtype


def _select_boss_config_reference(
    state,
    draws,
    configs,
    weights,
    entries,
    boss,
    operation,
    seed_rva,
):
    seed=_draw(state,draws,LEVEL_SHIFTS,35,seed_rva,"Level._generationRNG",f"{operation} config seed")
    private=[seed]; left=50
    while True:
        selector=_draw(state,draws,BOSS_SHIFTS,39,0x0033930E,f"{operation} RoomConfig.private",f"{operation} config iteration",private=private)
        selection=select_room_reference(entries,weights,RoomConfigQueryReference(selector,True,0,5,subtype=abs(boss.boss_id)))
        configs.append(ReferenceConfigTrace(operation,(selection,))); _config_draws(draws,operation,(selection,)); entry=selection.selected
        if entry is None: return None
        if not 3700 <= entry.variant < 3850 or left <= 0: return entry
        left -= 1


def _sync_reference_generator(generator, state):
    dead=set(state.dead_ends)
    generator.rooms=[ReferenceRoom(
        room.column,room.line,int(room.shape),room.generation_index,room.doors,
        room.origin_direction,room.origin_direction,room.link_column,room.link_line,
        set(room.neighbors),room.generation_index in dead,room.distance_from_start,
    ) for room in state.rooms]
    generator.room_map[:]=state.room_map
    generator.dead_ends[:]=state.dead_ends


def _prepare_xl_extra_boss_room_reference(state,generator,primary_room,required_doors):
    _sync_reference_generator(generator,state)
    generator.num_boss_rooms=1
    candidates=generator.get_neighbor_candidates(primary_room,False)
    generator.shuffle_candidates(candidates,primary_room)
    pending=-1
    for candidate in candidates:
        if not generator.is_pos_free((candidate.column,candidate.line),candidate.shape): continue
        if generator.count_neighbor_links(candidate.link_position)>=2: continue
        if required_doors & (1 << candidate.origin_neighbor_door_slot)==0: continue
        placed=generator.place_room(candidate); placed.dead_end=True
        pending=placed.generation_index; generator.next_boss_room_index=pending
        break
    for room in generator.rooms: generator.update_room_connections(room)
    for rid,room in enumerate(state.rooms):
        room.doors=generator.rooms[rid].doors; room.neighbors=set(generator.rooms[rid].neighbors)
    if pending>=0:
        placed=generator.rooms[pending]
        state.rooms.append(GeneratedRoom(
            placed.generation_index,placed.column,placed.line,placed.shape,
            placed.origin_neighbor_connect_dir,placed.link_column,placed.link_line,
            placed.distance_from_start,placed.doors,set(placed.neighbors),
        ))
        state.room_map[:]=generator.room_map
    return pending


def _mark_boss_perimeter_reference(generator,state,rid):
    offsets=((0,0),(-1,0),(0,-1),(1,0),(0,1))
    for column,line in state.rooms[rid].cells:
        for dx,dy in offsets:
            x=column+dx; y=line+dy
            if 0<=x<13 and 0<=y<13: generator.blocked_positions[y*13+x]=True


def _result(state, completed, abort, boss, boss_room, boss_entry, type8, shop_room, shop_entry, treasure_room, treasure_entry, snapshot, draws, configs, conditions, *, additional_bosses=(), additional_boss_rooms=(), additional_boss_configs=(), treasure_rooms=(), treasure_configs=()):
    return ReferencePostResult(
        completed,abort,boss,boss_room,None if boss_entry is None else boss_entry.key,tuple(type8),
        shop_room,None if shop_entry is None else shop_entry.key,
        treasure_room,None if treasure_entry is None else treasure_entry.key,snapshot,
        tuple(state.rooms),tuple(state.room_map),tuple(state.dead_ends),tuple(draws),tuple(configs),
        tuple(state.candidate_trace),tuple(state.geometry_trace),tuple(conditions),
        state.level_rng_state,
        tuple(additional_bosses),tuple(additional_boss_rooms),tuple(additional_boss_configs),
        tuple(treasure_rooms),tuple(treasure_configs),
    )


def run_post_reference(generator, level_state, boss_state, weights, entries, profile):
    state=_post_state(generator,level_state); draws=[]; configs=[]; conditions=[]
    profile.validate()
    if profile.level_stage not in (1, 2, 3, 4, 5, 6, 7, 8) or (
        profile.is_xl and profile.level_stage not in (1, 3, 5, 7)
    ) or 589 in profile.collectible_ids:
        raise ValueError("through-Treasure reference supports canonical Basement I/II/Caves I/II/Depths I/II/Womb I/II")
    boss=boss_state.select_floor_boss(
        profile.level_stage, profile.stage_type, profile.room_config_stage
    )
    boss_entry=_select_boss_config_reference(state,draws,configs,weights,entries,boss,"Boss",0x003394A4)
    if boss_entry is None: return _result(state,False,"Boss RoomConfig",boss,-1,None,[],-1,None,-1,None,0,draws,configs,conditions)
    boss_room=_consume(state,boss_entry,"DetermineBossRoom",1)
    if boss_room < 0: return _result(state,False,"Boss geometry",boss,-1,boss_entry,[],-1,None,-1,None,0,draws,configs,conditions)
    if not reshape_end_room_reference(state,boss_room,boss_entry.shape,boss_entry.door_mask,events=state.geometry_trace): return _result(state,False,"Boss geometry validation",boss,boss_room,boss_entry,[],-1,None,-1,None,0,draws,configs,conditions)
    _assign(state,boss_room,boss_entry)

    conditions.append(ReferenceConditionTrace("0x00339540..0x003398AB","additional multi-boss Stage 12 block",False,"skip"))
    additional_bosses=[]; additional_boss_rooms=[]; additional_boss_configs=[]; last_boss=boss_room
    if profile.is_xl:
        pending=_prepare_xl_extra_boss_room_reference(state,generator,boss_room,boss_entry.door_mask)
        level_snapshot=state.level_rng_state
        second=boss_state.select_floor_boss(
            profile.level_stage + 1, profile.stage_type, profile.room_config_stage
        ); additional_bosses.append(second)
        second_entry=_select_boss_config_reference(state,draws,configs,weights,entries,second,"Boss[1]",0x00339951)
        if second_entry is None:
            return _result(state,False,"Boss[1] RoomConfig",boss,boss_room,boss_entry,[],-1,None,-1,None,0,draws,configs,conditions,additional_bosses=additional_bosses)
        if pending<0 or not reshape_end_room_reference(state,pending,second_entry.shape,second_entry.door_mask,events=state.geometry_trace):
            return _result(state,False,"Boss[1] geometry",boss,boss_room,boss_entry,[],-1,None,-1,None,0,draws,configs,conditions,additional_bosses=additional_bosses)
        _assign(state,pending,second_entry); additional_boss_rooms.append(pending); additional_boss_configs.append(second_entry.key)
        generator.num_boss_rooms=2; generator.next_boss_room_index=-1
        state.level_rng_state=level_snapshot; last_boss=pending
        conditions.append(ReferenceConditionTrace("0x00339926..0x00339A0D","effective XL",True,"place second Boss; restore Level RNG only after success"))
    else:
        conditions.append(ReferenceConditionTrace("0x00339926..0x00339A0D","effective XL",False,"skip"))
    if profile.level_stage==3:
        _mark_boss_perimeter_reference(generator,state,last_boss)

    seed=_draw(state,draws,LEVEL_SHIFTS,35,0x00339A87,"Level._generationRNG","Type8 seed"); private=[seed]; type8=[]
    for iteration in range(1):
        selector=_draw(state,draws,TYPE8_SHIFTS,9,0x00339B1E,"RoomType8.private","Type8 iteration",private=private)
        selection=select_room_reference(entries,weights,RoomConfigQueryReference(selector,True,0,8,subtype=-1))
        configs.append(ReferenceConfigTrace("RoomType8",(selection,))); _config_draws(draws,"RoomType8",(selection,)); entry=selection.selected
        if entry is None: return _result(state,False,"RoomType8 RoomConfig",boss,boss_room,boss_entry,type8,-1,None,-1,None,0,draws,configs,conditions,additional_bosses=additional_bosses,additional_boss_rooms=additional_boss_rooms,additional_boss_configs=additional_boss_configs)
        rid=_consume(state,entry,"GetNewEndRoom(RoomType8)")
        if rid < 0: return _result(state,False,"RoomType8 geometry",boss,boss_room,boss_entry,type8,-1,None,-1,None,0,draws,configs,conditions,additional_bosses=additional_bosses,additional_boss_rooms=additional_boss_rooms,additional_boss_configs=additional_boss_configs)
        _assign(state,rid,entry); type8.append(rid)

    snapshot=_draw(state,draws,LEVEL_SHIFTS,35,0x00339BE7,"Level._generationRNG","post-Type8 snapshot")
    conditions.append(ReferenceConditionTrace("0x00339C0A..0x00339C81",f"ordinary Stage {profile.level_stage} Shop eligibility",True,"enter Shop"))
    conditions.append(ReferenceConditionTrace("0x00339CAA..0x00339CD1","fresh Shop visit/count state",True,"enter Shop"))
    shop_seed=_draw(state,draws,LEVEL_SHIFTS,35,0x00339DB4,"Level._generationRNG","Shop private seed"); private=[shop_seed]
    for rva,reason in zip((0x00339E04,0x00339E52,0x00339EB2,0x00339F46),("shop count 1","shop count 2","shop route parity","shop collectible subtype")):
        _draw(state,draws,SHOP_SHIFTS,19,rva,"Shop subtype.private",reason,private=private)
    shop_selector=_draw(state,draws,LEVEL_SHIFTS,35,0x0033A1C7,"Level._generationRNG","Shop config")
    shop_sel=select_room_reference(entries,weights,RoomConfigQueryReference(shop_selector,True,0,2,subtype=11)); configs.append(ReferenceConfigTrace("Shop",(shop_sel,))); _config_draws(draws,"Shop",(shop_sel,)); shop_entry=shop_sel.selected
    if shop_entry is None: return _result(state,False,"Shop RoomConfig",boss,boss_room,boss_entry,type8,-1,None,-1,None,snapshot,draws,configs,conditions,additional_bosses=additional_bosses,additional_boss_rooms=additional_boss_rooms,additional_boss_configs=additional_boss_configs)
    shop_room=_consume(state,shop_entry,"GetNewEndRoom(Shop)")
    if shop_room < 0: return _result(state,False,"Shop geometry",boss,boss_room,boss_entry,type8,-1,shop_entry,-1,None,snapshot,draws,configs,conditions,additional_bosses=additional_bosses,additional_boss_rooms=additional_boss_rooms,additional_boss_configs=additional_boss_configs)
    _assign(state,shop_room,shop_entry)

    conditions.append(ReferenceConditionTrace("0x0033A2C3..0x0033A383",f"ordinary Stage {profile.level_stage} Treasure eligibility",True,"enter Treasure"))
    treasure_rooms=[]; treasure_configs=[]; treasure_entries=[]; treasure_entry=None; first_snapshot=None
    for iteration in range(2 if profile.is_xl else 1):
        operation="Treasure" if iteration==0 else f"Treasure[{iteration}]"
        chance=_draw(state,draws,LEVEL_SHIFTS,35,0x0033A455,"Level._generationRNG",f"{operation} subtype probability")
        if chance % 100 == 0: subtype=1
        else: _draw(state,draws,LEVEL_SHIFTS,35,0x0033A4B8,"Level._generationRNG",f"{operation} chance path"); subtype=0
        selector=_draw(state,draws,LEVEL_SHIFTS,35,0x0033A76B,"Level._generationRNG",f"{operation} config")
        sels=select_room_with_stage_fallback_reference(entries,weights,RoomConfigQueryReference(selector,True,profile.room_config_stage,4,subtype=subtype),profile.fallback_room_config_stage)
        configs.append(ReferenceConfigTrace(operation,sels)); _config_draws(draws,operation,sels); treasure_entry=sels[-1].selected
        if treasure_entry is None:
            return _result(state,False,f"{operation} RoomConfig",boss,boss_room,boss_entry,type8,shop_room,shop_entry,-1,None,snapshot,draws,configs,conditions,additional_bosses=additional_bosses,additional_boss_rooms=additional_boss_rooms,additional_boss_configs=additional_boss_configs,treasure_rooms=treasure_rooms,treasure_configs=treasure_configs)
        treasure_room=_consume(state,treasure_entry,f"GetNewEndRoom({operation})")
        if treasure_room < 0:
            return _result(state,False,f"{operation} geometry",boss,boss_room,boss_entry,type8,shop_room,shop_entry,-1,treasure_entry,snapshot,draws,configs,conditions,additional_bosses=additional_bosses,additional_boss_rooms=additional_boss_rooms,additional_boss_configs=additional_boss_configs,treasure_rooms=treasure_rooms,treasure_configs=treasure_configs)
        _assign(state,treasure_room,treasure_entry); treasure_rooms.append(treasure_room); treasure_configs.append(treasure_entry.key); treasure_entries.append(treasure_entry)
        if iteration==0: first_snapshot=state.level_rng_state
    if profile.is_xl:
        state.level_rng_state=first_snapshot
        conditions.append(ReferenceConditionTrace("0x0033A8A1..0x0033A8EC","effective XL Treasure count",True,"place second Treasure; restore Level RNG only after success"))
    return _result(state,True,None,boss,boss_room,boss_entry,type8,shop_room,shop_entry,treasure_rooms[0],treasure_entries[0],snapshot,draws,configs,conditions,additional_bosses=additional_bosses,additional_boss_rooms=additional_boss_rooms,additional_boss_configs=additional_boss_configs,treasure_rooms=treasure_rooms,treasure_configs=treasure_configs)


def generate_basement1_through_treasure_reference(start_seed: int,difficulty: str,*,boss_entries: tuple[BossPoolEntryReference,...],special_definitions: tuple[RoomDefinition,...],basement_definitions: tuple[RoomDefinition,...],max_attempts: int=100) -> ReferenceBasement1Result:
    profile=CanonicalBasement1Profile(difficulty); profile.validate(); inputs=derive_basement1_topology_inputs(start_seed,difficulty)
    entries=entries_from_definitions_reference(special_definitions,stage=0)+entries_from_definitions_reference(basement_definitions,stage=1)
    weights=RoomConfigMutableStateReference(); weights.reset_pool(entries)
    bosses=BossPoolRuntimeReference.fresh_basement(start_seed,boss_entries)
    generator=LevelGeneratorReference(inputs.generator_seed,[]); level_state=inputs.generator_seed; target=inputs.target_room_count; attempts=[]
    for number in range(1,max_attempts+1):
        attempt_target=target
        bosses.begin_attempt(); start_level=level_state; start_gen=generator.rng.seed; start_boss=bosses.pool_states[1]; before=dict(weights.weights)
        generator.blocked_positions[:]=[False]*169; generator.attempt=number
        generator.generate_once(target,inputs.required_dead_ends,inputs.allowed_shapes_mask,ReferenceRoom(6,6,1))
        usable=len(generator.dead_ends)>=inputs.required_dead_ends; post=None
        if usable:
            post=run_post_reference(generator,level_state,bosses,weights,entries,profile); level_state=post.final_level_rng_state
        elif number>=10 and number%5==0 and target<64: target+=1
        mutations=tuple((k,before.get(k,v),v) for k,v in sorted(weights.weights.items()) if before.get(k,v)!=v)
        attempts.append(ReferenceGenerationAttempt(number,attempt_target,usable,_room_signature(generator),start_level,level_state,start_gen,generator.rng.seed,start_boss,bosses.pool_states[1],tuple(sorted(bosses.level_blacklist)),tuple(sorted(bosses.removed)),mutations,post))
        if post is not None and post.completed:
            bosses.commit_floor(); return ReferenceBasement1Result(True,tuple(attempts),level_state,generator.rng.seed,bosses.pool_states[1],tuple(sorted(bosses.removed)),tuple(sorted(weights.weights.items())))
    return ReferenceBasement1Result(False,tuple(attempts),level_state,generator.rng.seed,bosses.pool_states[1],tuple(sorted(bosses.removed)),tuple(sorted(weights.weights.items())))
