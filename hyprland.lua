local active_border_color = { colors = { "rgba(00f48eee)", "rgba(ff9f00ee)" }, angle = 45 }
local inactive_border_color = "rgba(0a3d27aa)"

hl.config({
  general = {
    col = {
      active_border = active_border_color,
      inactive_border = inactive_border_color,
    },
  },

  group = {
    col = {
      border_active = active_border_color,
      border_inactive = inactive_border_color,
    },
  },
})
