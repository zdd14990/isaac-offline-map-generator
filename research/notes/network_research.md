# Public Source Research

Research snapshot: 2026-08-17. Public sources are supporting evidence only;
current-executable static evidence takes priority.

## Reviewed repositories

| Project | Pinned commit | Useful evidence | Limit for this project |
|---|---|---|---|
| [REPENTOGON](https://github.com/TeamREPENTOGON/REPENTOGON) | `edf0a8cd58a170259a6d9c56dd5d742556d23cfb` | ZHL signatures/names for `Seeds`, `RNG`, and `LevelGenerator`; class layouts | Not a standalone floor generator. Runtime patching/scanning paths are prohibited and were not run. |
| [eden-seed-finder](https://github.com/2o181o28/eden-seed-finder) | `f8d46aac86505193a3906bd9cea486bbcbabdc63` | Seed string codec, xorshift implementation, 81-entry shift table, older stage-seed work | Its shift-table index 60 differs from this EXE and its stage-seed path is not yet accepted for the current profile. |
| [Basement Renovator](https://github.com/Basement-Renovator/basement-renovator) | `b703ca09b2f6a6a5143e665e46f7bfcfce120822` | Current STB parser and room shape/data conventions | Room editor/parser, not exact seed-to-floor generation. |
| [Gibbed.Rebirth](https://github.com/gibbed/Gibbed.Rebirth) | `8454c449cc60d680d57e3edb27ea9e56009c024a` | `ARCH000` and `STB1` file formats | Older data-tooling project, not Repentance+ level generation. |
| [BoIRResourceDecryption](https://github.com/bladecoding/BoIRResourceDecryption) | `6fff8eb39c43474e6372ac4af0aa8ab2299130e4` | Independent archive-format implementation | Resource decoding only. |

The public Python seed generator by ChildishGiant/SolarPolarMan was also used
as an independent checksum/alphabet cross-check:
https://gist.github.com/ChildishGiant/bf39d195dbdc9093417bc8f5b85b57e8

## Existing exact floor generator search

GitHub/web searches covered seed generators, RNG implementations, Isaac
`LevelGenerator`, `roomMap[169]`, stage seeds, map viewers, Secret/Super/Ultra
Secret placement, red-room generation, and Repentance/Repentance+ topology.
Among the reviewed results, no standalone implementation was found that proves
the full relation

`current Repentance+ start seed → exact stage seed → exact complete floor`

for this executable profile. Many results are mods, room editors, Eden/item
seed tools, navigation heuristics, or explicitly Isaac-like generators. They
cannot serve as a layout oracle or an exact implementation.

This is a bounded search result, not proof that no such project exists. Source
research should continue alongside binary work.

## Version-qualified fixture search

A second search after recovering the topology loop specifically required all
of: Repentance+ `v1.9.7.17`, seed, floor, difficulty, and a complete map. It
found a current-version changelog page and several Repentance+ seed posts, but
no sample satisfying all fields. The seed posts were published against older
Repentance+ builds or did not show a complete floor map. They are not accepted
as regression fixtures.

Result: `tests/fixtures/known_maps.json` contains an intentionally empty
fixture list rather than admitting an ambiguous-version oracle.

## Key version-difference finding

The copied EXE's 81 xorshift triples were extracted directly from RVA
`0x0071F4C8`. Public `eden-seed-finder` matches 80 entries but has `(9,5,1)` at
index 60; the current binary has `(9,5,14)`. This project uses the binary value
and records the difference rather than silently inheriting the older table.
