import os #用于文件操作（检查、删除测试数据库）
import sqlite3 #用于SQLite数据库操作
import pytest #测试框架
from task1.database_loader import (
    create_database,
    load_data_to_db,
    get_all_records,
    get_connection
)

# Test database path
# 定义测试数据库路径，和真实数据库分开，防止污染
TEST_DB_PATH = "task1/data/test_life_expectancy.db"


@pytest.fixture
def clean_test_db():
    """Remove test database before and after each test."""
    # Clean before test
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    yield TEST_DB_PATH
    
    # Clean after test
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def test_create_database_creates_file(clean_test_db):
    """Test that create_database creates a SQLite database file."""
    create_database(TEST_DB_PATH)
    assert os.path.exists(TEST_DB_PATH)


def test_get_connection_returns_valid_connection(clean_test_db):
    """Test that get_connection returns a valid SQLite connection."""
    create_database(TEST_DB_PATH)
    
    conn = get_connection(TEST_DB_PATH)
    assert conn is not None
    assert isinstance(conn, sqlite3.Connection)
    
    conn.close()


def test_create_database_creates_table(clean_test_db):
    """Test that create_database creates the life_expectancy table with correct schema."""
    create_database(TEST_DB_PATH)
    
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='life_expectancy'")
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == "life_expectancy"
    
    conn.close()


def test_load_data_to_db_inserts_records(clean_test_db):
    """Test that load_data_to_db correctly inserts cleaned data into database."""
    create_database(TEST_DB_PATH)
    
    # Sample cleaned data
    sample_data = [
        {
            "country": "China",
            "country_code": "CHN",
            "region": "Asia",
            "year": 2015,
            "life_expectancy": 76.5,
            "adult_mortality": 85.0,
            "infant_mort": 9.3
        },
        {
            "country": "India",
            "country_code": "IND",
            "region": "Asia",
            "year": 2015,
            "life_expectancy": 68.3,
            "adult_mortality": 164.0,
            "infant_mort": 37.9
        }
    ]
    
    load_data_to_db(TEST_DB_PATH, sample_data)
    
    # Verify data was inserted
    conn = sqlite3.connect(TEST_DB_PATH) 
    cursor = conn.cursor() 
    cursor.execute("SELECT COUNT(*) FROM life_expectancy") 
    count = cursor.fetchone()[0] 
    
    assert count == 2 # Two records should be inserted
    
    conn.close() 


def test_get_all_records_returns_data(clean_test_db):
    """Test that get_all_records retrieves all records from database."""
    create_database(TEST_DB_PATH)
    
    sample_data = [
        {
            "country": "China",
            "country_code": "CHN",
            "region": "Asia",
            "year": 2015,
            "life_expectancy": 76.5
        }
    ]
    
    load_data_to_db(TEST_DB_PATH, sample_data)
    records = get_all_records(TEST_DB_PATH)
    
    assert len(records) == 1
    assert records[0]["country"] == "China"
    assert records[0]["year"] == 2015


def test_load_data_handles_none_values(clean_test_db):
    """Test that database correctly handles None values in numeric fields."""
    create_database(TEST_DB_PATH)
    
    sample_data = [
        {
            "country": "TestCountry",
            "year": 2015,
            "life_expectancy": None,  # Missing value
            "adult_mortality": 100.0,
            "infant_mort": None
        }
    ]
    
    load_data_to_db(TEST_DB_PATH, sample_data)
    records = get_all_records(TEST_DB_PATH)
    
    assert len(records) == 1
    assert records[0]["life_expectancy"] is None
    assert records[0]["infant_mort"] is None
