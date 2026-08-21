"""Headless, GUI-free entry point for bots.

This is the single stable surface a bot should call.  It reuses the confirmed
clean generation pipelines, the Pillow renderer and the official minimap icon
cache from this package; it never opens a Tk window, never performs UI
automation and never launches the game executable.

A bot needs only::

    from isaacmap.bot_api import generate_map_image_for_bot

    result = generate_map_image_for_bot("B911 99AC", "NORMAL", 5, "cache/isaac_maps")

The supported floors and their stage numbers are derived from the single
``SUPPORTED_FLOORS`` registry in :mod:`isaacmap.preview`, so a caller never
maintains a second copy of the support truth.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path

from .preview import (
    SUPPORTED_FLOORS,
    PreviewError,
    PreviewGenerationFailed,
    UnsupportedPreviewFloor,
    generate_preview,
)
from .seed import InvalidSeedError, decode_seed
from .generation_profile import RunGenerationProfile, resolve_run_generation_profile

# Version-locked executable profile.  Both values feed the cache key so a
# changed generator/executable silently invalidates previously cached images.
EXE_SHA256 = "3bdfc8bae0dc7e334b76009d0ad45dfbb16ee5f00c06ffbc3a0094e34d44616b"
SUPPORT_VERSION = "first_release_scope_v1"

SUPPORTED_DIFFICULTIES = ("NORMAL", "HARD")

MAIN_ROUTE = "MAIN"
ALT_ROUTE = "ALT"
ROUTES = (MAIN_ROUTE, ALT_ROUTE)

# Factual floor names for every user-facing stage token.  Support status comes
# from ``SUPPORTED_FLOORS`` (the generation truth), never from this table.
MAIN_FLOOR_NAMES: dict[int, str] = {
    1: "Basement I",
    2: "Basement II",
    3: "Caves I",
    4: "Caves II",
    5: "Depths I",
    6: "Depths II",
    7: "Womb I",
    8: "Womb II",
}
ALT_FLOOR_NAMES: dict[int, str] = {
    1: "Downpour I",
    2: "Dross",
    3: "Mines I",
    4: "Ashpit",
    5: "Mausoleum I",
    6: "Gehenna",
}
FLOOR_NAMES: dict[str, dict[int, str]] = {
    MAIN_ROUTE: MAIN_FLOOR_NAMES,
    ALT_ROUTE: ALT_FLOOR_NAMES,
}


def parse_stage_token(token: str) -> tuple[str, int] | None:
    """Parse a user stage token into ``(route, stage)`` or ``None``.

    Accepts main-route ``"1".."8"`` and alternate-route ``"1+".."6+"``.
    Validation is syntactic only; support is decided by ``SUPPORTED_FLOORS``.
    """

    text = str(token).strip()
    if not text:
        return None
    if text.endswith("+"):
        if len(text) != 2 or not text[0].isdigit():
            return None
        stage = int(text[0])
        if stage not in ALT_FLOOR_NAMES:
            return None
        return (ALT_ROUTE, stage)
    if text.isdigit():
        stage = int(text)
        if stage not in MAIN_FLOOR_NAMES:
            return None
        return (MAIN_ROUTE, stage)
    return None


def floor_name_for(route: str, stage_number: int) -> str | None:
    """Return the factual floor name for a route/stage, or ``None``."""
    return FLOOR_NAMES.get(route, {}).get(stage_number)

# Backward-compatible numeric mapping for the MAIN route.  ALT has its own
# overlapping 1+..6+ namespace and is reported separately by ``--supported``.
STAGE_TO_FLOOR: dict[int, str] = {
    stage: name
    for stage, name in MAIN_FLOOR_NAMES.items()
    if name in SUPPORTED_FLOORS
}
FLOOR_TO_STAGE: dict[str, int] = {name: stage for stage, name in STAGE_TO_FLOOR.items()}


def stage_number_to_floor_name(stage_number: int) -> str | None:
    """Map a numeric stage to its floor name, or ``None`` when unsupported."""
    return STAGE_TO_FLOOR.get(stage_number)


def supported_stage_numbers() -> tuple[int, ...]:
    """Return the supported MAIN-route numeric stages, ascending."""
    return tuple(sorted(STAGE_TO_FLOOR))


def supported_stage_summary() -> str:
    """Human-readable summary of the supported stage range (for bot replies).

    MAIN and ALT are separate routes with independent stage numbering, so the
    summary lists both ranges explicitly instead of merging them.
    """

    parts: list[str] = []
    for route, token_suffix in ((MAIN_ROUTE, ""), (ALT_ROUTE, "+")):
        names = FLOOR_NAMES[route]
        supported = [
            stage for stage, name in names.items() if name in SUPPORTED_FLOORS
        ]
        if not supported:
            continue
        first = names[supported[0]]
        last = names[supported[-1]]
        parts.append(
            f"stage {supported[0]}{token_suffix}-{supported[-1]}{token_suffix}"
            f"（{first} 到 {last}）"
        )
    return "；".join(parts)


@dataclass
class BotMapResult:
    """Structured result of one headless map-image request."""

    ok: bool
    error: str | None = None
    error_message: str | None = None
    floor_name: str | None = None
    stage_number: int | None = None
    route: str | None = None
    difficulty: str | None = None
    generation_profile: str | None = None
    seed_text: str | None = None
    image_path: str | None = None
    json_path: str | None = None
    attempts: int | None = None
    cache_hit: bool = False
    algorithm_evidence: str | None = None


def normalize_seed_text(seed_text: str) -> str | None:
    """Compact/upper-case a user seed into the binary's ``XXXX XXXX`` form.

    This is format normalization only (the same edit the preview UI performs
    on its seed field).  Checksum validation stays with :func:`decode_seed`.
    Returns ``None`` when the compacted text is not exactly eight characters.
    """
    compact = "".join(str(seed_text).split()).upper()
    if len(compact) != 8:
        return None
    return f"{compact[:4]} {compact[4:]}"


def _version_token(profile: RunGenerationProfile | None = None) -> str:
    """Fold executable, support and generation-profile state into cache keys."""
    resolved = profile or resolve_run_generation_profile()
    payload = f"{EXE_SHA256}|{SUPPORT_VERSION}|{resolved.fingerprint}"
    return sha256(payload.encode("utf-8")).hexdigest()[:8]


_ICONS: dict | None = None


def _load_icons() -> dict:
    """Load the official minimap icon cache once (in-process memoized)."""
    global _ICONS
    if _ICONS is not None:
        return _ICONS
    from .ui.icons import ensure_official_icon_cache

    project_root = Path(__file__).resolve().parents[2]
    cache_dir = project_root / "output" / "ui_cache"
    _ICONS = dict(ensure_official_icon_cache(cache_dir).images)
    return _ICONS

def generate_map_image_for_bot(
    seed_text: str,
    difficulty: str,
    stage_number: int,
    output_dir: str,
    *,
    route: str = MAIN_ROUTE,
    canvas_width: int = 1400,
    canvas_height: int = 900,
) -> BotMapResult:
    """Generate (or reuse a cached) PNG for one supported floor, fail closed.

    ``difficulty`` is ``"NORMAL"`` or ``"HARD"``; ``route`` is ``"MAIN"`` or
    ``"ALT"``; ``stage_number`` is the numeric stage inside that route.  The
    produced PNG and a JSON snapshot land in ``output_dir`` with a file name
    that also encodes the route, executable hash and support version, which
    makes the file name itself the cache key (so main ``1`` and alt ``1+``
    never collide).
    """

    normalized_difficulty = str(difficulty).strip().upper()
    if normalized_difficulty not in SUPPORTED_DIFFICULTIES:
        return BotMapResult(
            ok=False,
            error="INVALID_DIFFICULTY",
            error_message=f"difficulty must be NORMAL or HARD, got {difficulty!r}",
        )

    normalized_route = str(route).strip().upper()
    if normalized_route not in ROUTES:
        return BotMapResult(
            ok=False,
            error="INVALID_ROUTE",
            error_message=f"route must be MAIN or ALT, got {route!r}",
        )

    if isinstance(stage_number, bool) or not isinstance(stage_number, int):
        return BotMapResult(
            ok=False,
            error="INVALID_STAGE",
            error_message=f"stage must be an integer, got {stage_number!r}",
        )
    floor_name = floor_name_for(normalized_route, stage_number)
    if floor_name is None:
        return BotMapResult(
            ok=False,
            error="INVALID_STAGE",
            error_message=(
                f"stage {stage_number} is outside route {normalized_route}; "
                f"valid stages: {', '.join(map(str, FLOOR_NAMES[normalized_route]))}"
            ),
            route=normalized_route,
            stage_number=stage_number,
        )
    if floor_name not in SUPPORTED_FLOORS:
        return BotMapResult(
            ok=False,
            error="UNSUPPORTED_FLOOR",
            error_message=(
                f"{floor_name} is not in the SUPPORTED_FLOORS registry; "
                "generation is FAIL CLOSED until it is reconstructed"
            ),
            floor_name=floor_name,
            route=normalized_route,
            stage_number=stage_number,
        )


    normalized_seed = normalize_seed_text(seed_text)
    if normalized_seed is None:
        return BotMapResult(
            ok=False,
            error="INVALID_SEED",
            error_message=f"seed must be exactly 8 characters, got {seed_text!r}",
            seed_text=str(seed_text),
        )
    try:
        decode_seed(normalized_seed)  # always use the strict binary validator
    except (InvalidSeedError, TypeError, ValueError) as exc:
        return BotMapResult(
            ok=False,
            error="INVALID_SEED",
            seed_text=normalized_seed,
        )

    try:
        generation_profile = resolve_run_generation_profile()
    except ValueError as exc:
        return BotMapResult(
            ok=False,
            error="INVALID_PROFILE",
            error_message=str(exc),
            floor_name=floor_name,
            stage_number=stage_number,
            route=normalized_route,
            difficulty=normalized_difficulty,
            seed_text=normalized_seed,
        )

    version_token = _version_token(generation_profile)
    compact_seed = normalized_seed.replace(" ", "")
    base_name = f"{compact_seed}_{normalized_route}_{normalized_difficulty}_stage{stage_number}_{version_token}"
    out_dir = Path(output_dir)
    image_path = out_dir / f"{base_name}.png"
    json_path = out_dir / f"{base_name}.json"

    # Cache hit: same seed + difficulty + stage + exe/support version already
    if image_path.is_file():
        attempts = None
        evidence = None
        try:
            cached = json.loads(json_path.read_text(encoding="utf-8"))
            attempts = cached.get("attempts")
            evidence = cached.get("algorithm_evidence")
        except (OSError, ValueError):
            attempts = None
        return BotMapResult(
            ok=True,
            floor_name=floor_name,
            stage_number=stage_number,
            route=normalized_route,
            difficulty=normalized_difficulty,
            generation_profile=generation_profile.name,
            seed_text=normalized_seed,
            image_path=str(image_path),
            json_path=str(json_path) if json_path.is_file() else None,
            attempts=attempts,
            cache_hit=True,
            algorithm_evidence=evidence,
        )

    try:
        preview = generate_preview(normalized_seed, normalized_difficulty, floor_name)
    except UnsupportedPreviewFloor as exc:
        return BotMapResult(
            ok=False,
            error="UNSUPPORTED_FLOOR",
            error_message=str(exc),
            floor_name=floor_name,
            stage_number=stage_number,
            route=normalized_route,
            generation_profile=generation_profile.name,
            seed_text=normalized_seed,
        )
    except (PreviewGenerationFailed, PreviewError, OSError, ValueError) as exc:
        return BotMapResult(
            ok=False,
            error="GENERATION_FAILED",
            error_message=str(exc),
            floor_name=floor_name,
            stage_number=stage_number,
            route=normalized_route,
            difficulty=normalized_difficulty,
            generation_profile=generation_profile.name,
            seed_text=normalized_seed,
        )

    try:
        from .ui.models import PreviewMapModel, preview_to_dict
        from .ui.renderer import render_map

        model = PreviewMapModel.from_preview(preview)
        image, _layout = render_map(
            model,
            canvas_width,
            canvas_height,
            icons=_load_icons(),
        )
        payload = preview_to_dict(preview)
        payload.setdefault("seed_text", normalized_seed)
        payload.setdefault("difficulty", normalized_difficulty)
        payload.setdefault("generation_profile", generation_profile.name)
        payload.setdefault("floor_name", floor_name)
        payload.setdefault("stage_number", stage_number)
        payload.setdefault("route", normalized_route)
        payload.setdefault("algorithm_evidence", preview.algorithm_evidence)
    except Exception as exc:  # render must never crash the caller
        return BotMapResult(
            ok=False,
            error="GENERATION_FAILED",
            error_message=f"render/export failed: {exc}",
            floor_name=floor_name,
            stage_number=stage_number,
            route=normalized_route,
            difficulty=normalized_difficulty,
            generation_profile=generation_profile.name,
            seed_text=normalized_seed,
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        tmp_png = Path(f"{image_path}.tmp")
        image.convert("RGBA").save(tmp_png, format="PNG")
        os.replace(tmp_png, image_path)

        tmp_json = Path(f"{json_path}.tmp")
        tmp_json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        os.replace(tmp_json, json_path)
    except Exception as exc:
        return BotMapResult(
            ok=False,
            error="GENERATION_FAILED",
            error_message=f"writing output failed: {exc}",
            floor_name=floor_name,
            stage_number=stage_number,
            route=normalized_route,
            difficulty=normalized_difficulty,
            generation_profile=generation_profile.name,
            seed_text=normalized_seed,
        )

    return BotMapResult(
        ok=True,
        floor_name=floor_name,
        stage_number=stage_number,
        route=normalized_route,
        difficulty=normalized_difficulty,
        generation_profile=generation_profile.name,
        seed_text=normalized_seed,
        image_path=str(image_path),
        json_path=str(json_path),
        attempts=preview.attempt_count,
        cache_hit=False,
        algorithm_evidence=preview.algorithm_evidence,
    )


def main(argv: list[str] | None = None) -> int:
    """Small stable CLI (subprocess fallback) mirroring the import API."""
    parser = argparse.ArgumentParser(
        prog="isaacmap.bot_api",
        description="Headless Isaac floor-map PNG/JSON export for bots.",
    )
    parser.add_argument("--seed")
    parser.add_argument("--difficulty", choices=("NORMAL", "HARD"))
    parser.add_argument("--stage", type=int)
    parser.add_argument("--route", choices=ROUTES, default=MAIN_ROUTE)
    parser.add_argument("--output-dir")
    parser.add_argument("--canvas-width", type=int, default=1400)
    parser.add_argument("--canvas-height", type=int, default=900)
    parser.add_argument(
        "--supported",
        action="store_true",
        help="print the supported stage registry as JSON and exit",
    )
    args = parser.parse_args(argv)

    if args.supported:
        generation_profile = resolve_run_generation_profile()
        print(
            json.dumps(
                {
                    "generation_profile": generation_profile.name,
                    "curse_rates": {
                        "NORMAL": generation_profile.normal_curse_rate,
                        "HARD": generation_profile.hard_curse_rate,
                    },
                    "stages": list(supported_stage_numbers()),
                    "summary": supported_stage_summary(),
                    "routes": {
                        route: {
                            str(stage): name
                            for stage, name in FLOOR_NAMES[route].items()
                        }
                        for route in ROUTES
                    },
                    "supported": {
                        route: [
                            stage
                            for stage, name in FLOOR_NAMES[route].items()
                            if name in SUPPORTED_FLOORS
                        ]
                        for route in ROUTES
                    },
                },
                ensure_ascii=False,
            )
        )
        return 0

    if not args.seed or not args.difficulty or args.stage is None or not args.output_dir:
        parser.error("--seed, --difficulty, --stage and --output-dir are required")

    result = generate_map_image_for_bot(
        args.seed,
        args.difficulty,
        args.stage,
        args.output_dir,
        route=args.route,
        canvas_width=args.canvas_width,
        canvas_height=args.canvas_height,
    )
    print(json.dumps(asdict(result), ensure_ascii=False))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
