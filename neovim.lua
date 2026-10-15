return {
  {
    "bjarneo/aether.nvim",
    branch = "v3",
    name = "aether",
    priority = 1000,
    opts = {
      colors = {
        bg = "#000000",
        dark_bg = "#010502",
        darker_bg = "#000000",
        lighter_bg = "#06140c",

        fg = "#effbf5",
        dark_fg = "#6d8f80",
        light_fg = "#f7fffb",
        bright_fg = "#ffffff",
        muted = "#6d8f80",

        red = "#ef4444",
        yellow = "#ff9f00",
        orange = "#ff9f00",
        green = "#00f48e",
        cyan = "#00ff9f",
        blue = "#0a3d27",
        magenta = "#bf5af2",
        brown = "#1a2e24",

        bright_red = "#f87171",
        bright_yellow = "#ffc14d",
        bright_green = "#5dffb8",
        bright_cyan = "#7dffe0",
        bright_blue = "#147a4a",
        bright_magenta = "#d7a4f7",

        accent = "#00f48e",
        cursor = "#00f48e",
        foreground = "#effbf5",
        background = "#000000",
        selection = "#063322",
        selection_foreground = "#000000",
        selection_background = "#00f48e",
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
