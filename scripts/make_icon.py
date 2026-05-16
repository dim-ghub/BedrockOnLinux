#!/usr/bin/env python3
"""Generate data/icon.png (256x256) — a Minecraft-style grass block.
Pure stdlib (zlib), no Pillow. Run: python3 scripts/make_icon.py"""
import struct, zlib, os, random
from pathlib import Path

S, SCALE = 16, 16
W = H = S * SCALE
random.seed(7)

GRASS_TOP = (94, 178, 64)
GRASS_HI = (122, 204, 90)
DIRT = (134, 96, 67)
DIRT_DK = (107, 74, 50)
EDGE = (32, 28, 24)

grid = [[DIRT for _ in range(S)] for _ in range(S)]
for y in range(S):
    for x in range(S):
        if y < 4:                                   # grass cap
            grid[y][x] = GRASS_HI if random.random() < .28 else GRASS_TOP
        elif y == 4:                                # ragged grass/dirt edge
            grid[y][x] = GRASS_TOP if random.random() < .5 else DIRT
        else:                                       # dirt body
            grid[y][x] = DIRT_DK if random.random() < .22 else DIRT
for i in range(S):                                  # 1px dark border
    grid[0][i] = grid[S - 1][i] = grid[i][0] = grid[i][S - 1] = EDGE

rows = bytearray()
for y in range(H):
    rows.append(0)                                  # PNG filter: none
    gy = y // SCALE
    for x in range(W):
        r, g, b = grid[gy][x // SCALE]
        rows += bytes((r, g, b, 255))


def chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data +
            struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))


png = b"\x89PNG\r\n\x1a\n"
png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
png += chunk(b"IDAT", zlib.compress(bytes(rows), 9))
png += chunk(b"IEND", b"")

out = Path(__file__).resolve().parent.parent / "data" / "icon.png"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(png)
print(f"wrote {out} ({len(png)} bytes, {W}x{H})")
