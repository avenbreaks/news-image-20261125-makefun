#!/usr/bin/env python3
"""Render the front page for Wednesday 25 November 2026.

Everything is drawn from scratch with Pillow: a masthead, one lead
story, three mid-page stories and three short stories, each with a
small flat illustration, plus a ticker of the day's other news. The
output is a 1024 by 1024 PNG, deterministic, so running the script
twice gives byte-identical files.

The stories are the headlines as reported on 25 November 2026:
Houthi fighters hit Riyadh's tallest tower, the PIF Tower, for the
second time in a week, wounding 11; Zelenskyy confirms Ukraine
struck a Russian cargo ship in the Gulf of Finland and sank a
Russian warship off Benghazi, Libya, and Moscow calls it
"terrorism"; NATO sends AWACS early-warning aircraft to Poland
after missiles landed there during an attack on Ukraine; Iran says
three oil tankers were hit by naval mines in the Strait of Hormuz;
Gaza's death toll reaches 74,746 and Oxfam warns pollution risks
cover 99% of the strip; the UN says five women are killed every
hour by a partner or family member; COP31's collapse leaves
climate talks with no deal at all.
The ticker adds Sarkozy's corruption case going to trial, Trump's
Thanksgiving turkey pardon, England's T20 win over Australia, the
BJP-Akali alliance for Punjab 2027, the Fort Hood shooter's stay
of execution, and RFE/RL's return to shortwave for Afghan girls.
"""
import os  # filesystem paths
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

SIDE = 1024
MARGIN = 36
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PALETTE = {
    "paper": (246, 241, 229),
    "ink": (20, 20, 20),
    "red": (178, 34, 27),
    "blue": (31, 78, 121),
    "teal": (15, 118, 110),
    "grey": (90, 86, 76),
    "sea": (46, 110, 138),
    "wall": (120, 116, 104),
    "roof": (84, 80, 70),
    "dark": (52, 52, 52),
    "lit": (255, 214, 130),
    "brick": (150, 52, 40),
    "smoke": (150, 148, 140),
    "soot": (120, 118, 110),
    "water": (38, 90, 120),
    "hull": (60, 60, 62),
    "deck": (200, 200, 190),
    "crate": (140, 140, 130),
    "pale": (210, 230, 240),
    "land": (74, 140, 90),
    "ocean": (58, 124, 165),
    "flame_a": (255, 140, 0),
    "flame_b": (255, 90, 0),
    "flame_c": (255, 170, 40),
    "gold": (255, 220, 100),
    "navy": (20, 60, 56),
    "purple": (102, 51, 153),
    "steel": (150, 160, 170),
}


def load_font(filename, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


def serif_bold(size):
    return load_font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load_font("DejaVuSerif.ttf", size)


def sans_bold(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return load_font("DejaVuSans.ttf", size)


def split_words(dr, text, fnt, width):
    """Greedy word wrap: lines that fit inside width."""
    out = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if dr.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def draw_lines(dr, x, y, text, fnt, width, color, gap):
    """Draw wrapped text, return the y just below the last line."""
    for ln in split_words(dr, text, fnt, width):
        dr.text((x, y), ln, font=fnt, fill=color)
        y += gap
    return y


def hline(dr, x0, y, x1, width=2):
    dr.line([(x0, y), (x1, y)], fill=PALETTE["ink"], width=width)


def card_title(dr, x, y, width, kicker, title, tsize):
    """Kicker + wrapped title; returns y below the title block."""
    dr.text((x, y), kicker, font=sans_bold(15), fill=PALETTE["red"])
    end = draw_lines(dr, x, y + 22, title, sans_bold(tsize), width,
                     PALETTE["ink"], tsize + 4)
    return end + 4


def flame_row(dr, cx, base_y, specs, half=10):
    """A row of triangular flames centred on cx, sitting on base_y."""
    for dx, height, colour in specs:
        dr.polygon([(cx + dx - half, base_y), (cx + dx, base_y - height),
                    (cx + dx + half, base_y)], fill=colour)


def smoke_puffs(dr, cx, top_y, radii, step, colour):
    """Grey puffs rising from top_y, each step pixels higher."""
    for i, rr in enumerate(radii):
        cy = top_y - i * step
        dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=colour)


def tower_art(dr, x, y, w, h):
    """Riyadh's PIF Tower: a tall glass slab, scarred mid-height."""
    ink = PALETTE["ink"]
    base = y + h
    tw = 62
    tx = x + (w - tw) // 2
    dr.rectangle([tx, y + 6, tx + tw, base], fill=PALETTE["steel"],
                 outline=ink, width=2)
    for wy in range(y + 16, base - 8, 14):
        dr.line([(tx + 4, wy), (tx + tw - 4, wy)], fill=PALETTE["pale"],
                width=2)
    # blast scar about halfway up
    sy = y + h // 2
    dr.polygon([(tx + 6, sy - 6), (tx + tw // 2, sy + 2),
                (tx + tw - 6, sy - 8), (tx + tw - 2, sy + 12),
                (tx + 2, sy + 14)], fill=PALETTE["dark"])
    flame_row(dr, tx + tw // 2, sy + 4,
              [(-10, 18, PALETTE["flame_a"]), (4, 24, PALETTE["flame_b"])],
              half=8)
    smoke_puffs(dr, tx + tw + 12, y + 26, (8, 11), 9, PALETTE["smoke"])
    # low skyline
    dr.rectangle([x, base - 26, tx - 6, base], fill=PALETTE["wall"])
    dr.rectangle([tx + tw + 6, base - 18, x + w, base],
                 fill=PALETTE["wall"])


def ship_art(dr, x, y, w, h):
    """Cargo ship burning on the sea, inside its box."""
    sea_y = y + h - 24
    dr.rectangle([x, sea_y, x + w, y + h], fill=PALETTE["water"])
    dr.rectangle([x + 10, sea_y - 26, x + w - 10, sea_y],
                 fill=PALETTE["hull"])
    dr.rectangle([x + w // 2 - 8, sea_y - 44, x + w // 2 + 22, sea_y - 26],
                 fill=PALETTE["deck"])
    dr.rectangle([x + 16, sea_y - 38, x + 44, sea_y - 26],
                 fill=PALETTE["crate"])
    fx = x + w // 2 + 4
    flame_row(dr, fx, sea_y - 38,
              [(-16, 26, PALETTE["flame_a"]), (0, 36, PALETTE["flame_b"]),
               (16, 24, PALETTE["flame_c"])])
    smoke_puffs(dr, fx + 8, y + 22, (9, 12), 10, PALETTE["soot"])


def radar_art(dr, x, y, w, h):
    """AWACS plane over a radar sweep, inside its box."""
    ink = PALETTE["ink"]
    dr.ellipse([x + 6, y + h - 52, x + 58, y + h], outline=ink, width=2)
    dr.line([(x + 32, y + h - 26), (x + 32, y + h - 52)], fill=ink,
            width=2)
    dr.arc([x + 14, y + h - 44, x + 50, y + h - 8], start=200, end=340,
           fill=PALETTE["teal"], width=3)
    # plane silhouette, nose right
    px, py = x + 120, y + 46
    dr.polygon([(px - 70, py), (px + 60, py - 6), (px + 78, py),
                (px + 60, py + 6)], fill=PALETTE["dark"])
    dr.polygon([(px - 20, py - 4), (px + 6, py - 26), (px + 16, py - 4)],
               fill=PALETTE["dark"])
    dr.polygon([(px - 34, py + 4), (px - 8, py + 22), (px + 2, py + 4)],
               fill=PALETTE["dark"])
    dr.ellipse([px - 6, py - 16, px + 26, py - 4], fill=PALETTE["steel"],
               outline=ink, width=2)
    dr.line([(px - 78, py), (px - 96, py - 8)], fill=ink, width=2)
    dr.line([(px - 78, py), (px - 96, py + 8)], fill=ink, width=2)
    dr.text((x + 210, y + 18), "AWACS", font=sans_bold(22),
            fill=PALETTE["blue"])


def tanker_art(dr, x, y, w, h):
    """Oil tanker on the sea with a naval mine, inside its box."""
    sea_y = y + h - 24
    dr.rectangle([x, sea_y, x + w, y + h], fill=PALETTE["water"])
    dr.rectangle([x + 10, sea_y - 30, x + w - 10, sea_y],
                 fill=PALETTE["hull"])
    dr.rectangle([x + w - 60, sea_y - 52, x + w - 22, sea_y - 30],
                 fill=PALETTE["deck"])
    dr.rectangle([x + 24, sea_y - 44, x + w - 76, sea_y - 30],
                 fill=PALETTE["brick"])
    # spiked mine floating ahead of the bow
    mx, my = x + w - 34, sea_y + 10
    dr.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=PALETTE["dark"],
               outline=PALETTE["ink"], width=2)
    for dx, dy in ((-12, 0), (12, 0), (0, -12), (0, 12), (-8, -8),
                   (8, -8), (-8, 8), (8, 8)):
        dr.line([(mx, my), (mx + dx, my + dy)], fill=PALETTE["dark"],
                width=2)


def globe_art(dr, cx, cy, r):
    """A cracked globe: blue disc, meridians, red crack."""
    ink = PALETTE["ink"]
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PALETTE["ocean"],
               outline=ink, width=3)
    for k in (-0.55, 0.0, 0.55):
        x0 = cx + int(r * k)
        dr.arc([x0 - int(r * 0.45), cy - r, x0 + int(r * 0.45), cy + r],
               start=270, end=90, fill=PALETTE["pale"], width=2)
    dr.line([(cx - r, cy), (cx + r, cy)], fill=PALETTE["pale"], width=2)
    dr.ellipse([cx - r + 12, cy - r + 18, cx - 8, cy - 6],
               fill=PALETTE["land"])
    dr.ellipse([cx + 2, cy + 4, cx + r - 14, cy + r - 16],
               fill=PALETTE["land"])
    crack = [(cx + 6, cy - r + 4), (cx - 12, cy - r // 2), (cx + 10, cy - 4),
             (cx - 8, cy + r // 3), (cx + 4, cy + r - 8)]
    dr.line(crack, fill=PALETTE["red"], width=5, joint="curve")


def drop_art(dr, cx, cy, r):
    """A water drop with a warning mark, for the Gaza story."""
    dr.ellipse([cx - r, cy - r // 2, cx + r, cy + r],
               fill=PALETTE["ocean"], outline=PALETTE["ink"], width=2)
    dr.polygon([(cx, cy - r - 14), (cx - r, cy - r // 2 + 4),
                (cx + r, cy - r // 2 + 4)], fill=PALETTE["ocean"])
    dr.text((cx, cy - 6), "!", font=sans_bold(28), fill=(255, 255, 255),
            anchor="ma")


def ribbon_art(dr, cx, cy, s):
    """A purple awareness ribbon: loop on top, crossed tails below."""
    pur = PALETTE["purple"]
    dr.ellipse([cx - s // 4, cy - s // 2, cx + s // 4, cy - 2],
               outline=pur, width=4)
    dr.polygon([(cx - s // 5, cy - 2), (cx + s // 5, cy - 2),
                (cx + s // 2, cy + s // 2), (cx + s // 8, cy + s // 2)],
               fill=pur)
    dr.polygon([(cx - s // 5, cy - 2), (cx + s // 5, cy - 2),
                (cx - s // 2, cy + s // 2), (cx - s // 8, cy + s // 2)],
               fill=pur)


def render_front_page():
    page = Image.new("RGB", (SIDE, SIDE), PALETTE["paper"])
    dr = ImageDraw.Draw(page)
    m = MARGIN

    # ---------- masthead ----------
    hline(dr, m, 30, SIDE - m, 3)
    dr.text((SIDE // 2, 44), "THE WORLD IN ONE PAGE",
            font=serif_bold(56), fill=PALETTE["ink"], anchor="mt")
    hline(dr, m, 116, SIDE - m, 2)
    dr.text((m, 126), "WEDNESDAY, 25 NOVEMBER 2026",
            font=sans_bold(19), fill=PALETTE["ink"])
    dr.text((SIDE - m, 126), "ONE DAY  ·  ONE PAGE",
            font=sans_bold(19), fill=PALETTE["ink"], anchor="rt")
    hline(dr, m, 154, SIDE - m, 3)

    # ---------- lead: Riyadh tower ----------
    ly = 168
    dr.text((m, ly), "YEMEN  ·  RIYADH, SAUDI ARABIA",
            font=sans_bold(16), fill=PALETTE["red"])
    dr.text((m, ly + 26), "RIYADH TOWER",
            font=serif_bold(66), fill=PALETTE["ink"])
    dr.text((m, ly + 100), "HIT AGAIN",
            font=serif_bold(66), fill=PALETTE["ink"])
    dr.text((m, ly + 178), "Drone strike wounds 11 in second attack in a week",
            font=serif(24), fill=PALETTE["ink"])
    lead_body = ("Houthi fighters strike the PIF Tower, the Saudi "
                 "capital's tallest building and home of the sovereign "
                 "wealth fund, for the second time in six days. The "
                 "Saudi-led coalition vows a decisive response.")
    draw_lines(dr, m, ly + 216, lead_body, sans(18), 560,
               PALETTE["ink"], 24)
    tower_art(dr, 700, ly + 20, 252, 250)
    dr.text((826, ly + 276), "The PIF Tower, hit on 19 Nov",
            font=sans(15), fill=PALETTE["grey"], anchor="mt")
    dr.text((826, ly + 296), "and again on 24 November.",
            font=sans(15), fill=PALETTE["grey"], anchor="mt")
    hline(dr, m, 508, SIDE - m, 2)

    # ---------- row 2: three stories ----------
    ry = 522
    stories = [
        (ship_art, "UKRAINE  ·  BALTIC & LIBYA",
         "Kyiv confirms ship strikes",
         "Ukraine hit a Russian ship in the Gulf of Finland and sank "
         "a warship off Libya."),
        (radar_art, "NATO  ·  POLAND",
         "AWACS jets to watch Poland",
         "NATO sends early-warning jets after missiles landed in "
         "Poland."),
        (tanker_art, "IRAN  ·  STRAIT OF HORMUZ",
         "Three tankers hit by mines",
         "Iran's Guard says three oil tankers were hit by mines in "
         "the Strait of Hormuz."),
    ]
    for idx, (art, kick, head, body) in enumerate(stories):
        cx = m + idx * 312
        after = card_title(dr, cx, ry, 300, kick, head, 25)
        art(dr, cx, after + 8, 300, 96)
        draw_lines(dr, cx, after + 116, body, sans(15), 300,
                   PALETTE["ink"], 20)
    hline(dr, m, 774, SIDE - m, 2)

    # ---------- row 3: three short stories ----------
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
    for idx, (kind, tx, kick, head, line1, line2) in enumerate(shorts):
        cx = m + idx * 312
        after = card_title(dr, cx, ry, 300, kick, head, 23)
        if kind == "drop":
            drop_art(dr, cx + 40, after + 40, 24)
        elif kind == "ribbon":
            ribbon_art(dr, cx + 40, after + 34, 52)
        else:
            globe_art(dr, cx + 40, after + 36, 26)
        dr.text((cx + tx, after + 10), line1, font=sans(16),
                fill=PALETTE["ink"])
        dr.text((cx + tx, after + 32), line2, font=sans(16),
                fill=PALETTE["ink"])
    hline(dr, m, 938, SIDE - m, 2)

    # ---------- ticker ----------
    ty = 946
    dr.text((m, ty), "ALSO ON 25 NOVEMBER",
            font=sans_bold(14), fill=PALETTE["red"])
    ticker = ("Sarkozy case to trial  ·  Trump pardons turkeys Freedom "
              "and Feathers  ·  England beat Australia in the 2nd T20I "
              " ·  BJP–Akali ally for Punjab 2027  ·  Fort Hood shooter "
              "seeks stay of execution")
    draw_lines(dr, m, ty + 22, ticker, sans(14), SIDE - 2 * m,
               PALETTE["ink"], 18)
    hline(dr, m, 1000, SIDE - m, 2)
    dr.text((SIDE // 2, 1006),
            "All stories as reported on Wednesday 25 November 2026",
            font=sans(12), fill=PALETTE["grey"], anchor="mt")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    render_front_page()
