"""
Database Loader Module - Robust Version

This module handles all database operations for the life expectancy dataset.
Following the Single Responsibility Principle, it focuses solely on:
- Creating database schema
- Loading cleaned data into SQLite database
- Providing database connections and queries

SOLID Principles:
- SRP: Only responsible for database operations
- OCP: Schema can be extended without modifying core logic
- DIP: Returns data in generic formats (list of dicts) for flexibility
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
from contextlib import contextmanager


def create_database(db_path: str) -> None:
    """
    Create SQLite database and life_expectancy table.
    
    Args:
        db_path: Path to the SQLite database file
        
    Raises:
        ValueError: If db_path is empty or invalid
        sqlite3.Error: If database creation fails
    """
    if not db_path: # in case of empty string
        raise ValueError("Database path cannot be empty")
    
    # Ensure directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    # if语句中db_dir是在确保os取到了目录的名称，防止db_path直接是文件名没有目录时报错
    # if语句中not后的os语句是为了确保目录存在，如果不存在就创建
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create life_expectancy table matching cleaned CSV columns
        # Note: Columns with hyphens need quotes in SQLite
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS life_expectancy (
                id INTEGER PRIMARY KEY AUTOINCREMENT, -- for unique record identification
                country TEXT NOT NULL,
                country_code TEXT,
                region TEXT,
                year INTEGER NOT NULL,
                life_expect REAL,
                life_exp60 REAL,
                adult_mortality REAL,
                infant_mort REAL,
                "age1-4mort" REAL,
                alcohol REAL,
                bmi REAL,
                "age5-19thinness" REAL,
                "age5-19obesity" REAL,
                hepatitis REAL,
                measles REAL,
                polio REAL,
                diphtheria REAL,
                basic_water REAL,
                doctors REAL,
                hospitals REAL,
                gni_capita REAL,
                "gghe-d" REAL,
                che_gdp REAL,
                une_pop REAL,
                une_infant REAL,
                une_life REAL,
                une_hiv REAL,
                une_gni REAL,
                une_poverty REAL,
                une_edu_spend REAL,
                une_literacy REAL,
                une_school REAL,
                UNIQUE(country, year) -- Prevent duplicate entries
            )
        """)
        
        # Create indices for common query patterns
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_country -- B-tree index for faster country lookups
            ON life_expectancy(country)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_year -- B-tree index for faster year-based queries
            ON life_expectancy(year)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_region -- B-tree index for region-based queries
            ON life_expectancy(region)
        """)
        
        conn.commit()
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to create database: {e}")
    finally:
        if conn:
            conn.close()


def get_connection(db_path: str) -> sqlite3.Connection:
    """
    Get a SQLite database connection.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        SQLite connection object with row_factory enabled
        
    Raises:
        ValueError: If db_path is empty
        sqlite3.Error: If connection fails
        FileNotFoundError: If database file doesn't exist
    """
    # different with create_database, here we only need to report an error rather than create the file
    # so we don't need the db_dir check and creation
    if not db_path:
        raise ValueError("Database path cannot be empty")
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        # Enable dict-like row access for easier data manipulation
        conn.row_factory = sqlite3.Row # remains the relationship between keys and values
        return conn
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


@contextmanager
def _get_connection_context(db_path: str):
    """Context manager for database connections to ensure proper cleanup."""
    conn = get_connection(db_path)  # Reuse get_connection() - DRY principle
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def load_data_to_db(db_path: str, data: List[Dict[str, Any]]) -> None:
    """
    Load cleaned data into the database.
    
    Args:
        db_path: Path to the SQLite database file
        data: List of dictionaries containing cleaned data
        
    Raises:
        ValueError: If data is None or db_path is empty
        sqlite3.Error: If database operations fail
    """
    if not db_path:
        raise ValueError("Database path cannot be empty")
    
    if data is None:
        raise ValueError("Data cannot be None")
    
    if not data:
        return  # Empty list is valid, just no-op
    
    try:
        with _get_connection_context(db_path) as conn:
            cursor = conn.cursor()
            
            # Extract column names from the first record
            columns = list(data[0].keys())
            # 自动获取：['country', 'country_code', 'region', ..., 'une_school']

            # Properly quote column names that contain special characters
            quoted_columns = [f'"{col}"' if '-' in col else col for col in columns]
            placeholders = ", ".join(["?"] * len(columns)) #“?, ?, ?, ?, ?”
            # 生成：'?, ?, ?, ?, ?, ?, ?, ..., ?' (32个问号)

            
            column_names = ", ".join(quoted_columns) 
            # 生成：'country, country_code, region, year, ...'

            # Use INSERT OR REPLACE to handle duplicates gracefully
            insert_sql = f"INSERT OR REPLACE INTO life_expectancy ({column_names}) VALUES ({placeholders})"
            
            # Batch insert for better performance
            records = []
            for record in data: # get each dictionary in the list
                # Ensure all columns are present, use None for missing
                values = [record.get(col) for col in columns] 
                # get values according to the column names in sequence
                records.append(values) 
                # e.g. 
                # records = [
                #     ['China', 'CHN', 'Asia', 2015, 76.1, ...], 
                #     ['India', 'IND', 'Asia', 2015, 68.3, ...], ...]
                # ]
            
            cursor.executemany(insert_sql, records)
            
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to load data to database: {e}")


def get_all_records(db_path: str) -> List[Dict[str, Any]]:
    """
    Retrieve all records from the database.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        List of dictionaries representing database rows
        
    Raises:
        ValueError: If db_path is empty
        sqlite3.Error: If query fails
    """
    if not db_path:
        raise ValueError("Database path cannot be empty")
    
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM life_expectancy ORDER BY country, year")
        rows = cursor.fetchall()
        
        # Convert Row objects to dictionaries
        records = [dict(row) for row in rows]
        
        return records
        
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to retrieve records: {e}")
    finally:
        conn.close()


def get_records_by_country(db_path: str, country: str) -> List[Dict[str, Any]]:
    """
    Retrieve records for a specific country.
    
    Args:
        db_path: Path to the SQLite database file
        country: Country name to filter by
        
    Returns:
        List of dictionaries for the specified country
    """
    if not db_path or not country:
        raise ValueError("Database path and country cannot be empty")
    
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM life_expectancy WHERE country = ? ORDER BY year",
            (country,) 
            # the data must be in tuple form and single element tuple needs a comma
        )
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
        
    finally:
        conn.close()


def get_records_by_year_range(db_path: str, start_year: int, end_year: int) -> List[Dict[str, Any]]:
    """
    Retrieve records within a year range.
    
    Args:
        db_path: Path to the SQLite database file
        start_year: Starting year (inclusive)
        end_year: Ending year (inclusive)
        
    Returns:
        List of dictionaries within the year range
    """
    if not db_path:
        raise ValueError("Database path cannot be empty")
    
    if start_year > end_year:
        raise ValueError("Start year cannot be greater than end year")
    
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM life_expectancy WHERE year BETWEEN ? AND ? ORDER BY year, country",
            (start_year, end_year)
        )
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
        
    finally:
        conn.close()


# ============================================================================
# CRUD Operations - Generalized Design
# ============================================================================

def _quote_field_name(field: str) -> str:
    """
    Quote field name if it contains hyphens for SQL compatibility.
    
    Args:
        field: Field name to potentially quote
        
    Returns:
        Quoted field name if contains hyphen, otherwise original name
        
    Example:
        >>> _quote_field_name("country")
        'country'
        >>> _quote_field_name("health-spending")
        '"health-spending"'
    """
    return f'"{field}"' if '-' in field else field


def _build_where_clause(filters: Dict[str, Any]) -> tuple:
    """
    Build SQL WHERE clause from filters dictionary.
    
    Args:
        filters: Dictionary of field names and values to filter by
        
    Returns:
        Tuple of (where_clause_string, values_tuple)
        
    Example:
        >>> _build_where_clause({"country": "China", "year": 2015})
        ("WHERE country = ? AND year = ?", ("China", 2015))
    """
    if not filters:
        return "", ()
    
    conditions = []
    values = []
    
    for field, value in filters.items():
        field_name = _quote_field_name(field)
        conditions.append(f"{field_name} = ?")
        values.append(value)
    
    where_clause = "WHERE " + " AND ".join(conditions)
    return where_clause, tuple(values)


def create_record(db_path: str, record: Dict[str, Any]) -> None:
    """
    Create a new record in the database.
    
    Args:
        db_path: Path to the SQLite database file
        record: Dictionary containing the new record data
        
    Raises:
        ValueError: If record already exists (duplicate country-year) or missing required fields
        sqlite3.Error: If database operation fails
        
    Note:
        This enforces uniqueness. Use load_data_to_db() for INSERT OR REPLACE behavior.
    """
    if not db_path:
        raise ValueError("Database path cannot be empty")
    
    if not record:
        raise ValueError("Record cannot be empty")
    
    # Check required fields
    required_fields = ["country", "year", "region", "life_expect"]
    missing_fields = [field for field in required_fields if field not in record]
    if missing_fields:
        raise ValueError(
            f"Record must contain required fields: {', '.join(missing_fields)}. "
            "Core fields (country, year, region, life_expect) are mandatory for data quality."
        )
    
    # Check if record already exists
    existing = get_records_by_country(db_path, record["country"])
    for rec in existing:
        if rec["year"] == record["year"]:
            raise ValueError(
                f"Record for {record['country']} in year {record['year']} already exists. "
                "Use update_record() to modify existing records."
            )
    
    # Insert new record using load_data_to_db
    try:
        with _get_connection_context(db_path) as conn:
            cursor = conn.cursor()
            
            columns = list(record.keys())
            quoted_columns = [_quote_field_name(col) for col in columns]
            placeholders = ", ".join(["?"] * len(columns))
            column_names = ", ".join(quoted_columns)
            
            insert_sql = f"INSERT INTO life_expectancy ({column_names}) VALUES ({placeholders})"
            cursor.execute(insert_sql, tuple(record.values()))
            
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Failed to create record: {e}")


def update_record(db_path: str, country: str, year: int, updates: Dict[str, Any]) -> None:
    """
    Update specific fields for a country-year record.
    
    Args:
        db_path: Path to the SQLite database file
        country: Country name to identify the record
        year: Year to identify the record
        updates: Dictionary of field names and new values to update
        
    Raises:
        ValueError: If no record found or updates dict is empty
        sqlite3.Error: If database operation fails
        
    Example:
        >>> update_record("data.db", "China", 2015, {"life_expect": 76.5, "bmi": 24.0})
    """
    if not db_path:
        raise ValueError("Database path cannot be empty")
    
    if not updates:
        raise ValueError("Updates dictionary cannot be empty")
    
    # Check if record exists
    existing = get_records_by_country(db_path, country)
    found = any(rec["year"] == year for rec in existing)
    if not found:
        raise ValueError(f"No record found for {country} in year {year}")
    
    try:
        with _get_connection_context(db_path) as conn:
            cursor = conn.cursor()
            
            # Build SET clause
            set_parts = []
            values = []
            for field, value in updates.items():
                field_name = _quote_field_name(field)
                set_parts.append(f"{field_name} = ?")
                values.append(value)
            
            set_clause = ", ".join(set_parts)
            values.extend([country, year])  # Add WHERE parameters
            
            update_sql = f"UPDATE life_expectancy SET {set_clause} WHERE country = ? AND year = ?"
            cursor.execute(update_sql, tuple(values))
            
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to update record: {e}")


def delete_record(db_path: str, country: str, year: int) -> None:
    """
    Delete a specific country-year record.
    
    Args:
        db_path: Path to the SQLite database file
        country: Country name to identify the record
        year: Year to identify the record
        
    Raises:
        ValueError: If no record found to delete
        sqlite3.Error: If database operation fails
    """
    # Use generalized delete_records function
    deleted = delete_records(db_path, filters={"country": country, "year": year})
    if deleted == 0:
        raise ValueError(f"No record found for {country} in year {year}")


def delete_records(db_path: str, filters: Dict[str, Any]) -> int:
    """
    Delete records matching the given filters (GENERALIZED).
    
    Args:
        db_path: Path to the SQLite database file
        filters: Dictionary of field names and values to filter by
        
    Returns:
        Number of records deleted
        
    Raises:
        ValueError: If filters is empty
        sqlite3.Error: If database operation fails
        
    Examples:
        >>> delete_records("data.db", {"country": "China"})  # Delete all China records
        >>> delete_records("data.db", {"region": "Asia"})    # Delete all Asia records
        >>> delete_records("data.db", {"country": "China", "year": 2015})  # Delete specific record
    """
    if not db_path:
        raise ValueError("Database path cannot be empty")
    
    if not filters:
        raise ValueError("Filters cannot be empty (prevents accidental deletion of all records)")
    
    try:
        with _get_connection_context(db_path) as conn:
            cursor = conn.cursor()
            
            where_clause, values = _build_where_clause(filters)
            delete_sql = f"DELETE FROM life_expectancy {where_clause}"
            
            cursor.execute(delete_sql, values)
            return cursor.rowcount
            
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to delete records: {e}")


def delete_records_by_country(db_path: str, country: str) -> int:
    """
    Delete all records for a specific country.
    
    Args:
        db_path: Path to the SQLite database file
        country: Country name to delete all records for
        
    Returns:
        Number of records deleted
        
    Note:
        This is a convenience wrapper around delete_records().
    """
    return delete_records(db_path, filters={"country": country})
