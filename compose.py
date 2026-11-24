#!/usr/bin/env python3
"""Compose the 23 November 2026 front page (1024x1024): three generated
scene illustrations plus PIL-drawn headlines, text and captions.
Fresh build for news-image-20261123. Run: python3 compose.py
-> writes entry.png here. Deterministic: no network, no randomness,
no timestamps; the same input files always produce the same bytes.
"""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREEN = (27, 120, 55)
GREY = (90, 90, 88)
RULE = (60, 60, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, fnt, width):
    """Greedy word wrap: lines of `text` that fit in `width` pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_para(draw, x, y, width, text, fnt, fill=INK, leading=None):
    leading = leading or int(fnt.size * 1.35)
    for line in wrap_lines(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def cover(im, w, h):
    """Centre-crop an image to exactly w x h."""
    iw, ih = im.size
    s = max(w / iw, h / ih)
    im = im.resize((round(iw * s), round(ih * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    right = W - M

    # ---- Masthead ----
    d.text((W // 2, 18), "THE WORLD", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    d.line([(M, 96), (right, 96)], fill=RULE, width=2)
    d.text((W // 2, 104), "MONDAY, 23 NOVEMBER 2026  \u2022  ONE DAY IN PICTURES",
           font=font(SANS_B, 19), fill=INK, anchor="ma")
    d.line([(M, 134), (right, 134)], fill=RULE, width=2)

    # ---- Lead story: Huang is back, markets soar ----
    y = 148
    nv = Image.open(HERE / "assets" / "media-generation-nvidia-surge-0-b5cf84cd-544e-4d00-ba6c-3334bbb7c62c.webp").convert("RGB")
    img.paste(cover(nv, 512, 268), (484, y))
    d.text((484, y + 274), "Traders cheer on Wall Street as Nvidia shares surge.",
           font=font(SERIF, 13), fill=GREY)
    d.text((M, y), "HUANG", font=font(SERIF_B, 44), fill=RED)
    d.text((M, y + 48), "IS BACK", font=font(SERIF_B, 44), fill=RED)
    d.text((M, y + 96), "+31%", font=font(SERIF_B, 44), fill=GREEN)
    by = draw_para(d, M, y + 152, 440,
                   "Nvidia's board reinstated Jensen Huang as chief executive "
                   "on Monday, 11 days after he resigned amid scandal, and "
                   "shares soared 31%, adding about $950 billion in value.",
                   font(SANS, 16))
    draw_para(d, M, by + 6, 440,
              "The S&P 500 rose 4.7% and the Nasdaq 6.5% in one of the most "
              "extraordinary days in Wall Street history.",
              font(SANS, 16))

    # ---- Row 2: Merkury sunk off Libya + AWACS for Poland ----
    y2 = 470
    d.line([(M, y2 - 10), (right, y2 - 10)], fill=RULE, width=2)
    col_w = 474
    # left: warship sunk off Libya
    mk = Image.open(HERE / "assets" / "media-generation-merkury-benghazi-0-b5a94fd7-0f77-43c1-8d4a-3bb5f2a39e40.webp").convert("RGB")
    img.paste(cover(mk, col_w, 150), (M, y2))
    d.text((M, y2 + 158), "WARSHIP SUNK", font=font(SERIF_B, 24), fill=INK)
    d.text((M, y2 + 187), "OFF LIBYA", font=font(SERIF_B, 24), fill=INK)
    draw_para(d, M, y2 + 222, col_w,
              "Ukraine said seven sea drones sank the Russian corvette "
              "Merkury at Benghazi and hit the cargo ship MV Angara, "
              "destroying a Ka-27 helicopter.",
              font(SANS, 16), leading=20)
    # right: NATO AWACS for Poland
    aw = Image.open(HERE / "assets" / "media-generation-awacs-poland-0-a6c5d073-bfa9-4b5e-9224-5b9cf5ab357c.webp").convert("RGB")
    img.paste(cover(aw, col_w, 150), (522, y2))
    d.text((522, y2 + 158), "NATO WATCHES", font=font(SERIF_B, 24), fill=INK)
    d.text((522, y2 + 187), "OVER POLAND", font=font(SERIF_B, 24), fill=INK)
    draw_para(d, 522, y2 + 222, col_w,
              "NATO will send an AWACS early-warning aircraft to Poland "
              "after Russian missiles came down there on Friday, Warsaw "
              "said after an emergency allied meeting.",
              font(SANS, 16), leading=20)

    # ---- Row 3: Iran sanctions + Democrats' House win ----
    y3 = 770
    d.line([(M, y3 - 10), (right, y3 - 10)], fill=RULE, width=2)
    d.text((M, y3), "SANCTIONS HIT IRAN'S BANKS", font=font(SERIF_B, 21), fill=INK)
    draw_para(d, M, y3 + 30, col_w,
              "The US Treasury sanctioned more than two dozen Iranian "
              "exchange houses and front companies. Iran's courts awarded "
              "$290bn in damages against the US, and Tehran vowed to "
              "counter the blockade.",
              font(SANS, 15), leading=19)
    d.text((522, y3), "DEMOCRATS' BIGGEST WIN SINCE 1992", font=font(SERIF_B, 21), fill=INK)
    draw_para(d, 522, y3 + 30, col_w,
              "Democrats won at least 258 House seats, their largest "
              "majority since 1992, after flipping a North Carolina seat "
              "in the midterm count.",
              font(SANS, 15), leading=19)

    # ---- Briefs strip ----
    y4 = 906
    d.line([(M, y4 - 8), (right, y4 - 8)], fill=RULE, width=2)
    d.text((M, y4), "ALSO TODAY", font=font(SANS_B, 17), fill=RED)
    briefs = [
        "INDONESIA: Factory fire toll reaches 24; about 30 still missing in the Cikande ruins.",
        "SUDAN: Drones struck homes and a UN building in Khartoum, witnesses said.",
        "CHINA: Trump calls Putin \u2018my friend\u2019 after meeting him and Xi Jinping in Shenzhen.",
        "NEPAL: India pledges about \u20ac1.4bn to rebuild after a deadly glacier flood.",
        "YEMEN: Houthis and local officials trade blame for a deadly strike on buses in Lahj.",
    ]
    by = y4 + 24
    for b in briefs:
        d.text((M, by), "\u2022", font=font(SANS_B, 14), fill=RED)
        by = draw_para(d, M + 18, by, right - M - 18, b, font(SANS, 13), leading=14)
    d.text((W // 2, H - 16), "Sources: AP, Reuters, AFP, CNN, Al Jazeera  \u2022  All events 23 November 2026",
           font=font(SANS, 11), fill=GREY, anchor="ma")

    out = HERE / "entry.png"
    img.save(out, "PNG", optimize=True)
    print("saved", out, out.stat().st_size, "bytes", img.size)


if __name__ == "__main__":
    main()
