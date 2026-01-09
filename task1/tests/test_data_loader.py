import os
import pytest
from task1.src.data_loader import load_csv

# Get path relative to project root
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
CSV_FILE = os.path.join(DATA_DIR, 'life_expectancy.csv')

def test_load_csv_returns_list():#测试load_csv函数是否返回列表
    """Basic TDD step: loader should always return a list."""
    result = load_csv(CSV_FILE)
    assert isinstance(result, list)#see if the result is a list

def test_load_csv_missing_file():#测试load_csv函数在文件不存在时是否抛出FileNotFoundError异常
    with pytest.raises(FileNotFoundError):
        load_csv(os.path.join(DATA_DIR, "does_not_exist.csv"))#see if FileNotFoundError is raised when file does not exist