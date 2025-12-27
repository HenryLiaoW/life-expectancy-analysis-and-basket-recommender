"""
Test suite for data_filter module (TDD RED Phase).

This module tests data filtering and statistical analysis using pandas.
Tests define the expected behavior before implementation.

Key functionalities to test:
- Converting database records to pandas DataFrame
- Filtering by country, year range, and region
- Statistical calculations (mean, median, trend analysis)
- Multi-condition filtering
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
    get_country_trend
)


# Test database path
TEST_DB_PATH = "task1/data/test_filter.db"


@pytest.fixture
def test_db_with_data():
    """Create test database with sample health data."""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    create_database(TEST_DB_PATH)
    
    # Sample data covering multiple countries, years, and regions
    sample_data = [
        {"country": "China", "country_code": "CHN", "region": "Asia", 
         "year": 2015, "life_expect": 76.1, "adult_mortality": 120, "infant_mort": 8.1},
        {"country": "China", "country_code": "CHN", "region": "Asia", 
         "year": 2016, "life_expect": 76.4, "adult_mortality": 118, "infant_mort": 7.8},
        {"country": "China", "country_code": "CHN", "region": "Asia", 
         "year": 2017, "life_expect": 76.7, "adult_mortality": 116, "infant_mort": 7.5},
        
        {"country": "India", "country_code": "IND", "region": "Asia", 
         "year": 2015, "life_expect": 68.3, "adult_mortality": 190, "infant_mort": 37.9},
        {"country": "India", "country_code": "IND", "region": "Asia", 
         "year": 2016, "life_expect": 68.6, "adult_mortality": 188, "infant_mort": 36.5},
        {"country": "India", "country_code": "IND", "region": "Asia", 
         "year": 2017, "life_expect": 69.0, "adult_mortality": 186, "infant_mort": 35.2},
        
        {"country": "USA", "country_code": "USA", "region": "Americas", 
         "year": 2015, "life_expect": 78.9, "adult_mortality": 110, "infant_mort": 5.9},
        {"country": "USA", "country_code": "USA", "region": "Americas", 
         "year": 2016, "life_expect": 78.7, "adult_mortality": 112, "infant_mort": 5.8},
        {"country": "USA", "country_code": "USA", "region": "Americas", 
         "year": 2017, "life_expect": 78.5, "adult_mortality": 114, "infant_mort": 5.7},
        
        {"country": "Brazil", "country_code": "BRA", "region": "Americas", 
         "year": 2015, "life_expect": 74.8, "adult_mortality": 145, "infant_mort": 14.2},
        {"country": "Brazil", "country_code": "BRA", "region": "Americas", 
         "year": 2016, "life_expect": 75.0, "adult_mortality": 143, "infant_mort": 13.8},
        {"country": "Brazil", "country_code": "BRA", "region": "Americas", 
         "year": 2017, "life_expect": 75.2, "adult_mortality": 141, "infant_mort": 13.4},
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
