from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.boss_pool import load_boss_pool_xml
from isaacmap.floor_init import derive_basement1_topology_inputs
from isaacmap.resources import load_stb
from isaacmap.special_rooms import room_configs_from_definitions, run_boss_then_type8
from isaacmap.special_rooms_differential import compare_boss_then_type8
from isaacmap.topology import generate_basement1_topology_research
from isaacmap.topology_reference import generate_basement1_topology_reference


RESOURCE_ROOT = Path("research/input/extracted_resources/merged/resources")
BOSS_ENTRIES = load_boss_pool_xml(RESOURCE_ROOT / "bosspools.xml")["basement"]
SPECIAL_DEFINITIONS = tuple(load_stb(RESOURCE_ROOT / "rooms/00.special rooms.stb"))
SPECIAL_CONFIGS = room_configs_from_definitions(SPECIAL_DEFINITIONS)


@pytest.mark.parametrize("difficulty", ["NORMAL", "HARD"])
def test_first_fifty_boss_then_type8_cases_match_reference(difficulty: str) -> None:
    for game_start_seed in range(1, 51):
        inputs = derive_basement1_topology_inputs(game_start_seed, difficulty)
        compare_boss_then_type8(
            generate_basement1_topology_research(inputs),
            generate_basement1_topology_reference(inputs),
            game_start_seed=game_start_seed,
            level_rng_state=inputs.generator_seed,
            boss_entries=BOSS_ENTRIES,
            special_definitions=SPECIAL_DEFINITIONS,
        )


def test_seed_one_records_true_boss_then_type8_order_and_rng_objects() -> None:
    inputs = derive_basement1_topology_inputs(1, "NORMAL")
    result = run_boss_then_type8(
        generate_basement1_topology_research(inputs),
        game_start_seed=1,
        level_rng_state=inputs.generator_seed,
        boss_entries=BOSS_ENTRIES,
        special_configs=SPECIAL_CONFIGS,
    )
    assert result.boss.boss_id == 17
    assert result.boss_room == 9
    assert result.type8_rooms == (8,)
    assert result.dead_ends == (4, 3, 2)
    assert result.final_level_rng_state == 0x398E4633
    identities = [draw.object_identity for draw in result.rng_trace]
    assert identities == [
        "Level._generationRNG",
        "Level::select_boss_room_config.local",
        "RoomConfig::GetRandomRoom.local(seed=0xE807DB4A)",
        "Level._generationRNG",
        "post-topology RoomType8.local",
        "RoomConfig::GetRandomRoom.local(seed=0xCA56B4F1)",
    ]
    assert [draw.binary_rva for draw in result.rng_trace] == [
        0x003394A4,
        0x0033930E,
        0x0042CBDE,
        0x00339A87,
        0x00339B1E,
        0x0042CBDE,
    ]


def test_type8_is_existing_endroom_mutation_and_stable_candidate_removal() -> None:
    inputs = derive_basement1_topology_inputs(1, "NORMAL")
    topology = generate_basement1_topology_research(inputs)
    before_room_count = len(topology.rooms)
    before_order = topology.dead_ends
    result = run_boss_then_type8(
        topology,
        game_start_seed=1,
        level_rng_state=inputs.generator_seed,
        boss_entries=BOSS_ENTRIES,
        special_configs=SPECIAL_CONFIGS,
    )
    assert len(result.rooms) == before_room_count
    assert before_order == (9, 8, 4, 3, 2)
    assert result.boss_room == before_order[0]
    assert result.type8_rooms == (before_order[1],)
    assert result.dead_ends == before_order[2:]
    assert result.rooms[result.type8_rooms[0]].room_type == 8


def test_collectible_589_requests_second_type8_without_merging_rng_identity() -> None:
    inputs = derive_basement1_topology_inputs(1, "HARD")
    result = run_boss_then_type8(
        generate_basement1_topology_research(inputs),
        game_start_seed=1,
        level_rng_state=inputs.generator_seed,
        boss_entries=BOSS_ENTRIES,
        special_configs=SPECIAL_CONFIGS,
        collectible_589_owned=True,
    )
    assert len(result.type8_rooms) == 2
    type8_draws = [
        draw for draw in result.rng_trace
        if draw.object_identity == "post-topology RoomType8.local"
    ]
    assert len(type8_draws) == 2
    assert type8_draws[0].post_state == type8_draws[1].pre_state


def test_boss_match_failure_returns_outer_generation_retry_signal() -> None:
    # The first such NORMAL case in the 1..10,000 corpus.  The binary caller
    # treats a null post-topology result as a reason to continue the outer
    # generation loop; it does not accept this topology as the final floor.
    inputs = derive_basement1_topology_inputs(0x00000CAE, "NORMAL")
    result = run_boss_then_type8(
        generate_basement1_topology_research(inputs),
        game_start_seed=0x00000CAE,
        level_rng_state=inputs.generator_seed,
        boss_entries=BOSS_ENTRIES,
        special_configs=SPECIAL_CONFIGS,
    )
    assert not result.completed
    assert result.abort_operation == "Boss"
    assert result.boss.boss_id == 56
    assert result.boss_room == -1
