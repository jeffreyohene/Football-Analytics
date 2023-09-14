# Libraries
library(worldfootballR)
library(tidyverse)

# Scrape data from understat with worldfootballR
shots <- understat_team_season_shots('https://understat.com/team/Chelsea/2023')


# We need a filtering condition to filter shots hit by Chelsea
players <- unique(shots$player)

# Create a new vector based on players to extract Chelsea shots
# do a quick visual scan of scraped data to see if any names are being excluded
# sometimes there are issues because of player names and accents

che <- c("Enzo Fernández", "Nicolas Jackson", "Axel Disasi","Ben Chilwell",
         "Reece James","Levi Colwill","Thiago Silva","Conor Gallagher",
         "Carney Chukwuemeka","Malo Gusto","Raheem Sterling","Moisés Caicedo",
         "Mykhailo Mudryk","Noni Madueke", "Ian Maatsen")

# Filter for shots hit and conceded by Chelsea
# Verify if the total rows tallies with subsets
che_shots <- shots |>
  filter(player %in% che)

agn_che <- shots |>
  filter(!player %in% che)

# We will use Python to visualize our shots so we will export it as a .csv file
write.csv(che_shots, "che_shots.csv")
write.csv(agn_che, "agn_che.csv")