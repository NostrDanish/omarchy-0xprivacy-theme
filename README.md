# 0xPrivacy

Full Omarchy theme. Default is the live desktop: black field, phosphor `#00ff41`, rose `0x`, the Lockup wallpaper, the glitch screensaver, and the green `0xPrivacy-Phosphor` icon set.

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

Bar text and menu selection are `#00ff41`. Window borders are phosphor to rose. Launcher covers are hacker green, 89 icons, in `icons/0xPrivacy-Phosphor/`.
