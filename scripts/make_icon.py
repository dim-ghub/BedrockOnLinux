#!/usr/bin/env python3
"""Generate data/icon.png (256x256) — a clean Minecraft-style grass block on a
rounded dark tile. Pure stdlib (zlib), no Pillow.  python3 scripts/make_icon.py"""
import struct, zlib, random
from pathlib import Path

W = H = 256
random.seed(11)

BG1 = (24, 27, 34)        # tile gradient top
BG2 = (15, 17, 21)        # tile gradient bottom
GRASS = (104, 187, 73)
GRASS_HI = (132, 209, 96)
GRASS_LO = (78, 150, 54)
DIRT = (140, 100, 70)
DIRT_DK = (108, 76, 52)
OUTLINE = (10, 12, 15)
RADIUS = 46


def rounded(x, y):
    """True if pixel is inside the rounded-rect tile."""
    for cx, cy in ((RADIUS, RADIUS), (W - RADIUS, RADIUS),
                   (RADIUS, H - RADIUS), (W - RADIUS, H - RADIUS)):
        if ((x < RADIUS and y < RADIUS and (cx, cy) == (RADIUS, RADIUS)) or
            (x > W - RADIUS and y < RADIUS and (cx, cy) == (W - RADIUS, RADIUS)) or
            (x < RADIUS and y > H - RADIUS and (cx, cy) == (RADIUS, H - RADIUS)) or
            (x > W - RADIUS and y > H - RADIUS and (cx, cy) == (W - RADIUS, H - RADIUS))):
            if (x - cx) ** 2 + (y - cy) ** 2 > RADIUS ** 2:
                return False
    return True


# block geometry: a 128px cube centred, with a slanted top face
BX, BY, BSZ = 64, 60, 128
CELL = BSZ // 16


def px(x, y):
    if not rounded(x, y):
        return None                                   # transparent
    inside_block = BX <= x < BX + BSZ and BY <= y < BY + BSZ
    if inside_block:
        lx, ly = x - BX, y - BY
        gx, gy = lx // CELL, ly // CELL
        # 1px block outline
        if lx < 3 or ly < 3 or lx >= BSZ - 3 or ly >= BSZ - 3:
            return OUTLINE
        if gy < 4:                                     # grass cap
            r = random.random()
            return GRASS_HI if r < .30 else (GRASS_LO if r > .85 else GRASS)
        if gy == 4:
            return GRASS if random.random() < .5 else DIRT
        return DIRT_DK if random.random() < .24 else DIRT
    # tile background vertical gradient + soft drop shadow under the block
    t = y / H
    r = int(BG1[0] * (1 - t) + BG2[0] * t)
    g = int(BG1[1] * (1 - t) + BG2[1] * t)
    b = int(BG1[2] * (1 - t) + BG2[2] * t)
    if BX - 10 <= x < BX + BSZ + 14 and BY + BSZ - 6 <= y < BY + BSZ + 22:
        r, g, b = int(r * .6), int(g * .6), int(b * .6)
    return (r, g, b)


rows = bytearray()
for y in range(H):
    rows.append(0)                                     # filter: none
    for x in range(W):
        p = px(x, y)
        rows += bytes((*p, 255)) if p else b"\0\0\0\0"


def chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data +
            struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))


png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
       + chunk(b"IDAT", zlib.compress(bytes(rows), 9))
       + chunk(b"IEND", b""))

out = Path(__file__).resolve().parent.parent / "data" / "icon.png"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(png)
print(f"wrote {out} ({len(png)} bytes, {W}x{H})")
