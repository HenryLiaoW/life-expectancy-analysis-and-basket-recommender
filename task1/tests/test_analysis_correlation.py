"""
Tests for analysis_correlation.py

Following TDD best practices:
- Test smallest units first (safe_float, pearson_corr)
- Test edge cases (empty data, None values, single point)
- Test integration (run_correlation_analysis with real data)
"""

from task1.src.analysis_correlation import safe_float, pearson_corr, run_correlation_analysis
import pytest
import math


# ---------------------------------------------------
# Tests for safe_float
# ---------------------------------------------------
def test_safe_float_valid_string():
    """Valid numeric string should convert to float."""
    assert safe_float("42.5") == 42.5


def test_safe_float_integer_string():
    """Integer string should convert to float."""
    assert safe_float("100") == 100.0


def test_safe_float_negative():
    """Negative numbers should be handled."""
    assert safe_float("-12.34") == -12.34


def test_safe_float_empty_string():
    """Empty string should return None."""
    assert safe_float("") is None


def test_safe_float_invalid_string():
    """Non-numeric string should return None."""
    assert safe_float("abc") is None


def test_safe_float_none_input():
    """None input should return None."""
    assert safe_float(None) is None


def test_safe_float_already_numeric():
    """Numeric input (int or float) should convert to float."""
    assert safe_float(42) == 42.0
    assert safe_float(3.14) == 3.14


# ---------------------------------------------------
# Tests for pearson_corr
# ---------------------------------------------------
def test_pearson_perfect_positive_correlation():
    """
    Perfect positive correlation: y = x
    Expected r = 1.0
    """
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [1.0, 2.0, 3.0, 4.0, 5.0]
    
    r = pearson_corr(x, y)
    assert r is not None
    assert abs(r - 1.0) < 1e-10  # Close to 1.0


def test_pearson_perfect_negative_correlation():
    """
    Perfect negative correlation: y = -x
    Expected r = -1.0
    """
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [5.0, 4.0, 3.0, 2.0, 1.0]
    
    r = pearson_corr(x, y)
    assert r is not None
    assert abs(r - (-1.0)) < 1e-10  # Close to -1.0


def test_pearson_no_correlation():
    """
    No linear relationship (e.g., horizontal line)
    Expected r ≈ 0
    """
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [5.0, 5.0, 5.0, 5.0, 5.0]  # Constant y
    
    r = pearson_corr(x, y)
    # When one variable has no variance, correlation is undefined
    # Our implementation returns None
    assert r is None


def test_pearson_handles_none_values():
    """
    Correlation should skip None pairs and compute on valid data only.
    """
    x = [1.0, 2.0, None, 4.0, 5.0]
    y = [2.0, 4.0, 6.0, None, 10.0]
    
    # Valid pairs: (1,2), (2,4), (5,10)
    # Perfect correlation y = 2x
    r = pearson_corr(x, y)
    assert r is not None
    assert abs(r - 1.0) < 1e-10


def test_pearson_insufficient_data():
    """
    Less than 2 valid pairs should return None.
    """
    x = [1.0]
    y = [2.0]
    
    r = pearson_corr(x, y)
    assert r is None


def test_pearson_all_none():
    """
    All None values should return None.
    """
    x = [None, None, None]
    y = [None, None, None]
    
    r = pearson_corr(x, y)
    assert r is None


def test_pearson_empty_lists():
    """
    Empty lists should return None.
    """
    r = pearson_corr([], [])
    assert r is None


def test_pearson_realistic_correlation():
    """
    Test with realistic data showing moderate positive correlation.
    """
    # Simulated: higher BMI → slightly higher life expectancy (made-up data)
    x = [22.1, 23.5, 25.0, 26.8, 28.2]  # BMI
    y = [72.0, 73.5, 75.0, 76.2, 77.8]  # Life expectancy
    
    r = pearson_corr(x, y)
    assert r is not None
    assert r > 0.9  # Should be strong positive correlation


# ---------------------------------------------------
# Integration test for run_correlation_analysis
# ---------------------------------------------------
def test_run_correlation_analysis_executes_without_error(tmp_path):
    """
    Integration test: ensure run_correlation_analysis can execute
    with a small synthetic CSV file without crashing.
    
    This validates:
    - CSV loading works
    - Correlation computation works
    - Output formatting works
    """
    # Create a minimal test CSV
    test_csv = tmp_path / "test_data.csv"
    test_csv.write_text(
        "country,year,life_expect,adult_mortality,infant_mort\n"
        "A,2010,75.0,100,10\n"
        "B,2011,76.5,95,9\n"
        "C,2012,78.0,90,8\n"
    )
    
    # Run analysis on test file
    results = run_correlation_analysis(cleaned_path=str(test_csv))
    
    # Should return a list of tuples
    assert isinstance(results, list)
    
    # Should have results for adult_mortality and infant_mort
    # (life_exp60 and others won't be in our test data)
    var_names = [var for var, corr in results]
    assert "adult_mortality" in var_names
    assert "infant_mort" in var_names


def test_pearson_known_calculation():
    """
    Hand-calculated example to verify formula correctness.
    
    Data:
    x = [1, 2, 3]
    y = [2, 4, 5]
    
    Mean x = 2, Mean y = 3.667
    
    Numerator: (1-2)(2-3.667) + (2-2)(4-3.667) + (3-2)(5-3.667)
             = (-1)(-1.667) + 0 + (1)(1.333)
             = 1.667 + 1.333 = 3.0
    
    Den x: sqrt((1-2)^2 + (2-2)^2 + (3-2)^2) = sqrt(1+0+1) = sqrt(2)
    Den y: sqrt((-1.667)^2 + (0.333)^2 + (1.333)^2) ≈ sqrt(4.667) ≈ 2.16
    
    r = 3.0 / (sqrt(2) * 2.16) ≈ 0.981
    """
    x = [1.0, 2.0, 3.0]
    y = [2.0, 4.0, 5.0]
    
    r = pearson_corr(x, y)
    
    assert r is not None
    # Expected r ≈ 0.981 (strong positive)
    assert 0.97 < r < 0.99


# ---------------------------------------------------
# Edge case: Mixed valid and invalid data
# ---------------------------------------------------
def test_pearson_mixed_valid_invalid():
    """
    Mix of valid floats, None, and string representations.
    Only valid pairs should be used.
    """
    x = [1.0, None, 3.0, 4.0]
    y = [2.0, 4.0, None, 8.0]
    
    # Valid pairs: (1, 2), (4, 8)
    # Perfect correlation y = 2x
    r = pearson_corr(x, y)
    assert r is not None
    assert abs(r - 1.0) < 1e-10
