"""
Test visualization functionality (matplotlib charts).

This test verifies that the visualization module can generate
high-quality charts from filtered data.
"""

import os
import sys
import pandas as pd

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from task1.visualization import (
    generate_life_expectancy_trend_chart,
    generate_summary_table
)
from task1.database_loader import get_all_records


def test_chart_generation():
    """Test that chart generation works correctly."""
    print("\n" + "="*60)
    print("Testing Visualization Module")
    print("="*60)
    
    # Load data from demo database
    print("\n📋 Step 1: Loading data from CLI_demo.db...")
    db_path = "task1/data/CLI_demo.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    records = get_all_records(db_path)
    data = pd.DataFrame(records)
    print(f"✅ Loaded {len(data)} records")
    
    # Filter to China only for testing
    print("\n📋 Step 2: Filtering to China data...")
    china_data = data[data['country'] == 'China']
    print(f"✅ Filtered to {len(china_data)} China records")
    
    # Generate chart using visualization module
    print("\n📋 Step 3: Generating chart with visualization.py...")
    output_path = "task1/output/test_life_expectancy_trends.png"
    
    result_path = generate_life_expectancy_trend_chart(
        data=china_data,
        output_path=output_path,
        dpi=300,
        show_chart=False  # Don't show in test
    )
    print(f"✅ Chart generated: {result_path}")
    
    # Verify file exists
    print("\n📋 Step 4: Verifying output file...")
    assert os.path.exists(output_path), f"Output file not found: {output_path}"
    
    # Check file size
    file_size = os.path.getsize(output_path)
    print(f"✅ File size: {file_size:,} bytes")
    
    assert file_size >= 10000, f"File size too small: {file_size} bytes (expected >= 10KB)"
    
    print("\n" + "="*60)
    print("🎉 Visualization test PASSED!")
    print("="*60)
    print(f"\n📊 Generated chart: {output_path}")
    print(f"   Size: {file_size:,} bytes")
    print(f"   DPI: 300")
    print(f"   Countries: China")
    print(f"   Years: {china_data['year'].min()} - {china_data['year'].max()}")


def test_table_generation():
    """Test that pandas table generation works correctly."""
    print("\n" + "="*60)
    print("Testing Pandas Table Generation")
    print("="*60)
    
    # Load data
    print("\n📋 Step 1: Loading data from CLI_demo.db...")
    db_path = "task1/data/CLI_demo.db"
    
    assert os.path.exists(db_path), f"Database not found: {db_path}"
    
    records = get_all_records(db_path)
    data = pd.DataFrame(records)
    print(f"✅ Loaded {len(data)} records")
    
    # Generate summary table
    print("\n📋 Step 2: Generating summary table...")
    summary_df = generate_summary_table(
        data=data,
        group_by='country'
    )
    print(f"✅ Generated summary table with {len(summary_df)} rows")
    print("\n📊 Summary Table Preview:")
    print(summary_df.to_string())
    
    # Verify table structure
    print("\n📋 Step 3: Verifying table structure...")
    assert len(summary_df) > 0, "Table is empty"
    
    print(f"✅ Table has {len(summary_df)} rows and {len(summary_df.columns)} columns")
    
    print("\n" + "="*60)
    print("🎉 Pandas table test PASSED!")
    print("="*60)


if __name__ == "__main__":
    chart_success = test_chart_generation()
    table_success = test_table_generation()
    
    print("\n" + "="*60)
    print("OVERALL TEST RESULTS")
    print("="*60)
    print(f"Chart generation: {'✅ PASSED' if chart_success else '❌ FAILED'}")
    print(f"Table generation: {'✅ PASSED' if table_success else '❌ FAILED'}")
    
    success = chart_success and table_success
    sys.exit(0 if success else 1)
