#!/usr/bin/env bash
set -euo pipefail

PROFILE="saved-0xprivacy"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME:?HOME must be set}/.config/omarchy/branding/screensavers/$PROFILE"

for file in node-loop.mp4 quit-on-key.lua runner.sh 06-node-attract.png README.md; do
  if [[ ! -f "$SCRIPT_DIR/$file" ]]; then
    printf 'Missing package file: %s\n' "$SCRIPT_DIR/$file" >&2
    exit 1
  fi
done

install -d "$DEST"
install -m 0644 "$SCRIPT_DIR/node-loop.mp4" "$DEST/node-loop.mp4"
install -m 0644 "$SCRIPT_DIR/quit-on-key.lua" "$DEST/quit-on-key.lua"
install -m 0644 "$SCRIPT_DIR/06-node-attract.png" "$DEST/06-node-attract.png"
install -m 0644 "$SCRIPT_DIR/README.md" "$DEST/README.md"
install -m 0755 "$SCRIPT_DIR/runner.sh" "$DEST/runner.sh"

printf 'Installed the 0xPrivacy screensaver profile to %s\n' "$DEST"
printf 'It was not activated. To activate it: omarchy-screensaver-profile set %s\n' "$PROFILE"
