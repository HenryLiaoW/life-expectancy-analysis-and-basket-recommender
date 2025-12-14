"""
Correlation analysis for Task 1 (PAI Individual Assignment)

Research question:
Which health and socio-economic factors are most strongly associated
with national life expectancy (life_expect)?

This script will perform:
- loading of cleaned dataset
- selection of low-missing, analytically reliable variables
- Pearson correlation analysis against life_expect
- ranked, interpretable output

This is an exploratory analysis step (EDA), not a predictive model.

NOTE: This is a stub file for TDD RED phase.
      Tests should FAIL until implementation is complete.
"""

import csv
from typing import List, Dict


# --------------------------------------------------
# Utility functions
# --------------------------------------------------
def load_cleaned_csv(path: str) -> List[Dict]:
    """Load cleaned CSV as list of dictionaries."""
    # TODO: Implement CSV loading
    pass


def safe_float(x):
    """Convert value to float if possible, else return None."""
    # TODO: Implement safe float conversion
    pass


def pearson_corr(x_vals, y_vals):
    """
    Compute Pearson correlation coefficient manually.
    Uses only pairs where both values are present.
    """
    # TODO: Implement Pearson correlation formula
    pass


# --------------------------------------------------
# Main analysis
# --------------------------------------------------
def run_correlation_analysis(
    cleaned_path: str = "task1/data/life_expectancy_cleaned.csv",
):
    """
    Compute Pearson correlation between life expectancy and health/socioeconomic factors.
    
    Research Question:
        Which factors are most strongly associated with national life expectancy?
    
    Args:
        cleaned_path (str): Path to cleaned CSV file (output from pipeline)
        
    Returns:
        list[tuple]: List of (variable_name, correlation_coefficient) tuples,
                     sorted by absolute correlation strength (strongest first)
    """
    # TODO: Implement correlation analysis workflow
    pass


# --------------------------------------------------
# Script entry point
# --------------------------------------------------
if __name__ == "__main__":
    run_correlation_analysis()
