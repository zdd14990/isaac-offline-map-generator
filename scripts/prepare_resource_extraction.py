"""Build an isolated ResourceExtractor harness containing only relevant inputs."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ARCHIVES = (
    "config.a",
    "rooms.a",
    "afterbirth.a",
    "afterbirthp.a",
    "repentance.a",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("game", type=Path)
    parser.add_argument("harness", type=Path)
    args = parser.parse_args()

    extractor_dir = args.game / "tools" / "ResourceExtractor"
    packed_dir = args.game / "resources" / "packed"
    harness_tool = args.harness / "tool"
    harness_input = args.harness / "input" / "resources" / "packed"
    harness_output = args.harness / "output"
    harness_tool.mkdir(parents=True, exist_ok=True)
    harness_input.mkdir(parents=True, exist_ok=True)
    harness_output.mkdir(parents=True, exist_ok=True)

    shutil.copy2(extractor_dir / "ResourceExtractor.exe", harness_tool / "ResourceExtractor.exe")

    source_lines = (extractor_dir / "filelist.txt").read_text(encoding="utf-8").splitlines()
    selected = sorted(
        line
        for line in source_lines
        if line.startswith("resources/") and line.lower().endswith((".xml", ".stb"))
    )
    (harness_tool / "filelist.txt").write_text("\n".join(selected) + "\n", encoding="utf-8")

    for archive in ARCHIVES:
        shutil.copy2(packed_dir / archive, harness_input / archive)

    print(f"Harness: {args.harness.resolve()}")
    print(f"Selected names: {len(selected)}")
    print(f"Archives: {', '.join(ARCHIVES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

