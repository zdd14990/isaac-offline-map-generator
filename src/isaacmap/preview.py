"""Fail-closed adapter for confirmed canonical research maps.

This module imports only clean accepted-layout pipelines.  It never imports a
differential/reference implementation and rejects every unrecovered
floor/profile instead of approximating it.  Later floors replay the recovered
generation lifecycle from the run seed; the UI receives only the accepted
floor result.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable

from .basement1_full_pipeline import (
    Basement1FullAttemptResult,
    Basement1FullResult,
    FULL_LAYOUT_STATUS,
    generate_basement1_full,
)
from .basement1_pipeline import PostTopologyAttemptResult
from .basement1_secret_pipeline import PostTreasureThroughSecretResult
from .basement1_ultra_pipeline import PostSecretThroughUltraResult
from .basement2_full_pipeline import Basement2FullResult, generate_basement2_full
from .basement2_lifecycle import generate_basement2_lifecycle, Basement2LifecycleResult
from .caves1_full_pipeline import Caves1FullResult
from .caves1_lifecycle import generate_caves1_lifecycle
from .caves2_full_pipeline import Caves2FullResult
from .caves2_lifecycle import generate_caves2_lifecycle
from .depths1_full_pipeline import Depths1FullResult
from .depths1_lifecycle import generate_depths1_lifecycle
from .depths2_full_pipeline import Depths2FullResult
from .depths2_lifecycle import generate_depths2_lifecycle
from .generation_profile import resolve_run_generation_profile
from .womb1_lifecycle import generate_womb1_lifecycle
from .womb1_full_pipeline import Womb1FullResult
from .womb2_full_pipeline import Womb2FullResult
from .womb2_lifecycle import generate_womb2_lifecycle
from .late_room_config import LateDefaultPassResult
from .boss_pool import BossPoolEntry, load_boss_pool_xml
from .resources import RoomDefinition, load_stb
from .seed import decode_seed, encode_seed


GENERATION_STATUS = FULL_LAYOUT_STATUS
ALGORITHM_EVIDENCE = "CONFIRMED_BINARY"
GAMEPLAY_FIXTURE = "NOT_EXTERNALLY_VALIDATED_GAMEPLAY"
SUPPORTED_FLOOR = "Basement I"
SUPPORTED_DIFFICULTIES = ("NORMAL", "HARD")


class PreviewError(RuntimeError):
    """Base error for the deliberately limited preview surface."""


class UnsupportedPreviewFloor(PreviewError):
    """Raised instead of approximating an unrecovered floor."""


class MissingPreviewResources(PreviewError):
    """Raised when the statically extracted official resources are absent."""


class PreviewGenerationFailed(PreviewError):
    """Raised when the recovered pipeline does not finish within its limit."""


@dataclass(frozen=True)
class _PreviewResources:
    bosses: tuple[BossPoolEntry, ...]
    caves_bosses: tuple[BossPoolEntry, ...]
    depths_bosses: tuple[BossPoolEntry, ...]
    womb_bosses: tuple[BossPoolEntry, ...]
    downpour_bosses: tuple[BossPoolEntry, ...]
    dross_bosses: tuple[BossPoolEntry, ...]
    mines_bosses: tuple[BossPoolEntry, ...]
    ashpit_bosses: tuple[BossPoolEntry, ...]
    mausoleum_bosses: tuple[BossPoolEntry, ...]
    gehenna_bosses: tuple[BossPoolEntry, ...]
    special: tuple[RoomDefinition, ...]
    basement: tuple[RoomDefinition, ...]
    caves: tuple[RoomDefinition, ...]
    depths: tuple[RoomDefinition, ...]
    womb: tuple[RoomDefinition, ...]
    downpour: tuple[RoomDefinition, ...]
    dross: tuple[RoomDefinition, ...]
    mines: tuple[RoomDefinition, ...]
    ashpit: tuple[RoomDefinition, ...]
    mausoleum: tuple[RoomDefinition, ...]
    gehenna: tuple[RoomDefinition, ...]
    blue_womb: tuple[RoomDefinition, ...]
PreviewPipelineResult = Basement1FullResult | Basement2FullResult | Caves1FullResult | Caves2FullResult | Depths1FullResult | Womb1FullResult | Womb2FullResult


@dataclass(frozen=True)
class PreviewFloorSpec:
    """One fail-closed floor entry backed by a clean confirmed pipeline."""

    name: str
    output_slug: str
    replayed_floors: tuple[str, ...]
    generate: Callable[[int, str, _PreviewResources], PreviewPipelineResult]


@dataclass(frozen=True)
class PreviewGeneration:
    """Read-only wrapper around one accepted clean floor result."""

    seed: str
    start_seed: int
    difficulty: str
    generation_profile: str
    floor: str
    generation_status: str
    partial: bool
    algorithm_evidence: str
    gameplay_fixture: str
    replayed_floors: tuple[str, ...]
    pipeline_result: PreviewPipelineResult

    @property
    def attempts(self) -> tuple[Basement1FullAttemptResult, ...]:
        return self.pipeline_result.attempts

    @property
    def attempt_count(self) -> int:
        return len(self.attempts)

    @property
    def final_attempt_index(self) -> int:
        return self.attempt_count - 1

    @property
    def final_attempt(self) -> Basement1FullAttemptResult:
        if not self.attempts:
            raise PreviewGenerationFailed("pipeline returned no generation attempts")
        return self.attempts[-1]

    @property
    def final_post_topology(self) -> PostTopologyAttemptResult:
        post = self.final_attempt.through_treasure
        if post is None or not post.completed:
            raise PreviewGenerationFailed("pipeline returned no completed final attempt")
        return post

    @property
    def final_through_secret(self) -> PostTreasureThroughSecretResult:
        final = self.final_attempt.through_secret
        if final is None or not final.completed:
            raise PreviewGenerationFailed("pipeline returned no completed Secret boundary")
        return final

    @property
    def final_through_ultra(self) -> PostSecretThroughUltraResult:
        final = self.final_attempt.through_ultra
        if final is None or not final.completed:
            raise PreviewGenerationFailed("pipeline returned no completed Ultra boundary")
        return final

    @property
    def final_late_default(self) -> LateDefaultPassResult:
        final = self.final_attempt.late_default
        if final is None or not final.completed:
            raise PreviewGenerationFailed("pipeline returned no accepted late-default pass")
        return final

    @property
    def rooms(self) -> tuple[object, ...]:
        """Final accepted-attempt descriptors after all ordinary configs."""

        return self.pipeline_result.rooms

    @property
    def room_map(self) -> tuple[int, ...]:
        """Final accepted-attempt 13x13 descriptor map after Ultra placement."""

        return self.pipeline_result.room_map

    @property
    def descriptor_configs(self) -> tuple[tuple[int, object], ...]:
        return self.pipeline_result.descriptor_configs

    @property
    def secret_grid_index(self) -> int | None:
        geometry = self.final_through_secret.secret_geometry
        return geometry.grid_index if geometry.room_id >= 0 else None

    @property
    def ultra_secret_grid_index(self) -> int | None:
        geometry = self.final_through_ultra.ultra_geometry
        return geometry.grid_index if geometry.room_id >= 0 else None


def default_resource_root() -> Path:
    """Return the project's statically extracted merged resource directory."""

    project_root = Path(__file__).resolve().parents[2]
    return project_root / "research" / "input" / "extracted_resources" / "merged" / "resources"


@lru_cache(maxsize=4)
def _load_preview_resources(resource_root: str) -> _PreviewResources:
    root = Path(resource_root)
    required = (
        root / "bosspools.xml",
        root / "rooms" / "00.special rooms.stb",
        root / "rooms" / "01.basement.stb",
        root / "rooms" / "04.caves.stb",
        root / "rooms" / "13.blue womb.stb",
        root / "rooms" / "07.depths.stb",
        root / "rooms" / "10.womb.stb",
        root / "rooms" / "27.downpour.stb",
        root / "rooms" / "28.dross.stb",
        root / "rooms" / "29.mines.stb",
        root / "rooms" / "30.ashpit.stb",
        root / "rooms" / "31.mausoleum.stb",
        root / "rooms" / "32.gehenna.stb",
    )
    missing = tuple(path for path in required if not path.is_file())
    if missing:
        paths = ", ".join(str(path) for path in missing)
        raise MissingPreviewResources(f"missing statically extracted resources: {paths}")

    pools = load_boss_pool_xml(required[0])
    bosses = pools.get("basement", ())
    caves_bosses = pools.get("caves", ())
    depths_bosses = pools.get("depths", ())
    womb_bosses = pools.get("womb", ())
    downpour_bosses = pools.get("downpour", ())
    dross_bosses = pools.get("dross", ())
    mines_bosses = pools.get("mines", ())
    ashpit_bosses = pools.get("ashpit", ())
    mausoleum_bosses = pools.get("mausoleum", ())
    gehenna_bosses = pools.get("gehenna", ())
    if not bosses:
        raise MissingPreviewResources("the extracted Basement boss pool is empty")
    if not caves_bosses:
        raise MissingPreviewResources("the extracted Caves boss pool is empty")
    if not depths_bosses:
        raise MissingPreviewResources("the extracted Depths boss pool is empty")
    if not womb_bosses:
        raise MissingPreviewResources("the extracted Womb boss pool is empty")
    if not downpour_bosses:
        raise MissingPreviewResources("the extracted Downpour boss pool is empty")
    if not dross_bosses:
        raise MissingPreviewResources("the extracted Dross boss pool is empty")
    if not mines_bosses:
        raise MissingPreviewResources("the extracted Mines boss pool is empty")
    if not ashpit_bosses:
        raise MissingPreviewResources("the extracted Ashpit boss pool is empty")
    if not mausoleum_bosses:
        raise MissingPreviewResources("the extracted Mausoleum boss pool is empty")
    if not gehenna_bosses:
        raise MissingPreviewResources("the extracted Gehenna boss pool is empty")
    return _PreviewResources(
        bosses=tuple(bosses),
        caves_bosses=tuple(caves_bosses),
        depths_bosses=tuple(depths_bosses),
        womb_bosses=tuple(womb_bosses),
        downpour_bosses=tuple(downpour_bosses),
        dross_bosses=tuple(dross_bosses),
        mines_bosses=tuple(mines_bosses),
        ashpit_bosses=tuple(ashpit_bosses),
        mausoleum_bosses=tuple(mausoleum_bosses),
        gehenna_bosses=tuple(gehenna_bosses),
        special=tuple(load_stb(required[1])),
        basement=tuple(load_stb(required[2])),
        caves=tuple(load_stb(required[3])),
        blue_womb=tuple(load_stb(required[4])),
        depths=tuple(load_stb(required[5])),
        womb=tuple(load_stb(required[6])),
        downpour=tuple(load_stb(required[7])),
        dross=tuple(load_stb(required[8])),
        mines=tuple(load_stb(required[9])),
        ashpit=tuple(load_stb(required[10])),
        mausoleum=tuple(load_stb(required[11])),
        gehenna=tuple(load_stb(required[12])),
    )


def _generate_downpour1(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> "Basement1FullResult":
    from .downpour1_lifecycle import generate_downpour1_lifecycle

    return generate_downpour1_lifecycle(
        start_seed,
        difficulty,
        downpour_boss_entries=resources.downpour_bosses,
        special_definitions=resources.special,
        downpour_definitions=resources.downpour,
        blue_womb_definitions=resources.blue_womb,
    ).layout


def _generate_womb1(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> "Womb1FullResult":
    basement2 = generate_basement2_lifecycle(
        start_seed, difficulty, boss_entries=resources.bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        blue_womb_definitions=resources.blue_womb,
    )
    caves1 = generate_caves1_lifecycle(
        basement2, basement_boss_entries=resources.bosses,
        caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, blue_womb_definitions=resources.blue_womb,
    )
    caves2 = generate_caves2_lifecycle(
        caves1, basement_boss_entries=resources.bosses,
        caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, blue_womb_definitions=resources.blue_womb,
    )
    depths1 = generate_depths1_lifecycle(
        caves2, depths_boss_entries=resources.depths_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, depths_definitions=resources.depths,
        blue_womb_definitions=resources.blue_womb,
    )
    depths2 = generate_depths2_lifecycle(
        depths1, depths_boss_entries=resources.depths_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, depths_definitions=resources.depths,
        blue_womb_definitions=resources.blue_womb,
    )
    womb1 = generate_womb1_lifecycle(
        depths2, womb_boss_entries=resources.womb_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, depths_definitions=resources.depths,
        womb_definitions=resources.womb, blue_womb_definitions=resources.blue_womb,
    )
    return womb1.layout


def _generate_dross(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> "Basement1FullResult":
    from .dross_lifecycle import generate_dross_lifecycle

    return generate_dross_lifecycle(
        start_seed,
        difficulty,
        dross_boss_entries=resources.dross_bosses,
        special_definitions=resources.special,
        dross_definitions=resources.dross,
        blue_womb_definitions=resources.blue_womb,
    ).layout


def _generate_mines1(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> "Basement1FullResult":
    from .mines1_lifecycle import generate_mines1_lifecycle

    return generate_mines1_lifecycle(
        start_seed,
        difficulty,
        mines1_boss_entries=resources.mines_bosses,
        special_definitions=resources.special,
        mines1_definitions=resources.mines,
        blue_womb_definitions=resources.blue_womb,
    ).layout


def _generate_ashpit(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> "Basement1FullResult":
    from .ashpit_lifecycle import generate_ashpit_lifecycle

    return generate_ashpit_lifecycle(
        start_seed,
        difficulty,
        ashpit_boss_entries=resources.ashpit_bosses,
        special_definitions=resources.special,
        ashpit_definitions=resources.ashpit,
        blue_womb_definitions=resources.blue_womb,
    ).layout


def _generate_mausoleum1(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> "Basement1FullResult":
    from .mausoleum1_lifecycle import generate_mausoleum1_lifecycle

    return generate_mausoleum1_lifecycle(
        start_seed,
        difficulty,
        mausoleum1_boss_entries=resources.mausoleum_bosses,
        special_definitions=resources.special,
        mausoleum1_definitions=resources.mausoleum,
        blue_womb_definitions=resources.blue_womb,
    ).layout


def _generate_gehenna(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> "Basement1FullResult":
    from .gehenna_lifecycle import generate_gehenna_lifecycle

    return generate_gehenna_lifecycle(
        start_seed,
        difficulty,
        gehenna_boss_entries=resources.gehenna_bosses,
        special_definitions=resources.special,
        gehenna_definitions=resources.gehenna,
        blue_womb_definitions=resources.blue_womb,
    ).layout


def _generate_womb2(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> "Womb2FullResult":
    basement2 = generate_basement2_lifecycle(
        start_seed, difficulty, boss_entries=resources.bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        blue_womb_definitions=resources.blue_womb,
    )
    caves1 = generate_caves1_lifecycle(
        basement2, basement_boss_entries=resources.bosses,
        caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, blue_womb_definitions=resources.blue_womb,
    )
    caves2 = generate_caves2_lifecycle(
        caves1, basement_boss_entries=resources.bosses,
        caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, blue_womb_definitions=resources.blue_womb,
    )
    depths1 = generate_depths1_lifecycle(
        caves2, depths_boss_entries=resources.depths_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, depths_definitions=resources.depths,
        blue_womb_definitions=resources.blue_womb,
    )
    depths2 = generate_depths2_lifecycle(
        depths1, depths_boss_entries=resources.depths_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, depths_definitions=resources.depths,
        blue_womb_definitions=resources.blue_womb,
    )
    womb1 = generate_womb1_lifecycle(
        depths2, womb_boss_entries=resources.womb_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, depths_definitions=resources.depths,
        womb_definitions=resources.womb, blue_womb_definitions=resources.blue_womb,
    )
    womb2 = generate_womb2_lifecycle(
        womb1, womb_boss_entries=resources.womb_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, depths_definitions=resources.depths,
        womb_definitions=resources.womb, blue_womb_definitions=resources.blue_womb,
    )
    return womb2.layout


def _generate_basement1(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> Basement1FullResult:
    return generate_basement1_full(
        start_seed,
        difficulty,
        boss_entries=resources.bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
    )


def _generate_basement2(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> Basement2FullResult:
    return generate_basement2_full(
        start_seed,
        difficulty,
        boss_entries=resources.bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        blue_womb_definitions=resources.blue_womb,
    )



def _generate_caves1(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> Caves1FullResult:
    basement2 = generate_basement2_lifecycle(
        start_seed,
        difficulty,
        boss_entries=resources.bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        blue_womb_definitions=resources.blue_womb,
    )
    caves1 = generate_caves1_lifecycle(
        basement2,
        basement_boss_entries=resources.bosses,
        caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        caves_definitions=resources.caves,
        blue_womb_definitions=resources.blue_womb,
    )
    return caves1.layout


def _generate_caves2(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> Caves2FullResult:
    basement2 = generate_basement2_lifecycle(
        start_seed,
        difficulty,
        boss_entries=resources.bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        blue_womb_definitions=resources.blue_womb,
    )
    caves1 = generate_caves1_lifecycle(
        basement2,
        basement_boss_entries=resources.bosses,
        caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        caves_definitions=resources.caves,
        blue_womb_definitions=resources.blue_womb,
    )
    caves2 = generate_caves2_lifecycle(
        caves1,
        basement_boss_entries=resources.bosses,
        caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        caves_definitions=resources.caves,
        blue_womb_definitions=resources.blue_womb,
    )
    return caves2.layout



def _generate_depths1(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> Depths1FullResult:
    basement2 = generate_basement2_lifecycle(
        start_seed,
        difficulty,
        boss_entries=resources.bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        blue_womb_definitions=resources.blue_womb,
    )
    caves1 = generate_caves1_lifecycle(
        basement2,
        basement_boss_entries=resources.bosses,
        caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        caves_definitions=resources.caves,
        blue_womb_definitions=resources.blue_womb,
    )
    caves2 = generate_caves2_lifecycle(
        caves1,
        basement_boss_entries=resources.bosses,
        caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        caves_definitions=resources.caves,
        blue_womb_definitions=resources.blue_womb,
    )
    depths1 = generate_depths1_lifecycle(
        caves2,
        depths_boss_entries=resources.depths_bosses,
        special_definitions=resources.special,
        basement_definitions=resources.basement,
        caves_definitions=resources.caves,
        depths_definitions=resources.depths,
        blue_womb_definitions=resources.blue_womb,
    )
    return depths1.layout


def _generate_depths2(
    start_seed: int,
    difficulty: str,
    resources: _PreviewResources,
) -> Depths2FullResult:
    basement2 = generate_basement2_lifecycle(
        start_seed, difficulty, boss_entries=resources.bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        blue_womb_definitions=resources.blue_womb,
    )
    caves1 = generate_caves1_lifecycle(
        basement2, basement_boss_entries=resources.bosses, caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, blue_womb_definitions=resources.blue_womb,
    )
    caves2 = generate_caves2_lifecycle(
        caves1, basement_boss_entries=resources.bosses, caves_boss_entries=resources.caves_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, blue_womb_definitions=resources.blue_womb,
    )
    depths1 = generate_depths1_lifecycle(
        caves2, depths_boss_entries=resources.depths_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, depths_definitions=resources.depths,
        blue_womb_definitions=resources.blue_womb,
    )
    depths2 = generate_depths2_lifecycle(
        depths1, depths_boss_entries=resources.depths_bosses,
        special_definitions=resources.special, basement_definitions=resources.basement,
        caves_definitions=resources.caves, depths_definitions=resources.depths,
        blue_womb_definitions=resources.blue_womb,
    )
    return depths2.layout




# This is the sole product-facing support gate.  A floor is not generatable
# until its complete accepted layout has an independently recorded binary
# proof and differential corpus.
SUPPORTED_FLOORS: dict[str, PreviewFloorSpec] = {
    "Basement I": PreviewFloorSpec(
        "Basement I",
        "basement1",
        ("Basement I",),
        _generate_basement1,
    ),
    "Basement II": PreviewFloorSpec(
        "Basement II",
        "basement2",
        ("Basement I", "Basement II"),
        _generate_basement2,
    ),
    "Caves I": PreviewFloorSpec(
        "Caves I",
        "caves1",
        ("Basement I", "Basement II", "Caves I"),
        _generate_caves1,
    ),
    "Caves II": PreviewFloorSpec(
        "Caves II",
        "caves2",
        ("Basement I", "Basement II", "Caves I", "Caves II"),
        _generate_caves2,
    ),
    "Depths I": PreviewFloorSpec(
        "Depths I",
        "depths1",
        ("Basement I", "Basement II", "Caves I", "Caves II", "Depths I"),
        _generate_depths1,
    ),
    "Depths II": PreviewFloorSpec(
        "Depths II",
        "depths2",
        ("Basement I", "Basement II", "Caves I", "Caves II", "Depths I", "Depths II"),
        _generate_depths2,
    ),
    "Womb I": PreviewFloorSpec(
        "Womb I",
        "womb1",
        ("Basement I", "Basement II", "Caves I", "Caves II", "Depths I", "Depths II", "Womb I"),
        _generate_womb1,
    ),
    "Womb II": PreviewFloorSpec(
        "Womb II",
        "womb2",
        ("Basement I", "Basement II", "Caves I", "Caves II", "Depths I", "Depths II", "Womb I", "Womb II"),
        _generate_womb2,
    ),
    "Downpour I": PreviewFloorSpec(
        "Downpour I",
        "downpour1",
        ("Downpour I",),
        _generate_downpour1,
    ),
    "Dross": PreviewFloorSpec(
        "Dross",
        "dross",
        ("Downpour I", "Dross"),
        _generate_dross,
    ),
    "Mines I": PreviewFloorSpec(
        "Mines I",
        "mines1",
        ("Mines I",),
        _generate_mines1,
    ),
    "Ashpit": PreviewFloorSpec(
        "Ashpit",
        "ashpit",
        ("Mines I", "Ashpit"),
        _generate_ashpit,
    ),
    "Mausoleum I": PreviewFloorSpec(
        "Mausoleum I",
        "mausoleum1",
        ("Mausoleum I",),
        _generate_mausoleum1,
    ),
    "Gehenna": PreviewFloorSpec(
        "Gehenna",
        "gehenna",
        ("Mausoleum I", "Gehenna"),
        _generate_gehenna,
    ),
}


def generate_preview(
    seed: str | int,
    difficulty: str,
    floor: str,
    *,
    resource_root: Path | str | None = None,
) -> PreviewGeneration:
    """Generate a supported accepted-layout research map or fail closed.

    The accepted profile is the configured reproducible vanilla generation
    profile in NORMAL/HARD. Every floor outside ``SUPPORTED_FLOORS`` remains
    unsupported.
    """

    normalized_floor = str(floor).strip()
    spec = SUPPORTED_FLOORS.get(normalized_floor)
    if spec is None:
        raise UnsupportedPreviewFloor(
            f"{normalized_floor or floor!r}: UNSUPPORTED — generator not recovered yet"
        )

    normalized_difficulty = str(difficulty).strip().upper()
    if normalized_difficulty not in SUPPORTED_DIFFICULTIES:
        raise PreviewError("difficulty must be NORMAL or HARD")
    generation_profile = resolve_run_generation_profile()

    if isinstance(seed, str):
        start_seed = decode_seed(seed)
        display_seed = seed
    else:
        display_seed = encode_seed(seed)
        start_seed = seed

    root = Path(resource_root) if resource_root is not None else default_resource_root()
    resources = _load_preview_resources(str(root.resolve()))
    result = spec.generate(start_seed, normalized_difficulty, resources)
    if not result.completed:
        raise PreviewGenerationFailed(
            f"clean {spec.name} pipeline did not produce an accepted layout"
        )
    evidence = (
        "CONFIRMED_BINARY"
        if "CONFIRMED_BINARY" in result.generation_status
        else "PARTIAL_BINARY"
    )
    return PreviewGeneration(
        seed=display_seed,
        start_seed=start_seed,
        difficulty=normalized_difficulty,
        generation_profile=generation_profile.name,
        floor=spec.name,
        generation_status=result.generation_status,
        partial=False,
        algorithm_evidence=evidence,
        gameplay_fixture=GAMEPLAY_FIXTURE,
        replayed_floors=spec.replayed_floors,
        pipeline_result=result,
    )
