import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
import scienceplots

# Load the data
file_path = 'data/combined_cup_processed_participation.csv'
data = pd.read_csv(file_path)

data = data[data['opponent_division'] != 4]


def test_draw_randomness_combined(data, country_name, max_stage=6):
    """
    Tests if the distribution of rank and division combinations in draws reflects random assignment
    within each round.
    """
    country_data = data[data['country_name'] == country_name]
    combined_results = {}

    # Define valid divisions
    valid_divisions = [1, 2, 3, 4, 5]  # Adjust based on your data

    for stage in range(1, max_stage + 1):
        # Filter for the current stage
        stage_data = country_data[country_data['stage'] == stage]

        # Filter for valid divisions
        stage_data = stage_data[stage_data['opponent_division'].isin(valid_divisions)]

        # Check if there is data for the stage after filtering
        if stage_data.empty:
            print(f"No data available for Round {stage} in {country_name}. Skipping...")
            continue

        # Create contingency table for division and rank
        contingency_table = pd.crosstab(stage_data['opponent_division'], stage_data['opponent_league_rank_prev'])

        # Perform Chi-Square Test
        chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

        # Store results
        combined_results[stage] = {
            'Chi2 Statistic': chi2_stat,
            'p-value': p_value,
            'Degrees of Freedom': dof,
            'Expected Frequencies': expected
        }

        # Save contingency table heatmap with observed frequencies
        plt.figure(figsize=(8, 6))
        sns.heatmap(contingency_table, annot=True, cmap="YlGnBu", fmt="d", cbar=False)
        plt.title(f"Observed Rank-Division Combinations for Round {stage} - {country_name}")
        plt.xlabel("Opponent League Rank")
        plt.ylabel("Opponent Division")
        plt.savefig(f"plots/Observed_Rank_Division_Round_{stage}_{country_name}.png")
        plt.close()  # Close the figure after saving

        # Save heatmap of expected frequencies
        expected_df = pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)
        plt.figure(figsize=(8, 6))
        sns.heatmap(expected_df, annot=True, cmap="YlOrRd", fmt=".1f", cbar=False)
        plt.title(f"Expected Rank-Division Combinations for Round {stage} - {country_name}")
        plt.xlabel("Opponent League Rank")
        plt.ylabel("Opponent Division")
        plt.savefig(f"plots/Expected_Rank_Division_Round_{stage}_{country_name}.png")
        plt.show()  # Close the figure after saving

        # Print the results for the round
        print(f"Round {stage}: Chi2 Statistic = {chi2_stat:.4f}, p-value = {p_value:.4f}, Degrees of Freedom = {dof}")

    return combined_results

# Example usage
combined_results = test_draw_randomness_combined(data, country_name='Germany', max_stage=4)
