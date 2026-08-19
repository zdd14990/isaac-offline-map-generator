"""Launch or smoke-test the Tkinter canonical-floor research map."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from isaacmap.ui.app import capture_smoke_screenshots, main as run_app


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--smoke-screenshots",
        action="store_true",
        help="run NORMAL and HARD in the real Tk UI and capture both windows",
    )
    parser.add_argument("--seed", default="B911 99AC")
    parser.add_argument("--normal-seed")
    parser.add_argument("--hard-seed")
    parser.add_argument("--floor", default="Basement I")
    args = parser.parse_args()
    if args.smoke_screenshots:
        for output in capture_smoke_screenshots(
            args.normal_seed or args.seed,
            args.hard_seed or args.seed,
            args.floor,
        ):
            print(output.resolve())
        return 0
    return run_app()


if __name__ == "__main__":
    raise SystemExit(main())
