"""
Create database from CSV file.

This script creates a SQLite database from any CSV file containing
life expectancy data. Supports both demo data and full datasets.
"""

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task1.config import (
    RAW_LIFE_EXPECTANCY_CSV,
    FULL_DATABASE,
    DEMO_DATABASE,
)
from task1.src.database_loader import create_database, load_data_to_db
from task1.src.data_loader import load_csv
from task1.src.cleaner import clean_dataset


def create_db_from_csv(csv_path: str, db_path: str, use_demo_data: bool = False):
    """
    Create SQLite database from CSV file.
    
    Args:
        csv_path: Path to CSV file
        db_path: Path for output database
        use_demo_data: If True, use conftest demo data instead of CSV
    """
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Removed existing {db_path}")
    
    # Create database schema
    create_database(db_path)
    print(f"✓ Created database: {db_path}")
    
    # Load data
    if use_demo_data:
        # Import demo data from conftest
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))
        from conftest import get_test_sample_data
        data = get_test_sample_data()
        print(f"✓ Loaded demo data: {len(data)} records")
    else:
        # Load from CSV
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        data = load_csv(csv_path)
        print(f"✓ Loaded CSV: {csv_path}")
        print(f"  Records: {len(data)}")
        
        # Clean data using cleaner.py
        print(f"🧹 Cleaning data...")
        data = clean_dataset(data)
        print(f"✓ Data cleaned: {len(data)} records")
    
    # Insert data into database
    load_data_to_db(db_path, data)
    print(f"✓ Inserted {len(data)} records")
    
    # Summary
    db_size = os.path.getsize(db_path)
    print(f"\n📊 Database Summary:")
    print(f"   Path: {db_path}")
    print(f"   Records: {len(data)}")
    print(f"   Size: {db_size:,} bytes ({db_size/1024:.1f} KB)")
    
    return db_path


def main():
    """CLI entry point for database creation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create database from CSV file")
    parser.add_argument(
        "--csv", 
        default=str(RAW_LIFE_EXPECTANCY_CSV),
        help=f"Path to CSV file (default: {RAW_LIFE_EXPECTANCY_CSV})"
    )
    parser.add_argument(
        "--db",
        default=str(FULL_DATABASE),
        help=f"Output database path (default: {FULL_DATABASE})"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Create demo database with test data (12 records)"
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("Database Creation Tool")
    print("="*60)
    print()
    
    if args.demo:
        # Create demo database
        db_path = create_db_from_csv(
            csv_path=None,
            db_path=str(DEMO_DATABASE),
            use_demo_data=True
        )
        print("\n💡 Usage:")
        print(f"  python task1/main_cli.py --db {db_path}")
        print("\n📝 Note: Demo contains 4 countries × 3 years = 12 records")
    else:
        # Create from CSV
        db_path = create_db_from_csv(
            csv_path=args.csv,
            db_path=args.db,
            use_demo_data=False
        )
        print("\n💡 Usage:")
        print(f"  python task1/main_cli.py --db {db_path}")


if __name__ == "__main__":
    main()
