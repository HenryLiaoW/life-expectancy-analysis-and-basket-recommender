"""
Correlation analysis for Task 1 (PAI Individual Assignment)

Research question:
Which health and socio-economic factors are most strongly associated
with national life expectancy (life_expect)?

This script performs:
- loading of cleaned dataset
- selection of low-missing, analytically reliable variables
- Pearson correlation analysis against life_expect
- ranked, interpretable output

This is an exploratory analysis step (EDA), not a predictive model.
"""

import csv
import math
from typing import List, Dict


# --------------------------------------------------
# Utility functions
# --------------------------------------------------
def load_cleaned_csv(path: str) -> List[Dict]:
    """Load cleaned CSV as list of dictionaries."""
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def safe_float(x):
    """Convert value to float if possible, else return None."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def pearson_corr(x_vals, y_vals):
    """
    Compute Pearson correlation coefficient manually.
    Uses only pairs where both values are present.
    """
    pairs = [(x, y) for x, y in zip(x_vals, y_vals) if x is not None and y is not None]
    if len(pairs) < 2:
        return None

    xs, ys = zip(*pairs)
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)

    num = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))

    if den_x == 0 or den_y == 0:
        return None

    return num / (den_x * den_y)


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
    
    Methodology:
        - Pearson correlation coefficient (measures linear association)
        - Hand-implemented algorithm (no external libraries per assignment constraints)
        - Automatic handling of missing values (None pairs are excluded)
        - Results sorted by absolute correlation strength
    
    SOLID Principles:
        - Single Responsibility: This function only coordinates correlation analysis
        - Open/Closed: Adding new predictors only requires updating the list
        - Dependency Inversion: Uses pearson_corr abstraction
    
    Args:
        cleaned_path (str): Path to cleaned CSV file (output from pipeline)
        
    Returns:
        list[tuple]: List of (variable_name, correlation_coefficient) tuples,
                     sorted by absolute correlation strength (strongest first)
                     
    Example Output:
        Correlation with life_expect (sorted by strength):
        
        infant_mort          : -0.812
        adult_mortality      : -0.723
        bmi                  : 0.561
        ...
        
    Note:
        This is exploratory data analysis (EDA), NOT predictive modeling.
        Correlation does not imply causation.
    """
    rows = load_cleaned_csv(cleaned_path)

    # Target variable
    target = "life_expect"

    # Candidate predictors (low-missing group, pre-selected)
    predictors = [
        "adult_mortality",
        "infant_mort",
        "age1-4mort",
        "bmi",
        "alcohol",
        "basic_water",
        "gghe-d",
        "che_gdp",
        "une_pop",
        "une_infant",
        "une_life",
        "une_gni",
        "life_exp60",  # included but discussed as highly correlated by definition
    ]

    # Extract target values
    y_vals = [safe_float(r.get(target)) for r in rows]

    results = []

    for var in predictors:
        x_vals = [safe_float(r.get(var)) for r in rows]
        corr = pearson_corr(x_vals, y_vals)

        if corr is not None:
            results.append((var, corr))

    # Sort by absolute correlation strength
    results.sort(key=lambda x: abs(x[1]), reverse=True)

    # Output
    print("\nCorrelation with life_expect (sorted by strength):\n")
    for var, corr in results:
        print(f"{var:20s} : {corr:.3f}")

    return results


# --------------------------------------------------
# Script entry point
# --------------------------------------------------
if __name__ == "__main__":
    run_correlation_analysis()
