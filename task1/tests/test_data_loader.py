import pytest
from task1.data_loader import load_csv

def test_load_csv_returns_list():
    result = load_csv("data/supermarket.csv")
    assert isinstance(result, list)
