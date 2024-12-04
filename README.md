# Evaluating the effect of cup participation on league performance: Evidence from European domestic cups

This repository contains the analysis and methodology from my MSc thesis: *Evaluating the Effect of Cup Participation on League Performance: Evidence from European Domestic Cups* (Grade: 8.0) as part of the MSc Econometrics and Management Science. The study investigates the causal effect of participating in and winning domestic cup fixtures on subsequent league performance, with a focus on randomness from cup draws as a source of exogenous variation.

## Problem Statement

Fixture congestion is a well-known issue in football, often cited as a challenge by players and managers. However, its impact on team performance remains debated. This study examines two primary questions:
1. Does winning a domestic cup fixture improve performance in the next league match?
2. Does participating in a domestic cup fixture, irrespective of the result, affect subsequent league performance?

The analysis covers domestic cup competitions in four countries: the FA Cup (England), DFB Pokal (Germany), KNVB Beker (Netherlands), and Taça de Portugal (Portugal).

## Methodology

### Data
- **Scope**: Data includes 2012-2023 seasons from four European leagues.
- **Variables**: Cup participation and outcomes, subsequent league performance, opponent strength, recovery days, travel distances, team financial characteristics (market value, squad size), and more.
- **Sources**: API-Football for fixtures and Transfermarkt for team financial data.

### Approach
1. **Instrumental Variable (IV) Estimation**:
   - Leveraged randomness in cup draws to create natural variation in opponent strength.
   - Used opponent division and previous season rank as instruments for winning and participating in cup matches.
2. **Two-Stage Least Squares (2SLS)**:
   - First stage: Predict cup participation or win based on instruments.
   - Second stage: Estimate causal effects on league performance using predicted participation/win.
3. **Robustness Checks**:
   - Tested alternative instruments like travel distance.
   - Conducted heterogeneity analysis to explore varying effects by team size and market value.

## Key Findings
- **Winning a Cup Fixture**:
  - Boosts league performance for smaller, lower-value teams due to psychological momentum.
  - No significant impact observed for larger, higher-value teams likely due to better resources for handling congestion.
- **Cup Participation**:
  - No evidence of significant effects on subsequent league performance, suggesting that fixture congestion alone does not directly harm performance.
- **Robustness**:
  - Results are consistent across different model specifications and robustness tests.

## Implications
- Smaller teams can leverage cup victories to improve league outcomes during congested periods.
- Larger teams are less affected by cup-related momentum but can strategically manage resources during fixture congestion.

## Contents
- **Data**: Pre-processed datasets and variable definitions.
- **Code**: Scripts for data preparation, model estimation, and robustness checks.
- **Figures**: Visualizations of causal effects and descriptive statistics.

## How to Use
1. Clone this repository:
   ```bash
   git clone https://github.com/jellewillekes/causal-effect-cup-football-iv-analysis.git
