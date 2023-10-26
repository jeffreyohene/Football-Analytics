library(tidyverse)
library(gganimate)

df <- read_csv('winners.csv')

#df <- df |> select(year, winner, title)

#df$year <- as.Date(paste0(df$year, "-01-01"), format = "%Y-%m-%d")

cc <- df |>
  group_by(winner) |>
  mutate(total_titles = cumsum(title))


cc <- cc |>
  group_by(year) |>
  mutate(rk = rank(total_titles, ties.method = 'first')) |> # Used the ties method as first so for ties, the latest winner ranks higher
  arrange(year)



# Define a vector of hex color codes for the football clubs
club_colors <- c(
  "Arsenal" = "#EF0107",
  "Manchester United" = "#DA020E",
  "Manchester City" = "#6CADDF",
  "Blackburn Rovers" = "#1E2D55",
  "Chelsea" = "#034694",
  "Liverpool" = "#C8102E",
  "Leicester City" = "#0053A0"
)

# Plot
p <- ggplot(cc, aes(rk, group = winner, fill = as.factor(winner), color = as.factor(winner))) +
  geom_tile(aes(y = total_titles/2, height = total_titles, width = 0.9), alpha = 1, color = NA) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.2))) +
  scale_fill_manual(values = club_colors) +
  labs(title = 'Premier League Champions Race: {closest_state}',
       x = '',
       y = '',
       subtitle = 'Clubs:
      <span style = "color: #DA020E">**United**</span>,
      <span style = "color: #1E2D55">**Blackburn**</span>,
      <span style = "color: #EF0107">**Arsenal**</span>,
      <span style = "color: #034694">**Chelsea**</span>,
      <span style = "color: #6CADDF">**City**</span>,
      <span style = "color: #0053A0">**Leicester**</span> &
      <span style = "color: #C8102E">**Liverpool**</span>.',
       caption='©2023 @jeffrstats') +
  coord_flip() +
  theme_minimal() +
  theme(
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.text.x = element_text(size = 15, color = "grey"),
    plot.margin = margin(2, 2, 2, 2, 'cm'),
    plot.title = element_text(size = 22, color = 'grey20', face = 'bold'),
    plot.subtitle = ggtext::element_markdown(size = 13, lineheight = 1),
    plot.caption = element_text(size = 14),
    legend.position = 'none',
    panel.grid.minor.y = element_blank(),
    panel.grid.major.y = element_blank()
  )

p <- p + transition_states(year, state_length = 0, wrap = F)

animate(
  p,
  fps = 20,
  start_pause = 25,
  end_pause = 35,
  duration = 15,
  width = 1200,
  height = 800)
