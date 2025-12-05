from task1.cleaner import clean_numeric
import pytest

# in charge of testing CLEAN_NUMERIC function
def test_clean_numeric_valid_value():
    assert clean_numeric("72.5") == 72.5

def test_clean_numeric_missing_value():
    assert clean_numeric("") is None

def test_clean_numeric_invalid_value():
    assert clean_numeric("abc") is None


