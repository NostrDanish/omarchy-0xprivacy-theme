return {
  {
    "bjarneo/aether.nvim",
    branch = "v3",
    name = "aether",
    priority = 1000,
    opts = {
      colors = {
        bg = "#050805",
        dark_bg = "#010502",
        darker_bg = "#000000",
        lighter_bg = "#0c140c",

        fg = "#c8ffc8",
        dark_fg = "#00ff41",
        light_fg = "#7cff7c",
        bright_fg = "#c8ffc8",
        muted = "#6d8f80",

        red = "#ff3333",
        yellow = "#ffff99",
        orange = "#ff9f00",
        green = "#39ff14",
        cyan = "#a0ecec",
        blue = "#00ff41",
        magenta = "#7cff7c",
        brown = "#2a6b2a",

        bright_red = "#ff5555",
        bright_yellow = "#ffff99",
        bright_green = "#7cff7c",
        bright_cyan = "#a0ecec",
        bright_blue = "#7ae5e5",
        bright_magenta = "#c8ffc8",

        accent = "#39ff14",
        cursor = "#39ff14",
        foreground = "#c8ffc8",
        background = "#050805",
        selection = "#0a1a0a",
        selection_foreground = "#050805",
        selection_background = "#39ff14",
      },
    },
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "aether",
    },
  },
}
