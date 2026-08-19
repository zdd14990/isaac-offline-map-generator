from __future__ import annotations

import json
from pathlib import Path

import pytest

from isaacmap.basement1_pipeline import generate_basement1_through_treasure
from isaacmap.basement1_pipeline_differential import compare_pipeline
from isaacmap.basement1_pipeline_reference import generate_basement1_through_treasure_reference
from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.boss_pool_reference import BossPoolEntryReference
from isaacmap.resources import load_stb
from isaacmap.topology import LevelGeneratorResearch
from isaacmap.topology_reference import LevelGeneratorReference


ROOT=Path("research/input/extracted_resources/merged/resources")
BOSSES=load_boss_pool_xml(ROOT/"bosspools.xml")["basement"]
BOSS_REFS=tuple(BossPoolEntryReference(x.boss_id,x.weight,x.initial_weight,x.achievement,x.alternate_boss_id) for x in BOSSES)
SPECIAL=tuple(load_stb(ROOT/"rooms/00.special rooms.stb"))
BASEMENT=tuple(load_stb(ROOT/"rooms/01.basement.stb"))


def _clean(seed,difficulty):
    return generate_basement1_through_treasure(seed,difficulty,boss_entries=BOSSES,special_definitions=SPECIAL,basement_definitions=BASEMENT)


def _reference(seed,difficulty):
    return generate_basement1_through_treasure_reference(seed,difficulty,boss_entries=BOSS_REFS,special_definitions=SPECIAL,basement_definitions=BASEMENT)


@pytest.mark.parametrize("difficulty",["NORMAL","HARD"])
def test_first_fifty_full_attempt_transactions_match_reference(difficulty):
    for seed in range(1,51): compare_pipeline(_clean(seed,difficulty),_reference(seed,difficulty))


def test_three_boss_geometry_retry_fixtures_lock_nonrollback_semantics():
    payload=json.loads(Path("tests/fixtures/boss_geometry_retries.json").read_text(encoding="utf-8"))
    for fixture in payload["fixtures"]:
        result=_clean(fixture["start_seed"],fixture["difficulty"])
        assert len(result.attempts)==len(fixture["attempts"])==2
        for actual,expected in zip(result.attempts,fixture["attempts"]):
            post=actual.post_topology; assert post is not None
            assert post.boss_selection.boss_id==expected["boss_id"]
            assert [post.boss_config.stage,post.boss_config.mode,post.boss_config.resource_index]==expected["boss_config"]
            assert post.abort_operation==expected["abort"]
            assert [actual.start_level_rng_state,actual.end_level_rng_state]==expected["level_rng"]
            assert [actual.start_generator_rng_state,actual.end_generator_rng_state]==expected["generator_rng"]
            assert [actual.start_boss_pool_state,actual.end_boss_pool_state]==expected["boss_pool_rng"]
            assert list(actual.level_blacklist_after)==expected["level_blacklist"]
            assert list(actual.permanent_removed_after)==expected["permanent_removed"]
            assert len(actual.room_config_mutations)==expected["weight_mutations"]
        assert list(result.permanent_removed_bosses)==fixture["committed_bosses"]


def test_failed_boss_preroll_and_config_decay_are_not_rolled_back():
    result=_clean(0xCAE,"NORMAL")
    first,second=result.attempts
    assert first.post_topology.abort_operation=="Boss geometry"
    assert second.start_boss_pool_state==first.end_boss_pool_state
    assert second.start_level_rng_state==first.end_level_rng_state
    assert second.start_generator_rng_state==first.end_generator_rng_state
    failed_key=first.room_config_mutations[0][0]
    assert dict(result.final_room_config_weights)[failed_key]==first.room_config_mutations[0][2]
    assert first.permanent_removed_after==()
    assert result.permanent_removed_bosses==(13,)


def test_type8_shop_treasure_mutate_existing_rooms_and_stably_consume_candidates():
    result=_clean(0xCAE,"NORMAL"); post=result.attempts[-1].post_topology; assert post and post.completed
    selected=(post.boss_room,*post.type8_rooms,post.shop_room,post.treasure_room)
    assert len(set(selected))==4
    assert [post.rooms[r].room_type for r in selected]==[5,8,2,4]
    assert [t.operation for t in post.candidate_traces]==["DetermineBossRoom","GetNewEndRoom(RoomType8)","GetNewEndRoom(Shop)","GetNewEndRoom(Treasure)"]
    for before,after in zip(post.candidate_traces,post.candidate_traces[1:]):
        assert before.dead_ends_after==after.candidate_order


def test_roomtype_order_and_rng_rvas_are_binary_ordered():
    result=_clean(0xCAE,"NORMAL"); post=result.attempts[-1].post_topology; assert post
    assert [t.operation for t in post.config_traces]==["Boss","RoomType8","Shop","Treasure"]
    assert len(post.config_traces[-1].selections)==2  # stage 1 miss, stage 0 fallback
    rvas=[d.binary_rva for d in post.rng_draws]
    assert rvas.index(0x003394A4)<rvas.index(0x00339A87)<rvas.index(0x00339BE7)<rvas.index(0x00339DB4)<rvas.index(0x0033A1C7)<rvas.index(0x0033A455)<rvas.index(0x0033A76B)


def test_intervening_binary_conditions_remain_in_reference_control_flow():
    clean=_clean(0xCAE,"NORMAL"); reference=_reference(0xCAE,"NORMAL")
    clean_post=clean.attempts[-1].post_topology; reference_post=reference.attempts[-1].post
    assert clean_post and reference_post
    expected=[
        ("0x00339540..0x003398AB",False),
        ("0x00339926..0x00339A0D",False),
        ("0x00339C0A..0x00339C81",True),
        ("0x00339CAA..0x00339CD1",True),
        ("0x0033A2C3..0x0033A383",True),
    ]
    assert [(c.binary_range,c.value) for c in clean_post.conditions]==expected
    assert [(c.binary_range,c.value) for c in reference_post.conditions]==expected


def test_tenth_unusable_attempt_commits_target_increment_only_to_next_attempt(monkeypatch):
    monkeypatch.setattr(LevelGeneratorResearch,"generate_once",lambda self,*args,**kwargs: None)
    monkeypatch.setattr(LevelGeneratorReference,"generate_once",lambda self,*args,**kwargs: None)
    clean=generate_basement1_through_treasure(
        1,"NORMAL",boss_entries=BOSSES,special_definitions=SPECIAL,
        basement_definitions=BASEMENT,max_attempts=11,
    )
    reference=generate_basement1_through_treasure_reference(
        1,"NORMAL",boss_entries=BOSS_REFS,special_definitions=SPECIAL,
        basement_definitions=BASEMENT,max_attempts=11,
    )
    compare_pipeline(clean,reference)
    initial=clean.attempts[0].target_room_count
    assert [attempt.target_room_count for attempt in clean.attempts]==[initial]*10+[initial+1]
    assert all(attempt.post_topology is None for attempt in clean.attempts)
