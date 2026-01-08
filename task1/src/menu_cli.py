"""
Interactive Menu-Driven CLI for Life Expectancy Data Pipeline System.

Designed for AI/DS teams: Access → Filter → Clean → Summarize → Present
"""

import os
import sys
import pandas as pd
from typing import Optional, Dict, Any

from task1.src.database_loader import get_all_records, create_record, update_record, delete_record
from task1.src.data_filter import filter_by_country, filter_by_region, filter_by_year_range
from task1.src.cleaner import clean_dataset
from task1.src import database_cleaner
from task1.src.logger import get_logger


class AnalysisSession:
    """Manages data pipeline state."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.original_data: Optional[pd.DataFrame] = None
        self.filtered_data: Optional[pd.DataFrame] = None
        self.cleaned_data: Optional[pd.DataFrame] = None
        self.filters: Dict[str, Any] = {}
        self.is_cleaned: bool = False
        
    def load_data(self) -> pd.DataFrame:
        """Load all data from database."""
        records = get_all_records(self.db_path)
        self.original_data = pd.DataFrame(records)
        self.filtered_data = self.original_data.copy()
        return self.original_data
    
    def apply_filter(self, **kwargs) -> pd.DataFrame:
        """Apply filters to data."""
        self.filters.update(kwargs)
        data = self.original_data.copy()
        
        if 'country' in self.filters and self.filters['country']:
            countries = self.filters['country']
            # Support both single country (str) and multiple countries (list)
            if isinstance(countries, list):
                data = data[data['country'].isin(countries)]
            else:
                data = data[data['country'] == countries]
        if 'region' in self.filters and self.filters['region']:
            data = data[data['region'] == self.filters['region']]
        if 'year_min' in self.filters:
            data = data[data['year'] >= self.filters['year_min']]
        if 'year_max' in self.filters:
            data = data[data['year'] <= self.filters['year_max']]
        
        self.filtered_data = data
        self.is_cleaned = False
        return self.filtered_data
    
    def get_current_data(self) -> pd.DataFrame:
        """Get current working dataset."""
        # Auto-load if no data exists
        if self.original_data is None:
            self.load_data()
        
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
        """Generate status bar text."""
        data = self.get_current_data()
        record_count = len(data) if data is not None else 0
        
        filter_text = "No filter"
        if self.filters:
            parts = []
            if 'country' in self.filters:
                countries = self.filters['country']
                if isinstance(countries, list):
                    if len(countries) <= 3:
                        parts.append(f"Country={', '.join(countries)}")
                    else:
                        parts.append(f"Country={len(countries)} countries")
                else:
                    parts.append(f"Country={countries}")
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
    """Print main menu header."""
    print("\n" + "="*50)
    print("Life Expectancy Data Pipeline (AI/DS Teams)")
    print("="*50)
    print(f"Status: {session.get_status_bar()}")
    print("="*50)


def print_main_menu():
    """Print menu options."""
    print("\n" + "="*50)
    print(" 1. DATA ACCESS (Database Management)")
    print("="*50)
    print("  1.1 - View database info")
    
    print("\n" + "="*50)
    print(" 2. DATA FILTERING (Query & Selection)")
    print("="*50)
    print("  2.1 - Filter by country")
    print("  2.2 - Filter by region")
    print("  2.3 - Filter by year range")
    print("  2.4 - Filter by development status (GNI-based)")
    print("  2.5 - Clear all filters")
    print("  2.6 - Preview current dataset")
    print("  2.7 - Export filtered data to CSV")
    
    print("\n" + "="*50)
    print(" 3. DATA CLEANING (Quality Control) ★")
    print("="*50)
    print("  3.1 - Create cleaned database from CSV (Pipeline Mode)")
    print("      → Uses cleaner.py to clean data during CSV import")
    print("  3.2 - Clean existing database (SQL Mode)")
    print("      → Uses SQL UPDATE to clean data in-place")
    print("  ⚠️  Both options will show Data Quality Report after cleaning")
    
    print("\n" + "="*50)
    print(" 4. DATA SUMMARIZATION (Analysis)")
    print("="*50)
    print("  4.1 - Correlation analysis")
    print("  4.2 - Country comparison")
    print("  4.3 - Statistical summary")
    print("  4.4 - Visualize trends (matplotlib)")
    print("  4.5 - Generate summary table (pandas)")
    print("  4.6 - Top improving countries (by life expectancy growth)")
    
    print("\n" + "="*50)
    print(" OTHER OPTIONS")
    print("="*50)
    print("  h - Show workflow guide")
    print("  0 - Exit")


def show_workflow_guide():
    """Display workflow guide."""
    print("\n" + "="*50)
    print("RECOMMENDED WORKFLOW FOR AI/DS TEAMS")
    print("="*50)
    print("""
Pipeline: ACCESS → FILTER → CLEAN → SUMMARIZE → PRESENT

Example:
  1. ACCESS (1.1) - View data → 12 records
  2. FILTER (2.2) - Select Asia → 9 records  
  3. CLEAN (3.4)  - Apply pipeline → 9 valid
  4. ANALYZE (4.1) - Correlations
  5. EXPORT (5.1) - Save CSV

Tip: Always filter first, then clean, then analyze!
    """)
    input("Press Enter to continue...")


def cmd_view_info(session: AnalysisSession):
    """View database info."""
    print("\n" + "="*50)
    print("DATABASE INFORMATION")
    print("="*50)
    
    data = session.get_current_data()
    
    if data is None or len(data) == 0:
        print("\n⚠️  No data loaded. Please load data first.")
        input("\nPress Enter to continue...")
        return
    
    print(f"\n📊 Dataset Overview:")
    print(f"  • Total Records: {len(data)}")
    print(f"  • Countries: {data['country'].nunique()}")
    print(f"  • Year Range: {data['year'].min()} - {data['year'].max()}")
    
    if 'life_expect' in data.columns:
        print(f"\n📈 Life Expectancy:")
        print(f"  • Range: {data['life_expect'].min():.1f} - {data['life_expect'].max():.1f} years")
        print(f"  • Average: {data['life_expect'].mean():.1f} years")
    
    input("\nPress Enter to continue...")


def cmd_filter_country(session: AnalysisSession):
    """Filter by country (supports multiple countries)."""
    print("\n" + "="*50)
    print("FILTER BY COUNTRY")
    print("="*50)
    
    # Show available countries
    data = session.get_current_data()
    countries = sorted(data['country'].unique())
    print(f"\n💡 {len(countries)} countries available")
    print("   (Enter country names separated by commas for multiple selection)")
    print("\n📋 Example: China, India, United States")
    
    country_input = input("\n🔍 Enter country name(s): ").strip()
    if country_input:
        # Split by comma and clean up whitespace
        country_list = [c.strip() for c in country_input.split(',')]
        
        # If only one country, use string; if multiple, use list
        if len(country_list) == 1:
            session.apply_filter(country=country_list[0])
            get_logger().log_filter("country", country_list[0])
            print(f"\n✅ Filtered to '{country_list[0]}': {len(session.filtered_data)} records")
        else:
            session.apply_filter(country=country_list)
            get_logger().log_filter("country", ', '.join(country_list))
            print(f"\n✅ Filtered to {len(country_list)} countries: {len(session.filtered_data)} records")
            print(f"   Countries: {', '.join(country_list)}")
    else:
        print("\n❌ No country entered")
    
    input("Press Enter to continue...")


def cmd_filter_region(session: AnalysisSession):
    """Filter by region."""
    print("\n" + "="*50)
    print("FILTER BY REGION")
    print("="*50)
    
    data = session.get_current_data()
    regions = sorted(data['region'].unique())
    print("\nAvailable regions:", ", ".join(regions))
    
    region = input("\nEnter region: ").strip()
    if region:
        session.apply_filter(region=region)
        get_logger().log_filter("region", region)
        print(f"\n✅ Filtered to {len(session.filtered_data)} records")
    else:
        print("\n❌ No region entered")
    
    input("Press Enter to continue...")


def cmd_filter_year_range(session: AnalysisSession):
    """Filter by year range."""
    print("\n" + "="*50)
    print("FILTER BY YEAR RANGE")
    print("="*50)
    
    try:
        year_min = int(input("\nStart year: ").strip())
        year_max = int(input("End year: ").strip())
        
        session.apply_filter(year_min=year_min, year_max=year_max)
        get_logger().log_filter("year_range", f"{year_min}-{year_max}")
        print(f"\n✅ Filtered to {len(session.filtered_data)} records")
    except ValueError:
        print("\n❌ Invalid year numbers")
    
    input("Press Enter to continue...")


def cmd_filter_development_status(session: AnalysisSession):
    """Filter by development status based on GNI per capita."""
    print("\n" + "="*50)
    print("FILTER BY DEVELOPMENT STATUS")
    print("="*50)
    
    current_data = session.get_current_data()
    
    # Show current filter context
    years = sorted(current_data['year'].unique())
    regions = sorted(current_data['region'].unique())
    countries = sorted(current_data['country'].unique())
    
    print(f"\n📊 Current filter status:")
    if len(years) == len(session.original_data['year'].unique()):
        print(f"   ⭕ Year range: All years ({years[0]}-{years[-1]})")
    else:
        print(f"   ✅ Year range: {years[0]}-{years[-1]} ({len(years)} years)")
    
    if len(regions) == len(session.original_data['region'].unique()):
        print(f"   ⭕ Regions: All regions ({len(regions)})")
    else:
        print(f"   ✅ Regions: {', '.join(regions)}")
    
    if len(countries) == session.original_data['country'].nunique():
        print(f"   ⭕ Countries: All countries ({len(countries)})")
    else:
        print(f"   ✅ Countries: {len(countries)} selected")
    
    print("\n💰 World Bank Income Classification (2024):")
    print("  1. High income (developed)      - GNI ≥ $14,006")
    print("  2. Upper middle income          - GNI $4,516-$14,005")
    print("  3. Lower middle income          - GNI $1,146-$4,515")
    print("  4. Low income                   - GNI ≤ $1,145")
    print("\n💡 Tip: Select multiple using commas (e.g., '1,2' or 'high,upper')")
    
    choice = input("\nSelect classification(s): ").strip()
    if not choice:
        return
    
    status_map = {
        '1': ('high', 'high income (developed)'),
        '2': ('upper-middle', 'upper middle income'),
        '3': ('lower-middle', 'lower middle income'),
        '4': ('low', 'low income'),
        'high': ('high', 'high income (developed)'),
        'high income': ('high', 'high income (developed)'),
        'upper': ('upper-middle', 'upper middle income'),
        'upper middle': ('upper-middle', 'upper middle income'),
        'lower': ('lower-middle', 'lower middle income'),
        'lower middle': ('lower-middle', 'lower middle income'),
        'low': ('low', 'low income')
    }
    
    # Parse comma-separated selections
    selections = [s.strip() for s in choice.split(',')]
    status_keys = []
    status_labels = []
    
    for sel in selections:
        choice_key = sel.lower()
        if choice_key in status_map:
            status_key, status_label = status_map[choice_key]
            if status_key not in status_keys:  # Avoid duplicates
                status_keys.append(status_key)
                status_labels.append(status_label)
        else:
            print(f"\n❌ Invalid choice: {sel}")
            input("\nPress Enter to continue...")
            return
    
    if status_keys:
        # Use list if multiple, single value if one
        filter_input = status_keys if len(status_keys) > 1 else status_keys[0]
        from task1.src.data_filter import filter_by_development_status
        
        try:
            filtered = filter_by_development_status(current_data, filter_input)
            
            # Calculate average GNI per country and sort by GNI (descending)
            country_gni = filtered.groupby('country')['gni_capita'].mean().sort_values(ascending=False)
            countries_in_category = country_gni.index.tolist()
            
            # Display results
            if len(status_labels) == 1:
                print(f"\n✅ {status_labels[0].capitalize()} countries in selected period:")
            else:
                combined_label = ', '.join(status_labels)
                print(f"\n✅ Selected classifications ({combined_label}):")
            
            print(f"   Total: {len(countries_in_category)} countries")
            print(f"   (Sorted by average GNI, highest first)\n")
            
            # Display with rank numbers for clarity
            for idx, country in enumerate(countries_in_category, 1):
                avg_gni = country_gni[country]
                print(f"   {idx:2d}. {country:<40} (avg GNI: ${avg_gni:,.0f})")
            
            # Apply filter
            session.filtered_data = filtered
            log_label = ', '.join(status_labels) if len(status_labels) > 1 else status_labels[0]
            get_logger().log_filter("development_status", log_label)
            print(f"\n📊 Result: {len(filtered)} records filtered")
            
        except ValueError as e:
            print(f"\n❌ Error: {e}")
    
    input("\n\nPress Enter to continue...")


def cmd_clear_filters(session: AnalysisSession):
    """Clear all filters."""
    session.clear_filters()
    print("\n✅ All filters cleared")
    input("Press Enter to continue...")


def cmd_preview_data(session: AnalysisSession):
    """Preview dataset with grouped column display."""
    print("\n" + "="*50)
    print("DATASET PREVIEW")
    print("="*50)
    
    data = session.get_current_data()
    print(f"\nShowing first 10 of {len(data)} records\n")
    
    # Define column groups for better readability
    # Note: 'country' is added to all groups except Basic Info for easy identification
    column_groups = {
        "📍 Basic Info": ["country", "country_code", "region", "year"],
        "❤️ Life Expectancy": ["country", "year", "life_expect", "life_exp60", "adult_mortality", "infant_mort", "age1-4mort"],
        "🏥 Health Indicators": ["country", "year", "alcohol", "bmi", "age5-19thinness", "age5-19obesity", "hepatitis", "measles"],
        "💉 Vaccination": ["country", "year", "polio", "diphtheria"],
        "🏗️ Infrastructure": ["country", "year", "basic_water", "doctors", "hospitals"],
        "💰 Economic": ["country", "year", "gni_capita", "gghe-d", "che_gdp"],
        "🌍 UNESCO Data - Demographics & Health": ["country", "year", "une_pop", "une_infant", "une_life", "une_hiv"],
        "🌍 UNESCO Data - Economic & Social": ["country", "year", "une_gni", "une_poverty", "une_edu_spend", "une_literacy", "une_school"]
    }
    
    # Sort by GNI per capita (descending) if column exists
    if 'gni_capita' in data.columns:
        data_sorted = data.sort_values('gni_capita', ascending=False)
        preview_data = data_sorted.head(10)
    else:
        preview_data = data.head(10)
    
    # Display each group separately
    for group_name, columns in column_groups.items():
        # Filter columns that exist in the dataset
        existing_cols = [col for col in columns if col in preview_data.columns]
        
        if existing_cols:
            print(f"\n{group_name}")
            print("-" * 50)
            group_df = preview_data[existing_cols]
            print(group_df.to_string(index=False))
    
    input("\n\n📌 Press Enter to continue...")


def cmd_create_cleaned_db(session: AnalysisSession):
    """Create cleaned database from CSV using cleaner.py."""
    print("\n" + "="*50)
    print("CREATE CLEANED DATABASE FROM CSV (Pipeline Mode)")
    print("="*50)
    print("\nThis will:")
    print("  1. Load CSV data")
    print("  2. Apply cleaner.py cleaning logic")
    print("  3. Create new SQLite database")
    print("  4. Show data quality report")
    print("\n💡 Cleaning rules (from cleaner.py):")
    print("  • Convert invalid numeric values to None")
    print("  • Validate year as integer")
    print("  • Keep all rows (no deletion)")
    
    # Get CSV path
    csv_path = input("\n📁 CSV file path (default: task1/data/life_expectancy.csv): ").strip()
    if not csv_path:
        csv_path = "task1/data/life_expectancy.csv"
    
    if not os.path.exists(csv_path):
        print(f"\n❌ File not found: {csv_path}")
        input("Press Enter to continue...")
        return
    
    # Get output DB path
    db_path = input("💾 Output database path (default: task1/data/cleaned_from_csv.db): ").strip()
    if not db_path:
        db_path = "task1/data/cleaned_from_csv.db"
    
    # Confirm
    print(f"\n⚠️  Will create: {db_path}")
    if os.path.exists(db_path):
        print(f"   Existing database will be replaced!")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ Cancelled")
        input("Press Enter to continue...")
        return
    
    try:
        # Import create_db module
        from task1.src.create_db import create_db_from_csv
        
        print("\n🔄 Creating cleaned database...")
        created_db = create_db_from_csv(csv_path, db_path, use_demo_data=False)
        
        print("\n✅ Database created successfully!")
        print(f"   Path: {created_db}")
        
        # Show quality report
        print("\n" + "="*50)
        print("DATA QUALITY REPORT")
        print("="*50)
        
        # Load the new database and show stats
        import sqlite3
        import pandas as pd
        
        conn = sqlite3.connect(created_db)
        df = pd.read_sql_query("SELECT * FROM life_expectancy", conn)
        conn.close()
        
        print(f"\n📊 Total Records: {len(df)}")
        print(f"   Countries: {df['country'].nunique() if 'country' in df.columns else 'N/A'}")
        print(f"   Year Range: {df['year'].min() if 'year' in df.columns else 'N/A'} - {df['year'].max() if 'year' in df.columns else 'N/A'}")
        
        print("\n🔍 Missing Values After Cleaning:")
        missing = df.isna().sum()
        for col, count in missing.items():
            if count > 0:
                print(f"   {col}: {count} ({count/len(df)*100:.1f}%)")
        
        if missing.sum() == 0:
            print("   ✅ No missing values!")
        
        get_logger().log_cleaning("CSV_PIPELINE", f"Created cleaned database: {created_db}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to continue...")


def cmd_remove_duplicates(session: AnalysisSession):
    """Remove duplicates."""
    print("\n" + "="*50)
    print("REMOVE DUPLICATES")
    print("="*50)
    
    data = session.get_current_data()
    before = len(data)
    data_cleaned = data.drop_duplicates()
    after = len(data_cleaned)
    
    if before > after:
        session.cleaned_data = data_cleaned
        session.is_cleaned = True
        print(f"\n✅ Removed {before-after} duplicates")
    else:
        print("\n✅ No duplicates found")
    
    input("Press Enter to continue...")


def cmd_quality_report(session: AnalysisSession):
    """Show quality report."""
    print("\n" + "="*50)
    print("DATA QUALITY REPORT")
    print("="*50)
    
    data = session.get_current_data()
    print(f"\n📊 Dataset: {len(data)} records")
    print(f"  • Missing values: {data.isna().sum().sum()}")
    print(f"  • Duplicates: {data.duplicated().sum()}")
    
    print(f"\n📈 Completeness:")
    completeness = (1 - data.isna().sum() / len(data)) * 100
    for col, pct in completeness.items():
        status = "✅" if pct == 100 else "⚠️"
        print(f"  {status} {col}: {pct:.1f}%")
    
    input("\nPress Enter to continue...")


def cmd_database_cleaning(session: AnalysisSession):
    """Clean database directly using SQL operations."""
    print("\n" + "="*50)
    print("DATABASE-LEVEL CLEANING (SQL-based)")
    print("="*50)
    print("\nThis will clean data directly in the database using SQL UPDATE.")
    print("Different from in-memory cleaning (3.1-3.4), this modifies the database file.")
    print("\n⚠️  WARNING: This operation will MODIFY the database!")
    print("\nCleaning operations:")
    print("  • Convert empty strings to NULL")
    print("  • Remove invalid numeric values")
    print("  • Validate year ranges")
    print("  • Remove duplicate records")
    
    # First, show what would be changed (dry run)
    print("\n🔍 Analyzing database...")
    try:
        dry_results = database_cleaner.clean_database_full(session.db_path, dry_run=True)
        database_cleaner.print_cleaning_report(dry_results)
        
        # Ask for confirmation
        print("\n⚠️  Proceed with actual cleaning? This cannot be undone! (y/n): ", end="")
        if input().lower() == 'y':
            print("\n🔄 Executing cleaning operations...")
            results = database_cleaner.clean_database_full(session.db_path, dry_run=False)
            database_cleaner.print_cleaning_report(results)
            get_logger().log_cleaning("DATABASE", f"Cleaned database: {sum(results.values())} operations")
            print("\n✅ Database cleaning completed!")
            
            # Reload data in session
            session.original_data = None
            session.filtered_data = None
            session.cleaned_data = None
            print("\n🔄 Reloading cleaned data...")
            
            # Reload and show quality report
            import pandas as pd
            import sqlite3
            conn = sqlite3.connect(session.db_path)
            df = pd.read_sql_query("SELECT * FROM life_expectancy", conn)
            conn.close()
            session.original_data = df
            
            print("\n" + "="*50)
            print("DATA QUALITY REPORT (After SQL Cleaning)")
            print("="*50)
            print(f"\n📊 Total Records: {len(df)}")
            print(f"   Countries: {df['country'].nunique() if 'country' in df.columns else 'N/A'}")
            print(f"   Year Range: {df['year'].min() if 'year' in df.columns else 'N/A'} - {df['year'].max() if 'year' in df.columns else 'N/A'}")
            
            print("\n🔍 Missing Values After Cleaning:")
            missing = df.isna().sum()
            for col, count in missing.items():
                if count > 0:
                    print(f"   {col}: {count} ({count/len(df)*100:.1f}%)")
            
            if missing.sum() == 0:
                print("   ✅ No missing values!")
        else:
            print("\n❌ Cleaning cancelled.")
    except Exception as e:
        print(f"\n❌ Error during database cleaning: {e}")
    
    input("\nPress Enter to continue...")


def cmd_correlation_analysis(session: AnalysisSession):
    """Correlation analysis."""
    print("\n" + "="*50)
    print("CORRELATION ANALYSIS")
    print("="*50)
    
    data = session.get_current_data()
    
    if len(data) < 10:
        print("\n⚠️  Need at least 10 records")
    else:
        # Show context
        countries = data['country'].unique()
        if len(countries) == 1:
            print(f"\n📍 Analysis for: {countries[0]} ({len(data)} records)")
        else:
            print(f"\n📍 Analysis scope: {len(countries)} countries, {len(data)} records")
        
        print("\n📊 Correlation with Life Expectancy:")
        corr_cols = ['life_expect', 'basic_water', 'gghe-d', 'bmi', 'alcohol']
        available = [c for c in corr_cols if c in data.columns]
        
        if len(available) > 1:
            corr = data[available].corr()['life_expect'].sort_values(ascending=False)
            for col, val in corr.items():
                if col != 'life_expect':
                    print(f"  {col:<20} r = {val:6.3f}")
        
        if len(countries) == 1:
            print("\n💡 Tip: Different countries may have different key factors.")
            print("   Clear filters (2.4) to see global correlations.")
    
    input("\nPress Enter to continue...")


def cmd_country_comparison(session: AnalysisSession):
    """Compare life expectancy statistics across countries."""
    print("\n" + "="*50)
    print("COUNTRY COMPARISON")
    print("="*50)
    print("\n💡 Compare mean/min/max life expectancy across countries")
    
    data = session.get_current_data()
    countries = sorted(data['country'].unique())
    
    print(f"\n📋 Available countries in current dataset: {len(countries)}")
    
    # Smart default behavior
    if len(countries) <= 5:
        # Auto-compare all if 5 or fewer
        print(f"   → Auto-comparing all {len(countries)} countries")
        selected = countries
    elif len(countries) <= 15:
        # Show all and let user choose
        for i, country in enumerate(countries, 1):
            print(f"   {i:2d}. {country}")
        
        print("\n💡 Options:")
        print("   • Enter country names (comma-separated): China, India")
        print("   • Enter 'top5' to compare top 5 by average life expectancy")
        print("   • Press Enter to compare all")
        
        input_str = input("\n🔍 Your choice: ").strip()
        
        if not input_str:
            selected = countries[:10]  # Limit to 10 for readability
            print(f"   → Comparing first 10 countries")
        elif input_str.lower() == 'top5':
            avg_life = data.groupby('country')['life_expect'].mean().sort_values(ascending=False)
            selected = avg_life.head(5).index.tolist()
            print(f"   → Comparing top 5 countries by life expectancy")
        else:
            selected = [c.strip() for c in input_str.split(",")]
    else:
        # Many countries - show sample and prompt
        print(f"\n   Sample: {', '.join(countries[:10])}")
        print(f"   ... and {len(countries)-10} more")
        
        print("\n💡 Options:")
        print("   • Enter country names (comma-separated): China, India, United States")
        print("   • Enter 'top5' to compare top 5 by average life expectancy")
        print("   • Enter 'random5' to compare 5 random countries")
        
        input_str = input("\n🔍 Your choice: ").strip()
        
        if input_str.lower() == 'top5':
            avg_life = data.groupby('country')['life_expect'].mean().sort_values(ascending=False)
            selected = avg_life.head(5).index.tolist()
            print(f"   → Comparing top 5 countries by life expectancy")
        elif input_str.lower() == 'random5':
            import random
            selected = random.sample(countries, min(5, len(countries)))
            print(f"   → Comparing 5 random countries")
        elif input_str:
            selected = [c.strip() for c in input_str.split(",")]
        else:
            print("\n❌ No selection made")
            input("\nPress Enter to continue...")
            return
    
    # Perform comparison
    if selected:
        comparison = data[data['country'].isin(selected)].groupby('country')['life_expect'].agg(['mean', 'min', 'max', 'count'])
        comparison = comparison.sort_values('mean', ascending=False)
        
        print("\n" + "="*70)
        print("📊 LIFE EXPECTANCY COMPARISON (sorted by mean)")
        print("="*70)
        print(f"\n{'Country':<30} {'Mean':>8} {'Min':>8} {'Max':>8} {'Years':>8}")
        print("-"*70)
        
        for country, row in comparison.iterrows():
            print(f"{country:<30} {row['mean']:>8.1f} {row['min']:>8.1f} {row['max']:>8.1f} {int(row['count']):>8}")
        
        print("="*70)
        
        # Generate visualization
        print("\n📊 Generating comparison chart...")
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            countries_list = comparison.index.tolist()
            means = comparison['mean'].values
            mins = comparison['min'].values
            maxs = comparison['max'].values
            
            x = np.arange(len(countries_list))
            width = 0.6
            
            # Bar chart with error bars
            bars = ax.bar(x, means, width, label='Mean', alpha=0.8, color='steelblue', edgecolor='navy')
            
            # Add error bars (min to max range)
            errors_low = means - mins
            errors_high = maxs - means
            ax.errorbar(x, means, yerr=[errors_low, errors_high], 
                       fmt='none', ecolor='darkred', capsize=5, alpha=0.7, linewidth=2)
            
            # Add value labels on top of bars
            for i, (bar, mean_val) in enumerate(zip(bars, means)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                       f'{mean_val:.1f}',
                       ha='center', va='bottom', fontweight='bold', fontsize=10)
            
            # Adjust Y-axis to show differences better (don't start from 0)
            y_min = min(mins) - 2
            y_max = max(maxs) + 2
            ax.set_ylim(y_min, y_max)
            
            ax.set_xlabel('Country', fontsize=12, fontweight='bold')
            ax.set_ylabel('Life Expectancy (years)', fontsize=12, fontweight='bold')
            ax.set_title('Life Expectancy Comparison (Mean with Min-Max Range)', 
                        fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(countries_list, rotation=45, ha='right', fontsize=10)
            ax.legend(loc='upper right')
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            plt.tight_layout()
            
            # Save to output folder
            import os
            output_dir = os.path.join(os.path.dirname(session.db_path), '..', 'output')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'country_comparison.png')
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            
            print(f"✅ Chart saved: {output_path}")
            
            # Show interactive window
            print("📊 Opening chart window (close window to continue)...")
            plt.show()
            
        except Exception as e:
            print(f"⚠️  Could not generate chart: {e}")
    
    input("\nPress Enter to continue...")


def cmd_statistical_summary(session: AnalysisSession):
    """Statistical summary."""
    print("\n" + "="*50)
    print("STATISTICAL SUMMARY")
    print("="*50)
    
    # Display filter context
    if session.filters:
        print("\n📌 Current Filters:")
        for key, value in session.filters.items():
            print(f"   • {key.title()}: {value}")
    else:
        print("\n📌 No filters applied (全部数据)")
    
    data = session.get_current_data()
    print(f"\n📊 Records: {len(data)}")
    if session.is_cleaned:
        print("✅ Data has been cleaned")
    
    numeric_cols = data.select_dtypes(include=['number']).columns
    
    # Display key metrics in readable format
    key_metrics = ['life_expect', 'adult_mortality', 'infant_mort', 
                   'alcohol', 'bmi', 'gdp']
    
    for metric in key_metrics:
        if metric in numeric_cols:
            stats = data[metric].describe()
            print(f"\n📊 {metric.replace('_', ' ').title()}")
            print(f"   Count: {int(stats['count']):,}")
            print(f"   Mean:  {stats['mean']:.2f}")
            print(f"   Std:   {stats['std']:.2f}")
            print(f"   Min:   {stats['min']:.2f}")
            print(f"   25%:   {stats['25%']:.2f}")
            print(f"   50%:   {stats['50%']:.2f}")
            print(f"   75%:   {stats['75%']:.2f}")
            print(f"   Max:   {stats['max']:.2f}")
    
    # Ask if user wants to export summary
    export = input("\n💾 Export summary statistics to CSV? (y/n): ").strip().lower()
    if export == 'y':
        summary_data = []
        for metric in key_metrics:
            if metric in numeric_cols:
                stats = data[metric].describe()
                summary_data.append({
                    'metric': metric,
                    'count': int(stats['count']),
                    'mean': stats['mean'],
                    'std': stats['std'],
                    'min': stats['min'],
                    '25%': stats['25%'],
                    '50%': stats['50%'],
                    '75%': stats['75%'],
                    'max': stats['max']
                })
        
        import pandas as pd
        summary_df = pd.DataFrame(summary_data)
        
        parts = []
        if 'country' in session.filters:
            parts.append(session.filters['country'])
        if 'region' in session.filters:
            parts.append(session.filters['region'])
        
        filename = f"summary_stats_{'_'.join(parts) if parts else 'all'}.csv"
        filepath = f"task1/output/{filename}"
        os.makedirs("task1/output", exist_ok=True)
        summary_df.to_csv(filepath, index=False)
        print(f"✅ Summary exported to: {filepath}")
    
    input("\nPress Enter to continue...")


def cmd_export_csv(session: AnalysisSession):
    """Export to CSV."""
    print("\n" + "="*50)
    print("EXPORT TO CSV")
    print("="*50)
    
    data = session.get_current_data()
    
    parts = []
    if 'country' in session.filters:
        parts.append(session.filters['country'])
    if 'region' in session.filters:
        parts.append(session.filters['region'])
    
    filename = f"exported_data_{'_'.join(parts) if parts else 'all'}.csv"
    filepath = f"task1/output/{filename}"
    
    os.makedirs("task1/output", exist_ok=True)
    data.to_csv(filepath, index=False)
    
    get_logger().log_export("CSV", filepath, len(data))
    print(f"\n✅ Exported {len(data)} records to:")
    print(f"   {filepath}")
    
    input("Press Enter to continue...")


def cmd_visualize_trends(session: AnalysisSession):
    """Generate matplotlib line chart for trends."""
    from task1.src.visualization import generate_life_expectancy_trend_chart
    
    data = session.get_current_data()
    if len(data) == 0:
        print("\n❌ No data to visualize")
        input("Press Enter to continue...")
        return
    
    print("\n" + "="*50)
    print("VISUALIZE TRENDS")
    print("="*50)
    
    try:
        # Delegate to visualization module
        output_path = generate_life_expectancy_trend_chart(
            data=data,
            output_path='task1/output/life_expectancy_trends.png',
            dpi=300,
            show_chart=True
        )
        
        get_logger().log_visualization("CHART", f"Life expectancy trend chart: {len(data)} records")
        print(f"\n✅ Chart saved to: {output_path}")
        
    except Exception as e:
        print(f"\n❌ Error generating chart: {e}")
    
    input("\nPress Enter to continue...")


def cmd_top_improving_countries(session: AnalysisSession):
    """Find and visualize top-k countries with fastest life expectancy improvement."""
    from task1.src.visualization import generate_life_expectancy_trend_chart
    
    print("\n" + "="*50)
    print("TOP IMPROVING COUNTRIES ANALYSIS")
    print("="*50)
    
    data = session.get_current_data()
    if len(data) == 0:
        print("\n❌ No data available")
        input("Press Enter to continue...")
        return
    
    # Check if life_expect column exists
    if 'life_expect' not in data.columns:
        print("\n❌ Life expectancy data not found")
        input("Press Enter to continue...")
        return
    
    # Display filter context
    if session.filters:
        print("\n📌 Analyzing within current filters:")
        for key, value in session.filters.items():
            print(f"   • {key.title()}: {value}")
    else:
        print("\n📌 Analyzing all countries globally")
    
    # Calculate improvement for each country
    print("\n🔄 Calculating life expectancy improvements...")
    
    improvements = []
    for country in data['country'].unique():
        country_data = data[data['country'] == country].sort_values('year')
        
        # Need at least 2 years of data
        if len(country_data) < 2:
            continue
        
        # Get earliest and latest life expectancy values
        life_values = country_data['life_expect'].dropna()
        if len(life_values) < 2:
            continue
        
        earliest_year = country_data['year'].min()
        latest_year = country_data['year'].max()
        
        earliest_life = country_data[country_data['year'] == earliest_year]['life_expect'].values[0]
        latest_life = country_data[country_data['year'] == latest_year]['life_expect'].values[0]
        
        if pd.notna(earliest_life) and pd.notna(latest_life):
            improvement = latest_life - earliest_life
            improvements.append({
                'country': country,
                'year_start': int(earliest_year),
                'year_end': int(latest_year),
                'life_start': earliest_life,
                'life_end': latest_life,
                'improvement': improvement,
                'years_span': int(latest_year - earliest_year)
            })
    
    if not improvements:
        print("\n❌ Insufficient data to calculate improvements")
        input("Press Enter to continue...")
        return
    
    # Sort by improvement (descending)
    improvements_df = pd.DataFrame(improvements).sort_values('improvement', ascending=False)
    
    print(f"\n✅ Calculated improvements for {len(improvements_df)} countries")
    
    # Ask for top-k
    try:
        k_input = input("\n📊 How many top countries to analyze? (default: 5): ").strip()
        k = int(k_input) if k_input else 5
        k = max(1, min(k, len(improvements_df)))  # Ensure valid range
    except ValueError:
        k = 5
        print("⚠️  Invalid input, using default k=5")
    
    # Get top k countries
    top_k = improvements_df.head(k)
    
    print(f"\n🏆 Top {k} Improving Countries:")
    print("=" * 80)
    for idx, row in enumerate(top_k.itertuples(), 1):
        print(f"{idx}. {row.country:25} "
              f"{row.life_start:5.1f} → {row.life_end:5.1f} years "
              f"(+{row.improvement:5.1f} over {row.years_span} years)")
    
    # Ask if user wants to visualize
    visualize = input("\n📈 Generate trend chart for these countries? (y/n): ").strip().lower()
    
    if visualize == 'y':
        # Filter data for top k countries
        top_countries = top_k['country'].tolist()
        filtered_data = data[data['country'].isin(top_countries)]
        
        try:
            output_path = generate_life_expectancy_trend_chart(
                data=filtered_data,
                output_path=f"task1/output/top_{k}_improving_countries.png"
            )
            
            print(f"\n✅ Chart saved: {output_path}")
            print("📊 Opening chart window (close window to continue)...")
            
            import matplotlib.pyplot as plt
            plt.show()
            
        except Exception as e:
            print(f"\n⚠️  Could not generate chart: {e}")
    
    # Ask if user wants to export summary
    export = input("\n💾 Export improvement summary to CSV? (y/n): ").strip().lower()
    if export == 'y':
        filename = f"top_{k}_improving_countries.csv"
        filepath = f"task1/output/{filename}"
        os.makedirs("task1/output", exist_ok=True)
        top_k.to_csv(filepath, index=False)
        print(f"✅ Summary exported to: {filepath}")
    
    input("\nPress Enter to continue...")


def cmd_summary_table(session: AnalysisSession):
    """Generate pandas summary statistics table."""
    from task1.visualization import generate_summary_table
    
    data = session.get_current_data()
    if len(data) == 0:
        print("\n❌ No data to summarize")
        input("Press Enter to continue...")
        return
    
    print("\n" + "="*50)
    print("GENERATE SUMMARY TABLE")
    print("="*50)
    
    # Display filter context
    if session.filters:
        print("\n📌 Current Filters:")
        for key, value in session.filters.items():
            print(f"   • {key.title()}: {value}")
    else:
        print("\n📌 No filters applied (全部数据)")
    
    # Smart options based on available columns
    print("\n📊 Group by options:")
    options = {}
    option_num = 1
    
    if 'country' in data.columns:
        print(f"  {option_num} - Country (compare specific countries)")
        options[str(option_num)] = 'country'
        option_num += 1
    
    if 'region' in data.columns:
        print(f"  {option_num} - Region (compare WHO regions)")
        options[str(option_num)] = 'region'
        option_num += 1
    
    if 'status' in data.columns:
        print(f"  {option_num} - Status (Developed vs Developing)")
        options[str(option_num)] = 'status'
        option_num += 1
    
    if 'year' in data.columns:
        print(f"  {option_num} - Year (time-based comparison)")
        options[str(option_num)] = 'year'
        option_num += 1
    
    if not options:
        print("\n❌ No suitable columns for grouping")
        input("Press Enter to continue...")
        return
    
    choice = input(f"\nSelect grouping (1-{len(options)}): ").strip()
    
    group_by = options.get(choice)
    
    if not group_by:
        print("\n❌ Invalid choice")
        input("Press Enter to continue...")
        return
    
    try:
        print(f"\n🔄 Generating summary table grouped by {group_by}...")
        summary_df = generate_summary_table(data, group_by=group_by)
        
        get_logger().log_visualization("TABLE", f"Summary table grouped by {group_by}: {len(data)} records")
        
        # Display in readable block format instead of wide table
        print("\n" + "="*80)
        print(f"SUMMARY TABLE - Grouped by {group_by.upper()}")
        print("="*80)
        
        # Dynamically find all mean_* columns (these are the metrics)
        mean_columns = [col for col in summary_df.columns if col.startswith('mean_')]
        metrics = [col.replace('mean_', '') for col in mean_columns]
        
        print(f"\n💡 Displaying {len(metrics)} metrics for each {group_by}")
        
        # Iterate through each group
        for idx, row in summary_df.iterrows():
            group_name = row[group_by]
            count = int(row['count']) if 'count' in row else 'N/A'
            
            print(f"\n📊 {group_name}")
            print(f"   Records: {count}")
            print("   " + "-" * 70)
            
            # Display all available metrics
            for metric in metrics:
                mean_col = f'mean_{metric}'
                min_col = f'min_{metric}'
                max_col = f'max_{metric}'
                
                if mean_col in row:
                    mean_val = row[mean_col]
                    
                    # Skip if mean is NaN
                    if pd.isna(mean_val):
                        continue
                    
                    min_val = row[min_col] if min_col in row and not pd.isna(row[min_col]) else None
                    max_val = row[max_col] if max_col in row and not pd.isna(row[max_col]) else None
                    
                    # Format metric name nicely
                    metric_display = metric.replace('_', ' ').replace('-', ' ').title()
                    if len(metric_display) > 25:
                        metric_display = metric_display[:22] + "..."
                    
                    if min_val is not None and max_val is not None:
                        print(f"   {metric_display:<28}: Mean={mean_val:>8.2f}  Range=[{min_val:.2f}, {max_val:.2f}]")
                    else:
                        print(f"   {metric_display:<28}: Mean={mean_val:>8.2f}")
        
        print("\n" + "="*80)
        
        # Ask if user wants to export summary table
        export = input("\n💾 Export summary table to CSV? (y/n): ").strip().lower()
        if export == 'y':
            parts = []
            if 'country' in session.filters:
                parts.append(session.filters['country'])
            if 'region' in session.filters:
                parts.append(session.filters['region'])
            
            filename = f"summary_table_{group_by}_{'_'.join(parts) if parts else 'all'}.csv"
            filepath = f"task1/output/{filename}"
            os.makedirs("task1/output", exist_ok=True)
            summary_df.to_csv(filepath, index=False)
            print(f"✅ Summary table exported to: {filepath}")
        
        # Show use case example
        if group_by == 'region':
            print("\n💡 Research Use Case:")
            print("   Compare health indicators across WHO regions.")
            print("   Example: 'Western Pacific region showed mean life expectancy of X years")
            print("   (range: Y-Z), compared to African region with mean of A years.'")
        elif group_by == 'status' and 'status' in data.columns:
            print("\n💡 Research Use Case:")
            print("   This table helps compare developed vs developing countries.")
            print("   Example citation: 'Developed countries showed mean life expectancy")
            print("   of XX.X years (n=XXX), compared to XX.X years in developing nations.'")
        elif group_by == 'country':
            print("\n💡 Research Use Case:")
            print("   This table provides exact statistics for cross-country comparison.")
            print("   Use mean/min/max values for precise numerical citations in reports.")
        
    except Exception as e:
        print(f"\n❌ Error generating summary table: {e}")
    
    input("\nPress Enter to continue...")


def run_menu_system(db_path: str):
    """Run interactive menu."""
    session = AnalysisSession(db_path)
    
    print("\n🔄 Loading database...")
    try:
        session.load_data()
        print(f"✅ Loaded {len(session.original_data)} records")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    while True:
        print_header(session)
        print_main_menu()
        
        choice = input("\nEnter choice: ").strip().lower()
        
        if choice == "1.1":
            cmd_view_info(session)
        elif choice == "2.1":
            cmd_filter_country(session)
        elif choice == "2.2":
            cmd_filter_region(session)
        elif choice == "2.3":
            cmd_filter_year_range(session)
        elif choice == "2.4":
            cmd_filter_development_status(session)
        elif choice == "2.5":
            cmd_clear_filters(session)
        elif choice == "2.6":
            cmd_preview_data(session)
        elif choice == "2.7":
            cmd_export_csv(session)
        elif choice == "3.1":
            cmd_create_cleaned_db(session)
        elif choice == "3.2":
            cmd_database_cleaning(session)
        elif choice == "4.1":
            cmd_correlation_analysis(session)
        elif choice == "4.2":
            cmd_country_comparison(session)
        elif choice == "4.3":
            cmd_statistical_summary(session)
        elif choice == "4.4":
            cmd_visualize_trends(session)
        elif choice == "4.5":
            cmd_summary_table(session)
        elif choice == "4.6":
            cmd_top_improving_countries(session)
        elif choice == "h":
            show_workflow_guide()
        elif choice == "0":
            print("\n👋 Thank you for using the system!\n")
            break
        else:
            print("\n❌ Invalid choice")
            input("Press Enter to continue...")


def main():
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Life Expectancy Data Pipeline")
    parser.add_argument("--db", default="task1/data/life_expectancy.db", help="Database path")
    args = parser.parse_args()
    
    if not os.path.exists(args.db):
        print(f"❌ Database not found: {args.db}")
        sys.exit(1)
    
    run_menu_system(args.db)


if __name__ == "__main__":
    main()
