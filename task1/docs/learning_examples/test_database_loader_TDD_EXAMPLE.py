"""
TDD Example: Tests written BEFORE implementing database_loader_robust.py

This is how the test file should look BEFORE you write any implementation.
These tests define the expected behavior and API design.

TDD Workflow:
1. Write this test file first (defines what you want)
2. Run tests (they will FAIL - that's expected!)
3. Write minimal code to make tests pass
4. Refactor and improve
5. Repeat

All tests here will fail initially because database_loader_robust.py doesn't exist yet.
"""

import os
import sqlite3
import pytest

# ============================================================================
# Step 1: Define what functions we WANT to exist
# ============================================================================
# At this point, database_loader_robust.py doesn't exist yet!
# We're designing the API through tests.

# from task1.database_loader_robust import (  # This will fail initially!
#     create_database,
#     load_data_to_db,
#     get_connection,
#     get_all_records,
#     get_records_by_country,
#     get_records_by_year_range
# )

# For now, we comment out the import and focus on writing test logic


# ============================================================================
# Step 2: Set up test fixtures
# ============================================================================

TEST_DB_PATH = "task1/data/test_tdd_database.db"


@pytest.fixture
def clean_test_db():
    """Remove test database before and after each test."""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    yield TEST_DB_PATH
    
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return [
        {
            "country": "China",
            "country_code": "CHN",
            "region": "Asia",
            "year": 2015,
            "life_expect": 76.5
        },
        {
            "country": "USA",
            "country_code": "USA",
            "region": "Americas",
            "year": 2015,
            "life_expect": 78.9
        }
    ]


# ============================================================================
# Step 3: Write tests that define EXPECTED behavior
# ============================================================================

def test_create_database_should_create_file(clean_test_db):
    """
    REQUIREMENT: create_database() should create a .db file
    
    This test defines what we expect:
    - Function name: create_database
    - Parameter: db_path (string)
    - Behavior: Creates a SQLite database file
    """
    # This will fail initially because create_database doesn't exist
    # create_database(TEST_DB_PATH)
    # assert os.path.exists(TEST_DB_PATH)
    
    # For demonstration, we skip this test until implementation
    pytest.skip("Implementation not yet written - TDD red phase")


def test_create_database_should_create_table_with_correct_schema(clean_test_db):
    """
    REQUIREMENT: Database should have life_expectancy table
    
    Expected schema:
    - Table name: life_expectancy
    - Columns: country, year, life_expect, etc.
    - Constraints: UNIQUE(country, year)
    """
    # create_database(TEST_DB_PATH)
    # 
    # conn = sqlite3.connect(TEST_DB_PATH)
    # cursor = conn.cursor()
    # 
    # # Verify table exists
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    # tables = [row[0] for row in cursor.fetchall()]
    # assert 'life_expectancy' in tables
    # 
    # # Verify UNIQUE constraint exists
    # cursor.execute("PRAGMA index_list(life_expectancy)")
    # indexes = cursor.fetchall()
    # assert len(indexes) > 0  # Should have at least the UNIQUE constraint
    # 
    # conn.close()
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_create_database_should_create_btree_indexes(clean_test_db):
    """
    REQUIREMENT: Database should have B-Tree indexes for performance
    
    Expected indexes:
    - idx_country (on country column)
    - idx_year (on year column)
    - idx_region (on region column)
    
    Why? To speed up common queries (country filtering, year ranges)
    """
    # create_database(TEST_DB_PATH)
    # 
    # conn = sqlite3.connect(TEST_DB_PATH)
    # cursor = conn.cursor()
    # 
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    # indexes = [row[0] for row in cursor.fetchall()]
    # 
    # assert 'idx_country' in indexes
    # assert 'idx_year' in indexes
    # assert 'idx_region' in indexes
    # 
    # conn.close()
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_get_connection_should_return_connection_with_row_factory(clean_test_db):
    """
    REQUIREMENT: get_connection() should return configured connection
    
    Expected behavior:
    - Returns sqlite3.Connection object
    - Has row_factory = sqlite3.Row (for dict-like access)
    - Validates that database file exists
    """
    # create_database(TEST_DB_PATH)
    # 
    # conn = get_connection(TEST_DB_PATH)
    # 
    # assert isinstance(conn, sqlite3.Connection)
    # assert conn.row_factory == sqlite3.Row
    # 
    # conn.close()
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_get_connection_should_raise_error_for_missing_database():
    """
    REQUIREMENT: get_connection() should fail gracefully
    
    Expected error handling:
    - Raises FileNotFoundError if database doesn't exist
    - Clear error message
    """
    # with pytest.raises(FileNotFoundError):
    #     get_connection("nonexistent_database.db")
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_get_connection_should_raise_error_for_empty_path():
    """
    REQUIREMENT: Input validation
    
    Expected:
    - Raises ValueError for empty string
    - Defensive programming
    """
    # with pytest.raises(ValueError):
    #     get_connection("")
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_load_data_to_db_should_insert_records(clean_test_db, sample_data):
    """
    REQUIREMENT: load_data_to_db() should insert data
    
    Expected behavior:
    - Accepts db_path and list of dicts
    - Inserts all records into database
    - Uses batch insert (executemany) for performance
    """
    # create_database(TEST_DB_PATH)
    # load_data_to_db(TEST_DB_PATH, sample_data)
    # 
    # conn = sqlite3.connect(TEST_DB_PATH)
    # cursor = conn.cursor()
    # cursor.execute("SELECT COUNT(*) FROM life_expectancy")
    # count = cursor.fetchone()[0]
    # 
    # assert count == 2
    # conn.close()
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_load_data_to_db_should_use_context_manager(clean_test_db, sample_data):
    """
    REQUIREMENT: Resource management with context manager
    
    Expected:
    - Uses 'with' statement for automatic cleanup
    - Commits transaction on success
    - Rolls back on failure
    - Always closes connection
    
    Design decision: Use context manager to prevent resource leaks
    """
    # This test verifies the behavior, not the implementation
    # Even if an error occurs, connection should be closed
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_load_data_to_db_should_handle_duplicates(clean_test_db):
    """
    REQUIREMENT: Handle duplicate records gracefully
    
    Expected behavior:
    - Use INSERT OR REPLACE strategy
    - If (country, year) already exists, update the record
    - Don't crash on duplicates
    
    Why? Data might be reloaded multiple times during development
    """
    # create_database(TEST_DB_PATH)
    # 
    # # Insert initial data
    # initial = [{"country": "China", "year": 2015, "life_expect": 76.0}]
    # load_data_to_db(TEST_DB_PATH, initial)
    # 
    # # Insert duplicate with different value
    # duplicate = [{"country": "China", "year": 2015, "life_expect": 76.5}]
    # load_data_to_db(TEST_DB_PATH, duplicate)
    # 
    # # Should have only 1 record with updated value
    # conn = sqlite3.connect(TEST_DB_PATH)
    # cursor = conn.cursor()
    # cursor.execute("SELECT COUNT(*), life_expect FROM life_expectancy")
    # count, life_expect = cursor.fetchone()
    # 
    # assert count == 1
    # assert life_expect == 76.5
    # conn.close()
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_load_data_to_db_should_validate_inputs(clean_test_db):
    """
    REQUIREMENT: Input validation
    
    Expected error handling:
    - Raise ValueError if data is None
    - Handle empty list gracefully (no error, just no-op)
    - Raise ValueError if db_path is empty
    """
    # create_database(TEST_DB_PATH)
    # 
    # # Test 1: None data should raise error
    # with pytest.raises(ValueError):
    #     load_data_to_db(TEST_DB_PATH, None)
    # 
    # # Test 2: Empty list should not raise error
    # load_data_to_db(TEST_DB_PATH, [])  # Should succeed
    # 
    # # Test 3: Empty path should raise error
    # with pytest.raises(ValueError):
    #     load_data_to_db("", [{"country": "China"}])
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_get_all_records_should_return_list_of_dicts(clean_test_db, sample_data):
    """
    REQUIREMENT: Query function returns user-friendly format
    
    Expected:
    - Returns List[Dict[str, Any]]
    - Each dict represents one row
    - Dict keys are column names
    - Values are properly typed
    
    Why dict instead of tuple? Easier to work with, self-documenting
    """
    # create_database(TEST_DB_PATH)
    # load_data_to_db(TEST_DB_PATH, sample_data)
    # 
    # records = get_all_records(TEST_DB_PATH)
    # 
    # assert isinstance(records, list)
    # assert len(records) == 2
    # assert isinstance(records[0], dict)
    # assert records[0]["country"] == "China"
    # assert records[0]["year"] == 2015
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_get_all_records_should_return_sorted_data(clean_test_db, sample_data):
    """
    REQUIREMENT: Data should be sorted for consistency
    
    Expected sorting:
    - ORDER BY country, year
    - Predictable output order
    
    Why? Makes results easier to read and test
    """
    # create_database(TEST_DB_PATH)
    # load_data_to_db(TEST_DB_PATH, sample_data)
    # 
    # records = get_all_records(TEST_DB_PATH)
    # 
    # # Should be sorted: China first, then USA
    # assert records[0]["country"] == "China"
    # assert records[1]["country"] == "USA"
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_get_records_by_country_should_filter_correctly(clean_test_db, sample_data):
    """
    REQUIREMENT: Country-based filtering
    
    Expected behavior:
    - Parameter: country name (string)
    - Returns only records matching that country
    - Uses idx_country index for performance
    - SQL: WHERE country = ?
    """
    # create_database(TEST_DB_PATH)
    # load_data_to_db(TEST_DB_PATH, sample_data)
    # 
    # china_records = get_records_by_country(TEST_DB_PATH, "China")
    # 
    # assert len(china_records) == 1
    # assert china_records[0]["country"] == "China"
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_get_records_by_country_should_use_parameterized_query(clean_test_db):
    """
    REQUIREMENT: SQL injection prevention
    
    Expected:
    - Uses ? placeholders
    - NOT f-strings or string concatenation
    - Security best practice
    
    This test verifies that malicious input doesn't break the database
    """
    # create_database(TEST_DB_PATH)
    # 
    # # Malicious input attempt
    # malicious = "China'; DROP TABLE life_expectancy; --"
    # 
    # # Should safely return empty results, not execute the SQL injection
    # records = get_records_by_country(TEST_DB_PATH, malicious)
    # 
    # # Database should still exist and be intact
    # assert os.path.exists(TEST_DB_PATH)
    # conn = sqlite3.connect(TEST_DB_PATH)
    # cursor = conn.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    # tables = [row[0] for row in cursor.fetchall()]
    # assert 'life_expectancy' in tables  # Table should still exist
    # conn.close()
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_get_records_by_year_range_should_filter_inclusively(clean_test_db):
    """
    REQUIREMENT: Year range filtering
    
    Expected behavior:
    - Parameters: start_year, end_year (integers)
    - Returns records where start_year <= year <= end_year
    - SQL: WHERE year BETWEEN ? AND ?
    - Both bounds are inclusive
    """
    # create_database(TEST_DB_PATH)
    # 
    # test_data = [
    #     {"country": "China", "year": 2014, "life_expect": 75.0},
    #     {"country": "China", "year": 2015, "life_expect": 76.0},
    #     {"country": "China", "year": 2016, "life_expect": 77.0},
    #     {"country": "China", "year": 2017, "life_expect": 78.0},
    # ]
    # load_data_to_db(TEST_DB_PATH, test_data)
    # 
    # # Query for 2015-2016 (inclusive)
    # records = get_records_by_year_range(TEST_DB_PATH, 2015, 2016)
    # 
    # assert len(records) == 2
    # assert all(2015 <= r["year"] <= 2016 for r in records)
    
    pytest.skip("Implementation not yet written - TDD red phase")


def test_get_records_by_year_range_should_validate_range(clean_test_db):
    """
    REQUIREMENT: Input validation
    
    Expected:
    - Raise ValueError if start_year > end_year
    - Defensive programming to prevent logical errors
    """
    # create_database(TEST_DB_PATH)
    # 
    # with pytest.raises(ValueError):
    #     get_records_by_year_range(TEST_DB_PATH, 2020, 2015)  # Invalid range
    
    pytest.skip("Implementation not yet written - TDD red phase")


# ============================================================================
# Step 4: Run tests to see them FAIL (Red phase of TDD)
# ============================================================================
# At this point, ALL tests should be skipped or fail
# This is GOOD - it means we know what to build!

# Next steps in TDD:
# 1. Uncomment the imports
# 2. Uncomment one test at a time
# 3. Write minimal code to make that test pass
# 4. Refactor
# 5. Move to next test

"""
TDD Cycle Summary:

RED Phase (Current):
- Write tests first (this file)
- All tests fail/skip
- This defines the API and requirements

GREEN Phase (Next):
- Write minimal code to make one test pass
- Don't over-engineer
- Just make it work

REFACTOR Phase (After):
- Improve code quality
- Add error handling
- Optimize performance
- But tests still pass!

Benefits:
- Tests document expected behavior
- Confidence when refactoring
- No untested code
- Clear requirements from the start
"""
