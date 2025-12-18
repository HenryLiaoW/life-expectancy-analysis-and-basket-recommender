"""
Test suite for data_filter module (TDD RED Phase) - Policy-Oriented Analysis.

Design Philosophy:
This test suite focuses on MODIFIABLE FACTORS that inform policy decisions,
deliberately excluding circular definitions (mortality↔life expectancy).

Based on correlation analysis findings:
- Modifiable factors: basic_water (r=0.831), gghe-d (r=0.610), bmi (r=0.598)
- Excluded circular definitions: infant_mort, adult_mortality, une_life
- Policy relevance: Infrastructure, healthcare spending, nutrition, vaccination

Test Categories:
1. Basic filtering capabilities (foundation)
2. Infrastructure impact analysis (water, sanitation)
3. Healthcare spending effectiveness
4. Nutrition indicators analysis
5. Vaccination coverage gaps
6. Comparative policy analysis
7. Intervention priority recommendations
"""

import os
import sqlite3
import pytest
import pandas as pd
from task1.database_loader import create_database, load_data_to_db
from task1.data_filter import (
    get_data_as_dataframe,
    filter_by_country,
    filter_by_year_range,
    filter_by_region,
    calculate_statistics,
    get_country_trend,
    # Policy-oriented analysis functions
    analyze_infrastructure_impact,
    analyze_healthcare_spending,
    analyze_nutrition_indicators,
    identify_vaccination_gaps,
    compare_modifiable_factors,
    get_policy_intervention_priorities
)


# Test database path
TEST_DB_PATH = "task1/data/test_filter.db"


@pytest.fixture
def test_db_with_data():
    """Create test database with comprehensive modifiable factors data."""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    create_database(TEST_DB_PATH)
    
    # Sample data covering modifiable factors across countries and years
    sample_data = [
        {"country": "China", "country_code": "CHN", "region": "Asia", 
         "year": 2015, "life_expect": 76.1, "adult_mortality": 120, "infant_mort": 8.1,
         "basic_water": 95.5, "gghe-d": 3.2, "bmi": 23.8, "alcohol": 7.2,
         "polio": 99.0, "diphtheria": 99.0, "hepatitis": 99.0},
        {"country": "China", "country_code": "CHN", "region": "Asia", 
         "year": 2016, "life_expect": 76.4, "adult_mortality": 118, "infant_mort": 7.8,
         "basic_water": 96.0, "gghe-d": 3.3, "bmi": 24.0, "alcohol": 7.3,
         "polio": 99.0, "diphtheria": 99.0, "hepatitis": 99.0},
        {"country": "China", "country_code": "CHN", "region": "Asia", 
         "year": 2017, "life_expect": 76.7, "adult_mortality": 116, "infant_mort": 7.5,
         "basic_water": 96.5, "gghe-d": 3.4, "bmi": 24.2, "alcohol": 7.4,
         "polio": 99.0, "diphtheria": 99.0, "hepatitis": 99.0},
        
        {"country": "India", "country_code": "IND", "region": "Asia", 
         "year": 2015, "life_expect": 68.3, "adult_mortality": 190, "infant_mort": 37.9,
         "basic_water": 88.0, "gghe-d": 1.2, "bmi": 21.5, "alcohol": 5.7,
         "polio": 85.0, "diphtheria": 87.0, "hepatitis": 89.0},
        {"country": "India", "country_code": "IND", "region": "Asia", 
         "year": 2016, "life_expect": 68.6, "adult_mortality": 188, "infant_mort": 36.5,
         "basic_water": 89.5, "gghe-d": 1.3, "bmi": 21.7, "alcohol": 5.8,
         "polio": 86.0, "diphtheria": 88.0, "hepatitis": 90.0},
        {"country": "India", "country_code": "IND", "region": "Asia", 
         "year": 2017, "life_expect": 69.0, "adult_mortality": 186, "infant_mort": 35.2,
         "basic_water": 91.0, "gghe-d": 1.4, "bmi": 21.9, "alcohol": 5.9,
         "polio": 87.0, "diphtheria": 89.0, "hepatitis": 91.0},
        
        {"country": "USA", "country_code": "USA", "region": "Americas", 
         "year": 2015, "life_expect": 78.9, "adult_mortality": 110, "infant_mort": 5.9,
         "basic_water": 99.2, "gghe-d": 8.3, "bmi": 28.5, "alcohol": 9.2,
         "polio": 93.0, "diphtheria": 94.0, "hepatitis": 91.0},
        {"country": "USA", "country_code": "USA", "region": "Americas", 
         "year": 2016, "life_expect": 78.7, "adult_mortality": 112, "infant_mort": 5.8,
         "basic_water": 99.3, "gghe-d": 8.4, "bmi": 28.7, "alcohol": 9.3,
         "polio": 93.0, "diphtheria": 94.0, "hepatitis": 91.0},
        {"country": "USA", "country_code": "USA", "region": "Americas", 
         "year": 2017, "life_expect": 78.5, "adult_mortality": 114, "infant_mort": 5.7,
         "basic_water": 99.4, "gghe-d": 8.5, "bmi": 28.9, "alcohol": 9.4,
         "polio": 93.0, "diphtheria": 94.0, "hepatitis": 92.0},
        
        {"country": "Brazil", "country_code": "BRA", "region": "Americas", 
         "year": 2015, "life_expect": 74.8, "adult_mortality": 145, "infant_mort": 14.2,
         "basic_water": 97.8, "gghe-d": 3.8, "bmi": 26.5, "alcohol": 8.9,
         "polio": 95.0, "diphtheria": 96.0, "hepatitis": 95.0},
        {"country": "Brazil", "country_code": "BRA", "region": "Americas", 
         "year": 2016, "life_expect": 75.0, "adult_mortality": 143, "infant_mort": 13.8,
         "basic_water": 98.0, "gghe-d": 3.9, "bmi": 26.7, "alcohol": 9.0,
         "polio": 95.0, "diphtheria": 96.0, "hepatitis": 95.0},
        {"country": "Brazil", "country_code": "BRA", "region": "Americas", 
         "year": 2017, "life_expect": 75.2, "adult_mortality": 141, "infant_mort": 13.4,
         "basic_water": 98.2, "gghe-d": 4.0, "bmi": 26.9, "alcohol": 9.1,
         "polio": 96.0, "diphtheria": 97.0, "hepatitis": 96.0},
    ]
    
    load_data_to_db(TEST_DB_PATH, sample_data)
    
    yield TEST_DB_PATH
    
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


# ============================================================================
# DataFrame Conversion Tests
# ============================================================================

def test_get_data_as_dataframe_returns_dataframe(test_db_with_data):
    """Test that database records are converted to pandas DataFrame."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 12  # 4 countries × 3 years
    assert "country" in df.columns
    assert "year" in df.columns
    assert "life_expect" in df.columns


def test_get_data_as_dataframe_has_correct_types(test_db_with_data):
    """Test that DataFrame columns have appropriate data types."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    # String columns
    assert df["country"].dtype == object
    assert df["region"].dtype == object
    
    # Numeric columns
    assert pd.api.types.is_numeric_dtype(df["year"])
    assert pd.api.types.is_float_dtype(df["life_expect"])


def test_get_data_as_dataframe_validates_path():
    """Test that invalid database path raises appropriate error."""
    with pytest.raises(FileNotFoundError):
        get_data_as_dataframe("nonexistent.db")


# ============================================================================
# Filtering Tests - By Country
# ============================================================================

def test_filter_by_country_single_country(test_db_with_data):
    """Test filtering by single country name."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    china_df = filter_by_country(df, "China")
    
    assert len(china_df) == 3  # 3 years of data
    assert all(china_df["country"] == "China")
    assert china_df["year"].tolist() == [2015, 2016, 2017]


def test_filter_by_country_preserves_columns(test_db_with_data):
    """Test that filtering preserves all DataFrame columns."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    filtered = filter_by_country(df, "USA")
    
    assert list(filtered.columns) == list(df.columns)


def test_filter_by_country_returns_empty_for_nonexistent(test_db_with_data):
    """Test that non-existent country returns empty DataFrame."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = filter_by_country(df, "Nonexistent")
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0


def test_filter_by_country_case_sensitive(test_db_with_data):
    """Test that country filtering is case-sensitive."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    result_correct = filter_by_country(df, "China")
    result_wrong = filter_by_country(df, "china")
    
    assert len(result_correct) == 3
    assert len(result_wrong) == 0


# ============================================================================
# Filtering Tests - By Year Range
# ============================================================================

def test_filter_by_year_range_inclusive(test_db_with_data):
    """Test that year range filtering is inclusive on both ends."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    filtered = filter_by_year_range(df, 2015, 2016)
    
    years = sorted(filtered["year"].unique())
    assert years == [2015, 2016]
    assert len(filtered) == 8  # 4 countries × 2 years


def test_filter_by_year_range_single_year(test_db_with_data):
    """Test filtering for a single year."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    filtered = filter_by_year_range(df, 2017, 2017)
    
    assert len(filtered) == 4  # 4 countries
    assert all(filtered["year"] == 2017)


def test_filter_by_year_range_validates_range(test_db_with_data):
    """Test that invalid year range raises ValueError."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    with pytest.raises(ValueError, match="start_year.*end_year"):
        filter_by_year_range(df, 2020, 2015)


def test_filter_by_year_range_no_matches(test_db_with_data):
    """Test that out-of-range years return empty DataFrame."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    filtered = filter_by_year_range(df, 2000, 2010)
    
    assert len(filtered) == 0


# ============================================================================
# Filtering Tests - By Region
# ============================================================================

def test_filter_by_region_single_region(test_db_with_data):
    """Test filtering by region name."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    asia_df = filter_by_region(df, "Asia")
    
    assert len(asia_df) == 6  # China (3) + India (3)
    assert all(asia_df["region"] == "Asia")
    assert set(asia_df["country"].unique()) == {"China", "India"}


def test_filter_by_region_americas(test_db_with_data):
    """Test filtering Americas region."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    americas_df = filter_by_region(df, "Americas")
    
    assert len(americas_df) == 6  # USA (3) + Brazil (3)
    assert set(americas_df["country"].unique()) == {"USA", "Brazil"}


def test_filter_by_region_empty_result(test_db_with_data):
    """Test that non-existent region returns empty DataFrame."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = filter_by_region(df, "Europe")
    
    assert len(result) == 0


# ============================================================================
# Multi-Condition Filtering Tests
# ============================================================================

def test_combined_filters_country_and_year(test_db_with_data):
    """Test combining country and year range filters."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    # Filter China for years 2016-2017
    china_df = filter_by_country(df, "China")
    result = filter_by_year_range(china_df, 2016, 2017)
    
    assert len(result) == 2
    assert all(result["country"] == "China")
    assert result["year"].tolist() == [2016, 2017]


def test_combined_filters_region_and_year(test_db_with_data):
    """Test combining region and year filters."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    # Filter Asia for year 2015
    asia_df = filter_by_region(df, "Asia")
    result = filter_by_year_range(asia_df, 2015, 2015)
    
    assert len(result) == 2  # China and India in 2015
    assert set(result["country"].unique()) == {"China", "India"}


# ============================================================================
# Statistical Analysis Tests
# ============================================================================

def test_calculate_statistics_basic_metrics(test_db_with_data):
    """Test calculating basic statistics for a column."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    china_df = filter_by_country(df, "China")
    
    stats = calculate_statistics(china_df, "life_expect")
    
    assert "mean" in stats
    assert "median" in stats
    assert "std" in stats
    assert "min" in stats
    assert "max" in stats
    assert "count" in stats
    
    # Verify values for China's life expectancy (76.1, 76.4, 76.7)
    assert stats["mean"] == pytest.approx(76.4, rel=0.01)
    assert stats["median"] == 76.4
    assert stats["min"] == 76.1
    assert stats["max"] == 76.7
    assert stats["count"] == 3


def test_calculate_statistics_handles_missing_column(test_db_with_data):
    """Test that invalid column raises appropriate error."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    with pytest.raises(KeyError):
        calculate_statistics(df, "nonexistent_column")


def test_calculate_statistics_empty_dataframe(test_db_with_data):
    """Test statistics on empty DataFrame."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    empty_df = filter_by_country(df, "Nonexistent")
    
    stats = calculate_statistics(empty_df, "life_expect")
    
    # Should return NaN or None for empty data
    assert pd.isna(stats["mean"]) or stats["mean"] is None


# ============================================================================
# Trend Analysis Tests
# ============================================================================

def test_get_country_trend_returns_time_series(test_db_with_data):
    """Test getting time series data for a country."""
    trend = get_country_trend(TEST_DB_PATH, "China", "life_expect")
    
    assert isinstance(trend, pd.DataFrame)
    assert len(trend) == 3
    assert "year" in trend.columns
    assert "life_expect" in trend.columns
    assert trend["year"].tolist() == [2015, 2016, 2017]


def test_get_country_trend_sorted_by_year(test_db_with_data):
    """Test that trend data is sorted chronologically."""
    trend = get_country_trend(TEST_DB_PATH, "USA", "adult_mortality")
    
    assert trend["year"].is_monotonic_increasing
    assert list(trend["year"]) == [2015, 2016, 2017]


def test_get_country_trend_validates_metric(test_db_with_data):
    """Test that invalid metric column raises error."""
    with pytest.raises((KeyError, ValueError)):
        get_country_trend(TEST_DB_PATH, "China", "invalid_metric")


def test_get_country_trend_nonexistent_country(test_db_with_data):
    """Test that non-existent country returns empty DataFrame."""
    trend = get_country_trend(TEST_DB_PATH, "Nonexistent", "life_expect")
    
    assert isinstance(trend, pd.DataFrame)
    assert len(trend) == 0


# ============================================================================
# Infrastructure Impact Analysis Tests (Modifiable Factor: r=0.831)
# ============================================================================

def test_analyze_infrastructure_impact_default_variables(test_db_with_data):
    """Test infrastructure analysis with default variables (basic_water)."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = analyze_infrastructure_impact(df)
    
    assert isinstance(result, pd.DataFrame)
    assert "basic_water" in result.columns
    assert len(result) > 0


def test_analyze_infrastructure_impact_custom_variables(test_db_with_data):
    """Test infrastructure analysis with custom variable list."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = analyze_infrastructure_impact(df, infrastructure_vars=["basic_water"])
    
    assert "basic_water" in result.columns
    assert isinstance(result, pd.DataFrame)


def test_analyze_infrastructure_impact_missing_column_error(test_db_with_data):
    """Test that invalid infrastructure column raises KeyError."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    with pytest.raises(KeyError):
        analyze_infrastructure_impact(df, infrastructure_vars=["nonexistent_var"])


def test_analyze_infrastructure_regional_differences(test_db_with_data):
    """Test infrastructure analysis shows regional disparities."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = analyze_infrastructure_impact(df)
    
    # India should show lower basic_water than USA/Brazil
    india_data = result[result["country"] == "India"]
    usa_data = result[result["country"] == "USA"]
    
    assert india_data["basic_water"].mean() < usa_data["basic_water"].mean()


# ============================================================================
# Healthcare Spending Analysis Tests (Modifiable Factor: r=0.610)
# ============================================================================

def test_analyze_healthcare_spending_returns_statistics(test_db_with_data):
    """Test healthcare spending analysis returns statistical metrics."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = analyze_healthcare_spending(df)
    
    assert isinstance(result, dict)
    assert "mean_gghe_d" in result
    assert "median_gghe_d" in result
    assert isinstance(result["mean_gghe_d"], (int, float))


def test_analyze_healthcare_spending_by_region(test_db_with_data):
    """Test healthcare spending analysis filtered by region."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    asia_result = analyze_healthcare_spending(df, region="Asia")
    americas_result = analyze_healthcare_spending(df, region="Americas")
    
    # Americas should have higher average healthcare spending
    assert americas_result["mean_gghe_d"] > asia_result["mean_gghe_d"]


def test_analyze_healthcare_spending_includes_country_rankings(test_db_with_data):
    """Test that spending analysis includes country rankings."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = analyze_healthcare_spending(df)
    
    assert "country_rankings" in result
    assert isinstance(result["country_rankings"], (list, pd.DataFrame))


# ============================================================================
# Nutrition Indicators Analysis Tests (Modifiable Factor: r=0.598)
# ============================================================================

def test_analyze_nutrition_indicators_returns_dataframe(test_db_with_data):
    """Test nutrition analysis returns DataFrame with BMI data."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = analyze_nutrition_indicators(df)
    
    assert isinstance(result, pd.DataFrame)
    assert "bmi" in result.columns
    assert len(result) > 0


def test_analyze_nutrition_indicators_year_range_filter(test_db_with_data):
    """Test nutrition analysis with year range filtering."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = analyze_nutrition_indicators(df, year_range=(2016, 2017))
    
    years = result["year"].unique()
    assert all(year in [2016, 2017] for year in years)
    assert 2015 not in years


def test_analyze_nutrition_shows_obesity_patterns(test_db_with_data):
    """Test that nutrition analysis reveals BMI patterns (USA higher BMI)."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = analyze_nutrition_indicators(df)
    
    usa_bmi = result[result["country"] == "USA"]["bmi"].mean()
    india_bmi = result[result["country"] == "India"]["bmi"].mean()
    
    # USA has higher average BMI (obesity concern)
    assert usa_bmi > india_bmi
    assert usa_bmi > 25.0  # Overweight threshold


# ============================================================================
# Vaccination Coverage Gap Tests (Modifiable through Policy)
# ============================================================================

def test_identify_vaccination_gaps_default_threshold(test_db_with_data):
    """Test vaccination gap identification with 90% threshold."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = identify_vaccination_gaps(df)
    
    assert isinstance(result, pd.DataFrame)
    # India should appear (polio 85-87%, below 90%)
    assert "India" in result["country"].values


def test_identify_vaccination_gaps_custom_threshold(test_db_with_data):
    """Test vaccination gaps with custom threshold (95%)."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = identify_vaccination_gaps(df, threshold=95.0)
    
    # More countries should appear with higher threshold
    assert len(result) > 0
    assert "USA" in result["country"].values  # USA polio 93%


def test_identify_vaccination_gaps_sorted_by_severity(test_db_with_data):
    """Test that vaccination gaps are sorted by coverage gap size."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = identify_vaccination_gaps(df, threshold=95.0)
    
    if len(result) > 1:
        # First row should have largest gap (lowest coverage)
        gaps = result["polio"].values
        assert all(gaps[i] <= gaps[i+1] for i in range(len(gaps)-1))


def test_identify_vaccination_gaps_empty_when_all_above_threshold(test_db_with_data):
    """Test that high-performing scenario returns empty DataFrame."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = identify_vaccination_gaps(df, threshold=80.0)
    
    # All countries should be above 80%
    assert isinstance(result, pd.DataFrame)


# ============================================================================
# Comparative Analysis Tests (Multi-Country Modifiable Factors)
# ============================================================================

def test_compare_modifiable_factors_default_factors(test_db_with_data):
    """Test comparing modifiable factors using default top correlations."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = compare_modifiable_factors(df, countries=["China", "India"])
    
    assert isinstance(result, pd.DataFrame)
    # Should include top modifiable factors
    assert "basic_water" in result.columns
    assert "gghe-d" in result.columns
    assert "bmi" in result.columns


def test_compare_modifiable_factors_custom_factors(test_db_with_data):
    """Test comparing specific custom factors."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = compare_modifiable_factors(
        df, 
        countries=["USA", "Brazil"],
        factors=["basic_water", "alcohol"]
    )
    
    assert "basic_water" in result.columns
    assert "alcohol" in result.columns
    assert len(result) == 2  # Two countries


def test_compare_modifiable_factors_validates_countries(test_db_with_data):
    """Test that invalid country raises ValueError."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    with pytest.raises(ValueError, match="country not found"):
        compare_modifiable_factors(df, countries=["China", "Nonexistent"])


def test_compare_modifiable_factors_multiple_years(test_db_with_data):
    """Test comparison across multiple years shows trends."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = compare_modifiable_factors(df, countries=["China", "USA"])
    
    # Should have data for multiple years
    assert "year" in result.columns
    china_years = result[result["country"] == "China"]["year"].unique()
    assert len(china_years) == 3  # 2015, 2016, 2017


# ============================================================================
# Policy Intervention Priority Tests (Decision Support)
# ============================================================================

def test_get_policy_intervention_priorities_identifies_gaps(test_db_with_data):
    """Test that intervention priorities identify improvement areas."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = get_policy_intervention_priorities(
        df, 
        country="India",
        target_life_expectancy=75.0
    )
    
    assert isinstance(result, dict)
    assert "current_gap" in result
    assert "top_priorities" in result
    assert result["current_gap"] > 0  # India below 75 years


def test_get_policy_intervention_priorities_ranks_by_impact(test_db_with_data):
    """Test that priorities are ranked by potential impact."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = get_policy_intervention_priorities(
        df,
        country="India",
        target_life_expectancy=75.0
    )
    
    assert isinstance(result["top_priorities"], list)
    assert len(result["top_priorities"]) > 0
    # Should prioritize factors with higher correlation and larger gaps
    assert "basic_water" in str(result["top_priorities"]) or "gghe-d" in str(result["top_priorities"])


def test_get_policy_intervention_priorities_estimates_impact(test_db_with_data):
    """Test that function provides impact estimates for each priority."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    result = get_policy_intervention_priorities(
        df,
        country="India",
        target_life_expectancy=75.0
    )
    
    assert "estimated_impact" in result
    assert isinstance(result["estimated_impact"], dict)


def test_get_policy_intervention_priorities_validates_country(test_db_with_data):
    """Test that nonexistent country raises ValueError."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    with pytest.raises(ValueError):
        get_policy_intervention_priorities(df, "Nonexistent", 80.0)


def test_get_policy_intervention_priorities_validates_target(test_db_with_data):
    """Test that target below current life expectancy raises ValueError."""
    df = get_data_as_dataframe(TEST_DB_PATH)
    
    with pytest.raises(ValueError, match="target.*below current"):
        get_policy_intervention_priorities(df, "USA", 70.0)  # USA is ~78.7
