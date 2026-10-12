# 0xPrivacy Screensaver

An animated phosphor-green terminal attract mode with Matrix rain, glitch effects, a skull mark, and terminal chatter. The animation is rendered by `privacy.py`; the PNG is a static preview.

## Install into Omarchy

After installing this theme, run:

```bash
bash ~/.config/omarchy/themes/0xprivacy/screensaver/install.sh
```

The installer copies the profile to `~/.config/omarchy/branding/screensavers/saved-0xprivacy`. It does **not** switch your active screensaver. To activate it explicitly:

```bash
omarchy-screensaver-profile set saved-0xprivacy
```

Then use `omarchy-screensaver-profile demo` to preview it, or wait for your normal idle trigger. Restore another profile with `omarchy-screensaver-profile set <name>`.

## Runtime

- Python 3 and a terminal with true-color ANSI support are required; no third-party Python modules are used.
- The runner locates `privacy.py` relative to itself, so the profile can be copied or installed without editing paths.
- Default animation rate is 12 FPS. The runner uses low CPU/IO scheduling priority and restores cursor visibility when it exits.
- `OMARCHY_SAVER_FPS` can override the rate if needed.
