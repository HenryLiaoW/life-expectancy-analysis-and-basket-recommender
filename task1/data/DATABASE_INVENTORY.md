# Database Inventory - Task1 Data Directory

**Last Updated:** January 2026  
**Current Database Count:** 3 databases (2 production + 1 test)

---

## Production Databases

### 1. CLI_demo.db
**Size:** 28 KB | **Records:** 13  
**Purpose:** Lightweight demonstration database for interactive CLI menu system  
**Usage:** Default database for `main.py` interactive sessions  
**Content:** Sample data from 3 countries (Brazil, China, India) × 3 years (2015-2017) + additional test records  
**Created by:** `create_db.py --demo` or `main.py` menu option  
**Used in:**
- `task1/main.py` (default database for interactive menu)
- `task1/demo_filtering_summary.py` (workflow demonstrations)
- `task1/tests/test_visualization.py` (visualization tests)

**Key Features:**
- Fast loading (<0.1s)
- Representative sample for UI testing
- Contains all 27 health/economic indicators
- Sufficient for demonstrating filtering and analysis functions

---

### 2. life_expectancy.db
**Size:** 664 KB | **Records:** 3,111  
**Purpose:** Full production database with complete WHO life expectancy dataset  
**Usage:** Real-world policy analysis, comprehensive data exploration  
**Content:** 183 countries × 17 years (2000-2016), 27 health/economic indicators  
**Created by:** `create_db.py` from `life_expectancy.csv`  
**Used in:**
- `task1/policy_analysis_demo.py` (Africa/Asia/Eastern Mediterranean policy scenarios)
- `task1/analysis_correlation.py` (Pearson correlation analysis across 27 indicators)
- Real policy research and statistical analysis

**Key Features:**
- Complete WHO dataset (2000-2016)
- 799 African records for regional policy analysis
- 27 health indicators including: life_expectancy, adult_mortality, infant_deaths, basic_water, gghe-d, bmi, etc.
- Supports correlation analysis (r=0.831 for basic_water, r=0.610 for gghe-d)

---

## Test Databases (Automated Testing)

### 3. test_database_mode.db
**Size:** 908 KB | **Records:** 3,111  
**Purpose:** Integration test database for validating **Database Mode** cleaning pipeline  
**Usage:** Automated testing of SQL-based cleaning operations  
**Content:** Full dataset loaded from CSV for cleaning validation  
**Created by:** `test_cleaning_modes.py::test_database_mode()` during pytest execution  
**Test Flow:**
1. Load raw CSV → database
2. Apply SQL-based cleaning operations via `database_cleaner.py`
3. Validate cleaning effectiveness (null handling, type conversion)
4. Verify data integrity post-cleaning

**Lifecycle:** Created during test setup, auto-deleted after test completion  
**Note:** Larger than production DB due to pre-cleaning raw data with intentional dirty records

---

## Database Comparison Matrix

| Database                  | Size   | Records | Type       | Purpose          | Lifecycle   | Test Coverage |
|---------------------------|--------|---------|------------|------------------|-------------|---------------|
| **CLI_demo.db**           | 28 KB  | 13      | Production | Demo/UI Testing  | Persistent  | 23 tests      |
| **life_expectancy.db**    | 664 KB | 3,111   | Production | Full Analysis    | Persistent  | 46 tests      |
| **test_database_mode.db** | 908 KB | 3,111   | Test       | Cleaning Pipeline| Test-scoped | 2 tests       |

**Total Test Coverage:** 135 automated tests validating database operations, cleaning, and analysis functions

---

## Usage Guidelines

### For Interactive Exploration
```bash
# Quick demonstration (13 records, <0.1s loading)
python task1/main.py  # Uses CLI_demo.db by default

# Full dataset analysis (3,111 records)
python task1/main.py --db task1/data/life_expectancy.db

# Policy analysis demonstration
python task1/policy_analysis_demo.py  # Uses life_expectancy.db
```

### For Development and Testing
```bash
# Run all tests (135 tests, auto-creates test databases)
pytest task1/tests/ -v

# Run specific database tests
pytest task1/tests/test_database_loader.py -v  # 34 CRUD tests
pytest task1/tests/test_cleaning_modes.py -v   # 2 cleaning pipeline tests
```

### For Production Deployment
- **Essential databases:** `CLI_demo.db`, `life_expectancy.db` (included in repository)
- **Test databases:** Auto-generated during pytest execution (not committed)
- **Regeneration:** Databases can be rebuilt from CSV files if needed

---

## Database Regeneration Commands

```bash
# Create demo database (13 records for quick testing)
python task1/create_db.py --demo

# Create full production database from CSV (3,111 records)
python task1/create_db.py

# Alternative: Clean CSV first, then create database
python task1/pipeline_clean_export.py  # Creates life_expectancy_cleaned.csv
python task1/create_db.py              # Loads cleaned CSV → life_expectancy.db
```

---

## Database Schema

All databases share the same schema with 27 indicator columns:

**Identifiers:** country, year, region  
**Health Indicators:** life_expectancy, adult_mortality, infant_deaths, basic_water, gghe-d, bmi, measles, polio, diphtheria, etc.  
**Economic Indicators:** income_composition, gdp_per_capita

---

## Repository Policy

- ✅ **Committed:** `CLI_demo.db`, `life_expectancy.db`, `life_expectancy.csv`, `life_expectancy_cleaned.csv`
- ❌ **Gitignored:** `test_database_mode.db` (regenerated by pytest)
- 🔄 **Regeneration:** All databases can be rebuilt from CSV source files

**Last Updated:** January 2026

- **Test DBs 3x larger:** Pre-cleaning raw data contains more null values
- **Post-cleaning:** Size reduces by ~25% after SQL cleaning operations
- **Recommend:** Delete test DBs after development sessions (auto-regenerated by pytest)
- **Total size:** ~3.4 MB (acceptable for git repo with proper .gitignore)

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-06  
**Maintained By:** Task1 Development Team
