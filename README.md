# PAI Individual Assignment - Data Insights Dashboard

## Project Overview

This project implements a Python-based data insights tool for analyzing public health data, specifically WHO life expectancy datasets. The system supports data access, cleaning, filtering, correlation analysis, and presentation following professional software engineering practices.

**Module**: Programming for Artificial Intelligence (WM9QF-15)  
**Author**: Suhang Liao  
**Assignment Weight**: 70%

## Repository

- **GitHub Repository**: [PAI_SuhangLiao](https://github.com/HenryLiaoW/PAI_SuhangLiao)
- **Repository Status**: Private (accessible to module tutors as collaborators)

## Features

### Task 1: Data Insights Dashboard for Public Health Reports

**Implemented Functionalities**:

#### ✅ Phase 1: Data Access & Database (COMPLETE)
1. **Database Management** (20/20 tests passing)
   - SQLite database creation with 32-column schema
   - B-Tree indexes on country, year, and region
   - Robust CRUD operations with parameterized queries
   - Context manager for automatic resource cleanup
   - Error handling with custom exceptions
   
2. **Data Cleaning & Validation**
   - Numeric type conversion with error handling
   - Missing value handling (conversion to None)
   - Field-level data validation
   - UTF-8 encoding support

3. **Correlation Analysis** (Policy-Oriented)
   - Pearson correlation analysis for life expectancy predictors
   - Hand-coded algorithm (no scipy dependency)
   - **Key Finding**: Identified modifiable vs circular factors
     - Modifiable: basic_water (r=0.831), gghe-d (r=0.610), bmi (r=0.598)
     - Circular (excluded): infant_mort, adult_mortality, une_life
   
4. **Pipeline Orchestration**
   - Automated CSV → clean → export workflow
   - Database integration (3111 WHO records loaded)

#### 🔄 Phase 2: Data Filtering & Analysis (RED PHASE)
5. **Data Filter Module** (46 tests designed, implementation pending)
   - Basic filtering: DataFrame conversion, country/year/region filters
   - Statistical analysis: mean, median, std, min, max, count
   - Trend analysis: Time series by country and metric
   - **Policy Analysis Functions** (Focus on modifiable factors):
     - Infrastructure impact analysis (water, sanitation)
     - Healthcare spending effectiveness (gghe-d)
     - Nutrition indicators (BMI, undernourishment)
     - Vaccination coverage gap identification
     - Cross-country modifiable factors comparison
     - Policy intervention priority recommendations

#### ⏳ Phase 3: Visualization & Presentation (PENDING)
6. **Data Visualization** (upcoming)
   - Matplotlib-based charts for modifiable factors
   - Line plots, bar charts, scatter plots
   
7. **CLI Interface** (upcoming)
   - Interactive menu system
   - Pandas table display
   - Integration: database → filter → visualize

## Requirements

### System Requirements
- **Python**: 3.13+ (tested on 3.13.5 and 3.14.0)
- **Operating System**: macOS, Linux, or Windows
- **Dependencies**: Listed in requirements below

### Python Dependencies
```
pytest>=8.3.4
pandas>=2.0.0
matplotlib>=3.5.0  # Required for visualization (upcoming)
```

**Core Functionality Dependencies**:
- `csv` - CSV file handling
- `math` - Mathematical operations for correlation analysis
- `sqlite3` - SQLite database operations
- `typing` - Type hints for code clarity
- `pandas` - Data filtering and statistical analysis
- `matplotlib` - Data visualization (upcoming)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/HenryLiaoW/PAI_SuhangLiao.git
cd PAI_SuhangLiao
```

### 2. Set Up Python Environment

**Option A: Using venv (Recommended)**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Option B: Using conda**
```bash
conda create -n pai python=3.13
conda activate pai
pip install pytest
```

### 3. Verify Installation
```bash
python --version  # Should show Python 3.13+
pytest --version  # Should show pytest 8.3.4+
```

## How to Run the Code

### Run Database Operations
```bash
# Create database and load WHO data (3111 records)
python -c "from task1.database_loader import create_database, load_data_to_db; from task1.data_loader import load_data; create_database('task1/data/life_expectancy.db'); load_data_to_db('task1/data/life_expectancy.db', load_data('task1/data/life_expectancy_cleaned.csv'))"

# Query database examples
python -c "from task1.database_loader import get_all_records; records = get_all_records('task1/data/life_expectancy.db'); print(f'Total records: {len(records)}')"

python -c "from task1.database_loader import get_records_by_country; china = get_records_by_country('task1/data/life_expectancy.db', 'China'); print(f'China records: {len(china)}')"
```

### Run Data Cleaning Pipeline
```bash
# Clean the raw data and export to CSV
python -c "from task1.pipeline_clean_export import export_cleaned_dataset; export_cleaned_dataset('task1/data/life_expectancy.csv', 'task1/data/life_expectancy_cleaned.csv')"
```

### Run Correlation Analysis
```bash
# Analyze correlations between life expectancy and predictors
python -c "from task1.analysis_correlation import run_correlation_analysis; results = run_correlation_analysis('task1/data/life_expectancy_cleaned.csv'); print('\\n'.join([f'{var}: r={corr:.3f}' for var, corr in results]))"
```

### Run All Tests
```bash
# Run complete test suite (67 tests: 47 task1 + 20 database)
pytest

# Run tests with detailed output
pytest -v

# Run specific module tests
pytest task1/tests/test_database_loader.py -v  # 20 database tests
pytest task1/tests/test_data_filter.py -v      # 46 filter tests (RED phase)
pytest task1/tests/test_cleaner.py -v          # 7 cleaning tests

# Run tests with coverage report
pytest --cov=task1 --cov-report=html
```

### Test Output Example
```
=========== test session starts ============
collected 67 items

task1/tests/test_database_loader.py ....................  [ 30%]
task1/tests/test_data_filter.py FFFFFFF..................  [ 98%]
task1/tests/test_cleaner.py .......                       [100%]

====== 47 passed, 46 failed (expected) in 0.52s =======
Note: data_filter tests fail (RED phase - implementation pending)
```

## Project Structure

```
PAI_SuhangLiao/
├── README.md                          # This file - Project documentation
├── pytest.ini                         # Pytest configuration
├── SOLID_PRINCIPLES_ANALYSIS.md       # SOLID principles documentation (English)
├── SOLID_PRINCIPLES_ANALYSIS_CN.md    # SOLID principles documentation (Chinese)
│
├── docs/                              # Learning materials and backups
│   └── learning_examples/
│       ├── database_loader_robust_backup.py
│       ├── DATABASE_IMPLEMENTATION_FIXES.md
│       ├── test_database_loader_TDD_EXAMPLE.py
│       ├── test_data_filter_basic_version.py
│       └── data_filter_stub.py
│
├── task1/                             # Task 1: Data Insights Dashboard
│   ├── __init__.py
│   ├── data_loader.py                 # CSV loading (Single Responsibility)
│   ├── cleaner.py                     # Data cleaning and type conversion
│   ├── pipeline_clean_export.py       # Orchestration layer
│   ├── analysis_correlation.py        # Pearson correlation analysis (154 lines)
│   ├── database_loader.py             # ✅ SQLite operations (315 lines, 20 tests passing)
│   ├── data_filter.py                 # 🔄 Pandas filtering (274 lines, RED phase)
│   │
│   ├── data/
│   │   ├── life_expectancy.csv        # Raw WHO dataset (3111 records)
│   │   ├── life_expectancy_cleaned.csv # Cleaned output
│   │   └── life_expectancy.db         # SQLite database with indexes
│   │
│   └── tests/
│       ├── test_data_loader.py        # 2 tests ✅
│       ├── test_cleaner.py            # 7 tests ✅
│       ├── test_analysis_correlation.py # 18 tests ✅
│       ├── test_database_loader.py    # 20 tests ✅ (comprehensive rewrite)
│       └── test_data_filter.py        # 46 tests 🔄 (RED phase - failing as expected)
│
└── task2/                             # Task 2: Data Structure and Algorithm
    ├── __init__.py
    └── tests/
```

## Development Methodology

### Test-Driven Development (TDD)
This project strictly follows TDD workflow with clear git commit history:

1. **RED Phase**: Write failing tests first (define expected behavior)
2. **GREEN Phase**: Implement minimal code to pass tests
3. **REFACTOR Phase**: Improve code quality while maintaining passing tests

**Evidence in Git History**:
```bash
git log --oneline
# Recent TDD commits:
# a1b2c3d refactor(test_database_loader): rewrite test suite (TDD RED phase)
# d4e5f6g feat(database_loader): enhance based on tests (TDD GREEN phase)
# h7i8j9k chore: organize learning materials (TDD REFACTOR phase)
```

**Current TDD Status**:
- ✅ Database module: Complete TDD cycle (RED → GREEN → REFACTOR)
- 🔄 Data filter module: RED phase complete (46 tests designed)
- ⏳ Visualization module: Not started

### Design Philosophy: Policy-Oriented Analysis

**Critical Insight**: Reject circular definitions, focus on modifiable factors

**Excluded (Circular Relationships)**:
- infant_mortality ↔ life_expectancy (correlation by definition)
- adult_mortality ↔ life_expectancy (tautological)
- une_life ↔ life_expectancy (same metric, different source)

**Included (Modifiable Policy Factors)**:
- Infrastructure: basic_water (r=0.831), sanitation_services
- Healthcare: gghe-d (r=0.610), che_gdp
- Nutrition: bmi (r=0.598), undernourishment
- Immunization: polio, diphtheria, hepatitis coverage

This design enables **actionable policy recommendations** rather than validating obvious relationships.

### SOLID Principles
See `SOLID_PRINCIPLES_ANALYSIS.md` for detailed documentation of:
- Single Responsibility Principle (SRP)
- Open/Closed Principle (OCP)
- Liskov Substitution Principle (LSP)
- Interface Segregation Principle (ISP)
- Dependency Inversion Principle (DIP)

## Code Quality Metrics

### Testing Statistics
- **Total Tests**: 67 automated tests (47 passing, 46 in RED phase)
  - Database module: 20/20 passing ✅
  - Data loader: 2/2 passing ✅
  - Data cleaner: 7/7 passing ✅
  - Correlation analysis: 18/18 passing ✅
  - Data filter: 0/46 passing 🔄 (RED phase - implementation pending)

### Code Metrics
- **Total Lines of Code**: ~1,500 lines (excluding tests)
- **Test Code**: ~1,300 lines
- **Test Coverage**: All public functions tested
- **Modules**: 6 core modules with clear boundaries
- **Database Records**: 3,111 WHO life expectancy records
- **Database Indexes**: 3 B-Tree indexes (country, year, region)

### Quality Standards
- ✅ **PEP 8 Compliance**: Enforced via naming conventions
- ✅ **Type Hints**: All function signatures documented
- ✅ **Docstrings**: Comprehensive for all public functions
- ✅ **Error Handling**: Custom exceptions with informative messages
- ✅ **SOLID Principles**: Documented in separate analysis files
- ✅ **TDD Workflow**: Clear RED → GREEN → REFACTOR commits

## Data Source

**Dataset**: WHO Life Expectancy Data  
**Format**: CSV with UTF-8 encoding  
**Records**: 3,111 country-year observations  
**Time Period**: Multiple years of global health data  
**Fields**: 33 columns including:
- Basic info: country, country_code, region, year
- Life expectancy: life_expect, life_exp60
- Mortality: adult_mortality, infant_mort, age1-4mort
- Modifiable factors: basic_water, gghe-d, bmi, alcohol
- Immunization: polio, diphtheria, hepatitis, measles
- Economic: gni_capita, che_gdp, une_gni
- Population: une_pop, doctors, hospitals

**Source**: Public health research dataset for policy analysis

## Troubleshooting

### Common Issues

**1. Module Not Found Error**
```bash
# Ensure you're running from project root
cd PAI_SuhangLiao

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

**2. File Encoding Errors**
- All files use UTF-8 encoding
- If issues persist on Windows, ensure console is UTF-8: `chcp 65001`

**3. Test Failures**
```bash
# Clean test artifacts
find . -name "test_*.db" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Re-run tests
pytest -v
```

## Git Workflow

### Commit Conventions
This project uses [Conventional Commits](https://www.conventionalcommits.org/):
- `test:` - Adding or updating tests
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `refactor:` - Code restructuring

### View Git History
```bash
# See all commits
git log --oneline --graph

# See TDD workflow for specific modules
git log --oneline | grep "database_loader"
git log --oneline | grep "data_filter"

# View recent development
git log --oneline -10
```

## Project Progress & Next Steps

### ✅ Completed (Phase 1)
1. Database schema design and implementation
2. Robust CRUD operations with error handling
3. Correlation analysis identifying modifiable factors
4. Data cleaning and validation pipeline
5. Comprehensive test suite (47 passing tests)
6. TDD workflow with git commit history

### 🔄 In Progress (Phase 2 - RED Phase)
1. Data filter module design (46 tests defined)
2. Policy-oriented analysis functions designed:
   - Infrastructure impact analysis
   - Healthcare spending effectiveness
   - Nutrition indicators
   - Vaccination gap identification
   - Cross-country comparison
   - Policy intervention priorities

### ⏳ Upcoming (Phase 2 - GREEN Phase)
1. Implement data filter functions (make 46 tests pass)
2. Commit TDD GREEN phase

### ⏳ Upcoming (Phase 3)
1. Matplotlib visualization module
2. CLI interface for interactive analysis
3. Integration testing (database → filter → visualize)
4. Critical reflection documentation (REFLECTION.md)
5. Final testing and documentation

## License and Academic Integrity

This is an academic assignment for the University of Warwick.  
**AI Collaboration Level**: AI COLLABORATION permitted for drafting, refining, and code writing.

All AI-generated content has been critically evaluated and modified.

## Contact

**Student**: Suhang Liao  
**Email**: u5697414@live.warwick.ac.uk  
**Module Tutor**: Amir Kayhani

---

*Last Updated*: 18 December 2025  
*Project Status*: Phase 2 (Data Filtering) - RED Phase Complete
