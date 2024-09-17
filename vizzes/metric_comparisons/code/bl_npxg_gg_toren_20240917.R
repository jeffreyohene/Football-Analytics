# 17.09.2024
# dieser plot ist nach den ersten 3 Spielen der Bundesliga-Saison 2024/2025
# gebrauchte packages sind kickR f datenscraping, ggplot f den plot und
# ggrepel für labelling

# lade die libraries
library(kickR)
library(ggplot2)
library(ggrepel)

# schüssdaten von fbref.com mit kickR scrapen
shooting <- fbref_team_stats(league = "bundesliga",
                             type = "shooting")

# die scraping gibt die spalten als chr objekte zurück
# wir müssen sie in integer oder numerische Werte umwandeln
shooting$xg_performance <- as.numeric(gsub("\\+", "", shooting$xg_performance))
shooting$npxg_performance <- as.numeric(gsub("\\+", "", shooting$npxg_performance))
shooting$shots <- as.integer(shooting$shots)
shooting$shots_on_target <- as.integer(shooting$shots_on_target)
shooting$goals_against <- as.integer(shooting$goals_against)
shooting$xG <- as.numeric(shooting$xG)
shooting$npxG <- as.numeric(shooting$npxG)

# benutzerdefiniertes vector von primärfarbe hexcodes jedes Club
club_colors <- c(
  "Augsburg" = "#ba3733",
  "Bayern Munich" = "#dc052d",
  "Bochum" = "#00519e",
  "Dortmund" = "#fdea29",
  "Eint Frankfurt" = "#e1000f",
  "Freiburg" = "#d20019",
  "Gladbach" = "#01814a",
  "Heidenheim" = "#e30613",
  "Hoffenheim" = "#1c4790",
  "Holstein Kiel" = "#0071b9",
  "Leverkusen" = "#e32219",
  "Mainz 05" = "#e2001a",
  "RB Leipzig" = "#e2001a",
  "St. Pauli" = "#8e4c2e",
  "Stuttgart" = "#e30916",
  "Union Berlin" = "#e10600",
  "Werder Bremen" = "#00815a",
  "Wolfsburg" = "#64a12d"
)

# plot
ggplot(shooting,
       aes(
         x = npxG,
         y = goals_against,
         size = shots,
         fill = club
         )) +
  geom_point(shape = 21,
             stroke = 0.95,
             color = "black",
             alpha = 0.65) +
  geom_text_repel(
    aes(label = club),
    size = 3.5,
    fontface = "bold",
    color = "black",
    box.padding = 0.35,
    segment.color = NA) +
  scale_color_manual(values = club_colors) +
  scale_fill_manual(values = club_colors) +
  scale_y_continuous(
    breaks = seq(0, max(shooting$goals_against), by = 1)) +
  labs(
    title = "Vergleich von npxG und erzielten Tore in der Bundesliga",
    subtitle = "Vergleich der Vereine",
    x = "npxG",
    y = "Tore",
    caption = "Datenquelle: FBREF.com via kickR",
    color = "Verein"
  ) +
  theme_light(base_family = "Roboto") +
  theme(
    plot.title = element_text(
      face = "bold",
      size = 12),
    plot.subtitle = element_text(
      size = 10,
      margin = margin(0, 0, 10, 0)),
    plot.caption = element_text(
      hjust = 0,
      face = "italic",
      size = 7,
      margin = margin(10, 0, 0, 0)),
    axis.title = element_text(face = "bold"),
    legend.position = "none",
    legend.title = element_text(
      face = "bold",
      size = 10),
    legend.text = element_text(size = 9),
    panel.grid.major = element_line(
      color = "gray90",
      linetype = "dotted"),
    panel.grid.minor = element_blank(),
    panel.border = element_blank(),
    plot.background = element_rect(
      fill = "white",
      color = NA)
  )

# in lokalen directory speichern
ggsave("bl_npxg_gg_toren_20240917.png", width = 10, height = 6, dpi = 300)
