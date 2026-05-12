# PAI Individual Assignment - Data Analysis & Recommendation Systems

This repository contains two Python projects completed for **WM9QF-15 Programming for Artificial Intelligence** at the University of Warwick:

1. **Life Expectancy Data Analysis System** - a data cleaning, SQLite storage, analysis, and visualisation pipeline for WHO-style life expectancy data.
2. **Supermarket Recommendation System** - a graph-based market-basket recommendation engine built from transaction records.

The project was originally developed as an individual coursework submission, but the codebase is structured as a reproducible analytics portfolio project: data loading, cleaning, persistence, querying, analysis, visualisation, testing, and documentation are all included.

---

## Portfolio Summary

| Area | Evidence |
|---|---|
| Data analysis | Filtering, descriptive statistics, trend analysis, Pearson correlation, policy-oriented analysis |
| Data infrastructure | SQLite schema creation, indexed tables, CRUD operations, batch loading, transaction-safe writes |
| Recommendation systems | Graph-based co-occurrence analysis, frequent-pair mining, basket recommendations |
| Software quality | 252 automated tests across both tasks, TDD workflow, SOLID/DRY documentation |
| Reproducibility | CLI entry points, fixed project structure, included datasets, documented run commands |

## Key Results

- Processed **3,111 life-expectancy records** covering **183 countries** from **2000-2016**.
- Built a Load-Clean-Store-Query-Analyze-Visualize workflow using Python and SQLite.
- Implemented indexed SQLite tables and CRUD operations for structured analytical queries.
- Built a supermarket recommendation system from **38,765 transaction records**.
- Constructed a co-purchase graph with **167 items** and **6,260 edges**.
- Verified recommendation performance with a mean query latency of **16.40 microseconds** in the project benchmark.

---

## Repository Structure

```text
PAI_SuhangLiao/
├── task1/                         # Life Expectancy Data Analysis System
│   ├── data/                      # Source and cleaned datasets
│   ├── docs/                      # Detailed task documentation
│   ├── output/                    # Example analysis outputs and charts
│   ├── scripts/                   # Demo and batch-processing scripts
│   ├── src/                       # Core modules
│   │   ├── cleaner.py             # CSV cleaning pipeline
│   │   ├── database_loader.py     # SQLite schema, loading, CRUD operations
│   │   ├── database_cleaner.py    # SQL-based cleaning operations
│   │   ├── data_filter.py         # Analysis and filtering functions
│   │   ├── analysis_correlation.py# Pearson correlation analysis
│   │   ├── visualization.py       # PNG/CSV output generation
│   │   └── menu_cli.py            # Interactive analysis interface
│   └── tests/                     # Task 1 test suite
│
├── task2/                         # Supermarket Recommendation System
│   ├── data/                      # Transaction dataset
│   ├── docs/                      # Detailed task documentation
│   ├── src/                       # Graph and recommendation modules
│   │   ├── graph_interface.py
│   │   ├── graph_adjacency_list.py
│   │   ├── recommendation_engine.py
│   │   └── analyze_graph_density.py
│   ├── tests/                     # Task 2 test suite
│   └── verify_performance_metrics.py
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Quick Start

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Task 1: Life Expectancy Analysis

```bash
python -m task1.main
```

Quick command-line analysis:

```bash
python -m task1.quick_analysis --help
```

Example demo scripts:

```bash
python task1/scripts/pipeline_clean_export.py
python task1/scripts/demo_filtering_summary.py
python task1/scripts/policy_analysis_demo.py
```

### 3. Run Task 2: Supermarket Recommendation

```bash
python -m task2.main
```

Alternative CLI:

```bash
python -m task2.cli
```

Performance benchmark:

```bash
python task2/verify_performance_metrics.py
```

### 4. Run tests

```bash
pytest task1/tests/ -v
pytest task2/tests/ -v
```

---

## Task 1: Life Expectancy Data Analysis System

Task 1 implements a complete analytics workflow for life-expectancy data:

- Load raw CSV records.
- Clean and validate records.
- Store cleaned data in SQLite.
- Query records by country, year, region, and development status.
- Generate descriptive statistics, trend summaries, correlation analysis, and visual outputs.
- Export analysis results as CSV/PNG files.

Important modules:

- [`task1/src/database_loader.py`](task1/src/database_loader.py): SQLite schema creation, indexes, batch loading, CRUD operations.
- [`task1/src/data_filter.py`](task1/src/data_filter.py): analytical filters and summary functions.
- [`task1/src/analysis_correlation.py`](task1/src/analysis_correlation.py): Pearson correlation analysis against life expectancy.
- [`task1/src/visualization.py`](task1/src/visualization.py): chart and table outputs.

Detailed documentation:

- [Task 1 README](task1/docs/README.md)
- [Task 1 Chinese README](task1/docs/README_CN.md)
- [SOLID analysis](task1/docs/SOLID.md)
- [DRY analysis](task1/docs/DRY_ANALYSIS.md)
- [FURPS+ and MoSCoW requirements](task1/docs/FURPS+&MoSCoW.md)

---

## Task 2: Supermarket Recommendation System

Task 2 builds a recommendation system from supermarket transaction records using graph-based co-occurrence analysis.

Supported analysis:

- Single-item recommendations.
- Frequent product-pair discovery.
- Co-purchase frequency checks.
- Basket-based recommendations.
- Dynamic graph updates from new transactions.
- Graph density and performance analysis.

Implementation highlights:

- Adjacency-list graph representation for sparse co-purchase relationships.
- Heap-based Top-K frequent-pair retrieval.
- Dependency-injected recommendation engine.
- Reproducible performance verification script.

Important modules:

- [`task2/src/graph_adjacency_list.py`](task2/src/graph_adjacency_list.py): graph implementation.
- [`task2/src/recommendation_engine.py`](task2/src/recommendation_engine.py): recommendation logic.
- [`task2/verify_performance_metrics.py`](task2/verify_performance_metrics.py): benchmark and verification script.

Detailed documentation:

- [Task 2 README](task2/docs/README.md)
- [Task 2 Chinese README](task2/docs/README_CN.md)
- [Performance verification](task2/PERFORMANCE_VERIFICATION.txt)
- [SOLID analysis](task2/docs/SOLID.md)
- [DRY analysis](task2/docs/DRY_ANALYSIS.md)
- [FURPS+ and MoSCoW requirements](task2/docs/FURPS+&MoSCoW.md)

---

## Technical Stack

- **Language**: Python
- **Data handling**: pandas, NumPy, CSV
- **Database**: SQLite
- **Visualisation**: Matplotlib
- **Testing**: pytest
- **Design practices**: TDD, SOLID, DRY, CLI design, reproducible outputs

---

## Notes

- This repository was submitted for an academic module assessment.
- Some generated databases, logs, and temporary outputs are intentionally excluded from version control.
- The included datasets and source outputs are sufficient to understand and run the core workflows.

## Author

**Suhang Liao**  
MSc Applied Artificial Intelligence, University of Warwick  
Repository: <https://github.com/HenryLiaoW/PAI_SuhangLiao>
