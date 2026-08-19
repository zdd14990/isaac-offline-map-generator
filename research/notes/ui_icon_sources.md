# Research Preview official icon sources

Profile: `Binding of Isaac: Repentance+ v1.9.7.17.J460`

Executable SHA256:
`3BDFC8BAE0DC7E334B76009D0AD45DFBB16EE5F00C06FFBC3A0094E34D44616B`

Safety: all discovery and extraction was static. `isaac-ng.exe` was not
started, loaded or invoked. The original game archives were read only; cropped
frames are written only to the project's ignored `output/ui_cache/` directory.

## Search result

The installed `tools/ResourceExtractor/filelist.txt` was searched for PNG,
ANM2 and XML paths matching `minimap`, `map icon`, `room icon`, `boss`,
`treasure`, `shop`, `secret`, `super secret`, and `ultra secret`. The current
official minimap icon actor is:

- Source asset: `resources/gfx/ui/minimap_icons.anm2` →
  `resources/gfx/ui/minimap_icons.png`
- Source archive: `C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\resources\packed\afterbirthp.a`
- Source ANM2: `resources/gfx/ui/minimap_icons.anm2`
- Source PNG: `resources/gfx/ui/minimap_icons.png`
- ANM2 spritesheet declaration: `Spritesheet Path="minimap_icons.png" Id="0"`

The same logical assets were checked across `graphics.a`, `afterbirth.a`,
`afterbirthp.a`, and `repentance.a`. The effective current pair is in
`afterbirthp.a`; `repentance.a` has no overriding entry for either path.

## Frame index and RoomType bindings

`src/isaacmap/ui/minimap_assets.py` now parses the complete ANM2 structure:
animation, layer id/name, animation frame, spritesheet id/path, crop, size,
position and pivot. Only semantic `RoomType -> animation name` bindings are
declared; the crop rectangles below are obtained from ANM2 at extraction time.

RoomType values are confirmed by the frozen installation's static
`resources/scripts/enums.lua`.

All rectangles use Pillow's `(left, top, right, bottom)` convention.

| RoomType | Preview key | ANM2 animation | Frame | Crop rectangle |
|---|---|---|---:|---|
| 2 `ROOM_SHOP` | `shop` | `IconShop` | 0 | `(0, 0, 16, 16)` |
| 4 `ROOM_TREASURE` | `treasure` | `IconTreasureRoom` | 0 | `(64, 0, 80, 16)` |
| 5 `ROOM_BOSS` | `boss` | `IconBoss` | 0 | `(16, 16, 32, 32)` |
| 6 `ROOM_MINIBOSS` | `miniboss` | `IconMiniboss` | 0 | `(0, 16, 16, 32)` |
| 7 `ROOM_SECRET` | `secret` | `IconSecretRoom` | 0 | `(16, 0, 32, 16)` |
| 8 `ROOM_SUPERSECRET` | `super_secret` | `IconSuperSecretRoom` | 0 | `(32, 0, 48, 16)` |
| 9 `ROOM_ARCADE` | `arcade` | `IconArcade` | 0 | `(96, 16, 112, 32)` |
| 10 `ROOM_CURSE` | `curse` | `IconCurseRoom` | 0 | `(64, 16, 80, 32)` |
| 11 `ROOM_CHALLENGE` | `challenge` | `IconAmbushRoom` | 0 | `(32, 16, 48, 32)` |
| 12 `ROOM_LIBRARY` | `library` | `IconLibrary` | 0 | `(48, 0, 64, 16)` |
| 13 `ROOM_SACRIFICE` | `sacrifice` | `IconSacrificeRoom` | 0 | `(80, 16, 96, 32)` |
| 14 `ROOM_DEVIL` | `devil` | `IconDevilRoom` | 0 | `(96, 0, 112, 16)` |
| 15 `ROOM_ANGEL` | `angel` | `IconAngelRoom` | 0 | `(80, 0, 96, 16)` |
| 17 `ROOM_BOSSRUSH` | `boss_rush` | `IconBossAmbushRoom` | 0 | `(48, 16, 64, 32)` |
| 18 `ROOM_ISAACS` | `isaacs` | `IconIsaacsRoom` | 0 | `(0, 32, 16, 48)` |
| 19 `ROOM_BARREN` | `barren` | `IconBarrenRoom` | 0 | `(16, 32, 32, 48)` |
| 20 `ROOM_CHEST` | `chest` | `IconChestRoom` | 0 | `(112, 16, 128, 32)` |
| 21 `ROOM_DICE` | `dice` | `IconDiceRoom` | 0 | `(112, 0, 128, 16)` |
| 24 `ROOM_PLANETARIUM` | `planetarium` | `IconPlanetarium` | 0 | `(64, 32, 80, 48)` |
| 25 `ROOM_TELEPORTER` | `teleporter` | `IconTeleporterRoom` | 0 | `(80, 32, 96, 48)` |
| 26 `ROOM_TELEPORTER_EXIT` | `teleporter_exit` | `IconTeleporterRoom` | 0 | `(80, 32, 96, 48)` |
| 29 `ROOM_ULTRASECRET` | `ultra_secret` | `IconUltraSecretRoom` | 0 | `(0, 128, 16, 144)` |

The runtime manifest is `output/ui_cache/icon_manifest.json`. Rendering uses
`Image.Resampling.NEAREST` to preserve the pixel art.

No official Start animation exists in this minimap icon ANM2. Start therefore
uses the permitted `S` text marker. Normal rooms have no icon. RoomTypes 3, 16,
22, 23, 27, 28 and 30 have no verified matching room animation and use the
explicit fallbacks `ERR`, `DNG`, `BM`, `GE`, `SE`, `BL` and `DM`. Ultra's
official frame is indexed and cached, but is not rendered until the generation
pipeline itself returns a type-29 descriptor.

## Fallback

If the verified archive/assets cannot be read, every known special RoomType
has a short text fallback. It does not download third-party art and does not
guess alternate Isaac filenames.
