library(tidyverse)
library(ggrepel)

# Get a list of all CSV files in the current directory
csv_files <- list.files(pattern = "*.csv")

# Initialize an empty list to store the data frames
data_frames <- list()

# Loop through the CSV files and import them with skip
for (file in csv_files) {
  # Use the file name (without the .csv extension) as the list element name
  data_frames[[sub("\\.csv$", "", file)]] <- read_csv(file, skip = 1)
}

# Loop through the data_frames list and assign each data frame to a variable
for (file_name in names(data_frames)) {
  # Use the file name as the variable name
  assign(file_name, data_frames[[file_name]])
}



colnames(standard)


team_colors <- c("Arsenal" = "#EF0107", 
                 "Aston Villa" = "#9E112E", 
                 "Bournemouth" = "#DA020E",
                 "Brentford" = "#EF3340",
                 "Brighton" = "#0057B8",
                 "Burnley" = "#6C1D45",
                 "Chelsea" = "#034694",
                 "Crystal Palace" = "#005CBF",
                 "Everton" = "#003399",
                 "Fulham" = "#000000",
                 "Liverpool" = "#C8102E",
                 "Luton Town" = "#FF5700",
                 "Manchester City" = "#6CAEE0",
                 "Manchester Utd" = "#DA020E",
                 "Newcastle United" = "#000000",
                 "Nott'ham Forest" = "#FF171F",
                 "Sheffield Utd" = "#E03A3E",
                 "Tottenham" = "#FFFFFF",
                 "West Ham" = "#7A263A",
                 "Wolves" = "#FFDB00")

team_names <- c("Arsenal" = "AFC", 
                 "Aston Villa" = "AVL", 
                 "Bournemouth" = "BOU",
                 "Brentford" = "BRE",
                 "Brighton" = "BRI",
                 "Burnley" = "BUR",
                 "Chelsea" = "CHE",
                 "Crystal Palace" = "CRY",
                 "Everton" = "EVE",
                 "Fulham" = "FUL",
                 "Liverpool" = "LIV",
                 "Luton Town" = "LUT",
                 "Manchester City" = "MCI",
                 "Manchester United" = "MUN",
                 "Newcastle United" = "NEW",
                 "Nottingham Forest" = "NFO",
                 "Sheffield United" = "SHE",
                 "Tottenham Hotspur" = "TOT",
                 "West Ham United" = "WHU",
                 "Wolverhampton Wanderers" = "WOL")

standard$Gls...9 <- as.numeric(standard$Gls...9)

bad_box <- data.frame(
  xmin = -Inf, xmax = 6.2, 
  ymin = -Inf, ymax = 6.5)
above_avg_box <- data.frame(
  xmin = -Inf, xmax = 6.2, 
  ymin = 6.5, ymax = Inf)
good_low_box <- data.frame(
  xmin = 6.2, xmax = Inf, 
  ymin = -Inf, ymax = 6.5)
very_good_box <- data.frame(
  xmin = 6.2, xmax = Inf, 
  ymin = 6.5, ymax = Inf)

rect_data <- rbind(good_low_box, bad_box, above_avg_box, very_good_box)


# Calculate the mean values
mean_xG <- mean(standard$`xG...17`)
mean_Gls <- mean(standard$`Gls...9`)

# Create a ggplot scatterplot with a trendline for the mean

# Custom formatting function to remove decimal points and format as integers
format_integer <- function(x) {
  as.integer(x)
}

ggplot() +
  geom_rect(data = rect_data,
            aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax),
            fill = c("#FFDB00", "#EF3340", "#FFD699", "#00FF7F"),
            alpha = c(0.1, 0.1, 0.2, 0.1)) +
  geom_point(data = standard, aes(x = `Gls...9`, y = `xG...17`, color = Squad), size = 4.5) +
  geom_text(data = standard, aes(x = `Gls...9`, y = `xG...17`, label = team_names), nudge_x = 0.27, nudge_y = 0.15, size = 3) +
  labs(
    x = "Goals Scored",
    y = "Expected Goals",
    title = "Expected Goals vs. Goals Scored In the Premier League",
    subtitle = "*Stats are after Gameweek 4"
  ) +
  theme_minimal() +
  geom_hline(yintercept = mean_xG, linetype = "dashed") +  # Mean xG
  geom_vline(xintercept = mean_Gls, linetype = "dashed") +  # Mean Goals
  annotate("text", x = mean_Gls - 0.95, y = 11, 
           label = paste("Average Goals:", round(mean_Gls, 2)), color = "grey20") +
  annotate("text", x = max(standard$`Gls...9`), y = mean_xG + 0.2, 
           label = paste("Average xG:", round(mean_xG, 2)), color = "grey20") +
  annotate("text", fontface = "bold", x = 11.2, 
           y = 11, hjust = 0, color = "#2E8B57", size = 4,
           label = "Very High xG\nMore Goals") +
  annotate("text", fontface = "bold", x = 1.2, 
           y = 11, hjust = 0, color = "#FFA500", size = 4,
           label = "Very High xG\nFewer Goals") +
  annotate("text", fontface = "bold", x = 4.5, 
           y = 1.77, hjust = 0, color = "#EF3340", size = 4,
           label = "Very Low xG\nFewer Goals") +
  scale_color_manual(values = team_colors) +
  guides(color = FALSE) +
  theme(
    plot.title = element_text(size = 18, face = "bold", color = "#034694"),
    axis.text.x = element_text(size = 12),
    axis.text.y = element_text(size = 12),
    axis.title = element_text(size = 14)
  ) +
  scale_x_continuous(labels = format_integer) +  # Apply the custom formatting function to x-axis
  scale_y_continuous(labels = format_integer)
