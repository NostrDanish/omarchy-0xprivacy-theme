#!/usr/bin/env bash
set -euo pipefail

# Install the full 0xPrivacy theme pieces Omarchy does not apply by itself:
# green/red launcher icons, the 0xHermes wallpaper, and the screensaver.
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ICON_SRC="$ROOT/icons/0xPrivacy-Phosphor"
ICON_DEST="${XDG_DATA_HOME:-$HOME/.local/share}/icons/0xPrivacy-Phosphor"
WALLPAPER="$ROOT/backgrounds/00-node.png"

if [[ ! -d "$ICON_SRC" ]]; then
  printf 'Missing icon theme: %s\n' "$ICON_SRC" >&2
  exit 1
fi
if [[ ! -f "$WALLPAPER" ]]; then
  printf 'Missing wallpaper: %s\n' "$WALLPAPER" >&2
  exit 1
fi

rm -rf "$ICON_DEST"
mkdir -p "$(dirname "$ICON_DEST")"
cp -a "$ICON_SRC" "$ICON_DEST"
rm -f "$ICON_DEST/icon-theme.cache"
if command -v gtk-update-icon-cache >/dev/null; then
  gtk-update-icon-cache -f "$ICON_DEST" >/dev/null
fi
gsettings set org.gnome.desktop.interface icon-theme '0xPrivacy-Phosphor'

bash "$ROOT/screensaver/install.sh"
if command -v omarchy-screensaver-profile >/dev/null; then
  omarchy-screensaver-profile set saved-0xprivacy
fi

if command -v omarchy-theme-bg-set >/dev/null; then
  omarchy-shell -q background setInstant "$WALLPAPER" || true
  omarchy-theme-bg-set "$WALLPAPER"
fi

printf '0xPrivacy theme pieces installed.\n'
printf 'icon-theme=%s\n' "$(gsettings get org.gnome.desktop.interface icon-theme)"
if command -v omarchy-screensaver-profile >/dev/null; then
  printf 'screensaver=%s\n' "$(omarchy-screensaver-profile current)"
fi
if command -v omarchy >/dev/null; then
  printf 'wallpaper=%s\n' "$(omarchy theme bg current)"
fi
