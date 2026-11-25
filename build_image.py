#!/usr/bin/env python3
"""Front page for Wednesday 25 November 2026, drawn with Pillow.

One 1024x1024 PNG: masthead, a lead story, three mid-page cards,
three short stories and a ticker. Every picture is a flat vector-style
drawing made by the functions below; no external images are used.

Stories, as reported on 25 November 2026: Houthi fighters hit the
PIF Tower in Riyadh for the second time in a week, wounding 11;
Zelenskyy confirms Ukraine struck a Russian cargo ship in the Gulf
of Finland and sank a Russian warship off Benghazi; NATO sends
AWACS early-warning aircraft to Poland; Iran says three oil tankers
were hit by naval mines in the Strait of Hormuz; Gaza's death toll
reaches 74,746; the UN says five women are killed every hour by a
partner or family member; COP31 ends with no deal at all.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
MX = 36
FONTDIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (178, 34, 27)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GREY = (90, 86, 76)
SEA = (46, 110, 138)
WALL = (120, 116, 104)
ROOF = (84, 80, 70)
DARK = (52, 52, 52)
LIT = (255, 214, 130)
BRICK = (150, 52, 40)
SMOKE = (150, 148, 140)
SOOT = (120, 118, 110)
WATER = (38, 90, 120)
HULL = (60, 60, 62)
DECK = (200, 200, 190)
CRATE = (140, 140, 130)
PALE = (210, 230, 240)
LAND = (74, 140, 90)
OCEAN = (58, 124, 165)
FLAME1 = (255, 140, 0)
FLAME2 = (255, 90, 0)
FLAME3 = (255, 170, 40)
GOLD = (255, 220, 100)
NAVY = (20, 60, 56)
PURPLE = (102, 51, 153)
STEEL = (150, 160, 170)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTDIR, name), size)


def sb(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sr(size):
    return font("DejaVuSerif.ttf", size)


def hb(size):
    return font("DejaVuSans-Bold.ttf", size)


def rg(size):
    return font("DejaVuSans.ttf", size)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        elif cur:
            lines.append(cur)
            cur = word
        else:
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, width, color, step):
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=color)
        y += step
    return y


def rule(d, y, x0=None, x1=None, wdt=2):
    d.line([(x0 or MX, y), (x1 or W - MX, y)], fill=INK, width=wdt)


def kicker_title(d, x, y, width, kick, title, size):
    d.text((x, y), kick, font=hb(15), fill=RED)
    return para(d, x, y + 22, title, hb(size), width, INK, size + 4) + 4


def flames(d, cx, base, specs, half=10):
    for dx, h, col in specs:
        d.polygon([(cx + dx - half, base), (cx + dx, base - h),
                   (cx + dx + half, base)], fill=col)


def puffs(d, cx, top, radii, step, col):
    for i, r in enumerate(radii):
        cy = top - i * step
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def pic_tower(d, x, y, w, h):
    base = y + h
    tw = 62
    tx = x + (w - tw) // 2
    d.rectangle([tx, y + 6, tx + tw, base], fill=STEEL, outline=INK, width=2)
    yy = y + 16
    while yy < base - 8:
        d.line([(tx + 4, yy), (tx + tw - 4, yy)], fill=PALE, width=2)
        yy += 14
    sy = y + h // 2
    d.polygon([(tx + 6, sy - 6), (tx + tw // 2, sy + 2),
               (tx + tw - 6, sy - 8), (tx + tw - 2, sy + 12),
               (tx + 2, sy + 14)], fill=DARK)
    flames(d, tx + tw // 2, sy + 4,
           [(-10, 18, FLAME1), (4, 24, FLAME2)], half=8)
    puffs(d, tx + tw + 12, y + 26, (8, 11), 9, SMOKE)
    d.rectangle([x, base - 26, tx - 6, base], fill=WALL)
    d.rectangle([tx + tw + 6, base - 18, x + w, base], fill=WALL)


def pic_ship(d, x, y, w, h):
    sea = y + h - 24
    d.rectangle([x, sea, x + w, y + h], fill=WATER)
    d.rectangle([x + 10, sea - 26, x + w - 10, sea], fill=HULL)
    d.rectangle([x + w // 2 - 8, sea - 44, x + w // 2 + 22, sea - 26],
                fill=DECK)
    d.rectangle([x + 16, sea - 38, x + 44, sea - 26], fill=CRATE)
    fx = x + w // 2 + 4
    flames(d, fx, sea - 38,
           [(-16, 26, FLAME1), (0, 36, FLAME2), (16, 24, FLAME3)])
    puffs(d, fx + 8, y + 22, (9, 12), 10, SOOT)


def pic_radar(d, x, y, w, h):
    d.ellipse([x + 6, y + h - 52, x + 58, y + h], outline=INK, width=2)
    d.line([(x + 32, y + h - 26), (x + 32, y + h - 52)], fill=INK, width=2)
    d.arc([x + 14, y + h - 44, x + 50, y + h - 8], start=200, end=340,
          fill=TEAL, width=3)
    px, py = x + 120, y + 46
    d.polygon([(px - 70, py), (px + 60, py - 6), (px + 78, py),
               (px + 60, py + 6)], fill=DARK)
    d.polygon([(px - 20, py - 4), (px + 6, py - 26), (px + 16, py - 4)],
              fill=DARK)
    d.polygon([(px - 34, py + 4), (px - 8, py + 22), (px + 2, py + 4)],
              fill=DARK)
    d.ellipse([px - 6, py - 16, px + 26, py - 4], fill=STEEL,
              outline=INK, width=2)
    d.line([(px - 78, py), (px - 96, py - 8)], fill=INK, width=2)
    d.line([(px - 78, py), (px - 96, py + 8)], fill=INK, width=2)
    d.text((x + 210, y + 18), "AWACS", font=hb(22), fill=BLUE)


def pic_tanker(d, x, y, w, h):
    sea = y + h - 24
    d.rectangle([x, sea, x + w, y + h], fill=WATER)
    d.rectangle([x + 10, sea - 30, x + w - 10, sea], fill=HULL)
    d.rectangle([x + w - 60, sea - 52, x + w - 22, sea - 30], fill=DECK)
    d.rectangle([x + 24, sea - 44, x + w - 76, sea - 30], fill=BRICK)
    mx, my = x + w - 34, sea + 10
    d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=DARK,
              outline=INK, width=2)
    for dx, dy in ((-12, 0), (12, 0), (0, -12), (0, 12), (-8, -8),
                   (8, -8), (-8, 8), (8, 8)):
        d.line([(mx, my), (mx + dx, my + dy)], fill=DARK, width=2)


def pic_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN,
              outline=INK, width=3)
    for k in (-0.55, 0.0, 0.55):
        x0 = cx + int(r * k)
        d.arc([x0 - int(r * 0.45), cy - r, x0 + int(r * 0.45), cy + r],
              start=270, end=90, fill=PALE, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=PALE, width=2)
    d.ellipse([cx - r + 12, cy - r + 18, cx - 8, cy - 6], fill=LAND)
    d.ellipse([cx + 2, cy + 4, cx + r - 14, cy + r - 16], fill=LAND)
    crack = [(cx + 6, cy - r + 4), (cx - 12, cy - r // 2), (cx + 10, cy - 4),
             (cx - 8, cy + r // 3), (cx + 4, cy + r - 8)]
    d.line(crack, fill=RED, width=5, joint="curve")


def pic_drop(d, cx, cy, r):
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r], fill=OCEAN,
              outline=INK, width=2)
    d.polygon([(cx, cy - r - 14), (cx - r, cy - r // 2 + 4),
               (cx + r, cy - r // 2 + 4)], fill=OCEAN)
    d.text((cx, cy - 6), "!", font=hb(28), fill=(255, 255, 255),
           anchor="ma")


def pic_ribbon(d, cx, cy, s):
    d.ellipse([cx - s // 4, cy - s // 2, cx + s // 4, cy - 2],
              outline=PURPLE, width=4)
    d.polygon([(cx - s // 5, cy - 2), (cx + s // 5, cy - 2),
               (cx + s // 2, cy + s // 2), (cx + s // 8, cy + s // 2)],
              fill=PURPLE)
    d.polygon([(cx - s // 5, cy - 2), (cx + s // 5, cy - 2),
               (cx - s // 2, cy + s // 2), (cx - s // 8, cy + s // 2)],
              fill=PURPLE)


def main():
    page = Image.new("RGB", (W, W), PAPER)
    d = ImageDraw.Draw(page)

    rule(d, 30, wdt=3)
    d.text((W // 2, 44), "THE WORLD IN ONE PAGE", font=sb(56),
           fill=INK, anchor="mt")
    rule(d, 116)
    d.text((MX, 126), "WEDNESDAY, 25 NOVEMBER 2026", font=hb(19), fill=INK)
    d.text((W - MX, 126), "ONE DAY  ·  ONE PAGE", font=hb(19), fill=INK,
           anchor="rt")
    rule(d, 154, wdt=3)

    ly = 168
    d.text((MX, ly), "YEMEN  ·  RIYADH, SAUDI ARABIA", font=hb(16), fill=RED)
    d.text((MX, ly + 26), "RIYADH TOWER", font=sb(66), fill=INK)
    d.text((MX, ly + 100), "HIT AGAIN", font=sb(66), fill=INK)
    d.text((MX, ly + 178),
           "Drone strike wounds 11 in second attack in a week",
           font=sr(24), fill=INK)
    para(d, MX, ly + 216,
         "Houthi fighters strike the PIF Tower, the Saudi capital's "
         "tallest building and home of the sovereign wealth fund, for "
         "the second time in six days. The Saudi-led coalition vows a "
         "decisive response.", rg(18), 560, INK, 24)
    pic_tower(d, 700, ly + 20, 252, 250)
    d.text((826, ly + 276), "The PIF Tower, hit on 19 Nov", font=rg(15),
           fill=GREY, anchor="mt")
    d.text((826, ly + 296), "and again on 24 November.", font=rg(15),
           fill=GREY, anchor="mt")
    rule(d, 508)

    ry = 522
    cards = [
        (pic_ship, "UKRAINE  ·  BALTIC & LIBYA",
         "Kyiv confirms ship strikes",
         "Ukraine hit a Russian ship in the Gulf of Finland and sank "
         "a warship off Libya."),
        (pic_radar, "NATO  ·  POLAND",
         "AWACS jets to watch Poland",
         "NATO sends early-warning jets after missiles landed in "
         "Poland."),
        (pic_tanker, "IRAN  ·  STRAIT OF HORMUZ",
         "Three tankers hit by mines",
         "Iran's Guard says three oil tankers were hit by mines in "
         "the Strait of Hormuz."),
    ]
    for i, (art, kick, head, body) in enumerate(cards):
        cx = MX + i * 312
        after = kicker_title(d, cx, ry, 300, kick, head, 25)
        art(d, cx, after + 8, 300, 96)
        para(d, cx, after + 116, body, rg(15), 300, INK, 20)
    rule(d, 774)

    ry = 790
    shorts = [
        ("drop", 78, "GAZA  ·  THE TOLL",
         "Death toll now 74,746",
         "Oxfam: pollution risks", "cover 99% of the strip."),
        ("ribbon", 78, "WOMEN  ·  25 NOVEMBER",
         "Five women killed every hour",
         "UN: five women an hour", "killed by a partner or family."),
        ("globe", 86, "CLIMATE  ·  AFTER COP31",
         "No deal in Antalya",
         "Guterres: 'deeply", "disappointing' collapse."),
    ]
    for i, (kind, tx, kick, head, l1, l2) in enumerate(shorts):
        cx = MX + i * 312
        after = kicker_title(d, cx, ry, 300, kick, head, 23)
        if kind == "drop":
            pic_drop(d, cx + 40, after + 40, 24)
        elif kind == "ribbon":
            pic_ribbon(d, cx + 40, after + 34, 52)
        else:
            pic_globe(d, cx + 40, after + 36, 26)
        d.text((cx + tx, after + 10), l1, font=rg(16), fill=INK)
        d.text((cx + tx, after + 32), l2, font=rg(16), fill=INK)
    rule(d, 938)

    ty = 946
    d.text((MX, ty), "ALSO ON 25 NOVEMBER", font=hb(14), fill=RED)
    para(d, MX, ty + 22,
         "Sarkozy case to trial  ·  Trump pardons turkeys Freedom and "
         "Feathers  ·  England beat Australia in the 2nd T20I  ·  "
         "BJP–Akali ally for Punjab 2027  ·  Fort Hood shooter seeks "
         "stay of execution", rg(14), W - 2 * MX, INK, 18)
    rule(d, 1000)
    d.text((W // 2, 1006),
           "All stories as reported on Wednesday 25 November 2026",
           font=rg(12), fill=GREY, anchor="mt")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
