import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
import scienceplots

# Load the data
file_path = 'data/combined_cup_processed_participation.csv'
data = pd.read_csv(file_path)

data = data[data['opponent_division'] != 3]


def test_complete_draw_randomness(data, country_name, max_stage=6):
    """
    Tests if the distribution of rank and division combinations in draws reflects random assignment
    within each fixture and each round.
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

        # Test Fixture ID vs. Opponent Division
        division_contingency_table = pd.crosstab(stage_data['fixture_id'], stage_data['opponent_division'])
        chi2_stat_div, p_value_div, dof_div, expected_div = chi2_contingency(division_contingency_table)

        # Test Fixture ID vs. Opponent Rank
        rank_contingency_table = pd.crosstab(stage_data['fixture_id'], stage_data['opponent_league_rank_prev'])
        chi2_stat_rank, p_value_rank, dof_rank, expected_rank = chi2_contingency(rank_contingency_table)

        # Store results
        combined_results[stage] = {
            'Fixture vs Division Chi2 Statistic': chi2_stat_div,
            'Fixture vs Division p-value': p_value_div,
            'Fixture vs Division Degrees of Freedom': dof_div,
            'Fixture vs Rank Chi2 Statistic': chi2_stat_rank,
            'Fixture vs Rank p-value': p_value_rank,
            'Fixture vs Rank Degrees of Freedom': dof_rank,
            'Expected Frequencies (Division)': expected_div,
            'Expected Frequencies (Rank)': expected_rank
        }

        # Save heatmaps for observed frequencies
        plt.figure(figsize=(8, 6))
        sns.heatmap(division_contingency_table, annot=True, cmap="YlGnBu", fmt="d", cbar=False)
        plt.title(f"Observed Fixture-Division Combinations for Round {stage} - {country_name}")
        plt.xlabel("Opponent Division")
        plt.ylabel("Fixture ID")
        plt.savefig(f"plots/Observed_Fixture_Division_Round_{stage}_{country_name}.png")
        plt.close()

        plt.figure(figsize=(8, 6))
        sns.heatmap(rank_contingency_table, annot=True, cmap="YlOrRd", fmt="d", cbar=False)
        plt.title(f"Observed Fixture-Rank Combinations for Round {stage} - {country_name}")
        plt.xlabel("Opponent Rank")
        plt.ylabel("Fixture ID")
        plt.savefig(f"plots/Observed_Fixture_Rank_Round_{stage}_{country_name}.png")
        plt.close()

        # Save heatmaps for expected frequencies
        expected_div_df = pd.DataFrame(expected_div, index=division_contingency_table.index,
                                       columns=division_contingency_table.columns)
        plt.figure(figsize=(8, 6))
        sns.heatmap(expected_div_df, annot=True, cmap="YlOrRd", fmt=".1f", cbar=False)
        plt.title(f"Expected Fixture-Division Combinations for Round {stage} - {country_name}")
        plt.xlabel("Opponent Division")
        plt.ylabel("Fixture ID")
        plt.savefig(f"plots/Expected_Fixture_Division_Round_{stage}_{country_name}.png")
        plt.close()

        expected_rank_df = pd.DataFrame(expected_rank, index=rank_contingency_table.index,
                                        columns=rank_contingency_table.columns)
        plt.figure(figsize=(8, 6))
        sns.heatmap(expected_rank_df, annot=True, cmap="YlOrRd", fmt=".1f", cbar=False)
        plt.title(f"Expected Fixture-Rank Combinations for Round {stage} - {country_name}")
        plt.xlabel("Opponent Rank")
        plt.ylabel("Fixture ID")
        plt.savefig(f"plots/Expected_Fixture_Rank_Round_{stage}_{country_name}.png")
        plt.close()

        # Print the results for the round
        print(
            f"Round {stage}: Fixture vs Division - Chi2 Statistic = {chi2_stat_div:.4f}, p-value = {p_value_div:.4f}, Degrees of Freedom = {dof_div}")
        print(
            f"Round {stage}: Fixture vs Rank - Chi2 Statistic = {chi2_stat_rank:.4f}, p-value = {p_value_rank:.4f}, Degrees of Freedom = {dof_rank}")

    return combined_results


# Example usage
combined_results = test_complete_draw_randomness(data, country_name='Portugal', max_stage=6)
