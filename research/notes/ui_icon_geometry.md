# Research Preview icon geometry and RoomType coverage

Profile: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

Executable SHA256:
`3BDFC8BAE0DC7E334B76009D0AD45DFBB16EE5F00C06FFBC3A0094E34D44616B`

Safety: this phase read only static installed resources and ran the project's
Python UI/tests. `isaac-ng.exe` was not started or loaded.

## P0 icon-center diagnosis

The old renderer averaged occupied-cell center coordinates, while drawing the
room from a rasterized union mask containing inter-cell bridges.  Those are
not quite the same geometry for large and L rooms.  It then centered the full
official 16x16 sprite frame.  The official glyph alpha is intentionally
offset within that frame (for example `IconSecretRoom` has alpha bounds
`(3, 2, 10, 10)`), so a mathematically centered frame still looked high and
left.

The renderer now:

1. obtains all occupied cells from the existing binary-derived RoomShape
   helper;
2. constructs the exact mask used to render their union and bridges;
3. calculates its alpha-weighted first moments to obtain the room geometry
   centroid;
4. resizes the fixed icon frame according to map zoom only with
   `Image.Resampling.NEAREST`;
5. calculates the resized sprite's alpha centroid and aligns that visible
   centroid to the room centroid.

Icon size does not depend on how many cells the RoomShape occupies. Tests cover
RoomShape values 1..12, all four L shapes, visible-alpha alignment and fixed
size across 1x1/2x2 rooms.

## P1 RoomType evidence and coverage

RoomType numeric values are copied from the frozen installation's static
`resources/scripts/enums.lua` (`ROOM_NULL=0` through
`ROOM_DEATHMATCH=30`). They are not inferred from enum order in the UI.

`src/isaacmap/ui/minimap_assets.py` indexes every ANM2 animation, layer,
frame, spritesheet id/path, crop, size, position and pivot. The semantic
RoomType-to-animation table selects official animation names; crop rectangles
are always read from ANM2 rather than duplicated in code.

The 22 RoomTypes with official room-related minimap animations are 2, 4, 5,
6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 24, 25, 26 and 29.
RoomTypes 3, 16, 22, 23, 27, 28 and 30 have no verified matching room icon in
this ANM2 and use explicit text fallback. Normal rooms remain unmarked; Start
uses `S` because the asset has no Start-room animation.

The M6 accepted descriptor types that can occur in the frozen canonical
Basement I profile all have official mappings: Shop, Treasure, Boss, MiniBoss,
Secret, Super Secret, Curse, Library, Sacrifice, Isaac's, Dice and
Planetarium. The legend is rebuilt from the final accepted map and lists only
special types that actually occur, plus fixed Start and Normal entries.

## Verification

- Targeted renderer/ANM2 tests: 51 passed.
- Full suite after P0/P1: 166 passed.
- Visual fixture NORMAL `B911 9PTT`: Sacrifice and Curse icons present.
- Visual fixture HARD `B911 9M4P`: MiniBoss, Sacrifice and Curse icons present.
- Screenshots: `output/screenshots/preview_secret_normal.png` and
  `output/screenshots/preview_secret_hard.png`.

