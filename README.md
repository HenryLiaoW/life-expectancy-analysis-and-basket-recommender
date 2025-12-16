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
1. **Data Access & Loading**
   - CSV file loading with UTF-8 encoding support
   - Data loading into SQLite database (in progress)
   
2. **Data Cleaning & Structuring**
   - Numeric type conversion with error handling
   - Missing value handling (conversion to None)
   - Field-level data validation
   
3. **Statistical Analysis**
   - Pearson correlation analysis for life expectancy predictors
   - Hand-coded correlation algorithm (no scipy dependency)
   
4. **Pipeline Orchestration**
   - Automated data cleaning workflow
   - Export cleaned data to CSV

## Requirements

### System Requirements
- **Python**: 3.13+ (tested on 3.13.5 and 3.14.0)
- **Operating System**: macOS, Linux, or Windows
- **Dependencies**: Listed in requirements below

### Python Dependencies
```
pytest>=8.3.4
```

All core functionality uses Python standard library only:
- `csv` - CSV file handling
- `math` - Mathematical operations
- `sqlite3` - Database operations
- `typing` - Type hints

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
# Run complete test suite (27 tests)
pytest

# Run tests with detailed output
pytest -v

# Run specific test file
pytest task1/tests/test_cleaner.py -v

# Run tests with coverage report
pytest --cov=task1 --cov-report=html
```

### Test Output Example
```
=========== test session starts ============
collected 27 items

task1/tests/test_analysis_correlation.py ..................  [ 66%]
task1/tests/test_cleaner.py .......                          [ 92%]
task1/tests/test_data_loader.py ..                           [100%]

============ 27 passed in 0.02s ============
```

## Project Structure

```
PAI_SuhangLiao/
├── README.md                          # This file
├── pytest.ini                         # Pytest configuration
├── SOLID_PRINCIPLES_ANALYSIS.md       # SOLID principles documentation (English)
├── SOLID_PRINCIPLES_ANALYSIS_CN.md    # SOLID principles documentation (Chinese)
│
├── task1/                             # Task 1: Data Insights Dashboard
│   ├── __init__.py
│   ├── data_loader.py                 # CSV loading (Single Responsibility)
│   ├── cleaner.py                     # Data cleaning and type conversion
│   ├── pipeline_clean_export.py       # Orchestration layer
│   ├── analysis_correlation.py        # Pearson correlation analysis
│   ├── database_loader.py             # SQLite database operations (in progress)
│   │
│   ├── data/
│   │   ├── life_expectancy.csv        # Raw WHO dataset
│   │   └── life_expectancy_cleaned.csv # Cleaned output
│   │
│   └── tests/
│       ├── test_data_loader.py        # 2 tests
│       ├── test_cleaner.py            # 7 tests
│       ├── test_analysis_correlation.py # 18 tests
│       └── test_database_loader.py    # 7 tests (in progress)
│
└── task2/                             # Task 2: Data Structure and Algorithm
    ├── __init__.py
    └── tests/
```

## Development Methodology

### Test-Driven Development (TDD)
This project strictly follows TDD workflow:

1. **RED Phase**: Write failing tests first
2. **GREEN Phase**: Implement minimal code to pass tests
3. **REFACTOR Phase**: Improve code quality while maintaining passing tests

**Evidence in Git History**:
```bash
git log --oneline
# Shows clear TDD progression:
# 1. test: add comprehensive tests (RED)
# 2. test: add stub implementation (RED complete)
# 3. feat: implement functionality (GREEN)
# 4. docs: enhance documentation (REFACTOR)
```

### SOLID Principles
See `SOLID_PRINCIPLES_ANALYSIS.md` for detailed documentation of:
- Single Responsibility Principle (SRP)
- Open/Closed Principle (OCP)
- Liskov Substitution Principle (LSP)
- Interface Segregation Principle (ISP)
- Dependency Inversion Principle (DIP)

## Code Quality Metrics

- **Total Tests**: 27 automated tests
- **Test Coverage**: All public functions tested
- **Modules**: 4 core modules with clear boundaries
- **Dependencies**: Minimal (Python stdlib only for core features)
- **PEP 8 Compliance**: Enforced via naming conventions and structure
- **Documentation**: Comprehensive docstrings for all public functions

## Data Source

**Dataset**: WHO Life Expectancy Data  
**Format**: CSV with UTF-8 encoding  
**Fields**: Country, year, life expectancy, adult mortality, infant mortality, BMI, GDP, etc.  
**Source**: Public health research dataset

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

# See TDD workflow
git log --oneline | grep -E "(test|feat|docs)"
```

## License and Academic Integrity

This is an academic assignment for the University of Warwick.  
**AI Collaboration Level**: AI COLLABORATION permitted for drafting, refining, and code writing.

All AI-generated content has been critically evaluated and modified.

## Contact

**Student**: Suhang Liao  
**Email**: u5697414@live.warwick.ac.uk  
**Module Tutor**: Amir Kayhani

---

*Last Updated*: 15 December 2025
