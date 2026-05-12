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

from task1.config import CLEANED_LIFE_EXPECTANCY_CSV


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
    cleaned_path: str = str(CLEANED_LIFE_EXPECTANCY_CSV),
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

    # ========================================================================
    # PRIMARY PREDICTORS (low-missing group, pre-selected for analysis)
    # ========================================================================
    # NOTE: This exploratory analysis includes ALL available indicators
    # to provide a comprehensive correlation overview.
    #
    # ⚠️ CIRCULAR DEFINITIONS (correlated by definition, NOT policy-modifiable):
    #    - adult_mortality: Component of life expectancy calculation
    #    - infant_mort: Directly affects population life expectancy
    #    - age1-4mort: Early-life mortality component
    #    - life_exp60: Derived from overall life expectancy
    #
    # ✅ MODIFIABLE FACTORS (actionable through policy interventions):
    #    - basic_water: Infrastructure investment
    #    - gghe-d: Healthcare spending allocation
    #    - bmi: Nutrition and food security programs
    #    - alcohol: Public health regulations
    #
    # These circular definitions are EXCLUDED from downstream policy modules
    # (see data_filter.py: get_policy_intervention_priorities)
    
    predictors = [
        # Circular definitions (exploratory only, excluded from policy recommendations)
        "adult_mortality",      # r ≈ -0.72 (by definition)
        "infant_mort",          # r ≈ -0.81 (by definition)
        "age1-4mort",           # r ≈ -0.77 (by definition)
        "life_exp60",           # r ≈ +0.99 (derived from life_expect)
        
        # Modifiable factors (used in policy prioritization)
        "basic_water",          # r ≈ +0.83 (infrastructure)
        "gghe-d",               # r ≈ +0.61 (healthcare spending)
        "bmi",                  # r ≈ +0.60 (nutrition)
        "alcohol",              # r ≈ +0.42 (public health)
        
        # Other indicators (exploratory)
        "che_gdp",
        "une_pop",
        "une_infant",
        "une_life",
        "une_gni",
    ]
    
    # ========================================================================
    # ADDITIONAL PREDICTORS (higher missing rates, exploratory analysis)
    # Comment out this section if you only want low-missing variables
    # ========================================================================
    additional_predictors = [
        # Infrastructure-related indicators
        "doctors",        # Missing: ~43%
        "hospitals",      # Missing: ~96% (very high!)
        "gni_capita",     # Missing: ~22%
        # Health indicators
        "age5-19thinness",
        "age5-19obesity",
        "hepatitis",
        "measles",
        "polio",
        "diphtheria",
        # Socio-economic indicators
        "une_poverty",
        "une_edu_spend",
        "une_literacy",
        "une_school",
        "une_hiv",
    ]
    
    # Combine (comment out this line to use only primary predictors)
    predictors = predictors + additional_predictors

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
