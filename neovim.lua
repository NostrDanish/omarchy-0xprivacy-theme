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

        fg = "#e8ffe8",
        dark_fg = "#00ff41",
        light_fg = "#7cff7c",
        bright_fg = "#f2fff4",
        muted = "#6d8f80",

        red = "#ff3333",
        yellow = "#ff9f00",
        orange = "#ff6600",
        green = "#39ff14",
        cyan = "#2f9a2f",
        blue = "#c8ffc8",
        magenta = "#7cff7c",
        brown = "#2f9a2f",

        bright_red = "#ff5555",
        bright_yellow = "#ffb84d",
        bright_green = "#7cff7c",
        bright_cyan = "#2f9a2f",
        bright_blue = "#c8ffc8",
        bright_magenta = "#e8ffe8",

        accent = "#39ff14",
        cursor = "#39ff14",
        foreground = "#e8ffe8",
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
