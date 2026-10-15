# 0xPrivacy

Full Omarchy theme: forest black, neon green `#39ff14`, rose `#ff2e63`, the 0xHermes wallpaper, its 12 FPS screensaver, and the green/red `0xPrivacy-Phosphor` icon set.

Omarchy applies colors, Hyprland, Neovim, and VS Code from this directory only when the theme path is your own copy or a symlink. A bare git clone is treated as untrusted and those files are dropped.

## Install

```bash
omarchy theme install https://github.com/NostrDanish/omarchy-0xprivacy-theme
bash ~/.config/omarchy/themes/0xprivacy/install.sh
```

`install.sh` copies the icon theme, selects it, installs and selects the screensaver, and sets the wallpaper to `backgrounds/0xhermes.png`.

If this checkout is already on disk:

```bash
ln -sfn "$PWD" ~/.config/omarchy/themes/0xprivacy
omarchy theme refresh
bash "$PWD/install.sh"
```

`omarchy theme refresh` can cycle the wallpaper. `install.sh` puts it back on 0xHermes.

## What is included

| Piece | Path |
|---|---|
| Wallpaper | `backgrounds/0xhermes.png` |
| Screensaver | `screensaver/hermes-crazy.mp4` |
| Icons | `icons/0xPrivacy-Phosphor/` |
| Bar colors | `shell.toml` — text `#39ff14`, active `#ff2e63` |

The screensaver is one loop of the 0xHermes wallpaper: rose scan, phosphor shear, margin rain. Any ordinary key quits. Do not raise it above 12 FPS on a hot laptop.

Launcher icons are duotone. Dark ink is rose. Bright ink is neon green. Regenerate after installing apps:

```bash
/usr/bin/python3 generate-app-icons.py
```
