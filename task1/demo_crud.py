#!/usr/bin/env python3
"""
CRUD Operations Demo - Interactive Testing

This script demonstrates Create, Read, Update, Delete operations
on the life expectancy database.

Usage:
    python task1/demo_crud.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task1.database_loader import (
    create_database,
    create_record,
    get_all_records,
    get_records_by_country,
    update_record,
    delete_record,
    delete_records,
    delete_records_by_country
)

# Demo database path
DEMO_DB = "task1/data/crud_demo.db"


def print_section(title):
    """Print section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_records(records, limit=5):
    """Print records in a readable format."""
    if not records:
        print("  (No records found)")
        return
    
    print(f"  Found {len(records)} record(s):")
    for i, record in enumerate(records[:limit], 1):
        print(f"  {i}. {record['country']} ({record['year']}): "
              f"Life Expectancy = {record['life_expect']}, "
              f"BMI = {record.get('bmi', 'N/A')}")
    
    if len(records) > limit:
        print(f"  ... ({len(records) - limit} more records)")


def demo_crud():
    """Run CRUD operations demonstration."""
    
    # Clean up previous demo database
    if os.path.exists(DEMO_DB):
        os.remove(DEMO_DB)
    
    print("\n" + "🔧 CRUD Operations Demo".center(70, "="))
    
    # ========================================================================
    # Step 1: Create Database
    # ========================================================================
    print_section("Step 1: CREATE Database Schema")
    create_database(DEMO_DB)
    print(f"  ✓ Database created: {DEMO_DB}")
    
    # ========================================================================
    # Step 2: CREATE - Insert New Records
    # ========================================================================
    print_section("Step 2: CREATE - Insert New Records")
    
    # Create individual records
    records_to_create = [
        {"country": "China", "region": "Asia", "year": 2015, "life_expect": 76.1, "bmi": 23.8},
        {"country": "China", "region": "Asia", "year": 2016, "life_expect": 76.4, "bmi": 24.0},
        {"country": "India", "region": "Asia", "year": 2015, "life_expect": 68.3, "bmi": 21.5},
        {"country": "USA", "region": "Americas", "year": 2015, "life_expect": 78.9, "bmi": 28.5},
        {"country": "Brazil", "region": "Americas", "year": 2015, "life_expect": 74.8, "bmi": 26.5},
    ]
    
    for record in records_to_create:
        create_record(DEMO_DB, record)
        print(f"  ✓ Created: {record['country']} ({record['year']})")
    
    # ========================================================================
    # Step 3: READ - Query Records
    # ========================================================================
    print_section("Step 3: READ - Query All Records")
    all_records = get_all_records(DEMO_DB)
    print_records(all_records)
    
    print_section("Step 3b: READ - Query by Country (China)")
    china_records = get_records_by_country(DEMO_DB, "China")
    print_records(china_records)
    
    # ========================================================================
    # Step 4: UPDATE - Modify Existing Records
    # ========================================================================
    print_section("Step 4: UPDATE - Update China 2015 Life Expectancy")
    print(f"  Before: {china_records[0]['life_expect']}")
    
    update_record(DEMO_DB, country="China", year=2015, 
                  updates={"life_expect": 76.5, "bmi": 24.2})
    
    updated_records = get_records_by_country(DEMO_DB, "China")
    print(f"  After:  {updated_records[0]['life_expect']}")
    print(f"  ✓ Updated China 2015: life_expect → 76.5, bmi → 24.2")
    
    # ========================================================================
    # Step 5: DELETE - Remove Records (Single)
    # ========================================================================
    print_section("Step 5: DELETE - Delete Single Record (India 2015)")
    print(f"  Before deletion: {len(get_all_records(DEMO_DB))} records")
    
    delete_record(DEMO_DB, country="India", year=2015)
    print(f"  ✓ Deleted India 2015")
    
    print(f"  After deletion:  {len(get_all_records(DEMO_DB))} records")
    
    # ========================================================================
    # Step 6: DELETE - Remove Records (By Filter)
    # ========================================================================
    print_section("Step 6: DELETE - Delete by Region (Americas)")
    print(f"  Before deletion: {len(get_all_records(DEMO_DB))} records")
    
    deleted_count = delete_records(DEMO_DB, filters={"region": "Americas"})
    print(f"  ✓ Deleted {deleted_count} Americas records")
    
    remaining = get_all_records(DEMO_DB)
    print(f"  After deletion:  {len(remaining)} records")
    print_records(remaining)
    
    # ========================================================================
    # Step 7: DELETE - Remove All Records for Country
    # ========================================================================
    print_section("Step 7: DELETE - Delete All China Records")
    deleted_count = delete_records_by_country(DEMO_DB, "China")
    print(f"  ✓ Deleted {deleted_count} China record(s)")
    
    final_records = get_all_records(DEMO_DB)
    print(f"  Final count: {len(final_records)} records")
    print_records(final_records)
    
    # ========================================================================
    # Summary
    # ========================================================================
    print_section("✅ CRUD Operations Summary")
    print("""
  ✓ CREATE: create_record() - Insert new records with duplicate check
  ✓ READ:   get_all_records(), get_records_by_country() - Query data
  ✓ UPDATE: update_record() - Modify specific fields
  ✓ DELETE: delete_record() - Remove single record
  ✓ DELETE: delete_records() - Remove by flexible filters (GENERALIZED)
  ✓ DELETE: delete_records_by_country() - Convenience wrapper
    
  Key Features:
  • Parameterized queries (SQL injection safe)
  • Duplicate detection for CREATE
  • Existence validation for UPDATE/DELETE
  • Flexible filtering (country, region, year, combinations)
  • Transaction support with automatic rollback
    """)
    
    print(f"\n  Demo database: {DEMO_DB}")
    print(f"  You can inspect it with: sqlite3 {DEMO_DB}\n")


if __name__ == "__main__":
    try:
        demo_crud()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
