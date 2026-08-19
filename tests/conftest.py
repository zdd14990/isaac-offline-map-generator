"""Pytest configuration.

A subset of the test suite (``tests/unit/*`` and ``tests/differential/*``)
reads the locally extracted game resources under
``research/input/extracted_resources/merged/resources``.  This repository
never redistributes game assets, so those tests are skipped automatically when
the extraction output is absent instead of failing a fresh clone.  See the
README, "Game resources", for how to produce the extraction from a legal local
game installation.
"""

from __future__ import annotations

from pathlib import Path

import pytest

RESOURCE_ROOT = Path("research/input/extracted_resources/merged/resources")

# Test modules that require the locally extracted game resources.
RESOURCE_DEPENDENT_FILES = frozenset({
    "tests/differential/test_caves1_full_pipeline_differential.py",
    "tests/differential/test_caves2_full_pipeline_differential.py",
    "tests/differential/test_depths1_full_pipeline_differential.py",
    "tests/differential/test_depths2_full_pipeline_differential.py",
    "tests/unit/test_basement1_full_pipeline.py",
    "tests/unit/test_basement1_pipeline.py",
    "tests/unit/test_basement1_secret_pipeline.py",
    "tests/unit/test_basement2_boss_pool.py",
    "tests/unit/test_basement2_full_pipeline.py",
    "tests/unit/test_basement2_lifecycle.py",
    "tests/unit/test_basement2_pipeline.py",
    "tests/unit/test_basement2_secret_pipeline.py",
    "tests/unit/test_boss_pool.py",
    "tests/unit/test_caves1_boss_pool.py",
    "tests/unit/test_caves1_full_pipeline.py",
    "tests/unit/test_late_room_config.py",
    "tests/unit/test_post_layout_lifecycle.py",
    "tests/unit/test_room_config.py",
    "tests/unit/test_special_rooms.py",
    "tests/unit/test_ultra_secret.py",
})


def pytest_collection_modifyitems(session, config, items) -> None:
    if RESOURCE_ROOT.is_dir():
        return
    skip = pytest.mark.skip(
        reason="game resources not extracted locally; see README \"Game resources\""
    )
    for item in items:
        path = getattr(item, "path", None) or item.fspath
        relative = Path(str(path)).as_posix()
        if relative in RESOURCE_DEPENDENT_FILES:
            item.add_marker(skip)
