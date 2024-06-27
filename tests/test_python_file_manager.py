# tests/test_python_file_manager.py
import pytest
from src.models.python_file_manager import PythonFileManager
from unittest.mock import mock_open, patch

def test_read_file():
    file_manager = PythonFileManager()
    m = mock_open(read_data="print('Hello, World!')")
    with patch('builtins.open', m):
        content = file_manager.read_file('test.py')
    assert content == "print('Hello, World!')"

def test_process_file():
    file_manager = PythonFileManager()
    m = mock_open(read_data="print('Hello, World!')")
    with patch('builtins.open', m):
        content = file_manager.process_file('test.py')
    assert content == "print('Hello, World!')"
