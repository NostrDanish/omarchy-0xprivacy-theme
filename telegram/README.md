# 0xPrivacy Telegram Desktop theme

**`0xPrivacy-Phosphor.tdesktop-theme`** is the importable Telegram Desktop theme bundle. It contains a complete 467-entry `colors.tdesktop-theme` palette and a custom, low-contrast phosphor-grid `background.png`.

The palette follows the Omarchy theme: near-black `#050805` / `#020302`, dark-green surfaces `#0c140c` / `#0a2a0a`, phosphor accent `#39ff14`, and readable pale-green text `#c8ffc8`. Error states remain red for clarity. The color-key schema is based on Telegram Desktop's official `night-green.tdesktop-theme` at commit `1e66d5874c973b9b573492796cbb641152c03f3c`.

## Apply in Telegram Desktop

Open **Settings → Chat Settings → ⋮ → Create New Theme → Import Existing Theme**, then select `0xPrivacy-Phosphor.tdesktop-theme`.

## Regenerate

Run `/usr/bin/python3 ~/.config/omarchy/themes/0xprivacy/generate-telegram-theme.py`. The generator downloads the pinned official reference palette, applies the 0xPrivacy color roles, and rebuilds the bundle plus its readable palette and wallpaper beside this README.
