import os
import pytest
from task1.data_loader import load_csv

def test_load_csv_returns_list():
    """Basic TDD step: loader should always return a list."""
    result = load_csv("task1/data/life_expectancy.csv")
    assert isinstance(result, list)
