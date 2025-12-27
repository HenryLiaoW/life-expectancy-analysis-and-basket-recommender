# PAI Individual Assignment - Suhang Liao

**Module**: WM9QF-15 Programming for Artificial Intelligence  
**Date**: December 2025

---

## 📁 Project Structure

This repository contains Task 1 of the Programming for Artificial Intelligence individual assignment.

```
PAI_SuhangLiao/
├── task1/                          # Task 1: Life Expectancy Data Analysis System
│   ├── docs/                       # 📚 All project documentation
│   │   ├── README.md               # ⭐ Complete project documentation
│   │   ├── README_CN.md            # 中文版项目文档
│   │   ├── REFLECTIVE_REPORT.md    # Academic reflection report
│   │   ├── REQUIREMENTS_ANALYSIS.md
│   │   ├── SOLID_PRINCIPLES_ANALYSIS.md
│   │   ├── CLI_ARCHITECTURE.md
│   │   ├── ROBUSTNESS_ANALYSIS.md
│   │   └── ...
│   │
│   ├── main.py                     # Main entry point
│   ├── menu_cli.py                 # Interactive analysis menu
│   ├── analysis_cli.py             # Command-line analysis tool
│   ├── data_filter.py              # Analysis functions (12 functions)
│   ├── database_loader.py          # Database CRUD operations
│   ├── cleaner.py                  # Data cleaning
│   └── tests/                      # Test suite (135 tests)
│
└── pytest.ini                      # Test configuration

```

---

## 🚀 Quick Start

### 1. View Complete Documentation

**English**: [task1/docs/README.md](task1/docs/README.md)  
**中文**: [task1/docs/README_CN.md](task1/docs/README_CN.md)

### 2. Run the System

```bash
# Option 1: Interactive menu (recommended)
python -m task1.main

# Option 2: Command-line analysis tool
python task1/analysis_cli.py --help
```

### 3. Run Tests

```bash
# Run all tests
pytest task1/tests/ -v

# Expected: 135 passed in ~1.2s
```

---

## 📊 Project Highlights

- **158 automated tests** (135 in task1/tests/ + 23 in docs/learning_examples/)
- **Test-Driven Development (TDD)** with comprehensive Git history
- **SOLID principles** applied throughout design
- **Policy-oriented analysis** focusing on modifiable health factors
- **3 CLI interfaces** for different user workflows
- **3,111 WHO records** covering 183 countries (2015-2017)

---

## 📚 Key Documentation

All documentation is located in [`task1/docs/`](task1/docs/):

| Document | Description |
|----------|-------------|
| [README.md](task1/docs/README.md) | Complete project documentation (English) |
| [README_CN.md](task1/docs/README_CN.md) | 完整项目文档（中文） |
| [REFLECTIVE_REPORT.md](task1/docs/REFLECTIVE_REPORT.md) | Academic reflection on methodological choices |
| [REQUIREMENTS_ANALYSIS.md](task1/docs/REQUIREMENTS_ANALYSIS.md) | Detailed requirements analysis |
| [SOLID_PRINCIPLES_ANALYSIS.md](task1/docs/SOLID_PRINCIPLES_ANALYSIS.md) | SOLID principles application |
| [CLI_ARCHITECTURE.md](task1/docs/CLI_ARCHITECTURE.md) | CLI tools architecture explanation |
| [ROBUSTNESS_ANALYSIS.md](task1/docs/ROBUSTNESS_ANALYSIS.md) | Code quality validation report |

---

## 🎯 Assessment Criteria Addressed

✅ **Functional Requirements**: Data loading, cleaning, analysis, visualization, interactive CLI  
✅ **Software Quality**: TDD methodology, 158 automated tests, 0 warnings  
✅ **Design Principles**: SOLID principles with documented evidence  
✅ **Code Clarity**: Comprehensive docstrings, type hints, clear structure  
✅ **Version Control**: 65+ Git commits demonstrating TDD workflow  
✅ **Documentation**: Complete README, reflective report, technical documentation

---

## 👤 Author

**Suhang Liao**  
Student ID: [Your Student ID]  
Email: [Your Email]

---

## 📄 License

This project is submitted as part of the WM9QF-15 Programming for Artificial Intelligence module assessment.

---

**For complete documentation, please see [task1/docs/README.md](task1/docs/README.md)**
