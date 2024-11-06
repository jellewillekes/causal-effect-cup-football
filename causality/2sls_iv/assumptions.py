import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scienceplots  # Ensure SciencePlots is imported

# Apply the science and IEEE styles
plt.style.use(['science', 'ieee', 'no-latex'])

# Load the data
file_path = 'data/combined_cup_processed_participation.csv'
data = pd.read_csv(file_path)


def plot_unique_combination_percentage(data, country_name, year, max_stage=6):
    """
    Generates a bar chart showing the percentage of unique combinations of opponent rank and division
    by round for a specific country and year, using a scientific plotting style.
    """
    # Filter the dataset for the specified country, year, and stage limit
    country_data = data[
        (data['country_name'] == country_name) & (data['year'] == year) & (data['stage'].between(1, max_stage))
        ]

    # Dictionary to store unique combination percentages per stage
    unique_combinations_percentage = {}

    # Calculate unique combination percentages for each stage
    for stage in range(1, max_stage + 1):
        stage_data = country_data[country_data['stage'] == stage]
        combinations = stage_data[['opponent_league_rank_prev', 'opponent_division']]
        total_count = combinations.shape[0]
        unique_count = combinations.drop_duplicates().shape[0]
        unique_combinations_percentage[stage] = (unique_count / total_count) * 100 if total_count > 0 else 0

    # Plotting the unique combination percentage per round
    plt.figure(figsize=(10, 6))
    plt.bar(unique_combinations_percentage.keys(), unique_combinations_percentage.values(), color="lightgray",
            edgecolor="black", alpha=0.8)
    plt.xlabel("Cup Round", fontsize=12)
    plt.ylabel("Unique Combination (%)", fontsize=12)
    plt.title(f"Percentage of Unique Combinations of Opponent Position and Division for FA Cup {year}", fontsize=14)

    # Use ScalarFormatter to display integers without the percentage symbol
    plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(20))  # Sets ticks at intervals of 20

    # Add a horizontal line at y=100 for reference, if relevant to context
    plt.axhline(100, color='gray', linestyle='--', linewidth=1)

    # Save the bar chart to a file
    bar_chart_file = f"data/{country_name}_{year}_unique_combinations.png"
    plt.tight_layout()
    plt.savefig(bar_chart_file, dpi=300)
    plt.show()
    print(f"Bar chart saved to {bar_chart_file}")


# Call the function to generate the plot
plot_unique_combination_percentage(data, 'England', 2020)
