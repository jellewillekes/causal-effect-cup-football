import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import scienceplots
from sklearn.linear_model import LinearRegression
from utils.load import project_root

# Apply the science and IEEE styles
plt.style.use(['science', 'ieee', 'no-latex'])


def save_plot(plotname, save_dir):
    plt.savefig(os.path.join(save_dir, f'{plotname}.png'), dpi=300, bbox_inches='tight')
    plt.close()


def is_categorical(variable_data):
    return len(variable_data.dropna().unique()) <= 3


# Correlation and Relationship Analysis
def plot_correlation_heatmap(data, outcome_vars, instrumental_vars, treatment_vars, control_vars, save_dir):
    all_vars = outcome_vars + instrumental_vars + treatment_vars + control_vars
    corr = data[all_vars].corr()

    # Plot the heatmap with science style settings and grayscale
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='Greys', fmt='.2f',
                cbar_kws={'label': 'Correlation Coefficient'},
                xticklabels=all_vars, yticklabels=all_vars,
                annot_kws={'size': 9}, linewidths=0.5, linecolor='gray')

    plt.xticks(fontsize=10, rotation=45, ha='right')
    plt.yticks(fontsize=10, rotation=0)

    # Add group borders to distinguish Outcome (Y), Instrument (Z), Treatment (T), and Control (C) groups
    label_positions = [len(outcome_vars), len(outcome_vars) + len(instrumental_vars),
                       len(outcome_vars) + len(instrumental_vars) + len(treatment_vars)]
    for pos in label_positions:
        plt.gca().add_patch(plt.Rectangle((pos, pos), len(all_vars) - pos, len(all_vars) - pos,
                                          fill=False, edgecolor='black', lw=1))
        plt.gca().add_patch(plt.Rectangle((0, pos), pos, len(all_vars) - pos,
                                          fill=False, edgecolor='black', lw=1))
        plt.gca().add_patch(plt.Rectangle((pos, 0), len(all_vars) - pos, pos,
                                          fill=False, edgecolor='black', lw=1))

    # Add labels for the variable groups
    label_offset = -1.2
    plt.text(len(outcome_vars) / 2, -1.5 - label_offset, 'Y', ha='center', va='center', fontsize=12, weight='bold')
    plt.text(len(outcome_vars) + len(instrumental_vars) / 2, -1.5 - label_offset, 'Z', ha='center', va='center',
             fontsize=12, weight='bold')
    plt.text(len(outcome_vars) + len(instrumental_vars) + len(treatment_vars) / 2, -1.5 - label_offset, 'W',
             ha='center', va='center', fontsize=12, weight='bold')
    plt.text(len(outcome_vars) + len(instrumental_vars) + len(treatment_vars) + len(control_vars) / 2,
             -1.5 - label_offset, 'X', ha='center', va='center', fontsize=12, weight='bold')

    # Mirror labels on the left side
    plt.text(len(all_vars) + 0.5, len(outcome_vars) / 2, 'Y', ha='center', va='center', fontsize=12, weight='bold')
    plt.text(len(all_vars) + 0.5, len(outcome_vars) + len(instrumental_vars) / 2, 'Z', ha='center', va='center',
             fontsize=12, weight='bold')
    plt.text(len(all_vars) + 0.5, len(outcome_vars) + len(instrumental_vars) + len(treatment_vars) / 2, 'W',
             ha='center', va='center', fontsize=12, weight='bold')
    plt.text(len(all_vars) + 0.5,
             len(outcome_vars) + len(instrumental_vars) + len(treatment_vars) + len(control_vars) / 2, 'X',
             ha='center', va='center', fontsize=12, weight='bold')

    # Adjust title and layout
    # plt.title('Correlation Heatmap', pad=20, fontsize=14)
    plt.tight_layout()
    save_plot('correlation_heatmap', save_dir)


def plot_next_fixture_performance_by_rank_diff(data, save_dir):
    # Filter data for matches within 5 days
    filtered_data = data[data['Days till League Fixture'] <= 5].copy()

    # Define bins and labels for rank differences
    bins = [-float('inf'), -20, -5, -1, 1, 5, 20, float('inf')]
    labels = ['Much Better', 'Better', 'Little Better', 'Neutral', 'Little Worse', 'Worse', 'Much Worse']
    filtered_data['rank_diff_binned'] = pd.cut(filtered_data['rank_diff'], bins=bins, labels=labels)

    # Group data and compute mean league performance by rank difference and cup result
    grouped_data = filtered_data.groupby(['rank_diff_binned', 'Cup Win'])['League Performance r'].mean().unstack()
    grouped_data.columns = ['Loss', 'Win']

    # Set font and figure size for APA style
    plt.rcParams.update({'font.size': 10, 'font.family': 'sans-serif'})  # Set default font size and family
    plt.figure(figsize=(10, 6))  # Adjust figure size

    # Plot grouped data with muted colors
    ax = grouped_data.plot(kind='bar', stacked=False, color=['#A0A0A0', '#4C9A2A'], alpha=0.8, edgecolor='black',
                           ax=plt.gca())
    ax.set_ylim(0, 2.5)
    ax.set_yticks([0.5, 1, 1.5, 2, 2.5])

    # Apply APA-compliant labels and titles
    plt.grid(axis='y', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    # plt.title('Average League Performance Based on Opponent Strength in Cup Fixture', fontsize=12, pad=10)
    plt.ylabel('Average Points in Next League Fixture', fontsize=10)
    plt.xlabel('Relative Strength of Opponent in Cup Fixture', fontsize=10)

    # APA-style legend
    plt.legend(title='Cup Fixture Result', fontsize=9, title_fontsize='10', frameon=False)

    # Ensure layout without overlapping text
    plt.tight_layout()

    # Save the plot
    save_plot('performance_next_fixture_by_rank_diff', save_dir)


def plot_effect_fixture_days(data, save_dir):
    # Filter data for matches within 6 days (excluding 1 day)
    filtered_data = data[(data['Days till League Fixture'] <= 6) & (data['Days till League Fixture'] != 1)].copy()

    # Convert 'Days till League Fixture' to integers for integer display on x-axis
    filtered_data['Days till League Fixture'] = filtered_data['Days till League Fixture'].astype(int)

    # Define conditions and labels for 'rank_category' based on Division and Top 6 in Division 1
    conditions = [
        (filtered_data['Division'] == 1) & (filtered_data['Team Position'] <= 6),  # Top 6 in Division 1
        (filtered_data['Division'] == 1) & (filtered_data['Team Position'] > 6),  # Remaining teams in Division 1
        (filtered_data['Division'] == 2),  # Division 2
        (filtered_data['Division'] >= 3),  # Division 3 and below
    ]
    labels = ['Top 6', 'League 1', 'League 2', 'League 3+']

    # Apply conditions to create the 'rank_category' column
    filtered_data['rank_category'] = np.select(conditions, labels, default='Other')

    # Group data by 'Days till League Fixture' and 'rank_category' and calculate mean league performance
    grouped_data = filtered_data.groupby(['Days till League Fixture', 'rank_category'])[
        'League Performance r'].mean().reset_index()

    # Set font and figure size for APA style
    plt.rcParams.update({'font.size': 10, 'font.family': 'sans-serif'})  # Default font size and family
    plt.figure(figsize=(10, 6))  # Adjust figure size for consistency

    # Use muted colors for consistency with the other plot
    palette = ['#A0A0A0', '#4C9A2A', '#6aa84f', '#808080']  # Muted grayscale and green shades
    ax = sns.barplot(
        x='Days till League Fixture',
        y='League Performance r',
        hue='rank_category',
        data=grouped_data,
        palette=palette,
        alpha=0.8,
        edgecolor='black'
    )

    # Ensure x-axis displays integers only
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Update labels for APA-style readability
    plt.xlabel('Recovery Days Between Cup and League Fixture', fontsize=12)
    plt.ylabel('Average Points in League Fixture', fontsize=10)
    # plt.title('Average Points in League Fixture after a Cup Fixture by Recovery Days and Team Division',
    #          fontsize=12, pad=10)

    # Adjust legend placement and font size for APA style
    plt.legend(title='Team Division', fontsize=9, title_fontsize=10, frameon=False, loc='upper right')

    # Configure gridlines and save plot
    plt.grid(axis='y', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.ylim(0, 3)
    plt.tight_layout()
    save_plot('performance_effect_fixture_days', save_dir)

