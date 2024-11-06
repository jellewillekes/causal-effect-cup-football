import os
import pandas as pd
from utils.load import project_root, load_csv
from plot_new import *

# Load data
country = 'Combined'
cup = 'combined_cup'
data = load_csv(os.path.join(project_root(), 'eda', 'data', 'combined_cup_processed_participation.csv'))

# Directory to save plots
save_dir = os.path.join(project_root(), 'eda', 'plots/new', country)
os.makedirs(save_dir, exist_ok=True)

# Variable mapping dictionary (current column names -> paper definitions)
variable_definitions = {
    'next_team_points_round': 'League Performance r',
    'next_team_points_round_plus': 'League Performance r+1', # Points earned by the team in their subsequent league
    # match
    'opponent_league_rank_prev': 'Opponent Position',  # Rank of the opponent in the previous season
    'opponent_division': 'Division',  # Division of the opponent in the previous season
    'team_win': 'Cup Win',  # Indicates if the team won the cup match
    'team_league_rank_prev': 'Team Position',  # Team's rank in their league in the previous season
    'team_size': 'Team Size',  # Number of players in the team
    'foreigners': 'Foreign Players',  # Number of foreign players in the team
    'mean_age': 'Mean Age',  # Average age of players in the team
    'mean_value': 'Mean Market Value',  # Average market value of players
    'total_value': 'Total Market Value',  # Aggregate market value of the squad
    'distance': 'Distance Traveled',  # Distance traveled for the cup match
    'extra_time': 'Extra Time',  # Indicates if the cup match included extra time
    'next_fixture_days_round': 'Days till League Fixture',  # Days until next league match
    'team_home': 'Team Home',  # Added based on previous code
    'country_code': 'Country'  # Country where the team is based
}

# Rename columns in DataFrame for plotting
data = data.rename(columns=variable_definitions)

# Variables of interest with updated names
outcome_vars = ['League Performance r', 'League Performance r+1']
instrumental_vars = ['Opponent Position', 'Division']
treatment_vars = ['Cup Win']
control_vars = [
    'Team Position', 'Distance Traveled', 'Team Size', 'Mean Age',
    'Foreign Players', 'Mean Market Value', 'Total Market Value',
    'Extra Time', 'Days till League Fixture', 'Country'
]

plot_effect_fixture_days(data, save_dir)

plot_correlation_heatmap(data, outcome_vars, instrumental_vars, treatment_vars, control_vars, save_dir)
plot_next_fixture_performance_by_rank_diff(data, save_dir)

# Call the plotting function for variable distributions
# plot_variable_distributions(data, outcome_vars, instrumental_vars, treatment_vars, control_vars, save_dir)
# plot_financial_control_variables(data, save_dir)

# plot_avg_points_by_cup_round_line(data, save_dir)
# plot_rank_change_by_cup_round_line(data, save_dir)

# plot_next_fixture_performance_by_rank_diff(data, save_dir)
# plot_league_rank_change_by_opponent_strenght(data, save_dir)

# Call the function to plot the correlation heatmap

# plot_avg_points_by_cup_round(data, save_dir)
# plot_win_percentage_by_cup_round(data, save_dir)
#
# plot_league_rank_change_by_cup_round(data, save_dir)
#
# plot_effect_travel_distance(data, save_dir)
#
# plot_effect_fixture_days(data, save_dir)
#
# plot_effect_fixture_days_regression(data, save_dir)
#
# plot_extra_time_effect_on_performance(data, save_dir)
