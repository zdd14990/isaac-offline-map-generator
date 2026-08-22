"""Extract coarse room components from a captured Isaac minimap PNG."""

from __future__ import annotations

from collections import Counter, deque
from pathlib import Path
import sys

from PIL import Image


def main() -> None:
    image = Image.open(Path(sys.argv[1])).convert("RGB")
    colors = Counter(image.getdata())
    print("size", image.size)
    print("colors", colors.most_common(12))

    # Vanilla minimap interiors in the supplied capture are flat-filled. Keep
    # only the neutral gray/white/red/gold room interiors and exclude the blue
    # animated floor background.
    pixels = image.load()
    mask: set[tuple[int, int]] = set()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue = pixels[x, y]
            neutral = max(red, green, blue) - min(red, green, blue) <= 10
            room_gray = neutral and 25 <= red <= 225
            dark_room_gray = 35 <= red <= 50 and 30 <= green <= 48 and 25 <= blue <= 42
            if room_gray or dark_room_gray:
                mask.add((x, y))

    components: list[tuple[int, int, int, int, int]] = []
    while mask:
        start = mask.pop()
        queue = deque((start,))
        min_x = max_x = start[0]
        min_y = max_y = start[1]
        size = 0
        while queue:
            x, y = queue.popleft()
            size += 1
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if neighbor in mask:
                    mask.remove(neighbor)
                    queue.append(neighbor)
        if size >= 100:
            components.append((min_x, min_y, max_x, max_y, size))

    for component in sorted(components, key=lambda item: (item[1], item[0])):
        print(component)


if __name__ == "__main__":
    main()
