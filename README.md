# 0xPrivacy

Phosphor mainframe theme for this Omarchy box.

- Neon `#39ff14` / matrix `#00ff41` on `#050805`
- Wallpaper: dense rain + HUD + skull (`backgrounds/01-root-shell.png`)
- Icons: 0xPrivacy-Phosphor frameless, monochrome-green app icons (inherits Yaru-olive-dark)
- App-cover generator: run `/usr/bin/python3 ~/.config/omarchy/themes/0xprivacy/generate-app-icons.py` after installing/removing apps
- Telegram: full 467-color `telegram/0xPrivacy-Phosphor.tdesktop-theme` bundle + matching phosphor-grid chat wallpaper; regenerate with `/usr/bin/python3 ~/.config/omarchy/themes/0xprivacy/generate-telegram-theme.py`
- Keyboard RGB: 57,255,20
- Optional screensaver bundle: animated 0xPrivacy attract mode + preview in `screensaver/`. After installing the theme, install the profile with `bash ~/.config/omarchy/themes/0xprivacy/screensaver/install.sh`; activation is separate and documented in `screensaver/README.md`.

```bash
omarchy theme set 0xprivacy
omarchy theme bg set ~/.config/omarchy/backgrounds/0xprivacy/01-root-shell.png
```
