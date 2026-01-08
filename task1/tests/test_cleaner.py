from task1.src.cleaner import clean_numeric, clean_row
import pytest

# ---------------------------------------------------
# Tests for clean_numeric
# ---------------------------------------------------
def test_clean_numeric_valid_value():
    assert clean_numeric("72.5") == 72.5

def test_clean_numeric_missing_value():
    assert clean_numeric("") is None

def test_clean_numeric_invalid_value():
    assert clean_numeric("abc") is None

# ---------------------------------------------------
# Tests for clean_row
# ---------------------------------------------------
def test_clean_row_basic_fields():
    row = {
        "country": "China",
        "country_code": "CHN",
        "region": "Asia",
        "year": "2025",
        "life_expectancy": "99.9",
    }

    cleaned = clean_row(row)

    # String fields should stay as they are
    assert cleaned["country"] == "China"
    assert cleaned["country_code"] == "CHN"
    assert cleaned["region"] == "Asia"

    # year should be cast to int
    assert cleaned["year"] == 2025

    # life_expectancy should be cast to float
    assert cleaned["life_expectancy"] == 99.9


def test_clean_row_missing_numeric_to_none():
    """
    Missing values (e.g. empty strings) should be turned into None by clean_row
    """
    row = {
        "life_expectancy": "",
        "year": "2001",
    }

    cleaned = clean_row(row)

    # Empty numeric fields end up as None
    assert cleaned["life_expectancy"] is None

    # year still converts normally
    assert cleaned["year"] == 2001


def test_clean_row_invalid_numeric_to_none():
    """
    Nonsense numeric input (e.g. 'abc' in "life_expectancy") should be turned into None by clean_row
    """
    row = {
        "life_expectancy": "abc",
        "year": "2001",
    }

    cleaned = clean_row(row)

    # Invalid numeric content ends up as None
    assert cleaned["life_expectancy"] is None

    # year should still convert correctly
    assert cleaned["year"] == 2001


def test_clean_row_all_numeric_fields():
    """
    A representative set of numeric fields should all be standardised to float or None
    """
    row = {
        "life_expect": "50.0",
        "life_exp60": "15.2",
        "adult_mortality": "380.5",
        "infant_mort": "0.14",
        "bmi": "21.7",
        "une_poverty": "",
    }

    cleaned = clean_row(row)

    assert cleaned["life_expect"] == 50.0
    assert cleaned["life_exp60"] == 15.2
    assert cleaned["adult_mortality"] == 380.5
    assert cleaned["infant_mort"] == 0.14
    assert cleaned["bmi"] == 21.7
    assert cleaned["une_poverty"] is None
