# Trying to do vizzes completely in R instead of the: 
# scrape data with R, visualize with Python route.
# I will improve the design in the comin weeks but here's the initial template.


# Load necessary libraries
library(tidyverse)
library(worldfootballR)
library(StatsBombR)
library(ggsoccer)
library(ggtext)
library(SBpitch)
library(patchwork)  # Added patchwork library

# Understat URL for match shots data
url <- 'https://understat.com/match/22760'

# Fetch match shots data
shots <- understat_match_shots(url)

# Extract home and away team names
home_team <- shots[1, "home_team"]
away_team <- shots[1, "away_team"]

# Create an 'outcome' column for shots and goals
shots <- shots %>%
  mutate(outcome = ifelse(result == 'Goal', 'Goal', 'Shot'))

# Scale X and Y coordinates to match the pitch dimensions
shots$X <- shots$X * 120
shots$Y <- shots$Y * 80

# Filter shots for the home and away teams
home <- shots %>%
  filter(home_away == 'h')

away <- shots %>%
  filter(home_away == 'a')

# Adjust X and Y coordinates for the away team to mirror the pitch
away$X <- 120 - (away$X)
away$Y <- 80 - (away$Y)

# Create the pitch
pitch <- create_Pitch(grass_colour = "#ffffff", line_colour = "grey40",
                      background_colour = "#ffffff", goal_colour = "#000000",
                      goaltype = "line", middlethird = F, BasicFeatures = F,
                      JdeP = F, padding = 1)

# Define custom colors for shots and goals
shot_colors <- c('Goal' = '#07F586', 'Shot' = '#DB433B')

# Add home team shots with custom border color
home_shots <- geom_point(data = home, 
                         mapping = aes(x = X, 
                                       y = Y, 
                                       color = outcome,  
                                       size = xG * 160))

# Add away team shots with custom border color
away_shots <- geom_point(data = away, 
                         mapping = aes(x = X, 
                                       y = Y, 
                                       color = outcome,
                                       size = xG * 160))

# Combine the layers and customize the color aesthetics
shotmap <- pitch + home_shots + away_shots +
  scale_color_manual(values = shot_colors) +
  theme(plot.title = element_text(hjust = 0.1),
        plot.subtitle = element_text(hjust = 0.09),)

# Create a shotmap with HTML-style labels and centering
shotmap <- shotmap + 
  labs(
    title = paste("Shotmap of", home_team, "vs", away_team),
    subtitle = 'Color Guide: 
      <span style = "color: #DB433B">**Shots**</span> | 
      <span style = "color: #07F586">**Goals**</span>.'
  ) +
  theme(
    plot.subtitle = element_markdown(),
    legend.position = "none",
    plot.background = element_rect(fill = "#ffffff")
  )


# Calculate cumulative xG for home and away teams
home$xg_total <- cumsum(home$xG)
away$xg_total <- cumsum(away$xG)

# create new dataframes for cumulative xG plot
home2 <- home |>
  select(minute,xG,player,outcome,xg_total)

away2 <- away |>
  select(minute,xG,player,outcome,xg_total)


# Extract last shot minute and cumulative xG for both teams
# we would use this to standardize our data so both dataframes start from 0th
# minute and ends after the last shot
cum_xg_home <- tail(home2$xg_total, 1)
cum_xg_away <- tail(away2$xg_total, 1)
last_shot <- tail(shots$minute, 1)

# Create new rows as lists for each team
n_row1 <- list(minute = 0, xG = 0, player = '', outcome = '', xg_total = 0)
n_row_fin <- list(minute = last_shot + 1, xG = 0, player = '', outcome = '', 
                  xg_total = cum_xg_home)
n_row2 <- list(minute = last_shot + 1, xG = 0, player = '', outcome = '', 
               xg_total = cum_xg_away)

# Add new rows to the top and bottom of the dataframes
home2 <- bind_rows(n_row1, home2)
home2 <- bind_rows(home2, n_row_fin)
away2 <- bind_rows(n_row1, away2)
away2 <- bind_rows(away2, n_row2)

# Create a cumulative xG plot for both teams
p <- ggplot() + 
  geom_step(data = home2, 
            mapping = aes(x = minute, 
                          y = xg_total), 
            colour = "#DBC251", 
            size = 1.5, 
            alpha = 0.8)

p <- p + geom_step(data = away2, 
                   mapping = aes(x = minute, 
                                 y = xg_total), 
                   colour = "#07F586", 
                   size = 1.5, 
                   alpha = 0.8)

# Filter for goals
home_g <- home2 %>%
  filter(outcome == 'Goal')

away_g <- away2 %>%
  filter(outcome == 'Goal')

# Add goal markers to the cumulative xG plot
p <- p + 
  geom_point(data = away_g, 
             aes(x = minute, y = xg_total), 
             colour = "black", 
             size = 6, 
             alpha = 1, 
             fill = "#07F586", 
             shape = 21)

# Customize labels and theme for the cumulative xG plot
p <- p + 
  labs(
    x = 'Minute',
    y = 'Cumulative xG',
    title = paste("xG Match Story:", home_team, "vs", away_team),
    subtitle = 'Color Guide: 
      <span style = "color: #DBC251">**Girona**</span> | 
      <span style = "color: #07F586">**Real Madrid**</span>.'
  ) +
  theme_bw() +
  theme(
    plot.subtitle = element_markdown()
  )

# Arrange plots vertically
dashboard <- shotmap / p

# Customize the layout if needed
dashboard <- dashboard +
  plot_layout(guides = 'collect')  # Collect legends to a single legend

# Define the filename for saving the dashboard
filename <- "dashboard.png"

# Save the dashboard as an image
ggsave(filename, plot = dashboard, width = 9.5, height = 12, dpi = 300)
       