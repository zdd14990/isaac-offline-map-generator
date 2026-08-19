"""Headless CLI launcher for :mod:`isaacmap.bot_api` (bot subprocess entry).

A bot shelling out should run this script rather than importing the package:
it mirrors the repo's existing ``launch_preview.py`` pattern by putting the
``src`` directory on ``sys.path`` before importing, so the ``isaacmap``
package resolves regardless of the caller's working directory.

Usage (JSON on stdout)::

    python scripts/map_export.py --seed "B911 99AC" --difficulty NORMAL \
        --stage 5 --output-dir /path/to/cache
    python scripts/map_export.py --supported
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from isaacmap.bot_api import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
