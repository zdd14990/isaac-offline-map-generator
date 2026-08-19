# Resource Extraction and Database Notes

## Result

Static extraction produced:

- 156 named XML/STB paths from the installed `filelist.txt`;
- 166 archive-layer records;
- 95 merged last-wins files: 61 STB and 34 XML;
- 30,845 parsed `STB1` room definitions;
- 148,342 door records;
- 772,118 spawn positions and 777,626 weighted entity choices.

Generated indices:

- `research/input/extracted_resources/resource_index.csv`
- `research/resources/room_database_index.json`

The extracted payloads are research inputs and are Git-ignored.

## Archive path

`src/isaacmap/archive.py` is a clean Python implementation of the installed
`ARCH000` container mechanisms needed by the named resources: the two filename
hash functions, LZW, raw-DEFLATE MiniZ chunks, and archive checksum. Its format
interpretation was cross-checked with Gibbed.Rebirth commit
`8454c449cc60d680d57e3edb27ea9e56009c024a` and
BoIRResourceDecryption commit
`6fff8eb39c43474e6372ac4af0aa8ab2299130e4`.

Every archive read verifies the stored archive checksum. A raw encrypted
MiniZ transition is not yet implemented, but none of the 156 XML/STB targets in
the current `afterbirthp.a` uses it.

Merge order currently follows the official extractor's observed archive
enumeration for the selected data archives:

`repentance.a → config.a → rooms.a → afterbirth.a → afterbirthp.a`

Later records win. This ordering must be revalidated if the version profile or
the file list changes.

## STB path

`src/isaacmap/resources.py` parses the complete `STB1` record structure needed
for a room database: room type, variant, subtype, difficulty, name, weight,
stored and bordered dimensions, shape, doors, spawn positions, and weighted
entity choices. The binary layout was cross-checked independently with:

- Gibbed.Rebirth `StageBinaryFile.cs`;
- Basement Renovator `roomconvert.py`, commit
  `b703ca09b2f6a6a5143e665e46f7bfcfce120822`.

All 61 current merged STB files parse to exact EOF. Trailing bytes, truncation,
wrong magic, and invalid UTF-8 are rejected.

## Official extractor failure

The first allowed ResourceExtractor attempt created a log beside its tool and
failed; that log was moved into the project to restore the game directory.
Additional attempts used isolated copies under `research/input/`, but also
failed with Windows exception `0xc0000005`/heap corruption, including a small
archive case. No isolated attempt wrote to the game installation. All logs are
kept as `research/resources/ResourceExtractor_log*.failed.txt`.

The static reader is the current workaround. This is not a claim that the
official extractor is generally broken—only that it failed for this machine,
tool build, and archive set.
