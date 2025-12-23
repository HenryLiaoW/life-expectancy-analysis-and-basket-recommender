"""
Comprehensive test suite for database_loader module (TDD RED Phase).

This test suite defines the expected behavior before implementation:
- Database schema creation with B-Tree indexes
- Robust connection management with row_factory
- Data loading with duplicate handling and validation
- Query functions (all records, by country, by year range)
- Input validation and error handling

Run with: pytest task1/tests/test_database_loader_NEW.py -v
"""

import os
import sqlite3
import pytest
from task1.database_loader import (
    create_database,
    load_data_to_db,
    get_all_records,
    get_connection,
    get_records_by_country,
    get_records_by_year_range
)


# Test database path - separate from production database
TEST_DB_PATH = "task1/data/test_life_expectancy.db"


@pytest.fixture
def clean_test_db():
    """Remove test database before and after each test to ensure isolation."""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    yield TEST_DB_PATH
    
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture
def sample_data():
    """Sample health data for testing."""
    return [
        {
            "country": "China",
            "country_code": "CHN",
            "region": "Asia",
            "year": 2015,
            "life_expect": 76.5,
            "adult_mortality": 120,
            "infant_mort": 8.0
        },
        {
            "country": "China",
            "country_code": "CHN",
            "region": "Asia",
            "year": 2016,
            "life_expect": 76.8,
            "adult_mortality": 115,
            "infant_mort": 7.5
        },
        {
            "country": "India",
            "country_code": "IND",
            "region": "Asia",
            "year": 2015,
            "life_expect": 68.3,
            "adult_mortality": 190,
            "infant_mort": 37.0
        }
    ]


# ============================================================================
# Database Creation Tests
# ============================================================================

def test_create_database_creates_file(clean_test_db):
    """Test that create_database creates a SQLite database file."""
    create_database(TEST_DB_PATH)
    assert os.path.exists(TEST_DB_PATH)


def test_create_database_creates_table(clean_test_db):
    """Test that create_database creates the life_expectancy table."""
    create_database(TEST_DB_PATH)
    
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='life_expectancy'")
    result = cursor.fetchone()
    
    assert result is not None
    conn.close()


def test_create_database_creates_indexes(clean_test_db):
    """Test that B-Tree indexes are created for query optimization."""
    create_database(TEST_DB_PATH)
    
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = [row[0] for row in cursor.fetchall()]
    
    assert 'idx_country' in indexes, "Missing B-Tree index on country"
    assert 'idx_year' in indexes, "Missing B-Tree index on year"
    assert 'idx_region' in indexes, "Missing B-Tree index on region"
    
    conn.close()


def test_create_database_validates_empty_path():
    """Test that create_database rejects empty path."""
    with pytest.raises(ValueError, match="path cannot be empty"):
        create_database("")


# ============================================================================
# Connection Management Tests  
# ============================================================================

def test_get_connection_returns_valid_connection(clean_test_db):
    """Test that get_connection returns a valid SQLite connection."""
    create_database(TEST_DB_PATH)
    
    conn = get_connection(TEST_DB_PATH)
    
    assert conn is not None
    assert isinstance(conn, sqlite3.Connection)
    
    conn.close()


def test_get_connection_sets_row_factory(clean_test_db):
    """Test that connection has Row factory for dict-like access."""
    create_database(TEST_DB_PATH)
    
    conn = get_connection(TEST_DB_PATH)
    assert conn.row_factory == sqlite3.Row
    
    conn.close()


def test_get_connection_raises_error_for_nonexistent_db():
    """Test that get_connection fails for missing database."""
    with pytest.raises(FileNotFoundError):
        get_connection("nonexistent_database.db")


def test_get_connection_validates_empty_path():
    """Test that get_connection rejects empty path."""
    with pytest.raises(ValueError, match="path cannot be empty"):
        get_connection("")


# ============================================================================
# Data Loading Tests
# ============================================================================

def test_load_data_to_db_inserts_records(clean_test_db, sample_data):
    """Test that load_data_to_db successfully inserts all records."""
    create_database(TEST_DB_PATH)
    load_data_to_db(TEST_DB_PATH, sample_data)
    
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM life_expectancy")
    count = cursor.fetchone()[0]
    
    assert count == 3, f"Expected 3 records, found {count}"
    conn.close()


def test_load_data_to_db_handles_duplicates(clean_test_db):
    """Test that INSERT OR REPLACE handles duplicate country+year."""
    create_database(TEST_DB_PATH)
    
    initial = [{"country": "China", "year": 2015, "life_expect": 76.0}]
    load_data_to_db(TEST_DB_PATH, initial)
    
    updated = [{"country": "China", "year": 2015, "life_expect": 76.5}]
    load_data_to_db(TEST_DB_PATH, updated)
    
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), life_expect FROM life_expectancy WHERE country='China' AND year=2015")
    count, life_expect = cursor.fetchone()
    
    assert count == 1, "Should have only 1 record (replaced)"
    assert life_expect == 76.5, "Value should be updated"
    conn.close()


def test_load_data_raises_error_for_none_data(clean_test_db):
    """Test that load_data_to_db validates input data."""
    create_database(TEST_DB_PATH)
    
    with pytest.raises(ValueError, match="Data cannot be None"):
        load_data_to_db(TEST_DB_PATH, None)


def test_load_data_handles_empty_list(clean_test_db):
    """Test that empty data list is handled gracefully."""
    create_database(TEST_DB_PATH)
    
    load_data_to_db(TEST_DB_PATH, [])
    
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM life_expectancy")
    count = cursor.fetchone()[0]
    
    assert count == 0
    conn.close()


def test_load_data_validates_db_path(sample_data):
    """Test that load_data_to_db validates database path."""
    with pytest.raises(ValueError, match="path cannot be empty"):
        load_data_to_db("", sample_data)


# ============================================================================
# Query Tests
# ============================================================================

def test_get_all_records_returns_list_of_dicts(clean_test_db, sample_data):
    """Test that get_all_records returns data as list of dicts."""
    create_database(TEST_DB_PATH)
    load_data_to_db(TEST_DB_PATH, sample_data)
    
    records = get_all_records(TEST_DB_PATH)
    
    assert isinstance(records, list)
    assert len(records) == 3
    assert isinstance(records[0], dict)
    assert "country" in records[0]
    assert "year" in records[0]
    assert "life_expect" in records[0]


def test_get_all_records_returns_sorted(clean_test_db, sample_data):
    """Test that records are sorted by country then year."""
    create_database(TEST_DB_PATH)
    load_data_to_db(TEST_DB_PATH, sample_data)
    
    records = get_all_records(TEST_DB_PATH)
    
    # Should be: China 2015, China 2016, India 2015
    assert records[0]["country"] == "China"
    assert records[0]["year"] == 2015
    assert records[1]["country"] == "China"
    assert records[1]["year"] == 2016
    assert records[2]["country"] == "India"


def test_get_records_by_country_filters_correctly(clean_test_db, sample_data):
    """Test that get_records_by_country returns only matching records."""
    create_database(TEST_DB_PATH)
    load_data_to_db(TEST_DB_PATH, sample_data)
    
    china_records = get_records_by_country(TEST_DB_PATH, "China")
    
    assert len(china_records) == 2
    assert all(r["country"] == "China" for r in china_records)
    assert china_records[0]["year"] == 2015
    assert china_records[1]["year"] == 2016


def test_get_records_by_country_returns_empty_for_nonexistent(clean_test_db, sample_data):
    """Test that non-existent country returns empty list."""
    create_database(TEST_DB_PATH)
    load_data_to_db(TEST_DB_PATH, sample_data)
    
    records = get_records_by_country(TEST_DB_PATH, "Nonexistent")
    
    assert isinstance(records, list)
    assert len(records) == 0


def test_get_records_by_year_range_filters_correctly(clean_test_db):
    """Test that get_records_by_year_range filters by year range."""
    create_database(TEST_DB_PATH)
    
    data = [
        {"country": "Test", "year": 2014, "life_expect": 74.0},
        {"country": "Test", "year": 2015, "life_expect": 75.0},
        {"country": "Test", "year": 2016, "life_expect": 76.0},
        {"country": "Test", "year": 2017, "life_expect": 77.0},
    ]
    load_data_to_db(TEST_DB_PATH, data)
    
    records = get_records_by_year_range(TEST_DB_PATH, 2015, 2016)
    
    assert len(records) == 2
    assert all(2015 <= r["year"] <= 2016 for r in records)


def test_get_records_by_year_range_inclusive(clean_test_db):
    """Test that BETWEEN includes both boundary years."""
    create_database(TEST_DB_PATH)
    
    data = [
        {"country": "Test", "year": 2015, "life_expect": 70.0},
        {"country": "Test", "year": 2020, "life_expect": 75.0},
    ]
    load_data_to_db(TEST_DB_PATH, data)
    
    records = get_records_by_year_range(TEST_DB_PATH, 2015, 2020)
    
    assert len(records) == 2, "Both boundaries should be included"


def test_get_records_by_year_range_raises_error_for_invalid_range(clean_test_db):
    """Test that invalid year range raises ValueError."""
    create_database(TEST_DB_PATH)
    
    with pytest.raises(ValueError, match="Start year cannot be greater than end year"):
        get_records_by_year_range(TEST_DB_PATH, 2020, 2015)


# ============================================================================
# CRUD Operations Tests (TDD RED Phase)
# ============================================================================

def test_update_record_by_country_year_updates_single_field(clean_test_db):
    """Test updating a specific field for a country-year record."""
    from task1.database_loader import update_record
    
    create_database(TEST_DB_PATH)
    
    # Insert initial data
    data = [
        {"country": "China", "year": 2015, "life_expect": 76.0, "bmi": 23.5},
    ]
    load_data_to_db(TEST_DB_PATH, data)
    
    # Update life_expect value
    update_record(TEST_DB_PATH, country="China", year=2015, updates={"life_expect": 76.5})
    
    # Verify update
    records = get_records_by_country(TEST_DB_PATH, "China")
    assert len(records) == 1
    assert records[0]["life_expect"] == 76.5
    assert records[0]["bmi"] == 23.5  # Other fields unchanged


def test_update_record_updates_multiple_fields(clean_test_db):
    """Test updating multiple fields in one operation."""
    from task1.database_loader import update_record
    
    create_database(TEST_DB_PATH)
    
    data = [
        {"country": "India", "year": 2016, "life_expect": 68.0, "bmi": 21.5, "alcohol": 5.7},
    ]
    load_data_to_db(TEST_DB_PATH, data)
    
    # Update multiple fields
    update_record(TEST_DB_PATH, country="India", year=2016, 
                  updates={"life_expect": 68.5, "bmi": 21.8})
    
    # Verify updates
    records = get_records_by_country(TEST_DB_PATH, "India")
    assert records[0]["life_expect"] == 68.5
    assert records[0]["bmi"] == 21.8
    assert records[0]["alcohol"] == 5.7  # Unchanged field


def test_update_record_raises_error_for_nonexistent_record(clean_test_db):
    """Test that updating non-existent record raises ValueError."""
    from task1.database_loader import update_record
    
    create_database(TEST_DB_PATH)
    
    with pytest.raises(ValueError, match="No record found"):
        update_record(TEST_DB_PATH, country="Nonexistent", year=2015, 
                      updates={"life_expect": 80.0})


def test_update_record_validates_empty_updates(clean_test_db):
    """Test that empty updates dict raises ValueError."""
    from task1.database_loader import update_record
    
    create_database(TEST_DB_PATH)
    
    data = [{"country": "China", "year": 2015, "life_expect": 76.0}]
    load_data_to_db(TEST_DB_PATH, data)
    
    with pytest.raises(ValueError, match="Updates dictionary cannot be empty"):
        update_record(TEST_DB_PATH, country="China", year=2015, updates={})


def test_delete_record_by_country_year_removes_single_record(clean_test_db):
    """Test deleting a specific country-year record."""
    from task1.database_loader import delete_record
    
    create_database(TEST_DB_PATH)
    
    data = [
        {"country": "China", "year": 2015, "life_expect": 76.0},
        {"country": "China", "year": 2016, "life_expect": 76.5},
    ]
    load_data_to_db(TEST_DB_PATH, data)
    
    # Delete 2015 record
    delete_record(TEST_DB_PATH, country="China", year=2015)
    
    # Verify deletion
    records = get_records_by_country(TEST_DB_PATH, "China")
    assert len(records) == 1
    assert records[0]["year"] == 2016


def test_delete_record_raises_error_for_nonexistent_record(clean_test_db):
    """Test that deleting non-existent record raises ValueError."""
    from task1.database_loader import delete_record
    
    create_database(TEST_DB_PATH)
    
    with pytest.raises(ValueError, match="No record found"):
        delete_record(TEST_DB_PATH, country="Nonexistent", year=2015)


def test_delete_all_records_for_country_removes_multiple_records(clean_test_db):
    """Test deleting all records for a specific country."""
    from task1.database_loader import delete_records_by_country
    
    create_database(TEST_DB_PATH)
    
    data = [
        {"country": "China", "year": 2015, "life_expect": 76.0},
        {"country": "China", "year": 2016, "life_expect": 76.5},
        {"country": "India", "year": 2015, "life_expect": 68.0},
    ]
    load_data_to_db(TEST_DB_PATH, data)
    
    # Delete all China records
    deleted_count = delete_records_by_country(TEST_DB_PATH, "China")
    
    assert deleted_count == 2
    
    # Verify China records removed
    china_records = get_records_by_country(TEST_DB_PATH, "China")
    assert len(china_records) == 0
    
    # Verify India record still exists
    india_records = get_records_by_country(TEST_DB_PATH, "India")
    assert len(india_records) == 1


def test_delete_records_by_country_returns_zero_for_nonexistent(clean_test_db):
    """Test that deleting non-existent country returns 0."""
    from task1.database_loader import delete_records_by_country
    
    create_database(TEST_DB_PATH)
    
    deleted_count = delete_records_by_country(TEST_DB_PATH, "Nonexistent")
    assert deleted_count == 0


def test_create_record_inserts_new_record(clean_test_db):
    """Test creating a new record in the database."""
    from task1.database_loader import create_record
    
    create_database(TEST_DB_PATH)
    
    # Create new record
    new_record = {
        "country": "Japan",
        "year": 2015,
        "life_expect": 83.5,
        "bmi": 22.5,
        "region": "Asia"
    }
    create_record(TEST_DB_PATH, new_record)
    
    # Verify insertion
    records = get_records_by_country(TEST_DB_PATH, "Japan")
    assert len(records) == 1
    assert records[0]["life_expect"] == 83.5


def test_create_record_raises_error_for_duplicate(clean_test_db):
    """Test that creating duplicate country-year raises ValueError."""
    from task1.database_loader import create_record
    
    create_database(TEST_DB_PATH)
    
    record = {"country": "China", "year": 2015, "life_expect": 76.0}
    load_data_to_db(TEST_DB_PATH, [record])
    
    # Attempt to create duplicate
    with pytest.raises(ValueError, match="already exists"):
        create_record(TEST_DB_PATH, record)


# ============================================================================
# Generalized CRUD Tests (Flexible Filtering)
# ============================================================================

def test_delete_records_by_region_removes_all_regional_data(clean_test_db):
    """Test deleting all records for a specific region."""
    from task1.database_loader import delete_records
    
    create_database(TEST_DB_PATH)
    
    data = [
        {"country": "China", "region": "Asia", "year": 2015, "life_expect": 76.0},
        {"country": "India", "region": "Asia", "year": 2015, "life_expect": 68.0},
        {"country": "USA", "region": "Americas", "year": 2015, "life_expect": 78.0},
    ]
    load_data_to_db(TEST_DB_PATH, data)
    
    # Delete all Asia records
    deleted_count = delete_records(TEST_DB_PATH, filters={"region": "Asia"})
    
    assert deleted_count == 2
    
    # Verify only Americas remains
    all_records = get_all_records(TEST_DB_PATH)
    assert len(all_records) == 1
    assert all_records[0]["country"] == "USA"


def test_delete_records_by_year_removes_specific_year(clean_test_db):
    """Test deleting all records for a specific year."""
    from task1.database_loader import delete_records
    
    create_database(TEST_DB_PATH)
    
    data = [
        {"country": "China", "year": 2015, "life_expect": 76.0},
        {"country": "China", "year": 2016, "life_expect": 76.5},
        {"country": "India", "year": 2015, "life_expect": 68.0},
    ]
    load_data_to_db(TEST_DB_PATH, data)
    
    # Delete all 2015 records
    deleted_count = delete_records(TEST_DB_PATH, filters={"year": 2015})
    
    assert deleted_count == 2
    
    # Verify only 2016 remains
    remaining = get_all_records(TEST_DB_PATH)
    assert len(remaining) == 1
    assert remaining[0]["year"] == 2016


def test_delete_records_with_multiple_filters(clean_test_db):
    """Test delete with combined filters (country + year)."""
    from task1.database_loader import delete_records
    
    create_database(TEST_DB_PATH)
    
    data = [
        {"country": "China", "year": 2015, "life_expect": 76.0},
        {"country": "China", "year": 2016, "life_expect": 76.5},
        {"country": "India", "year": 2015, "life_expect": 68.0},
    ]
    load_data_to_db(TEST_DB_PATH, data)
    
    # Delete only China 2015
    deleted_count = delete_records(TEST_DB_PATH, filters={"country": "China", "year": 2015})
    
    assert deleted_count == 1
    
    # Verify others remain
    remaining = get_all_records(TEST_DB_PATH)
    assert len(remaining) == 2


def test_delete_records_raises_error_for_empty_filters(clean_test_db):
    """Test that empty filters prevent accidental deletion of all data."""
    from task1.database_loader import delete_records
    
    create_database(TEST_DB_PATH)
    
    with pytest.raises(ValueError, match="Filters cannot be empty"):
        delete_records(TEST_DB_PATH, filters={})
