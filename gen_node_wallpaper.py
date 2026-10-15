#!/usr/bin/env python3
"""0xPrivacy node wallpaper.

Black field, mint type, amber index, one violet glitch.
Not the Hermes mascot and not a photo plate.
Does not write or delete 0xhermes.png.
"""
from __future__ import annotations

import os

import cairo

W, H = 2560, 1080
MINT = (0 / 255, 244 / 255, 142 / 255)
AMBER = (255 / 255, 159 / 255, 0 / 255)
VIOLET = (191 / 255, 90 / 255, 242 / 255)
INK = (0, 0, 0)
PALE = (239 / 255, 251 / 255, 245 / 255)
DISPLAY = "Noto Sans Black"
MONO = "JetBrainsMono Nerd Font"


def rgb(cr: cairo.Context, color, alpha: float = 1.0) -> None:
    cr.set_source_rgba(*color, alpha)


def font(cr: cairo.Context, family: str, size: float) -> None:
    cr.select_font_face(family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)


def width(cr: cairo.Context, text: str) -> float:
    return cr.text_extents(text).x_advance


def glitch(cr: cairo.Context, text: str, x: float, y: float, size: float) -> None:
    font(cr, DISPLAY, size)
    text_w = width(cr, text)
    rgb(cr, VIOLET, 0.28)
    cr.move_to(x - 3, y)
    cr.show_text(text)
    rgb(cr, AMBER, 0.22)
    cr.move_to(x + 3, y)
    cr.show_text(text)
    rgb(cr, MINT, 1)
    cr.move_to(x, y)
    cr.show_text(text)
    for band_y, shift in ((y - size * 0.70, 10), (y - size * 0.34, -8)):
        cr.save()
        cr.rectangle(x - 12, band_y, text_w + 24, size * 0.08)
        cr.clip()
        rgb(cr, MINT, 1)
        cr.move_to(x + shift, y)
        cr.show_text(text)
        cr.restore()


def render(path: str) -> None:
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surface)
    cr.set_antialias(cairo.ANTIALIAS_BEST)
    rgb(cr, INK)
    cr.paint()

    rgb(cr, MINT, 0.85)
    cr.set_line_width(2)
    cr.move_to(96, 150)
    cr.line_to(96, H - 150)
    cr.stroke()

    font(cr, MONO, 22)
    rgb(cr, AMBER, 0.95)
    cr.move_to(128, 196)
    cr.show_text("[00]")
    rgb(cr, MINT, 0.55)
    cr.move_to(210, 196)
    cr.show_text("// node online")

    glitch(cr, "DIGITAL", 128, 470, 168)
    glitch(cr, "CAGE", 128, 650, 168)

    font(cr, MONO, 26)
    rgb(cr, PALE, 0.82)
    cr.move_to(132, 730)
    cr.show_text("$ your keys. your data. your freedom.")

    font(cr, MONO, 20)
    checks = (
        "NIP-01   ok",
        "NIP-44   ok",
        "schnorr  ok",
        "no kyc   ok",
        "ipfs     ok",
    )
    font(cr, MONO, 18)
    rgb(cr, AMBER, 0.8)
    cr.move_to(W - 420, 220)
    cr.show_text("system active")
    y = 280
    for line in checks:
        rgb(cr, MINT, 0.55)
        cr.move_to(W - 420, y)
        cr.show_text(line)
        y += 36

    font(cr, MONO, 18)
    ticker = "tor   ·   monero   ·   nostr   ·   simplex   ·   tails   ·   mullvad   ·   ipfs   ·   whonix   ·   cashu   ·   sip-01"
    rgb(cr, MINT, 0.32)
    cr.move_to(132, H - 78)
    cr.show_text(ticker)

    font(cr, MONO, 16)
    rgb(cr, MINT, 0.35)
    cr.move_to(W - 280, H - 42)
    cr.show_text("0xprivacy.sys")

    os.makedirs(os.path.dirname(path), exist_ok=True)
    surface.write_to_png(path)


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(root, "backgrounds", "00-node.png")
    render(out)
    preview = cairo.ImageSurface(cairo.FORMAT_ARGB32, 2560, 1440)
    pcr = cairo.Context(preview)
    pcr.set_source_rgb(0, 0, 0)
    pcr.paint()
    plate = cairo.ImageSurface.create_from_png(out)
    pcr.set_source_surface(plate, 0, (1440 - H) / 2)
    pcr.paint()
    preview.write_to_png(os.path.join(root, "preview.png"))
    print(out)
