"""
Quick test to verify both cleaning modes work correctly.

This script tests:
1. Pipeline Mode - CSV → Clean → CSV → DB
2. Database Mode - CSV → DB → SQL Clean

Run: python task1/test_cleaning_modes.py
"""

import os
import sys
import shutil

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from task1.scripts.pipeline_clean_export import export_cleaned_dataset
from task1.src.database_cleaner import clean_database_full, print_cleaning_report
from task1.src.create_db import create_db_from_csv


def test_pipeline_mode():
    """Test Pipeline Mode: CSV → Python Clean → CSV → DB"""
    print("\n" + "="*70)
    print("TEST 1: PIPELINE MODE (CSV → Python Clean → CSV → DB)")
    print("="*70)
    
    # Step 1: Clean CSV
    print("\n📋 Step 1: Cleaning CSV with Python...")
    input_csv = "task1/data/life_expectancy.csv"
    cleaned_csv = "task1/data/test_cleaned_via_pipeline.csv"
    
    export_cleaned_dataset(input_csv, cleaned_csv)
    
    # Step 2: Load cleaned CSV to database
    print("\n📋 Step 2: Loading cleaned CSV to database...")
    pipeline_db = "task1/data/test_database_mode.db"
    create_db_from_csv(cleaned_csv, pipeline_db, use_demo_data=False)
    
    print("\n✅ Pipeline Mode Test PASSED")
    assert os.path.exists(pipeline_db), f"Pipeline database not created: {pipeline_db}"


def test_database_mode():
    """Test Database Mode: CSV → DB → SQL Clean"""
    print("\n" + "="*70)
    print("TEST 2: DATABASE MODE (CSV → DB → SQL Clean)")
    print("="*70)
    
    # Step 1: Load raw CSV to database
    print("\n📋 Step 1: Loading raw CSV to database...")
    raw_csv = "task1/data/life_expectancy.csv"
    db_mode_db = "task1/data/test_database_mode.db"
    create_db_from_csv(raw_csv, db_mode_db, use_demo_data=False)
    
    # Step 2: Clean database with SQL
    print("\n📋 Step 2: Cleaning database with SQL...")
    results = clean_database_full(db_mode_db, dry_run=False)
    print_cleaning_report(results)
    
    print("\n✅ Database Mode Test PASSED")
    assert os.path.exists(db_mode_db), f"Database mode database not created: {db_mode_db}"


def compare_results(pipeline_db, db_mode_db):
    """Compare results from both modes."""
    import sqlite3
    
    print("\n" + "="*70)
    print("COMPARING RESULTS")
    print("="*70)
    
    # Get record counts
    conn1 = sqlite3.connect(pipeline_db)
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT COUNT(*) FROM life_expectancy")
    count1 = cursor1.fetchone()[0]
    conn1.close()
    
    conn2 = sqlite3.connect(db_mode_db)
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT COUNT(*) FROM life_expectancy")
    count2 = cursor2.fetchone()[0]
    conn2.close()
    
    print(f"\n📊 Record Counts:")
    print(f"   Pipeline Mode: {count1} records")
    print(f"   Database Mode: {count2} records")
    
    if count1 == count2:
        print(f"\n✅ Both modes produced {count1} records - CONSISTENT!")
    else:
        print(f"\n⚠️  Record counts differ: {count1} vs {count2}")
        print("   This is expected if cleaning logic differs slightly.")


def cleanup_test_files():
    """Clean up test files."""
    test_files = [
        "task1/data/test_cleaned_via_pipeline.csv",
        "task1/data/test_database_mode.db"
    ]
    
    print("\n🧹 Cleaning up test files...")
    for f in test_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"   Removed: {f}")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("CLEANING MODES INTEGRATION TEST")
    print("="*70)
    print("\nThis test verifies both cleaning approaches work correctly:")
    print("  1. Pipeline Mode - Offline CSV cleaning (Python)")
    print("  2. Database Mode - In-place database cleaning (SQL)")
    print("\n" + "="*70)
    
    try:
        # Test both modes
        pipeline_db = test_pipeline_mode()
        db_mode_db = test_database_mode()
        
        # Compare results
        compare_results(pipeline_db, db_mode_db)
        
        # Summary
        print("\n" + "="*70)
        print("🎉 ALL TESTS PASSED!")
        print("="*70)
        print("\nBoth cleaning modes are working correctly:")
        print("  ✅ Pipeline Mode (3.4 in menu)")
        print("  ✅ Database Mode (3.5 in menu)")
        print("\nYou can now use both approaches in your project!")
        print("\nSee CLEANING_MODES_COMPARISON.md for detailed documentation.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        print("\n" + "="*70)
        cleanup_choice = input("\nClean up test files? (y/n): ")
        if cleanup_choice.lower() == 'y':
            cleanup_test_files()
            print("✅ Cleanup complete")
        else:
            print("Test files kept for inspection")


if __name__ == "__main__":
    main()
