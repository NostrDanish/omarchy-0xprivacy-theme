#!/usr/bin/env bash
set -euo pipefail

# 0xPrivacy — low-priority neon-green hacker attract mode.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

restore_cursor() {
  hyprctl eval 'hl.config({ cursor = { invisible = false } })' &>/dev/null || true
}
trap restore_cursor EXIT INT TERM HUP QUIT

printf '\033]11;rgb:0a/0a/0a\007'
hyprctl eval 'hl.config({ cursor = { invisible = true } })' &>/dev/null || true

deadline=$((SECONDS + 3))
while ((SECONDS < deadline)); do
  size="$(stty size 2>/dev/null || echo 24 80)"
  rows="${size% *}"
  cols="${size#* }"
  if ((rows >= 40 && cols >= 120)); then
    break
  fi
  sleep 0.03
done

export COLUMNS="${cols:-200}"
export LINES="${rows:-60}"
export OMARCHY_SAVER_FPS="${OMARCHY_SAVER_FPS:-12}"
export PYTHONDONTWRITEBYTECODE=1

nice -n 15 ionice -c3 /usr/bin/python3 -B -O "$SCRIPT_DIR/privacy.py"
