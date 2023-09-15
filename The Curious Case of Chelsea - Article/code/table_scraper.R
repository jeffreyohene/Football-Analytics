# Libraries needed
library(tidyverse)
library(rvest)

# Custom function to extract a table based on XPath and table ID
extract_table <- function(page, xpath, table_id) {
  page |>
    html_node(xpath = xpath) |>
    html_table()
}

# FBREF website
# Note: if you send multiple requests within 3 seconds, you will be 
# blocked for around 12 hours.
url <- "https://fbref.com/en/comps/9/Premier-League-Stats"

# Read the HTML content of the page
page <- read_html(url)

# Specify the XPaths and table IDs
table_data <- list(
  standard = '//*[@id="div_stats_squads_standard_for"]',
  goalkeeping = '//*[@id="div_stats_squads_keeper_for"]',
  goalkeeping_adv = '//*[@id="div_stats_squads_keeper_adv_for"]',
  shooting = '//*[@id="div_stats_squads_shooting_for"]',
  passing = '//*[@id="div_stats_squads_passing_for"]',
  pass_types = '//*[@id="div_stats_squads_passing_types_for"]',
  gca = '//*[@id="div_stats_squads_gca_for"]',
  def = '//*[@id="div_stats_squads_defense_for"]',
  poss = '//*[@id="div_stats_squads_possession_for"]',
  misc = '//*[@id="div_stats_squads_misc_for"]'
)

# Extract tables using our extract_table function
table_list <- lapply(table_data, function(xpath) extract_table(page, xpath))

# Save files to our dir
for (table_name in names(table_list)) {
  table <- table_list[[table_name]]
  csv_filename <- paste(table_name, ".csv", sep = "")
  write.csv(table, file = csv_filename, row.names = FALSE)
}
