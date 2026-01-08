"""
Data loading utilities for Task 1 (PAI Individual Assignment)

Core principle: Single Responsibility
- This module does ONE thing: load CSV files into dictionaries
- Separation of concerns: loading is independent of cleaning or analysis
- Testability: simple interface makes unit testing straightforward
"""

import csv


def load_csv(path):
    """
    Load a CSV file and return a list of dictionaries.
    
    Each row becomes a dict where keys are column headers.
    This uses Python's built-in csv.DictReader as required by assignment constraints.
    
    Args:
        path (str): Absolute or relative path to the CSV file
        
    Returns:
        list[dict]: List of dictionaries, one per row
        
    Raises:
        FileNotFoundError: If the file does not exist
        csv.Error: If the file is not valid CSV
        
    Example:
        >>> rows = load_csv("data/life_expectancy.csv")
        >>> print(rows[0].keys())
        dict_keys(['country', 'year', 'life_expect', ...])
    """
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
