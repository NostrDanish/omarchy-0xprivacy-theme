#!/usr/bin/env python3
"""Centered 0x / PRIVACY lockup for the 1920 crop of a 2560 wallpaper.

Rose is only the 0x. PRIVACY is phosphor. Does not touch 0xhermes.png.
"""
from __future__ import annotations

import os

import cairo

W, H = 2560, 1080
ROSE = (255 / 255, 46 / 255, 99 / 255)
GREEN = (0 / 255, 255 / 255, 65 / 255)
PALE = (232 / 255, 255 / 255, 236 / 255)
DISPLAY = "Noto Sans Black"
MONO = "JetBrainsMono Nerd Font"


def rgb(cr, color, alpha=1.0):
    cr.set_source_rgba(*color, alpha)


def font(cr, family, size):
    cr.select_font_face(family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)


def width(cr, text):
    return cr.text_extents(text).x_advance


def render(path: str) -> None:
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surface)
    cr.set_antialias(cairo.ANTIALIAS_BEST)
    cr.set_source_rgb(0, 0, 0)
    cr.paint()

    bloom = cairo.RadialGradient(1280, 520, 40, 1280, 520, 720)
    bloom.add_color_stop_rgba(0, 0.02, 0.12, 0.04, 1)
    bloom.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(bloom)
    cr.paint()

    # Scan only inside the bloom, not a matrix rain.
    rgb(cr, GREEN, 0.035)
    cr.set_line_width(1)
    y = 180
    while y < 900:
        cr.move_to(520, y)
        cr.line_to(2040, y)
        y += 4
    cr.stroke()

    font(cr, DISPLAY, 210)
    prefix = "0x"
    name = "PRIVACY"
    gap = 28
    total = width(cr, prefix) + gap + width(cr, name)
    x = 1280 - total / 2
    baseline = 560
    rgb(cr, ROSE, 1)
    cr.move_to(x, baseline)
    cr.show_text(prefix)
    name_x = x + width(cr, prefix) + gap
    rgb(cr, GREEN, 1)
    cr.move_to(name_x, baseline)
    cr.show_text(name)

    name_w = width(cr, name)
    rgb(cr, ROSE, 0.9)
    cr.set_line_width(3)
    cr.move_to(name_x, baseline + 22)
    cr.line_to(name_x + name_w, baseline + 22)
    cr.stroke()

    font(cr, MONO, 22)
    line = "NO LOGS   ·   NO TRACE   ·   NO NAME"
    rgb(cr, PALE, 0.55)
    cr.move_to(1280 - width(cr, line) / 2, baseline + 78)
    cr.show_text(line)

    font(cr, MONO, 16)
    rgb(cr, GREEN, 0.35)
    cr.move_to(420, H - 48)
    cr.show_text("0xprivacy.sys")
    rgb(cr, ROSE, 0.45)
    label = "node online"
    cr.move_to(2140 - width(cr, label), H - 48)
    cr.show_text(label)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    surface.write_to_png(path)


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(root, "backgrounds", "00-lockup.png")
    render(out)
    print(out)
