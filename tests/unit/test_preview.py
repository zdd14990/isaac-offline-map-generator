from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path

import pytest

from isaacmap.preview import (
    GENERATION_STATUS,
    SUPPORTED_FLOORS,
    UnsupportedPreviewFloor,
    generate_preview,
)
from isaacmap.basement2_full_pipeline import BASEMENT2_LAYOUT_STATUS
from isaacmap.seed import encode_seed
from isaacmap.topology_geometry import occupied_cells
from isaacmap.ui.models import (
    PreviewMapModel,
    RenderRoom,
    preview_to_dict,
    room_tooltip,
)
from isaacmap.ui.renderer import compute_layout, connection_segments, room_icon_key


CORPUS_REPORT = Path("research/binary/basement1_secret_differential_report.json")


@lru_cache(maxsize=4)
def _find_corpus_secret_preview(
    difficulty: str,
    *,
    require_retry: bool = False,
    require_bounds_expansion: bool = False,
) -> tuple[int, object]:
    """Select a fixture by running the clean pipeline over the recorded corpus."""

    start, end = json.loads(CORPUS_REPORT.read_text(encoding="utf-8"))["seed_range"]
    for start_seed in range(start, end + 1):
        preview = generate_preview(encode_seed(start_seed), difficulty, "Basement I")
        expands_bounds = True
        if preview.secret_grid_index is not None and require_bounds_expansion:
            m5_cells = tuple(
                cell
                for room in preview.final_post_topology.rooms
                for cell in occupied_cells(room.column, room.line, room.shape)
            )
            columns = tuple(column for column, _row in m5_cells)
            rows = tuple(row for _column, row in m5_cells)
            secret_column = preview.secret_grid_index % 13
            secret_row = preview.secret_grid_index // 13
            expands_bounds = not (
                min(columns) <= secret_column <= max(columns)
                and min(rows) <= secret_row <= max(rows)
            )
        if (
            preview.secret_grid_index is not None
            and (not require_retry or preview.attempt_count > 1)
            and expands_bounds
        ):
            return start_seed, preview
    raise AssertionError(f"no matching {difficulty} Secret fixture in M6 corpus")


def test_preview_adapter_exposes_clean_accepted_basement1_layout() -> None:
    preview = generate_preview("B911 99AC", "NORMAL", "Basement I")
    assert preview.generation_status == GENERATION_STATUS
    assert preview.partial is False
    assert preview.algorithm_evidence == "CONFIRMED_BINARY"
    assert preview.gameplay_fixture == "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"
    assert preview.attempt_count == 2  # Seed 1 locks the Treasure retry fixture.
    assert preview.final_attempt_index == 1
    assert PreviewMapModel.from_preview(preview).rooms

    payload = preview_to_dict(preview)
    assert payload["status"] == "FULL_LAYOUT_PIPELINE_CONFIRMED_BINARY"
    assert len(payload["attempt_trace"]) == 2
    assert payload["attempt_trace"][0]["outcome"] == "Treasure geometry"
    assert payload["attempt_trace"][1]["outcome"] == "accepted"
    assert payload["secret_generation_supported"] is True
    assert payload["secret_generated"] is True
    assert "Secret Room" not in payload["not_yet_generated"]
    assert payload["ultra_secret_generation_supported"] is True
    assert payload["normal_room_configs_supported"] is True
    assert payload["not_yet_generated"] == []


def test_unsupported_floor_fails_before_generator_call(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("clean generator must not be called for an unsupported floor")

    monkeypatch.setattr("isaacmap.preview.generate_basement1_full", forbidden)
    monkeypatch.setattr("isaacmap.preview.generate_basement2_full", forbidden)
    with pytest.raises(UnsupportedPreviewFloor, match="UNSUPPORTED"):
        generate_preview("B911 99AC", "HARD", "Sheol")


def test_preview_support_registry_contains_only_confirmed_complete_floors() -> None:
    assert tuple(SUPPORTED_FLOORS) == (
        "Basement I", "Basement II", "Caves I", "Caves II", "Depths I", "Depths II",
        "Womb I", "Womb II",
    )
    assert SUPPORTED_FLOORS["Basement I"].replayed_floors == ("Basement I",)
    assert SUPPORTED_FLOORS["Basement II"].replayed_floors == (
        "Basement I",
        "Basement II",
    )
    assert SUPPORTED_FLOORS["Caves I"].replayed_floors == (
        "Basement I",
        "Basement II",
        "Caves I",
    )
    assert SUPPORTED_FLOORS["Caves II"].replayed_floors == (
        "Basement I",
        "Basement II",
        "Caves I",
        "Caves II",
    )
    assert SUPPORTED_FLOORS["Depths I"].replayed_floors == (
        "Basement I",
        "Basement II",
        "Caves I",
        "Caves II",
        "Depths I",
    )
    assert SUPPORTED_FLOORS["Depths II"].replayed_floors == (
        "Basement I",
        "Basement II",
        "Caves I",
        "Caves II",
        "Depths I",
        "Depths II",
    )
    assert SUPPORTED_FLOORS["Womb I"].replayed_floors == (
        "Basement I",
        "Basement II",
        "Caves I",
        "Caves II",
        "Depths I",
        "Depths II",
        "Womb I",
    )
    assert SUPPORTED_FLOORS["Womb II"].replayed_floors == (
        "Basement I",
        "Basement II",
        "Caves I",
        "Caves II",
        "Depths I",
        "Depths II",
        "Womb I",
        "Womb II",
    )


@pytest.mark.parametrize("difficulty", ["NORMAL", "HARD"])
def test_preview_adapter_replays_and_exposes_clean_accepted_basement2_layout(
    difficulty: str,
) -> None:
    preview = generate_preview("B911 99AC", difficulty, "Basement II")
    assert preview.floor == "Basement II"
    assert preview.difficulty == difficulty
    assert preview.generation_status == BASEMENT2_LAYOUT_STATUS
    assert preview.generation_status == "BASEMENT2_FULL_LAYOUT_PIPELINE_CONFIRMED_BINARY"
    assert preview.partial is False
    assert preview.algorithm_evidence == "CONFIRMED_BINARY"
    assert preview.gameplay_fixture == "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"
    assert preview.replayed_floors == ("Basement I", "Basement II")
    assert preview.final_attempt.abort_operation is None
    assert preview.rooms == preview.pipeline_result.rooms
    assert preview.room_map == preview.pipeline_result.room_map
    assert preview.descriptor_configs == preview.pipeline_result.descriptor_configs
    assert len(preview.pipeline_result.permanent_removed_bosses) == 2

    model = PreviewMapModel.from_preview(preview)
    assert len(model.rooms) == len(preview.rooms)
    assert all(room.config_resource_index is not None for room in model.rooms)
    payload = preview_to_dict(preview)
    assert payload["floor"] == "Basement II"
    assert payload["status"] == BASEMENT2_LAYOUT_STATUS
    assert payload["not_yet_generated"] == []
    assert payload["secret_generation_supported"] is True
    assert payload["ultra_secret_generation_supported"] is True
    assert payload["normal_room_configs_supported"] is True


@pytest.mark.parametrize("difficulty", ["NORMAL", "HARD"])
def test_m6_corpus_secret_uses_final_descriptors_and_expands_bounds(
    difficulty: str,
) -> None:
    _start_seed, preview = _find_corpus_secret_preview(
        difficulty, require_bounds_expansion=True
    )
    secret_final = preview.final_through_secret
    final = preview.final_late_default
    model = PreviewMapModel.from_preview(preview)
    secret_rooms = [room for room in model.rooms if room.room_type == 7]
    assert len(secret_rooms) == 1
    secret = secret_rooms[0]

    assert tuple(room.generation_index for room in model.rooms) == tuple(
        room.generation_index for room in final.rooms
    )
    assert model.room_map == preview.room_map
    assert preview.secret_grid_index == secret_final.secret_geometry.grid_index
    assert secret.grid_index == secret_final.secret_geometry.grid_index
    assert preview.room_map[secret.grid_index] == secret.generation_index

    layout = compute_layout(model.rooms, 900, 600)
    secret_column, secret_row = secret.grid_index % 13, secret.grid_index // 13
    assert layout.min_column <= secret_column <= layout.max_column
    assert layout.min_row <= secret_row <= layout.max_row
    m5_model = tuple(
        RenderRoom.from_generated(room) for room in preview.final_post_topology.rooms
    )
    m5_layout = compute_layout(m5_model, 900, 600)
    assert not (
        m5_layout.min_column <= secret_column <= m5_layout.max_column
        and m5_layout.min_row <= secret_row <= m5_layout.max_row
    )
    assert room_icon_key(secret) == "secret"
    assert "RoomType: ROOM_SECRET" in room_tooltip(secret)
    assert "Shape: ROOMSHAPE_1x1" in room_tooltip(secret)

    secret_connections = [
        connection
        for connection in connection_segments(model)
        if secret.generation_index in (connection.source_room, connection.target_room)
    ]
    assert secret_connections


def test_retry_fixture_exposes_only_final_attempt_secret_descriptors() -> None:
    _start_seed, preview = _find_corpus_secret_preview("NORMAL", require_retry=True)
    assert preview.attempt_count > 1
    model = PreviewMapModel.from_preview(preview)
    assert model.room_map == preview.pipeline_result.room_map
    assert len(model.rooms) == len(preview.pipeline_result.rooms)
    assert preview.attempts[-1].late_default.completed
    assert all(attempt.abort_operation is not None for attempt in preview.attempts[:-1])


def test_preview_exposes_ultra_and_all_normal_configs() -> None:
    preview = generate_preview("B911 99AC", "HARD", "Basement I")
    model = PreviewMapModel.from_preview(preview)
    ultra = [room for room in model.rooms if room.room_type == 29]
    assert len(ultra) == 1
    assert ultra[0].grid_index == preview.ultra_secret_grid_index
    assert room_icon_key(ultra[0]) == "ultra_secret"
    assert "RoomType: ROOM_ULTRASECRET" in room_tooltip(ultra[0])
    assert all(room.variant >= 0 and room.subtype >= 0 for room in model.rooms)
    assert all(room.config_resource_index is not None for room in model.rooms)
    assert "Config: stage=" in room_tooltip(model.rooms[0])


def test_m6_corpus_has_no_natural_secret_none_fixture() -> None:
    report = json.loads(CORPUS_REPORT.read_text(encoding="utf-8"))
    assert report["difficulties"]["NORMAL"]["secret_missing"] == 0
    assert report["difficulties"]["HARD"]["secret_missing"] == 0
