#!/usr/bin/env python3
"""0xPrivacy — BREAK THE DIGITAL CAGE

Night-vision attract: a halftone peace hand inside a visor, cage bars that
split, and the manifesto from 0xprivacy.online. Any key exits.

Stays at or below 12 FPS. This chassis cooks if the saver paints harder.
"""
from __future__ import annotations

import math
import os
import random
import select
import shutil
import sys
import termios
import time
import tty

RESET = "\033[0m"
HIDE = "\033[?25l"
SHOW = "\033[?25h"
ALT_ON = "\033[?1049h"
ALT_OFF = "\033[?1049l"
HOME = "\033[H"
CLEAR = "\033[2J"
SYNC_B = "\033[?2026h"
SYNC_E = "\033[?2026l"

NEON = (57, 255, 20)
ROSE = (255, 46, 99)
PALE = (199, 245, 206)
DIM = (46, 92, 58)
FOREST = (10, 72, 36)
BG = (2, 8, 4)

HAND = (
    "                 ▄▄██▄▄              ▄▄██▄▄                 ",
    "               ▄████████▄          ▄████████▄               ",
    "              ████▓▓▓▓████        ████▓▓▓▓████              ",
    "              ███▓▓▓▓▓▓███        ███▓▓▓▓▓▓███              ",
    "              ███▓▓▓▓▓▓███        ███▓▓▓▓▓▓███              ",
    "              ███▓▓▓▓▓▓███        ███▓▓▓▓▓▓███              ",
    "               ▀██▓▓▓▓██▀          ▀██▓▓▓▓██▀               ",
    "                 ▀█▓▓█▀              ▀█▓▓█▀                 ",
    "                   ██                  ██                   ",
    "                    ▀██▄            ▄██▀                    ",
    "                      ▀████████████▀                       ",
    "                       ▄██████████▄                        ",
    "                     ▄██████████████▄                      ",
    "                   ▄███▓▓▓▓▓▓▓▓▓▓███▄                      ",
    "                  ████▓▓▓▓▓▓▓▓▓▓▓▓████                     ",
    "                 ███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████                    ",
    "                 ███▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████                   ",
    "                  ▀███▓▓▓▓▓▓▓▓▓▓▓▓███▀                    ",
    "                    ▀██████████████▀                      ",
    "                      ▀████████████▀                       ",
    "                        ▀████████▀                         ",
)

LINES = (
    "YOUR KEYS. YOUR DATA. YOUR FREEDOM.",
    "BREAK THE DIGITAL CAGE",
    "NO TRACKERS. NO KYC. NO EXCEPTIONS.",
    "TOR   MONERO   NOSTR   SIMPLEX   TAILS   NYM   IPFS",
    "WE ARE DONE BEING WATCHED.",
)
GLYPHS = "01"


def key_waiting() -> bool:
    return bool(select.select([sys.stdin], [], [], 0)[0])


def fg(rgb: tuple[int, int, int]) -> str:
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


def bg(rgb: tuple[int, int, int]) -> str:
    return f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


def q(rgb: tuple[int, int, int], step: int = 32) -> tuple[int, int, int]:
    return (rgb[0] - rgb[0] % step, rgb[1] - rgb[1] % step, rgb[2] - rgb[2] % step)


FPS = min(12.0, float(os.environ.get("OMARCHY_SAVER_FPS", "12") or 12))


class CageBreak:
    def __init__(self) -> None:
        self.w = 0
        self.h = 0
        self.t = 0.0
        self.tick = 0
        self.rng = random.Random(0x0A71)
        self.line_i = 0
        self.line_age = 0.0
        self.scroll = 0.0
        self.rain: list[dict] = []
        self._wash: list[tuple[int, int, int]] = []

    def resize(self, w: int, h: int) -> None:
        w, h = max(80, w), max(24, h)
        if w == self.w and h == self.h:
            return
        self.w, self.h = w, h
        self._wash = []
        cy = (h - 1) / 2
        for y in range(h):
            ny = abs(y - cy) / max(1.0, cy)
            self._wash.append(q((int(2 + 8 * (1 - ny)), int(8 + 22 * (1 - ny * 0.35)), int(4 + 8 * (1 - ny)))))
        self.rain = []
        for x in range(8, w - 8, 3):
            if self.rng.random() > 0.55:
                continue
            self.rain.append(
                {
                    "x": x,
                    "y": self.rng.uniform(-h, h),
                    "speed": self.rng.uniform(6, 16),
                    "length": self.rng.randint(4, 10),
                    "seed": self.rng.randrange(1 << 20),
                }
            )

    def step(self, dt: float) -> None:
        self.t += dt
        self.tick += 1
        self.scroll = (self.scroll + dt * 8) % 80
        self.line_age += dt
        if self.line_age > 3.4:
            self.line_age = 0.0
            self.line_i = (self.line_i + 1) % len(LINES)
        for col in self.rain:
            col["y"] += col["speed"] * dt
            if col["y"] - col["length"] > self.h:
                col["y"] = -col["length"]
                col["seed"] = self.rng.randrange(1 << 20)

    def _inside_visor(self, x: int, y: int) -> float:
        cx, cy = (self.w - 1) / 2, (self.h - 1) * 0.46
        rx, ry = self.w * 0.34, self.h * 0.38
        nx = (x - cx) / max(1.0, rx)
        ny = (y - cy) / max(1.0, ry)
        return nx * nx + ny * ny

    def paint(self) -> str:
        w, h = self.w, self.h
        cells = [[" "] * w for _ in range(h)]
        ink: list[tuple[int, int, int]] = [DIM] * (w * h)
        back: list[tuple[int, int, int]] = [BG] * (w * h)

        def put(x: int, y: int, ch: str, color: tuple[int, int, int], wash: tuple[int, int, int] | None = None) -> None:
            if 0 <= x < w and 0 <= y < h and ch:
                cells[y][x] = ch
                ink[y * w + x] = color
                if wash is not None:
                    back[y * w + x] = wash

        for y in range(h):
            wash = self._wash[y]
            row = y * w
            for x in range(w):
                back[row + x] = wash

        for y in range(h):
            for x in range(w):
                dist = self._inside_visor(x, y)
                if dist < 0.86:
                    back[y * w + x] = (4, 16, 8) if y % 2 else (2, 12, 6)
                elif 0.86 <= dist <= 1.05:
                    mark = ROSE if abs(x - w / 2) < 2 and y < h * 0.22 else NEON
                    put(x, y, "•" if dist > 0.96 else "·", mark)

        for col in self.rain:
            x = col["x"]
            seed = col["seed"]
            for i in range(col["length"]):
                y = int(col["y"]) - i
                if not (0 <= y < h) or self._inside_visor(x, y) > 0.8:
                    continue
                put(x, y, GLYPHS[(seed + i) & 1], PALE if i == 0 else FOREST)

        gap = 3 + int(2.5 * (1 + math.sin(self.t * 0.7)))
        cy = int(h * 0.46)
        for x in (3, 7, 11, w - 4, w - 8, w - 12):
            if not (0 <= x < w):
                continue
            for y in range(2, h - 2):
                if abs(y - cy) <= gap:
                    if abs(y - cy) == gap:
                        put(x, y, "━", ROSE)
                    continue
                put(x, y, "│", DIM if y % 2 else FOREST)

        split = int(4 + 6 * (0.5 + 0.5 * math.sin(self.t * 0.9)))
        chain_y = max(2, int(h * 0.16))
        left, right = "════○", "○════"
        origin = w // 2 - split - len(left)
        for i, ch in enumerate(left):
            put(origin + i, chain_y, ch, ROSE if ch == "○" else NEON)
        for i, ch in enumerate(right):
            put(w // 2 + split + i, chain_y, ch, ROSE if ch == "○" else NEON)
        if split > 6 and (self.tick // 3) % 2 == 0:
            put(w // 2, chain_y, "×", ROSE)

        rise = int(math.sin(self.t * 0.6) * 1.5)
        hand_y = max(3, (h - len(HAND)) // 2 + 1 + rise)
        hand_x = max(0, (w - len(HAND[0])) // 2)
        phase = self.tick // 2
        for j, line in enumerate(HAND):
            y = hand_y + j
            if not (0 <= y < h - 2):
                continue
            for i, ch in enumerate(line):
                if ch == " ":
                    continue
                x = hand_x + i
                if ch == "▓":
                    put(x, y, "▓" if (i + j + phase) % 3 else "░", NEON, (6, 28, 10))
                else:
                    put(x, y, ch, PALE if (i + j) % 11 else NEON)

        title = "0xPRIVACY"
        tx = (w - len(title)) // 2
        ty = max(1, hand_y - 2)
        for i, ch in enumerate(title):
            put(tx + i, ty, ch, ROSE if i < 2 else NEON)

        line = LINES[self.line_i]
        ly = min(h - 3, hand_y + len(HAND) + 1)
        lx = max(1, (w - len(line)) // 2)
        color = ROSE if "BREAK" in line or "DONE" in line else PALE
        for i, ch in enumerate(line):
            put(lx + i, ly, ch, color)

        footer = "ANY KEY EXITS   ·   0xPRIVACY.ONLINE   ·   BREAK THE DIGITAL CAGE"
        arsenal = "  TOR * MONERO * NOSTR * SIMPLEX * SIGNAL * TAILS * NYM * IPFS * WHONIX *  "
        start = int(self.scroll) % len(arsenal)
        band = (arsenal + arsenal)[start : start + max(0, w - 4)]
        for i, ch in enumerate(band):
            put(2 + i, h - 1, ch, ROSE if ch == "*" else DIM)
        for i, ch in enumerate(footer[: max(0, w - 2)]):
            put(1 + i, h - 2, ch, DIM)

        out = [SYNC_B, HOME]
        for y in range(h):
            prev_f = prev_b = None
            parts: list[str] = []
            row = y * w
            for x in range(w):
                color = ink[row + x]
                wash = back[row + x]
                if color != prev_f:
                    parts.append(fg(color))
                    prev_f = color
                if wash != prev_b:
                    parts.append(bg(wash))
                    prev_b = wash
                parts.append(cells[y][x])
            parts.append(RESET)
            if y < h - 1:
                parts.append("\n")
            out.append("".join(parts))
        out.append(SYNC_E)
        return "".join(out)


def main() -> int:
    cols = int(os.environ.get("COLUMNS") or 0)
    rows = int(os.environ.get("LINES") or 0)
    try:
        size = shutil.get_terminal_size(fallback=(cols or 160, rows or 42))
        cols, rows = size.columns, size.lines
    except Exception:
        cols, rows = cols or 160, rows or 42

    scene = CageBreak()
    scene.resize(cols, rows)
    fd = sys.stdin.fileno()
    old = None
    is_tty = sys.stdin.isatty()
    if is_tty:
        old = termios.tcgetattr(fd)
        tty.setcbreak(fd)
    sys.stdout.write(ALT_ON + HIDE + CLEAR + HOME + bg(BG))
    sys.stdout.flush()
    try:
        target = 1.0 / max(6.0, FPS)
        last = time.perf_counter()
        while True:
            if is_tty and key_waiting():
                while key_waiting():
                    os.read(fd, 64)
                break
            now = time.perf_counter()
            dt = min(0.12, now - last)
            last = now
            scene.step(dt)
            sys.stdout.write(scene.paint())
            sys.stdout.flush()
            wait = target - (time.perf_counter() - now)
            if wait > 0.004:
                if is_tty and select.select([sys.stdin], [], [], wait)[0]:
                    os.read(fd, 64)
                    break
                if not is_tty:
                    time.sleep(wait)
    finally:
        if old is not None:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        sys.stdout.write(SHOW + RESET + ALT_OFF + CLEAR)
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
