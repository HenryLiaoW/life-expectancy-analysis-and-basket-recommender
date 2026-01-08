"""
Data Filter Module - Demonstration Script

Demonstrates filtering and summary capabilities:
1. Conditional filtering (country, date range, region)
2. Statistical summaries (mean, min, max, count)
3. Trends over time
4. Grouped results (by country, region)
"""

from task1.src.data_filter import (
    get_data_as_dataframe,
    filter_by_country,
    filter_by_year_range,
    filter_by_region,
    calculate_statistics,
    get_country_trend,
    compare_modifiable_factors
)


def demo_filtering():
    """Demonstrate: conditional data filtering"""
    print("\n" + "="*50)
    print("1. Conditional Data Filtering")
    print("="*50)
    
    db_path = "task1/data/CLI_demo.db"
    df = get_data_as_dataframe(db_path)
    
    print(f"\nOriginal data: {len(df)} records")
    
    # 1.1 Filter by country
    china_data = filter_by_country(df, "China")
    print(f"\n✅ Filter by country (China): {len(china_data)} records")
    print(china_data[["year", "life_expect"]].to_string(index=False))
    
    # 1.2 Filter by date range
    recent_data = filter_by_year_range(df, 2016, 2017)
    print(f"\n✅ Filter by date range (2016-2017): {len(recent_data)} records")
    print(recent_data[["country", "year", "life_expect"]].head())
    
    # 1.3 Filter by region
    americas_data = filter_by_region(df, "Americas")
    print(f"\n✅ Filter by region (Americas): {len(americas_data)} records")
    print(americas_data[["country", "region", "year", "life_expect"]].head())
    
    # 1.4 Combined filtering
    china_recent = filter_by_year_range(
        filter_by_country(df, "China"), 
        2016, 2017
    )
    print(f"\n✅ Combined filter (China + 2016-2017): {len(china_recent)} records")
    print(china_recent[["country", "year", "life_expect"]])


def demo_summary_statistics():
    """Demonstrate: generate summary statistics"""
    print("\n" + "="*50)
    print("2. Summary Statistics")
    print("="*50)
    
    db_path = "task1/data/CLI_demo.db"
    df = get_data_as_dataframe(db_path)
    
    # 2.1 Global statistics
    print("\n✅ Global life expectancy statistics:")
    stats = calculate_statistics(df, "life_expect")
    for key, value in stats.items():
        print(f"  {key:10s}: {value:.2f}")
    
    # 2.2 Country-specific statistics
    print("\n✅ China life expectancy statistics:")
    china_data = filter_by_country(df, "China")
    china_stats = calculate_statistics(china_data, "life_expect")
    for key, value in china_stats.items():
        print(f"  {key:10s}: {value:.2f}")
    
    # 2.3 Year-specific statistics
    print("\n✅ Global life expectancy statistics for 2017:")
    data_2017 = filter_by_year_range(df, 2017, 2017)
    stats_2017 = calculate_statistics(data_2017, "life_expect")
    for key, value in stats_2017.items():
        print(f"  {key:10s}: {value:.2f}")


def demo_trends_over_time():
    """Demonstrate: trends over time"""
    print("\n" + "="*50)
    print("3. Trends Over Time")
    print("="*50)
    
    db_path = "task1/data/CLI_demo.db"
    
    # 3.1 Single country trend
    print("\n✅ China life expectancy trend (2015-2017):")
    china_trend = get_country_trend(db_path, "China", "life_expect")
    print("\n" + china_trend[["year", "life_expect"]].to_string(index=False))
    
    # Show trend direction
    if len(china_trend) > 1:
        trend_diff = china_trend["life_expect"].iloc[-1] - china_trend["life_expect"].iloc[0]
        print(f"\n   Trend: {'↗️ Improving' if trend_diff > 0 else '↘️ Declining'} ({trend_diff:+.1f} years)")
    
    # 3.2 Multiple indicators trend
    print("\n✅ China basic water access trend:")
    water_trend = get_country_trend(db_path, "China", "basic_water")
    print(water_trend.to_string(index=False))
    
    # 3.3 Non-existent country (returns empty DataFrame)
    print("\n✅ Non-existent country (Atlantis):")
    empty_trend = get_country_trend(db_path, "Atlantis", "life_expect")
    print(f"  Returns empty DataFrame: {empty_trend.empty}")
    print(f"  Columns preserved: {list(empty_trend.columns)}")


def demo_grouped_results():
    """Demonstrate: grouped results"""
    print("\n" + "="*50)
    print("4. Grouped Results (by country, region)")
    print("="*50)
    
    db_path = "task1/data/CLI_demo.db"
    df = get_data_as_dataframe(db_path)
    
    # 4.1 Country comparison (latest year)
    print("\n✅ Country comparison - basic water and alcohol (latest year):")
    comparison = compare_modifiable_factors(
        df, 
        countries=["China", "USA", "Brazil"],
        factors=["basic_water", "alcohol"]
    )
    print(comparison.to_string(index=False))
    
    # 4.2 Country comparison (all years)
    print("\n✅ Country comparison - all years:")
    comparison_all = compare_modifiable_factors(
        df, 
        countries=["China", "USA"],
        factors=["basic_water"],
        include_all_years=True
    )
    print(comparison_all.to_string(index=False))
    
    # 4.3 Regional statistics
    print("\n✅ Regional statistics - life expectancy:")
    regions = df["region"].unique()
    for region in regions:
        region_data = filter_by_region(df, region)
        stats = calculate_statistics(region_data, "life_expect")
        print(f"\n  {region}:")
        print(f"    mean: {stats['mean']:.2f}, min: {stats['min']:.2f}, "
              f"max: {stats['max']:.2f}, count: {stats['count']}")


def demo_advanced_use_case():
    """Demonstrate: advanced use case - combining multiple features"""
    print("\n" + "="*50)
    print("5. Advanced Use Case - Regional Comparison")
    print("="*50)
    
    db_path = "task1/data/CLI_demo.db"
    df = get_data_as_dataframe(db_path)
    
    print("\n✅ Asia vs Americas water access comparison (2015-2017):")
    
    for region in ["Asia", "Americas"]:
        print(f"\n{region}:")
        region_data = filter_by_region(df, region)
        
        for year in [2015, 2016, 2017]:
            year_data = filter_by_year_range(region_data, year, year)
            if not year_data.empty:
                stats = calculate_statistics(year_data, "basic_water")
                print(f"  {year}: mean={stats['mean']:.1f}%, "
                      f"range=[{stats['min']:.1f}% - {stats['max']:.1f}%]")


if __name__ == "__main__":
    # Run all demonstrations
    demo_filtering()
    demo_summary_statistics()
    demo_trends_over_time()
    demo_grouped_results()
    demo_advanced_use_case()
    
    print("\n" + "="*50)
    print("✅ All demonstrations completed!")
    print("="*50)
    print("\nCore capabilities:")
    print("  1. ✅ Filter by country/date/region")
    print("  2. ✅ Statistical summaries")
    print("  3. ✅ Analyze trends over time")
    print("  4. ✅ Group comparison")
    print("  5. ✅ Complex queries")
