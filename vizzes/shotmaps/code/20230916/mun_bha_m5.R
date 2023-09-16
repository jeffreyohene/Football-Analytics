# Load libraries
library(worldfootballR)
library(tidyverse)

# Match link
url <- 'https://understat.com/match/21936'

shots <- understat_match_shots(url)

# create outcome column for shots and goals
shots <- shots |>
  mutate(outcome = ifelse(result == 'Goal', 'Goal', 'Shot'))

# Opta dimensions is 100 x 100, we're going to use a statsbomb 120 x 80 pitch
shots$X <- shots$X * 120
shots$Y <- shots$Y * 80


# For single games we can filter home_away column directly so no need for
# a players' vector to filter
home <- shots |>
  filter(home_away == 'h')

away <- shots |>
  filter(home_away == 'a')


# We will use Python to visualize our shots so we will export it as a .csv file
# use projects so it saves automatically to project directory.
write.csv(home, 'home.csv')
write.csv(away, 'away.csv')