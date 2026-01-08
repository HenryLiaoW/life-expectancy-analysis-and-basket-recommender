# FURPS+ Requirements Analysis
## Life Expectancy Data Insights Dashboard

**Project**: Task 1 - Data Insights Dashboard for Public Health Policy Analysis  
**Analysis Date**: January 2026  
**Methodology**: FURPS+ + MoSCoW Prioritization

---

## Requirements Table

| # | Requirement | Acceptance Criteria | FURPS+ Category | MoSCoW Priority |
|---|-------------|---------------------|-----------------|-----------------|
| **1** | The system shall load public health data from a CSV file and make it available for analysis. | CSV data is successfully parsed, cleaned, and loaded into memory; records can be queried by year, country, and region via CLI without runtime errors. | F (Functionality) | **Must** |
| **2** | The system shall robustly handle missing, malformed, or inconsistent data values. | Invalid numeric fields are converted to None, type errors are avoided, and downstream analysis functions execute without failure on incomplete datasets. | R (Reliability) | **Must** |
| **3** | The system shall support descriptive statistical analysis and correlation-based exploration of life expectancy indicators. | Users can compute summary statistics and correlation values for selected indicators, and results are reproducible across repeated executions. | F (Functionality) | **Must** |
| **4** | The system shall provide a clear, menu-driven command-line interface for exploratory analysis. | Users can navigate analysis, database, and export workflows through explicit menu options without modifying source code. | U (Usability) | **Should** |
| **5** | The system shall persist cleaned data in a local database and support CRUD operations. | Records can be created, read, updated, and deleted using parameterised SQL queries, with changes correctly reflected in subsequent queries. | F (Functionality) | **Should** |
| **6** | The system shall ensure database consistency during write operations. | All database updates are executed within transactions; failures trigger rollback without leaving partial updates. | R (Reliability) | **Should** |
| **7** | The system shall execute analytical queries with low latency on the given dataset. | Query execution completes in sub-second response times for 3,111-record dataset operations. | P (Performance) | **Could** |
| **8** | The system shall allow new analytical indicators to be added without modifying existing analysis logic. | New indicators can be introduced by extending DataFrame-based analysis functions without changes to database or cleaning modules. | S (Supportability) | **Could** |
| **9** | The system shall support automated testing of analysis, cleaning, and database components. | Unit tests execute independently with deterministic results; database tests run using isolated fixtures. | S (Supportability) | **Must** |
| **10** | The system shall exclude predictive modelling and causal inference. | No predictive algorithms or forecasting outputs are implemented; all results are descriptive and correlation-based only. | + (Constraints) | **Must** |

---

## MoSCoW Priority Summary

| Priority | Count | Key Requirements |
|----------|-------|------------------|
| **Must Have** | 5 | Data loading, Data cleaning robustness, Descriptive analysis, Automated testing, Constraint compliance (no predictive modelling) |
| **Should Have** | 3 | Menu-driven CLI, Database persistence (CRUD), Transaction consistency |
| **Could Have** | 2 | Query performance optimization, Extensible analysis framework (OCP) |
| **Won't Have** | - | Predictive modelling, Real-time data streaming, Web interface, Multi-user concurrent access |
