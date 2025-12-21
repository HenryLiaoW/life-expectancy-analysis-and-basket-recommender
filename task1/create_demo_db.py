"""
Generate demo.db for CLI demonstrations.

This script creates a small demo database with 12 records (4 countries × 3 years)
for CLI usage examples. The data is identical to the test data from conftest.py.
"""

import os
import sys

# Add project root and tests to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from task1.database_loader import create_database, load_data_to_db
from conftest import get_test_sample_data


def main():
    """Generate demo database for CLI demonstrations."""
    demo_db_path = "task1/data/demo.db"
    
    # Remove existing demo.db if it exists
    if os.path.exists(demo_db_path):
        os.remove(demo_db_path)
        print(f"✓ Removed existing {demo_db_path}")
    
    # Create database
    create_database(demo_db_path)
    print(f"✓ Created database: {demo_db_path}")
    
    # Load demo data (imported from conftest.py)
    demo_data = get_test_sample_data()
    load_data_to_db(demo_db_path, demo_data)
    print(f"✓ Loaded {len(demo_data)} records")
    
    print("\n📊 Demo database ready for CLI demonstrations!")
    print(f"   - Database: {demo_db_path}")
    print(f"   - Records: {len(demo_data)}")
    print("   - Countries: China, India, USA, Brazil")
    print("   - Years: 2015-2017")
    print("\n💡 Usage:")
    print("  python task1/cli.py --db task1/data/demo.db info")
    print("\n📝 Note: Demo data is identical to test data in conftest.py")


if __name__ == "__main__":
    main()
