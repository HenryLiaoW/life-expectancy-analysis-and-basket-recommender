"""
Visualization module for life expectancy data analysis.

This module provides chart generation functionality following the Single 
Responsibility Principle - it handles only visualization logic, not UI or 
data loading concerns.

Design principles:
- Pure functions with clear inputs/outputs
- No side effects except file I/O
- Comprehensive error handling
- Type hints for clarity
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Optional


def generate_life_expectancy_trend_chart(
    data: pd.DataFrame,
    output_path: str = "task1/output/life_expectancy_trends.png",
    dpi: int = 300,
    show_chart: bool = False
) -> str:
    """
    Generate a line chart showing life expectancy trends over time.
    
    Creates a multi-line chart where each country's life expectancy is
    plotted as a separate line with markers, showing progression over years.
    
    Design rationale:
    - Accepts DataFrame (not database path) for separation of concerns
    - Returns file path for verification in tests
    - show_chart parameter allows both interactive and automated use
    
    Args:
        data: DataFrame containing at minimum: 'country', 'year', 'life_expect' columns
        output_path: Where to save the PNG file
        dpi: Image resolution (300 = publication quality)
        show_chart: Whether to display interactively (False for tests)
        
    Returns:
        Absolute path to the generated PNG file
        
    Raises:
        ValueError: If data is None, empty, or missing required columns
        OSError: If unable to create output directory or write file
        
    Example:
        >>> df = pd.DataFrame({
        ...     'country': ['China', 'China'],  
        ...     'year': [2015, 2016],
        ...     'life_expect': [76.0, 76.5]
        ... })
        >>> path = generate_life_expectancy_trend_chart(df, show_chart=False)
        >>> assert os.path.exists(path)
    """
    # Input validation - fail fast
    if data is None:
        raise ValueError("Data cannot be None")
    
    if len(data) == 0:
        raise ValueError("Data cannot be empty")
    
    # Check required columns
    required_cols = ['country', 'year', 'life_expect']
    missing = [col for col in required_cols if col not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Count unique countries to adjust figure size
    num_countries = data['country'].nunique()
    
    # Dynamic figure sizing based on number of countries
    if num_countries <= 5:
        figsize = (12, 7)
    elif num_countries <= 10:
        figsize = (14, 8)
    elif num_countries <= 20:
        figsize = (16, 10)
    else:
        # For many countries, increase height significantly
        figsize = (18, 12)
    
    # Create figure with professional dimensions
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot each country as a separate line
    for country in data['country'].unique():
        country_data = data[data['country'] == country].sort_values('year')
        
        # Skip empty subsets
        if len(country_data) == 0:
            continue
            
        ax.plot(
            country_data['year'],
            country_data['life_expect'],
            marker='o',
            linewidth=2,
            markersize=6,
            label=country,
            alpha=0.8  # Slight transparency for overlapping lines
        )
    
    # Professional styling
    ax.set_xlabel('Year', fontsize=13, fontweight='bold')
    ax.set_ylabel('Life Expectancy (years)', fontsize=13, fontweight='bold')
    ax.set_title(
        f'Life Expectancy Trends Over Time ({num_countries} countries)',
        fontsize=15,
        fontweight='bold',
        pad=20
    )
    
    # Legend placement - adaptive based on number of countries
    if num_countries <= 10:
        # Few countries - legend inside plot area
        ax.legend(loc='best', fontsize=10, framealpha=0.9)
    elif num_countries <= 20:
        # Moderate - smaller font, more columns
        ax.legend(loc='best', fontsize=8, framealpha=0.9, ncol=2)
    else:
        # Many countries - legend outside plot area on the right
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', 
                 fontsize=7, framealpha=0.9, ncol=1)
    
    # Grid for easier reading
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Tight layout to avoid label cutoff
    plt.tight_layout()
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:  # Only create if there's a directory component
        os.makedirs(output_dir, exist_ok=True)
    
    # Save with high quality
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    
    # Display if requested
    if show_chart:
        plt.show()
    else:
        plt.close(fig)  # Explicitly close to free memory
    
    # Return absolute path for verification
    return os.path.abspath(output_path)


def generate_summary_table(
    data: pd.DataFrame,
    group_by: str = 'country',
    metrics: Optional[list] = None
) -> pd.DataFrame:
    """
    Generate a summary statistics table using pandas.
    
    Creates a formatted table showing key statistics (mean, min, max, count)
    grouped by a specified column. This provides a complementary view to
    charts, showing exact numerical values.
    
    Args:
        data: DataFrame containing life expectancy data
        group_by: Column name to group by (default: 'country')
        metrics: List of columns to summarize (if None, auto-select numeric)
        
    Returns:
        DataFrame with summary statistics (mean, min, max, count)
        
    Raises:
        ValueError: If data is None, empty, or group_by column missing
        
    Example:
        >>> df = pd.DataFrame({
        ...     'country': ['China', 'China', 'India'],
        ...     'year': [2015, 2016, 2015],
        ...     'life_expect': [76.0, 76.5, 68.3]
        ... })
        >>> summary = generate_summary_table(df, group_by='country')
        >>> print(summary.columns)
        Index(['count', 'mean_life_expect', 'min_life_expect', 'max_life_expect'], dtype='object')
    """
    # Input validation
    if data is None:
        raise ValueError("Data cannot be None")
    
    if len(data) == 0:
        raise ValueError("Data cannot be empty")
    
    if group_by not in data.columns:
        raise ValueError(f"Group by column '{group_by}' not found in data")
    
    # Auto-select numeric columns if not specified
    if metrics is None:
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        
        # Use all numeric columns except the grouping column itself and 'year' (unless grouping by year)
        metrics = [col for col in numeric_cols 
                  if col != group_by and (col != 'year' or group_by == 'year')]
        
        # Sort metrics: prioritize common health indicators first, then alphabetically
        priority_order = ['life_expect', 'adult_mortality', 'infant_mort', 'bmi', 'alcohol']
        priority = [m for m in priority_order if m in metrics]
        others = sorted([m for m in metrics if m not in priority_order])
        metrics = priority + others
    
    # Generate summary statistics
    summary_data = []
    
    for name, group in data.groupby(group_by):
        row = {group_by: name, 'count': len(group)}
        
        for metric in metrics:
            if metric in group.columns:
                row[f'mean_{metric}'] = group[metric].mean()
                row[f'min_{metric}'] = group[metric].min()
                row[f'max_{metric}'] = group[metric].max()
        
        summary_data.append(row)
    
    # Create DataFrame
    summary_df = pd.DataFrame(summary_data)
    
    # Sort by group_by column
    summary_df = summary_df.sort_values(group_by)
    
    # Round numeric values for readability
    numeric_columns = summary_df.select_dtypes(include=['float64']).columns
    summary_df[numeric_columns] = summary_df[numeric_columns].round(2)
    
    return summary_df


# Additional visualization functions could be added here following same pattern
# e.g., generate_bar_chart(), generate_heatmap(), etc.
