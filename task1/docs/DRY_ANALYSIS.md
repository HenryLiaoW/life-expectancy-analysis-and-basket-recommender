# DRY Principle Analysis
## Task 1: Life Expectancy Data Analysis System

**Project**: Programming for Artificial Intelligence - Individual Assignment  
**Analysis Date**: January 2026  
**Methodology**: DRY (Don't Repeat Yourself) Principle Assessment

---

## Overview

This document demonstrates how the Task 1 implementation applies the DRY principle by centralising repeated logic into reusable components. The analysis focuses on identifying repetition risks across data processing workflows and documenting the design decisions that eliminate duplication while maintaining code clarity and testability.

---

## DRY Principle Assessment

| Aspect | Repetition Risk | DRY Design Decision | Evidence in Implementation |
|--------|----------------|---------------------|---------------------------|
| **Data Cleaning Logic** | Numeric parsing and missing-value handling repeated across loaders, filters, and analyses. | Centralised numeric cleaning into reusable utility functions. | `clean_numeric()` and `clean_row()` used consistently across ingestion and validation pipelines in `cleaner.py`. All downstream components assume pre-cleaned data. |
| **Filtering Operations** | Similar filtering patterns (country, region, year) duplicated across analysis functions. | Abstracted filtering logic into parameterised DataFrame-based functions. | `filter_by_country()`, `filter_by_region()`, `filter_by_year_range()` share a common structure and are reused across all analytical workflows in `data_filter.py`. |
| **Database Access** | SQL queries duplicated across CRUD operations, risking inconsistent parameter binding and transaction handling. | Encapsulated all database interactions in `DatabaseLoader` class with parameterised query methods. | No raw SQL appears outside the persistence layer. All CRUD operations route through `DatabaseLoader.insert()`, `query()`, `update()`, `delete()` methods with consistent transaction semantics. |
| **CLI Workflow** | Menu options risk duplicating business logic if each handler re-implements data loading, validation, and output formatting. | CLI delegates all behaviour to tested modules; `main.py` orchestrates calls without re-implementing logic. | `main.py` routes actions to `data_loader.load_data()`, `data_filter.filter_*()`, and `database_loader.*()` without duplicating their implementations. Business logic resides in tested modules, not UI layer. |
| **Logging & Validation** | Repeated input validation and error handling across multiple entry points. | Centralised validation during data cleaning phase; downstream components assume validated data. | Input validation occurs once in `cleaner.py` during CSV ingestion. Analysis and database modules operate on validated DataFrames, eliminating redundant checks. |

---

## Key Design Insights

### 1. Cleaning Rules as Single Source of Truth
The system applies the DRY principle by centralising repeated logic into reusable components. Data cleaning rules are implemented once in `cleaner.py` and reused across ingestion, analysis, and database persistence:

```python
# Centralized cleaning logic in cleaner.py
def clean_numeric(value: str) -> Optional[float]:
    """Single implementation for all numeric field cleaning"""
    # Used consistently across all data processing paths

def clean_row(row_dict: Dict[str, str]) -> Dict[str, Any]:
    """Single function applies cleaning rules to all records"""
    # Prevents inconsistent handling of missing/malformed values
```

This design prevents inconsistent handling of missing or malformed values across different system components.

---

### 2. Database Access Encapsulation
Similarly, database access logic is fully encapsulated within a dedicated persistence layer (`database_loader.py`):

```python
class DatabaseLoader:
    def insert(self, records):
        """All insertions use parameterised queries"""
        # Single implementation of SQL insertion logic
    
    def query(self, filters):
        """All queries route through this method"""
        # Eliminates duplicated SQL across the system
```

This avoids duplicated SQL across the system and ensures consistent transaction handling.

---

### 3. DataFrame Abstraction Reduces Filtering Duplication
By standardising on pandas DataFrame as the analytical interface, filtering operations are implemented once and reused across all analysis functions:

```python
# Reusable filtering functions in data_filter.py
def filter_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Single implementation reused across all country-based analyses"""
    return df[df['country'] == country]

def filter_by_region(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """Single implementation reused across regional analyses"""
    return df[df['region'] == region]

def filter_by_development_status(df: pd.DataFrame, status) -> pd.DataFrame:
    """Single implementation for GNI-based filtering, supports single/multiple selection"""
    # Reusable logic with World Bank classification thresholds
    # Prevents duplication of income level filtering across analyses
```

Analysis functions compose these primitives rather than re-implementing filtering logic. The development status filter demonstrates DRY by supporting both single and multiple selections through the same implementation, eliminating the need for separate functions.

---

### 4. CLI as Thin Orchestration Layer
The CLI layer (`main.py`) demonstrates DRY by delegating all behaviour to tested modules without re-implementing business logic:

```python
# main.py - thin orchestration without logic duplication
def cmd_analyze_country(session, country):
    """Delegates to tested analysis module"""
    data = filter_by_country(session.df, country)  # Reuses filtering
    results = compute_statistics(data)              # Reuses analysis
    # No business logic duplicated in UI layer
```

This design reduces maintenance overhead and ensures that changes to data handling or validation rules propagate consistently throughout the application.

---

## Implementation Evidence

### Test Coverage
- **135 automated tests** validate that shared logic behaves consistently:
  - Data cleaning tests ensure `clean_numeric()` and `clean_row()` handle edge cases uniformly
  - Filtering tests verify parameterised functions produce expected results
  - Database tests confirm CRUD operations use consistent transaction semantics
  
### Code Metrics
- **Zero SQL duplication**: All database queries encapsulated in `DatabaseLoader` class
- **Single cleaning implementation**: `cleaner.py` contains the only numeric validation logic
- **Parameterised filtering**: 5 filter functions (`filter_by_country`, `filter_by_region`, `filter_by_year_range`, etc.) reused across 12 analysis functions

### Refactoring Confidence
- Centralised cleaning logic enabled addition of new health indicators (e.g., `schooling`, `income_composition`) without modifying validation rules in multiple locations
- Database schema changes required updates only in `DatabaseLoader`, not in analysis or CLI modules

---

## Conclusion

The Task 1 implementation demonstrates mature application of the DRY principle by identifying repetition risks early and centralising logic into reusable, well-tested components. Key achievements include:

1. **Single Source of Truth**: Data cleaning, filtering, and database access each have exactly one implementation
2. **Reduced Maintenance Overhead**: Changes to validation rules or SQL queries require updates in only one location
3. **Improved Testability**: Shared logic is validated once through comprehensive test coverage, eliminating redundant test cases

This approach simplifies refactoring and guarantees that optimisation or bug fixes apply uniformly across the system.
