# 0xPrivacy

Full Omarchy theme. Default is the live desktop: near-black field, phosphor `#39ff14`, phosphor green, rose `0x`, the Lockup wallpaper, the glitch screensaver, and the green `0xPrivacy-Phosphor` icon set.

The palette comes from `privacy-tokens.json` v1.5. `colors.toml` is the single source of truth: Omarchy's renderer derives the terminal, editor, Hyprland, and Hermes skins from it, and `lucas.system-pulse` reads the active theme's `colors.toml` at runtime for its statusline inks.

Omarchy applies colors, Hyprland, Neovim, VS Code, and menus only when the theme path is your own copy or a symlink. A bare git clone drops `hyprland.lua`, `neovim.lua`, and `vscode.json`.

## Install

```bash
omarchy theme install https://github.com/NostrDanish/omarchy-0xprivacy-theme
bash ~/.config/omarchy/themes/0xprivacy/install.sh
```

`install.sh` copies the icon theme, selects it, installs and selects `saved-0xprivacy`, and sets the wallpaper to `backgrounds/00-lockup.png`.

`omarchy theme refresh` can cycle the wallpaper. Run `install.sh` again to put Lockup back.

## Wallpapers

The picker labels come from the filenames. `00-lockup.png` sorts first, so a fresh apply lands on it.

| File | What it is |
|---|---|
| `backgrounds/00-lockup.png` | Default. Rose `0x`, phosphor `PRIVACY`. |
| `backgrounds/04-stealth-mode.png` | The same wordmark, left aligned. |
| `backgrounds/0xhermes.png` | Phosphor mascot plus the wordmark. |
| `backgrounds/00-node.png` | DIGITAL CAGE node. |
| `backgrounds/01-root-shell.png` | Mascot and wordmark, root footer. |
| `backgrounds/02-ghost-protocol.png` | Mascot only. |
| `backgrounds/03-cipher-storm.png` | Mascot, wordmark, verify line. |

## Screensaver

`screensaver/privacy-glitch.mp4` is an 8-second 12 FPS loop: the rose `0x` tears in, `PRIVACY` types on, margin rain, one slice glitch. Any ordinary key quits. Do not pass `--fps` to mpv.

## Menus and icons

Bar text and menu selection are `#39ff14`. Window borders run phosphor to trust blue. Launcher covers are hacker green, 89 icons, in `icons/0xPrivacy-Phosphor/`.

## Statusline

`lucas.system-pulse` resolves its metric inks from the active theme's `colors.toml`, not from a theme-local file. Each named key and its `colorN` twin carry the same value so the two lookup paths agree.

| Metric | Key | Ink | Contrast on `#050805` |
|---|---|---|---|
| CPU | `green` / `color2` | `#39ff14` | 14.84:1 |
| Memory | `magenta` / `color5` | `#7cff7c` | 15.77:1 |
| GPU | `blue` / `color4` | `#00ff41` | 14.84:1 |
| Heat | `yellow` / `color3` | `#ffff99` | 19.18:1 |
| Disk | `cyan` / `color6` | `#a0ecec` | 15.05:1 |

`statusline.yaml` mirrors this table as a human-readable record. It does not drive the widget.
