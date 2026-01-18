# PAI Individual Assignment - Suhang Liao

**Module**: WM9QF-15 Programming for Artificial Intelligence  
**Date**: December 2025  
**Repository**: https://github.com/HenryLiaoW/PAI_SuhangLiao

---

## 📁 Project Structure

This repository contains Task 1 and Task 2 of the Programming for Artificial Intelligence individual assignment.

```
PAI_SuhangLiao/
├── task1/                          # Task 1: Life Expectancy Data Analysis System
│   ├── docs/                       # 📚 Project documentation
│   │   ├── README.md               # ⭐ Complete documentation (English)
│   │   ├── README_CN.md            # 中文版项目文档
│   │   ├── FURPS+&MoSCoW.md        # Requirements analysis
│   │   ├── SOLID.md                # SOLID principles analysis
│   │   └── DRY_ANALYSIS.md         # DRY principle analysis
│   │
│   ├── main.py                     # Main entry point
│   ├── quick_analysis.py           # Quick query CLI tool
│   ├── scripts/                    # Demo & example scripts
   ├── src/                        # Core modules (11 modules)
   │   ├── menu_cli.py             # Interactive analysis menu
   │   ├── data_filter.py          # Analysis functions (14 functions)
│   │   ├── database_loader.py      # Database CRUD operations
│   │   └── cleaner.py              # Data cleaning
│   └── tests/                      # Test suite (167 tests)
│       ├── test_development_status_filter.py # 32 tests
│
├── task2/                          # Task 2: Supermarket Recommendation System
│   ├── docs/                       # 📚 Project documentation
│   │   ├── README.md               # ⭐ Complete documentation (English)
│   │   ├── README_CN.md            # 中文版项目文档
│   │   ├── FURPS+&MoSCoW.md        # Requirements analysis
│   │   ├── SOLID.md                # SOLID principles analysis
│   │   └── DRY_ANALYSIS.md         # DRY principle analysis
│   │
│   ├── main.py                     # Entry point (interactive menu)
│   ├── cli.py                      # Command-line interface
│   ├── verify_performance_metrics.py # Performance verification script
│   ├── PERFORMANCE_VERIFICATION.txt  # Timestamped results
│   │
│   ├── src/                        # Core modules
│   │   ├── graph_adjacency_list.py  # Graph implementation (adjacency list)
│   │   ├── graph_interface.py       # Graph interface (ABC)
│   │   ├── recommendation_engine.py # Market basket analysis engine
│   │   └── analyze_graph_density.py # Density analysis
│   │
│   └── tests/                      # Test suite (85 tests)
│       ├── test_main.py            # 56 tests (integration & edge cases)
│       ├── test_recommendation_engine.py # 24 tests
│       ├── test_graph_adjacency_list.py  # 16 tests
│       └── test_smoke.py           # 1 smoke test
│
└── pytest.ini                      # Test configuration

```

---

## 🚀 Quick Start

### Task 1: Life Expectancy Data Analysis

**Complete Documentation**: [task1/docs/README.md](task1/docs/README.md) | [中文版](task1/docs/README_CN.md)

```bash
# Run interactive menu (recommended)
python -m task1.main

# Run command-line analysis tool
python -m task1.quick_analysis --help

# Run tests (167 tests)
pytest task1/tests/ -v
```

### Task 2: Supermarket Recommendation System

**Complete Documentation**: [task2/docs/README.md](task2/docs/README.md) | [中文版](task2/docs/README_CN.md)

```bash
# Run interactive menu (recommended)
python -m task2.main

# Run CLI (interactive mode)
python -m task2.cli

# Run tests (85 tests)
pytest task2/tests/ -v

# Verify performance metrics
python task2/verify_performance_metrics.py
```

---

## 📊 Project Highlights

### Task 1: Life Expectancy Analysis
- **167 automated tests** with TDD methodology (including 32 for development status filter)
- **SOLID principles** applied throughout design
- **Policy-oriented analysis** focusing on modifiable health factors
- **Development status filtering** by World Bank GNI classification (high/upper-middle/lower-middle/low)
- **3 CLI interfaces** for different user workflows
- **3,111 WHO records** covering 183 countries (2000-2016)

### Task 2: Supermarket Recommendation System
- **85 automated tests** with 100% pass rate (TDD approach)
- **Graph-based co-occurrence analysis** using adjacency list
- **Heap optimization**: O(E log k) instead of O(E log E) for Top-K
- **Market basket analysis** for product recommendations
- **Efficient pattern mining** from customer transaction data

---

## 📚 Key Documentation

### Task 1 Documentation ([`task1/docs/`](task1/docs/))

| Document | Description |
|----------|-------------|
| [README.md](task1/docs/README.md) | Complete project documentation (English) |
| [README_CN.md](task1/docs/README_CN.md) | 完整项目文档（中文） |
| [FURPS+&MoSCoW.md](task1/docs/FURPS+&MoSCoW.md) | Requirements analysis with FURPS+ methodology |
| [SOLID.md](task1/docs/SOLID.md) | SOLID principles analysis with evidence |
| [DRY_ANALYSIS.md](task1/docs/DRY_ANALYSIS.md) | DRY principle implementation analysis |

### Task 2 Documentation ([`task2/docs/`](task2/docs/))

| Document | Description |
|----------|-------------|
| [README.md](task2/docs/README.md) | Complete project documentation (English) |
| [README_CN.md](task2/docs/README_CN.md) | 完整项目文档（中文） |
| [FURPS+&MoSCoW.md](task2/docs/FURPS+&MoSCoW.md) | Requirements analysis with FURPS+ methodology |
| [SOLID.md](task2/docs/SOLID.md) | SOLID principles analysis with evidence |
| [DRY_ANALYSIS.md](task2/docs/DRY_ANALYSIS.md) | DRY principle implementation analysis |
| [verify_performance_metrics.py](task2/verify_performance_metrics.py) | Automated performance verification script |
| [PERFORMANCE_VERIFICATION.txt](task2/PERFORMANCE_VERIFICATION.txt) | Timestamped performance test results |

---

## 🎯 Assessment Criteria Addressed

✅ **Functional Requirements**: Task 1 (data analysis) & Task 2 (data structures & algorithms)  
✅ **Test Coverage**: 252 automated tests (167 + 85) with TDD methodology  
✅ **Design Principles**: SOLID & DRY principles with documented evidence in both tasks  
✅ **Code Clarity**: Comprehensive docstrings, type hints, clear structure  
✅ **Version Control**: Git repository with test files (test_main.py for both tasks)  
✅ **Documentation**: Complete READMEs with run commands, edge case testing, performance verification

---

## 👤 Author

**Suhang Liao**  
Student ID: 5697414
Email: u5697414@live.warwick.ac.uk

---

## 📄 License

This project is submitted as part of the WM9QF-15 Programming for Artificial Intelligence module assessment.

---

**For complete documentation, please see [task1/docs/README.md](task1/docs/README.md)**
