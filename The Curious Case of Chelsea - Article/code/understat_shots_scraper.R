# Libraries
library(worldfootballR)
library(tidyverse)

# Scrape data from understat with worldfootballR
shots <- understat_team_season_shots('https://understat.com/team/Chelsea/2023')

#Shot type: You can do a visual that shows blocked shots, missed shots, 
# saved shots, shots on goal but I prefer to categorize them into two: shots &
# goals so the shotmap looks cleaner.
shots <- shots |>
  mutate(outcome = ifelse(result == 'Goal', 'Goal', 'Shot'))

# Opta dimensions is 100 x 100, we're going to use a statsbomb 120 x 80 pitch
shots$X <- shots$X * 120
shots$Y <- shots$Y * 80

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
# use projects so it saves automatically to project directory.
write.csv(che_shots, "che_shots.csv")
write.csv(agn_che, "agn_che.csv")