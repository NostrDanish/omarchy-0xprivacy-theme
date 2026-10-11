return {
  {
    "bjarneo/aether.nvim",
    branch = "v3",
    name = "aether",
    priority = 1000,
    opts = {
      colors = {
        bg = "#050805",
        dark_bg = "#020302",
        darker_bg = "#000000",
        lighter_bg = "#0c140c",

        fg = "#00ff41",
        dark_fg = "#1a6b1a",
        light_fg = "#7cff7c",
        bright_fg = "#c8ffc8",
        muted = "#1a4a1a",

        red = "#ff3333",
        yellow = "#c8ff00",
        orange = "#ff6600",
        green = "#00ff41",
        cyan = "#00ffc8",
        blue = "#00aa66",
        magenta = "#39ff14",
        brown = "#2a6b2a",

        bright_red = "#ff5555",
        bright_yellow = "#ffff99",
        bright_green = "#39ff14",
        bright_cyan = "#7fffd4",
        bright_blue = "#00ffc8",
        bright_magenta = "#7cff7c",

        accent = "#39ff14",
        cursor = "#39ff14",
        foreground = "#00ff41",
        background = "#050805",
        selection = "#0a2a0a",
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
