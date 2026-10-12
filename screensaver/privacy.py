#!/usr/bin/env python3
"""0xPrivacy — HACKER ATTRACT

0xPrivacy hacker attract mode: black field, neon green matrix,
glitch tears, skull mark, terminal chatter. Fills 2560x1080. Any key exits.
"""

from __future__ import annotations

import math
import os
import random
import select
import shutil
import socket
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

# 0xPrivacy / Hacker Vibes palette
YEL = (57, 255, 20)      # neon green primary
CYAN = (0, 255, 65)      # matrix green
PINK = (255, 51, 51)     # alert red glitch
WHITE = (200, 255, 200)
DIMW = (0, 80, 20)
BG_RGB = (10, 10, 10)

LOGO = [
    "   #####   #   #  #####   #####    ###   #     #     #      #####   #     #  ",
    "  #     #   # #   #    #  #    #    #    #     #    # #    #     #   #   #   ",
    "  #     #    #    #    #  #    #    #    #     #   #   #   #          # #    ",
    "  #     #   # #   #####   #####     #    #     #  #     #  #           #     ",
    "  #     #  #   #  #       #   #     #     #   #   #######  #           #     ",
    "  #     #         #       #    #    #      # #    #     #  #     #     #     ",
    "   #####          #       #    #   ###      #     #     #   #####      #     ",
]

# 0xPrivacy skull mark (ASCII attract logo) — each row width 30
MASK = [
    "      ##################      ",
    "   ########################   ",
    "  ##########################  ",
    " ####    ####    ####    #### ",
    " ###  ########  ########  ### ",
    " ###  ########  ########  ### ",
    " ####    ####    ####    #### ",
    "  ####                  ####  ",
    "   ####      ##      ####     ",
    "    #####  ######  #####      ",
    "     #### ## ## ## ####       ",
    "      ###  ##  ##  ###        ",
    "       ## ###  ### ##         ",
    "        ## ##  ## ##          ",
    "         ##      ##           ",
]

STATUS = (
    "mesh // ENCRYPTED",
    "tor circuits: hot",
    "0xprivacy online",
    "we own the night",
    "dead drops live",
    "follow the rabbit",
    "operate // ghost",
    "profiler: null",
    "cameras: spoofed",
    "exfil channel ready",
)

CHATTER = (
    "> probe mesh.gateway ... ACK",
    "> dump /var/keys ... 0xPRIV",
    "> spoof profiler.id = null",
    "> inject dead_drop://loop",
    "> camera.grid[12..48] owned",
    "> traffic.lights = chaos",
    "> broadcast 0xprivacy://invite",
    "> encrypt tunnel // onion",
    "> wipe logs --force",
    "> ping privacy.mesh ... LIVE",
    "> unlock ghost.exe",
    "> shadow mode: engaged",
)

GLYPHS = "01ABCDEF#@$%&*"
TAGS = (
    "WE OWN THE NIGHT",
    "FOLLOW THE RABBIT",
    "PRIVACY IS A RIGHT",
    "OPERATE // 0xPRIVACY",
    "STAY GHOST",
    "BREACH THE SYSTEM",
)


def key_waiting() -> bool:
    return bool(select.select([sys.stdin], [], [], 0)[0])


def fg(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{int(r)};{int(g)};{int(b)}m"


def bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{int(r)};{int(g)};{int(b)}m"


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
    )


def q(c: tuple[int, int, int], step: int = 32) -> tuple[int, int, int]:
    """Snap RGB so ANSI runs collapse (less CPU in Python + foot)."""
    return (c[0] - c[0] % step, c[1] - c[1] % step, c[2] - c[2] % step)


FPS = float(os.environ.get("OMARCHY_SAVER_FPS", "12"))


class PrivacyAttract:
    def __init__(self) -> None:
        self.w = 0
        self.h = 0
        self.t = 0.0
        self.tick = 0
        self.rng = random.Random(0x0A71AC)
        self.columns: list[dict] = []
        self.glitch_rows: list[dict] = []
        self.chatter: list[dict] = []
        self._typed = 0
        self._tag = TAGS[0]
        self._status_i = 0
        self._status_age = 0.0
        self._host = socket.gethostname().split(".")[0][:16]
        self._scan = 0.0
        self._rgb_split = 0.0
        self._flash = 0.0
        self._mask_pulse = 0.0
        self.skyline: list[int] = []
        self.sparks: list[dict] = []
        self._bg: list[list[tuple[int, int, int]]] = []
        self._cells: list[list[tuple[str, tuple[int, int, int], tuple[int, int, int]]]] = []

    def resize(self, w: int, h: int) -> None:
        w = max(60, w)
        h = max(20, h)
        if w == self.w and h == self.h:
            return
        self.w, self.h = w, h
        # Full-field rain: dense edges, lighter center (mask stays readable)
        self.columns = []
        for x in range(w):
            cx = abs(x - w * 0.5) / (w * 0.5)
            # density rises toward edges; always some mid rain
            if self.rng.random() > (0.14 + 0.42 * cx):
                continue
            layer = self.rng.choice((0, 0, 1, 1, 2))  # parallax depth
            self.columns.append(
                {
                    "x": x,
                    "y": self.rng.uniform(-h, h),
                    "speed": (0.2, 0.55, 1.15)[layer] * self.rng.uniform(0.7, 1.3),
                    "length": (6, 12, 20)[layer] + self.rng.randint(0, 6),
                    "seed": self.rng.randrange(1 << 30),
                    "tone": self.rng.choice(("y", "y", "c", "c", "d", "d")),
                    "layer": layer,
                }
            )
        # City skyline heights across bottom
        self.skyline = []
        hgt = self.rng.randint(3, 8)
        for x in range(w):
            if self.rng.random() < 0.08:
                hgt = self.rng.randint(2, max(3, h // 5))
            elif self.rng.random() < 0.2:
                hgt = max(2, hgt + self.rng.choice((-1, 0, 1)))
            self.skyline.append(hgt)
        self.sparks = []
        self.glitch_rows = []
        self.chatter = []
        for i in range(min(5, h // 8)):
            self.chatter.append(
                {
                    "text": self.rng.choice(CHATTER),
                    "y": 2 + i * 2,
                    "x": self.rng.randint(2, max(2, w // 5)),
                    "age": self.rng.uniform(0, 3),
                    "life": self.rng.uniform(2.5, 5.0),
                }
            )
        self._rebuild_static()

    def _rebuild_static(self) -> None:
        """Vignette / CRT wash once per resize — not per frame."""
        w, h = self.w, self.h
        cx0, cy0 = (w - 1) * 0.5, (h - 1) * 0.5
        bg: list[list[tuple[int, int, int]]] = []
        cells: list[list[tuple[str, tuple[int, int, int], tuple[int, int, int]]]] = []
        for y in range(h):
            depth = y / max(1, h - 1)
            base = mix(BG_RGB, (8, 18, 8), 0.35 * depth)
            base = mix(base, (4, 20, 10), 0.14 * (1.0 - depth))
            if y % 2 == 0:
                base = mix(base, (0, 0, 0), 0.22)
            row_bg: list[tuple[int, int, int]] = []
            row_cells: list[tuple[str, tuple[int, int, int], tuple[int, int, int]]] = []
            for x in range(w):
                nx = (x - cx0) / max(1.0, cx0)
                ny = (y - cy0) / max(1.0, cy0)
                vig = min(1.0, (nx * nx + ny * ny) * 0.55)
                wash = q(mix(base, (0, 0, 0), 0.45 * vig))
                row_bg.append(wash)
                row_cells.append((" ", DIMW, wash))
            bg.append(row_bg)
            cells.append(row_cells)
        self._bg = bg
        self._cells = cells

    def _tone_color(self, tone: str, bright: float) -> tuple[int, int, int]:
        if tone == "y":
            base = YEL
        elif tone == "c":
            base = CYAN
        else:
            base = DIMW
        return q(mix(BG_RGB, base, 0.2 + 0.8 * bright))

    def paint(self) -> str:
        w, h = self.w, self.h
        cells = self._cells
        wash = self._bg
        # Reset from cached wash — no per-frame hypot/vignette.
        for y in range(h):
            brow = wash[y]
            row = cells[y]
            for x in range(w):
                row[x] = (" ", DIMW, brow[x])

        # Scanline: one cheap band instead of mixing every cell
        scan_y = int((self._scan % 1.0) * h)
        for y in range(max(0, scan_y - 1), min(h, scan_y + 2)):
            row = cells[y]
            for x in range(w):
                ch, f, b = row[x]
                row[x] = (ch, f, q(mix(b, YEL, 0.08)))

        # Perspective city grid (floor rushing toward horizon)
        horizon = int(h * 0.62)
        for y in range(horizon, h - 2):
            t = (y - horizon) / max(1, h - horizon - 2)
            # vanishing-point verticals
            spacing = max(2, int(lerp(28, 4, t)))
            mid = w // 2
            # horizontal road lines
            if int((y + int(self.t * 18)) % max(2, int(lerp(10, 2, t)))) == 0:
                for x in range(w):
                    ch, f, b = cells[y][x]
                    cells[y][x] = (ch, f, mix(b, CYAN, 0.08 + 0.12 * t))
            for k in range(-40, 41):
                x = mid + k * spacing
                if 0 <= x < w:
                    ch, f, b = cells[y][x]
                    if ch in (" ", ".", ":", "/"):
                        cells[y][x] = ("|", mix(BG_RGB, CYAN, 0.15 + 0.35 * t), b)

        # Skyline silhouette with window blinks
        if self.skyline:
            for x, bh in enumerate(self.skyline[:w]):
                for dy in range(bh):
                    y = h - 3 - dy
                    if y < 0:
                        continue
                    win = ((x * 19 + dy * 7 + self.tick // 12) % 11) == 0
                    if dy == bh - 1:
                        cells[y][x] = ("^", mix(BG_RGB, YEL, 0.35), mix(BG_RGB, (10, 22, 10), 0.5))
                    elif win:
                        glow = YEL if (x + dy + self.tick // 20) % 5 else CYAN
                        cells[y][x] = ("+", mix(BG_RGB, glow, 0.55), mix(BG_RGB, glow, 0.12))
                    else:
                        cells[y][x] = ("#", mix(BG_RGB, DIMW, 0.55), mix(BG_RGB, (16, 16, 18), 0.7))

        # Far + mid + near glyph rain (parallax)
        for col in self.columns:
            x = col["x"]
            if x >= w:
                continue
            layer = col.get("layer", 1)
            head = col["y"]
            dim_mid = 0.55 if (w * 0.32 < x < w * 0.68) else 1.0
            for i in range(col["length"]):
                y = int(head - i)
                if 0 <= y < h - 3:
                    bright = max(0.08, 1.0 - i / col["length"]) * dim_mid
                    if layer == 0:
                        bright *= 0.35
                    elif layer == 2:
                        bright = min(1.0, bright * 1.15)
                    if i == 0:
                        bright = min(1.0, bright + 0.25)
                    ch = GLYPHS[(col["seed"] + self.tick + i * 7) % len(GLYPHS)]
                    c = self._tone_color(col["tone"], bright)
                    if i == 0 and layer >= 1:
                        c = WHITE if col["tone"] == "y" else CYAN
                    old_ch, _, b = cells[y][x]
                    # don't stomp skyline solids too hard
                    if old_ch == "#" and y > h - 12:
                        continue
                    cells[y][x] = (ch, c, b)

        # Floating sparks / packet blips
        for s in self.sparks:
            x, y = int(s["x"]), int(s["y"])
            if 0 <= x < w and 0 <= y < h:
                cells[y][x] = ("*", mix(BG_RGB, s["color"], s["life"]), cells[y][x][2])
                if 0 <= x + 1 < w:
                    cells[y][x + 1] = ("-", mix(BG_RGB, s["color"], s["life"] * 0.5), cells[y][x + 1][2])

        # Network nodes + pulsing links (brighter)
        step_x = max(6, w // 26)
        step_y = max(3, h // 14)
        for y in range(2, horizon, step_y):
            for x in range(2, w - 2, step_x):
                pulse = 0.35 + 0.65 * abs(math.sin(self.t * 1.6 + x * 0.05 + y * 0.1))
                if pulse < 0.45:
                    continue
                ch, f, b = cells[y][x]
                if ch in (" ", ".", ":", "/"):
                    cells[y][x] = ("+", mix(BG_RGB, CYAN, 0.5 * pulse), mix(b, CYAN, 0.08 * pulse))

        for y in range(3, horizon, step_y):
            phase = (self.t * 70 + y * 7) % (w + 60) - 30
            for dx in range(18):
                x = int(phase + dx)
                if 0 <= x < w:
                    ch, f, b = cells[y][x]
                    if ch in (" ", ".", ":", "/", "+", "|"):
                        cells[y][x] = ("=", mix(BG_RGB, CYAN, 0.6 - dx * 0.03), b)

        # Terminal chatter (left column)
        for c in self.chatter:
            y = int(c["y"])
            if not (0 <= y < h - 3):
                continue
            fade = min(1.0, c["life"] / 1.2)
            text = c["text"]
            for i, ch in enumerate(text):
                xx = int(c["x"]) + i
                if 0 <= xx < w // 3:
                    cells[y][xx] = (ch, mix(BG_RGB, CYAN, 0.35 + 0.55 * fade), cells[y][xx][2])

        # 0xPrivacy skull — center stage
        mask_w = len(MASK[0])
        mask_h = len(MASK)
        mx = max(0, (w - mask_w) // 2)
        my = max(1, h // 2 - mask_h // 2 - 4)
        pulse = 0.72 + 0.28 * abs(math.sin(self.t * 2.2))
        if self._flash > 0:
            pulse = 1.0
        for j, line in enumerate(MASK):
            yy = my + j
            if yy >= h:
                break
            for i, ch in enumerate(line):
                xx = mx + i
                if xx < w and ch != " ":
                    # hollow eyes / nose stay empty (spaces in art)
                    col = mix(BG_RGB, YEL, pulse)
                    # jaw a touch dimmer
                    if j >= mask_h - 3:
                        col = mix(BG_RGB, YEL, pulse * 0.85)
                    if self._rgb_split > 0 and ((i + j + self.tick) % 7) == 0:
                        cells[yy][min(w - 1, xx + 1)] = (ch, PINK, BG_RGB)
                        cells[yy][max(0, xx - 1)] = (ch, CYAN, BG_RGB)
                    cells[yy][xx] = (ch, col, mix(BG_RGB, YEL, 0.12 * pulse))

        # LOGO wordmark above mask
        logo_y = max(1, my - len(LOGO) - 1)
        logo_x = max(0, (w - len(LOGO[0])) // 2)
        for j, line in enumerate(LOGO):
            yy = logo_y + j
            if yy >= h or yy < 0:
                continue
            for i, ch in enumerate(line):
                xx = logo_x + i
                if 0 <= xx < w and ch != " ":
                    if self._rgb_split > 0 and j == int(self.t * 10) % len(LOGO):
                        cells[yy][min(w - 1, xx + 1)] = (ch, PINK, BG_RGB)
                        cells[yy][max(0, xx - 1)] = (ch, CYAN, BG_RGB)
                    cells[yy][xx] = (ch, YEL, mix(BG_RGB, YEL, 0.07))

        # Typewriter tagline under mask
        tag_y = my + mask_h + 1
        typed = self._tag[: self._typed]
        tag_x = max(0, (w - len(self._tag)) // 2)
        if 0 <= tag_y < h:
            for i, ch in enumerate(typed):
                xx = tag_x + i
                if 0 <= xx < w:
                    cells[tag_y][xx] = (ch, WHITE, BG_RGB)
            cx = tag_x + len(typed)
            if cx < w and (self.tick // 7) % 2 == 0:
                cells[tag_y][cx] = ("#", YEL, BG_RGB)

        # Invite strip
        invite = "[ PRESS ANY KEY // 0xPRIVACY ]"
        iy = tag_y + 2
        ix = max(0, (w - len(invite)) // 2)
        if 0 <= iy < h and (int(self.t * 2) % 2 == 0 or self._flash > 0):
            for i, ch in enumerate(invite):
                xx = ix + i
                if 0 <= xx < w:
                    cells[iy][xx] = (ch, mix(BG_RGB, YEL, 0.85), mix(BG_RGB, YEL, 0.08))

        # Status bar
        status = STATUS[self._status_i]
        meta = f"{self._host} | 0xprivacy | {status} | mesh:LIVE"
        by = h - 2
        bx = max(0, (w - len(meta)) // 2)
        if by > 0:
            for i, ch in enumerate(meta):
                xx = bx + i
                if 0 <= xx < w:
                    col = DIMW
                    if "0xprivacy" in meta[max(0, i - 8) : i + 1]:
                        col = YEL
                    elif "LIVE" in meta[max(0, i - 3) : i + 1]:
                        col = CYAN
                    cells[by][xx] = (ch, col, mix(BG_RGB, YEL, 0.06))

        # Top HUD
        hud = f"0xPRIVACY // HACKER ATTRACT  t={self.t:06.1f}  fps~{int(FPS)}"
        for i, ch in enumerate(hud[: w - 4]):
            cells[0][2 + i] = (ch, mix(BG_RGB, DIMW, 0.7), mix(BG_RGB, YEL, 0.04))

        # Pink glitch tear rows (chromatic shift)
        for g in self.glitch_rows:
            y = g["y"]
            if not (0 <= y < h):
                continue
            shift = g["shift"]
            for x in range(w):
                src = (x - shift) % w
                ch, f, b = cells[y][src]
                cells[y][x] = (ch, mix(f, PINK, 0.7), mix(b, PINK, 0.18))

        # Side accent bars — green / alert red stripe
        for y in range(h):
            cells[y][0] = ("|", CYAN, BG_RGB)
            cells[y][1] = ("|", mix(BG_RGB, CYAN, 0.5), BG_RGB)
            cells[y][w - 1] = ("|", PINK, BG_RGB)
            cells[y][w - 2] = ("|", mix(BG_RGB, PINK, 0.5), BG_RGB)

        # Invite pulse is logo-only — skip full-frame mix (was O(w*h) every flash)

        out = [SYNC_B, HOME]
        for y in range(h):
            prev_f = None
            prev_b = None
            parts: list[str] = []
            for x in range(w):
                ch, f, b = cells[y][x]
                f = q(f)
                b = q(b)
                if f != prev_f:
                    parts.append(fg(*f))
                    prev_f = f
                if b != prev_b:
                    parts.append(bg(*b))
                    prev_b = b
                parts.append(ch)
            parts.append(RESET)
            if y < h - 1:
                parts.append("\n")
            out.append("".join(parts))
        out.append(SYNC_E)
        return "".join(out)

    def step(self, dt: float) -> None:
        self.t += dt
        self.tick += 1
        self._scan = (self._scan + dt * 0.28) % 1.0
        if self._rgb_split > 0:
            self._rgb_split = max(0.0, self._rgb_split - dt * 3)
        if self._flash > 0:
            self._flash = max(0.0, self._flash - dt * 2.5)

        for col in self.columns:
            col["y"] += col["speed"] * (dt * 34)
            if col["y"] - col["length"] > self.h:
                col["y"] = -col["length"]
                col["seed"] = self.rng.randrange(1 << 30)
                col["tone"] = self.rng.choice(("y", "y", "c", "c", "d"))

        # Packet sparks drifting across the field
        for s in self.sparks:
            s["x"] += s["vx"] * dt
            s["y"] += s["vy"] * dt
            s["life"] -= dt * 0.8
        self.sparks = [s for s in self.sparks if s["life"] > 0 and -2 <= s["x"] < self.w + 2]
        if len(self.sparks) < 8 and self.rng.random() < 0.06:
            self.sparks.append(
                {
                    "x": float(self.rng.randint(0, max(1, self.w - 1))),
                    "y": float(self.rng.randint(1, max(2, int(self.h * 0.55)))),
                    "vx": self.rng.uniform(-40, 40),
                    "vy": self.rng.uniform(-6, 14),
                    "life": self.rng.uniform(0.4, 1.2),
                    "color": self.rng.choice((YEL, CYAN, PINK)),
                }
            )

        if self._typed < len(self._tag) and self.tick % 2 == 0:
            self._typed += 1
        elif self._typed >= len(self._tag) and self.tick % 380 == 0:
            self._typed = 0
            self._tag = self.rng.choice(TAGS)
            self._flash = 0.4

        self._status_age += dt
        if self._status_age > 2.2:
            self._status_age = 0.0
            self._status_i = (self._status_i + 1) % len(STATUS)

        # Chatter lifecycle
        for c in self.chatter:
            c["age"] += dt
            c["life"] -= dt
        self.chatter = [c for c in self.chatter if c["life"] > 0]
        if len(self.chatter) < 4 and self.rng.random() < 0.05:
            self.chatter.append(
                {
                    "text": self.rng.choice(CHATTER),
                    "y": self.rng.randint(2, max(3, self.h - 5)),
                    "x": self.rng.randint(2, max(3, self.w // 6)),
                    "age": 0.0,
                    "life": self.rng.uniform(2.0, 4.5),
                }
            )

        self.glitch_rows = [g for g in self.glitch_rows if g["life"] > 0]
        for g in self.glitch_rows:
            g["life"] -= dt
        if self.rng.random() < 0.03:
            self.glitch_rows.append(
                {
                    "y": self.rng.randint(1, max(1, self.h - 3)),
                    "shift": self.rng.choice((-5, -3, -2, -1, 1, 2, 3, 5, 7)),
                    "life": self.rng.uniform(0.06, 0.32),
                }
            )
            self._rgb_split = 0.4


def main() -> int:
    cols = int(os.environ.get("COLUMNS") or 0)
    rows = int(os.environ.get("LINES") or 0)
    try:
        sz = shutil.get_terminal_size(fallback=(cols or 200, rows or 60))
        cols, rows = sz.columns, sz.lines
    except Exception:
        cols = cols or 200
        rows = rows or 60

    scene = PrivacyAttract()
    scene.resize(cols, rows)

    fd = sys.stdin.fileno()
    old = None
    is_tty = sys.stdin.isatty()
    if is_tty:
        old = termios.tcgetattr(fd)
        tty.setcbreak(fd)

    sys.stdout.write(ALT_ON + HIDE + CLEAR + HOME + bg(*BG_RGB))
    sys.stdout.flush()

    try:
        target_dt = 1.0 / max(6.0, FPS)
        last = time.perf_counter()
        while True:
            if is_tty and key_waiting():
                while key_waiting():
                    os.read(fd, 64)
                break
            if scene.tick % 20 == 0:
                try:
                    sz = shutil.get_terminal_size()
                    scene.resize(max(sz.columns, cols), max(sz.lines, rows))
                except Exception:
                    pass

            now = time.perf_counter()
            dt = min(0.12, now - last)
            last = now
            scene.step(dt)
            sys.stdout.write(scene.paint())
            sys.stdout.flush()

            spent = time.perf_counter() - now
            wait = target_dt - spent
            if wait > 0.004:
                if is_tty:
                    if select.select([sys.stdin], [], [], wait)[0]:
                        os.read(fd, 64)
                        break
                else:
                    time.sleep(wait)
    finally:
        if old is not None:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        sys.stdout.write(SHOW + RESET + ALT_OFF + CLEAR)
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
