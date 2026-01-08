"""
Interactive Menu-Driven CLI for Life Expectancy Data Pipeline System.

Designed for AI/DS teams: Access → Filter → Clean → Summarize → Present
"""

import os
import sys
import pandas as pd
from typing import Optional, Dict, Any

from task1.database_loader import get_all_records, create_record, update_record, delete_record
from task1.data_filter import filter_by_country, filter_by_region, filter_by_year_range
from task1.cleaner import clean_dataset
from task1 import database_cleaner
from task1.logger import get_logger


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
            data = data[data['country'] == self.filters['country']]
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
    print("  2.4 - Clear all filters")
    print("  2.5 - Preview current dataset")
    
    print("\n" + "="*50)
    print(" 3. DATA CLEANING (Quality Control) ★")
    print("="*50)
    print("  3.1 - Handle missing values")
    print("  3.2 - Remove duplicates")
    print("  3.3 - Data quality report")
    print("  3.4 - Apply full cleaning pipeline (in-memory)")
    print("  3.5 - Clean database directly (SQL-based) 🆕")
    print("  ⚠️  3.1-3.4 apply to filtered data, 3.5 modifies database")
    
    print("\n" + "="*50)
    print(" 4. DATA SUMMARIZATION (Analysis)")
    print("="*50)
    print("  4.1 - Correlation analysis")
    print("  4.2 - Country comparison")
    print("  4.3 - Statistical summary")
    
    print("\n" + "="*50)
    print(" 5. DATA PRESENTATION (Export & Visualization)")
    print("="*50)
    print("  5.1 - Export current data to CSV")
    print("  5.2 - Visualize trends (matplotlib)")
    print("  5.3 - Generate summary table (pandas)")
    
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
    """Filter by country."""
    print("\n" + "="*50)
    print("FILTER BY COUNTRY")
    print("="*50)
    
    country = input("\nEnter country name: ").strip()
    if country:
        session.apply_filter(country=country)
        get_logger().log_filter("country", country)
        print(f"\n✅ Filtered to {len(session.filtered_data)} records")
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
        "🌍 UNESCO Data": ["country", "year", "une_pop", "une_infant", "une_life", "une_hiv", "une_gni", 
                          "une_poverty", "une_edu_spend", "une_literacy", "une_school"]
    }
    
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


def cmd_handle_missing(session: AnalysisSession):
    """Handle missing values."""
    print("\n" + "="*50)
    print("HANDLE MISSING VALUES")
    print("="*50)
    
    data = session.get_current_data()
    missing = data.isna().sum()
    
    print("\nMissing values:")
    for col, count in missing.items():
        if count > 0:
            print(f"  {col}: {count}")
    
    if missing.sum() == 0:
        print("\n✅ No missing values!")
    else:
        choice = input("\n1=Remove rows, 2=Fill mean, 0=Cancel: ")
        if choice == "1":
            data_cleaned = data.dropna()
            session.cleaned_data = data_cleaned
            session.is_cleaned = True
            print(f"\n✅ Removed {len(data)-len(data_cleaned)} rows")
        elif choice == "2":
            data_cleaned = data.copy()
            for col in data.select_dtypes(include=['float64', 'int64']).columns:
                data_cleaned[col].fillna(data_cleaned[col].mean(), inplace=True)
            session.cleaned_data = data_cleaned
            session.is_cleaned = True
            print("\n✅ Filled with means")
    
    input("Press Enter to continue...")


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
            print("\n🔄 Session data cleared. Use option 1.1 to reload.")
        else:
            print("\n❌ Cleaning cancelled.")
    except Exception as e:
        print(f"\n❌ Error during database cleaning: {e}")
    
    input("\nPress Enter to continue...")


def cmd_full_cleaning(session: AnalysisSession):
    """Apply full cleaning to in-memory data."""
    print("\n" + "="*50)
    print("FULL CLEANING PIPELINE (In-Memory)")
    print("="*50)
    
    data = session.get_current_data()
    print(f"\nStarting: {len(data)} records")
    
    print("\n1️⃣ Removing duplicates...")
    data = data.drop_duplicates()
    print(f"   → {len(data)} records")
    
    print("\n2️⃣ Handling missing values...")
    for col in data.select_dtypes(include=['float64', 'int64']).columns:
        data[col].fillna(data[col].mean(), inplace=True)
    print(f"   → {len(data)} records")
    
    print("\n3️⃣ Standardizing...")
    if 'region' in data.columns:
        data['region'] = data['region'].str.strip().str.title()
    print(f"   → {len(data)} records")
    
    session.cleaned_data = data
    session.is_cleaned = True
    
    get_logger().log_cleaning("PIPELINE", f"In-memory cleaning: {len(data)} records cleaned")
    print(f"\n✅ Complete! {len(data)} records")
    input("Press Enter to continue...")


def cmd_correlation_analysis(session: AnalysisSession):
    """Correlation analysis."""
    print("\n" + "="*50)
    print("CORRELATION ANALYSIS")
    print("="*50)
    
    data = session.get_current_data()
    
    if len(data) < 10:
        print("\n⚠️  Need at least 10 records")
    else:
        print("\n📊 Correlation with Life Expectancy:")
        corr_cols = ['life_expect', 'basic_water', 'gghe-d', 'bmi', 'alcohol']
        available = [c for c in corr_cols if c in data.columns]
        
        if len(available) > 1:
            corr = data[available].corr()['life_expect'].sort_values(ascending=False)
            for col, val in corr.items():
                if col != 'life_expect':
                    print(f"  {col:<20} r = {val:6.3f}")
    
    input("\nPress Enter to continue...")


def cmd_country_comparison(session: AnalysisSession):
    """Country comparison."""
    print("\n" + "="*50)
    print("COUNTRY COMPARISON")
    print("="*50)
    
    data = session.get_current_data()
    countries = sorted(data['country'].unique())
    
    print(f"\nAvailable: {', '.join(countries[:10])}")
    if len(countries) > 10:
        print(f"... and {len(countries)-10} more")
    
    input_str = input("\nEnter countries (comma-separated): ")
    if input_str:
        selected = [c.strip() for c in input_str.split(",")]
        comparison = data[data['country'].isin(selected)].groupby('country')['life_expect'].agg(['mean', 'min', 'max'])
        print("\n📊 Comparison:")
        print(comparison)
    
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
    from task1.visualization import generate_life_expectancy_trend_chart
    
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
    
    print("\n📊 Group by options:")
    print("  1 - Country (compare specific countries)")
    print("  2 - Status (Developed vs Developing)")
    print("  3 - Year (time-based comparison)")
    
    choice = input("\nSelect grouping (1-3): ").strip()
    
    group_by_map = {
        '1': 'country',
        '2': 'status',
        '3': 'year'
    }
    
    group_by = group_by_map.get(choice)
    
    if not group_by:
        print("\n❌ Invalid choice")
        input("Press Enter to continue...")
        return
    
    if group_by not in data.columns:
        print(f"\n❌ Column '{group_by}' not found in data")
        input("Press Enter to continue...")
        return
    
    try:
        print(f"\n🔄 Generating summary table grouped by {group_by}...")
        summary_df = generate_summary_table(data, group_by=group_by)
        
        get_logger().log_visualization("TABLE", f"Summary table grouped by {group_by}: {len(data)} records")
        print("\n" + "="*80)
        print(f"SUMMARY TABLE - Grouped by {group_by.upper()}")
        print("="*80)
        print(summary_df.to_string(index=False))
        print("\n" + "="*80)
        
        # Show use case example
        if group_by == 'status' and 'status' in data.columns:
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
            cmd_clear_filters(session)
        elif choice == "2.5":
            cmd_preview_data(session)
        elif choice == "3.1":
            cmd_handle_missing(session)
        elif choice == "3.2":
            cmd_remove_duplicates(session)
        elif choice == "3.3":
            cmd_quality_report(session)
        elif choice == "3.4":
            cmd_full_cleaning(session)
        elif choice == "3.5":
            cmd_database_cleaning(session)
        elif choice == "4.1":
            cmd_correlation_analysis(session)
        elif choice == "4.2":
            cmd_country_comparison(session)
        elif choice == "4.3":
            cmd_statistical_summary(session)
        elif choice == "5.1":
            cmd_export_csv(session)
        elif choice == "5.2":
            cmd_visualize_trends(session)
        elif choice == "5.3":
            cmd_summary_table(session)
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
