# FURPS+ Requirements Analysis
## Supermarket Recommendation System

**Project**: Task 2 - Graph-Based Product Recommendation Engine  
**Analysis Date**: January 2026  
**Methodology**: FURPS+ + MoSCoW Prioritization

---

## Requirements Table

| # | Requirement | Acceptance Criteria | FURPS+ Category | MoSCoW Priority |
|---|-------------|---------------------|-----------------|-----------------|
| **1** | The system shall support item-level association queries, incremental transaction updates, and retrieval of global Top-K co-purchased item pairs. | Given an item name, the system returns a ranked list of co-purchased items; new transactions update edge weights correctly; global Top-K frequent item pairs can be retrieved deterministically. | F (Functionality) | **Must** |
| **2** | The system shall provide a simple and deterministic interface for querying recommendations. | Recommendation outputs are consistently ordered across repeated runs; tie-breaking rules are explicitly defined (count desc, name asc). | U (Usability) | **Must** |
| **3** | The system shall ensure stable behaviour under repeated queries and edge cases. | Identical recommendation calls return identical outputs; empty or low-frequency items do not cause runtime errors. | R (Reliability) | **Must** |
| **4** | The system shall efficiently compute Top-K frequent item pairs without full sorting. | Top-K selection runs in O(E log k) time using heap-based selection; empirical measurements show 16.40μs mean query latency over 1,000 iterations. | P (Performance) | **Must** |
| **5** | The system shall enable future changes to graph representation or recommendation logic without major refactoring. | Recommendation logic is decoupled from concrete graph implementation via abstraction; alternative graph structures can be introduced without modifying recommendation engine code. | S (Supportability) | **Should** |
| **6** | The system shall be testable, extensible, and aligned with TDD practices. | Core behaviours are validated through automated unit and integration tests (85 tests); refactoring does not break existing functionality as confirmed by test suite. | + (Design Constraints) | **Must** |

---

## MoSCoW Priority Summary

| Priority | Count | Key Requirements |
|----------|-------|------------------|
| **Must Have** | 5 | Item-level queries and Top-K retrieval, Deterministic recommendation ordering, Reliable edge case handling, Sub-20μs query performance, Comprehensive test coverage (85 tests) |
| **Should Have** | 1 | Graph abstraction for extensibility (DIP compliance) |
| **Could Have** | - | Web API interface, Real-time transaction streaming, Graph visualization dashboard |
| **Won't Have** | - | User authentication, Distributed graph storage, Machine learning-based recommendations |

---

## Notes

- **Performance Validation**: Query latency measured via `time.perf_counter()` with 5-run averaging; reproducible via `verify_performance_metrics.py`.
- **Testability**: 85 automated tests ensure deterministic behavior and enable confident refactoring.
- **Key Trade-off**: Prioritized algorithmic efficiency (heap-based Top-K) over feature breadth to meet performance requirements.
