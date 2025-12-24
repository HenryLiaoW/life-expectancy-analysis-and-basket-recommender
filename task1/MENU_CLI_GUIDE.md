# Life Expectancy Data Pipeline System - Menu CLI

## 🎯 Overview

Interactive menu-driven CLI designed for AI and Data Science teams to support the complete data pipeline workflow:

**Access → Filter → Clean → Summarize → Present**

## 🚀 Quick Start

### Run with Demo Database (12 records)
```bash
cd /Users/henry/AAI/PAI/individual/PAI_SuhangLiao
PYTHONPATH=$PWD python task1/menu_cli.py --db task1/data/CLI_demo.db
```

### Run with Full Database (3111 records)
```bash
PYTHONPATH=$PWD python task1/menu_cli.py --db task1/data/life_expectancy.db
```

## 📋 Menu Structure

### Section 1: DATA ACCESS (Database Management)
- **1.1** View database info & statistics
- **1.2** Create new record (Interactive)
- **1.3** Update existing record
- **1.4** Delete record

### Section 2: DATA FILTERING (Query & Selection)
- **2.1** Filter by country
- **2.2** Filter by region
- **2.3** Filter by year range
- **2.4** Clear all filters
- **2.5** Preview current dataset

### Section 3: DATA CLEANING (Quality Control) ★
- **3.1** Handle missing values
- **3.2** Remove duplicate records
- **3.3** Validate data integrity
- **3.4** Show data quality report
- **3.5** Apply full cleaning pipeline

⚠️ Cleaning applies to current filtered data

### Section 4: DATA SUMMARIZATION (Analysis & Aggregation)
- **4.1** Correlation analysis
- **4.2** Country comparison
- **4.3** Statistical summary
- **4.4** Policy recommendations

### Section 5: DATA PRESENTATION (Visualization & Export)
- **5.1** Export current data to CSV
- **5.2** Generate visualization
- **5.3** Generate full report

### Other Options
- **h** - Show workflow guide (recommended pipeline)
- **0** - Exit system

## 🎓 Recommended Workflow Example

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   ACCESS    │────▶│   FILTER    │────▶│    CLEAN    │
│  (Load DB)  │     │ (Selection) │     │  (Quality)  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   PRESENT   │◀────│  SUMMARIZE  │◀────│ Cleaned Data│
│(Export/Viz) │     │  (Analysis) │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Example Session:

1. **ACCESS (1.1)**: View database info → 12 records
2. **FILTER (2.2)**: Select Region=Asia → 9 records
3. **FILTER (2.3)**: Add Year range 2015-2017 → 9 records
4. **PREVIEW (2.5)**: Review filtered dataset
5. **CLEAN (3.5)**: Apply full cleaning pipeline → 9 valid records
6. **ANALYZE (4.1)**: Run correlation analysis → health-spending r=0.65
7. **EXPORT (5.1)**: Export to `exported_data_Asia.csv`

## 💡 Key Features

### Session State Management
The system tracks your workflow:
- **Current filters**: Country, Region, Year range
- **Data status**: Cleaned ✓ / Not cleaned
- **Record count**: Updates in real-time

Status bar shows: `[Filter: Region=Asia] | Records: 9 | Cleaned ✓`

### Data Flow Intelligence
- Filter operations affect subsequent analysis
- Cleaning applies only to filtered subset
- Export saves the current working dataset
- All operations preserve original data

### User-Friendly Design
- Clear visual hierarchy with box borders
- Numbered menu system (e.g., 2.1, 3.5)
- Real-time feedback (✅ ❌ ⚠️)
- Confirmation prompts for destructive operations

## 🔧 Technical Details

### Architecture

**AnalysisSession Class**:
- Manages data pipeline state
- Tracks filtered_data vs cleaned_data
- Provides status reporting

**Modular Integration**:
- `database_loader.py` → Section 1 (Access)
- `data_filter.py` → Section 2 (Filter)
- `cleaner.py` → Section 3 (Clean)
- `analysis_correlation.py` → Section 4 (Summarize)
- Export functions → Section 5 (Present)

### Comparison: Menu vs Command-Line Mode

| Feature | Menu CLI | Original CLI |
|---------|----------|--------------|
| **Discovery** | All options visible | Must know commands |
| **Workflow** | Guided step-by-step | Manual chaining |
| **State** | Session-based | Stateless |
| **Learning** | Low learning curve | Requires docs |
| **Automation** | Not suitable | Excellent for scripts |
| **Use Case** | Demo, Education, Exploration | Testing, Automation |

**Both modes coexist**: Use menu for exploration, CLI for automation!

## 📊 Design Rationale (For Academic Report)

This system addresses the assignment requirement:

> "Support data access, filtering, cleaning, aggregation, and presentation (not predictive modeling). This simulates tools that software developers might build to support AI or Data Science teams."

### How It Meets Requirements:

| Requirement | Implementation | Menu Section |
|-------------|----------------|--------------|
| **Data Access** | CRUD operations via database_loader | Section 1 |
| **Filtering** | Country/Region/Year filters via data_filter | Section 2 |
| **Cleaning** | Missing values, duplicates, validation | Section 3 ★ |
| **Aggregation** | Correlation, statistics, comparison | Section 4 |
| **Presentation** | CSV export, visualizations, reports | Section 5 |

### Software Engineering Principles:

**1. Separation of Concerns**:
- Session management (AnalysisSession)
- Business logic (existing modules)
- Presentation (menu functions)

**2. Open-Closed Principle**:
- Easy to add new menu options
- Existing modules unchanged

**3. Single Responsibility**:
- Each cmd_* function handles one feature

**4. User-Centered Design**:
- Progressive disclosure
- Clear feedback
- Workflow guidance

## 🎯 For AI/DS Teams

### Why This Tool?

**Problem**: Data scientists often receive raw data that needs:
- Exploration (What's in it?)
- Filtering (Select relevant subset)
- Cleaning (Handle quality issues)
- Analysis (Find patterns)
- Export (Share with team)

**Solution**: This tool provides a **guided workflow** to:
1. Understand the dataset (Section 1)
2. Select relevant data (Section 2)
3. Ensure quality (Section 3)
4. Generate insights (Section 4)
5. Share results (Section 5)

### Real-World Use Cases:

**Case 1: Regional Health Analysis**
```
Filter by Region=Europe → Clean data → Analyze correlations → Export for ML model
```

**Case 2: Country Comparison Study**
```
Filter by countries (China, USA, India) → Compare trends → Generate report
```

**Case 3: Data Quality Check**
```
Load full database → Run quality report → Identify issues → Apply cleaning
```

## 🚀 Future Enhancements

- [ ] Save and load filter presets
- [ ] Export pipeline as Python script (reproducibility)
- [ ] Interactive visualizations (matplotlib integration)
- [ ] Batch processing mode
- [ ] REST API for programmatic access
- [ ] Web interface (Flask/FastAPI)

## 📝 Testing the System

### Quick Test Workflow:

```bash
# Start the system
PYTHONPATH=$PWD python task1/menu_cli.py --db task1/data/CLI_demo.db

# Follow this sequence:
1. Press 'h' → Read workflow guide
2. Press '1.1' → View database info (12 records)
3. Press '2.2' → Filter by Region, enter "Asia" (9 records)
4. Press '2.5' → Preview filtered data
5. Press '3.4' → Show quality report
6. Press '4.1' → Run correlation analysis
7. Press '5.1' → Export to CSV
8. Press '0' → Exit
```

### Expected Output:

- Status bar updates after each operation
- Clear feedback messages (✅ ❌)
- Record count changes reflected
- Files saved in `task1/output/`

## 📚 Related Documentation

- [CLI Usage Guide](CLI_USAGE.md) - Original command-line mode
- [CRUD CLI Guide](CRUD_CLI_GUIDE.md) - Interactive CRUD operations
- [Data Filter Architecture](../docs/DATA_FILTER_ARCHITECTURE.md) - System design
- [Test Database Guide](TEST_DATABASE_GUIDE.md) - Testing setup

---

**Designed for**: PAI Assignment - Supporting AI/DS Teams
**Author**: Suhang Liao
**Date**: December 2025
