"""
Pytest configuration and shared fixtures for task1 tests.
Pytest 配置文件：为 task1 测试提供共享的 fixtures（测试夹具）

Core Functions | 核心功能：
--------------
1. Shared fixtures for all test files | 为所有测试文件提供共享的 fixtures
   - test_db_with_data: Auto-create/cleanup test DB (session-level)
     自动创建/清理测试数据库（会话级，所有测试共享）
   - sample_countries: Return test country list ["China", "India", "USA", "Brazil"]
     返回测试国家列表
   - sample_years: Return test year range (2015, 2017)
     返回测试年份范围
   - test_data_summary: Return test data structure summary (12 records, 4 countries × 3 years)
     返回测试数据结构摘要（12条记录，4国家×3年）
   
2. Test data generator | 测试数据生成器
   - get_test_sample_data(): Generate 12 fixed records with modifiable factors
     生成12条固定测试记录（包含可修改政策因素）
   
3. Global test configuration | 全局测试配置
   - TEST_DB_PATH: Centralized DB path (task1/data/test_filter.db)
     集中管理数据库路径

Design Philosophy | 设计哲学：
-------------------
- Session-level fixture: initialize test DB once for all tests (fast)
  会话级fixture：所有测试共享一个数据库（快速执行）
  
- Minimal data: only essential records for testing filter logic
  最小化数据：仅包含测试过滤逻辑必需的记录
  
- No complex relationships: single table, no foreign keys
  无复杂关系：单表结构，无外键约束
"""

import os
import pytest
from task1.src.database_loader import create_database, load_data_to_db

# Test database path
TEST_DB_PATH = "task1/data/test_filter.db"


def get_test_sample_data():
    """
    Generate test sample data.
    
    Design rationale:
    - Hand-crafted: ensures predictable test behavior
    - Minimal: 12 records (4 countries × 3 years)
    - Representative: covers different regions and value ranges
    
    Why not real data extraction?
    1. Tests verify CODE LOGIC, not real-world data analysis
    2. Hand-crafted data can cover edge cases precisely
    3. 100% predictable - won't break when CSV updates
    4. Faster execution
    
    Returns:
        List[dict]: Test data records
    """
    return [
        # China (Asia) - High life expectancy, improving trend
        {"country": "China", "country_code": "CHN", "region": "Asia", 
         "year": 2015, "life_expect": 76.1, "adult_mortality": 120, "infant_mort": 8.1,
         "basic_water": 95.5, "gghe-d": 3.2, "bmi": 23.8, "alcohol": 7.2,
         "polio": 99.0, "diphtheria": 99.0, "hepatitis": 99.0},
        {"country": "China", "country_code": "CHN", "region": "Asia", 
         "year": 2016, "life_expect": 76.4, "adult_mortality": 118, "infant_mort": 7.8,
         "basic_water": 96.0, "gghe-d": 3.3, "bmi": 24.0, "alcohol": 7.3,
         "polio": 99.0, "diphtheria": 99.0, "hepatitis": 99.0},
        {"country": "China", "country_code": "CHN", "region": "Asia", 
         "year": 2017, "life_expect": 76.7, "adult_mortality": 116, "infant_mort": 7.5,
         "basic_water": 96.5, "gghe-d": 3.4, "bmi": 24.2, "alcohol": 7.4,
         "polio": 99.0, "diphtheria": 99.0, "hepatitis": 99.0},
        
        # India (Asia) - Lower baseline, visible improvement potential
        {"country": "India", "country_code": "IND", "region": "Asia", 
         "year": 2015, "life_expect": 68.3, "adult_mortality": 190, "infant_mort": 37.9,
         "basic_water": 88.0, "gghe-d": 1.2, "bmi": 21.5, "alcohol": 5.7,
         "polio": 85.0, "diphtheria": 87.0, "hepatitis": 89.0},
        {"country": "India", "country_code": "IND", "region": "Asia", 
         "year": 2016, "life_expect": 68.6, "adult_mortality": 188, "infant_mort": 36.5,
         "basic_water": 89.5, "gghe-d": 1.3, "bmi": 21.7, "alcohol": 5.8,
         "polio": 86.0, "diphtheria": 88.0, "hepatitis": 90.0},
        {"country": "India", "country_code": "IND", "region": "Asia", 
         "year": 2017, "life_expect": 69.0, "adult_mortality": 186, "infant_mort": 35.2,
         "basic_water": 91.0, "gghe-d": 1.4, "bmi": 21.9, "alcohol": 5.9,
         "polio": 87.0, "diphtheria": 89.0, "hepatitis": 91.0},
        
        # USA (Americas) - High life expectancy, obesity concern
        {"country": "USA", "country_code": "USA", "region": "Americas", 
         "year": 2015, "life_expect": 78.9, "adult_mortality": 110, "infant_mort": 5.9,
         "basic_water": 99.2, "gghe-d": 8.3, "bmi": 28.5, "alcohol": 9.2,
         "polio": 93.0, "diphtheria": 94.0, "hepatitis": 91.0},
        {"country": "USA", "country_code": "USA", "region": "Americas", 
         "year": 2016, "life_expect": 78.7, "adult_mortality": 112, "infant_mort": 5.8,
         "basic_water": 99.3, "gghe-d": 8.4, "bmi": 28.7, "alcohol": 9.3,
         "polio": 93.0, "diphtheria": 94.0, "hepatitis": 91.0},
        {"country": "USA", "country_code": "USA", "region": "Americas", 
         "year": 2017, "life_expect": 78.5, "adult_mortality": 114, "infant_mort": 5.7,
         "basic_water": 99.4, "gghe-d": 8.5, "bmi": 28.9, "alcohol": 9.4,
         "polio": 93.0, "diphtheria": 94.0, "hepatitis": 92.0},
        
        # Brazil (Americas) - Middle range, good infrastructure
        {"country": "Brazil", "country_code": "BRA", "region": "Americas", 
         "year": 2015, "life_expect": 74.8, "adult_mortality": 145, "infant_mort": 14.2,
         "basic_water": 97.8, "gghe-d": 3.8, "bmi": 26.5, "alcohol": 8.9,
         "polio": 95.0, "diphtheria": 96.0, "hepatitis": 95.0},
        {"country": "Brazil", "country_code": "BRA", "region": "Americas", 
         "year": 2016, "life_expect": 75.0, "adult_mortality": 143, "infant_mort": 13.8,
         "basic_water": 98.0, "gghe-d": 3.9, "bmi": 26.7, "alcohol": 9.0,
         "polio": 95.0, "diphtheria": 96.0, "hepatitis": 95.0},
        {"country": "Brazil", "country_code": "BRA", "region": "Americas", 
         "year": 2017, "life_expect": 75.2, "adult_mortality": 141, "infant_mort": 13.4,
         "basic_water": 98.2, "gghe-d": 4.0, "bmi": 26.9, "alcohol": 9.1,
         "polio": 96.0, "diphtheria": 97.0, "hepatitis": 96.0},
    ]


@pytest.fixture(scope='session')
def test_db_with_data():
    """
    Session-level fixture: initialize test database once for all tests.
    
    Scope rationale:
    - session: create DB once, reuse for all tests (fast)
    - Not function: data_filter tests are READ-ONLY, no isolation needed
    - Auto cleanup: removes DB after test session
    
    Yields:
        str: Path to test database
    """
    # Clean up any existing test DB
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    # Create database with test data
    create_database(TEST_DB_PATH)
    sample_data = get_test_sample_data()
    load_data_to_db(TEST_DB_PATH, sample_data)
    
    yield TEST_DB_PATH
    
    # Cleanup after all tests
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture
def sample_countries():
    """Return list of countries in test data."""
    return ["China", "India", "USA", "Brazil"]


@pytest.fixture
def sample_years():
    """Return year range in test data."""
    return (2015, 2017)


@pytest.fixture
def test_data_summary():
    """
    Return summary of test data structure.
    Useful for parametrized tests and documentation.
    """
    return {
        'total_records': 12,
        'countries': 4,
        'years_per_country': 3,
        'regions': {
            'Asia': ['China', 'India'],
            'Americas': ['USA', 'Brazil']
        },
        'year_range': (2015, 2017)
    }
