import os
import pytest
from task1.data_loader import load_csv

def test_load_csv_returns_list():#测试load_csv函数是否返回列表
    """Basic TDD step: loader should always return a list."""
    result = load_csv("task1/data/life_expectancy.csv")
    assert isinstance(result, list)#see if the result is a list

def test_load_csv_missing_file():#测试load_csv函数在文件不存在时是否抛出FileNotFoundError异常
    with pytest.raises(FileNotFoundError):
        load_csv("task1/data/does_not_exist.csv")#see if FileNotFoundError is raised when file does not exist