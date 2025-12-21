#!/usr/bin/env python3
"""
Life Expectancy Analysis CLI

Command-line interface for analyzing life expectancy data with policy insights.

Usage Examples:
    # Show database info
    python cli.py info

    # Filter by country
    python cli.py filter --country China

    # Analyze water access impact
    python cli.py analyze water-access --region Asia

    # Compare countries
    python cli.py compare China India USA

    # Get policy priorities
    python cli.py policy --country India --target 75
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task1.data_filter import (
    get_data_as_dataframe,
    filter_by_country,
    filter_by_year_range,
    filter_by_region,
    calculate_statistics,
    get_country_trend,
    analyze_water_access_impact,
    analyze_healthcare_spending,
    analyze_nutrition_indicators,
    identify_vaccination_gaps,
    compare_modifiable_factors,
    get_policy_intervention_priorities,
)

# Default database path
# During development/testing: use demo.db for fast feedback (TDD)
# For production: change to life_expectancy.db
DEFAULT_DB = "task1/data/demo.db"


class LifeExpectancyCLI:
    """Main CLI application class."""
    
    def __init__(self, db_path: str = DEFAULT_DB):
        self.db_path = db_path
    
    def cmd_info(self, args):
        """Display database information."""
        print("\n" + "="*70)
        print("📊 Life Expectancy Database Info")
        print("="*70)
        
        df = get_data_as_dataframe(self.db_path)
        
        print(f"\n✓ Database: {self.db_path}")
        print(f"✓ Total Records: {len(df):,}")
        print(f"✓ Countries: {df['country'].nunique()}")
        print(f"✓ Year Range: {df['year'].min()} - {df['year'].max()}")
        print(f"✓ Regions: {', '.join(sorted(df['region'].unique()))}")
        
        print("\n📈 Data Summary:")
        print(f"  • Life Expectancy: {df['life_expect'].min():.1f} - {df['life_expect'].max():.1f} years")
        print(f"  • Average: {df['life_expect'].mean():.1f} years")
        
        print("\n🌍 Top 5 Countries (Latest Year):")
        latest_year = df['year'].max()
        top5 = df[df['year'] == latest_year].nlargest(5, 'life_expect')[['country', 'life_expect']]
        for idx, row in top5.iterrows():
            print(f"  {row['country']:20} {row['life_expect']:.1f} years")
        
        print("\n" + "="*70 + "\n")
    
    def cmd_filter(self, args):
        """Filter data by various criteria."""
        print("\n" + "="*70)
        print("🔍 Filtering Data")
        print("="*70)
        
        df = get_data_as_dataframe(self.db_path)
        
        # Apply filters
        if args.country:
            df = filter_by_country(df, args.country)
            print(f"\n✓ Filtered by country: {args.country}")
        
        if args.region:
            df = filter_by_region(df, args.region)
            print(f"✓ Filtered by region: {args.region}")
        
        if args.year_start or args.year_end:
            start = args.year_start or df['year'].min()
            end = args.year_end or df['year'].max()
            df = filter_by_year_range(df, start, end)
            print(f"✓ Filtered by years: {start} - {end}")
        
        if df.empty:
            print("\n❌ No records found matching the criteria.")
            return
        
        # Display results
        print(f"\n📊 Results: {len(df)} records")
        
        if args.stats:
            print("\n📈 Statistics:")
            stats = calculate_statistics(df, 'life_expect')
            print(f"  • Mean:   {stats['mean']:.2f} years")
            print(f"  • Median: {stats['median']:.2f} years")
            print(f"  • Min:    {stats['min']:.2f} years")
            print(f"  • Max:    {stats['max']:.2f} years")
            print(f"  • StdDev: {stats['std']:.2f}")
        
        if args.show:
            print("\n📋 Data Preview:")
            cols = ['country', 'year', 'life_expect', 'region']
            print(df[cols].head(args.show).to_string(index=False))
        
        if args.output:
            df.to_csv(args.output, index=False)
            print(f"\n✓ Data exported to: {args.output}")
        
        print("\n" + "="*70 + "\n")
    
    def cmd_analyze(self, args):
        """Perform policy-oriented analysis."""
        print("\n" + "="*70)
        print(f"🔬 Analysis: {args.analysis_type}")
        print("="*70)
        
        df = get_data_as_dataframe(self.db_path)
        
        if args.analysis_type == 'water-access':
            result = analyze_water_access_impact(df)
            print("\n💧 Water Access Impact Analysis")
            print(f"\n📊 Countries analyzed: {result['country'].nunique()}")
            print("\n🌍 Water Access Coverage (top 10):")
            top10 = result.groupby('country')['basic_water'].mean().nlargest(10)
            for country, value in top10.items():
                print(f"  {country:20} {value:.1f}%")
        
        elif args.analysis_type == 'healthcare':
            stats = analyze_healthcare_spending(df, region=args.region)
            print("\n🏥 Healthcare Spending Analysis")
            if args.region:
                print(f"Region: {args.region}")
            print(f"\n💰 Average spending (gghe-d): {stats['mean_gghe_d']:.2f}%")
            print(f"   Median: {stats['median_gghe_d']:.2f}%")
            print(f"   Min: {stats['min_gghe_d']:.2f}%")
            print(f"   Max: {stats['max_gghe_d']:.2f}%")
            
            if 'country_rankings' in stats:
                print("\n🏆 Top 10 Countries by Healthcare Spending:")
                rankings = stats['country_rankings']
                for idx, row in rankings.head(10).iterrows():
                    print(f"  {row['country']:20} {row['gghe-d']:.2f}%")
        
        elif args.analysis_type == 'nutrition':
            result = analyze_nutrition_indicators(df)
            print("\n🍎 Nutrition Indicators Analysis")
            print(f"\n📊 Average BMI by region:")
            bmi_by_region = result.groupby('region')['bmi'].mean().sort_values(ascending=False)
            for region, bmi in bmi_by_region.items():
                status = "⚠️  Overweight" if bmi > 25 else "✓ Normal"
                print(f"  {region:15} {bmi:.1f}  {status}")
        
        elif args.analysis_type == 'vaccination':
            gaps = identify_vaccination_gaps(df, threshold=args.threshold or 90.0)
            print(f"\n💉 Vaccination Coverage Gaps (< {args.threshold or 90}%)")
            if gaps.empty:
                print("\n✓ No significant gaps found!")
            else:
                print(f"\n⚠️  {len(gaps)} countries with coverage gaps:")
                print(gaps[['country', 'year', 'polio', 'diphtheria']].head(10).to_string(index=False))
        
        print("\n" + "="*70 + "\n")
    
    def cmd_compare(self, args):
        """Compare modifiable factors across countries."""
        print("\n" + "="*70)
        print(f"⚖️  Comparing Countries: {', '.join(args.countries)}")
        print("="*70)
        
        df = get_data_as_dataframe(self.db_path)
        
        # Show which factors are being compared
        if args.factors:
            factors_used = args.factors.split(',')
            print(f"\n📋 Comparing factors: {', '.join(factors_used)}")
        else:
            print(f"\n📋 Comparing factors: basic_water, gghe-d, bmi, alcohol (default top correlations)")
            print(f"   💡 Use --factors to customize (e.g., --factors basic_water,infant_mort,polio)")
        
        try:
            result = compare_modifiable_factors(
                df, 
                countries=args.countries,
                factors=args.factors.split(',') if args.factors else None,
                include_all_years=args.all_years
            )
            
            print(f"\n📊 Comparison Results ({len(result)} records)")
            print("\n" + result.to_string(index=False))
            
            if args.output:
                result.to_csv(args.output, index=False)
                print(f"\n✓ Data exported to: {args.output}")
        
        except ValueError as e:
            print(f"\n❌ Error: {e}")
        
        print("\n" + "="*70 + "\n")
    
    def cmd_policy(self, args):
        """Get policy intervention priorities."""
        print("\n" + "="*70)
        print(f"🎯 Policy Priorities for {args.country}")
        print("="*70)
        
        df = get_data_as_dataframe(self.db_path)
        
        try:
            result = get_policy_intervention_priorities(
                df,
                country=args.country,
                target_life_expectancy=args.target
            )
            
            print(f"\n📍 Current gap: {result['current_gap']:.2f} years below target")
            print(f"   Target: {args.target:.1f} years")
            
            print("\n🔝 Top Priorities (by impact):")
            for i, priority in enumerate(result['top_priorities'][:5], 1):
                print(f"  {i}. {priority}")
            
            if 'estimated_impact' in result:
                print("\n📈 Estimated Impact:")
                for factor, impact in result['estimated_impact'].items():
                    print(f"  • {factor}: +{impact:.2f} years")
        
        except ValueError as e:
            print(f"\n❌ Error: {e}")
        
        print("\n" + "="*70 + "\n")
    
    def cmd_trend(self, args):
        """Show time series trend for a country."""
        print("\n" + "="*70)
        print(f"📈 Trend Analysis: {args.country}")
        print("="*70)
        
        try:
            trend = get_country_trend(self.db_path, args.country, args.metric)
            
            if trend.empty:
                print(f"\n❌ No data found for {args.country}")
                return
            
            print(f"\n📊 {args.metric.replace('_', ' ').title()} over time:")
            print("\n" + trend.to_string(index=False))
            
            # Simple ASCII chart
            values = trend[args.metric].values
            print(f"\n📉 Trend: ", end="")
            if values[-1] > values[0]:
                print("↗️  Improving" if args.metric == 'life_expect' else "↗️  Increasing")
            elif values[-1] < values[0]:
                print("↘️  Declining" if args.metric == 'life_expect' else "↘️  Decreasing")
            else:
                print("→ Stable")
            
            if args.output:
                trend.to_csv(args.output, index=False)
                print(f"\n✓ Data exported to: {args.output}")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        print("\n" + "="*70 + "\n")


def create_parser():
    """Create argument parser with all commands."""
    parser = argparse.ArgumentParser(
        description="Life Expectancy Analysis CLI - Policy-Oriented Insights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s info
  %(prog)s filter --country China --stats
  %(prog)s analyze water-access --region Asia
  %(prog)s compare China India USA
  %(prog)s policy --country India --target 75
  %(prog)s trend --country China --metric life_expect
        """
    )
    
    parser.add_argument(
        '--db', 
        default=DEFAULT_DB,
        help=f'Database path (default: {DEFAULT_DB})'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Info command
    subparsers.add_parser('info', help='Show database information')
    
    # Filter command
    filter_parser = subparsers.add_parser('filter', help='Filter data by criteria')
    filter_parser.add_argument('--country', help='Filter by country name')
    filter_parser.add_argument('--region', help='Filter by region')
    filter_parser.add_argument('--year-start', type=int, help='Start year')
    filter_parser.add_argument('--year-end', type=int, help='End year')
    filter_parser.add_argument('--stats', action='store_true', help='Show statistics')
    filter_parser.add_argument('--show', type=int, metavar='N', help='Show N records')
    filter_parser.add_argument('--output', '-o', help='Export to CSV file')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Perform policy analysis')
    analyze_parser.add_argument(
        'analysis_type',
        choices=['water-access', 'healthcare', 'nutrition', 'vaccination'],
        help='Type of analysis'
    )
    analyze_parser.add_argument('--region', help='Filter by region')
    analyze_parser.add_argument('--threshold', type=float, help='Threshold for vaccination gaps')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare countries')
    compare_parser.add_argument('countries', nargs='+', help='Countries to compare')
    compare_parser.add_argument('--factors', help='Comma-separated factors (default: top correlations)')
    compare_parser.add_argument('--all-years', action='store_true', help='Include all years')
    compare_parser.add_argument('--output', '-o', help='Export to CSV file')
    
    # Policy command
    policy_parser = subparsers.add_parser('policy', help='Get policy priorities')
    policy_parser.add_argument('--country', required=True, help='Target country')
    policy_parser.add_argument('--target', type=float, required=True, help='Target life expectancy')
    
    # Trend command
    trend_parser = subparsers.add_parser('trend', help='Show time series trend')
    trend_parser.add_argument('--country', required=True, help='Country name')
    trend_parser.add_argument('--metric', default='life_expect', help='Metric to analyze')
    trend_parser.add_argument('--output', '-o', help='Export to CSV file')
    
    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Check if database exists
    if not Path(args.db).exists():
        print(f"❌ Error: Database not found: {args.db}")
        print("\nPlease create the database first:")
        print("  python task1/pipeline_clean_export.py")
        sys.exit(1)
    
    # Initialize CLI
    cli = LifeExpectancyCLI(args.db)
    
    # Execute command
    try:
        command_method = getattr(cli, f'cmd_{args.command}')
        command_method(args)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
