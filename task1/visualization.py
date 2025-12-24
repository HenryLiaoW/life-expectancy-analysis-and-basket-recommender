"""
Data Visualization Module - Public Health Data Insights

This module provides visualization capabilities for health data analysis,
supporting policy-oriented decision making through clear visual representations.

Visualization Types:
1. Trend Analysis (Line charts for time series)
2. Comparative Analysis (Bar charts for country comparisons)
3. Correlation Analysis (Scatter plots for relationships)
4. Distribution Analysis (Histograms for data distributions)
5. Regional Analysis (Grouped bar charts)

Following SOLID Principles:
- SRP: Each function handles one specific visualization type
- OCP: Extensible for new chart types without modifying existing code
- LSP: All functions accept DataFrame input consistently
- ISP: Separate functions for different visualization needs
- DIP: Depends on abstractions (DataFrame) not concrete implementations
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List, Optional, Tuple
from pathlib import Path


def plot_country_trend(
    df: pd.DataFrame,
    country: str,
    metric: str,
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> None:
    """
    Plot time series trend for a specific country and metric.
    
    Args:
        df: DataFrame containing health data
        country: Country name to plot
        metric: Metric column to visualize (e.g., 'life_expect')
        save_path: Optional path to save the figure
        figsize: Figure size (width, height)
        
    Returns:
        None (displays or saves plot)
        
    Example:
        >>> df = get_data_as_dataframe("data.db")
        >>> plot_country_trend(df, "China", "life_expect")
    """
    # Filter data for the specified country
    country_data = df[df["country"] == country].copy()
    
    if country_data.empty:
        raise ValueError(f"No data found for country: {country}")
    
    if metric not in country_data.columns:
        raise KeyError(f"Metric '{metric}' not found in DataFrame")
    
    # Sort by year for proper line plot
    country_data = country_data.sort_values("year")
    
    # Create the plot
    plt.figure(figsize=figsize)
    plt.plot(
        country_data["year"],
        country_data[metric],
        marker='o',
        linewidth=2,
        markersize=8,
        label=country
    )
    
    # Styling
    plt.xlabel("Year", fontsize=12, fontweight='bold')
    plt.ylabel(metric.replace("_", " ").title(), fontsize=12, fontweight='bold')
    plt.title(f"{metric.replace('_', ' ').title()} Trend - {country}", 
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=10)
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_multi_country_comparison(
    df: pd.DataFrame,
    countries: List[str],
    metric: str,
    year: Optional[int] = None,
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 6)
) -> None:
    """
    Compare a metric across multiple countries using bar chart.
    
    Args:
        df: DataFrame containing health data
        countries: List of country names to compare
        metric: Metric to compare
        year: Specific year to compare (if None, uses average across all years)
        save_path: Optional path to save the figure
        figsize: Figure size (width, height)
        
    Returns:
        None (displays or saves plot)
    """
    # Filter data for specified countries
    filtered_df = df[df["country"].isin(countries)].copy()
    
    if filtered_df.empty:
        raise ValueError("No data found for specified countries")
    
    # Filter by year if specified
    if year is not None:
        filtered_df = filtered_df[filtered_df["year"] == year]
        title_suffix = f" ({year})"
    else:
        # Calculate average across all years
        filtered_df = filtered_df.groupby("country")[metric].mean().reset_index()
        title_suffix = " (Average)"
    
    # Create bar chart
    plt.figure(figsize=figsize)
    
    if year is None:
        # Use the aggregated data
        plt.bar(filtered_df["country"], filtered_df[metric], 
                color='steelblue', alpha=0.8, edgecolor='black')
    else:
        # Use year-specific data
        country_values = []
        for country in countries:
            country_data = filtered_df[filtered_df["country"] == country]
            if not country_data.empty:
                country_values.append(country_data[metric].values[0])
            else:
                country_values.append(0)
        
        plt.bar(countries, country_values, 
                color='steelblue', alpha=0.8, edgecolor='black')
    
    # Styling
    plt.xlabel("Country", fontsize=12, fontweight='bold')
    plt.ylabel(metric.replace("_", " ").title(), fontsize=12, fontweight='bold')
    plt.title(f"{metric.replace('_', ' ').title()} Comparison{title_suffix}", 
              fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_scatter_correlation(
    df: pd.DataFrame,
    x_metric: str,
    y_metric: str,
    color_by: Optional[str] = "region",
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8)
) -> None:
    """
    Create scatter plot to visualize correlation between two metrics.
    
    Args:
        df: DataFrame containing health data
        x_metric: Metric for x-axis
        y_metric: Metric for y-axis
        color_by: Column to use for color coding (e.g., 'region', 'country')
        save_path: Optional path to save the figure
        figsize: Figure size (width, height)
        
    Returns:
        None (displays or saves plot)
    """
    # Remove rows with missing values in either metric
    clean_df = df[[x_metric, y_metric, color_by]].dropna()
    
    if clean_df.empty:
        raise ValueError("No valid data for scatter plot")
    
    # Create scatter plot
    plt.figure(figsize=figsize)
    
    if color_by and color_by in clean_df.columns:
        # Color by category
        categories = clean_df[color_by].unique()
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        
        for category, color in zip(categories, colors):
            mask = clean_df[color_by] == category
            plt.scatter(
                clean_df[mask][x_metric],
                clean_df[mask][y_metric],
                label=category,
                alpha=0.6,
                s=100,
                color=color,
                edgecolor='black',
                linewidth=0.5
            )
        plt.legend(title=color_by.replace("_", " ").title(), fontsize=9)
    else:
        plt.scatter(
            clean_df[x_metric],
            clean_df[y_metric],
            alpha=0.6,
            s=100,
            color='steelblue',
            edgecolor='black',
            linewidth=0.5
        )
    
    # Add correlation coefficient
    correlation = clean_df[x_metric].corr(clean_df[y_metric])
    plt.text(
        0.05, 0.95,
        f'Correlation: {correlation:.3f}',
        transform=plt.gca().transAxes,
        fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )
    
    # Add trend line
    z = np.polyfit(clean_df[x_metric], clean_df[y_metric], 1)
    p = np.poly1d(z)
    x_line = np.linspace(clean_df[x_metric].min(), clean_df[x_metric].max(), 100)
    plt.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label='Trend')
    
    # Styling
    plt.xlabel(x_metric.replace("_", " ").title(), fontsize=12, fontweight='bold')
    plt.ylabel(y_metric.replace("_", " ").title(), fontsize=12, fontweight='bold')
    plt.title(f"{y_metric.replace('_', ' ').title()} vs {x_metric.replace('_', ' ').title()}", 
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_regional_comparison(
    df: pd.DataFrame,
    metric: str,
    aggregation: str = "mean",
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> None:
    """
    Compare metric across different regions using grouped bar chart.
    
    Args:
        df: DataFrame containing health data
        metric: Metric to compare across regions
        aggregation: Aggregation method ('mean', 'median', 'min', 'max')
        save_path: Optional path to save the figure
        figsize: Figure size (width, height)
        
    Returns:
        None (displays or saves plot)
    """
    if "region" not in df.columns:
        raise KeyError("DataFrame must contain 'region' column")
    
    # Aggregate data by region
    if aggregation == "mean":
        regional_data = df.groupby("region")[metric].mean()
    elif aggregation == "median":
        regional_data = df.groupby("region")[metric].median()
    elif aggregation == "min":
        regional_data = df.groupby("region")[metric].min()
    elif aggregation == "max":
        regional_data = df.groupby("region")[metric].max()
    else:
        raise ValueError(f"Invalid aggregation method: {aggregation}")
    
    # Create bar chart
    plt.figure(figsize=figsize)
    bars = plt.bar(
        regional_data.index,
        regional_data.values,
        color='coral',
        alpha=0.8,
        edgecolor='black'
    )
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{height:.1f}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    # Styling
    plt.xlabel("Region", fontsize=12, fontweight='bold')
    plt.ylabel(f"{aggregation.title()} {metric.replace('_', ' ').title()}", 
               fontsize=12, fontweight='bold')
    plt.title(f"{metric.replace('_', ' ').title()} by Region ({aggregation.title()})", 
              fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_distribution_histogram(
    df: pd.DataFrame,
    metric: str,
    bins: int = 20,
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> None:
    """
    Plot histogram to show distribution of a metric.
    
    Args:
        df: DataFrame containing health data
        metric: Metric to visualize distribution
        bins: Number of histogram bins
        save_path: Optional path to save the figure
        figsize: Figure size (width, height)
        
    Returns:
        None (displays or saves plot)
    """
    if metric not in df.columns:
        raise KeyError(f"Metric '{metric}' not found in DataFrame")
    
    # Remove NaN values
    data = df[metric].dropna()
    
    if data.empty:
        raise ValueError(f"No valid data for metric: {metric}")
    
    # Create histogram
    plt.figure(figsize=figsize)
    n, bins_edges, patches = plt.hist(
        data,
        bins=bins,
        color='lightgreen',
        alpha=0.7,
        edgecolor='black'
    )
    
    # Add statistics
    mean_val = data.mean()
    median_val = data.median()
    
    plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
    plt.axvline(median_val, color='blue', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
    
    # Styling
    plt.xlabel(metric.replace("_", " ").title(), fontsize=12, fontweight='bold')
    plt.ylabel("Frequency", fontsize=12, fontweight='bold')
    plt.title(f"Distribution of {metric.replace('_', ' ').title()}", 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_multi_metric_trends(
    df: pd.DataFrame,
    country: str,
    metrics: List[str],
    save_path: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 8)
) -> None:
    """
    Plot multiple metrics on the same chart for comparison (with subplots).
    
    Args:
        df: DataFrame containing health data
        country: Country name to plot
        metrics: List of metrics to visualize
        save_path: Optional path to save the figure
        figsize: Figure size (width, height)
        
    Returns:
        None (displays or saves plot)
    """
    # Filter data for the specified country
    country_data = df[df["country"] == country].copy()
    
    if country_data.empty:
        raise ValueError(f"No data found for country: {country}")
    
    # Sort by year
    country_data = country_data.sort_values("year")
    
    # Create subplots
    n_metrics = len(metrics)
    n_cols = 2
    n_rows = (n_metrics + 1) // 2
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if n_metrics > 1 else [axes]
    
    for idx, metric in enumerate(metrics):
        if metric not in country_data.columns:
            print(f"Warning: Metric '{metric}' not found, skipping...")
            continue
        
        axes[idx].plot(
            country_data["year"],
            country_data[metric],
            marker='o',
            linewidth=2,
            markersize=8,
            color=f'C{idx}'
        )
        
        axes[idx].set_xlabel("Year", fontsize=10, fontweight='bold')
        axes[idx].set_ylabel(metric.replace("_", " ").title(), fontsize=10, fontweight='bold')
        axes[idx].set_title(f"{metric.replace('_', ' ').title()}", fontsize=11, fontweight='bold')
        axes[idx].grid(True, alpha=0.3, linestyle='--')
    
    # Hide unused subplots
    for idx in range(n_metrics, len(axes)):
        axes[idx].set_visible(False)
    
    fig.suptitle(f"Multi-Metric Trends - {country}", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()


# Utility function to create output directory
def ensure_output_directory(output_dir: str = "task1/output/figures") -> Path:
    """
    Ensure output directory exists for saving figures.
    
    Args:
        output_dir: Directory path to create
        
    Returns:
        Path object of the directory
    """
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path
