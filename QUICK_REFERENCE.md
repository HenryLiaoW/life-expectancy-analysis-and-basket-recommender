# Quick Reference: Common Operations & Workflows

**Purpose**: Fast reference guide for common tasks and operations  
**Audience**: Future agent sessions, developers, users  
**Last Updated**: December 24, 2025

---

## 🚀 Quick Start Commands

### Environment Setup
```bash
# Clone and setup
git clone https://github.com/HenryLiaoW/PAI_SuhangLiao.git
cd PAI_SuhangLiao

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pytest pandas matplotlib
```

### Verify Installation
```bash
python --version  # Should be 3.13+
python -c "import pandas; import matplotlib; print('✅ All dependencies installed')"
```

---

## 📊 Data Pipeline Operations

### 1. Clean Raw Data
```bash
python -c "
from task1.pipeline_clean_export import export_cleaned_dataset
export_cleaned_dataset(
    'task1/data/life_expectancy.csv',
    'task1/data/life_expectancy_cleaned.csv'
)
print('✅ Data cleaned')
"
```

### 2. Create and Load Database
```bash
python -c "
from task1.database_loader import create_database, load_data_to_db
from task1.data_loader import load_data

# Create database with schema
create_database('task1/data/life_expectancy.db')

# Load cleaned data
records = load_data('task1/data/life_expectancy_cleaned.csv')
load_data_to_db('task1/data/life_expectancy.db', records)

print(f'✅ Loaded {len(records)} records')
"
```

### 3. Run Correlation Analysis
```bash
python -c "
from task1.analysis_correlation import run_correlation_analysis

results = run_correlation_analysis('task1/data/life_expectancy_cleaned.csv')
print('Top correlations with life expectancy:')
for var, corr in sorted(results, key=lambda x: abs(x[1]), reverse=True)[:5]:
    print(f'  {var:20s}: r = {corr:+.3f}')
"
```

---

## 🖥️ Interactive Interfaces

### Menu-Driven CLI (Recommended for Exploration)
```bash
# With full database
PYTHONPATH=$PWD python task1/menu_cli.py --db task1/data/life_expectancy.db

# With demo database (12 records)
PYTHONPATH=$PWD python task1/menu_cli.py --db task1/data/CLI_demo.db
```

**Menu Structure**:
- Section 1: Data Access (CRUD)
- Section 2: Data Filtering
- Section 3: Data Cleaning
- Section 4: Data Summarization
- Section 5: Data Presentation

### Command-Line CLI (For Scripting)
```bash
# Create new record
python task1/cli.py create

# Read all records for a country
python task1/cli.py read --country "China"

# Update a record
python task1/cli.py update --country "China" --year 2015

# Delete a record
python task1/cli.py delete --country "TestCountry" --year 2020
```

---

## 🧪 Testing Commands

### Run All Tests
```bash
pytest -v
```

### Run Specific Test Modules
```bash
# Database tests
pytest task1/tests/test_database_loader.py -v

# Data filter tests
pytest task1/tests/test_data_filter.py -v

# Cleaning tests
pytest task1/tests/test_cleaner.py -v

# Correlation tests
pytest task1/tests/test_analysis_correlation.py -v
```

### Run with Coverage Report
```bash
pytest --cov=task1 --cov-report=html
# Open htmlcov/index.html in browser
```

### Test a Single Function
```bash
pytest task1/tests/test_database_loader.py::test_create_database -v
```

---

## 🔍 Data Query Examples

### Query Database Directly
```bash
python -c "
from task1.database_loader import get_all_records, get_records_by_country

# Get all records
all_records = get_all_records('task1/data/life_expectancy.db')
print(f'Total records: {len(all_records)}')

# Get records for specific country
china = get_records_by_country('task1/data/life_expectancy.db', 'China')
print(f'China records: {len(china)}')

# Print first record
if china:
    print(f'Sample: {china[0][\"country\"]} ({china[0][\"year\"]}): {china[0][\"life_expect\"]} years')
"
```

### Filter and Analyze
```bash
python -c "
from task1.data_filter import get_data_as_dataframe, filter_by_country, calculate_statistics

# Load data
df = get_data_as_dataframe('task1/data/life_expectancy.db')
print(f'Loaded {len(df)} records')

# Filter for India
india = filter_by_country(df, 'India')
print(f'India: {len(india)} records')

# Calculate statistics
stats = calculate_statistics(india, 'life_expect')
print(f'Life expectancy: mean={stats[\"mean\"]:.2f}, min={stats[\"min\"]:.2f}, max={stats[\"max\"]:.2f}')
"
```

---

## 📈 Visualization Examples

### Generate Basic Visualizations
```bash
python -c "
from task1.visualization import (
    plot_life_expectancy_trend,
    plot_regional_comparison,
    plot_correlation_scatter
)

# Time series for a country
plot_life_expectancy_trend(
    'task1/data/life_expectancy.db',
    'China',
    'task1/output/figures/china_trend.png'
)

# Regional comparison
plot_regional_comparison(
    'task1/data/life_expectancy.db',
    'life_expect',
    'task1/output/figures/regional_comparison.png'
)

# Correlation scatter
plot_correlation_scatter(
    'task1/data/life_expectancy.db',
    'basic_water',
    'life_expect',
    'task1/output/figures/water_correlation.png'
)

print('✅ Visualizations created in task1/output/figures/')
"
```

### View Existing Visualizations
```bash
ls -lh task1/output/figures/
# bmi_distribution.png
# china_life_expect_trend.png
# healthcare_spending_comparison.png
# india_multi_metrics.png
# regional_life_expectancy.png
# water_life_correlation.png
```

---

## 🛠️ Common Maintenance Tasks

### Clean Test Artifacts
```bash
# Remove test databases
find . -name "test_*.db" -delete

# Remove Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Remove pytest cache
rm -rf .pytest_cache
```

### Reset Database
```bash
# Backup existing database
cp task1/data/life_expectancy.db task1/data/life_expectancy.db.backup

# Recreate from scratch
python -c "
from task1.database_loader import create_database, load_data_to_db
from task1.data_loader import load_data
import os

db_path = 'task1/data/life_expectancy.db'
if os.path.exists(db_path):
    os.remove(db_path)

create_database(db_path)
records = load_data('task1/data/life_expectancy_cleaned.csv')
load_data_to_db(db_path, records)
print('✅ Database recreated')
"
```

### Verify Data Integrity
```bash
python -c "
from task1.database_loader import get_all_records

records = get_all_records('task1/data/life_expectancy.db')
print(f'Total records: {len(records)}')

# Check for required fields
countries = set(r['country'] for r in records if r['country'])
years = set(r['year'] for r in records if r['year'])

print(f'Countries: {len(countries)}')
print(f'Years: {len(years)} (range: {min(years)}-{max(years)})')

# Check for missing life expectancy
missing = sum(1 for r in records if r['life_expect'] is None)
print(f'Records with missing life_expect: {missing}')
"
```

---

## 🔧 Development Workflows

### TDD Workflow for New Feature
```bash
# 1. Create test file
touch task1/tests/test_new_feature.py

# 2. Write tests (RED phase)
# Edit test_new_feature.py to add test cases

# 3. Run tests (should fail)
pytest task1/tests/test_new_feature.py -v

# 4. Implement feature (GREEN phase)
# Edit task1/new_feature.py

# 5. Run tests (should pass)
pytest task1/tests/test_new_feature.py -v

# 6. Refactor (REFACTOR phase)
# Improve code quality while keeping tests passing

# 7. Commit with conventional commit message
git add task1/tests/test_new_feature.py task1/new_feature.py
git commit -m "feat(new_feature): implement XYZ functionality"
```

### Documentation Workflow
```bash
# 1. Create guide file
touch task1/NEW_FEATURE_GUIDE.md

# 2. Write guide with sections:
#    - Overview
#    - Quick Start
#    - Detailed Usage
#    - Examples
#    - Troubleshooting

# 3. Create demo file
touch task1/demo_new_feature.py

# 4. Write working examples

# 5. Test demo
python task1/demo_new_feature.py

# 6. Commit together
git add task1/NEW_FEATURE_GUIDE.md task1/demo_new_feature.py
git commit -m "docs(new_feature): add user guide and demo"
```

---

## 📚 Documentation Navigation

### For Users
- **Getting Started**: `README.md` (English) or `README_CN.md` (Chinese)
- **CRUD Operations**: `task1/CRUD_CLI_GUIDE.md`
- **Interactive Menu**: `task1/MENU_CLI_GUIDE.md`
- **Database Info**: `task1/data/DATABASE_OVERVIEW.md`

### For Developers
- **Architecture**: `docs/DATA_FILTER_ARCHITECTURE.md`
- **API Reference**: `docs/DATA_FILTER_QUICK_REFERENCE.md`
- **SOLID Principles**: `SOLID_PRINCIPLES_ANALYSIS.md`
- **Requirements**: `REQUIREMENTS_ANALYSIS.md`

### For Learning
- **Database Lessons**: `docs/learning_examples/DATABASE_IMPLEMENTATION_FIXES.md`
- **Agent Insights**: `AGENT_LEARNING_SUMMARY.md`
- **Patterns**: `AGENT_CONVERSATION_PATTERNS.md`

---

## 🐛 Troubleshooting Quick Fixes

### "Module Not Found" Error
```bash
# Solution 1: Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Solution 2: Install in editable mode
pip install -e .

# Solution 3: Run from project root
cd /path/to/PAI_SuhangLiao
python task1/script.py
```

### "Database is Locked" Error
```bash
# Close all connections
python -c "import gc; gc.collect()"

# If persistent, find and kill process
lsof | grep life_expectancy.db  # On Unix/Mac
# Kill the process ID

# Or recreate database
rm task1/data/life_expectancy.db
# Recreate as shown in "Reset Database" section
```

### "UTF-8 Encoding" Error
```bash
# Unix/Mac
export LANG=en_US.UTF-8

# Windows
chcp 65001

# In Python script, ensure:
# open(file, 'r', encoding='utf-8')
```

### "pytest: command not found"
```bash
# Install pytest
pip install pytest

# Or use python -m pytest
python -m pytest -v
```

### Test Failures
```bash
# Clean artifacts
find . -name "test_*.db" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Run specific failing test with verbose output
pytest task1/tests/test_module.py::test_function -vv

# Run with print statements visible
pytest -s task1/tests/test_module.py
```

---

## 🔗 Code Reuse Patterns

### Pattern 1: Load Data into DataFrame
```python
from task1.data_filter import get_data_as_dataframe

df = get_data_as_dataframe('task1/data/life_expectancy.db')
# Now use pandas operations on df
```

### Pattern 2: Apply Multiple Filters
```python
from task1.data_filter import (
    get_data_as_dataframe,
    filter_by_country,
    filter_by_year_range
)

df = get_data_as_dataframe('task1/data/life_expectancy.db')
df = filter_by_country(df, 'China')
df = filter_by_year_range(df, 2010, 2015)
# df now contains China data for 2010-2015
```

### Pattern 3: Calculate and Display Statistics
```python
from task1.data_filter import calculate_statistics

stats = calculate_statistics(df, 'life_expect')
print(f"Mean: {stats['mean']:.2f}")
print(f"Std:  {stats['std']:.2f}")
print(f"Min:  {stats['min']:.2f}")
print(f"Max:  {stats['max']:.2f}")
```

### Pattern 4: CRUD with Error Handling
```python
from task1.database_loader import create_record, DatabaseError

try:
    create_record(db_path, {
        'country': 'TestCountry',
        'year': 2020,
        'life_expect': 75.5
    })
    print("✅ Record created")
except DatabaseError as e:
    print(f"❌ Error: {e}")
```

### Pattern 5: Safe Database Operations
```python
import sqlite3

db_path = 'task1/data/life_expectancy.db'
try:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM life_expectancy")
        count = cursor.fetchone()[0]
        print(f"Records: {count}")
except sqlite3.Error as e:
    print(f"Database error: {e}")
```

---

## 🎯 Performance Tips

### For Large Datasets
```python
# Use pandas for bulk operations instead of loops
import pandas as pd

# Good: Vectorized operation
df['bmi_category'] = df['bmi'].apply(
    lambda x: 'healthy' if 18.5 <= x <= 25 else 'other'
)

# Avoid: Loop over rows
# for idx, row in df.iterrows():  # Slow!
#     ...
```

### For Database Queries
```python
# Use indexes (already created on country, year, region)
# Queries filtering by these fields are fast

# For other fields, consider adding indexes
import sqlite3
with sqlite3.connect(db_path) as conn:
    conn.execute("CREATE INDEX IF NOT EXISTS idx_custom ON life_expectancy(field_name)")
```

### For Visualizations
```python
# Clear figure between plots to free memory
import matplotlib.pyplot as plt

plt.clf()  # Clear current figure
plt.cla()  # Clear current axes
plt.close('all')  # Close all figures
```

---

## 📝 Git Operations

### Common Commits
```bash
# After writing tests
git add task1/tests/test_*.py
git commit -m "test(module): add comprehensive test suite"

# After implementation
git add task1/module.py
git commit -m "feat(module): implement core functionality"

# After refactoring
git add task1/module.py
git commit -m "refactor(module): extract helper function for clarity"

# After documentation
git add docs/*.md task1/*.md
git commit -m "docs: add user guides and API reference"

# Checkpoint commit (end of session)
git add .
git commit -m "Checkpoint from agent session - added XYZ features"
```

### View History
```bash
# One-line format
git log --oneline --graph

# Last 10 commits
git log --oneline -10

# Commits by author
git log --author="username" --oneline

# Commits with specific keyword
git log --grep="database" --oneline
```

### Undo Changes
```bash
# Discard uncommitted changes to a file
git checkout -- task1/module.py

# Discard all uncommitted changes
git reset --hard HEAD

# Amend last commit (if not pushed)
git add forgotten_file.py
git commit --amend --no-edit
```

---

## 🎓 Learning Resources

### Project Documentation
- Start with: `README.md`
- Understand architecture: `docs/DATA_FILTER_ARCHITECTURE.md`
- Learn from mistakes: `docs/learning_examples/DATABASE_IMPLEMENTATION_FIXES.md`
- Agent collaboration: `AGENT_CONVERSATION_PATTERNS.md`

### Code Examples
- CRUD operations: `task1/demo_crud.py`
- Filtering: `task1/demo_filtering_summary.py`
- Visualization: `task1/demo_visualization.ipynb`

### Test Examples
- TDD example: `docs/learning_examples/test_database_loader_TDD_EXAMPLE.py`
- Comprehensive tests: `task1/tests/test_database_loader.py`

---

## ✅ Pre-Submission Checklist

Before finalizing work:

### Code Quality
- [ ] All tests passing: `pytest -v`
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] No TODO/FIXME comments (or tracked in issues)
- [ ] Code follows PEP 8

### Documentation
- [ ] README updated with new features
- [ ] User guides created/updated
- [ ] API documentation current
- [ ] Examples working

### Testing
- [ ] New features have tests
- [ ] Edge cases covered
- [ ] Error handling tested
- [ ] Integration tests pass

### Git
- [ ] All changes committed
- [ ] Commit messages follow convention
- [ ] No sensitive data in repo
- [ ] .gitignore properly configured

### Deliverables
- [ ] All required files present
- [ ] Demo files work
- [ ] Visualizations generated
- [ ] Database loads correctly

---

## 🆘 Getting Help

### Within Project
1. Check relevant guide in `task1/` or `docs/`
2. Look at demo files for examples
3. Review test files for usage patterns
4. Check learning examples for common issues

### External Resources
- Python docs: https://docs.python.org/3/
- Pandas docs: https://pandas.pydata.org/docs/
- Matplotlib docs: https://matplotlib.org/stable/contents.html
- Pytest docs: https://docs.pytest.org/

### Contact
- **Student**: Suhang Liao
- **Email**: u5697414@live.warwick.ac.uk
- **Module**: WM9QF-15

---

*Last Updated*: December 24, 2025  
*Purpose*: Quick reference for daily operations  
*Keep This Updated*: Add new commands and patterns as discovered
