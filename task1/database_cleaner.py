"""
Database-level data cleaning module.

This module provides SQL-based data cleaning directly on SQLite databases,
complementing the CSV-based pipeline cleaning approach.

Use cases:
- Clean data after loading raw CSV into database
- Demonstrate SQL data manipulation capabilities
- Alternative workflow: CSV → DB → Clean in DB

Comparison with pipeline_clean_export.py:
- Pipeline approach: CSV → Python clean → CSV → DB (preserves intermediate files)
- Database approach: CSV → DB → SQL UPDATE (in-place cleaning)
"""

import sqlite3
from typing import Dict, List, Tuple
from contextlib import contextmanager


@contextmanager
def _get_connection(db_path: str):
    """Context manager for database connections with transaction support."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def analyze_data_quality(db_path: str) -> Dict[str, any]:
    """
    Analyze data quality metrics before cleaning.
    
    Returns statistics about:
    - Total records
    - NULL value counts per column
    - Invalid value patterns
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        Dictionary with quality metrics
    """
    with _get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Get total record count
        cursor.execute("SELECT COUNT(*) as total FROM life_expectancy")
        total_records = cursor.fetchone()['total']
        
        # Get column names
        cursor.execute("PRAGMA table_info(life_expectancy)")
        columns = [row['name'] for row in cursor.fetchall() if row['name'] != 'id']
        
        # Count NULL values per column
        null_counts = {}
        for col in columns:
            cursor.execute(f'SELECT COUNT(*) as nulls FROM life_expectancy WHERE "{col}" IS NULL OR "{col}" = ""')
            null_counts[col] = cursor.fetchone()['nulls']
        
        # Calculate NULL percentages
        null_percentages = {
            col: (count / total_records * 100) if total_records > 0 else 0
            for col, count in null_counts.items()
        }
        
        return {
            'total_records': total_records,
            'null_counts': null_counts,
            'null_percentages': null_percentages,
            'columns_analyzed': len(columns)
        }


def clean_numeric_columns(db_path: str, dry_run: bool = False) -> Dict[str, int]:
    """
    Clean numeric columns in the database using SQL UPDATE statements.
    
    Cleaning operations:
    1. Convert empty strings to NULL
    2. Remove non-numeric characters (except decimal point and minus)
    3. Set invalid values to NULL
    
    Args:
        db_path: Path to SQLite database
        dry_run: If True, only report what would be changed without modifying data
        
    Returns:
        Dictionary with column names and number of rows updated
    """
    # Numeric columns from the life expectancy dataset
    numeric_columns = [
        'life_expect', 'life_exp60', 'adult_mortality', 'infant_mort',
        'age1-4mort', 'alcohol', 'bmi', 'age5-19thinness', 'age5-19obesity',
        'hepatitis', 'measles', 'polio', 'diphtheria', 'basic_water',
        'doctors', 'hospitals', 'gni_capita', 'gghe-d', 'che_gdp',
        'une_pop', 'une_infant', 'une_life', 'une_hiv', 'une_gni',
        'une_poverty', 'une_edu_spend', 'une_literacy', 'une_school'
    ]
    
    results = {}
    
    with _get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        for col in numeric_columns:
            # Count rows that need cleaning
            cursor.execute(f'''
                SELECT COUNT(*) as count FROM life_expectancy 
                WHERE "{col}" IS NOT NULL 
                AND "{col}" != ''
                AND (
                    CAST("{col}" AS TEXT) NOT GLOB '*[0-9.]*'
                    OR CAST("{col}" AS TEXT) GLOB '*[a-zA-Z]*'
                )
            ''')
            invalid_count = cursor.fetchone()['count']
            
            if dry_run:
                results[col] = invalid_count
            else:
                # Clean empty strings to NULL
                cursor.execute(f'''
                    UPDATE life_expectancy 
                    SET "{col}" = NULL 
                    WHERE "{col}" = ''
                ''')
                
                # Clean invalid numeric values to NULL
                cursor.execute(f'''
                    UPDATE life_expectancy 
                    SET "{col}" = NULL 
                    WHERE "{col}" IS NOT NULL 
                    AND (
                        CAST("{col}" AS TEXT) NOT GLOB '*[0-9.]*'
                        OR CAST("{col}" AS TEXT) GLOB '*[a-zA-Z]*'
                    )
                ''')
                
                results[col] = cursor.rowcount
    
    return results


def clean_year_column(db_path: str, min_year: int = 1900, max_year: int = 2100) -> int:
    """
    Clean year column to ensure valid year values.
    
    Args:
        db_path: Path to SQLite database
        min_year: Minimum valid year
        max_year: Maximum valid year
        
    Returns:
        Number of rows updated
    """
    with _get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Set invalid years to NULL
        cursor.execute(f'''
            UPDATE life_expectancy 
            SET year = NULL 
            WHERE year IS NOT NULL 
            AND (year < ? OR year > ?)
        ''', (min_year, max_year))
        
        return cursor.rowcount


def remove_duplicate_records(db_path: str) -> int:
    """
    Remove duplicate records based on (country, year) combination.
    Keeps the record with the lowest id.
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        Number of duplicate rows deleted
    """
    with _get_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Delete duplicates, keeping the first occurrence
        cursor.execute('''
            DELETE FROM life_expectancy 
            WHERE id NOT IN (
                SELECT MIN(id) 
                FROM life_expectancy 
                GROUP BY country, year
            )
        ''')
        
        return cursor.rowcount


def clean_database_full(
    db_path: str, 
    clean_numeric: bool = True,
    clean_year: bool = True,
    remove_duplicates: bool = True,
    dry_run: bool = False
) -> Dict[str, any]:
    """
    Execute complete database cleaning pipeline.
    
    This is the main entry point for database-level cleaning,
    analogous to export_cleaned_dataset() in pipeline_clean_export.py
    
    Args:
        db_path: Path to SQLite database
        clean_numeric: Clean numeric columns
        clean_year: Clean year column
        remove_duplicates: Remove duplicate records
        dry_run: If True, report changes without modifying data
        
    Returns:
        Dictionary with cleaning results and statistics
    """
    results = {
        'before': analyze_data_quality(db_path),
        'operations': {}
    }
    
    if clean_numeric:
        numeric_results = clean_numeric_columns(db_path, dry_run)
        results['operations']['numeric_cleaning'] = {
            'columns_processed': len(numeric_results),
            'total_updates': sum(numeric_results.values()),
            'details': numeric_results
        }
    
    if clean_year and not dry_run:
        year_updates = clean_year_column(db_path)
        results['operations']['year_cleaning'] = {
            'rows_updated': year_updates
        }
    
    if remove_duplicates and not dry_run:
        duplicates_removed = remove_duplicate_records(db_path)
        results['operations']['duplicate_removal'] = {
            'rows_deleted': duplicates_removed
        }
    
    if not dry_run:
        results['after'] = analyze_data_quality(db_path)
    
    return results


def print_cleaning_report(results: Dict[str, any]):
    """
    Print human-readable cleaning report.
    
    Args:
        results: Results dictionary from clean_database_full()
    """
    print("\n" + "="*60)
    print("DATABASE CLEANING REPORT")
    print("="*60)
    
    before = results['before']
    print(f"\n📊 Before Cleaning:")
    print(f"   Total records: {before['total_records']}")
    print(f"   Columns analyzed: {before['columns_analyzed']}")
    
    # Show top 5 columns with most NULL values
    null_pcts = before['null_percentages']
    top_nulls = sorted(null_pcts.items(), key=lambda x: x[1], reverse=True)[:5]
    if top_nulls:
        print(f"\n   Top 5 columns with NULL values:")
        for col, pct in top_nulls:
            print(f"      {col}: {pct:.1f}%")
    
    print(f"\n🔧 Operations Performed:")
    for op_name, op_data in results['operations'].items():
        if op_name == 'numeric_cleaning':
            print(f"   ✓ Numeric cleaning: {op_data['total_updates']} values updated")
        elif op_name == 'year_cleaning':
            print(f"   ✓ Year validation: {op_data['rows_updated']} invalid years fixed")
        elif op_name == 'duplicate_removal':
            print(f"   ✓ Duplicate removal: {op_data['rows_deleted']} duplicates deleted")
    
    if 'after' in results:
        after = results['after']
        print(f"\n✅ After Cleaning:")
        print(f"   Total records: {after['total_records']}")
        print(f"   Records changed: {before['total_records'] - after['total_records']}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    """
    Example usage:
    python task1/database_cleaner.py
    """
    import sys
    
    # Default to test database
    db_path = "task1/data/test_life_expectancy.db"
    
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    
    print(f"Analyzing database: {db_path}")
    
    # Dry run first
    print("\n🔍 DRY RUN - Analyzing what would be cleaned...")
    dry_results = clean_database_full(db_path, dry_run=True)
    print_cleaning_report(dry_results)
    
    # Ask for confirmation
    print("\n⚠️  This will modify the database. Continue? (y/n): ", end="")
    if input().lower() == 'y':
        print("\n🔄 Executing cleaning operations...")
        results = clean_database_full(db_path, dry_run=False)
        print_cleaning_report(results)
        print("\n✅ Database cleaning completed!")
    else:
        print("\n❌ Cleaning cancelled.")
