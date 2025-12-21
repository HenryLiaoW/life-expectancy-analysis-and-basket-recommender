# Data Filter Module - Architecture Documentation

**Date**: 18 December 2025  
**Module**: `task1/data_filter.py`  
**Test Suite**: `task1/tests/test_data_filter.py`  
**Total Functions**: 12  
**Total Tests**: 46  

---

## 🏗️ Architecture Overview - Pyramid Structure

The data filter module is designed with a **4-layer pyramid architecture**, from low-level data access to high-level policy decision support.

```
                    🎯 DECISION SUPPORT LAYER
        ┌─────────────────────────────────────────────┐
        │  get_policy_intervention_priorities()       │  ← Policy recommendations
        │     Input: country + target life expectancy │
        │     Output: which factors to improve         │
        └─────────────────────────────────────────────┘
                            ↑ calls
        ┌─────────────────────────────────────────────┐
        │  compare_modifiable_factors()                │  ← Multi-country comparison
        │  identify_vaccination_gaps()                 │  ← Find vaccination gaps
        │  analyze_nutrition_indicators()              │  ← Nutrition analysis
        │  analyze_healthcare_spending()               │  ← Healthcare spending analysis
        │  analyze_infrastructure_impact()             │  ← Infrastructure analysis
        └─────────────────────────────────────────────┘
                🔬 DOMAIN-SPECIFIC ANALYSIS LAYER
                            ↑ calls
        ┌─────────────────────────────────────────────┐
        │  get_country_trend()        Time series     │
        │  calculate_statistics()     Statistical metrics│
        │  filter_by_region()         Region filter    │
        │  filter_by_year_range()     Year filter      │
        │  filter_by_country()        Country filter   │
        └─────────────────────────────────────────────┘
                📊 BASIC FILTERING LAYER (FOUNDATION)
                            ↑ calls
        ┌─────────────────────────────────────────────┐
        │  get_data_as_dataframe()                     │
        │     SQLite → pandas DataFrame                │
        └─────────────────────────────────────────────┘
                💾 DATA ACCESS LAYER
```

---

## 🔗 Function Call Chains (Simple to Complex)

### **Chain 1: Basic Query (Single Function)**
```
Database → get_data_as_dataframe() → DataFrame
                ↓
    filter_by_country("China") → China's data
```

### **Chain 2: Combined Filters (Multiple Conditions)**
```
Database → get_data_as_dataframe() → DataFrame
                ↓
    filter_by_country("China") → China data
                ↓
    filter_by_year_range(2016, 2017) → China 2016-2017
```

### **Chain 3: Statistical Analysis**
```
Database → get_data_as_dataframe() → DataFrame
                ↓
    filter_by_country("India") → India data
                ↓
    calculate_statistics("life_expect") 
                ↓
    {mean: 68.6, median: 68.6, std: 0.35, ...}
```

### **Chain 4: Domain-Specific Analysis (Policy Focus)**
```
Database → get_data_as_dataframe() → DataFrame
                ↓
    analyze_infrastructure_impact() 
                ↓
    Finding: India water coverage 88-91% < USA 99%
    Recommendation: Prioritize basic_water improvement
```

### **Chain 5: Policy Decision Support (Most Complex)**
```
Database → get_data_as_dataframe() → DataFrame
                ↓
    get_policy_intervention_priorities(
        country="India",
        target_life_expectancy=75.0
    )
                ↓
    Internal calls: filter_by_country("India")
                   analyze_infrastructure_impact()
                   analyze_healthcare_spending()
                   analyze_nutrition_indicators()
                   calculate_statistics()
                ↓
    Output: {
        "current_gap": 6.0 years,
        "top_priorities": [
            "Improve basic_water (88%→95%)",
            "Increase gghe-d (1.2%→3%)",
            "Improve bmi (21.5→23)"
        ],
        "estimated_impact": {
            "basic_water": +2.3 years,
            "gghe-d": +1.8 years,
            "bmi": +1.1 years
        }
    }
```

---

## 📦 Function Groups (Simplified Memory)

### **Group A - Data Preparation (1 function, 3 tests)**
- `get_data_as_dataframe()` ← Starting point for everything

### **Group B - Basic Filtering (4 functions, 13 tests)**
- `filter_by_country()` ← Filter by country name
- `filter_by_year_range()` ← Filter by year range
- `filter_by_region()` ← Filter by region
- **Composable** ← Can be chained together

### **Group C - Basic Analysis (2 functions, 7 tests)**
- `calculate_statistics()` ← Calculate mean, median, std, etc.
- `get_country_trend()` ← View time series trends

### **Group D - Policy Analysis (5 functions, 18 tests)**
- `analyze_infrastructure_impact()` ← Water, sanitation (r=0.831)
- `analyze_healthcare_spending()` ← Healthcare expenditure (r=0.610)
- `analyze_nutrition_indicators()` ← BMI, nutrition (r=0.598)
- `identify_vaccination_gaps()` ← Vaccination coverage gaps
- `compare_modifiable_factors()` ← Multi-country comparison

### **Group E - Decision Support (1 function, 5 tests)**
- `get_policy_intervention_priorities()` ← Ultimate tool
  - Internally calls all above functions

---

## 💡 Conceptual Model: LEGO Building Blocks

Think of the module as building with LEGO blocks:

```
Basic Functions (A+B+C) = LEGO Blocks
↓
Domain Functions (D) = Building Houses with Blocks
↓
Decision Functions (E) = Building Communities with Houses
```

**Only 6 basic functions** exist. Everything else is **composition and application**.

---

## 🎯 Design Philosophy: Modifiable Factors

### **Excluded (Circular Definitions)**
❌ infant_mortality ↔ life_expectancy (correlation by definition)  
❌ adult_mortality ↔ life_expectancy (tautological relationship)  
❌ une_life ↔ life_expectancy (same metric, different source)  

### **Included (Modifiable Policy Factors)**
✅ Infrastructure: `basic_water` (r=0.831), `sanitation_services`  
✅ Healthcare: `gghe-d` (r=0.610), `che_gdp`  
✅ Nutrition: `bmi` (r=0.598), `undernourishment`  
✅ Immunization: `polio`, `diphtheria`, `hepatitis` coverage  

**Rationale**: Enable **actionable policy recommendations** rather than validating obvious relationships.

---

## 📊 Complete Function Reference

### **Layer 1: Data Access**

#### `get_data_as_dataframe(db_path: str) -> pd.DataFrame`
- **Purpose**: Load all health data from SQLite into pandas
- **Implementation**:
  ```python
  records = database_loader.get_all_records(db_path)
  return pd.DataFrame(records)
  ```
- **Tests**: 3 (DataFrame type, column types, path validation)

---

### **Layer 2: Basic Filtering**

#### `filter_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame`
- **Purpose**: Filter by exact country name
- **Implementation**:
  ```python
  return df[df["country"] == country]
  ```
- **Tests**: 4 (exact match, column preservation, empty result, case sensitivity)

#### `filter_by_year_range(df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame`
- **Purpose**: Filter by inclusive year range [start, end]
- **Implementation**:
  ```python
  if start_year > end_year:
      raise ValueError(f"start_year must be <= end_year")
  return df[(df["year"] >= start_year) & (df["year"] <= end_year)]
  ```
- **Tests**: 4 (inclusive range, single year, validation, no matches)

#### `filter_by_region(df: pd.DataFrame, region: str) -> pd.DataFrame`
- **Purpose**: Filter by region name
- **Implementation**:
  ```python
  return df[df["region"] == region]
  ```
- **Tests**: 3 (Asia, Americas, empty result)

#### **Combined Filtering** (Composability)
- **Purpose**: Chain filters for complex queries
- **Implementation**:
  ```python
  china_df = filter_by_country(df, "China")
  result = filter_by_year_range(china_df, 2016, 2017)
  ```
- **Tests**: 2 (country+year, region+year)

---

### **Layer 3: Basic Analysis**

#### `calculate_statistics(df: pd.DataFrame, column: str) -> Dict[str, Any]`
- **Purpose**: Calculate descriptive statistics
- **Implementation**:
  ```python
  if column not in df.columns:
      raise KeyError(f"Column '{column}' not found")
  
  stats = df[column].describe().to_dict()
  # or manually:
  return {
      "mean": df[column].mean(),
      "median": df[column].median(),
      "std": df[column].std(),
      "min": df[column].min(),
      "max": df[column].max(),
      "count": df[column].count()
  }
  ```
- **Tests**: 3 (basic metrics, missing column error, empty DataFrame)

#### `get_country_trend(db_path: str, country: str, metric: str) -> pd.DataFrame`
- **Purpose**: Get time series for a specific country and metric
- **Implementation**:
  ```python
  df = get_data_as_dataframe(db_path)
  country_df = df[df["country"] == country]
  
  if metric not in df.columns:
      raise ValueError(f"Invalid metric: {metric}")
  
  result = country_df[["year", metric]]
  return result.sort_values("year", ascending=True)
  ```
- **Tests**: 4 (time series, sorted by year, metric validation, nonexistent country)

---

### **Layer 4: Domain-Specific Analysis**

#### `analyze_infrastructure_impact(df: pd.DataFrame, infrastructure_vars: Optional[List[str]] = None) -> pd.DataFrame`
- **Purpose**: Analyze infrastructure factors (water, sanitation)
- **Modifiable Factor**: `basic_water` (r=0.831)
- **Implementation**:
  ```python
  vars = infrastructure_vars or ["basic_water", "sanitation_services"]
  
  for var in vars:
      if var not in df.columns:
          raise KeyError(f"Column '{var}' not found")
  
  return df[["country", "year", "region"] + vars]
  ```
- **Tests**: 4 (default variables, custom variables, missing column error, regional differences)

#### `analyze_healthcare_spending(df: pd.DataFrame, region: Optional[str] = None) -> Dict[str, Any]`
- **Purpose**: Analyze healthcare spending effectiveness
- **Modifiable Factor**: `gghe-d` (r=0.610)
- **Implementation**:
  ```python
  if region:
      df = df[df["region"] == region]
  
  country_avg = df.groupby("country")["gghe-d"].mean()
  rankings = country_avg.sort_values(ascending=False)
  
  return {
      "mean_gghe_d": df["gghe-d"].mean(),
      "median_gghe_d": df["gghe-d"].median(),
      "country_rankings": rankings.to_dict()  # or DataFrame
  }
  ```
- **Tests**: 3 (statistics, by region, country rankings)

#### `analyze_nutrition_indicators(df: pd.DataFrame, year_range: Optional[tuple] = None) -> pd.DataFrame`
- **Purpose**: Analyze nutrition-related factors
- **Modifiable Factor**: `bmi` (r=0.598)
- **Implementation**:
  ```python
  if year_range:
      start, end = year_range
      df = df[(df["year"] >= start) & (df["year"] <= end)]
  
  nutrition_cols = ["country", "year", "bmi", "une_pop", "wasting"]
  return df[nutrition_cols]
  ```
- **Tests**: 3 (DataFrame return, year range filter, obesity patterns)

#### `identify_vaccination_gaps(df: pd.DataFrame, threshold: float = 90.0) -> pd.DataFrame`
- **Purpose**: Identify countries below vaccination threshold
- **Modifiable Factor**: Policy-driven immunization coverage
- **Implementation**:
  ```python
  vaccines = ["polio", "diphtheria", "hepatitis"]
  
  # Calculate minimum coverage across all vaccines
  df["min_coverage"] = df[vaccines].min(axis=1)
  
  # Filter below threshold
  gaps = df[df["min_coverage"] < threshold]
  
  # Sort by severity (lowest coverage first)
  return gaps.sort_values("min_coverage", ascending=True)
  ```
- **Tests**: 4 (default threshold, custom threshold, sorted by severity, empty result)

#### `compare_modifiable_factors(df: pd.DataFrame, countries: List[str], factors: Optional[List[str]] = None) -> pd.DataFrame`
- **Purpose**: Compare modifiable factors across countries
- **Implementation**:
  ```python
  # Validate countries exist
  for country in countries:
      if country not in df["country"].values:
          raise ValueError(f"Country '{country}' not found in data")
  
  # Use default top correlated factors if not specified
  factors = factors or ["basic_water", "gghe-d", "bmi", "alcohol"]
  
  # Filter and return
  result = df[df["country"].isin(countries)]
  return result[["country", "year"] + factors]
  ```
- **Tests**: 4 (default factors, custom factors, country validation, multiple years)

---

### **Layer 5: Decision Support**

#### `get_policy_intervention_priorities(df: pd.DataFrame, country: str, target_life_expectancy: float) -> Dict[str, Any]`
- **Purpose**: Recommend policy intervention priorities
- **Implementation**:
  ```python
  # 1. Validate country exists
  if country not in df["country"].values:
      raise ValueError(f"Country '{country}' not found")
  
  # 2. Get current state
  country_df = df[df["country"] == country]
  current_life_exp = country_df["life_expect"].mean()
  
  # 3. Validate target
  if target_life_expectancy <= current_life_exp:
      raise ValueError(f"Target ({target_life_expectancy}) must be above current ({current_life_exp})")
  
  # 4. Calculate gap
  gap = target_life_expectancy - current_life_exp
  
  # 5. Analyze modifiable factors
  infrastructure = analyze_infrastructure_impact(country_df)
  healthcare = analyze_healthcare_spending(country_df)
  nutrition = analyze_nutrition_indicators(country_df)
  
  # 6. Rank priorities by:
  #    - Correlation strength (from correlation analysis)
  #    - Gap to benchmark (compare to top countries)
  #    - Feasibility (policy implementability)
  
  # 7. Estimate impact using correlation coefficients
  priorities = [
      {"factor": "basic_water", "gap": 95 - current_water, "impact": gap_water * 0.831},
      {"factor": "gghe-d", "gap": 5 - current_spending, "impact": gap_spending * 0.610},
      {"factor": "bmi", "gap": 24 - current_bmi, "impact": gap_bmi * 0.598}
  ]
  
  return {
      "current_gap": gap,
      "top_priorities": sorted(priorities, key=lambda x: x["impact"], reverse=True),
      "estimated_impact": {p["factor"]: p["impact"] for p in priorities}
  }
  ```
- **Tests**: 5 (identifies gaps, ranks by impact, estimates impact, validates country, validates target)

---

## 🎓 Use Case Example: Policy Analysis for India

**Scenario**: You're a policy advisor analyzing India's health challenges

### **Step 1: Get Data**
```python
df = get_data_as_dataframe("life_expectancy.db")
```

### **Step 2: Filter to India**
```python
india_df = filter_by_country(df, "India")
```

### **Step 3: View Life Expectancy Trend**
```python
trend = get_country_trend("life_expectancy.db", "India", "life_expect")
# Shows: 68.3 (2015) → 68.6 (2016) → 69.0 (2017)
```

### **Step 4: Calculate Current Statistics**
```python
stats = calculate_statistics(india_df, "life_expect")
# Returns: {mean: 68.6, median: 68.6, std: 0.35, ...}
```

### **Step 5: Domain-Specific Analysis**
```python
# Infrastructure
infra = analyze_infrastructure_impact(india_df)
# Finding: basic_water 88-91% (vs USA 99%)

# Healthcare spending
healthcare = analyze_healthcare_spending(india_df)
# Finding: gghe-d 1.2-1.4% (vs USA 8.3%)

# Vaccination
vax_gaps = identify_vaccination_gaps(india_df, threshold=90.0)
# Finding: polio 85-87% < 90% threshold
```

### **Step 6: Get Policy Recommendations**
```python
priorities = get_policy_intervention_priorities(
    df,
    country="India",
    target_life_expectancy=75.0
)

# Returns:
# {
#     "current_gap": 6.0 years,
#     "top_priorities": [
#         "Improve basic_water (88%→95%) → +2.3 years",
#         "Increase gghe-d (1.2%→3%) → +1.8 years",
#         "Raise polio coverage (87%→95%) → +1.2 years"
#     ]
# }
```

---

## 📈 Test Coverage Summary

| Layer | Functions | Tests | Status |
|-------|-----------|-------|--------|
| Data Access | 1 | 3 | 🔄 RED phase |
| Basic Filtering | 4 | 13 | 🔄 RED phase |
| Basic Analysis | 2 | 7 | 🔄 RED phase |
| Domain Analysis | 5 | 18 | 🔄 RED phase |
| Decision Support | 1 | 5 | 🔄 RED phase |
| **TOTAL** | **12** | **46** | **🔄 RED phase** |

All 46 tests are currently **failing as expected** (RED phase complete). Implementation (GREEN phase) is next.

---

## 🔑 Key Takeaways

1. **Composability**: Basic functions are building blocks, domain functions combine them
2. **Layered Design**: Clear separation between data access, filtering, analysis, and decision support
3. **Policy Focus**: Deliberately exclude circular definitions, focus on modifiable factors
4. **Testability**: Each function has 3-5 tests covering normal cases, edge cases, and error handling
5. **Scalability**: Easy to add new domain-specific analysis functions without changing foundation

---

**For Report Writing**: 
- Use the pyramid diagram to explain architecture
- Reference the use case example to demonstrate practical application
- Cite the design philosophy section to justify excluding circular factors
- Include test coverage table to show comprehensive testing approach

---

*Last Updated*: 18 December 2025  
*Next Step*: Implement functions to make all 46 tests pass (GREEN phase)
