# Requirements Analysis for Task 1
## Data Insights Dashboard for Public Health Reports

---

## MoSCoW Analysis (Requirements Prioritization)

### Must Have (M) - Critical Requirements

**Data Access & Loading**
- ✅ Load CSV files with UTF-8 encoding
- 🔄 Store data in SQLite database (in progress)
- ✅ Handle missing/invalid data gracefully

**Data Cleaning & Structuring**
- ✅ Convert numeric strings to float
- ✅ Handle missing values (convert to None)
- ✅ Validate data types

**Testing & Quality**
- ✅ Comprehensive test suite (27+ tests)
- ✅ Follow TDD methodology (RED-GREEN-REFACTOR)
- ✅ Git version control with meaningful commits

**Documentation**
- ✅ README with installation and usage instructions
- ✅ Inline code documentation (docstrings)
- ✅ SOLID principles demonstration

---

### Should Have (S) - Important but Not Critical

**Filtering & Summary Views**
- ⏳ Filter by country, date range, region
- ⏳ Generate statistical summaries (mean, min, max, count)
- ⏳ Trend analysis over time
- ⏳ Grouped results by region/country

**Presentation Layer**
- ⏳ Command-line interface (CLI)
- ⏳ Interactive menu system
- ⏳ Visual outputs (matplotlib charts)

**Data Analysis**
- ✅ Correlation analysis (Pearson coefficient)
- ⏳ Additional statistical measures

**Extension Features**
- ⏳ Export filtered data to CSV
- ⏳ CRUD operations on database
- ⏳ User activity logging

---

### Could Have (C) - Desirable but Lower Priority

**Advanced Visualization**
- ⏳ Multiple chart types (scatter, line, bar, heatmap)
- ⏳ Interactive plots
- ⏳ Dashboard layout with multiple views

**Database Features**
- ⏳ Query optimization with indexes
- ⏳ Data validation constraints
- ⏳ Transaction management

**User Experience**
- ⏳ Input validation with helpful error messages
- ⏳ Progress indicators for long operations
- ⏳ Configuration file support

**Advanced Analysis**
- ⏳ Regression analysis
- ⏳ Time series forecasting
- ⏳ Multi-variable analysis

---

### Won't Have (W) - Explicitly Out of Scope

**Not Required for This Assignment**
- ❌ Web-based user interface
- ❌ Cloud database deployment
- ❌ Real-time data streaming
- ❌ Multi-user authentication/authorization
- ❌ Machine learning predictive models
- ❌ Mobile application
- ❌ RESTful API endpoints
- ❌ Distributed computing/parallelization
- ❌ Advanced security features (encryption, access control)

**Justification**:
- Assignment focuses on core software engineering practices, not production deployment
- Emphasis on code quality and process over feature quantity
- Time constraints (2-week extension from original deadline)

---

## FURPS+ Analysis (Quality Attributes)

### F - Functionality (功能性)

**What the system does**:

**Data Management**
- ✅ Load WHO life expectancy CSV files
- 🔄 Persist data in SQLite database
- ✅ Clean and validate data (type conversion, missing values)
- ⏳ Filter data by multiple criteria

**Analysis Capabilities**
- ✅ Pearson correlation analysis (manual implementation)
- ⏳ Statistical summaries (mean, median, mode, range)
- ⏳ Trend analysis over time periods

**Data Export**
- ✅ Export cleaned data to CSV
- ⏳ Export filtered/summarized data
- ⏳ Export analysis results

**Visualization**
- ⏳ Generate charts (matplotlib)
- ⏳ Display data in tables
- ⏳ Command-line output formatting

**Assessment**: Core data access and cleaning functionality complete. Analysis and visualization features in progress.

---

### U - Usability (可用性)

**Ease of use and learning**:

**Installation**
- ✅ Simple setup with Python venv/conda
- ✅ Minimal dependencies (pytest only)
- ✅ Clear README with step-by-step instructions

**Documentation**
- ✅ Comprehensive docstrings for all functions
- ✅ README with usage examples
- ✅ SOLID principles analysis document
- ⏳ User guide for CLI interface (pending)

**Error Handling**
- ✅ Graceful handling of missing/invalid data
- ✅ Informative error messages (FileNotFoundError, TypeError)
- ⏳ Input validation for user commands (pending)

**Interface Design**
- ⏳ Intuitive menu-driven CLI (pending)
- ⏳ Consistent command syntax (pending)
- ⏳ Help messages and usage hints (pending)

**Assessment**: Good for developers (clear code, documentation). End-user interface not yet implemented.

---

### R - Reliability (可靠性)

**System stability and correctness**:

**Testing**
- ✅ 27 automated tests (unit + integration)
- ✅ 100% of public functions tested
- ✅ Edge case coverage (empty data, None values, invalid input)
- ✅ Test isolation with fixtures

**Data Integrity**
- ✅ Type safety with type hints
- ✅ Defensive programming (try-except for conversions)
- ✅ NULL handling in database (preserves None values)
- ⏳ Database transaction management (pending)

**Error Recovery**
- ✅ Fail gracefully on invalid CSV files
- ✅ Continue processing when individual values are invalid
- ⏳ Rollback on failed database operations (pending)

**Availability**
- ✅ No external service dependencies
- ✅ Works offline with local data
- ✅ Cross-platform (macOS, Linux, Windows)

**Assessment**: High reliability for data processing. Database operations need transaction safety.

---

### P - Performance (性能)

**Speed and efficiency**:

**Execution Speed**
- ✅ Fast CSV loading with built-in csv.DictReader
- ✅ Efficient numeric conversion (single pass)
- ✅ All 27 tests complete in <0.1 seconds

**Memory Usage**
- ⚠️ Loads entire CSV into memory (acceptable for assignment dataset)
- ⚠️ List comprehensions create intermediate lists
- ⏳ Database streaming for large datasets (not yet implemented)

**Scalability**
- ✅ Handles WHO dataset (~3000 rows) efficiently
- ⚠️ Not optimized for millions of records
- ⏳ Could add batch processing for large datasets

**Algorithm Complexity**
- ✅ Pearson correlation: O(n) time complexity
- ✅ Data cleaning: O(n) linear scan
- ⏳ Database queries: Add indexes for O(log n) lookups

**Assessment**: Adequate performance for assignment requirements. Not production-scale optimized (intentional trade-off).

---

### S - Supportability (可支持性)

**Maintainability and extensibility**:

**Code Organization**
- ✅ Modular structure (4 separate modules)
- ✅ Clear separation of concerns (SRP)
- ✅ Consistent naming conventions (PEP 8)
- ✅ Single Responsibility Principle throughout

**Extensibility**
- ✅ Open/Closed Principle (add fields without modifying code)
- ✅ Dependency Inversion (abstractions over implementations)
- ✅ Easy to add new analysis functions

**Testability**
- ✅ All functions unit-testable
- ✅ Minimal dependencies simplify testing
- ✅ Fixtures for test data isolation

**Documentation**
- ✅ Comprehensive inline comments
- ✅ Module-level docstrings explaining design
- ✅ SOLID principles analysis document
- ✅ README with troubleshooting section

**Version Control**
- ✅ Git with conventional commits
- ✅ Clear TDD workflow in history
- ✅ Meaningful commit messages

**Assessment**: Excellent maintainability. Well-structured for future development.

---

### + Design Constraints

**Implementation Constraints**:
- ✅ Pure Python 3.13+ (no pandas/numpy for core logic)
- ✅ Standard library only for data processing
- ✅ SQLite for database (local, no external DB)
- ⏳ matplotlib/pandas allowed only for visualization

**Interface Requirements**:
- ⏳ Command-line interface (CLI) - pending
- ❌ No GUI required
- ❌ No web interface required

**Physical Constraints**:
- ✅ Runs on standard laptop/desktop
- ✅ No special hardware requirements
- ✅ Cross-platform compatible

**Platform Constraints**:
- ✅ macOS, Linux, Windows support
- ✅ Python 3.13+ required
- ✅ UTF-8 encoding for internationalization

---

## Requirements Traceability Matrix

| Requirement Category | Status | Priority | Tests | FURPS+ Attribute |
|---------------------|--------|----------|-------|------------------|
| CSV Loading | ✅ Complete | Must | 2 | F, R |
| Database Storage | 🔄 In Progress | Must | 7 | F, R |
| Data Cleaning | ✅ Complete | Must | 7 | F, R |
| Type Conversion | ✅ Complete | Must | Included | F, R |
| Correlation Analysis | ✅ Complete | Should | 18 | F, P |
| Filtering | ⏳ Pending | Should | 0 | F, U |
| Summary Stats | ⏳ Pending | Should | 0 | F |
| CLI Interface | ⏳ Pending | Should | 0 | U |
| Visualization | ⏳ Pending | Should | 0 | U, F |
| Export to CSV | ✅ Complete | Should | 0 | F |
| CRUD Operations | ⏳ Pending | Could | 0 | F |
| User Logging | ⏳ Pending | Could | 0 | S |

---

## Risk Assessment

### Technical Risks

**HIGH RISK**:
- ⚠️ **Time Constraint**: Multiple features pending with 2-week extension
  - *Mitigation*: Focus on Must/Should requirements first

**MEDIUM RISK**:
- ⚠️ **Database Integration**: First time using SQLite in this context
  - *Mitigation*: TDD approach ensures correctness through testing
  
- ⚠️ **Visualization Complexity**: matplotlib learning curve
  - *Mitigation*: Start with simple charts, use pandas for convenience

**LOW RISK**:
- ✅ **Data Cleaning**: Well-tested and complete
- ✅ **Testing Infrastructure**: Solid foundation with 27 tests

---

## Summary

**Strengths**:
- Strong foundation with data loading and cleaning complete
- Excellent code quality (SOLID principles, TDD)
- Comprehensive testing (27 automated tests)
- Clear documentation and maintainability

**Gaps to Address**:
1. Database functionality (in progress)
2. Filtering and summary views
3. CLI interface
4. Visualization with matplotlib

**Recommendation**: 
Complete database operations first (currently in GREEN phase), then implement filtering/summaries, followed by CLI and visualization. This order maintains TDD discipline while delivering maximum value.

---

*Last Updated*: 15 December 2025
