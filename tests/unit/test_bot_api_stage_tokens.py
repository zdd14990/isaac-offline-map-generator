"""Route/stage-token behavior of the headless bot API."""

from __future__ import annotations

from pathlib import Path

import pytest

from isaacmap.bot_api import (
    ALT_ROUTE,
    MAIN_ROUTE,
    floor_name_for,
    generate_map_image_for_bot,
    parse_stage_token,
)

RESOURCE_ROOT = Path("research/input/extracted_resources/merged/resources")


def test_parse_stage_token_main() -> None:
    assert parse_stage_token("1") == (MAIN_ROUTE, 1)
    assert parse_stage_token("8") == (MAIN_ROUTE, 8)
    assert parse_stage_token("6") == (MAIN_ROUTE, 6)


def test_parse_stage_token_alt() -> None:
    assert parse_stage_token("1+") == (ALT_ROUTE, 1)
    assert parse_stage_token("6+") == (ALT_ROUTE, 6)


@pytest.mark.parametrize("token", ["0", "9", "7+", "8+", "+", "1++", "abc", ""])
def test_parse_stage_token_rejects(token: str) -> None:
    assert parse_stage_token(token) is None


def test_floor_name_for() -> None:
    assert floor_name_for(MAIN_ROUTE, 7) == "Womb I"
    assert floor_name_for(MAIN_ROUTE, 8) == "Womb II"
    assert floor_name_for(ALT_ROUTE, 1) == "Downpour I"
    assert floor_name_for(ALT_ROUTE, 3) == "Mines I"
    assert floor_name_for(ALT_ROUTE, 5) == "Mausoleum I"
    assert floor_name_for(ALT_ROUTE, 6) == "Mausoleum II"
    assert floor_name_for(ALT_ROUTE, 7) is None
    assert floor_name_for(MAIN_ROUTE, 9) is None


def test_generation_fail_closed_for_alt_floors(tmp_path: Path) -> None:
    """Alt floors 2+..6+ still fail closed with the floor name carried back."""
    cases = [
        
        (ALT_ROUTE, 3, "Mines I"),
        (ALT_ROUTE, 4, "Mines II"),
        (ALT_ROUTE, 5, "Mausoleum I"),
        (ALT_ROUTE, 6, "Mausoleum II"),
    ]
    for route, stage, floor in cases:
        result = generate_map_image_for_bot(
            "B911 99AC", "NORMAL", stage, str(tmp_path), route=route
        )
        assert not result.ok, (route, stage)
        assert result.error == "UNSUPPORTED_FLOOR", (route, stage)
        assert result.floor_name == floor, (route, stage)
        assert result.route == route, (route, stage)


def test_downpour1_generates_for_bot(tmp_path: Path) -> None:
    """ALT 1+ (Downpour I) is now supported."""
    result = generate_map_image_for_bot(
        "B911 99AC", "NORMAL", 1, str(tmp_path), route=ALT_ROUTE
    )
    assert result.ok
    assert result.floor_name == "Downpour I"
    assert result.route == ALT_ROUTE
    assert result.algorithm_evidence == "PARTIAL_BINARY"
    assert result.image_path is not None


def test_womb_floors_generate_for_bot(tmp_path: Path) -> None:
    """Womb I/II are now supported on the MAIN route."""
    for route, stage, floor in (
        (MAIN_ROUTE, 7, "Womb I"),
        (MAIN_ROUTE, 8, "Womb II"),
    ):
        result = generate_map_image_for_bot(
            "B911 99AC", "NORMAL", stage, str(tmp_path), route=route
        )
        assert result.ok, (route, stage)
        assert result.floor_name == floor, (route, stage)
        assert result.image_path is not None, (route, stage)


def test_invalid_route_and_stage_rejected(tmp_path: Path) -> None:
    bad_route = generate_map_image_for_bot(
        "B911 99AC", "NORMAL", 5, str(tmp_path), route="SIDE"
    )
    assert not bad_route.ok and bad_route.error == "INVALID_ROUTE"
    out_of_range = generate_map_image_for_bot(
        "B911 99AC", "NORMAL", 7, str(tmp_path), route=ALT_ROUTE
    )
    assert not out_of_range.ok and out_of_range.error == "INVALID_STAGE"


@pytest.mark.skipif(
    not RESOURCE_ROOT.is_dir(),
    reason="game resources not extracted locally; see README 'Game resources'",
)
def test_cache_filename_contains_route(tmp_path: Path) -> None:
    result = generate_map_image_for_bot(
        "B911 99AC", "NORMAL", 5, str(tmp_path), route=MAIN_ROUTE
    )
    assert result.ok
    assert result.image_path is not None
    assert "_MAIN_NORMAL_stage5_" in result.image_path
