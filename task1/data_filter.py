"""
Data Filter Module - Policy-Oriented Health Data Analysis

This module provides data filtering and statistical analysis focused on
**modifiable factors** that can inform public health policy interventions.

Based on correlation analysis findings:
- Modifiable factors: basic_water (r=0.831), gghe-d (r=0.610), bmi (r=0.598)
- Circular definitions excluded: infant_mort, adult_mortality (correlation by definition)

Key Features:
- Basic data filtering (country, year range, region)
- Infrastructure impact analysis (water access, sanitation)
- Healthcare spending effectiveness analysis
- Nutritional indicators analysis (BMI, food security)
- Vaccination coverage gap identification

Following SOLID Principles:
- SRP: Focused on policy-relevant data analysis
- OCP: Extensible for new modifiable factors
- DIP: Works with any DataFrame, not coupled to specific database
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
from . import database_loader


def get_data_as_dataframe(db_path: str) -> pd.DataFrame:
    """
    Load all health data from database into pandas DataFrame.
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        DataFrame with all records
        
    Raises:
        FileNotFoundError: If database doesn't exist
    """
    if not Path(db_path).exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    
    records = database_loader.get_all_records(db_path)
    return pd.DataFrame(records)


def get_country_list(db_path: str) -> List[str]:
    """
    Get list of all unique countries in the database.
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        Sorted list of country names
        
    Raises:
        FileNotFoundError: If database doesn't exist
    """
    df = get_data_as_dataframe(db_path)
    return sorted(df["country"].unique().tolist())


def filter_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Filter DataFrame by country name.
    
    Args:
        df: Input DataFrame
        country: Country name (case-sensitive)
        
    Returns:
        Filtered DataFrame containing only specified country
    """
    return df[df["country"] == country]


def filter_by_year_range(df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Filter DataFrame by year range (inclusive).
    
    Args:
        df: Input DataFrame
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)
        
    Returns:
        Filtered DataFrame within year range
        
    Raises:
        ValueError: If start_year > end_year
    """
    if start_year > end_year:
        raise ValueError(f"start_year ({start_year}) cannot be greater than end_year ({end_year})")
    
    return df[(df["year"] >= start_year) & (df["year"] <= end_year)]


def filter_by_region(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Filter DataFrame by region name.
    
    Args:
        df: Input DataFrame
        region: Region name
        
    Returns:
        Filtered DataFrame containing only specified region
    """
    return df[df["region"] == region]


def calculate_statistics(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Calculate statistical metrics for a column.
    
    Args:
        df: Input DataFrame
        column: Column name to analyze
        
    Returns:
        Dictionary with keys: mean, median, std, min, max, count
        
    Raises:
        KeyError: If column doesn't exist
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame")
    
    series = df[column].dropna()  # Remove missing values
    
    return {
        "mean": float(series.mean()),
        "median": float(series.median()),
        "std": float(series.std()),
        "min": float(series.min()),
        "max": float(series.max()),
        "count": int(series.count())
    }


def get_country_trend(db_path: str, country: str, metric: str) -> pd.DataFrame:
    """
    Get time series trend for a specific country and metric.
    
    Args:
        db_path: Path to SQLite database
        country: Country name
        metric: Metric column name (e.g., 'life_expect')
        
    Returns:
        DataFrame with year and metric columns, sorted by year
        
    Raises:
        KeyError: If metric column doesn't exist
        ValueError: If metric is invalid
    """
    df = get_data_as_dataframe(db_path)
    
    if metric not in df.columns:
        raise KeyError(f"Metric column '{metric}' not found")
    
    country_df = filter_by_country(df, country)
    
    # Return empty DataFrame if country not found (don't raise)
    if country_df.empty: 
        return pd.DataFrame(columns=["year", metric])
        # 之前是 raise ValueError(f"Country '{country}' not found in database")
        # 改为返回空的DataFrame，方便调用方处理无数据情况。且不会中断程序执行。
    result = country_df[["year", metric]].sort_values("year")
    return result.reset_index(drop=True)


# ============================================================================
# Policy-Oriented Analysis Functions (Modifiable Factors)
# ============================================================================

def analyze_water_access_impact(
    df: pd.DataFrame, 
    water_vars: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Analyze water access impact on life expectancy.
    
    Focus on drinking water access as key modifiable factor:
    - basic_water: Population using at least basic drinking-water services (r=0.831)
    
    Note: Dataset only contains basic_water as water infrastructure indicator.
          No sanitation_services or other infrastructure data available.
    
    Args:
        df: Input DataFrame
        water_vars: List of water access columns to analyze.
                   Defaults to ['basic_water'] (only available column)
    
    Returns:
        DataFrame with water access metrics and life_expect for analysis
    
    Raises:
        KeyError: If required columns don't exist
    """
    if water_vars is None:
        # Use basic_water (only available water infrastructure indicator)
        water_vars = ["basic_water"] if "basic_water" in df.columns else []
    
    # Check columns exist
    missing_cols = [col for col in water_vars if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Columns not found: {missing_cols}")
    
    # Return filtered DataFrame with requested columns
    result_cols = ["country", "year", "region", "life_expect"] + water_vars
    result_cols = [col for col in result_cols if col in df.columns]
    
    return df[result_cols].copy()


def analyze_healthcare_spending(
    df: pd.DataFrame,
    region: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze healthcare spending effectiveness (gghe-d correlation r=0.610).
    
    Examines:
    - gghe-d: General government health expenditure as % of GDP
    - che_gdp: Current health expenditure as % of GDP
    - une_hiv: HIV incidence per 1000 uninfected
    
    Args:
        df: Input DataFrame
        region: Optional region filter for regional analysis
    
    Returns:
        Dictionary with spending statistics and health outcome correlations
    """
    if region:
        df = filter_by_region(df, region)
    
    results = {"region": region if region else "Global"}
    
    # Calculate statistics for gghe-d
    if "gghe-d" in df.columns:
        clean_df = df[["gghe-d", "life_expect"]].dropna()
        if len(clean_df) > 0:
            results["mean_gghe_d"] = float(clean_df["gghe-d"].mean())
            results["median_gghe_d"] = float(clean_df["gghe-d"].median())
            results["correlation_gghe_d"] = float(clean_df["gghe-d"].corr(clean_df["life_expect"]))
    
    # Add country rankings
    if len(df) > 0 and "gghe-d" in df.columns:
        rankings = df.groupby("country")["gghe-d"].mean().sort_values(ascending=False)
        results["country_rankings"] = rankings.reset_index().to_dict('records')
    
    return results


def analyze_nutrition_indicators(
    df: pd.DataFrame,
    year_range: Optional[tuple] = None
) -> pd.DataFrame:
    """
    Analyze nutrition-related modifiable factors.
    
    Focus on:
    - bmi: Average Body Mass Index (r=0.598)
    - une_pop: Population undernourishment prevalence
    - wasting: Wasting prevalence in children
    
    Args:
        df: Input DataFrame
        year_range: Optional (start_year, end_year) tuple for temporal analysis
    
    Returns:
        DataFrame with nutrition indicators and trends
    """
    if year_range:
        df = filter_by_year_range(df, year_range[0], year_range[1])
    
    nutrition_vars = ["bmi", "une_pop", "wasting"]
    
    # Return filtered DataFrame with nutrition columns
    result_cols = ["country", "year", "region", "life_expect"] + [v for v in nutrition_vars if v in df.columns]
    result_cols = [col for col in result_cols if col in df.columns]
    
    return df[result_cols].copy()


def identify_vaccination_gaps(
    df: pd.DataFrame,
    threshold: float = 90.0
) -> pd.DataFrame:
    """
    Identify countries with vaccination coverage below policy threshold.
    
    Vaccination indicators (modifiable through policy):
    - polio: Polio immunization coverage (%)
    - diphtheria: Diphtheria immunization coverage (%)
    - hepatitis_b: Hepatitis B immunization coverage (%)
    
    Args:
        df: Input DataFrame
        threshold: Minimum acceptable coverage percentage (default: 90%)
    
    Returns:
        DataFrame with countries below threshold, sorted by gap size
    """
    vacc_vars = ["polio", "diphtheria", "hepatitis"]
    
    # Filter rows where ANY vaccine is below threshold
    mask = pd.Series([False] * len(df), index=df.index)
    for var in vacc_vars:
        if var in df.columns:
            mask = mask | (df[var] < threshold)
    
    result = df[mask].copy()
    
    # Sort by average vaccine coverage (lowest first)
    if not result.empty and any(v in result.columns for v in vacc_vars):
        available_vacc = [v for v in vacc_vars if v in result.columns]
        result["avg_coverage"] = result[available_vacc].mean(axis=1)
        result = result.sort_values("avg_coverage")
        result = result.drop(columns=["avg_coverage"])
    
    return result.reset_index(drop=True)


def compare_modifiable_factors(
    df: pd.DataFrame,
    countries: List[str],
    factors: Optional[List[str]] = None,
    include_all_years: bool = False
) -> pd.DataFrame:
    """
    Compare modifiable factors across multiple countries.
    
    Default factors (based on correlation analysis):
    - basic_water (r=0.831)
    - gghe-d (r=0.610)
    - bmi (r=0.598)
    - alcohol (r=0.400)
    
    Args:
        df: Input DataFrame
        countries: List of country names to compare
        factors: Optional list of factor columns. Uses top correlations if None.
        include_all_years: If True, return all years; if False, return only latest year per country
    
    Returns:
        DataFrame with comparative analysis across countries
        
    Raises:
        ValueError: If any country not found in data
    """
    if factors is None:
        factors = ["basic_water", "gghe-d", "bmi", "alcohol"]
    
    # Check all countries exist
    available_countries = df["country"].unique()
    missing = [c for c in countries if c not in available_countries]
    if missing:
        raise ValueError(f"country not found: {', '.join(missing)}")
    
    # Filter to requested countries
    mask = df["country"].isin(countries)
    result = df[mask].copy()
    
    # If not including all years, get only the latest year for each country
    if not include_all_years:
        result = result.sort_values("year", ascending=False).groupby("country").first().reset_index()
    
    columns_to_keep = ["country", "year"] + [f for f in factors if f in df.columns]
    
    return result[columns_to_keep].reset_index(drop=True)


def get_policy_intervention_priorities(
    df: pd.DataFrame,
    country: str,
    target_life_expectancy: float
) -> Dict[str, Any]:
    """
    Recommend policy intervention priorities based on modifiable factors.
    
    Analyzes gap between current state and target, then recommends
    which modifiable factors to prioritize for maximum impact.
    
    Args:
        df: Input DataFrame
        country: Target country name
        target_life_expectancy: Desired life expectancy goal
    
    Returns:
        Dictionary with:
        - current_gap: Years below target
        - top_priorities: List of factors to improve (sorted by impact)
        - estimated_impact: Projected improvement from addressing each factor
        
    Raises:
        ValueError: If country not found or target is below current value
    """
    country_df = filter_by_country(df, country)
    
    if country_df.empty:
        raise ValueError(f"Country '{country}' not found in database")
    
    # Get most recent data
    latest = country_df.sort_values("year", ascending=False).iloc[0]
    current_life_expect = latest["life_expect"]
    
    if target_life_expectancy <= current_life_expect:
        raise ValueError(f"target below current life expectancy (current: {current_life_expect})")
    
    current_gap = target_life_expectancy - current_life_expect
    
    # Analyze modifiable factors (based on correlation strength)
    factors = [
        {"name": "basic_water", "correlation": 0.831},
        {"name": "gghe-d", "correlation": 0.610},
        {"name": "bmi", "correlation": 0.598}
    ]
    
    priorities = []
    estimated_impact_dict = {}
    
    for factor in factors:
        if factor["name"] in latest and pd.notna(latest[factor["name"]]):
            # Simple estimation: correlation * gap * factor
            estimated_impact = abs(factor["correlation"]) * current_gap * 0.1
            estimated_impact_dict[factor["name"]] = round(estimated_impact, 2)
            priorities.append({
                "factor": factor["name"],
                "current_value": float(latest[factor["name"]]),
                "correlation": factor["correlation"],
                "estimated_impact_years": round(estimated_impact, 2)
            })
    
    priorities.sort(key=lambda x: x["estimated_impact_years"], reverse=True)
    
    return {
        "country": country,
        "current_life_expectancy": float(current_life_expect),
        "target_life_expectancy": target_life_expectancy,
        "current_gap": round(current_gap, 2),
        "top_priorities": priorities,
        "estimated_impact": estimated_impact_dict
    }
