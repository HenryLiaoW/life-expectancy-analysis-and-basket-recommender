"""
Data Filter Module

This module provides data filtering and statistical analysis functionality
using pandas DataFrames. It connects database queries with data analysis.

Key Features:
- Convert database records to pandas DataFrame
- Filter data by country, year range, and region
- Calculate statistical metrics
- Analyze time series trends

Following SOLID Principles:
- SRP: Focused on data filtering and statistics
- OCP: Extensible for new filter types
- DIP: Works with any DataFrame, not coupled to specific database
"""

import pandas as pd
from typing import List, Dict, Any, Optional


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
    pass


def filter_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Filter DataFrame by country name.
    
    Args:
        df: Input DataFrame
        country: Country name (case-sensitive)
        
    Returns:
        Filtered DataFrame containing only specified country
    """
    pass


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
    pass


def filter_by_region(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Filter DataFrame by region name.
    
    Args:
        df: Input DataFrame
        region: Region name
        
    Returns:
        Filtered DataFrame containing only specified region
    """
    pass


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
    pass


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
    pass
