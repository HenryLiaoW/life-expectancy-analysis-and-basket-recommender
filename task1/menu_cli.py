"""
Interactive Menu-Driven CLI for Life Expectancy Data Pipeline System.

This module provides a user-friendly menu interface for AI/DS teams to:
- Access: Database management and CRUD operations
- Filter: Query and select data subsets
- Clean: Data quality control and validation
- Summarize: Statistical analysis and correlation
- Present: Visualization and export

Author: Suhang Liao
Date: December 2025
"""

import os
import sys
import pandas as pd
from typing import Optional, Dict, Any, List

# Import existing modules
from task1.database_loader import (
    create_database,
    get_all_records,
    get_records_by_country,
    get_records_by_year_range,
    create_record,
    update_record,
    delete_record,
)
from task1.data_filter import (
    filter_by_country,
    filter_by_region,
    filter_by_year_range,
    get_country_trend,
)
from task1.cleaner import clean_dataset
from task1.analysis_correlation import run_correlation_analysis


class AnalysisSession:
    """
    Manages the state of an analysis session.
    
    Tracks filtered data, cleaning status, and analysis results to support
    a complete data pipeline workflow: Access → Filter → Clean → Summarize → Present
    """
    
    def __init__(self, db_path: str):
        """
        Initialize a new analysis session.
        
        Args:
            db_path: Path to the SQLite database
        """
        self.db_path = db_path
        self.original_data: Optional[pd.DataFrame] = None
        self.filtered_data: Optional[pd.DataFrame] = None
        self.cleaned_data: Optional[pd.DataFrame] = None
        self.filters: Dict[str, Any] = {}
        self.is_cleaned: bool = False
        self.last_analysis: Optional[Dict[str, Any]] = None
        
    def load_data(self) -> pd.DataFrame:
        """Load all data from database into DataFrame."""
        records = get_all_records(self.db_path)
        self.original_data = pd.DataFrame(records)
        self.filtered_data = self.original_data.copy()
        return self.original_data
    
    def apply_filter(self, **kwargs) -> pd.DataFrame:
        """
        Apply filters to the data.
        
        Args:
            **kwargs: Filter criteria (country, region, year_min, year_max)
            
        Returns:
            Filtered DataFrame
        """
        self.filters.update(kwargs)
        
        # Start with original data
        data = self.original_data.copy()
        
        # Apply filters
        if 'country' in self.filters and self.filters['country']:
            data = data[data['country'] == self.filters['country']]
        
        if 'region' in self.filters and self.filters['region']:
            data = data[data['region'] == self.filters['region']]
        
        if 'year_min' in self.filters and self.filters['year_min']:
            data = data[data['year'] >= self.filters['year_min']]
        
        if 'year_max' in self.filters and self.filters['year_max']:
            data = data[data['year'] <= self.filters['year_max']]
        
        self.filtered_data = data
        self.is_cleaned = False  # Reset cleaning status when filters change
        return self.filtered_data
    
    def get_current_data(self) -> pd.DataFrame:
        """
        Get the current working dataset.
        
        Returns cleaned data if available, otherwise filtered data,
        otherwise original data.
        """
        if self.cleaned_data is not None and self.is_cleaned:
            return self.cleaned_data
        elif self.filtered_data is not None:
            return self.filtered_data
        else:
            return self.original_data
    
    def clear_filters(self):
        """Reset all filters."""
        self.filters = {}
        self.filtered_data = self.original_data.copy()
        self.is_cleaned = False
    
    def get_status_bar(self) -> str:
        """
        Generate status bar text showing current session state.
        
        Returns:
            Formatted status string
        """
        data = self.get_current_data()
        record_count = len(data) if data is not None else 0
        
        filter_text = "No filter"
        if self.filters:
            parts = []
            if 'country' in self.filters:
                parts.append(f"Country={self.filters['country']}")
            if 'region' in self.filters:
                parts.append(f"Region={self.filters['region']}")
            if 'year_min' in self.filters or 'year_max' in self.filters:
                y_min = self.filters.get('year_min', '?')
                y_max = self.filters.get('year_max', '?')
                parts.append(f"Year={y_min}-{y_max}")
            filter_text = ", ".join(parts)
        
        clean_status = "Cleaned ✓" if self.is_cleaned else "Not cleaned"
        
        return f"[{filter_text}] | Records: {record_count} | {clean_status}"


def print_header(session: AnalysisSession):
    """Print the main menu header with status."""
    print("\n" + "="*55)
    print("  Life Expectancy Data Pipeline System")
    print("="*55)
    print(f"  Status: {session.get_status_bar()}")
    print("="*55)


def print_main_menu():
    """Print the main menu options."""
    print("\n" + "="*55)
    print(" 1. DATA ACCESS (Database Management)")
    print("="*55)
    print("  1.1 - View database info & statistics")
    print("  1.2 - Create new record (Interactive)")
    print("  1.3 - Update existing record")
    print("  1.4 - Delete record")
    
    print("\n" + "="*55)
    print(" 2. DATA FILTERING (Query & Selection)")
    print("="*55)
    print("  2.1 - Filter by country")
    print("  2.2 - Filter by region")
    print("  2.3 - Filter by year range")
    print("  2.4 - Clear all filters")
    print("  2.5 - Preview current dataset")
    
    print("\n" + "="*55)
    print(" 3. DATA CLEANING (Quality Control) ★")
    print("="*55)
    print("  3.1 - Handle missing values")
    print("  3.2 - Remove duplicate records")
    print("  3.3 - Validate data integrity")
    print("  3.4 - Show data quality report")
    print("  3.5 - Apply full cleaning pipeline")
    print("\n  ⚠️  Cleaning applies to current filtered data")
    
    print("\n" + "="*55)
    print(" 4. DATA SUMMARIZATION (Analysis & Aggregation)")
    print("="*55)
    print("  4.1 - Correlation analysis")
    print("  4.2 - Country comparison")
    print("  4.3 - Statistical summary")
    print("  4.4 - Policy recommendations")
    
    print("\n" + "="*55)
    print(" 5. DATA PRESENTATION (Visualization & Export)")
    print("="*55)
    print("  5.1 - Export current data to CSV")
    print("  5.2 - Generate visualization")
    print("  5.3 - Generate full report")
    
    print("\n" + "="*55)
    print(" OTHER OPTIONS")
    print("="*55)
    print("  h - Show workflow guide (recommended pipeline)")
    print("  0 - Exit system")


def show_workflow_guide():
    """Display the recommended data pipeline workflow."""
    print("\n" + "="*55)
    print("  RECOMMENDED WORKFLOW FOR AI/DS TEAMS")
    print("="*55)
    print("""
DATA PIPELINE WORKFLOW:

  [ACCESS] --> [FILTER] --> [CLEAN] --> [SUMMARIZE] --> [PRESENT]
  (Load DB)   (Select)    (Quality)    (Analysis)      (Export)

EXAMPLE WORKFLOW:
  Step 1: ACCESS (1.1) - View database info → 12 records
  Step 2: FILTER (2.2) - Select Region=Asia → 9 records
  Step 3: FILTER (2.3) - Add Year range 2015-2020 → 9 records
  Step 4: CLEAN (3.5)  - Apply full cleaning → 9 valid records
  Step 5: ANALYZE (4.1) - Run correlation analysis
  Step 6: EXPORT (5.1) - Save to cleaned_asia_2015-2020.csv

TIP: Always filter first, then clean, then analyze!
    """)
    input("Press Enter to continue...")


def run_menu_system(db_path: str = "task1/data/life_expectancy.db"):
    """
    Run the interactive menu system.
    
    Args:
        db_path: Path to the database file
    """
    # Initialize session
    session = AnalysisSession(db_path)
    
    print("\n🔄 Loading database...")
    try:
        session.load_data()
        print(f"✅ Loaded {len(session.original_data)} records from database")
    except Exception as e:
        print(f"❌ Error loading database: {e}")
        return
    
    # Main menu loop
    while True:
        print_header(session)
        print_main_menu()
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        # Data Access section
        if choice == "1.1":
            cmd_view_info(session)
        elif choice == "1.2":
            cmd_create_record_menu(session)
        elif choice == "1.3":
            cmd_update_record_menu(session)
        elif choice == "1.4":
            cmd_delete_record_menu(session)
        
        # Data Filtering section
        elif choice == "2.1":
            cmd_filter_country(session)
        elif choice == "2.2":
            cmd_filter_region(session)
        elif choice == "2.3":
            cmd_filter_year_range(session)
        elif choice == "2.4":
            cmd_clear_filters(session)
        elif choice == "2.5":
            cmd_preview_data(session)
        
        # Data Cleaning section
        elif choice == "3.1":
            cmd_handle_missing(session)
        elif choice == "3.2":
            cmd_remove_duplicates(session)
        elif choice == "3.3":
            cmd_validate_data(session)
        elif choice == "3.4":
            cmd_quality_report(session)
        elif choice == "3.5":
            cmd_full_cleaning(session)
        
        # Data Summarization section
        elif choice == "4.1":
            cmd_correlation_analysis(session)
        elif choice == "4.2":
            cmd_country_comparison(session)
        elif choice == "4.3":
            cmd_statistical_summary(session)
        elif choice == "4.4":
            cmd_policy_recommendations(session)
        
        # Data Presentation section
        elif choice == "5.1":
            cmd_export_csv(session)
        elif choice == "5.2":
            cmd_generate_visualization(session)
        elif choice == "5.3":
            cmd_generate_report(session)
        
        # Other options
        elif choice == "h":
            show_workflow_guide()
        elif choice == "0":
            print("\n👋 Thank you for using the Life Expectancy Data Pipeline System!")
            print("   Designed for AI and Data Science Teams\n")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")
            input("Press Enter to continue...")


# ============================================================================
# Section 1: Data Access Commands
# ============================================================================

def cmd_view_info(session: AnalysisSession):
    """Display database information and statistics."""
    print("\n" + "="*70)
    print("  DATABASE INFORMATION")
    print("="*70)
    
    data = session.get_current_data()
    
    print(f"\n📊 Dataset Overview:")
    print(f"  • Total Records: {len(data)}")
    print(f"  • Countries: {data['country'].nunique()}")
    print(f"  • Regions: {data['region'].nunique() if 'region' in data.columns else 'N/A'}")
    print(f"  • Year Range: {data['year'].min()} - {data['year'].max()}")
    
    if 'life_expect' in data.columns:
        print(f"\n📈 Life Expectancy:")
        print(f"  • Range: {data['life_expect'].min():.1f} - {data['life_expect'].max():.1f} years")
        print(f"  • Average: {data['life_expect'].mean():.1f} years")
        print(f"  • Missing values: {data['life_expect'].isna().sum()}")
    
    print(f"\n🌍 Top 5 Countries (Latest Year):")
    latest_year = data['year'].max()
    latest_data = data[data['year'] == latest_year].sort_values('life_expect', ascending=False).head(5)
    for _, row in latest_data.iterrows():
        print(f"  {row['country']:<20} {row['life_expect']:.1f} years")
    
    input("\nPress Enter to continue...")


def cmd_create_record_menu(session: AnalysisSession):
    """Create a new record interactively."""
    print("\n" + "="*70)
    print("  CREATE NEW RECORD")
    print("="*70)
    print("\n📋 Required fields: country, year, region, life_expect")
    print("   Optional fields will be prompted after.\n")
    
    # This will be implemented similar to the existing CLI create command
    print("⚠️  Feature available in command-line mode:")
    print("   python task1/cli.py --db <path> create")
    input("\nPress Enter to continue...")


def cmd_update_record_menu(session: AnalysisSession):
    """Update an existing record."""
    print("\n⚠️  Feature available in command-line mode:")
    print("   python task1/cli.py --db <path> update")
    input("\nPress Enter to continue...")


def cmd_delete_record_menu(session: AnalysisSession):
    """Delete a record."""
    print("\n⚠️  Feature available in command-line mode:")
    print("   python task1/cli.py --db <path> delete")
    input("\nPress Enter to continue...")


# ============================================================================
# Section 2: Data Filtering Commands
# ============================================================================

def cmd_filter_country(session: AnalysisSession):
    """Filter data by country."""
    print("\n" + "="*70)
    print("  FILTER BY COUNTRY")
    print("="*70)
    
    country = input("\nEnter country name: ").strip()
    if country:
        session.apply_filter(country=country)
        print(f"\n✅ Filtered to {len(session.filtered_data)} records for {country}")
    else:
        print("\n❌ No country entered.")
    
    input("Press Enter to continue...")


def cmd_filter_region(session: AnalysisSession):
    """Filter data by region."""
    print("\n" + "="*70)
    print("  FILTER BY REGION")
    print("="*70)
    
    data = session.get_current_data()
    regions = sorted(data['region'].unique())
    
    print("\nAvailable regions:")
    for i, region in enumerate(regions, 1):
        print(f"  {i}. {region}")
    
    region = input("\nEnter region name: ").strip()
    if region:
        session.apply_filter(region=region)
        print(f"\n✅ Filtered to {len(session.filtered_data)} records for {region}")
    else:
        print("\n❌ No region entered.")
    
    input("Press Enter to continue...")


def cmd_filter_year_range(session: AnalysisSession):
    """Filter data by year range."""
    print("\n" + "="*70)
    print("  FILTER BY YEAR RANGE")
    print("="*70)
    
    try:
        year_min = input("\nEnter start year: ").strip()
        year_max = input("Enter end year: ").strip()
        
        if year_min and year_max:
            session.apply_filter(year_min=int(year_min), year_max=int(year_max))
            print(f"\n✅ Filtered to {len(session.filtered_data)} records for years {year_min}-{year_max}")
        else:
            print("\n❌ Invalid year range.")
    except ValueError:
        print("\n❌ Please enter valid year numbers.")
    
    input("Press Enter to continue...")


def cmd_clear_filters(session: AnalysisSession):
    """Clear all filters."""
    session.clear_filters()
    print("\n✅ All filters cleared. Showing full dataset.")
    input("Press Enter to continue...")


def cmd_preview_data(session: AnalysisSession):
    """Preview the current dataset."""
    print("\n" + "="*70)
    print("  DATASET PREVIEW")
    print("="*70)
    
    data = session.get_current_data()
    
    print(f"\nShowing first 10 records out of {len(data)} total:\n")
    print(data.head(10).to_string())
    
    input("\n\nPress Enter to continue...")


# ============================================================================
# Section 3: Data Cleaning Commands
# ============================================================================

def cmd_handle_missing(session: AnalysisSession):
    """Handle missing values in the dataset."""
    print("\n" + "="*70)
    print("  HANDLE MISSING VALUES")
    print("="*70)
    
    data = session.get_current_data()
    
    print("\nMissing values per column:")
    missing = data.isna().sum()
    for col, count in missing.items():
        if count > 0:
            print(f"  {col}: {count} ({count/len(data)*100:.1f}%)")
    
    if missing.sum() == 0:
        print("\n✅ No missing values found!")
        input("Press Enter to continue...")
        return
    
    print("\nOptions:")
    print("  1. Remove rows with missing values")
    print("  2. Fill with mean (numeric columns)")
    print("  0. Cancel")
    
    choice = input("\nChoice: ").strip()
    
    if choice == "1":
        before = len(data)
        data_cleaned = data.dropna()
        after = len(data_cleaned)
        session.cleaned_data = data_cleaned
        session.is_cleaned = True
        print(f"\n✅ Removed {before - after} rows. {after} records remain.")
    elif choice == "2":
        # Fill numeric columns with mean
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        data_cleaned = data.copy()
        for col in numeric_cols:
            data_cleaned[col].fillna(data_cleaned[col].mean(), inplace=True)
        session.cleaned_data = data_cleaned
        session.is_cleaned = True
        print("\n✅ Missing values filled with column means.")
    
    input("Press Enter to continue...")


def cmd_remove_duplicates(session: AnalysisSession):
    """Remove duplicate records."""
    print("\n" + "="*70)
    print("  REMOVE DUPLICATES")
    print("="*70)
    
    data = session.get_current_data()
    before = len(data)
    
    data_cleaned = data.drop_duplicates()
    after = len(data_cleaned)
    duplicates = before - after
    
    if duplicates > 0:
        session.cleaned_data = data_cleaned
        session.is_cleaned = True
        print(f"\n✅ Removed {duplicates} duplicate records.")
    else:
        print("\n✅ No duplicates found!")
    
    input("Press Enter to continue...")


def cmd_validate_data(session: AnalysisSession):
    """Validate data integrity."""
    print("\n" + "="*70)
    print("  DATA VALIDATION")
    print("="*70)
    
    data = session.get_current_data()
    
    print("\nValidating data ranges...")
    issues = []
    
    # Validate life expectancy
    if 'life_expect' in data.columns:
        invalid = data[(data['life_expect'] < 40) | (data['life_expect'] > 100)]
        if len(invalid) > 0:
            issues.append(f"Life expectancy out of range (40-100): {len(invalid)} records")
    
    # Validate BMI
    if 'bmi' in data.columns:
        invalid = data[(data['bmi'] < 10) | (data['bmi'] > 50)]
        if len(invalid) > 0:
            issues.append(f"BMI out of range (10-50): {len(invalid)} records")
    
    # Validate percentages
    for col in ['basic_water', 'polio', 'diphtheria']:
        if col in data.columns:
            invalid = data[(data[col] < 0) | (data[col] > 100)]
            if len(invalid) > 0:
                issues.append(f"{col} out of range (0-100): {len(invalid)} records")
    
    if not issues:
        print("\n✅ All data passed validation!")
    else:
        print(f"\n⚠️  Found {len(issues)} validation issues:")
        for issue in issues:
            print(f"  • {issue}")
    
    input("\nPress Enter to continue...")


def cmd_quality_report(session: AnalysisSession):
    """Show comprehensive data quality report."""
    print("\n" + "="*70)
    print("  DATA QUALITY REPORT")
    print("="*70)
    
    data = session.get_current_data()
    
    print(f"\n📊 Dataset: {len(data)} records")
    print(f"  • Missing values: {data.isna().sum().sum()}")
    print(f"  • Duplicate rows: {data.duplicated().sum()}")
    
    if 'life_expect' in data.columns:
        valid_life = data['life_expect'].between(40, 100).sum()
        print(f"  • Valid life expectancy (40-100): {valid_life}/{len(data)}")
    
    print(f"\n📈 Completeness by column:")
    completeness = (1 - data.isna().sum() / len(data)) * 100
    for col, pct in completeness.items():
        status = "✅" if pct == 100 else "⚠️"
        print(f"  {status} {col}: {pct:.1f}%")
    
    input("\nPress Enter to continue...")


def cmd_full_cleaning(session: AnalysisSession):
    """Apply full cleaning pipeline."""
    print("\n" + "="*70)
    print("  FULL CLEANING PIPELINE")
    print("="*70)
    
    data = session.get_current_data()
    print(f"\nStarting with {len(data)} records...")
    
    print("\n1️⃣ Removing duplicates...")
    data = data.drop_duplicates()
    print(f"   → {len(data)} records")
    
    print("\n2️⃣ Handling missing values (filling with mean)...")
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        data[col].fillna(data[col].mean(), inplace=True)
    print(f"   → {len(data)} records")
    
    print("\n3️⃣ Standardizing region names...")
    if 'region' in data.columns:
        data['region'] = data['region'].str.strip().str.title()
    print(f"   → {len(data)} records")
    
    print("\n4️⃣ Validating data...")
    issues_count = 0
    if 'life_expect' in data.columns:
        issues_count += len(data[(data['life_expect'] < 40) | (data['life_expect'] > 100)])
    print(f"   → {issues_count} validation issues")
    
    session.cleaned_data = data
    session.is_cleaned = True
    
    print(f"\n✅ Cleaning complete! Final dataset: {len(data)} records")
    input("Press Enter to continue...")


# ============================================================================
# Section 4: Data Summarization Commands
# ============================================================================

def cmd_correlation_analysis(session: AnalysisSession):
    """Perform correlation analysis."""
    print("\n" + "="*70)
    print("  CORRELATION ANALYSIS")
    print("="*70)
    
    data = session.get_current_data()
    
    if len(data) < 10:
        print("\n⚠️  Need at least 10 records for correlation analysis.")
        input("Press Enter to continue...")
        return
    
    print("\nAnalyzing correlations with life expectancy...")
    print("\nAvailable factors:")
    print("  1. Basic water access")
    print("  2. Health expenditure (gghe-d)")
    print("  3. BMI")
    print("  4. Alcohol consumption")
    
    # Calculate correlations
    corr_cols = ['life_expect', 'basic_water', 'gghe-d', 'bmi', 'alcohol']
    available_cols = [col for col in corr_cols if col in data.columns]
    
    if len(available_cols) > 1:
        corr_matrix = data[available_cols].corr()
        print(f"\n📊 Correlation with Life Expectancy:")
        life_corr = corr_matrix['life_expect'].sort_values(ascending=False)
        for col, value in life_corr.items():
            if col != 'life_expect':
                print(f"  {col:<20} r = {value:6.3f}")
    
    input("\nPress Enter to continue...")


def cmd_country_comparison(session: AnalysisSession):
    """Compare countries."""
    print("\n" + "="*70)
    print("  COUNTRY COMPARISON")
    print("="*70)
    
    data = session.get_current_data()
    countries = sorted(data['country'].unique())
    
    print(f"\nAvailable countries: {len(countries)}")
    print(", ".join(countries[:10]))
    if len(countries) > 10:
        print(f"... and {len(countries) - 10} more")
    
    print("\nEnter 2-5 countries to compare (comma-separated):")
    input_str = input("Countries: ").strip()
    
    if input_str:
        selected = [c.strip() for c in input_str.split(",")]
        comparison = data[data['country'].isin(selected)].groupby('country')['life_expect'].agg(['mean', 'min', 'max'])
        print("\n📊 Comparison:")
        print(comparison)
    
    input("\nPress Enter to continue...")


def cmd_statistical_summary(session: AnalysisSession):
    """Show statistical summary."""
    print("\n" + "="*70)
    print("  STATISTICAL SUMMARY")
    print("="*70)
    
    data = session.get_current_data()
    print("\n" + data.describe().to_string())
    
    input("\nPress Enter to continue...")


def cmd_policy_recommendations(session: AnalysisSession):
    """Generate policy recommendations."""
    print("\n⚠️  Feature under development")
    input("Press Enter to continue...")


# ============================================================================
# Section 5: Data Presentation Commands
# ============================================================================

def cmd_export_csv(session: AnalysisSession):
    """Export current dataset to CSV."""
    print("\n" + "="*70)
    print("  EXPORT TO CSV")
    print("="*70)
    
    data = session.get_current_data()
    
    # Generate filename
    filter_parts = []
    if 'country' in session.filters:
        filter_parts.append(session.filters['country'])
    if 'region' in session.filters:
        filter_parts.append(session.filters['region'])
    
    filename = f"exported_data_{'_'.join(filter_parts) if filter_parts else 'all'}.csv"
    filepath = f"task1/output/{filename}"
    
    # Ensure output directory exists
    os.makedirs("task1/output", exist_ok=True)
    
    data.to_csv(filepath, index=False)
    print(f"\n✅ Exported {len(data)} records to: {filepath}")
    
    input("Press Enter to continue...")


def cmd_generate_visualization(session: AnalysisSession):
    """Generate visualizations."""
    print("\n⚠️  Feature available via visualization.py module")
    input("Press Enter to continue...")


def cmd_generate_report(session: AnalysisSession):
    """Generate comprehensive report."""
    print("\n⚠️  Feature under development")
    input("Press Enter to continue...")


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    """Main entry point for the menu system."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Life Expectancy Data Pipeline - Interactive Menu System"
    )
    parser.add_argument(
        "--db",
        default="task1/data/life_expectancy.db",
        help="Path to database file"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.db):
        print(f"❌ Error: Database file not found: {args.db}")
        sys.exit(1)
    
    run_menu_system(args.db)


if __name__ == "__main__":
    main()
