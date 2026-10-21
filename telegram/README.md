# 0xPrivacy Telegram Desktop theme

**`0xPrivacy-Phosphor.tdesktop-theme`** is the importable Telegram Desktop theme bundle. It contains a complete 467-entry `colors.tdesktop-theme` palette and a custom low-contrast phosphor-grid chat background.

The palette follows the 0xPrivacy 80s hacker theme: deep green-black `#050805`, raised green surfaces `#0c140c`, neon green `#39ff14`, pale-green text `#c8ffc8`, amber `#ff9f00` for heat, and red `#ff3333` for errors. The color-key schema is based on Telegram Desktop's official `night-green.tdesktop-theme` at commit `1e66d5874c973b9b573492796cbb641152c03f3c`.

## Apply in Telegram Desktop

Open **Settings → Chat Settings → ⋮ → Create New Theme → Import Existing Theme**, then select `0xPrivacy-Phosphor.tdesktop-theme`.

## Regenerate

Run `/usr/bin/python3 ~/.config/omarchy/themes/0xprivacy/generate-telegram-theme.py`. The generator downloads the pinned official reference palette, applies the 0xPrivacy dark-web color roles, and rebuilds the bundle plus its readable palette and wallpaper beside this README.
